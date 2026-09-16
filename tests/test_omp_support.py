"""Behavior tests for native Oh My Pi support."""

from __future__ import annotations

import json
import re

import pytest

from learn_faster.cli.installer import init_project
from learn_faster.cli.launcher import launch_coach
from learn_faster.cli.paths import get_agent_templates_dir


MODES = {"balanced", "exam", "practical", "programming", "theory"}


def test_omp_installer_writes_native_commands_agents_and_rule(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        "learn_faster.cli.installer.inquirer.prompt",
        lambda _questions: {"mode": "balanced"},
    )

    init_project("omp")

    assert tmp_path.joinpath(".omp", "commands", "learn.md").is_file()
    assert tmp_path.joinpath(".omp", "agents", "practice-creator.md").is_file()
    rule = tmp_path.joinpath(".omp", "rules", "learn-faster.md").read_text()
    assert rule.startswith("---\nalwaysApply: true\n")
    config = json.loads(tmp_path.joinpath(".learning", "config.json").read_text())
    assert config["agent"] == "omp"


def test_omp_launch_passes_the_mode_prompt_and_no_extra_flags(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    tmp_path.joinpath(".learning").mkdir()
    tmp_path.joinpath(".learning", "config.json").write_text(
        json.dumps({"initialized": True, "agent": "omp", "learning_mode": "balanced"})
    )
    captured = []
    monkeypatch.setattr(
        "learn_faster.cli.launcher._run_agent",
        lambda cmd, _agent: captured.append(cmd),
    )

    launch_coach(initialize=True)

    assert captured[0][0:2] == ["omp", "--system-prompt"]
    assert captured[0][2]
    assert captured[0][3:] == []


def test_omp_templates_cover_every_learning_mode() -> None:
    templates = get_agent_templates_dir("omp")
    assert templates.joinpath("instructions.md").is_file()
    assert {path.name for path in templates.joinpath("modes").iterdir()} == MODES

    for mode in MODES:
        mode_dir = templates / "modes" / mode
        assert mode_dir.joinpath("system_prompts", "learn-faster.md").is_file()
        assert any(mode_dir.joinpath("commands").glob("*.md"))


def test_omp_mode_templates_only_reference_agents_they_ship() -> None:
    templates = get_agent_templates_dir("omp")

    for mode in MODES:
        mode_dir = templates / "modes" / mode
        shipped = {path.stem for path in mode_dir.glob("agents/*.md")}
        prose = "\n".join(
            path.read_text()
            for path in mode_dir.rglob("*.md")
            if path.parent.name != "agents"
        )
        referenced = set(re.findall(r"agent[:\s]+[\"`]([a-z][a-z-]+)[\"`]", prose))
        referenced |= set(re.findall(r"[\"`]([a-z][a-z-]+)[\"`] agent", prose))
        assert referenced <= shipped, (mode, referenced - shipped)

    # `ask` needs a UI; subagents run headless.
    for path in templates.rglob("agents/*.md"):
        tools = re.search(r"^tools: (.*)$", path.read_text(), re.MULTILINE)
        assert tools is not None
        assert "ask" not in {tool.strip() for tool in tools.group(1).split(",")}


def test_omp_templates_use_omp_tools_and_valid_ask_payloads() -> None:
    templates = get_agent_templates_dir("omp")
    markdown = list(templates.rglob("*.md"))
    combined = "\n".join(path.read_text() for path in markdown)

    for stale_syntax in (
        "AskUserQuestion",
        "@practice-creator",
        "WebSearch",
        "WebFetch",
        "subagent_type",
        "!`",
    ):
        assert stale_syntax not in combined

    for path in markdown:
        for block in re.findall(r"```json\n(.*?)\n```", path.read_text(), re.DOTALL):
            payload = json.loads(block)
            if "questions" not in payload:
                continue
            assert payload["questions"]
            for question in payload["questions"]:
                assert {"id", "question", "options"} <= set(question)
                assert "multiSelect" not in question
