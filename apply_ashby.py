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
        )
        ctx = browser.new_context()
        page = ctx.new_page()

        print(f"→ Opening {url}")
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(1500)

        # ── Text fields ──────────────────────────────────────────────────────
        def fill(placeholder: str, value: str):
            loc = page.locator(f'input[placeholder="{placeholder}"]').first
            loc.fill(value)

        fill("Type here...",        CANDIDATE["name"])
        fill("hello@example.com...", CANDIDATE["email"])
        fill("1-415-555-1234...",   CANDIDATE["phone"])

        # LinkedIn is the second "Type here..." input
        text_inputs = page.locator('input[type="text"]')
        count = text_inputs.count()
        if count >= 2:
            text_inputs.nth(1).fill(CANDIDATE["linkedin"])

        # ── Radio: SF Bay Area → Yes ──────────────────────────────────────
        try:
            yes_label = page.locator('label', has_text="Yes").first
            yes_label.click()
        except Exception:
            radios = page.locator('input[type="radio"]')
            if radios.count() > 0:
                radios.first.click()

        # ── Button: 5 days/week → Yes ─────────────────────────────────────
        try:
            yes_btn = page.locator('button', has_text="Yes").first
            yes_btn.click()
        except Exception:
            pass

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
        print("Waiting up to 5 minutes...")
        print("="*60)

        # Poll for the gate file
        deadline = time.time() + 300
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
