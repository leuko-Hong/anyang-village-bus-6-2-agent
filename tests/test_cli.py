from __future__ import annotations

import subprocess


def test_cli_happy_path() -> None:
    proc = subprocess.run(
        ["uv", "run", "--active", "python", "-m", "app.cli", "--audio", "fixtures/query-geumjeong.wav"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "가장 가까운 버스" in proc.stdout
    assert "다음 버스" in proc.stdout


def test_cli_happy_path_with_user_location() -> None:
    proc = subprocess.run(
        [
            "uv",
            "run",
            "--active",
            "python",
            "-m",
            "app.cli",
            "--audio",
            "fixtures/query-geumjeong.wav",
            "--user-lat",
            "37.399",
            "--user-lon",
            "126.924",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "가장 가까운 버스: GG70A1002" in proc.stdout
    assert "다음 버스: GG70A1003" in proc.stdout


def test_cli_rejects_partial_user_location() -> None:
    proc = subprocess.run(
        [
            "uv",
            "run",
            "--active",
            "python",
            "-m",
            "app.cli",
            "--audio",
            "fixtures/query-geumjeong.wav",
            "--user-lat",
            "37.399",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode != 0
    assert "Both --user-lat and --user-lon must be provided together." in proc.stdout


def test_cli_audio_not_found() -> None:
    proc = subprocess.run(
        ["uv", "run", "--active", "python", "-m", "app.cli", "--audio", "fixtures/absent.wav"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode != 0
    assert "AUDIO_FILE_NOT_FOUND" in proc.stdout or "AUDIO_FILE_NOT_FOUND" in proc.stderr
