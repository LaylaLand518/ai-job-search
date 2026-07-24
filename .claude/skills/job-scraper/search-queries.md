# Search Queries for Job Scraper

## Search Sites

Primary:
- **linkedin.com/jobs** — LinkedIn job listings (filter: San Francisco Bay Area)
- **handshake.com** — Handshake (early-career / new grad roles)

Secondary (company career pages via Google):
- Direct Google searches with `site:` filters for target companies

## Query Categories

Queries are grouped by priority. All queries target San Francisco Bay Area unless noted.

### Priority 1: Investment / Finance

Matches the strongest career direction — VC, PE, growth equity, investor relations.

```
site:linkedin.com/jobs "Investment Analyst" "San Francisco"
site:linkedin.com/jobs "VC Analyst" "San Francisco"
site:linkedin.com/jobs "Venture Capital Analyst" "San Francisco"
site:linkedin.com/jobs "Investor Relations" "San Francisco" AI
site:linkedin.com/jobs "Growth Equity Analyst" "San Francisco"
site:linkedin.com/jobs "Investment Associate" "San Francisco" AI
site:handshake.com "Investment Analyst" "San Francisco"
site:handshake.com "Investor Relations" "San Francisco"
```

### Priority 2: GTM / Strategy / Market Intelligence

Matches GTM, strategy, and market research roles at AI startups and tech companies.

```
site:linkedin.com/jobs "GTM Analyst" "San Francisco"
site:linkedin.com/jobs "Market Intelligence" "San Francisco" AI
site:linkedin.com/jobs "Strategy & Operations" "San Francisco" AI
site:linkedin.com/jobs "Business Development" "San Francisco" AI research
site:linkedin.com/jobs "Go-to-Market" "San Francisco" startup
site:handshake.com "GTM" "San Francisco"
site:handshake.com "Strategy" "San Francisco" AI
```

### Priority 3: Content / AI Research / Editorial

AI-focused content, research publishing, and editorial roles.

```
site:linkedin.com/jobs "AI Research" content "San Francisco"
site:linkedin.com/jobs "Content Strategist" AI "San Francisco"
site:linkedin.com/jobs "AI Content" analyst "San Francisco"
site:linkedin.com/jobs "Editorial" AI "San Francisco"
site:handshake.com "Content" AI "San Francisco"
```

### Priority 4: Broader Adjacent Roles

Wider net — product, community, and operations roles at AI companies.

```
site:linkedin.com/jobs "Research Analyst" AI "San Francisco"
site:linkedin.com/jobs "Community Manager" AI "San Francisco"
site:linkedin.com/jobs "Operations Associate" AI startup "San Francisco"
site:linkedin.com/jobs "Product Analyst" AI "San Francisco"
```

## Location Filter

- **Ideal:** San Francisco, Berkeley, Oakland
- **Acceptable:** South Bay (Palo Alto, Mountain View, Menlo Park) with remote flexibility
- **Borderline:** Full in-office South Bay — long BART/Caltrain commute from Berkeley
- **Too far:** LA, NYC, non-Bay Area (remote-only roles are fine from any location)

## Salary Filter

Minimum: $60,000/year. Flag any role below this threshold.

## Date Filter

Only include jobs posted within the last 14 days, or with an application deadline that has not yet passed. If a posting date cannot be determined, include it but flag as "date unknown".

## Adapting Queries

If the user specifies a focus area, select queries from the matching category and generate 2-3 custom queries for that focus. For example:
- `/scrape investment` → Priority 1 queries + custom VC/PE-specific searches
- `/scrape gtm` → Priority 2 queries + startup GTM-specific searches
- `/scrape content` → Priority 3 queries + AI media/editorial searches
