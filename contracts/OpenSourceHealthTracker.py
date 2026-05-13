# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json
import typing
from datetime import datetime, timezone


class OpenSourceHealthTracker(gl.Contract):
    tracker_name: str
    tracked_repos: str
    snapshots: str

    def __init__(self, tracker_name: str):
        self.tracker_name = tracker_name
        self.tracked_repos = "{}"
        self.snapshots = "{}"

    def _get_tracked(self) -> dict:
        return json.loads(self.tracked_repos)

    def _get_snapshots(self) -> dict:
        return json.loads(self.snapshots)

    def _save_tracked(self, data: dict):
        self.tracked_repos = json.dumps(data)

    def _save_snapshots(self, data: dict):
        self.snapshots = json.dumps(data)

    def _now() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    @gl.public.write
    def add_repo(self, owner: str, name: str) -> typing.Any:
        key = f"{owner}/{name}"
        tracked = self._get_tracked()
        tracked[key] = {
            "owner": owner,
            "name": name,
            "added_at": OpenSourceHealthTracker._now(),
            "flagged": False,
            "archived": False,
        }
        self._save_tracked(tracked)
        return f"Added repo {key}"

    @gl.public.write
    def analyze(self, owner: str, name: str) -> typing.Any:
        key = f"{owner}/{name}"
        tracked = self._get_tracked()
        if key not in tracked:
            tracked[key] = {
                "owner": owner,
                "name": name,
                "added_at": OpenSourceHealthTracker._now(),
                "flagged": False,
                "archived": False,
            }
            self._save_tracked(tracked)

        api_url = f"https://api.github.com/repos/{owner}/{name}"
        commits_url = f"https://api.github.com/repos/{owner}/{name}/commits?per_page=10"
        issues_url = f"https://api.github.com/repos/{owner}/{name}/issues?state=open&per_page=5"

        def leader_fn():
            raw = gl.nondet.web.get(api_url).body.decode("utf-8")
            commits_raw = gl.nondet.web.get(commits_url).body.decode("utf-8")
            issues_raw = gl.nondet.web.get(issues_url).body.decode("utf-8")

            task = f"""You are analyzing the health of an open source GitHub repository.

Repository metadata JSON:
{raw[:3000]}

Recent commits JSON (last 10):
{commits_raw[:2000]}

Open issues JSON (sample):
{issues_raw[:2000]}

Based on this data, produce a JSON object with ONLY these fields:
- health_score: integer 0-100
- stars: integer
- forks: integer
- open_issues: integer
- commit_frequency: string (one of: "very_high", "high", "moderate", "low", "stale")
- project_stage: string (one of: "active", "mature", "maintained", "slow", "abandoned")
- summary: string (one 2-sentence analysis)

Return ONLY valid JSON. No explanation, no markdown.
"""
            result_raw = gl.nondet.exec_prompt(task)
            cleaned = result_raw.strip().replace("```json", "").replace("```", "").strip()
            parsed = json.loads(cleaned)
            return parsed

        def validator_fn(leader_result):
            if not isinstance(leader_result, gl.vm.Return):
                return False
            val = leader_result.result
            if not isinstance(val, dict):
                return False
            score = val.get("health_score", -1)
            return isinstance(score, int) and 0 <= score <= 100

        result = gl.run_nondet_unsafe(leader_fn, validator_fn)

        snapshots = self._get_snapshots()
        if key not in snapshots:
            snapshots[key] = []

        entry = {
            "timestamp": OpenSourceHealthTracker._now(),
            "health_score": result.get("health_score"),
            "stars": result.get("stars"),
            "forks": result.get("forks"),
            "open_issues": result.get("open_issues"),
            "commit_frequency": result.get("commit_frequency"),
            "project_stage": result.get("project_stage"),
            "summary": result.get("summary"),
        }
        snapshots[key].append(entry)
        if len(snapshots[key]) > 20:
            snapshots[key] = snapshots[key][-20:]
        self._save_snapshots(snapshots)

        return json.dumps(entry)

    @gl.public.write
    def refresh(self, owner: str, name: str) -> typing.Any:
        return self.analyze(owner, name)

    @gl.public.write
    def compare(self, owner_a: str, name_a: str, owner_b: str, name_b: str) -> typing.Any:
        key_a = f"{owner_a}/{name_a}"
        key_b = f"{owner_b}/{name_b}"
        snapshots = self._get_snapshots()

        snap_a = snapshots.get(key_a, [])
        snap_b = snapshots.get(key_b, [])

        latest_a = snap_a[-1] if snap_a else {}
        latest_b = snap_b[-1] if snap_b else {}

        def leader_fn():
            task = f"""Compare two open source repositories based on their health snapshots.

Repository A ({key_a}):
{json.dumps(latest_a)}

Repository B ({key_b}):
{json.dumps(latest_b)}

Produce a JSON object with:
- winner: string (repo key that is healthier overall, or "tie")
- reasoning: string (2 sentences explaining why)
- score_diff: integer (absolute difference in health_score, 0 if unknown)

Return ONLY valid JSON. No explanation, no markdown.
"""
            raw = gl.nondet.exec_prompt(task)
            cleaned = raw.strip().replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned)

        def validator_fn(leader_result):
            if not isinstance(leader_result, gl.vm.Return):
                return False
            val = leader_result.result
            return isinstance(val, dict) and "winner" in val

        result = gl.run_nondet_unsafe(leader_fn, validator_fn)
        return json.dumps(result)

    @gl.public.write
    def flag(self, owner: str, name: str) -> typing.Any:
        key = f"{owner}/{name}"
        tracked = self._get_tracked()
        if key not in tracked:
            return f"Repo {key} not tracked"
        tracked[key]["flagged"] = True
        tracked[key]["flagged_at"] = OpenSourceHealthTracker._now()
        self._save_tracked(tracked)
        return f"Flagged {key}"

    @gl.public.write
    def unflag(self, owner: str, name: str) -> typing.Any:
        key = f"{owner}/{name}"
        tracked = self._get_tracked()
        if key not in tracked:
            return f"Repo {key} not tracked"
        tracked[key]["flagged"] = False
        self._save_tracked(tracked)
        return f"Unflagged {key}"

    @gl.public.write
    def archive(self, owner: str, name: str) -> typing.Any:
        key = f"{owner}/{name}"
        tracked = self._get_tracked()
        if key not in tracked:
            return f"Repo {key} not tracked"
        tracked[key]["archived"] = True
        tracked[key]["archived_at"] = OpenSourceHealthTracker._now()
        self._save_tracked(tracked)
        return f"Archived {key}"

    @gl.public.write
    def add_note(self, owner: str, name: str, note: str) -> typing.Any:
        key = f"{owner}/{name}"
        tracked = self._get_tracked()
        if key not in tracked:
            return f"Repo {key} not tracked"
        if "notes" not in tracked[key]:
            tracked[key]["notes"] = []
        tracked[key]["notes"].append({
            "text": note,
            "added_at": OpenSourceHealthTracker._now(),
        })
        self._save_tracked(tracked)
        return f"Note added to {key}"

    @gl.public.view
    def get_repo(self, owner: str, name: str) -> str:
        key = f"{owner}/{name}"
        tracked = self._get_tracked()
        snapshots = self._get_snapshots()
        repo = tracked.get(key, {})
        history = snapshots.get(key, [])
        return json.dumps({"repo": repo, "history": history})

    @gl.public.view
    def get_all_repos(self) -> str:
        return self.tracked_repos

    @gl.public.view
    def get_snapshots(self, owner: str, name: str) -> str:
        key = f"{owner}/{name}"
        snapshots = self._get_snapshots()
        return json.dumps(snapshots.get(key, []))

    @gl.public.view
    def get_latest(self, owner: str, name: str) -> str:
        key = f"{owner}/{name}"
        snapshots = self._get_snapshots()
        history = snapshots.get(key, [])
        if not history:
            return "{}"
        return json.dumps(history[-1])
