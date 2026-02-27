# Watcher Sub-Feature Refactor Plan

## Goal

1. Make the bus watcher callable as a stable sub-feature by another agent.
2. Separate human-facing output (`print`/`say`) from machine-facing output (JSON contract).
3. Keep current BUS_WATCHER usage flow working.

## Refactor Steps

1. Define call contract
2. Finalize `WatchResult` schema:
   - `status`
   - `message`
   - `nearest_seq`
   - `nearest_name`
   - `eta_min`
   - `should_alert`
   - `timestamp`
3. Define status codes:
   - `OK`
   - `NO_BUS`
   - `ALERT_TRIGGERED`
   - `TIMEOUT`
   - `ERROR`

4. Split core logic
5. Move pure watcher logic from `app/watcher.py` into `app/watcher_service.py` (new).
6. Implement return-value-based functions:
   - `run_once()`
   - `watch_until_alert()`
7. Keep `print`, `say`, `argparse` out of service layer.

8. Improve dependency boundaries
9. Inject provider, location resolver, and TTS behavior through interfaces/callbacks.
10. Remove absolute `.env` hardcoding and use default `load_config()` or `--env-path`.

11. Reshape CLI adapter
12. Keep `app/watcher.py` focused on CLI entrypoint.
13. Add CLI options:
   - `--json`
   - `--once`
   - `--no-tts`
   - `--env-path`
14. Preserve compatibility for existing options:
   - `--test`
   - `--interval`
   - `--alert-min`
   - `--alert-max`
   - `--max-duration`

15. Update entrypoint and docs
16. Add script entry:
   - `bus-watcher = "app.watcher:main"` in `pyproject.toml`
17. Update `BUS_WATCHER.md` with agent-call examples (`--json`).
18. Add sub-feature invocation section in `README.md`.

19. Expand tests
20. Add `watcher_service` unit tests.
21. Add JSON contract tests.
22. Add edge tests for timeout/no bus/alert boundaries.

## Done Criteria

1. Another agent can make decisions using `bus-watcher --json` output only.
2. Existing manual flow (`scripts/watch_bus.sh`) still works.
3. Tests pass and documented commands are reproducible.
