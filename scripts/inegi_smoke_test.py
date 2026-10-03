"""Smoke test no destructivo para DENUE."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "apps" / "api"))

from app.inegi.config import InegiSettings  # noqa: E402
from app.inegi.denue import DenueClient, DenueError  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--real", action="store_true", help="hacer una consulta real a DENUE")
    parser.add_argument("--condition", default="tecnologia")
    parser.add_argument("--entity", default="05", help="clave de Coahuila")
    args = parser.parse_args()
    settings = InegiSettings.from_env()
    if not args.real:
        print("SKIP: modo seguro; use --real para consultar DENUE.")
        print("CONFIG: token=" + ("presente" if settings.denue_token else "ausente"))
        return 0
    if not settings.denue_token:
        print("BLOCKED: falta INEGI_DENUE_TOKEN; no se hizo una llamada real.")
        return 2
    try:
        rows = DenueClient(settings).search_entity(args.condition, args.entity, 1, 10)
    except DenueError as exc:
        print(f"FAIL: {exc}")
        return 1
    print(f"PASS: DENUE respondió con {len(rows)} registros.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
