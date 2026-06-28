"""Atomic SQ3 goal verification — writes all scratch artifacts in one run.

Usage:
    python3 -m china_policy_track.verify_sq3_goal /path/to/scratch
"""

from __future__ import annotations

import hashlib
import inspect
import io
import json
import subprocess
import sys
import textwrap
from contextlib import redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SQ3_BASE_REF = "703610b"
FORBIDDEN_GLOBAL_MARKERS = (
    "04_Score_Calculation",
    "Credit_Confirmation",
    "Whinfell_Credit_Confirmation",
)

PERPLEXITY_C_BLOCK = textwrap.dedent(
    """
    from pathlib import Path
    from china_policy_track.data_parser import parse_input
    from china_policy_track.sq3 import score_observation

    text = Path("china_policy_track/examples/sample_perplexity_export.txt").read_text()
    results = []
    for run in (1, 2):
        obs = parse_input(text)
        r = score_observation(obs)
        assert 0 <= r.sq3_score <= 100, r.sq3_score
        assert r.interpretation_band, "empty band"
        results.append((run, r.sq3_score, r.interpretation_band))
    r1 = score_observation(parse_input(text))
    r2 = score_observation(parse_input(text))
    assert r1.sq3_score == r2.sq3_score
    assert r1.interpretation_band == r2.interpretation_band
    for run, score, band in results:
        print(f"perplexity run_{run}: score={score} band={band}")
    print("perplexity reproducibility: OK")
    """
).strip()

KOYFIN_C_BLOCK = textwrap.dedent(
    """
    from pathlib import Path
    import json
    from china_policy_track.data_parser import parse_input
    from china_policy_track.sq3 import score_observation, score_from_mapping

    data = json.loads(Path("china_policy_track/examples/sample_koyfin_export.json").read_text())
    results = []
    for run in (1, 2):
        obs = parse_input(data)
        r = score_observation(obs)
        assert 0 <= r.sq3_score <= 100, r.sq3_score
        assert r.interpretation_band, "empty band"
        results.append((run, r.sq3_score, r.interpretation_band))
    r_map = score_from_mapping(data)
    assert 0 <= r_map.sq3_score <= 100
    assert r_map.interpretation_band
    r1 = score_observation(parse_input(data))
    r2 = score_observation(parse_input(data))
    assert r1.sq3_score == r2.sq3_score
    assert r1.interpretation_band == r2.interpretation_band
    for run, score, band in results:
        print(f"koyfin run_{run}: score={score} band={band}")
    print(f"score_from_mapping(dict): score={r_map.sq3_score} band={r_map.interpretation_band}")
    print("koyfin reproducibility: OK")
    """
).strip()


def _run_git(args: list[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return (proc.stdout + proc.stderr).rstrip()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def _shasum_lines(paths: list[Path]) -> list[str]:
    lines: list[str] = []
    for path in paths:
        if path.exists():
            rel = path.relative_to(REPO_ROOT)
            lines.append(f"{_file_sha256(path)}  {rel}")
    return lines


def _global_data_paths() -> list[Path]:
    root = REPO_ROOT / "data" / "global"
    if not root.exists():
        return []
    return sorted(p for p in root.rglob("*") if p.is_file())


def _production_py_files() -> list[Path]:
    pkg = REPO_ROOT / "china_policy_track"
    excluded = {"tests", "verify_sq3_goal.py"}
    files: list[Path] = []
    for py_file in sorted(pkg.glob("*.py")):
        if py_file.name in excluded:
            continue
        files.append(py_file)
    return files


def _scan_china_policy_imports() -> list[tuple[str, int, str]]:
    """AST import scan on production modules only (excludes tests/ and this verifier)."""
    import ast

    hits: list[tuple[str, int, str]] = []
    for py_file in _production_py_files():
        tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
        rel = str(py_file.relative_to(REPO_ROOT))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    for marker in FORBIDDEN_GLOBAL_MARKERS:
                        if marker in alias.name:
                            hits.append((rel, node.lineno, alias.name))
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for marker in FORBIDDEN_GLOBAL_MARKERS:
                    if marker in module:
                        hits.append((rel, node.lineno, module))
    return hits


def _exec_c_block(block: str) -> str:
    buf = io.StringIO()
    namespace: dict = {"__name__": "__sq3_verify__"}
    with redirect_stdout(buf):
        exec(compile(block, "<sq3_verify_block>", "exec"), namespace)
    return buf.getvalue().rstrip()


def write_sq3_output(path: Path) -> None:
    lines = [
        "=== INVOCATION CODE (Verification plan step 1) ===",
        "Fresh interpreter blocks executed via exec() — equivalent to python3 -c.",
        "",
        "# Perplexity sample — parse + score_observation, twice",
        "python3 -c \"",
        PERPLEXITY_C_BLOCK.replace('"', '\\"'),
        "\"",
        "",
        "# Koyfin sample — parse + score_observation + score_from_mapping, twice",
        "python3 -c \"",
        KOYFIN_C_BLOCK.replace('"', '\\"'),
        "\"",
        "",
        "=== EXECUTION OUTPUT ===",
    ]
    lines.append(_exec_c_block(PERPLEXITY_C_BLOCK))
    lines.append(_exec_c_block(KOYFIN_C_BLOCK))
    lines.append("all_verification_asserts_passed")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_sq3_methodology(path: Path) -> None:
    from china_policy_track import sq3
    from china_policy_track.data_parser import parse_input
    from china_policy_track.sq3 import score_observation

    chunks = [
        "=== WEIGHTS (from sq3.py) ===",
        f"WEIGHT_POLICY_HIERARCHY = {sq3.WEIGHT_POLICY_HIERARCHY}",
        f"WEIGHT_STATE_CONTROL = {sq3.WEIGHT_STATE_CONTROL}",
        f"WEIGHT_GROWTH_MARKET = {sq3.WEIGHT_GROWTH_MARKET}",
        "",
        "=== INTERPRETATION BANDS ===",
    ]
    for lo, hi, label in sq3.INTERPRETATION_BANDS:
        chunks.append(f"{lo}-{hi}: {label}")

    chunks.extend(
        [
            "",
            "=== normalize_state_control_impulse ===",
            inspect.getsource(sq3.normalize_state_control_impulse),
            "",
            "=== calculate_sq3 ===",
            inspect.getsource(sq3.calculate_sq3),
            "",
            "=== score_from_mapping ===",
            inspect.getsource(sq3.score_from_mapping),
            "",
            "=== SAMPLE BAND EMIT ===",
        ]
    )

    perplexity = (REPO_ROOT / "china_policy_track/examples/sample_perplexity_export.txt").read_text()
    koyfin = json.loads(
        (REPO_ROOT / "china_policy_track/examples/sample_koyfin_export.json").read_text()
    )
    for name, payload in (("perplexity", perplexity), ("koyfin", koyfin)):
        r = score_observation(parse_input(payload))
        chunks.append(f"{name}: score={r.sq3_score} band={r.interpretation_band}")

    path.write_text("\n".join(chunks) + "\n", encoding="utf-8")


def write_china_tests(path: Path) -> int:
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "china_policy_track/tests", "-v"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    path.write_text(proc.stdout + proc.stderr, encoding="utf-8")
    return proc.returncode


def write_global_isolation(path: Path) -> None:
    from china_policy_track.sq3 import score_input

    global_paths = _global_data_paths()
    before = _shasum_lines(global_paths)

    score_input((REPO_ROOT / "china_policy_track/examples/sample_perplexity_export.txt").read_text())
    score_input(
        json.loads(
            (REPO_ROOT / "china_policy_track/examples/sample_koyfin_export.json").read_text()
        )
    )

    after = _shasum_lines(global_paths)
    package_hits = _scan_china_policy_imports()

    lines = [
        "=== Verification plan step 4: Global isolation ===",
        f"SQ3 commit range base: {SQ3_BASE_REF}..HEAD",
        "",
        "--- Command: git diff --name-only 703610b..HEAD ---",
        _run_git(["diff", "--name-only", f"{SQ3_BASE_REF}..HEAD"]),
        "",
        "--- Command: git diff 703610b..HEAD -- 04_Score_Calculation/ ---",
        _run_git(["diff", f"{SQ3_BASE_REF}..HEAD", "--", "04_Score_Calculation/"]) or "(no diff)",
        "",
        "--- Command: git diff 703610b..HEAD -- data/global/ ---",
        _run_git(["diff", f"{SQ3_BASE_REF}..HEAD", "--", "data/global/"]) or "(no diff)",
        "",
        "--- Command: AST import scan china_policy_track/*.py (excludes tests/, verify_sq3_goal.py) ---",
    ]
    if package_hits:
        for rel, lineno, marker in package_hits:
            lines.append(f"HIT {rel}:{lineno}: {marker}")
    else:
        lines.append("(no matches)")

    ls_proc = subprocess.run(
        ["ls", "-la", "data/global/", "data/global/v1/"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    lines.extend(
        [
            "",
            "--- Command: ls -la data/global/ data/global/v1/ ---",
            ls_proc.stdout.strip(),
            "",
            "--- shasum data/global files (before score_input x2) ---",
            *before,
            "",
            "--- shasum data/global files (after score_input x2) ---",
            *after,
            "",
            "data/global checksums: "
            + ("UNCHANGED" if before == after else "CHANGED"),
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 1:
        print("usage: python3 -m china_policy_track.verify_sq3_goal <scratch_dir>", file=sys.stderr)
        return 2

    scratch = Path(args[0])
    scratch.mkdir(parents=True, exist_ok=True)

    write_sq3_output(scratch / "sq3_output.log")
    write_sq3_methodology(scratch / "sq3_methodology.txt")
    test_rc = write_china_tests(scratch / "china_tests.log")
    write_global_isolation(scratch / "global_isolation.txt")

    print(f"verify_sq3_goal_ok scratch={scratch}")
    print(f"artifacts: sq3_output.log sq3_methodology.txt china_tests.log global_isolation.txt")
    return test_rc


if __name__ == "__main__":
    raise SystemExit(main())