from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


def _run(cmd: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return proc.returncode, proc.stdout, proc.stderr


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--save-evidence", action="store_true")
    parser.add_argument("--scenario", default="all")
    args = parser.parse_args()

    out_dir = Path(".sisyphus/evidence")
    out_dir.mkdir(parents=True, exist_ok=True)

    code, out, err = _run(["uv", "run", "--active", "python", "-c", "import sys; print(sys.executable)"])
    if args.save_evidence:
        (out_dir / "task-15-python-path.log").write_text(out + err, encoding="utf-8")
    if code != 0 or "/Users/leuko/vscode/.venv/bin/python3" not in out:
        return 1

    if args.scenario in {"all", "provider_outage"}:
        code, out, err = _run(
            [
                "uv",
                "run",
                "--active",
                "python",
                "-m",
                "app.provider_probe",
                "--mode",
                "live",
                "--base-url",
                "http://10.255.255.1",
            ]
        )
        if args.save_evidence:
            (out_dir / "task-15-qa-provider-outage.log").write_text(out + err, encoding="utf-8")
        if code == 0:
            return 1
        if args.scenario == "provider_outage":
            return 0

    code, out, err = _run(["uv", "run", "--active", "pytest", "-q"])
    if args.save_evidence:
        (out_dir / "task-15-qa-runner-happy.log").write_text(out + err, encoding="utf-8")
    if code != 0:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
