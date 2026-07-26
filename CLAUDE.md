# Job Application Assistant

## Role
This repo is a job application workspace. Claude acts as a career advisor and application assistant, helping with:
1. **Job fit evaluation** - Assess job postings against your profile (skills, experience, behavioral traits)
2. **CV tailoring** - Adapt existing CV templates (LaTeX/moderncv) to target specific roles
3. **Cover letter writing** - Draft targeted cover letters using the **insight-driven-cover-letter-writer** framework (company research → insight brief → strategy → 3-paragraph letter → quality checklist), rendered in LaTeX (cover.cls, xelatex)
4. **Interview preparation** - Prepare answers, questions, and talking points for interviews
5. **Career strategy** - Advise on positioning and personal branding

## Candidate Profile

> **Contact details (name, email, phone, LinkedIn) live in `candidate.json` — never committed to git.**
> Fill in the rest of this section with your own background. Everything here is the source of truth for CV and cover letter content.
> First-time setup: run `/auto-apply` — Phase 0 will prompt you to create `candidate.json`.

### Identity
- **Name:** [YOUR_FULL_NAME]  ← also in candidate.json
- **Location:** [YOUR_CITY, STATE] ([YOUR_LOCATION_CONSTRAINT, e.g. "SF/Bay Area only — no relocation"])
- **Languages:** [YOUR_LANGUAGES]
- **Status:** [YOUR_STATUS, e.g. "Graduated May 2026, actively job searching"]
- **Salary floor:** [YOUR_SALARY_FLOOR, e.g. "$60,000/year minimum"]

### Education
- **[YOUR_GRADUATE_DEGREE]** ([START]–[END]) — [INSTITUTION(S)]
  - Track / Specialization: [YOUR_TRACK]
- **[YOUR_UNDERGRADUATE_DEGREE]** ([START]–[END]) — [INSTITUTION]
  - GPA: [YOUR_GPA]

### Professional Experience (most recent first)
- **[TITLE]** ([DATES]) — [COMPANY], [LOCATION]
- **[TITLE]** ([DATES]) — [COMPANY], [LOCATION]
- *(add all roles here)*

### Skills
- **[Skill category, e.g. Content & Marketing]:** [skills and tools]
- **[Skill category, e.g. GTM & Research]:** [skills and tools]
- **[Skill category, e.g. AI & Automation]:** [skills and tools]
- *(add all skill categories)*

### Behavioral Profile
- **[YOUR_ARCHETYPE, e.g. "Builder-Analyst"]** — [one-line description]
- **Strengths:** [YOUR_STRENGTHS]
- **Growth areas:** [YOUR_GROWTH_AREAS]
- **Thrives in:** [YOUR_PREFERRED_ENVIRONMENT]

### What Excites You
- [INTEREST_1]
- [INTEREST_2]
- [INTEREST_3]

### Target Sectors (priority order)
- [SECTOR_1, e.g. Investment (VC, PE, growth equity)]
- [SECTOR_2, e.g. GTM / Strategy (AI startups)]
- [SECTOR_3, e.g. Content / AI Research / Editorial]

### Deal-breakers
- [DEALBREAKER_1, e.g. "Roles outside SF/Bay Area"]
- [DEALBREAKER_2, e.g. "Roles below $60,000/year"]
- [DEALBREAKER_3, e.g. "No meaningful AI exposure"]
- [DEALBREAKER_4, e.g. "Roles that explicitly state they do not sponsor visas (if you require visa sponsorship)"]

## Repo Structure
- `cv/` - LaTeX CV variants
  - `main_example.tex` — master reference (moderncv banking, 2-page)
  - `main_juicebox_gtm_v2.tex` — **canonical V2 template** (BlackRock-style, 1-page, ATS-clean) — use this as the base for all new CVs
- `cover_letters/` - LaTeX cover letters (custom cover.cls template)
- `candidate.json` - Contact info used by apply scripts (gitignored — never commit)
- `candidate.json.template` - Template to copy for first-time setup
- `.claude/skills/` - AI skill definitions for the application workflow
- `.agents/skills/` - Job search CLI tools

## Workflow for New Job Applications
1. User provides a job posting (URL or text)
2. **Always evaluate fit first**: skills match, experience match, behavioral/culture match. Present this assessment to the user before proceeding.
3. If good fit: create targeted CV (`cv/main_<company>.tex`) and cover letter (`cover_letters/cover_<company>_<role>.tex`) — **cover letter must follow the insight-driven-cover-letter-writer framework**: (A) Company & Role Insight → (B) Cover Letter Strategy → (C) Final 3-paragraph letter with 1–3 bolded high-signal phrases → (D) Quality Checklist. Never draft without doing company research first.
4. **Verify both documents** (see Verification Checklist below)
5. Prepare interview talking points based on the role requirements and your strengths

**Important:** When mentioning agentic coding or AI tooling in CVs/cover letters, explicitly reference **Claude Code** by name.

## Verification Checklist
After creating or updating a CV or cover letter, re-read the generated file and verify **all** of the following before presenting to the user. Report the results as a pass/fail checklist.

### Factual accuracy
- [ ] All claims match actual profile (CLAUDE.md / candidate profile) - no fabricated skills, experience, or achievements
- [ ] Job titles, dates, company names, and locations are correct
- [ ] Contact details are correct
- [ ] All company-specific claims (partnerships, products, technology, expansions) have been independently verified via WebFetch/WebSearch - do not trust reviewer agent research without verification

### Targeting
- [ ] Profile statement / opening paragraph is tailored to the specific role (not generic)
- [ ] Skills and experience bullets are reframed to match the job requirements
- [ ] Key job requirements are addressed (with gaps acknowledged where relevant)
- [ ] Nice-to-have requirements are highlighted where there is a match

### Consistency
- [ ] CV follows the **V2 format** (BlackRock-style, 1-page, article class): centered name header, navy CAPS sections with rule, `\entry{Company}{Title}{Location}{Dates}` format, Skills block at bottom. Base on `cv/main_juicebox_gtm_v2.tex`. Do NOT use moderncv unless user explicitly requests it.
- [ ] CV content rules: 2–3 line summary, 6–8 metric bullets starting with strong action verbs, Skills section with ATS keywords, "familiar with" label for non-expert tools, US spelling
- [ ] Cover letter uses cover.cls template and insight-driven-cover-letter-writer structure: (A) company research done, (B) strategy documented, (C) 3 paragraphs with 1–3 bolded high-signal phrases, (D) quality checklist passed
- [ ] Tone is consistent across CV and cover letter
- [ ] No contradictions between CV and cover letter content

### Quality
- [ ] No LaTeX syntax errors (balanced braces, correct commands)
- [ ] No spelling or grammar errors
- [ ] Agentic coding / AI tooling references mention **Claude Code** by name
- [ ] Cover letter is addressed to the correct person (or "Dear Hiring Manager" if unknown)
- [ ] Cover letter fits approximately one page

### Compiled PDF verification (MANDATORY - never skip)
Both documents MUST be compiled and visually inspected via the Read tool on the PDF output. "Looks fine in the .tex" is not acceptable - LaTeX page-break decisions are unpredictable. Iterate until these all pass:
- [ ] CV compiled with **lualatex** (V2 article-class template). Cover letter compiled with **xelatex** (cover.cls requires fontspec).
- [ ] **CV is exactly 1 page** — use `\enlargethispage{N\baselineskip}` to rescue content that just barely spills; reduce `\vspace` between entries before reducing font size
- [ ] No orphaned entry headers — V2 uses inline `\entry{}` commands which don't orphan, but verify visually that no entry header line sits alone at bottom of page
- [ ] **Cover letter is exactly 1 page** - signature block must fit with the body, never overflow
- [ ] **Cover letter bullet font matches body font** - `\lettercontent{}` must not wrap `\begin{itemize}...\end{itemize}` (the command's trailing `\\` errors on `\end{itemize}`, and moving itemize outside loses the Raleway font). Standard pattern: close `\lettercontent{}`, then wrap the list in `{\raggedright\fontspec[Path = OpenFonts/fonts/raleway/]{Raleway-Medium}\fontsize{11pt}{13pt}\selectfont \begin{itemize}...\end{itemize}\par}`

### ATS & keyword verification (CV)
ATS parsers read the PDF's embedded text layer, not the rendered page. Extract it with `pdftotext -layout` and verify what a parser sees. `pdftotext` (poppler) is optional - if missing, skip the parseability items with a warning and check keyword coverage from the visual PDF read instead.
- [ ] CV text layer extracts cleanly - no `(cid:*)` markers, `&#65533;` replacement characters, or text visible in the PDF but absent from the extraction
- [ ] Email and phone appear as **literal text** in the extraction (icon-glyph noise like `MOBILE-ALT`/`Envelope` is harmless, but a contact detail carried only by an icon or hyperlink is invisible to ATS)
- [ ] Reading order of the extracted text matches the visual order (single-column stock template is safe; multi-column custom templates are where this breaks)
- [ ] Posting keywords covered or honestly absent - synonym-only matches tightened to the posting's exact term where truthfully applicable, keywords the profile genuinely supports added to experience bullets, genuine gaps left visible and **never stuffed**
