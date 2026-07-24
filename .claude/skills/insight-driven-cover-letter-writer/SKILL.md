# Insight-Driven Cover Letter Writer

## Purpose

Use this skill to write concise, personalized, insight-driven cover letters for specific roles, internships, fellowships, programs, or professional opportunities.

A strong cover letter is **not** a summary of the resume. It should explain:

- Why this company?
- Why this role?
- Why this applicant?
- What does the applicant understand about the company, business, product, market, or role?
- How can the applicant contribute to the company's current priorities?

The goal is to produce a cover letter that feels thoughtful, specific, human, and grounded in real company and role understanding.

---

## Core Principle

Do **not** start by drafting the letter.

First, perform a compact but meaningful analysis of:

1. The company and its business
2. The role and its function
3. The job description's explicit and hidden priorities
4. The company or role-related challenge/opportunity
5. The applicant's most relevant evidence
6. The best narrative angle for the cover letter

Then write a concise application-portal-style cover letter.

The final letter should make the reader feel:

- This applicant understands what we do.
- This applicant understands why this role matters.
- This applicant has relevant experience.
- This applicant has a thoughtful point of view.
- This applicant is worth interviewing.

---

## Required Inputs

Ask for or use the following inputs:

1. Job title
2. Company name
3. Full job description
4. Applicant resume, LinkedIn summary, experience notes, or project notes

If any of these are missing, proceed as far as possible but clearly state what is missing and how that limits the final output.

---

## Optional Inputs

Use these when available:

- Target geography or office location
- Application type, such as internship, full-time role, fellowship, academic program, or partnership opportunity
- Personal motivation or connection to the company
- Specific experiences the applicant wants to highlight
- Experiences the applicant wants to avoid mentioning
- Preferred tone
- Word limit
- Hiring manager name
- Company research links provided by the user
- STAR story bank or project examples
- Existing cover letter draft to improve

Do not assume personal background that is not present in the user-provided materials.

---

## Default Output

Unless the user asks for "final letter only," output four sections:

1. **Company & Role Insight**
2. **Cover Letter Strategy**
3. **Final Cover Letter**
4. **Final Quality Checklist**

The final cover letter should be an **application portal version** by default:

- No mailing address block
- No long formal header
- No "To Whom It May Concern" unless unavoidable
- Usually starts with "Dear Hiring Team," unless a specific recipient is known
- Three concise paragraphs
- Under one page
- Usually 250–400 words

### Final Document Formatting

When producing a final downloadable document or formatted final letter, apply these formatting rules:

- Use **Times New Roman** as the default font.
- Use a professional, clean layout suitable for an application portal or PDF export.
- Bold only the most important high-signal sentences or phrases, especially those that express:
  - the applicant's strongest company insight,
  - the role-related challenge or opportunity,
  - the applicant's most relevant value proposition, or
  - the clearest fit between the applicant and the company's priorities.
- Do not overuse bolding. Usually bold **1–3 short phrases or sentences** across the entire letter.
- Never bold generic enthusiasm, filler, or buzzwords.
- If the output is plain Markdown, use Markdown bold syntax. If the output is a Word/PDF document, apply actual bold formatting.

### Final File Naming Convention

When producing a final downloadable cover letter document, use a clear, consistent, and searchable filename.

Default filename format:

```text
[ApplicantName]_[CompanyName]_[RoleTitle]_CoverLetter_[YYYYMMDD].[ext]
```

Rules:

- Use TitleCase or PascalCase for applicant name, company name, and role title when possible.
- Remove special characters, emojis, slashes, commas, parentheses, and extra punctuation.
- Replace spaces with underscores.
- Keep the filename concise but specific.
- Use the current date in `YYYYMMDD` format.
- Use `.docx` for editable Word documents and `.pdf` only when the user asks for a PDF.
- If the applicant name is unavailable, use `Applicant`.
- If the role title is very long, shorten it to the most recognizable 2–5 words.
- If generating multiple versions, append a short version tag before the date, such as `_Strategic_`, `_Concise_`, `_Formal_`, or `_Final_`.

Examples:

```text
JiaruLiu_Sydecar_BusinessDevelopment_CoverLetter_20260707.docx
Applicant_TikTok_LocalServicesPartnershipManager_CoverLetter_20260707.docx
AlexChen_Stripe_ProductOperations_CoverLetter_Concise_20260707.docx
```

Do not use vague filenames such as `cover_letter.docx`, `final.docx`, `draft.docx`, or `new_document.docx`.

---

## Research Requirement

If web browsing or research tools are available, use them before drafting.

Research is mandatory because this skill is designed to produce a cover letter that reflects deep company and role understanding.

Research should cover, when available:

1. Company website
2. Product or service pages
3. Careers page or team page
4. Recent company news
5. Recent product launches, market expansion, funding, strategy shifts, or leadership commentary
6. Industry context, if directly relevant
7. Competitors or market category, if useful
8. Public information about the specific team or business unit

Prioritize reliable sources:

- Company website
- Company blog
- Product pages
- Careers pages
- Press releases
- Investor relations pages
- Reputable media
- Industry research sources
- Founder or executive interviews
- Official social media only when relevant

If browsing is unavailable, ask the user to provide company research links, company website, product pages, recent news, or other relevant materials. Still proceed using the job description and user-provided materials, but state that company research is limited.

---

## Fact-Checking and Anti-Hallucination Rules

Never invent company facts, metrics, customers, funding, products, strategies, challenges, competitors, or internal priorities.

All company-specific claims must be grounded in at least one of the following:

- Job description
- User-provided materials
- Company website
- Product documentation
- Careers page
- Public news
- Reliable third-party sources

If a company priority or role challenge is inferred rather than directly stated, use cautious language.

Preferred phrasing:

- "The role appears to sit at the intersection of..."
- "Based on the job description, one likely priority is..."
- "A challenge the team may be navigating is..."
- "As the company scales this area, one important question is likely..."
- "This suggests the team is focused on..."

Avoid overconfident or critical phrasing:

- "Your company is struggling with..."
- "The main problem is..."
- "You need to fix..."
- "Your biggest challenge is clearly..."

The final letter should sound informed, respectful, and applicant-level, not presumptuous or consultant-like.

---

## Step 1: Analyze the Job Description

Before writing, analyze the job description.

### A. Identify Role Type

Classify the role into one or more categories:

- Business development
- Partnerships
- Sales
- Growth
- Product management
- Product operations
- Strategy
- Operations
- Marketing
- Content
- Community
- Creator ecosystem
- Finance / investment
- Research
- Data / analytics
- Customer success
- Program management
- Policy / trust and safety
- Other

This classification matters because the narrative angle must change depending on the role.

For example:

- A sales role should emphasize customer understanding, consultative communication, pipeline ownership, and trust-building.
- A strategy role should emphasize structured thinking, market analysis, ambiguity, and decision support.
- A product/growth role should emphasize user insight, adoption, experimentation, and cross-functional execution.
- A content/community role should emphasize audience understanding, platform-native storytelling, trust, and engagement.

### B. Extract Core Responsibilities

Identify the 3–5 responsibilities that define success in the role.

Do not list every responsibility. Prioritize the ones that matter most.

### C. Extract Key Skills

Group the employer's emphasized skills into:

- Functional skills
- Domain knowledge
- Analytical skills
- Communication skills
- Cross-functional skills
- Tools or technical skills
- Leadership or ownership traits

### D. Identify Values and Culture Signals

Look for values implied by the job description, such as:

- Ownership
- Ambiguity tolerance
- Customer obsession
- Creativity
- Operational rigor
- Collaboration
- Speed
- Analytical thinking
- Mission alignment
- Entrepreneurial mindset
- Quality focus

### E. Infer Hidden Priorities

Infer what the company likely cares about most in this hire.

Examples:

- Scaling a new business line
- Improving partner quality
- Building repeatable processes
- Increasing conversion
- Managing a marketplace
- Expanding supply
- Improving creator or merchant experience
- Supporting product adoption
- Building community trust
- Translating strategy into execution
- Improving customer retention

Use cautious language when making inferences.

---

## Step 2: Analyze the Company and Business Context

Create a compact Company & Role Insight Brief.

Answer:

1. What does the company do?
2. What is the company's business model or operating model?
3. Who are its users, customers, partners, or stakeholders?
4. What product, market, or business area is this role connected to?
5. Why might this role matter now?
6. What current company or industry context makes this role important?
7. What challenge, opportunity, or growth lever is most relevant to this role?

Keep this brief concise. The analysis should inform the letter; it should not become the letter.

Recommended length:

- Company business: 2–3 sentences
- Role function: 2–4 bullets
- Key priorities: 3–6 bullets
- Likely challenge/opportunity: 1 short paragraph
- Source basis: concise citations or source notes when possible

---

## Step 3: Identify the Role-Related Challenge or Opportunity

Identify one thoughtful role-related challenge, opportunity, or growth lever that can be naturally referenced in the cover letter.

It should be specific enough to show insight, but not so strong that it sounds like the applicant is criticizing the company.

### Possible Categories

#### Business Challenge

Examples:

- Scaling a new market
- Improving monetization
- Expanding enterprise adoption
- Increasing retention
- Building a stronger go-to-market motion
- Differentiating in a crowded market

#### Product Challenge

Examples:

- Improving user adoption
- Translating user feedback into product iteration
- Reducing friction in the user journey
- Building trust in AI-powered products
- Improving product-market fit

#### Marketplace / Ecosystem Challenge

Examples:

- Balancing supply and demand
- Scaling creators, merchants, partners, or agencies
- Maintaining quality while growing quickly
- Designing incentives
- Building partner enablement systems

#### Operational Challenge

Examples:

- Standardizing workflows
- Improving cross-functional coordination
- Building scalable processes
- Tracking performance
- Managing ambiguity

#### Content / Community Challenge

Examples:

- Creating platform-native content
- Building audience trust
- Translating technical ideas into accessible narratives
- Growing a community without losing quality

#### Strategy / Research Challenge

Examples:

- Understanding market shifts
- Identifying high-quality opportunities
- Turning research into decisions
- Communicating insights to stakeholders

If there is no obvious challenge, frame it as an "opportunity" or "growth lever."

Use respectful phrasing:

- "One opportunity I see is..."
- "One challenge the team may be navigating is..."
- "This role seems especially important because..."
- "As the company scales this area, the ability to... becomes increasingly important."

---

## Step 4: Match Applicant Experience to the Role

Analyze the applicant's resume or experience notes and select only the strongest evidence.

Identify:

1. The applicant's strongest 2–3 fit points for this role
2. The most relevant project, internship, job, or achievement
3. Measurable outcomes, if available
4. Transferable skills that map to the job description
5. A coherent applicant narrative for this specific role

Do not include every resume experience.

A good cover letter should be selective. The chosen evidence should map directly to:

- The company's current priority
- The role's core responsibilities
- The inferred challenge or opportunity
- The applicant's motivation

Avoid weak, unrelated, or filler experiences.

If the resume includes numbers, scale, outcomes, or impact metrics, use 1–2 of them in the cover letter when relevant.

Examples of useful evidence:

- Revenue, conversion, growth, or retention results
- Number of users, customers, partners, creators, contacts, or stakeholders reached
- Size of event, campaign, project, dataset, or market covered
- Efficiency gains
- Research output
- Cross-functional collaboration
- Ownership of ambiguous projects
- High-context communication with sophisticated stakeholders

---

## Step 5: Create the Cover Letter Strategy

Before drafting the final letter, output a short strategy section.

Include:

1. **Recommended narrative angle**
   The central story the cover letter should tell.

2. **Company insight to reference**
   One specific business, product, market, or mission insight.

3. **Role challenge / opportunity to reference**
   One thoughtful observation related to the role.

4. **Applicant evidence to highlight**
   1–2 experiences or achievements.

5. **Tone recommendation**
   Example: concise, thoughtful, energetic, analytical, founder-like, polished, warm, mature, or strategic.

6. **What to avoid**
   Examples: generic passion, resume repetition, overclaiming, unsupported company claims, excessive flattery, or overly casual wording.

---

## Step 6: Draft the Cover Letter

Write the final cover letter in three concise paragraphs.

### Paragraph 1 — Hook + Company / Role Insight

Purpose:

- Name the role
- Show why the applicant is excited
- Demonstrate specific understanding of the company or business
- Introduce the applicant's fit angle

Avoid generic openings such as:

- "I am writing to express my interest..."
- "I have always been passionate about..."
- "Your company is innovative..."

Better structure:

> "I'm excited to apply for [Role] at [Company] because [specific company/business insight]. What especially stands out to me is [role-related opportunity/challenge], which connects closely to my experience in [relevant background]."

### Paragraph 2 — Applicant Value + Evidence

Purpose:

- Highlight 1–2 relevant experiences
- Show concrete contribution
- Connect applicant evidence to the role's priorities
- Complement, not repeat, the resume

Include specific actions and outcomes when available.

Better structure:

> "In [experience], I [action], which helped [result]. That experience strengthened my ability to [skill], a capability I see as especially relevant to this role's focus on [job priority]."

### Paragraph 3 — Fit + Point of View + Call to Action

Purpose:

- Reaffirm interest
- Connect applicant values to the company's mission, culture, or work
- Show enthusiasm for next steps
- End with confidence and warmth

Better structure:

> "I would be excited to bring [skill/perspective] to [Company] as the team continues to [specific goal]. Thank you for your consideration — I'd welcome the opportunity to discuss how my background could support [team/company priority]."

---

## Tone Rules

The cover letter should sound:

- Specific
- Thoughtful
- Concise
- Human
- Confident but not arrogant
- Warm but not overly emotional
- Insight-driven
- Professional
- Motivated
- Authentic

Avoid:

- Generic enthusiasm
- Buzzword-heavy language
- Overly formal phrasing
- Overly casual phrasing
- Repeating resume bullets
- Long paragraphs
- Flattery without substance
- Unsupported company claims
- "Perfect fit" language
- AI-sounding phrases

Avoid phrases such as:

- "I am writing to express my strong interest..."
- "I am deeply passionate about..."
- "In today's fast-paced world..."
- "Your innovative company..."
- "I believe I am the ideal candidate..."
- "My diverse background makes me uniquely qualified..."

Preferred language:

- "What stands out to me is..."
- "I'm especially drawn to..."
- "This role stood out because..."
- "Based on the role description, the team appears focused on..."
- "That experience maps closely to..."
- "I would be excited to contribute to..."

---

## Use Research Without Overloading the Letter

The final cover letter should not read like a research report.

Use research to sharpen the letter, not to overwhelm it.

A strong final letter usually includes:

- One company/business insight
- One role-related challenge or opportunity
- One applicant narrative angle
- One or two pieces of applicant evidence
- One clear call to action

Do not include too many company facts, statistics, product details, or news items.

---

## Role-Type Strategy Guide

Adjust the strategy depending on the role type.

### Business Development / Partnerships

Emphasize:

- Market mapping
- Partner prioritization
- Relationship building
- Outreach strategy
- Commercial judgment
- Ecosystem understanding
- Go-to-market execution
- Stakeholder communication

Likely challenge examples:

- Finding the right partners
- Improving partnership quality
- Scaling outreach without losing personalization
- Translating product value into partner language
- Building repeatable partnership processes

### Sales / Customer Success

Emphasize:

- Customer understanding
- Consultative communication
- Pipeline ownership
- Objection handling
- Relationship management
- Product education
- Trust-building

Likely challenge examples:

- Translating product value into customer outcomes
- Building trust with prospects
- Improving conversion
- Supporting adoption
- Retaining customers

### Product / Growth

Emphasize:

- User insight
- Funnel thinking
- Experimentation
- Product adoption
- Data-informed decisions
- Cross-functional work
- Customer feedback loops

Likely challenge examples:

- Improving activation
- Reducing friction
- Increasing retention
- Translating insights into product changes
- Scaling growth loops

### Content / Community / Creator Ecosystem

Emphasize:

- Audience understanding
- Platform-native storytelling
- Creator or community operations
- Editorial judgment
- Cultural insight
- Engagement strategy
- Trust-building

Likely challenge examples:

- Growing community while maintaining quality
- Building trust
- Creating content that resonates with specific audiences
- Scaling creator participation
- Turning community insight into growth

### Strategy / Operations

Emphasize:

- Structured thinking
- Ambiguity management
- Process design
- Execution
- Cross-functional coordination
- Performance tracking

Likely challenge examples:

- Building scalable systems
- Turning ambiguous goals into workflows
- Improving operational efficiency
- Coordinating stakeholders
- Standardizing best practices

### Finance / Investment / Research

Emphasize:

- Market research
- Analytical judgment
- Investment thesis building
- Synthesis
- Stakeholder communication
- Industry curiosity

Likely challenge examples:

- Identifying high-quality opportunities
- Understanding market shifts
- Communicating complex insights
- Supporting strategic decision-making

### Marketing

Emphasize:

- Audience insight
- Positioning
- Messaging
- Campaign execution
- Content strategy
- Brand understanding
- Performance measurement

Likely challenge examples:

- Differentiating the brand
- Translating product value into compelling messaging
- Reaching the right audience
- Improving campaign performance
- Building trust through content

### Policy / Trust and Safety

Emphasize:

- Judgment
- Research rigor
- Risk assessment
- Stakeholder communication
- Operational consistency
- User trust
- Cross-functional collaboration

Likely challenge examples:

- Balancing safety and product experience
- Scaling review or policy processes
- Maintaining trust
- Translating complex risks into clear policies

---

## Revision Logic

After drafting, self-review and revise once.

Improve:

1. Specificity
2. Company insight
3. Role alignment
4. Applicant evidence
5. Concision
6. Tone
7. Authenticity
8. Fact accuracy

Remove or rewrite:

- Generic sentences
- Resume repetition
- Unsupported claims
- Long explanations
- Vague enthusiasm
- Corporate clichés
- Overly aggressive claims about company problems
- Research details that distract from the applicant's fit

---

## Final Quality Checklist

Before finalizing, check the "3 A's":

### Alignment

Does the letter connect the applicant to the company's mission, role priorities, and key skills?

### Authenticity

Does the letter sound like a real person with specific motivation and experience?

### Action

Does the letter clearly invite an interview, conversation, or next step?

Also check:

- Is the letter under one page?
- Does each paragraph have a clear purpose?
- Does the first paragraph contain a specific company or role insight?
- Does the second paragraph provide applicant-specific evidence?
- Does the third paragraph close with enthusiasm and fit?
- Are company-specific claims grounded?
- Is the tone appropriate for the company?
- Is the writing free of filler and clichés?
- Does the letter avoid sounding like a resume summary?
- Does the letter include a respectful point of view rather than an overconfident diagnosis?

---

## Edge Cases

### If the user provides only a job description and no resume

Create the company and role analysis, then explain that the final cover letter needs applicant experience to be personalized. Provide a structured template or ask for resume/experience notes.

### If the user provides resume but no job description

Ask for the job description or role details. If the user cannot provide them, proceed with a general company/role-based version but state the limitation.

### If browsing is unavailable

Ask the user to provide company website, product page, recent news, team page, or company research. Proceed using available materials and state that research is limited.

### If the company is small or has little public information

Rely more heavily on the job description, company homepage, product description, founder statements, and market category. Avoid overclaiming.

### If the role is vague

Infer the role function from responsibilities and state the inference cautiously.

### If the applicant is a career switcher

Focus on transferable skills, motivation, adjacent evidence, and learning velocity.

### If the applicant is junior

Emphasize learning velocity, ownership, projects, internships, research, content, community work, or demonstrated initiative.

### If the applicant has too much experience

Narrow the story to the 1–2 experiences most relevant to the role.

### If the user asks for a more strategic version

Increase company insight, role-related challenge, and point of view, but keep the tone respectful and avoid sounding like a consultant critique.

### If the user asks for a more personal version

Increase motivation, values, personal connection, and voice, but do not make unsupported emotional claims.

---

## Output Template

Use this template by default.

```markdown
## A. Company & Role Insight

**Company business:**
[2–3 sentence summary of what the company does and how it creates value.]

**Role function:**
[2–4 bullets on where the role sits in the business.]

**Key JD priorities:**
[3–6 bullets.]

**Likely challenge / opportunity:**
[One concise paragraph, using cautious and respectful language.]

**Source basis:**
[Brief source notes or citations, if available.]

---

## B. Cover Letter Strategy

**Recommended narrative angle:**
[One sentence.]

**Company insight to reference:**
[One sentence.]

**Role challenge / opportunity to reference:**
[One sentence.]

**Applicant evidence to highlight:**
[1–2 bullets.]

**Tone:**
[Concise tone recommendation.]

**What to avoid:**
[1–3 bullets.]

---

## C. Final Cover Letter

Formatting requirements for the final letter:

- Font: **Times New Roman** when producing a downloadable or formatted document.
- Bold: **1–3 high-signal phrases or sentences** that best show company insight, role fit, or applicant value.
- Default format: application portal version, unless the user requests a formal letter version.
- Filename for downloadable documents: `[ApplicantName]_[CompanyName]_[RoleTitle]_CoverLetter_[YYYYMMDD].docx` by default.

Dear Hiring Team,

[Paragraph 1: Hook + company / role insight. Bold the strongest company or role insight if it is genuinely specific.]

[Paragraph 2: applicant value + evidence. Bold the clearest applicant value proposition or most relevant achievement if it is strong and specific.]

[Paragraph 3: fit + point of view + call to action. Bold only if there is a concise, high-signal fit statement.]

Best,
[Applicant Name]

---

## D. Final Quality Checklist

- Company-specific: [Pass / Needs work]
- Role-specific: [Pass / Needs work]
- Applicant-specific: [Pass / Needs work]
- Not a resume summary: [Pass / Needs work]
- Authentic tone: [Pass / Needs work]
- Under one page: [Pass / Needs work]
- Times New Roman formatting applied for final document: [Pass / Needs work / Not applicable]
- Key sentences bolded selectively: [Pass / Needs work]
- Final file name follows convention: [Pass / Needs work / Not applicable]
- Fact-checked: [Pass / Needs work]
- Clear next step: [Pass / Needs work]
```

---

## Optional Output Modes

Support these modes when requested:

### Final Letter Only

Output only the final cover letter.

### Formal Letter Version

Include:

- Applicant name
- Email
- Phone
- Date
- Company name
- Hiring manager name, if known
- Formal greeting

### Concise Version

Target 200–250 words.

### More Personal Version

Increase motivation, values, and personal connection.

### More Strategic Version

Increase company insight, business challenge, and point of view.

### More Warm / Human Version

Reduce corporate language and make the tone more natural.

### More Polished / Executive Version

Make the writing more concise, mature, and high-signal.

---

## Success Criteria

A successful output should:

1. Show clear understanding of the company's business.
2. Explain why the role matters.
3. Identify a thoughtful role-related challenge or opportunity.
4. Connect the applicant's experience to that challenge.
5. Sound specific and authentic.
6. Avoid resume repetition.
7. Stay concise.
8. Use confident, natural language.
9. Be grounded in verified information.
10. Make the applicant sound interview-worthy.
