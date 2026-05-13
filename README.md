# GenLayer Intelligent Contracts — Batch 4: Open Source Intelligence Suite

A suite of three Intelligent Contracts deployed on GenLayer testnet that track, analyze, and compare open source ecosystems using live web data and AI reasoning. Each contract maintains multi-record storage with timestamped historical snapshots — enabling trend analysis over time, not just one-shot results.

---

## Deployed Contracts

| Contract | Address | Explorer |
|---|---|---|
| OpenSourceHealthTracker | `0x57e70e53F642d085B8CA22B17D9b43525BCCe5Be` | [TX Link](https://explorer-studio.genlayer.com/tx/0x2028807374b0a34cbd23704d2faa94bf925bc3d97466a58d706fe6346bf5ad53) |
| DeveloperReputationIndex | `0xfB4E11Be907456035807ce457E59D6C80dC594c9` | [TX Link](https://explorer-studio.genlayer.com/tx/0x793330292e63573e1b8307b611bd624bb9cc6cdc9f46c5750eda4be21046f13e) |
| TechStackTrendAnalyzer | `0x9857D3CedCfe87047E664fEb05d88781876FFaa3` | [TX Link](https://explorer-studio.genlayer.com/tx/0x20459aa5e727c2929adc90552e89ae8420301475aece386116f33887845d0147) |

---

## Contracts

### 1. OpenSourceHealthTracker

**Contract Address:** `0x57e70e53F642d085B8CA22B17D9b43525BCCe5Be`
**Deploy TX:** https://explorer-studio.genlayer.com/tx/0x2028807374b0a34cbd23704d2faa94bf925bc3d97466a58d706fe6346bf5ad53

Tracks the health of multiple GitHub repositories over time. For each repository, it fetches live metadata, recent commits, and open issues from the GitHub API, then uses LLM analysis to produce a structured health score from 0 to 100. Every `analyze()` or `refresh()` call appends a new timestamped snapshot, enabling health trending across days, weeks, and months.

**Write functions:**
- `add_repo(owner, name)` — register a new repository for tracking
- `analyze(owner, name)` — fetch live GitHub data and produce a new health snapshot
- `refresh(owner, name)` — re-run analysis and append a new snapshot
- `compare(owner_a, name_a, owner_b, name_b)` — AI head-to-head comparison of two repos
- `flag(owner, name)` — mark a repo as flagged for attention
- `unflag(owner, name)` — remove flag from a repo
- `archive(owner, name)` — mark a repo as archived
- `add_note(owner, name, note)` — attach a text note to a repo record

**View functions:**
- `get_repo(owner, name)` — full record and complete snapshot history
- `get_all_repos()` — all tracked repositories
- `get_snapshots(owner, name)` — all snapshots for a specific repo
- `get_latest(owner, name)` — most recent snapshot only

**Snapshot fields per analysis:**

| Field | Type | Description |
|---|---|---|
| `health_score` | integer 0–100 | Overall health rating |
| `stars` | integer | Current star count |
| `forks` | integer | Current fork count |
| `open_issues` | integer | Current open issue count |
| `commit_frequency` | string | very_high / high / moderate / low / stale |
| `project_stage` | string | active / mature / maintained / slow / abandoned |
| `summary` | string | 2-sentence written analysis |
| `timestamp` | string | ISO 8601 UTC timestamp |

---

### 2. DeveloperReputationIndex

**Contract Address:** `0xfB4E11Be907456035807ce457E59D6C80dC594c9`
**Deploy TX:** https://explorer-studio.genlayer.com/tx/0x793330292e63573e1b8307b611bd624bb9cc6cdc9f46c5750eda4be21046f13e

Tracks the professional reputation of multiple GitHub developers. For each developer, it pulls their public profile, recent repositories, and activity events, then scores them on a 0–100 reputation index. Repeated `refresh()` calls build a historical record of how a developer's reputation evolves over time. The `compare()` function produces a head-to-head assessment with categorized edge areas.

**Write functions:**
- `add_developer(username)` — register a GitHub developer for tracking
- `analyze(username)` — fetch live GitHub data and produce a new reputation snapshot
- `refresh(username)` — re-run analysis and append a new snapshot
- `compare(username_a, username_b)` — AI head-to-head comparison of two developers
- `flag(username)` — mark a developer as flagged
- `unflag(username)` — remove flag
- `archive(username)` — mark a developer as archived
- `add_note(username, note)` — attach a text note to a developer record

**View functions:**
- `get_developer(username)` — full record and complete snapshot history
- `get_all_developers()` — all tracked developers
- `get_snapshots(username)` — all snapshots for a developer
- `get_latest(username)` — most recent snapshot only

**Snapshot fields per analysis:**

| Field | Type | Description |
|---|---|---|
| `reputation_score` | integer 0–100 | Overall reputation rating |
| `followers` | integer | Current follower count |
| `public_repos` | integer | Number of public repositories |
| `total_stars_earned` | integer | Sum of stars across all repos |
| `primary_language` | string | Most used programming language |
| `activity_level` | string | very_active / active / moderate / low / inactive |
| `specialization` | string | full_stack / backend / frontend / systems / data / devops / mixed |
| `summary` | string | 2-sentence written assessment |
| `timestamp` | string | ISO 8601 UTC timestamp |

---

### 3. TechStackTrendAnalyzer

**Contract Address:** `0x9857D3CedCfe87047E664fEb05d88781876FFaa3`
**Deploy TX:** https://explorer-studio.genlayer.com/tx/0x20459aa5e727c2929adc90552e89ae8420301475aece386116f33887845d0147

Tracks the adoption momentum of multiple programming languages and frameworks. Uses GitHub search APIs combined with LLM knowledge to produce a trend score from 0 to 100, with momentum direction, maturity level, primary use cases, competing technologies, and job market signal. The `compare()` function advises which technology is stronger for new projects today.

**Write functions:**
- `add_technology(tech_name, category)` — register a technology for tracking
- `analyze(tech_name)` — fetch live signals and produce a new trend snapshot
- `refresh(tech_name)` — re-run analysis and append a new snapshot
- `compare(tech_a, tech_b)` — AI head-to-head comparison of two technologies
- `flag(tech_name)` — mark a technology as flagged
- `unflag(tech_name)` — remove flag
- `archive(tech_name)` — mark a technology as archived
- `add_source_url(tech_name, url)` — attach a reference URL to a technology record

**View functions:**
- `get_technology(tech_name)` — full record and complete snapshot history
- `get_all_technologies()` — all tracked technologies
- `get_snapshots(tech_name)` — all snapshots for a technology
- `get_latest(tech_name)` — most recent snapshot only

**Snapshot fields per analysis:**

| Field | Type | Description |
|---|---|---|
| `trend_score` | integer 0–100 | Overall adoption momentum score |
| `momentum` | string | rising / stable / declining / niche / emerging |
| `maturity` | string | experimental / growing / mature / legacy / unknown |
| `primary_use_cases` | list | Top 2–3 use cases |
| `competing_technologies` | list | Top 2–3 main alternatives |
| `job_market_signal` | string | high_demand / moderate_demand / low_demand / unknown |
| `community_health` | string | very_active / active / moderate / small / declining |
| `summary` | string | 2-sentence trend analysis |
| `timestamp` | string | ISO 8601 UTC timestamp |

---

## Architecture

All three contracts follow the same structural pattern:

- **Multi-record storage** via two JSON string fields per contract: one for entity metadata, one for timestamped snapshot history per entity
- **Circular snapshot buffer** — up to 20 snapshots retained per entity; oldest dropped automatically when limit is reached
- **`run_nondet_unsafe`** with tolerance validator for all scored outputs — validators verify `isinstance(result, gl.vm.Return)` first, then validate score range
- **No one-shot guards** — every entity supports unlimited `analyze()` and `refresh()` calls, building an auditable history over time
- **`compare()`** on all three contracts issues a second nondet call to produce a structured AI comparison with reasoning
- **`flag()` and `archive()`** write functions support curation workflows without data deletion
- **Constructor accepts `tracker_name: str`** — each deployed instance is labeled at deploy time

---

## Technical Compliance

| Rule | Status |
|---|---|
| Dependency hash on line 1, straight quotes | ✅ |
| `from genlayer import *` import | ✅ |
| Class inherits `gl.Contract` | ✅ |
| Class annotations: `str` / `bool` only | ✅ |
| `dict` / `list` initialized in `__init__` only | ✅ |
| Storage writes outside nondet blocks | ✅ |
| `run_nondet_unsafe` with validator for scored results | ✅ |
| `validator_fn` checks `isinstance(result, gl.vm.Return)` first | ✅ |
| No one-shot `has_analyzed` guard | ✅ |
| `refresh()` supported — appends new snapshot | ✅ |
| Multi-record storage with history per entity | ✅ |
| Straight quotes throughout | ✅ |

---

## GenLayer Resources

- Studio: https://studio.genlayer.com
- Explorer: https://explorer-studio.genlayer.com
- Portal: https://portal.genlayer.foundation
- Docs: https://docs.genlayer.com
- Linter: https://docs.genlayer.com/api-references/genlayer-linter
- Boilerplate: https://github.com/genlayerlabs/genlayer-project-boilerplate
