import argparse
from pathlib import Path
from bash_scripts_scheduler.core import sync_jobs, clear_jobs, status_jobs

def main():
    parser = argparse.ArgumentParser(
        description="A declarative cron scheduler for Bash scripts via YAML.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Global arguments
    parser.add_argument(
        "-c", "--config",
        type=str,
        default="~/Commands/schedule.yaml",
        help="Path to the schedule.yaml file (default: ~/Commands/schedule.yaml)"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Sync command
    subparsers.add_parser("sync", help="Read the YAML and apply jobs to crontab")

    # Clear command
    subparsers.add_parser("clear", help="Remove all managed jobs from crontab")

    # Status command
    subparsers.add_parser("status", help="List all currently managed jobs in crontab")

    args = parser.parse_args()
    config_path = Path(args.config).expanduser()

    if args.command == "sync":
        sync_jobs(config_path)
    elif args.command == "clear":
        clear_jobs()
    elif args.command == "status":
        status_jobs()

if __name__ == "__main__":
    main()
