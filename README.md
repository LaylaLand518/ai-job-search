<div align="center">

<h1>🤖 ai-job-search</h1>

<p>
  <strong>An end-to-end job application pipeline — powered by Claude Code.</strong><br>
  Discover roles, rank them against your profile, generate a tailored LaTeX CV and<br>
  insight-driven cover letter, then auto-submit via Playwright. You stay in control<br>
  at every step — three mandatory gates before anything is sent.
</p>

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Powered by Claude Code](https://img.shields.io/badge/Powered%20by-Claude%20Code-D97706)](https://claude.ai/code)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB)](https://python.org)
[![LaTeX](https://img.shields.io/badge/LaTeX-lualatex%20·%20xelatex-008080)](https://www.latex-project.org/)

<img src="claude_animation.gif" alt="Demo" width="700">

</div>

---

## How it works

```
Discover → Rank → [GATE 1] → Tailor → [GATE 2] → Apply → [GATE 3] → Track
```

| Phase | What happens |
|-------|-------------|
| **1 · Discover** | Scrapes LinkedIn & Handshake for today's postings in your target location |
| **2 · Rank** | Scores each role 0–100 across sector fit, role fit, AI exposure, location, and salary |
| **3 · Tailor** | Writes a 1-page ATS-clean LaTeX CV + insight-driven cover letter per role |
| **4 · Apply** | Fills and submits the ATS form via Playwright or LinkedIn Easy Apply |
| **5 · Track** | Logs every outcome to `job_search_tracker.csv` for deduplication and review |

> [!IMPORTANT]
> **Three gates you must pass through.** The pipeline pauses after ranking, after tailoring, and before final submit. Nothing moves forward without you typing approval. Gates cannot be skipped.

---

## What's different

### ✦ Insight-driven cover letters — not templates

Every letter starts with live company research: a product launch, a strategic pivot, a market moment. That insight becomes the thesis. No generic openers. No filler.

```
A. Company & Role Insight  →  B. Strategy  →  C. 3-paragraph letter  →  D. Quality Checklist
```

Inspired by [`LaylaLand518/insight-driven-cover-letter-writer`](https://github.com/LaylaLand518/insight-driven-cover-letter-writer).

### ✦ ATS-clean LaTeX CVs

V2 article-class template compiled with `lualatex`. Text layer verified with `pdftotext -layout` — no icon-glyph artifacts, literal contact info in the text stream, correct reading order. What ATS parsers actually see.

### ✦ Playwright file upload — no manual steps

`set_input_files()` bypasses Chrome's native file picker entirely. Solves the read-tier restriction on Windows where computer-use tools can screenshot Chrome but can't click into it.

### ✦ Zero personal data hardcoded

Your name, email, phone, and LinkedIn live in `candidate.json` (gitignored). The first run asks for everything interactively and saves it. The skill never stores personal data.

---

## Quick start

**1. Install dependencies**

```bash
pip install playwright
python -m playwright install chromium
```

LaTeX: [MiKTeX](https://miktex.org/) or TeX Live · `pdftotext` (poppler) optional but recommended

**2. Set up your profile**

```bash
cp candidate.json.template candidate.json
# fill in your name, email, phone, LinkedIn URL
# then open CLAUDE.md and fill in your work history, skills, and target sectors
```

Or skip this step — running `/auto-apply` triggers an interactive Phase 0 that collects everything and writes `candidate.json` for you.

**3. Run**

```
/auto-apply              # full pipeline — discover, rank, tailor, apply, track
/auto-apply --dry-run    # Phase 1+2 only: see what's out there before committing
/auto-apply --from 3     # resume at tailoring with jobs already ranked
```

---

## Hardened against real-world bugs

Every failure mode hit in production is documented and solved in `.claude/skills/auto-apply/SKILL.md`:

| Bug | Fix |
|-----|-----|
| `\uppercase` in LaTeX titleformat → undefined color `SECTIONBLUE` | Use `\MakeUppercase` in the before-code argument |
| `lualatex` footer page count wrong on first compile | Always run `lualatex` **twice** |
| Cover letter bullet font reverts to default | Put `itemize` **outside** `\lettercontent{}`, wrap in Raleway fontspec block |
| `file_upload` tool rejects local file paths | Use Playwright `set_input_files()` — no dialog involved |
| Gate file reads as `\xef\xbb\xbfsubmit` ≠ `"submit"` | Write with `[System.IO.File]::WriteAllText()`, never PowerShell `Out-File` |
| React form fields appear filled but submit empty | Use `nativeInputValueSetter` + `dispatchEvent('input'/'change')` |
| Radio buttons don't register in React | Click the `<label>` element, not the `<input>` |
| Playwright `spawn UNKNOWN` on Windows | Script auto-falls back to system Chrome via `executable_path` |

---

## Repo structure

```
ai-job-search/
├── CLAUDE.md                    # Your candidate profile — fill in the placeholders
├── candidate.json               # Contact info (gitignored — never committed)
├── candidate.json.template      # Copy this and fill in your details
├── apply_ashby.py               # Playwright form filler for Ashby / external ATS
├── cv/
│   └── main_juicebox_gtm_v2.tex # Canonical V2 CV template — base all new CVs here
├── cover_letters/
│   ├── cover.cls                # Custom cover letter class (xelatex + OpenFonts)
│   └── OpenFonts/               # Lato + Raleway font files
├── job_search_tracker.csv       # Application log + deduplication source
└── .claude/skills/
    ├── auto-apply/SKILL.md      # Full pipeline definition with all bug fixes
    ├── job-application-assistant/
    └── insight-driven-cover-letter-writer/
```

---

## Stack

| Layer | Tool |
|-------|------|
| AI agent | [Claude Code](https://claude.ai/code) (claude-sonnet) |
| Browser automation | Claude-in-Chrome MCP · Playwright |
| CV typesetting | LaTeX · `lualatex` · V2 article class |
| Cover letter | LaTeX · `xelatex` · `cover.cls` · OpenFonts (Lato + Raleway) |
| State management | `seen_jobs.json` · `job_search_tracker.csv` |
| Cross-session memory | `~/.claude/projects/*/memory/` |

---

## Credits

Built on top of **[`MadsLorentzen/ai-job-search`](https://github.com/MadsLorentzen/ai-job-search)** — the original Claude Code job search agent.

Cover letter framework from **[`LaylaLand518/insight-driven-cover-letter-writer`](https://github.com/LaylaLand518/insight-driven-cover-letter-writer)** — anchors every letter to a specific company insight rather than a template.

Made possible by **[`anthropics/claude-code`](https://github.com/anthropics/claude-code)** — the agentic CLI that orchestrates skills, memory, MCP tools, LaTeX, Playwright, and Python all in one local session.

---

<div align="center"><sub>Built with <a href="https://claude.ai/code">Claude Code</a></sub></div>
