# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json
import typing
from datetime import datetime, timezone
import gl


class DeveloperReputationIndex:
    tracked_devs: str
    snapshots: str

    def __init__(self):
        self.tracked_devs = "{}"
        self.snapshots = "{}"

    def _get_devs(self) -> dict:
        return json.loads(self.tracked_devs)

    def _get_snapshots(self) -> dict:
        return json.loads(self.snapshots)

    def _save_devs(self, data: dict):
        self.tracked_devs = json.dumps(data)

    def _save_snapshots(self, data: dict):
        self.snapshots = json.dumps(data)

    def _now() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    @gl.public.write
    def add_developer(self, username: str) -> typing.Any:
        devs = self._get_devs()
        devs[username] = {
            "username": username,
            "added_at": DeveloperReputationIndex._now(),
            "flagged": False,
            "archived": False,
        }
        self._save_devs(devs)
        return f"Tracking developer {username}"

    @gl.public.write
    def analyze(self, username: str) -> typing.Any:
        devs = self._get_devs()
        if username not in devs:
            devs[username] = {
                "username": username,
                "added_at": DeveloperReputationIndex._now(),
                "flagged": False,
                "archived": False,
            }
            self._save_devs(devs)

        profile_url = f"https://api.github.com/users/{username}"
        repos_url = f"https://api.github.com/users/{username}/repos?sort=pushed&per_page=10"
        events_url = f"https://api.github.com/users/{username}/events?per_page=15"

        def leader_fn():
            profile_raw = gl.nondet.web.get(profile_url).body.decode("utf-8")
            repos_raw = gl.nondet.web.get(repos_url).body.decode("utf-8")
            events_raw = gl.nondet.web.get(events_url).body.decode("utf-8")

            task = f"""You are computing a developer reputation index for a GitHub user.

GitHub Profile JSON:
{profile_raw[:2000]}

Recent Repositories JSON (last 10 pushed):
{repos_raw[:2500]}

Recent Events JSON (last 15 public events):
{events_raw[:2000]}

Analyze all signals including: followers, public repos, recent activity, repo stars earned, language diversity, project consistency, commit volume.

Produce a JSON object with ONLY these fields:
- reputation_score: integer 0-100
- followers: integer
- public_repos: integer
- total_stars_earned: integer (sum of stargazers_count across repos)
- primary_language: string (most used language)
- activity_level: string (one of: "very_active", "active", "moderate", "low", "inactive")
- specialization: string (one of: "full_stack", "backend", "frontend", "systems", "data", "devops", "mixed", "unknown")
- summary: string (one 2-sentence assessment)

Return ONLY valid JSON. No explanation, no markdown.
"""
            raw = gl.nondet.exec_prompt(task)
            cleaned = raw.strip().replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned)

        def validator_fn(leader_result):
            if not isinstance(leader_result, gl.vm.Return):
                return False
            val = leader_result.result
            if not isinstance(val, dict):
                return False
            score = val.get("reputation_score", -1)
            return isinstance(score, int) and 0 <= score <= 100

        result = gl.run_nondet_unsafe(leader_fn, validator_fn)

        snapshots = self._get_snapshots()
        if username not in snapshots:
            snapshots[username] = []

        entry = {
            "timestamp": DeveloperReputationIndex._now(),
            "reputation_score": result.get("reputation_score"),
            "followers": result.get("followers"),
            "public_repos": result.get("public_repos"),
            "total_stars_earned": result.get("total_stars_earned"),
            "primary_language": result.get("primary_language"),
            "activity_level": result.get("activity_level"),
            "specialization": result.get("specialization"),
            "summary": result.get("summary"),
        }
        snapshots[username].append(entry)
        if len(snapshots[username]) > 20:
            snapshots[username] = snapshots[username][-20:]
        self._save_snapshots(snapshots)

        return json.dumps(entry)

    @gl.public.write
    def refresh(self, username: str) -> typing.Any:
        return self.analyze(username)

    @gl.public.write
    def compare(self, username_a: str, username_b: str) -> typing.Any:
        snapshots = self._get_snapshots()
        snap_a = snapshots.get(username_a, [])
        snap_b = snapshots.get(username_b, [])
        latest_a = snap_a[-1] if snap_a else {}
        latest_b = snap_b[-1] if snap_b else {}

        def leader_fn():
            task = f"""Compare two software developers based on their reputation snapshots.

Developer A ({username_a}):
{json.dumps(latest_a)}

Developer B ({username_b}):
{json.dumps(latest_b)}

Produce a JSON object with:
- winner: string (username with higher overall reputation, or "tie")
- reasoning: string (2 sentences)
- score_diff: integer (absolute reputation_score difference)
- edge_categories: list of strings (areas where winner leads, e.g. ["followers","activity_level"])

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
    def flag(self, username: str) -> typing.Any:
        devs = self._get_devs()
        if username not in devs:
            return f"Developer {username} not tracked"
        devs[username]["flagged"] = True
        devs[username]["flagged_at"] = DeveloperReputationIndex._now()
        self._save_devs(devs)
        return f"Flagged {username}"

    @gl.public.write
    def unflag(self, username: str) -> typing.Any:
        devs = self._get_devs()
        if username not in devs:
            return f"Developer {username} not tracked"
        devs[username]["flagged"] = False
        self._save_devs(devs)
        return f"Unflagged {username}"

    @gl.public.write
    def archive(self, username: str) -> typing.Any:
        devs = self._get_devs()
        if username not in devs:
            return f"Developer {username} not tracked"
        devs[username]["archived"] = True
        devs[username]["archived_at"] = DeveloperReputationIndex._now()
        self._save_devs(devs)
        return f"Archived {username}"

    @gl.public.write
    def add_note(self, username: str, note: str) -> typing.Any:
        devs = self._get_devs()
        if username not in devs:
            return f"Developer {username} not tracked"
        if "notes" not in devs[username]:
            devs[username]["notes"] = []
        devs[username]["notes"].append({
            "text": note,
            "added_at": DeveloperReputationIndex._now(),
        })
        self._save_devs(devs)
        return f"Note added for {username}"

    @gl.public.view
    def get_developer(self, username: str) -> str:
        devs = self._get_devs()
        snapshots = self._get_snapshots()
        dev = devs.get(username, {})
        history = snapshots.get(username, [])
        return json.dumps({"developer": dev, "history": history})

    @gl.public.view
    def get_all_developers(self) -> str:
        return self.tracked_devs

    @gl.public.view
    def get_snapshots(self, username: str) -> str:
        snapshots = self._get_snapshots()
        return json.dumps(snapshots.get(username, []))

    @gl.public.view
    def get_latest(self, username: str) -> str:
        snapshots = self._get_snapshots()
        history = snapshots.get(username, [])
        if not history:
            return "{}"
        return json.dumps(history[-1])
