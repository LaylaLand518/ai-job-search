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

### Identity
- **Name:** Jiaru Liu (Layla)
- **Location:** Berkeley, CA (SF/Bay Area only — no relocation)
- **Languages:** Mandarin (Native), English (Fluent — IELTS 7.0, GMAT 700), French (Advanced), Korean (A2)
- **Status:** Graduated May 2026, actively job searching
- **Salary floor:** $60,000/year minimum

### Education
- **Master in Business Management** (2023–2026) — EDHEC Business School / Sungkyunkwan University / UC Berkeley, Haas School of Business (France, South Korea, US)
  - Track: Global Economy Transformation & Technology
- **BA in International Finance and Market / French** (2019–2023) — University of International Business and Economics, China
  - GPA: 3.6/4.0

### Professional Experience (most recent first)
- **Business Development Associate** (Jun 2026–Present) — AI Data Startup, Remote
- **Marketing & BD Associate** (Jun 2026–Present) — GenAI Assembling, San Francisco
- **User Researcher** (Mar 2026–Apr 2026) — VidaWheel, Remote
- **Fundraising Consultant** (Jan 2026–Mar 2026) — TerraByte, San Francisco
- **Content Marketing Manager, AI Research** (Nov 2025–Present) — Vanta Tech Club, UC Berkeley
- **Outreach Associate** (Oct 2025–May 2026) — Everyone.AI, San Francisco
- **Field Ambassador** (Oct 2025) — Vera Health, San Francisco
- **Outreach Team** (Sept 2025–Nov 2025) — AI Investment Summit 2025 @ UC Berkeley
- **Healthcare Investment Intern** (Jan 2025–Jul 2025) — Yushan Partners, Shanghai
- **Healthcare Investment Intern** (Jul 2024–Dec 2024) — Genesis Partners, Shanghai
- **Z Fellow, AI Research & Content Marketing** (Jul 2024–Present) — Z Potential, Remote
- **VC Investor Relations Associate** (Jul 2022–Jul 2023) — Marathon Venture Partners, Beijing

### Skills
- **Content & Marketing:** Content strategy, editorial calendar, content systems design, short-form video, social media management, organic growth; Ahrefs, Google Search Console, Google Analytics
- **GTM & Research:** Product positioning, messaging, GTM storytelling, user research (12+ interviews), ICP definition, customer journey mapping, competitive analysis, community & event marketing
- **Investment & Finance:** Financial modeling, TAM sizing, market sizing, comparable-company analysis, IC-style investment memos, diligence briefs, founder interviews; familiar with ARR, LTV/CAC, unit economics
- **AI & Automation:** AI product research, agentic frameworks, frontier AI ecosystem (OpenAI, Anthropic, Google), AI prompt engineering, Claude Code, Codex automation
- **Tools:** Microsoft Office, Figma, Python, R, STATA, Wind, Access, CRM

### Behavioral Profile
- **Builder-Analyst** — creates systems and workflows from scratch; combines analytical rigor with high written output
- **Strengths:** Systems thinking, multi-audience translation, parallel operations, AI ecosystem fluency
- **Growth areas:** Depth over breadth when targeting focused roles; AI-fluent operator (not software engineer)
- **Thrives in:** Fast-moving, cross-functional, early-stage environments with output ownership

### What Excites Me
- Learning something new in every role
- Working at the intersection of AI products, research, and real business problems
- Building things that didn't exist before

### Target Sectors (priority order)
- Investment (VC, PE, growth equity, IR)
- GTM / Strategy (AI startups, tech companies)
- Content / AI Research / Editorial

### Deal-breakers
- Roles outside SF/Bay Area (no relocation, no remote-only for non-SF companies unless the role is genuinely interesting)
- Roles below $60,000/year
- No meaningful AI exposure
- Roles that explicitly state they do not sponsor visas (candidate requires visa sponsorship)

## Repo Structure
- `cv/` - LaTeX CV variants
  - `main_example.tex` — master reference (moderncv banking, 2-page)
  - `main_juicebox_gtm_v2.tex` — **canonical V2 template** (BlackRock-style, 1-page, ATS-clean) — use this as the base for all new CVs
- `cover_letters/` - LaTeX cover letters (custom cover.cls template)
- `candidate.json` - Contact info used by apply scripts (gitignored — never commit)
- `.claude/skills/` - AI skill definitions for the application workflow

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
- [ ] CV text layer extracts cleanly - no `(cid:*)` markers, replacement characters, or text visible in the PDF but absent from the extraction
- [ ] Email and phone appear as **literal text** in the extraction
- [ ] Reading order of the extracted text matches the visual order
- [ ] Posting keywords covered or honestly absent - never stuffed
