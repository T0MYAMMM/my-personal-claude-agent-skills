# Personal Claude Agent Skills — Master Index

Collection of Claude agent skills cloned from across the ecosystem.

- **91 repos cloned** into `vendor/`
- **6,417 SKILL.md files** total
- **824 MB** on disk (depth-1 clones, `.git/` stripped)

Each subdir under `vendor/` is named `<owner>__<repo>/`. Skills live either at the repo root (single-skill repos) or in subfolders like `skills/`, `plugins/<plugin>/skills/`, or `<category>/skills/` (multi-skill repos / plugin marketplaces).

Skill discovery: `find vendor -iname SKILL.md`

---

## 1. Anthropic (Official, First-Party)

The source of truth — production-grade, well-documented.

| Repo | Skills | Path | Notes |
|---|---:|---|---|
| `anthropics__skills` | 18 | `skills/` | Flagship public catalog: docx, pdf, pptx, xlsx, mcp-builder, skill-creator, webapp-testing, claude-api, frontend-design, brand-guidelines, etc. |
| `anthropics__claude-plugins-official` | 28 | `plugins/<plugin>/skills/` | Code review, code-modernization, feature-dev, pr-review-toolkit, security-guidance, mcp-server-dev, agent-sdk-dev, plus LSP plugins for 12+ languages |
| `anthropics__knowledge-work-plugins` | 212 | `<category>/skills/` | engineering (10), data (10), marketing, finance, legal, sales, ops, design, HR, PM, customer-support, enterprise-search, bio-research, small-business |
| `anthropics__claude-for-legal` | 151 | `<practice>/skills/` | Commercial, corporate, employment, privacy, regulatory, AI-governance, IP, litigation legal |
| `anthropics__financial-services` | 117 | `plugins/.../skills/` | Pitch agent, financial-analysis, market-research, GL-reconciliation, KYC screening |
| `anthropics__life-sciences` | 6 | top-level | clinical-trial-protocol, nextflow-development, scvi-tools, single-cell-rna-qc + bio MCPs |
| `anthropics__healthcare` | 3 | top-level | clinical-trial-protocol, fhir-developer, prior-auth-review + healthcare MCPs |
| `anthropics__claude-cookbooks` | 7 | `skills/custom_skills/` | Financial statements, brand guidelines, financial models (Jupyter demos) |

---

## 2. Major Orgs / Vendors

Skills published by company engineering teams.

### Web / Frontend
| Repo | Skills | Notes |
|---|---:|---|
| `vercel-labs__agent-skills` | 9 | React best-practices, Next.js, React Native, view transitions, composition |
| `vercel-labs__next-skills` | 3 | Next.js-focused |
| `vercel-labs__skills` | 1 | `npx skills` cross-agent installer |
| `cloudflare__skills` | 8 | Workers, durable-objects, agents-sdk, wrangler, web-perf, email service |
| `netlify__context-and-tools` | 27 | Deploy, build, edge functions |
| `expo__skills` | 16 | Expo + React Native (deployment, native UI, API routes, dev-client) |
| `remotion-dev__skills` | 1 | Programmatic video creation |

### Infra / Devops
| Repo | Skills | Notes |
|---|---:|---|
| `getsentry__skills` | 27 | Sentry observability + skill-scanner |
| `getsentry__sentry-agent-skills` | 15 | Sister repo |
| `googleworkspace__cli` | 95 | Drive, Sheets, Gmail, Chat, Classroom, Forms, Keep, Calendar, Docs, Slides |
| `microsoft__skills` | 189 | .NET, Python, Java, Rust, TypeScript, Azure SDK grounding |
| `openai__skills` | 44 | Cross-vendor curated skills (incl. Netlify deploy) |

### AI / ML Vendors
| Repo | Skills | Notes |
|---|---:|---|
| `huggingface__skills` | 16 | HF CLI, datasets, Gradio, ML workflows |
| `huggingface__upskill` | 1 | Tool to generate/evaluate skills |
| `fal-ai-community__skills` | 17 | Image/video/3D/audio generation models |
| `replicate__skills` | 7 | Model discovery and execution |
| `google-labs-code__stitch-skills` | 14 | design-md, enhance-prompt, react-components, remotion, shadcn-ui |
| `google-labs-code__jules-skills` | 2 | Jules agent skills |

### Payments / Email / Browser
| Repo | Skills | Notes |
|---|---:|---|
| `stripe__ai` | 9 | Stripe best-practices, projects, upgrade-stripe |
| `resend__resend-skills` | 5 | Send / receive / agent-inbox |
| `resend__email-best-practices` | 1 | Companion content |
| `browserbase__skills` | 14 | Browser automation, scraping, research, cookie-sync, UI-test |

### Security
| Repo | Skills | Notes |
|---|---:|---|
| `trailofbits__skills` | 74 | Audit context, secure contracts, burpsuite, differential review, testing handbook |
| `NVIDIA__SkillSpector` | 23 | Skill security scanner (64 vulnerability patterns) |
| `cisco-ai-defense__skill-scanner` | 19 | Skill security scanner |
| `anikrahman0__security-skill-scanner` | 3 | Skill malicious-pattern scanner |
| `Dilaz__security-review-skill` | 1 | Exploit-driven security review |

---

## 3. Individual Creators — High Signal

| Repo | Skills | Notes |
|---|---:|---|
| `obra__superpowers` | 14 | Jamis Buck's battle-tested set: TDD, debugging, git worktrees, plan/execute |
| `obra__superpowers-skills` | 31 | Community-editable companion |
| `wshobson__agents` | 156 | Will Shobson's massive marketplace (~36k stars) |
| `jezweb__claude-skills` | 65 | Jezweb's 87-skill bundle (Cloudflare, AI/ML, frontend, DB) |
| `obie__skills` | 4 | Obie Fernandez: Rails activity timeline, Tiptap autosave, MCP OAuth, Stimulus |
| `addyosmani__agent-skills` | 23 | Addy Osmani's production engineering skills |
| `alirezarezvani__claude-skills` | 753 | 337-skill mega-bundle (mixed quality, but vast) |
| `Jeffallan__claude-skills` | 66 | Multi-category: languages, backend/frontend, data, ML, devops, security |
| `glebis__claude-skills` | 76 | AI workflow skills |
| `rand__cc-polymath` | 26 | Cloud infra, design, math |
| `mhattingpete__claude-skills-marketplace` | 18 | Git automation, test fixing, PR review |
| `djacobsmeyer__claude-skills-engineering` | 8 | Code review, devops, git, testing |
| `lucianghinda__superpowers-ruby` | 35 | Ruby + Rails superpowers |
| `levnikolaevich__claude-code-skills` | 137 | Agile pipeline, bootstrap, docs, audits, perf |
| `rampstackco__claude-skills` | 204 | 59-skill website-lifecycle library |
| `daymade__claude-code-skills` | 58 | 53-skill marketplace via CCPM |
| `sanjay3290__ai-skills` | 20 | Jules, Postgres, Deep Research, Imagen |
| `affaan-m__everything-claude-code` | 790 | Massive collection incl. AI regression testing |

---

## 4. Domain-Specific

### Code Review / PR / Testing
- `awesome-skills__code-review-skill` (1) — multi-language reviewer (React 19, Vue 3, Rust, TS, TanStack)
- `clear-solutions__unit-tests-skills` (2) — unit test generation
- Plus many under `wshobson__agents`, `obra__superpowers`

### Languages / Frameworks
- `palkan__skills` (1) — layered Rails architecture
- `Kavin-Kannan__rails-best-practices-skill` (1) — Rails best-practices
- `Shoebtamboli__rails_claude_skills` (18) — Rails generator/scaffolder
- `leonardomso__rust-skills` (1) — 179 Rust rules
- `actionbook__rust-skills` (38) — Rust developer assistance
- `laguagu__claude-code-nextjs-skills` (21) — Next.js 16 + AI SDK 6 + pgvector
- `wsimmonds__claude-nextjs-skills` (10) — Next.js with evals

### Data / AI / ML Engineering
- `hamelsmu__evals-skills` (7) — Hamel Husain's eval suite: eval-audit, error-analysis, synthetic-data, judge prompts, RAG eval
- `OmidZamani__dspy-skills` (24) — 22 DSPy skills (signatures, MIPROv2, GEPA, SIMBA, RAG, ReAct)
- `K-Dense-AI__claude-scientific-skills` (143) — 125+ bio/chem/clinical research skills
- `NeoLabHQ__context-engineering-kit` (63) — Prompt engineering, architecture, Kaizen
- `firecrawl__AI-research-SKILLs` (83) — AI research / engineering library
- `chrisvoncsefalvay__claude-d3js-skill` (1) — D3.js interactive viz
- `coffeefuelbump__csv-data-summarizer-claude-skill` (1) — CSV auto-analysis

### DevOps / IaC
- `antonbabenko__terraform-skill` (1) — Anton Babenko's Terraform + OpenTofu (testing, modules, CI/CD)
- `LukasNiessen__kubernetes-skill` (1) — Kubernetes/Helm with KubeShark grounding
- `farmage__opencode-skills` (132) — K8s, Terraform, Docker/CI, Cloud
- `zxkane__aws-skills` (5) — AWS CDK + serverless patterns

### Specialized Tools
- `davidcastagnetoa__skills` (230) — Alembic migrations + many more
- `conorluddy__ios-simulator-skill` (1) — iOS Simulator automation
- `lackeyjb__playwright-skill` (1) — Playwright browser automation
- `jthack__ffuf_claude_skill` (1) — ffuf fuzzing
- `smerchek__claude-epub-skill` (1) — Markdown → EPUB
- `yusufkaraaslan__Skill_Seekers` (2) — Convert doc sites / PDFs into skills
- `forrestchang__andrej-karpathy-skills` (1) — Karpathy coding principles

---

## 5. Marketplaces & Discovery Indexes

These don't ship SKILL.md files themselves — they catalog/link to other skills.

| Repo | Skills | Notes |
|---|---:|---|
| `Lap-Platform__claude-marketplace` | 1537 | 1500+ auto-generated API skills (Stripe, GitHub, Notion, etc.) |
| `ComposioHQ__awesome-claude-skills` | 864 | Curated index, includes skill content |
| `VoltAgent__awesome-agent-skills` | 0 | 1000+ curated skills index (links only) |
| `travisvn__awesome-claude-skills` | 0 | Curated index |
| `karanb192__awesome-claude-skills` | 0 | 50+ verified skills (TDD, debugging, git, docs) |
| `BehiSecc__awesome-claude-skills` | 0 | Skills index with categories |
| `mingrath__awesome-claude-skills` | 0 | Curated list |
| `GetBindu__awesome-claude-code-and-skills` | 0 | Skills + hooks + slash commands + agents |
| `heilcheng__awesome-agent-skills` | 0 | Curated index |
| `hesreallyhim__awesome-claude-code` | 0 | Skills + hooks + slash commands + agents |
| `simonw__claude-skills` | 0 | Simon Willison's mirror of Anthropic's `/mnt/skills` (different filename layout) |

---

## 6. Could Not Clone (Repos Don't Exist)

Hypothesized by research agents but don't have public repos:

- `supabase/skills`, `sanity-io/skills`, `hashicorp/skills`, `tinybirdco/skills`, `clickhouse/skills`, `neon/skills`, `google-gemini/skills` — these orgs do not have public `/skills` repos
- `applied-artificial-intelligence/claude-code-toolkit`, `majiayu000/claude-skill-registry`, `aiskillstore/marketplace` — incorrect name / private / moved

---

## How To Use

### Find a skill by name
```bash
find vendor -iname 'SKILL.md' -path '*<keyword>*'
```

### Find skills by description content
```bash
grep -r --include='SKILL.md' -l 'rag\|retrieval' vendor/
```

### Copy a single skill into your top-level (next to `web-scraping/`)
```bash
cp -r vendor/hamelsmu__evals-skills/skills/eval-audit ./eval-audit
```

### Refresh the catalog
```bash
cd vendor && bash ./_clone.sh
```

### Inspect a repo's structure
```bash
ls vendor/anthropics__skills/skills/
```

---

## Sources / Provenance

All repos were sourced from:
- GitHub `topic:claude-skills`, `topic:claude-code-skills`, `topic:agent-skills` searches
- Anthropic's official catalog and plugin marketplace listings
- 9 "awesome-claude-skills" community curation lists
- Engineering team publications (Vercel, Cloudflare, Stripe, etc.)

Original clone list: `vendor/_repos.txt`. Failures: `vendor/_failed.txt`. Successes: `vendor/_success.txt`. Re-run cloner: `bash vendor/_clone.sh`.
