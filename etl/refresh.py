"""Scheduled ETL entry point.

Sprint 1 intentionally performs no data collection. Keeping the scheduled job
successful while empty proves the CI/CD path without requesting broker access.
"""

from datetime import UTC, datetime


def main() -> None:
    print(f"ETL heartbeat: {datetime.now(UTC).isoformat()}")
    print("No sources enabled. Configure an authorized source adapter in Sprint 2.")


if __name__ == "__main__":
    main()
