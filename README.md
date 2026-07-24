<div align="center">

<h1>✈️ ApplyPilot</h1>

<p>
  <strong>An end-to-end job application pipeline — powered by Claude Code.</strong><br>
  Learns your background first, then discovers roles, ranks them against your profile,<br>
  generates a tailored LaTeX CV and insight-driven cover letter, and auto-submits via<br>
  Playwright. You're the pilot — four human gates keep you in command at every step.
</p>

<p>
  <strong>端到端求职自动化流水线 — 由 Claude Code 驱动。</strong><br>
  先深度理解你的背景，再发现职位、按画像打分、生成定制 LaTeX 简历和洞察驱动的求职信，<br>
  最后通过 Playwright 自动提交。你是机长——四个人工关卡让你全程掌控。
</p>

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Powered by Claude Code](https://img.shields.io/badge/Powered%20by-Claude%20Code-D97706)](https://claude.ai/code)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB)](https://python.org)
[![LaTeX](https://img.shields.io/badge/LaTeX-lualatex%20·%20xelatex-008080)](https://www.latex-project.org/)

<img src="claude_animation.gif" alt="Demo" width="700">

<br>

**[English](#how-it-works)** · **[中文](#工作原理)**

</div>

---

## How it works

```
Load Profile → [GATE 0] → Discover → Rank → [GATE 1] → Tailor → [GATE 2] → Apply → [GATE 3] → Track
```

| Phase | What happens |
|-------|-------------|
| **0 · Load Profile** | Reads `candidate.json` + `CLAUDE.md`, checks for unfilled placeholders, synthesizes your full background into a working profile |
| **1 · Discover** | Searches LinkedIn & Handshake using queries derived from your confirmed profile — sectors, titles, and skills |
| **2 · Rank** | Scores each role 0–100 across sector fit, role fit, AI exposure, location, and salary — against the profile loaded in Phase 0 |
| **3 · Tailor** | Writes a 1-page ATS-clean LaTeX CV + insight-driven cover letter per role |
| **4 · Apply** | Fills and submits the ATS form via Playwright or LinkedIn Easy Apply |
| **5 · Track** | Logs every outcome to `job_search_tracker.csv` for deduplication and review |

> [!IMPORTANT]
> **Four gates you must pass through.** Gate 0 confirms your profile before any search begins. Gates 1–3 gate the shortlist, the documents, and the final submit. Nothing moves forward without you typing approval. Gates cannot be skipped.

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

Or skip this — running `/auto-apply` triggers an interactive Phase 0 that collects everything, writes `candidate.json`, and walks you through confirming your profile before any search begins.

**3. Run**

```
/auto-apply              # full pipeline — profile check, discover, rank, tailor, apply, track
/auto-apply --dry-run    # profile check + discover + rank only, no tailoring or submission
/auto-apply --from 3     # resume at tailoring — still runs Phase 0 to reload the profile
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
ApplyPilot/
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
---

## 工作原理

```
加载画像 → [关卡 0] → 发现职位 → 评分排名 → [关卡 1] → 定制材料 → [关卡 2] → 投递申请 → [关卡 3] → 追踪记录
```

| 阶段 | 具体内容 |
|------|---------|
| **0 · 加载画像** | 读取 `candidate.json` 和 `CLAUDE.md`，检查未填写的占位符，将你的完整背景综合为工作画像 |
| **1 · 发现职位** | 根据确认后的画像（目标行业、职位名称、核心技能）生成搜索词，抓取 LinkedIn 和 Handshake 当天职位 |
| **2 · 评分排名** | 基于第 0 阶段加载的画像，从行业匹配、岗位契合、AI 曝光度、地点、薪资五个维度打分（满分 100）|
| **3 · 定制材料** | 为每个职位生成 1 页 ATS 兼容的 LaTeX 简历 + 洞察驱动的求职信 |
| **4 · 投递申请** | 通过 Playwright 或 LinkedIn Easy Apply 自动填写并提交申请表单 |
| **5 · 追踪记录** | 将所有结果写入 `job_search_tracker.csv`，用于去重和后续回顾 |

> [!IMPORTANT]
> **四个必须经过的人工关卡。** 关卡 0 在任何搜索开始前确认你的画像；关卡 1–3 分别把守候选名单、申请材料和最终提交。不输入确认，流程不会推进。关卡不可跳过。

---

## 有何不同

### ✦ 洞察驱动的求职信 — 而非套模板

每封信都从实时公司调研开始：一次产品发布、一个战略转折、一个市场时机。这个洞察就是信件的核心论点。没有千篇一律的开场白，没有废话填充。

```
A. 公司与职位洞察  →  B. 写作策略  →  C. 三段式正文（1–3 个加粗关键句）  →  D. 质量清单
```

灵感来自 [`LaylaLand518/insight-driven-cover-letter-writer`](https://github.com/LaylaLand518/insight-driven-cover-letter-writer)。

### ✦ ATS 兼容的 LaTeX 简历

V2 article 模板，使用 `lualatex` 编译。通过 `pdftotext -layout` 验证文字层——无图标乱码，联系方式以纯文本存储，文字顺序正确。这才是 ATS 解析器真正读到的内容。

### ✦ Playwright 文件上传 — 无需任何手动操作

`set_input_files()` 完全绕过 Chrome 的系统文件选择框。解决了 Windows 上 computer-use 工具只能截图 Chrome 但无法点击操作的限制。

### ✦ 零个人信息硬编码

姓名、邮箱、电话、LinkedIn 均存储在 `candidate.json`（已加入 .gitignore，不会提交）。首次运行时交互式收集并保存，skill 文件本身不存储任何个人数据。

---

## 快速开始

**1. 安装依赖**

```bash
pip install playwright
python -m playwright install chromium
```

LaTeX：[MiKTeX](https://miktex.org/) 或 TeX Live · `pdftotext`（poppler）可选但推荐安装

**2. 配置个人档案**

```bash
cp candidate.json.template candidate.json
# 填入姓名、邮箱、电话、LinkedIn 链接
# 再打开 CLAUDE.md，填入工作经历、技能和目标岗位方向
```

也可以跳过这一步——直接运行 `/auto-apply`，Phase 0 会交互式引导你完成所有配置、生成 `candidate.json`，并在任何搜索开始前确认你的画像。

**3. 运行**

```
/auto-apply              # 完整流水线 — 画像确认、发现、排名、定制、投递、追踪
/auto-apply --dry-run    # 画像确认 + 发现 + 排名，不进行定制或提交
/auto-apply --from 3     # 从第 3 阶段恢复，但仍会重新加载画像
```

---

## 针对真实 Bug 的修复

所有在实际使用中踩过的坑都记录在 `.claude/skills/auto-apply/SKILL.md` 中：

| Bug | 修复方案 |
|-----|---------|
| LaTeX `\uppercase` 将颜色名大写 → 颜色 `SECTIONBLUE` 未定义 | 在 `\titleformat` 的 before-code 参数中使用 `\MakeUppercase` |
| `lualatex` 首次编译页脚页码错误 | 始终运行 **两次** `lualatex` |
| 求职信列表字体恢复默认 | 将 `itemize` 放在 `\lettercontent{}` **外部**，用 Raleway fontspec 块包裹 |
| `file_upload` 工具拒绝本地文件路径 | 使用 Playwright `set_input_files()`，完全不涉及文件对话框 |
| 关卡文件被读取为 `\xef\xbb\xbfsubmit` ≠ `"submit"` | 使用 `[System.IO.File]::WriteAllText()` 写入，禁用 PowerShell `Out-File` |
| React 表单字段看似已填写但提交为空 | 使用 `nativeInputValueSetter` + `dispatchEvent('input'/'change')` |
| React 单选按钮点击无效 | 点击 `<label>` 元素，而非 `<input>` 本身 |
| Windows 上 Playwright `spawn UNKNOWN` | 脚本自动回退至系统 Chrome，通过 `executable_path` 指定 |

---

## 目录结构

```
ApplyPilot/
├── CLAUDE.md                    # 候选人档案模板 — 填入你自己的内容
├── candidate.json               # 联系方式（已加入 .gitignore，不会提交）
├── candidate.json.template      # 复制此文件并填入你的信息
├── apply_ashby.py               # 适用于 Ashby 等外部 ATS 的 Playwright 表单填写脚本
├── cv/
│   └── main_juicebox_gtm_v2.tex # V2 简历规范模板 — 所有新简历的基础
├── cover_letters/
│   ├── cover.cls                # 自定义求职信模板类（xelatex + OpenFonts）
│   └── OpenFonts/               # Lato + Raleway 字体文件
├── job_search_tracker.csv       # 申请记录 + 去重数据源
└── .claude/skills/
    ├── auto-apply/SKILL.md      # 完整流水线定义及所有 Bug 修复
    ├── job-application-assistant/
    └── insight-driven-cover-letter-writer/
```

---

## 技术栈

| 层级 | 工具 |
|------|------|
| AI 代理 | [Claude Code](https://claude.ai/code)（claude-sonnet）|
| 浏览器自动化 | Claude-in-Chrome MCP · Playwright |
| 简历排版 | LaTeX · `lualatex` · V2 article 模板 |
| 求职信 | LaTeX · `xelatex` · `cover.cls` · OpenFonts（Lato + Raleway）|
| 状态管理 | `seen_jobs.json` · `job_search_tracker.csv` |
| 跨会话记忆 | `~/.claude/projects/*/memory/` |

---

## 致谢

基于 **[`MadsLorentzen/ai-job-search`](https://github.com/MadsLorentzen/ai-job-search)** 构建 — 原始 Claude Code 求职代理项目。

求职信框架来自 **[`LaylaLand518/insight-driven-cover-letter-writer`](https://github.com/LaylaLand518/insight-driven-cover-letter-writer)** — 让每封信都锚定具体的公司洞察，而非套用模板。

由 **[`anthropics/claude-code`](https://github.com/anthropics/claude-code)** 驱动 — 这个 agentic CLI 将 skill、记忆、MCP 工具、LaTeX、Playwright 和 Python 整合在一个本地会话中协同运作。

---

<div align="center"><sub>Built with <a href="https://claude.ai/code">Claude Code</a></sub></div>
