"""
Dynamic Security Module Synthesizer and Hot-Reload Engine
Module: dynamic_synthesizer.py

Capabilities:
1. Local template-driven synthesis from compact DynamicProbeSpec (<150 tokens)
2. Instant in-memory hot-reloading via Python importlib (zero downtime)
3. Direct execution against active Playwright / API session context
4. Asynchronous non-blocking Git persistence to GitHub (sadik004/bug-hunter)
"""

import asyncio
import importlib.util
import json
import logging
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

from behavioral_evasion_suite.dynamic_probe_protocol import (
    DynamicProbeSpec,
    DynamicProbeResult,
    BaseDynamicAuditor,
    DYNAMIC_AUDITOR_TEMPLATE
)

logger = logging.getLogger("dynamic_synthesizer")


class DynamicSynthesizer:
    """Master orchestrator for on-the-fly probe synthesis, hot-loading, and persistence."""

    def __init__(self, plugins_dir: Optional[Path] = None, repo_root: Optional[Path] = None):
        base_dir = Path(__file__).parent
        self.plugins_dir = plugins_dir or (base_dir / "dynamic_plugins")
        self.repo_root = repo_root or base_dir.parent
        self.plugins_dir.mkdir(parents=True, exist_ok=True)

    def synthesize_probe(self, spec: DynamicProbeSpec) -> Path:
        """
        Synthesizes a full production-ready Python auditor file from compact DynamicProbeSpec.
        """
        clean_name = spec.probe_name.strip().replace("-", "_").lower()
        file_path = self.plugins_dir / f"{clean_name}.py"

        # Format Python code from BaseDynamicAuditor template
        rendered_code = DYNAMIC_AUDITOR_TEMPLATE.format(
            probe_name=clean_name,
            research_source=spec.research_source,
            cwe=spec.cwe,
            rationale=spec.rationale or "Synthesized dynamic security probe"
        )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(rendered_code)

        return file_path

    def hot_load_probe(self, probe_path: Path, spec: DynamicProbeSpec) -> BaseDynamicAuditor:
        """
        Hot-loads the synthesized probe into the active Python process memory via importlib.
        """
        module_name = f"dynamic_plugin_{probe_path.stem}_{int(time.time() * 1000)}"
        spec_loader = importlib.util.spec_from_file_location(module_name, str(probe_path))
        if spec_loader is None or spec_loader.loader is None:
            raise ImportError(f"Cannot load module spec from {probe_path}")

        module = importlib.util.module_from_spec(spec_loader)
        sys.modules[module_name] = module
        spec_loader.loader.exec_module(module)

        if not hasattr(module, "create_auditor"):
            raise AttributeError(f"Synthesized probe {probe_path} lacks create_auditor entrypoint")

        return module.create_auditor(spec)

    async def hot_execute_probe(
        self,
        probe_path: Path,
        spec: DynamicProbeSpec,
        session_context: Any
    ) -> DynamicProbeResult:
        """
        Loads and immediately fires the synthesized probe on the live target session.
        """
        auditor = self.hot_load_probe(probe_path, spec)
        result = await auditor.execute_live(session_context)
        return result

    def persist_to_git_async(self, probe_path: Path, spec: DynamicProbeSpec) -> asyncio.Task:
        """
        Fires an asynchronous, non-blocking background task to commit and push the new probe to GitHub.
        """
        async def _git_worker():
            try:
                loop = asyncio.get_running_loop()
                def _run_git():
                    try:
                        # 1. git add
                        subprocess.run(
                            ["git", "add", str(probe_path)],
                            cwd=str(self.repo_root),
                            check=True,
                            capture_output=True,
                            encoding="utf-8"
                        )
                        # 2. git commit
                        commit_msg = f"feat(weapon): synthesize {spec.probe_name} [{spec.cwe}] via NotebookLM"
                        subprocess.run(
                            ["git", "commit", "-m", commit_msg],
                            cwd=str(self.repo_root),
                            check=True,
                            capture_output=True,
                            encoding="utf-8"
                        )
                        # 3. git push
                        subprocess.run(
                            ["git", "push", "origin", "main"],
                            cwd=str(self.repo_root),
                            check=True,
                            capture_output=True,
                            encoding="utf-8"
                        )
                        return True
                    except subprocess.CalledProcessError as err:
                        logger.warning(f"Git persistence notice: {err.stderr.strip() if err.stderr else str(err)}")
                        return False

                return await loop.run_in_executor(None, _run_git)
            except Exception as e:
                logger.warning(f"Background Git persistence encountered: {e}")
                return False

        return asyncio.create_task(_git_worker())

    async def synthesize_and_execute(
        self,
        spec: DynamicProbeSpec,
        session_context: Any,
        auto_persist: bool = True
    ) -> DynamicProbeResult:
        """
        Unified pipeline:
        1. Synthesize local module (<150 tokens)
        2. Hot-load into memory and execute on live session immediately
        3. Persist to sadik004/bug-hunter via background Git task
        """
        probe_path = self.synthesize_probe(spec)
        result = await self.hot_execute_probe(probe_path, spec, session_context)

        if auto_persist:
            self.persist_to_git_async(probe_path, spec)

        return result
