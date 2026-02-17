from __future__ import annotations

import argparse
import sys

from .analytics import build_funnel_metrics
from .db import connect, init_db
from .models import ApplicationStatus
from .repository import ApplicationRepository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="jobtracker", description="Track job applications and report funnel metrics.")
    parser.add_argument("--db", default="applications.db", help="Path to SQLite database file")

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init-db", help="Create required database tables")

    add = sub.add_parser("add", help="Add a new job application")
    add.add_argument("--company", required=True)
    add.add_argument("--role", required=True)
    add.add_argument("--source", default="unknown")
    add.add_argument("--applied-date", default=None)
    add.add_argument("--notes", default="")

    list_cmd = sub.add_parser("list", help="List applications")
    list_cmd.add_argument("--status", choices=[s.value for s in ApplicationStatus], default=None)

    update = sub.add_parser("update-status", help="Update status for an existing application")
    update.add_argument("--id", type=int, required=True)
    update.add_argument("--status", choices=[s.value for s in ApplicationStatus], required=True)

    sub.add_parser("stats", help="Show funnel metrics")

    export_cmd = sub.add_parser("export-csv", help="Export applications to CSV")
    export_cmd.add_argument("--output", required=True)

    import_cmd = sub.add_parser("import-csv", help="Import applications from CSV")
    import_cmd.add_argument("--input", required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    conn = connect(args.db)
    repo = ApplicationRepository(conn)

    if args.command == "init-db":
        init_db(conn)
        print(f"Initialized database at {args.db}")
        return 0

    init_db(conn)

    if args.command == "add":
        app_id = repo.add_application(
            company=args.company,
            role=args.role,
            source=args.source,
            applied_date=args.applied_date,
            notes=args.notes,
        )
        print(f"Added application #{app_id}")
        return 0

    if args.command == "list":
        rows = repo.list_applications(status=args.status)
        if not rows:
            print("No applications found")
            return 0
        for row in rows:
            print(f"{row.id:>3} | {row.applied_date} | {row.company:<24} | {row.role:<24} | {row.status}")
        return 0

    if args.command == "update-status":
        changed = repo.update_status(args.id, args.status)
        if not changed:
            print(f"Application #{args.id} not found")
            return 1
        print(f"Updated application #{args.id} to '{args.status}'")
        return 0

    if args.command == "stats":
        metrics = build_funnel_metrics(repo.iter_all())
        print(f"Total applications:     {metrics.total}")
        print(f"Interview-stage count: {metrics.interviews}")
        print(f"Offers:                {metrics.offers}")
        print(f"Rejected:              {metrics.rejected}")
        print(f"Response rate:         {metrics.response_rate:.1%}")
        print(f"Offer rate:            {metrics.offer_rate:.1%}")
        print(f"Avg days to update:    {metrics.avg_days_to_update}")
        return 0

    if args.command == "export-csv":
        total = repo.export_csv(args.output)
        print(f"Exported {total} applications to {args.output}")
        return 0

    if args.command == "import-csv":
        imported = repo.import_csv(args.input)
        print(f"Imported {imported} applications from {args.input}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
