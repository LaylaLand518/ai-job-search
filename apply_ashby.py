"""
Ashby application auto-filler using Playwright.
Usage:
    python apply_ashby.py --url <ashby_url> --cv <cv_pdf_path> [--cover-letter <pdf_path>]

Reads candidate contact info from candidate.json (see candidate.json.template).
Fills all standard Ashby fields, uploads the CV without opening a file picker dialog,
then pauses for human review before submitting.

Requires: pip install playwright && python -m playwright install chromium
"""
import argparse
import json
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

# ── Candidate profile (loaded from candidate.json) ────────────────────────────
_profile_path = Path(__file__).parent / "candidate.json"
if not _profile_path.exists():
    sys.exit(
        "\ncandidate.json not found.\n"
        "Run /auto-apply — Phase 0 will guide you through setup, or:\n"
        "  cp candidate.json.template candidate.json\n"
        "  # fill in your details, then re-run\n"
    )

with _profile_path.open(encoding="utf-8") as _f:
    _profile = json.load(_f)

CANDIDATE = {
    "name":     _profile["name"],
    "email":    _profile["email"],
    "phone":    _profile["phone"],
    "linkedin": _profile.get("linkedin", ""),
    "location": _profile.get("location", ""),
}


def fill_ashby(url: str, cv_path: str, cover_letter_path: str | None = None):
    cv = Path(cv_path)
    if not cv.exists():
        sys.exit(f"CV not found: {cv_path}")

    with sync_playwright() as p:
        # Use installed Chrome if Playwright's managed Chromium can't launch
        import os
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        exe = next((c for c in chrome_paths if os.path.exists(c)), None)
        browser = p.chromium.launch(
            headless=False,
            slow_mo=80,
            executable_path=exe,  # None = use managed Chromium
            args=["--disable-blink-features=AutomationControlled"],
        )
        ctx = browser.new_context()
        page = ctx.new_page()

        # Navigate directly to /application sub-page so the form renders immediately
        app_url = url.rstrip("/")
        if not app_url.endswith("/application"):
            app_url += "/application"
        print(f"→ Opening {app_url}")
        page.goto(app_url, wait_until="networkidle")
        page.wait_for_timeout(3000)

        # ── React-safe fill via fiber onChange ───────────────────────────────
        FIBER_FILL_JS = """
(id, val) => {
  const el = document.getElementById(id);
  if (!el) return 'NOT FOUND';
  const fiberKey = Object.keys(el).find(k => k.startsWith('__reactFiber') || k.startsWith('__reactInternalInstance'));
  if (!fiberKey) return 'NO FIBER';
  let fiber = el[fiberKey];
  while (fiber) {
    const props = fiber.memoizedProps || fiber.pendingProps;
    if (props && props.onChange) {
      const proto = el instanceof HTMLTextAreaElement ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
      Object.getOwnPropertyDescriptor(proto, 'value').set.call(el, val);
      props.onChange({ target: el, currentTarget: el, type: 'change', nativeEvent: new Event('change') });
      return 'OK:' + el.value.slice(0, 30);
    }
    fiber = fiber.return;
  }
  return 'NO_ONCHANGE';
}
"""

        def fill_by_label(label_text: str, value: str, input_type: str = "text") -> bool:
            """Find an input by its associated label and fill it via React fiber or direct interaction."""
            import re as _rel
            # Match label text exactly (ignore trailing * for required fields)
            label = page.locator('label').filter(
                has_text=_rel.compile(rf'^\s*{_rel.escape(label_text)}\s*\*?\s*$')
            ).first
            try:
                label.wait_for(state="visible", timeout=3000)
            except Exception:
                # Fallback to substring match
                label = page.locator(f'label:has-text("{label_text}")').first
                try:
                    label.wait_for(state="visible", timeout=2000)
                except Exception:
                    print(f"  ✗ {label_text}: label not found")
                    return False

            input_id = label.get_attribute("for")

            # 1. React fiber fill (preferred — survives submit validation)
            if input_id:
                result = page.evaluate(FIBER_FILL_JS, [input_id, value])
                if result.startswith("OK"):
                    print(f"  ✓ {label_text} (fiber)")
                    return True

                # 2. Direct element interaction by id (type char-by-char triggers React onChange)
                try:
                    inp = page.locator(f'#{input_id}')
                    inp.wait_for(state="visible", timeout=2000)
                    inp.click()
                    inp.fill(value)
                    print(f"  ✓ {label_text} (direct id fill)")
                    return True
                except Exception:
                    pass

            # 3. Label-parent container → descendant input (no generic placeholder fallback)
            try:
                inp = page.locator(f'label:has-text("{label_text}")').locator('xpath=..').locator('input, textarea').first
                inp.wait_for(state="visible", timeout=2000)
                inp.click()
                inp.fill(value)
                print(f"  ✓ {label_text} (parent-container fill)")
                return True
            except Exception:
                pass

            print(f"  ✗ {label_text}: not found")
            return False

        # ── Text fields — try label-based first, placeholder as fallback ─────
        # Name field
        name_filled = (
            fill_by_label("Name", CANDIDATE["name"]) or
            fill_by_label("Full Name", CANDIDATE["name"]) or
            fill_by_label("First Name", CANDIDATE["name"].split()[0])
        )
        if not name_filled:
            # Last resort: first text input
            try:
                page.locator('input[type="text"]').first.fill(CANDIDATE["name"])
                print("  ✓ Name (first text input)")
            except Exception as e:
                print(f"  ✗ Name: {e}")

        fill_by_label("Email", CANDIDATE["email"])
        fill_by_label("Phone", CANDIDATE["phone"]) or fill_by_label("Phone Number", CANDIDATE["phone"])

        # LinkedIn — try label first
        fill_by_label("LinkedIn", CANDIDATE["linkedin"]) or fill_by_label("LinkedIn Profile", CANDIDATE["linkedin"])

        # Location — typeahead field requires typing + selecting from autocomplete dropdown
        def fill_location(value: str) -> bool:
            for label_text in ["Location", "Your location", "Current Location"]:
                label = page.locator(f'label:has-text("{label_text}")').first
                try:
                    label.wait_for(state="visible", timeout=2000)
                    input_id = label.get_attribute("for")
                    loc_input = page.locator(f'#{input_id}') if input_id else page.locator('input[placeholder="Start typing..."]').first
                    loc_input.click()
                    loc_input.fill("")
                    loc_input.type(value, delay=60)  # character-by-character to trigger autocomplete
                    page.wait_for_timeout(1500)
                    # Click first autocomplete suggestion
                    option = page.locator('[role="option"]').first
                    try:
                        option.wait_for(state="visible", timeout=3000)
                        option.click()
                        print(f"  ✓ Location (autocomplete selected)")
                        return True
                    except Exception:
                        # No dropdown — accept typed value as-is
                        loc_input.press("Tab")
                        print(f"  ✓ Location (typed, no dropdown)")
                        return True
                except Exception:
                    continue
            return False

        fill_location(CANDIDATE["location"])

        # ── Yes/No button questions: click every "Yes" button ────────────────
        import re as _re
        # Ashby Yes/No questions use <button> elements (not radio inputs or labels)
        yes_btns = page.locator('button').filter(has_text=_re.compile(r'^\s*Yes\s*$'))
        n_yes = yes_btns.count()
        print(f"  Found {n_yes} 'Yes' button(s)")
        for i in range(n_yes):
            try:
                yes_btns.nth(i).scroll_into_view_if_needed()
                yes_btns.nth(i).click()
                print(f"  ✓ Yes #{i+1}")
                page.wait_for_timeout(300)
            except Exception as e:
                print(f"  ✗ Yes #{i+1}: {e}")

        # ── Resume upload (no file picker — direct injection) ─────────────
        # Find the resume file input (second <input type="file"> on page)
        file_inputs = page.locator('input[type="file"]')
        resume_input = file_inputs.nth(1)
        resume_input.set_input_files(str(cv))
        print(f"✓ CV uploaded: {cv.name}")
        page.wait_for_timeout(1500)

        # ── Cover letter (if field exists and path provided) ───────────────
        if cover_letter_path:
            cl = Path(cover_letter_path)
            if cl.exists():
                cl_label = page.locator('label', has_text="Cover letter")
                if cl_label.count() > 0:
                    cl_inputs = page.locator('input[type="file"]')
                    for i in range(cl_inputs.count()):
                        inp = cl_inputs.nth(i)
                        if inp != resume_input:
                            try:
                                inp.set_input_files(str(cl))
                                print(f"✓ Cover letter uploaded: {cl.name}")
                                break
                            except Exception:
                                pass

        # ── Pre-submit review ─────────────────────────────────────────────
        import tempfile
        gate_file = Path(tempfile.gettempdir()) / "ashby_gate3.txt"
        gate_file.unlink(missing_ok=True)

        print("\n" + "="*60)
        print("READY TO SUBMIT — review the form in the browser window.")
        print(f"Gate 3: write 'submit' or 'cancel' to:\n  {gate_file}")
        print("Waiting up to 10 minutes...")
        print("="*60)

        # Poll for the gate file
        deadline = time.time() + 600
        answer = None
        while time.time() < deadline:
            if gate_file.exists():
                answer = gate_file.read_text(encoding='utf-8-sig').strip().lower()
                gate_file.unlink(missing_ok=True)
                break
            time.sleep(2)

        if answer == "submit":
            submit_btn = page.locator('button:has-text("Submit Application")')
            submit_btn.click()
            print("→ Clicked Submit. Waiting for confirmation...")
            try:
                page.wait_for_selector("text=Thank you", timeout=15000)
                print("✓ Application submitted successfully.")
            except PWTimeout:
                body = page.inner_text("body")
                if any(kw in body.lower() for kw in ["thank you", "submitted", "received", "application"]):
                    print("✓ Confirmation text found — application submitted.")
                else:
                    print("⚠ No confirmation detected. Check the browser window.")
            page.wait_for_timeout(3000)
        elif answer is None:
            print("✗ Timed out waiting for Gate 3 signal.")
        else:
            print("✗ Submission cancelled.")

        browser.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="Ashby application URL")
    ap.add_argument("--cv",  required=True, help="Path to CV PDF")
    ap.add_argument("--cover-letter", default=None, help="Path to cover letter PDF (optional)")
    args = ap.parse_args()
    fill_ashby(args.url, args.cv, args.cover_letter)


if __name__ == "__main__":
    main()
