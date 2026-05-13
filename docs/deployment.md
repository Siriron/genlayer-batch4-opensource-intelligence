# Deployment Guide — Batch 4: Open Source Intelligence Suite

## Deployed Contract Addresses

| Contract | Address | Explorer TX |
|---|---|---|
| OpenSourceHealthTracker | `0x57e70e53F642d085B8CA22B17D9b43525BCCe5Be` | https://explorer-studio.genlayer.com/tx/0x2028807374b0a34cbd23704d2faa94bf925bc3d97466a58d706fe6346bf5ad53 |
| DeveloperReputationIndex | `0xfB4E11Be907456035807ce457E59D6C80dC594c9` | https://explorer-studio.genlayer.com/tx/0x793330292e63573e1b8307b611bd624bb9cc6cdc9f46c5750eda4be21046f13e |
| TechStackTrendAnalyzer | `0x9857D3CedCfe87047E664fEb05d88781876FFaa3` | https://explorer-studio.genlayer.com/tx/0x20459aa5e727c2929adc90552e89ae8420301475aece386116f33887845d0147 |

---

## Prerequisites

- Python 3.10+
- `genvm-linter` installed: `pip install genvm-linter`
- Access to GenLayer Studio: https://studio.genlayer.com
- GitHub account

---

## Step 1 — Lint Contracts

Run before deploying. Exit code 0 = pass.

```bash
genvm-lint check OpenSourceHealthTracker.py
genvm-lint check DeveloperReputationIndex.py
genvm-lint check TechStackTrendAnalyzer.py
```

---

## Step 2 — Deploy via GenLayer Studio

For each contract:

1. Go to https://studio.genlayer.com
2. Click **Deploy Contract**
3. Upload the `.py` file directly — do not paste code
4. Select network: **testnet-bradbury**
5. Fill in the **Constructor Input** field `tracker_name` with a label e.g. `repo-tracker`, `dev-index`, `tech-trends`
6. Confirm deployment
7. Copy the Explorer TX URL from https://explorer-studio.genlayer.com

---

## Step 3 — Push to GitHub

### Repo name
```
genlayer-batch4-opensource-intelligence
```

### File structure
```
genlayer-batch4-opensource-intelligence/
├── OpenSourceHealthTracker.py
├── DeveloperReputationIndex.py
├── TechStackTrendAnalyzer.py
├── README.md
└── docs/
    └── deployment.md
```

### Getting commit-specific blob URLs (required for portal)

For each file:
1. Click the file in the repo
2. Click **History** (top right of file view)
3. Click the latest commit
4. Copy the full URL from your browser

Format:
```
https://github.com/Siriron/genlayer-batch4-opensource-intelligence/blob/<COMMIT_HASH>/OpenSourceHealthTracker.py
```

For the repo tree (T&I submission):
```
https://github.com/Siriron/genlayer-batch4-opensource-intelligence/tree/<COMMIT_HASH>
```

---

## Step 4 — Portal Submissions

Submit **6 missions** at https://portal.genlayer.foundation

---

### Submission 1 — OpenSourceHealthTracker (Product & Mission)

**Title:**
```
OpenSourceHealthTracker — Live GitHub Repository Health Scoring on GenLayer
```

**Description:**
```
OpenSourceHealthTracker is a GenLayer Intelligent Contract that tracks and scores the health of multiple GitHub repositories over time using live data and AI reasoning.

For each repository, the contract fetches real-time metadata, recent commits, and open issues directly from the GitHub API. It then uses an LLM to produce a structured health score from 0 to 100, with commit frequency classification, project stage assessment, and a written summary. Every analyze() or refresh() call appends a timestamped snapshot to that repository's history — up to 20 snapshots per repo — enabling health trending over days, weeks, and months.

Key features:
- Multi-record storage: track unlimited repositories in a single contract instance
- 8 write functions: add_repo, analyze, refresh, compare, flag, unflag, archive, add_note
- compare() produces an AI-reasoned head-to-head between any two tracked repos
- No one-shot guard: refresh() can be called repeatedly to build history
- run_nondet_unsafe with tolerance validator for scored outputs

Contract Address: 0x57e70e53F642d085B8CA22B17D9b43525BCCe5Be
Explorer TX: https://explorer-studio.genlayer.com/tx/0x2028807374b0a34cbd23704d2faa94bf925bc3d97466a58d706fe6346bf5ad53
GitHub: https://github.com/Siriron/genlayer-batch4-opensource-intelligence/blob/<COMMIT_HASH>/OpenSourceHealthTracker.py
```

---

### Submission 2 — DeveloperReputationIndex (Product & Mission)

**Title:**
```
DeveloperReputationIndex — AI-Scored GitHub Developer Reputation Tracker on GenLayer
```

**Description:**
```
DeveloperReputationIndex is a GenLayer Intelligent Contract that tracks and scores the professional reputation of multiple GitHub developers over time.

For each developer, the contract fetches their public GitHub profile, recent repositories, and activity events. An LLM then produces a 0–100 reputation score with follower count, total stars earned, primary language, activity level (very_active / active / moderate / low / inactive), and technical specialization (full_stack / backend / frontend / systems / data / devops / mixed). Every analyze() or refresh() call appends a new timestamped snapshot, building a reputation history that shows how a developer's standing evolves.

Key features:
- Multi-record storage: track unlimited developers in a single deployed instance
- 8 write functions: add_developer, analyze, refresh, compare, flag, unflag, archive, add_note
- compare() produces a structured AI comparison with edge categories showing where each developer leads
- No one-shot guard: refresh() builds a growing history per developer
- run_nondet_unsafe with tolerance validator for scored outputs

Contract Address: 0xfB4E11Be907456035807ce457E59D6C80dC594c9
Explorer TX: https://explorer-studio.genlayer.com/tx/0x793330292e63573e1b8307b611bd624bb9cc6cdc9f46c5750eda4be21046f13e
GitHub: https://github.com/Siriron/genlayer-batch4-opensource-intelligence/blob/<COMMIT_HASH>/DeveloperReputationIndex.py
```

---

### Submission 3 — TechStackTrendAnalyzer (Product & Mission)

**Title:**
```
TechStackTrendAnalyzer — Programming Language and Framework Trend Tracker on GenLayer
```

**Description:**
```
TechStackTrendAnalyzer is a GenLayer Intelligent Contract that tracks the adoption momentum of multiple programming languages and frameworks using live GitHub data and LLM reasoning.

For each technology, the contract queries GitHub's search API for repository and topic signals, then uses an LLM to produce a trend score from 0 to 100. Each snapshot includes momentum direction (rising / stable / declining / niche / emerging), maturity level, primary use cases, competing technologies, job market signal, and community health. Repeated refresh() calls build a trend history showing how a technology's momentum shifts over time.

Key features:
- Multi-record storage: track unlimited technologies in one deployed instance
- 8 write functions: add_technology, analyze, refresh, compare, flag, unflag, archive, add_source_url
- compare() advises which technology is stronger for new projects today with AI reasoning
- No one-shot guard: refresh() appends new snapshots indefinitely
- run_nondet_unsafe with tolerance validator for scored outputs

Contract Address: 0x9857D3CedCfe87047E664fEb05d88781876FFaa3
Explorer TX: https://explorer-studio.genlayer.com/tx/0x20459aa5e727c2929adc90552e89ae8420301475aece386116f33887845d0147
GitHub: https://github.com/Siriron/genlayer-batch4-opensource-intelligence/blob/<COMMIT_HASH>/TechStackTrendAnalyzer.py
```

---

### Submission 4 — Full Repo (Tools & Infrastructure)

**Title:**
```
Batch 4 Open Source Intelligence Suite — Full Repository
```

**Description:**
```
Full repository for the GenLayer Batch 4 Open Source Intelligence Suite — three Intelligent Contracts that track GitHub repository health, developer reputation, and technology trend adoption using live web data and AI reasoning.

Repository contains:
- OpenSourceHealthTracker.py — multi-repo health scoring with 8 write functions and snapshot history
- DeveloperReputationIndex.py — multi-developer reputation scoring with 8 write functions and snapshot history
- TechStackTrendAnalyzer.py — multi-technology trend scoring with 8 write functions and snapshot history
- README.md — full documentation with function reference and schema tables
- docs/deployment.md — full deployment and submission guide

All contracts: from genlayer import *, inherit gl.Contract, use run_nondet_unsafe with tolerance validators, support unlimited refresh() calls, maintain multi-record TreeMap storage with up to 20 snapshots per entity.

GitHub Repo: https://github.com/Siriron/genlayer-batch4-opensource-intelligence/tree/<COMMIT_HASH>
```

---

### Submission 5 — README (Documentation)

**Title:**
```
Batch 4 README — Open Source Intelligence Suite Contract Documentation
```

**Description:**
```
Full README documentation for the GenLayer Batch 4 Open Source Intelligence Suite.

Covers all three deployed contracts with complete function references, snapshot field schemas, contract addresses, explorer TX links, architecture overview, and technical compliance checklist.

Contracts documented:
- OpenSourceHealthTracker (0x57e70e53F642d085B8CA22B17D9b43525BCCe5Be)
- DeveloperReputationIndex (0xfB4E11Be907456035807ce457E59D6C80dC594c9)
- TechStackTrendAnalyzer (0x9857D3CedCfe87047E664fEb05d88781876FFaa3)

GitHub README: https://github.com/Siriron/genlayer-batch4-opensource-intelligence/blob/<COMMIT_HASH>/README.md
```

---

### Submission 6 — Deployment Guide (Documentation)

**Title:**
```
Batch 4 Deployment Guide — Open Source Intelligence Suite
```

**Description:**
```
Full deployment and portal submission guide for the GenLayer Batch 4 Open Source Intelligence Suite.

Covers linting with genvm-linter, deployment via GenLayer Studio with constructor input instructions, GitHub repo setup with commit-specific URL retrieval, and all 6 portal submission titles and full descriptions.

Deployed contract addresses:
- OpenSourceHealthTracker: 0x57e70e53F642d085B8CA22B17D9b43525BCCe5Be
- DeveloperReputationIndex: 0xfB4E11Be907456035807ce457E59D6C80dC594c9
- TechStackTrendAnalyzer: 0x9857D3CedCfe87047E664fEb05d88781876FFaa3

GitHub deployment guide: https://github.com/Siriron/genlayer-batch4-opensource-intelligence/blob/<COMMIT_HASH>/docs/deployment.md
```

---

## Notes

- Replace `<COMMIT_HASH>` in all URLs with the actual commit hash after pushing to GitHub
- All three contracts use `run_nondet_unsafe` — validators will show multiple rounds in Studio explorer; this is expected behavior
- The `compare()` function requires both entities to have at least one snapshot before calling
- GitHub public API is used unauthenticated — space out `analyze()` calls slightly during testing to avoid rate limits
- Constructor input `tracker_name` can be any descriptive string — it labels the deployed instance
