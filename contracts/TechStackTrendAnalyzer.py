# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json
import typing
from datetime import datetime, timezone
import gl


class TechStackTrendAnalyzer:
    tracked_techs: str
    snapshots: str

    def __init__(self):
        self.tracked_techs = "{}"
        self.snapshots = "{}"

    def _get_techs(self) -> dict:
        return json.loads(self.tracked_techs)

    def _get_snapshots(self) -> dict:
        return json.loads(self.snapshots)

    def _save_techs(self, data: dict):
        self.tracked_techs = json.dumps(data)

    def _save_snapshots(self, data: dict):
        self.snapshots = json.dumps(data)

    def _now() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    @gl.public.write
    def add_technology(self, tech_name: str, category: str) -> typing.Any:
        techs = self._get_techs()
        techs[tech_name] = {
            "tech_name": tech_name,
            "category": category,
            "added_at": TechStackTrendAnalyzer._now(),
            "flagged": False,
            "archived": False,
        }
        self._save_techs(techs)
        return f"Tracking {tech_name} ({category})"

    @gl.public.write
    def analyze(self, tech_name: str) -> typing.Any:
        techs = self._get_techs()
        if tech_name not in techs:
            techs[tech_name] = {
                "tech_name": tech_name,
                "category": "unknown",
                "added_at": TechStackTrendAnalyzer._now(),
                "flagged": False,
                "archived": False,
            }
            self._save_techs(techs)

        search_url = f"https://api.github.com/search/repositories?q=language:{tech_name}&sort=stars&per_page=5"
        topic_url = f"https://api.github.com/search/topics?q={tech_name}&per_page=3"

        def leader_fn():
            search_raw = gl.nondet.web.get(search_url).body.decode("utf-8")
            topic_raw = gl.nondet.web.get(topic_url).body.decode("utf-8")

            task = f"""You are analyzing the adoption trend and popularity of a technology or programming language named "{tech_name}".

GitHub repository search results for this technology:
{search_raw[:2500]}

GitHub topic search results:
{topic_raw[:1500]}

Use your training knowledge plus these signals to assess current adoption trends.

Produce a JSON object with ONLY these fields:
- trend_score: integer 0-100 (overall adoption momentum)
- momentum: string (one of: "rising", "stable", "declining", "niche", "emerging")
- maturity: string (one of: "experimental", "growing", "mature", "legacy", "unknown")
- primary_use_cases: list of strings (top 2-3 use cases)
- competing_technologies: list of strings (top 2-3 main alternatives)
- job_market_signal: string (one of: "high_demand", "moderate_demand", "low_demand", "unknown")
- community_health: string (one of: "very_active", "active", "moderate", "small", "declining")
- summary: string (one 2-sentence trend analysis)

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
            score = val.get("trend_score", -1)
            return isinstance(score, int) and 0 <= score <= 100

        result = gl.run_nondet_unsafe(leader_fn, validator_fn)

        snapshots = self._get_snapshots()
        if tech_name not in snapshots:
            snapshots[tech_name] = []

        entry = {
            "timestamp": TechStackTrendAnalyzer._now(),
            "trend_score": result.get("trend_score"),
            "momentum": result.get("momentum"),
            "maturity": result.get("maturity"),
            "primary_use_cases": result.get("primary_use_cases"),
            "competing_technologies": result.get("competing_technologies"),
            "job_market_signal": result.get("job_market_signal"),
            "community_health": result.get("community_health"),
            "summary": result.get("summary"),
        }
        snapshots[tech_name].append(entry)
        if len(snapshots[tech_name]) > 20:
            snapshots[tech_name] = snapshots[tech_name][-20:]
        self._save_snapshots(snapshots)

        return json.dumps(entry)

    @gl.public.write
    def refresh(self, tech_name: str) -> typing.Any:
        return self.analyze(tech_name)

    @gl.public.write
    def compare(self, tech_a: str, tech_b: str) -> typing.Any:
        snapshots = self._get_snapshots()
        snap_a = snapshots.get(tech_a, [])
        snap_b = snapshots.get(tech_b, [])
        latest_a = snap_a[-1] if snap_a else {}
        latest_b = snap_b[-1] if snap_b else {}

        def leader_fn():
            task = f"""Compare two technologies based on their trend snapshots.

Technology A ({tech_a}):
{json.dumps(latest_a)}

Technology B ({tech_b}):
{json.dumps(latest_b)}

Produce a JSON object with:
- stronger_trend: string (tech with better momentum/score, or "tie")
- reasoning: string (2 sentences)
- score_diff: integer (absolute trend_score difference)
- recommended_for_new_projects: string (which to recommend for new projects today, or "depends")

Return ONLY valid JSON. No explanation, no markdown.
"""
            raw = gl.nondet.exec_prompt(task)
            cleaned = raw.strip().replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned)

        def validator_fn(leader_result):
            if not isinstance(leader_result, gl.vm.Return):
                return False
            val = leader_result.result
            return isinstance(val, dict) and "stronger_trend" in val

        result = gl.run_nondet_unsafe(leader_fn, validator_fn)
        return json.dumps(result)

    @gl.public.write
    def flag(self, tech_name: str) -> typing.Any:
        techs = self._get_techs()
        if tech_name not in techs:
            return f"Technology {tech_name} not tracked"
        techs[tech_name]["flagged"] = True
        techs[tech_name]["flagged_at"] = TechStackTrendAnalyzer._now()
        self._save_techs(techs)
        return f"Flagged {tech_name}"

    @gl.public.write
    def unflag(self, tech_name: str) -> typing.Any:
        techs = self._get_techs()
        if tech_name not in techs:
            return f"Technology {tech_name} not tracked"
        techs[tech_name]["flagged"] = False
        self._save_techs(techs)
        return f"Unflagged {tech_name}"

    @gl.public.write
    def archive(self, tech_name: str) -> typing.Any:
        techs = self._get_techs()
        if tech_name not in techs:
            return f"Technology {tech_name} not tracked"
        techs[tech_name]["archived"] = True
        techs[tech_name]["archived_at"] = TechStackTrendAnalyzer._now()
        self._save_techs(techs)
        return f"Archived {tech_name}"

    @gl.public.write
    def add_source_url(self, tech_name: str, url: str) -> typing.Any:
        techs = self._get_techs()
        if tech_name not in techs:
            return f"Technology {tech_name} not tracked"
        if "source_urls" not in techs[tech_name]:
            techs[tech_name]["source_urls"] = []
        techs[tech_name]["source_urls"].append({
            "url": url,
            "added_at": TechStackTrendAnalyzer._now(),
        })
        self._save_techs(techs)
        return f"Source URL added for {tech_name}"

    @gl.public.view
    def get_technology(self, tech_name: str) -> str:
        techs = self._get_techs()
        snapshots = self._get_snapshots()
        tech = techs.get(tech_name, {})
        history = snapshots.get(tech_name, [])
        return json.dumps({"technology": tech, "history": history})

    @gl.public.view
    def get_all_technologies(self) -> str:
        return self.tracked_techs

    @gl.public.view
    def get_snapshots(self, tech_name: str) -> str:
        snapshots = self._get_snapshots()
        return json.dumps(snapshots.get(tech_name, []))

    @gl.public.view
    def get_latest(self, tech_name: str) -> str:
        snapshots = self._get_snapshots()
        history = snapshots.get(tech_name, [])
        if not history:
            return "{}"
        return json.dumps(history[-1])
