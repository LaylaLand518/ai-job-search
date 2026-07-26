---
name: auto-apply
description: >
  Full-pipeline job application automation: discover fresh postings on LinkedIn and
  Handshake (last 24 h, target location), rank them against the candidate profile, tailor
  a LaTeX PDF CV and cover letter per role, then auto-fill and submit via Playwright —
  with mandatory human review gates after tailoring and before final submit.
  Triggers on: /auto-apply, auto apply, find and apply, run pipeline
---

# Auto-Apply Pipeline

End-to-end job application pipeline. Profile is always loaded and confirmed before
any job is discovered. All candidate data comes from `CLAUDE.md` and `candidate.json`.

```
Phase 0: Load Profile  →  [GATE 0: confirm understanding]
  →  Phase 1: Discover  →  Phase 2: Rank  →  [GATE 1: approve shortlist]
  →  Phase 3: Tailor    →  [GATE 2: review CV + cover letter]
  →  Phase 4: Apply     →  [GATE 3: confirm final submit]
  →  Phase 5: Track
```

---

## Invocation

```
/auto-apply           — full pipeline, all phases
/auto-apply --dry-run — Phase 0+1+2 only: profile check + discover + rank, no tailoring or submission
/auto-apply --from 3  — resume at Phase 3; still runs Phase 0 to reload profile
```

---

## Phase 0: Load Profile

**Always runs first — even on `--from 3` restarts.** Never skip this phase.

### Step 0.1 — Contact info

Check whether `candidate.json` exists.

**If it does NOT exist**, ask the user:

> "Welcome! Before we start, I need your contact details. I'll ask a few questions —
> answers are saved to `candidate.json` (gitignored, never committed)."

Collect one at a time:
1. **Full name** (as it should appear on applications)
2. **Email address**
3. **Phone number** (format: 1-XXX-XXX-XXXX)
4. **LinkedIn URL**
5. **Location** (city, state — e.g. "Berkeley, CA")
6. **Location constraint** (e.g. "SF/Bay Area only — no relocation")
7. **Salary floor** (minimum, e.g. "$60,000/year")
8. **Target sectors** in priority order (e.g. "Investment, GTM/Strategy, Content/AI Research")
9. **Work authorization** ("authorized to work in US" / "need sponsorship")

Write `candidate.json`:
```json
{
  "name": "<collected>",
  "email": "<collected>",
  "phone": "<collected>",
  "linkedin": "<collected>",
  "location": "<collected>",
  "location_constraint": "<collected>",
  "salary_floor": <number>,
  "target_sectors": ["<sector1>", "<sector2>"],
  "work_authorized": true,
  "needs_sponsorship": true
}
```

**If it exists**, load it silently. Check whether `needs_sponsorship` is present; if missing, ask:
> "Do you currently need visa sponsorship to work in the US? (yes / no)"
and update the file.

### Step 0.2 — Read and check CLAUDE.md

Read the full `CLAUDE.md` file. Scan for unfilled placeholders — any line still
containing `[YOUR_`, `[TITLE]`, `[DATES]`, `[COMPANY]`, `[SKILL`, `[INTEREST`,
`[SECTOR`, `[DEALBREAKER`, etc.

**If placeholders remain:**

> "Your CLAUDE.md still has unfilled sections:
> - [list the specific placeholder lines]
>
> Please fill these in — they're needed to match jobs and write accurate CVs.
> Open CLAUDE.md, complete the placeholders, then type 'ready'."

Wait for 'ready', then re-read CLAUDE.md before continuing.

**If CLAUDE.md is fully filled**, proceed silently to Step 0.3.

### Step 0.3 — Synthesize the profile

Read every section of CLAUDE.md in full. Build a working profile summary covering:

- **Identity**: name, location, language, status, salary floor
- **Education**: degrees, institutions, tracks
- **Experience**: all roles with titles, companies, dates — note the most recent and most relevant to target sectors
- **Skills**: grouped by category; note which are core vs. "familiar with"
- **Behavioral profile**: archetype, strengths, growth areas, preferred environment
- **Motivations**: what excites them, what they care about building
- **Target sectors**: in priority order from candidate.json + CLAUDE.md
- **Deal-breakers**: hard constraints that automatically disqualify a role

Store this as the active **Candidate Profile** for all downstream phases.

### Step 0.4 — Profile confirmation (GATE 0)

Present the synthesized profile to the user:

```
## Candidate Profile — confirmed before search

Name:          <name>
Location:      <city> (<constraint>)
Salary floor:  <floor>
Work auth:     <status>

Experience highlight (most recent):
  • <Role> at <Company> (<dates>) — <1-line summary of what they did>
  • <Role> at <Company> (<dates>) — <1-line summary>
  [top 3–4 most relevant roles]

Core skills:   <comma-separated top skills>
Target sectors (priority order):
  1. <sector>
  2. <sector>
  3. <sector>
Deal-breakers: <list>
Strengths:     <list>
```

Ask:

> "Does this look right? If anything is wrong or missing, tell me now and I'll update
> the profile before searching. Type 'looks good' to start finding jobs."

Wait for confirmation. If the user corrects anything, update CLAUDE.md or candidate.json
accordingly, re-synthesize, and show the updated summary before continuing.

Only after the user confirms does Phase 1 begin.

---

### Step 0.5 — Standard Application Q&A

**Run this step only once** — check `candidate.json` for a `standard_qa` key. If it exists and is fully populated, skip silently.

If `standard_qa` is missing or incomplete, tell the user:

> "Before searching, I'll collect your answers to questions that come up on nearly every application. This saves time when forms have extra fields the script can't auto-fill. I'll ask once and save everything to `candidate.json` (gitignored — never committed)."

Ask each question below in sequence (one at a time). Accept freeform answers.

**Group A — Work eligibility (applies to all roles)**
1. Do you currently need visa sponsorship to work in the US? (yes/no)
2. Are you authorized to work in the US without sponsorship now, or only with sponsorship?

**Group B — Compensation & logistics**
3. What is your salary expectation range? (e.g. "$70,000–$90,000")
4. When could you start if hired today? (notice period / start date)
5. Are you willing to work in-office or hybrid? (yes/no, or describe preference)

**Group C — Sourcing & discovery**
6. How do you typically say you heard about a role? (e.g. "LinkedIn", "Company website", "Referral")

**Group D — Online presence**
7. Do you have a personal website or portfolio URL? (or "none")
8. Do you have a GitHub profile URL? (or "none")

**Group E — EEO / voluntary disclosures** (explain these are voluntary and used only for compliance forms)
9. Gender identity (for EEO forms — e.g. "Female", "Male", "Non-binary", "Prefer not to say")
10. Race/ethnicity (for EEO forms — e.g. "Asian", "Hispanic or Latino", "White", "Prefer not to say")
11. Veteran status (for EEO forms — e.g. "I am not a protected veteran", "Prefer not to say")
12. Disability status (for EEO forms — e.g. "No, I do not have a disability", "Prefer not to say")

**Group F — Boilerplate short answers**
13. In 2–3 sentences, what's your standard answer to "Why are you interested in this role / company?" (a generic version that can be customized per application)
14. In 1–2 sentences, how do you describe your current work situation? (e.g. "I recently completed my master's degree at UC Berkeley Haas and am currently working part-time at an AI startup while actively exploring full-time opportunities.")

Save answers to `candidate.json` under `standard_qa`:

```json
"standard_qa": {
  "needs_sponsorship": true,
  "work_auth_detail": "<collected>",
  "salary_expectation": "<collected>",
  "notice_period": "<collected>",
  "willing_inoffice": "<collected>",
  "how_did_you_hear": "<collected>",
  "website": "<collected or null>",
  "github": "<collected or null>",
  "eeo_gender": "<collected>",
  "eeo_race": "<collected>",
  "eeo_veteran": "<collected>",
  "eeo_disability": "<collected>",
  "why_interested_boilerplate": "<collected>",
  "current_situation": "<collected>"
}
```

When filling application forms in Phase 4, draw on these answers for any non-standard fields before asking the user again.

---

## Phase 1: Discover

**Prerequisite: Phase 0 must be complete and profile confirmed before this phase starts.**

### 1.0 Load state and derive search terms

Read `job_scraper/seen_jobs.json` (create with `{"seen": {}}` if missing).
Read `job_search_tracker.csv` to extract company+title of already-applied roles.

**Derive search queries from the confirmed Candidate Profile (Phase 0):**
- Use the candidate's target sectors as primary search categories
- Pull role-level keywords from their most recent titles and core skills
- Also read `.claude/skills/job-scraper/search-queries.md` for supplemental query ideas
- Location filter: use `location_constraint` from `candidate.json`

Do not use generic or hardcoded search terms. Every query must be grounded in
the specific profile confirmed in Phase 0.

### 1.1 LinkedIn Jobs (Chrome — authenticated session)

Use the `mcp__claude-in-chrome__*` tools with the user's existing logged-in Chrome session.

1. Navigate to LinkedIn Jobs with location filter matching the candidate's target location.
2. For each derived query (Priority 1 sector first, then 2, then 3), search and capture results.
3. Extract: title, company, location, date posted, apply URL.
4. Scroll once (~20 results per query); do not paginate aggressively.
5. WebFetch promising listings for full JD, requirements, salary.

**LinkedIn safety rules:**
- One query at a time. No rapid-fire requests.
- CAPTCHA / login prompt → STOP, record `blocked:linkedin-captcha`, continue with Handshake.
- Never create accounts or bypass gates.

### 1.2 Handshake (Chrome — authenticated session)

1. Navigate to `https://app.joinhandshake.com/stu/postings`
2. Filters: candidate's target location, Last 24 hours, Full-time.
3. Same derived queries. Extract and WebFetch.

### 1.3 Deduplication

Skip if URL or `company:title` already in `seen_jobs.json` or `job_search_tracker.csv`.
Skip if location is outside the candidate's `location_constraint`.
Skip immediately if the role matches any deal-breaker from the Candidate Profile.

### 1.4 Store raw pool

```json
{
  "seen": {
    "<url>": {
      "title": "...", "company": "...", "location": "...", "url": "...",
      "portal": "linkedin|handshake", "apply_url": "...",
      "apply_type": "easy_apply|external|handshake_native",
      "description_snippet": "...", "salary_disclosed": "...|unknown",
      "first_seen": "YYYY-MM-DD", "fit": null, "status": "discovered"
    }
  }
}
```

---

## Phase 2: Rank

Score every newly discovered job against the **Candidate Profile synthesized in Phase 0**.
Do not re-read CLAUDE.md here — use the profile already in context.

### Scoring rubric (0–100)

| Dimension | Weight | What to assess |
|-----------|--------|----------------|
| Sector fit | 30 | How well the role's function maps to the candidate's target sectors (priority order matters) |
| Role fit | 30 | Do the day-to-day responsibilities match the candidate's actual experience and skills? |
| AI exposure | 20 | Does the role genuinely touch AI products, research, or ecosystem (not just mentions AI)? |
| Location | 10 | Matches location_constraint = 10; adjacent area = 6; remote-ok = 8; outside constraint = 0 |
| Salary signal | 10 | Disclosed ≥ salary_floor = 10; undisclosed = 5; disclosed < salary_floor = 0 |

**Apply-type bonus:**
- LinkedIn Easy Apply or Handshake native: +5
- External ATS (Greenhouse, Lever, Ashby): 0
- Workday / Oracle / SuccessFactors: −10 (flag for user)

**Auto-disqualify (score = 0, status: skipped) if:**
- Location violates `location_constraint` AND role is not remote
- Salary explicitly disclosed below `salary_floor`
- Role matches any deal-breaker from the Candidate Profile
- JD explicitly states the company does **not** sponsor visas AND `needs_sponsorship` is true in `candidate.json` — mark as `skipped: no visa sponsorship` and do not present to user

**Verdict bands:**
- Strong (80–100): tailor fully
- Good (65–79): apply, standard tailoring
- Borderline (50–64): flag with explanation; apply only with user confirmation
- Weak (<50): skip with one-line reason

Update `seen_jobs.json` with `rank_score`, `rank_verdict`, `rank_reason`, `rank_date`, `status: ranked`.

### Present ranked table

```
## Job Shortlist — YYYY-MM-DD

Found N new jobs: X strong fit, Y good fit, Z borderline, W skipped.

| # | Score | Verdict | Title | Company | Portal | Apply Type | URL |
|---|-------|---------|-------|---------|--------|------------|-----|

### Why these scores?
For each Strong + Good fit job: 2–3 bullets on what matches, what's a stretch, any red flags.
For Borderline: explicit note on what's uncertain and what to ask the user.
```

**→ GATE 1: Pause.**

Ask:
> "Which numbers do you want to pursue? (e.g. '1 3 4') — or type 'all strong' to take
> all Strong-fit jobs. Borderline jobs need your explicit go-ahead.
> Type 'dry-run done' to stop here if this was a discovery-only run."

Wait for the user's response. Do not tailor or apply to anything without explicit approval.

---

## Phase 3: Tailor

For each approved job, tailor documents one at a time.

### 3.1 CV — LaTeX PDF (V2 format)

**Template:** Always base on `cv/main_juicebox_gtm_v2.tex` (V2 BlackRock-style).
Do NOT use moderncv unless user explicitly requests it.

**V2 format spec:**
- `\documentclass[10pt, letterpaper]{article}` — article class, not moderncv
- Colors: `sectionblue` RGB(28,69,135), `titleblue` RGB(31,107,169)
- `\titleformat{\section}` with `\MakeUppercase` in before-code — **NOT `\uppercase`**
  (using `\uppercase` uppercases the color name `sectionblue` → `SECTIONBLUE` → undefined color error)
- `\entry{Company}{Title}{Location}{Dates}` — inline command, no orphaned headers
- Centered name header; navy CAPS section titles with full-width rule
- `\setlist[itemize]` with tight spacing (itemsep=1.5pt, topsep=2pt)

**Content rules:**
- 2–3 line summary tailored to the role
- 6–8 metric bullets starting with strong action verbs; quantified impact
- Skills block at bottom with ATS keywords
- "familiar with" label for non-expert tools
- US spelling; mirror employer's language

**Compile (always run twice — second pass fixes footer page count):**
```powershell
cd cv
lualatex -interaction=nonstopmode main_<company>_<role>.tex
lualatex -interaction=nonstopmode main_<company>_<role>.tex
```

**1-page rescue sequence (if content spills to page 2):**
1. Reduce `\vspace` between entries from `2pt` to `1pt`
2. Combine weaker bullet pairs into one
3. Shorten summary from 3 lines to 2
4. Add `\enlargethispage{N\baselineskip}` (try N=4 first, increase if needed)
5. Reduce font from 10.5pt to 10pt as last resort

**ATS verification:**
```powershell
pdftotext -layout cv/<Name>_<Company>_<Role>_CV.pdf -
```
Check for: no `(cid:*)` markers, literal email + phone visible, clean reading order.
If pdftotext is missing, skip with a warning and verify from visual PDF read instead.

**Output:** `cv/<LastName>_<Company>_<RoleSlug>_CV.pdf`

---

### 3.2 Cover Letter — LaTeX PDF (insight-driven framework)

**MANDATORY: Always follow the insight-driven-cover-letter-writer framework.**
Never draft without company research first.

#### Step 1 — Research
Fetch the company website (use `mcp__claude-in-chrome__get_page_text` if WebFetch
is broken — it is more reliable for JS-heavy sites). Extract:
- What the product does and who it serves
- Current product launches, expansions, or pivots
- Key metrics or signals of company stage
- Any GTM / market signals relevant to the role

#### Step 2 — Output 4 sections in chat before writing LaTeX:

**A. Company & Role Insight**
- Company stage, product, business context
- What the role is actually solving for RIGHT NOW (not generically)
- The specific challenge or inflection point the hire addresses
- Source all company claims; use cautious language for inferences

**B. Cover Letter Strategy**
- Narrative angle (the one sentence that frames the letter)
- Company insight to reference (specific, not generic)
- Role challenge to name
- Applicant evidence to highlight (2–3 concrete examples from profile)
- Tone calibration
- What to avoid (generic phrases, unchecked company claims)

**C. Final Cover Letter (3 paragraphs)**
- Para 1: Company/role insight → why this moment matters
- Para 2: Applicant evidence → specific, quantified, traceable to real profile
- Para 3: Fit + POV + call to action
- Bold 1–3 high-signal phrases using `\textbf{}`
- Never open with "I am writing to express my strong interest..." or "I am deeply passionate about..."

**D. Quality Checklist**
- Alignment: role responsibilities addressed, company insight specific, ATS keywords mirrored
- Authenticity: all claims traceable to profile, no hallucinated company facts
- Action: clear specific ask in closing

#### LaTeX production rules:

**Template:** `cover_letters/cover_<company>_<role>.tex` based on `cover.cls`

**Compile with xelatex (NOT lualatex — cover.cls uses fontspec):**
```powershell
cd cover_letters
xelatex -interaction=nonstopmode cover_<company>_<role>.tex
```

**Bullet list pattern — bullets MUST go outside `\lettercontent{}`:**
```latex
\lettercontent{Paragraph text here.}
{\raggedright\fontspec[Path = OpenFonts/fonts/raleway/]{Raleway-Medium}%
\fontsize{11pt}{13pt}\selectfont
\begin{itemize}
    \item \textbf{Label}: bullet text
\end{itemize}\par}
\lettercontent{Next paragraph.}
```
⚠️ Never wrap `\begin{itemize}...\end{itemize}` inside `\lettercontent{}` —
the trailing `\\` in that command errors on `\end{itemize}` and the Raleway
font is lost.

**1-page rescue (if cover letter overflows):**
1. Trim bullets from 4 to 3
2. Shorten company paragraph by 1–2 sentences
3. Tighten closing paragraph

**Output:** `cover_letters/<LastName>_<Company>_<RoleSlug>_CoverLetter.pdf`

---

### 3.3 Present for review

Show:
- Fit snapshot (score, verdict, top 3 strengths, top 3 risks)
- Link to CV PDF
- Link to cover letter PDF
- Key ATS keywords included
- Any gaps flagged

**→ GATE 2: Pause. Ask 'apply [#]', 'edit [#]: <instruction>', or 'skip [#]'.**

---

## Phase 4: Apply

### 4.0 Pre-flight

- CV PDF exists and is ≤ 5 MB
- Cover letter PDF exists
- Load candidate contact info from `candidate.json`
- Determine ATS type (Ashby, Greenhouse, Lever, LinkedIn Easy Apply, Workday)

### 4.1 LinkedIn Easy Apply

Use `mcp__claude-in-chrome__*` tools.

Fill fields from `candidate.json`:
- Name, email, phone, LinkedIn URL, location
- Resume: upload CV PDF
- Work auth: use `work_authorized` field from candidate.json

**STOP immediately for:** CAPTCHA, login/2FA, salary field, sponsorship question,
custom essay, employment/income question. Draft answers, show user, wait for approval.

Present pre-submit summary → GATE 3 → user types 'submit' → click Submit.

### 4.2 Handshake Native Apply

Same as 4.1. Typically: resume upload + 1–2 short questions.

### 4.3 Ashby / External ATS — Playwright approach

**Do NOT use the Chrome extension for Ashby file uploads.** Known blockers:
- `mcp__claude-in-chrome__file_upload` only accepts files attached as chat messages —
  local disk paths are rejected with "only files the user has shared with this session"
- Computer-use cannot click in Chrome (Chrome is read-tier — screenshots only)
- A localhost HTTP file server is blocked by Ashby's CSP (`Failed to fetch`)
- The Windows file picker dialog is owned by Chrome (read-tier) — computer-use
  cannot type the path into it

**Use the Playwright script instead:**
```powershell
cd C:\<your-repo>
python apply_ashby.py --url "<ashby_url>" --cv "cv/<Name>_<Company>_<Role>_CV.pdf"
```

The script reads `candidate.json` automatically, then:
1. Launches an isolated Chrome window via Playwright
2. Fills all standard fields using React-safe input injection
3. Uploads the CV via `set_input_files()` — no file picker dialog needed
4. Waits for Gate 3 signal (a flag file)
5. Clicks Submit and verifies confirmation text

**Gate 3 trigger — write the flag file WITHOUT BOM:**
```powershell
[System.IO.File]::WriteAllText("$env:TEMP\ashby_gate3.txt", "submit")
```
⚠️ Never use `Out-File -Encoding utf8` or `| Out-File` — PowerShell 5.1 adds
a UTF-8 BOM, making the string `\xef\xbb\xbfsubmit` which does not equal `"submit"`.

**React form filling (if extending apply_ashby.py or writing new scripts):**
Standard DOM `el.value = x` doesn't trigger React's synthetic events. On Ashby, even
`execCommand('insertText')` fails because the Chrome extension context loses focus.
The only reliable method is calling React's `onChange` prop directly through the fiber:
```javascript
const el = document.getElementById(id);
const fiberKey = Object.keys(el).find(k => k.startsWith('__reactFiber') || k.startsWith('__reactInternalInstance'));
let fiber = el[fiberKey];
while (fiber) {
  const props = fiber.memoizedProps || fiber.pendingProps;
  if (props?.onChange) {
    const proto = el instanceof HTMLTextAreaElement ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
    Object.getOwnPropertyDescriptor(proto, 'value').set.call(el, value);
    props.onChange({ target: el, currentTarget: el, type: 'change', nativeEvent: new Event('change') });
    break;
  }
  fiber = fiber.return;
}
```
This directly updates React's internal state — the only approach that survives Ashby's submit validation.

**Radio buttons in React forms:**
`input[type="radio"].click()` or `form_input(true)` may not register.
Click the associated `<label>` element instead:
```javascript
const yesLabel = Array.from(document.querySelectorAll('label'))
  .find(l => l.textContent.trim() === 'Yes');
if (yesLabel) yesLabel.click();
```

**Prerequisite (one-time setup):**
```powershell
pip install playwright
python -m playwright install chromium
```
If Playwright's managed Chromium fails with `spawn UNKNOWN`, the script automatically
falls back to the system Chrome at `C:\Program Files\Google\Chrome\Application\chrome.exe`.

### 4.4 Greenhouse / Lever

Navigate via Chrome extension. Fill standard fields. For file upload, use the
Playwright pattern from 4.3 adapted to the specific ATS if the Chrome extension
`file_upload` tool fails.

### 4.5 Workday / Oracle / Enterprise ATS

Flag to user: high-friction, requires account creation, multi-step forms.
Do not auto-apply without explicit user confirmation.

### 4.6 Submission confirmation

Confirm by checking for: "Thank you", "Application submitted", "Application sent",
"received", or a confirmation URL (`/thanks`, `/confirmation`, `/submitted`).
A saved-job badge or Easy Apply label is NOT confirmation.
If no confirmation within 15 seconds → record `status: unconfirmed`, report to user.

---

## Phase 5: Track

Append to `job_search_tracker.csv`:

```csv
date,company,title,url,portal,fit_score,cv_path,cover_letter_path,status,notes
YYYY-MM-DD,Company,Title,https://...,ashby,88,cv/Name_Company_Role_CV.pdf,cover_letters/Name_Company_Role_CoverLetter.pdf,submitted,Playwright auto-submit confirmed
```

**Write without BOM:**
```powershell
$row | Add-Content job_search_tracker.csv -Encoding utf8
```

Update `seen_jobs.json` entry to `status: submitted` (or relevant status).

---

## End-of-Run Summary

```
## Auto-Apply Run Summary — YYYY-MM-DD HH:MM

Discovered:  N jobs (LinkedIn: X, Handshake: Y)
Ranked:      N (Strong: X, Good: Y, Borderline: Z, Skipped: W)
Approved:    N jobs by user
Tailored:    N CV + cover letter pairs
Submitted:   N applications confirmed
Blocked:     N (reasons: ...)
Needs user:  N (details: ...)

Next run:    /auto-apply (tomorrow, ~same time)
To review:   open job_search_tracker.csv
```

---

## Known Bugs & Solutions Reference

| Bug | Cause | Fix |
|-----|-------|-----|
| `Undefined color SECTIONBLUE` in CV | `\uppercase` in `\titleformat` uppercases the color name | Use `\MakeUppercase` in the before-code (5th arg), not the format arg |
| CV footer shows wrong page count (1/3 on 2-page doc) | lualatex needs 2 passes to resolve `\pageref{LastPage}` | Always run lualatex twice |
| Cover letter bullet font reverts to default | `\begin{itemize}` wrapped inside `\lettercontent{}` | Move itemize outside; wrap in `{\raggedright\fontspec{Raleway-Medium}...}` |
| `file_upload` rejects local CV path | Tool only accepts files shared as chat attachments | Use `apply_ashby.py` (Playwright `set_input_files()`) |
| File picker dialog not controllable | Chrome is computer-use read-tier; dialog owned by Chrome | Use Playwright — `set_input_files()` never opens a dialog |
| CSP blocks localhost HTTP fetch | Ashby's `Content-Security-Policy` header blocks non-CDN origins | Use Playwright — no browser-side fetch needed |
| Gate file read as `\xef\xbb\xbfsubmit` ≠ `"submit"` | `Out-File -Encoding utf8` adds UTF-8 BOM in PowerShell 5.1 | Use `[System.IO.File]::WriteAllText(path, "submit")` |
| React form fields appear filled but submit "missing entry" | `nativeInputValueSetter` fills DOM but React state stays empty on Ashby | Walk `__reactFiber*` up `.return` chain; call `props.onChange` directly with a full SyntheticEvent-like object (must include `preventDefault`, `stopPropagation`, `isPropagationStopped`, `isDefaultPrevented`, `persist` — omitting them throws `TypeError: e.preventDefault is not a function`) |
| Chrome extension PDF upload: file gets into DOM but Ashby UI doesn't update | Ashby file upload is async (pre-signed S3 URL); `navigator.clipboard.readText()` requires document focus | **Use Playwright** (`apply_ashby.py` / `set_input_files()`) — never fails. Chrome extension clipboard path requires Chrome window to be the active foreground application. |
| Location autocomplete rejects typed value on submit | Ashby location is a geocoder typeahead — needs actual dropdown selection | Type char-by-char (`page.type()` with delay), wait for `[role="option"]`, click first result |
| Radio button click doesn't register in React | `input.click()` may not trigger React's onChange handler | Click the `<label>` element associated with the radio instead |
| Playwright `spawn UNKNOWN` on Windows | Managed Chromium blocked (antivirus / permissions) | Script auto-falls back to system Chrome via `executable_path` |
| `pdftotext` not found | poppler not installed | Skip ATS extraction; verify keywords from visual PDF read instead |
| WebFetch broken on some URLs | Model/routing error | Use `mcp__claude-in-chrome__get_page_text` on the URL instead |
| `candidate.json` not found on script run | First-time setup not completed | Run `/auto-apply` (Phase 0 onboarding) or `cp candidate.json.template candidate.json` |

---

## Hard Rules

1. **Never fabricate.** No invented jobs, companies, credentials, or confirmations.
2. **Never bypass gates.** CAPTCHA, login, 2FA → always a user handoff.
3. **Never submit without Gate 3.** User must type 'submit' in chat first.
4. **Never apply to out-of-scope roles.** Outside location constraint or below salary floor → skip.
5. **No rapid-fire scraping.** One LinkedIn query at a time.
6. **Sponsorship and visa questions always go to the user.**
7. **Salary expectation questions always go to the user.**
8. **Cover letter always uses the insight-driven framework.** No drafting without company research.
9. **CV always uses V2 format.** Base on `cv/main_juicebox_gtm_v2.tex`. Never use moderncv.
10. **Dry run by default on first use** (empty seen_jobs.json + empty tracker).
11. **Never hardcode personal data.** All candidate info comes from `candidate.json` and `CLAUDE.md`.
12. **Profile must be confirmed before any job search.** Phase 0 Gate 0 is mandatory. Never discover or rank jobs with an unconfirmed or placeholder-filled profile.
13. **Search terms come from the profile, not thin air.** Derive all queries from the candidate's confirmed target sectors, titles, and skills. No generic or assumed keywords.
