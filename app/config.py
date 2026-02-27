from __future__ import annotations

from dataclasses import dataclass
import os


class ConfigError(ValueError):
    pass


@dataclass(frozen=True)
class AppConfig:
    bus_api_key: str
    bus_api_base_url: str
    bus_route_id: str
    bus_target_direction: str


def _load_env_file(env_path: str) -> dict[str, str]:
    values: dict[str, str] = {}
    with open(env_path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
    return values


def load_config(env_path: str | None = ".env") -> AppConfig:
    env = dict(os.environ)
    if env_path is not None and os.path.exists(env_path):
        env.update(_load_env_file(env_path))

    required = [
        "BUS_API_KEY",
        "BUS_API_BASE_URL",
        "BUS_ROUTE_ID",
        "BUS_TARGET_DIRECTION",
    ]
    missing = [k for k in required if not env.get(k)]
    if missing:
        raise ConfigError("Missing required env vars: " + ", ".join(missing))

    return AppConfig(
        bus_api_key=env["BUS_API_KEY"],
        bus_api_base_url=env["BUS_API_BASE_URL"],
        bus_route_id=env["BUS_ROUTE_ID"],
        bus_target_direction=env["BUS_TARGET_DIRECTION"],
    )
