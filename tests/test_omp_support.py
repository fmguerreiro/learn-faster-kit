"""Behavior tests for native Oh My Pi support."""

from __future__ import annotations

import json
import re

import pytest

from learn_faster.cli.agents import get_agent_profile
from learn_faster.cli.installer import init_project
from learn_faster.cli.launcher import ResumeTarget, build_resume_command, launch_coach
from learn_faster.cli.paths import get_agent_templates_dir


OMP = get_agent_profile("omp")
PROMPT = "FASTER coaching system prompt"
MODES = {"balanced", "exam", "practical", "programming", "theory"}


def test_omp_profile_uses_native_project_surfaces() -> None:
    assert OMP.executable == "omp"
    assert OMP.config_dir == ".omp"
    assert OMP.instruction_file == ".omp/rules/learn-faster.md"
    assert OMP.launch_style == "system-prompt"
    assert OMP.plan_mode_cmd == ""


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


@pytest.mark.parametrize(
    "initialize, auto_review, expected_tail",
    [
        (True, False, []),
        (False, True, ["/review"]),
    ],
)
def test_omp_launch_uses_system_prompt_and_native_flags(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
    initialize: bool,
    auto_review: bool,
    expected_tail: list[str],
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

    launch_coach(auto_review=auto_review, initialize=initialize)

    assert captured[0][0:2] == ["omp", "--system-prompt"]
    assert captured[0][2]
    assert captured[0][3:] == expected_tail


@pytest.mark.parametrize(
    "target, expected_tail",
    [
        (ResumeTarget(mode="last"), ["--continue"]),
        (ResumeTarget(mode="id", session_id="abc-123"), ["--resume", "abc-123"]),
        (ResumeTarget(mode="pick"), ["--resume"]),
        (ResumeTarget(mode="id", session_id="abc-123", fork=True), ["--fork", "abc-123"]),
    ],
)
def test_omp_resume_command_shape(
    target: ResumeTarget, expected_tail: list[str]
) -> None:
    cmd = build_resume_command(OMP, PROMPT, target)
    assert cmd[:3] == ["omp", "--system-prompt", PROMPT]
    assert cmd[3:] == expected_tail


@pytest.mark.parametrize("mode", ["last", "pick"])
def test_omp_fork_requires_explicit_session_id(mode: str) -> None:
    with pytest.raises(ValueError, match="explicit session id"):
        build_resume_command(OMP, PROMPT, ResumeTarget(mode=mode, fork=True))


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
        "$topic",
        "Claude Code",
        "CLAUDE.md",
    ):
        assert stale_syntax not in combined

    assert "tools: read, write, edit" in combined
    assert 'model: "@slow"' in combined

    for path in markdown:
        for block in re.findall(r"```json\n(.*?)\n```", path.read_text(), re.DOTALL):
            payload = json.loads(block)
            assert set(payload) == {"questions"}
            assert isinstance(payload["questions"], list)
            assert payload["questions"]
            for question in payload["questions"]:
                assert {"id", "question", "options"} <= set(question)
                assert "header" not in question
                assert "multiSelect" not in question
