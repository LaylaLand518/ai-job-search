# ai-job-search

> An end-to-end job application pipeline — discover, rank, tailor, and submit — powered by Claude Code and hardened against the real failure modes of browser automation.

---

## What this is

A job search automation system that runs entirely inside Claude Code. It discovers fresh postings on LinkedIn and Handshake, scores them against your profile, generates a tailored LaTeX CV and insight-driven cover letter for each role, fills the application form using Playwright, and logs every outcome to a tracker CSV — with mandatory human review at three gates before anything is submitted.

---

## The pipeline

```
Phase 1: Discover  →  Phase 2: Rank  →  [GATE 1: approve shortlist]
  →  Phase 3: Tailor  →  [GATE 2: review CV + cover letter]
  →  Phase 4: Apply   →  [GATE 3: confirm final submit]
  →  Phase 5: Track
```

### Phase 1 — Discover
Scrapes LinkedIn Jobs and Handshake for postings from the last 24 hours in the SF Bay Area. Deduplicates against `seen_jobs.json` and `job_search_tracker.csv` so the same role is never processed twice. Uses the Claude-in-Chrome MCP with an authenticated session.

### Phase 2 — Rank
Scores every new posting 0–100 across five dimensions:

| Dimension | Weight |
|-----------|--------|
| Sector fit (Investment > GTM/Strategy > Content/AI Research) | 30 |
| Role fit (day-to-day responsibilities vs. profile) | 30 |
| AI exposure | 20 |
| Location (SF/Oakland/Berkeley = full score) | 10 |
| Salary signal (≥ $60K disclosed = full score) | 10 |

Apply-type bonus: +5 for LinkedIn Easy Apply or Handshake native. −10 for Workday/Oracle (flagged to user; never auto-applied).

### Phase 3 — Tailor

**CV (V2 LaTeX format)**
Every CV is based on `cv/main_juicebox_gtm_v2.tex` — a BlackRock-style, 1-page, ATS-clean article-class template compiled with `lualatex`. The text layer is verified with `pdftotext -layout` to ensure no icon-glyph artifacts and literal contact info. Candidate contact details are read from `candidate.json` (gitignored).

Rules: 2–3 line summary, 6–8 metric bullets starting with strong action verbs, Skills block at bottom, "familiar with" for non-expert tools, US spelling.

**Cover letter (insight-driven framework)**
Every letter is anchored to a specific company insight — a product launch, a strategic inflection, a market moment — not a template. The four-section framework runs before any LaTeX is written:

```
A. Company & Role Insight  →  B. Cover Letter Strategy
  →  C. Final Letter (3 paragraphs, 1–3 bolded phrases)
  →  D. Quality Checklist (Alignment · Authenticity · Action)
```

Compiled with `xelatex` (cover.cls requires fontspec + OpenFonts).

### Phase 4 — Apply

| ATS type | Method |
|----------|--------|
| LinkedIn Easy Apply | Claude-in-Chrome MCP |
| Ashby / Greenhouse / Lever | `apply_ashby.py` (Playwright) |
| Workday / Oracle | Flagged to user — never auto-applied |

For Ashby and external ATS, a Playwright script (`apply_ashby.py`) fills all fields and uploads the CV using `set_input_files()` — no native file picker dialog, no manual step. Gate 3 is a flag file that Claude writes only after the user types `submit` in chat.

### Phase 5 — Track
Every outcome is logged to `job_search_tracker.csv` and `seen_jobs.json`. The tracker is the deduplication source for future runs.

---

## What makes it different

**Insight-driven cover letters, not template-filling.**
Research comes first; the letter argues a specific thesis about why this company, this role, right now. Inspired by [`LaylaLand518/insight-driven-cover-letter-writer`](https://github.com/LaylaLand518/insight-driven-cover-letter-writer).

**ATS-clean LaTeX CVs.**
V2 article-class template. Clean text layer, correct reading order, literal contact info — verified with `pdftotext -layout`. No moderncv icon artifacts.

**Playwright-based file upload.**
`set_input_files()` bypasses the native file picker entirely. Solves the read-tier restriction that prevents computer-use tools from interacting with Chrome's file dialog on Windows.

**Three mandatory human gates.**
Nothing is submitted without approval. No gate can be skipped.

**Hardened against real-world bugs.**
Every known failure mode is documented and solved in the skill definition:

| Bug | Fix |
|-----|-----|
| `\uppercase` uppercases LaTeX color names → undefined color | Use `\MakeUppercase` in before-code |
| lualatex footer shows wrong page count | Run lualatex twice |
| Cover letter bullet font reverts | Move `itemize` outside `\lettercontent{}` |
| `file_upload` rejects local paths | Use Playwright `set_input_files()` |
| Gate file read as `\xef\xbb\xbfsubmit` | Write with `[System.IO.File]::WriteAllText()`, not PowerShell `Out-File` |
| React form fields appear filled but submit empty | Use `nativeInputValueSetter` + `dispatchEvent('input'/'change')` |
| Radio buttons don't register in React | Click the `<label>` element, not the `<input>` |
| Playwright `spawn UNKNOWN` on Windows | Script falls back to system Chrome via `executable_path` |

---

## Technical stack

| Layer | Tool |
|-------|------|
| AI agent | Claude Code (claude-sonnet-4-6) |
| Browser automation | Claude-in-Chrome MCP + Playwright |
| CV typesetting | LaTeX (lualatex) · V2 article class |
| Cover letter | LaTeX (xelatex) · cover.cls · OpenFonts |
| State | `seen_jobs.json` + `job_search_tracker.csv` |
| Skill definitions | `.claude/skills/` SKILL.md files |
| Cross-session memory | `~/.claude/projects/*/memory/` |

---

## Repo structure

```
ai-job-search/
├── CLAUDE.md                          # Candidate profile template — fill in your own background
├── candidate.json                     # Contact info (gitignored — never committed)
├── candidate.json.template            # Copy this to candidate.json and fill in your details
├── cv/
│   ├── main_juicebox_gtm_v2.tex       # Canonical V2 template (base all CVs here)
│   └── main_example.tex               # Master reference (full history)
├── cover_letters/
│   ├── cover.cls                      # Custom cover letter class (xelatex)
│   └── OpenFonts/                     # Lato + Raleway fonts
├── apply_ashby.py                     # Playwright-based Ashby form filler
├── job_search_tracker.csv             # Application log
├── job_scraper/
│   └── seen_jobs.json                 # Deduplication state
└── .claude/skills/
    ├── auto-apply/SKILL.md            # Full pipeline definition
    ├── job-application-assistant/     # CV + cover letter tailoring logic
    └── insight-driven-cover-letter-writer/
```

---

## Setup

**1. Install dependencies**
```bash
pip install playwright
python -m playwright install chromium
```
MiKTeX or TeX Live required for LaTeX. `poppler` optional for ATS text extraction (`pdftotext`).

**2. Configure your profile**

Run `/auto-apply` — Phase 0 will ask for your name, email, phone, LinkedIn URL, location, and salary floor, then save them to `candidate.json` (gitignored). Then fill in your full work history and skills in `CLAUDE.md` (placeholders show exactly what's needed). Alternatively:

```bash
cp candidate.json.template candidate.json
# fill in your details in candidate.json, then edit CLAUDE.md
```

**3. Set your CV base template**

Customise `cv/main_juicebox_gtm_v2.tex`. All new CVs are derived from this file.

**4. Run**
```
/auto-apply            # full pipeline
/auto-apply --dry-run  # discover + rank only (no tailoring or submission)
/auto-apply --from 3   # resume at Phase 3 using already-ranked jobs
```

---

## Inspiration & credits

This project was shaped by open work shared generously by others.

**[`LaylaLand518/insight-driven-cover-letter-writer`](https://github.com/LaylaLand518/insight-driven-cover-letter-writer)**
The cover letter methodology that anchors every letter to a specific company insight. The four-section framework (Company & Role Insight → Strategy → Draft → Quality Checklist) is the backbone of Phase 3's cover letter step.

**[`MadsLorentzen/ai-job-search`](https://github.com/MadsLorentzen/ai-job-search)**
The original repo this project builds on top of.

**[`anthropics/claude-code`](https://github.com/anthropics/claude-code)**
The agentic CLI that makes this pipeline possible — skills, memory, MCP tools, LaTeX, Playwright, and Python all orchestrated locally.

---

*Built with [Claude Code](https://github.com/anthropics/claude-code)*
