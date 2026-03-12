import sys
import os
from datetime import datetime
from pathlib import Path
import yaml
from crontab import CronTab

# The identifier used to mark jobs managed by this tool in the crontab
CRON_COMMENT = "managed_by_yaml_scheduler"

def load_config(config_path: Path) -> dict:
    """Loads and parses the YAML configuration file."""
    if not config_path.exists():
        print(f"Error: Configuration file not found at {config_path}")
        sys.exit(1)

    with open(config_path, 'r') as file:
        try:
            return yaml.safe_load(file) or {}
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML file: {exc}")
            sys.exit(1)

def validate_script(base_dir: Path, script_name: str) -> Path:
    """Ensures the target bash script exists and is executable."""
    script_path = base_dir / script_name
    if not script_path.exists():
        print(f"Error: Bash script '{script_name}' not found in {base_dir}")
        sys.exit(1)
    if not os.access(script_path, os.X_OK):
        print(f"Error: Bash script '{script_path}' is not executable. Run 'chmod +x {script_path}'")
        sys.exit(1)
    return script_path

def backup_crontab(backups_path: Path) -> Path:
    """Saves a raw text backup of the entire user crontab."""
    cron = CronTab(user=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Ensure backup directory exists
    backups_path.mkdir(parents=True, exist_ok=True)

    backup_file = backups_path / f"crontab_{timestamp}.bak"
    content = cron.render()
    with open(backup_file, 'w') as f:
        f.write(content)

    print(f"Full crontab safely backed up to: {backup_file}")
    return backup_file

def clear_jobs():
    """Removes all cron jobs managed by this script."""
    cron = CronTab(user=True)
    cron.remove_all(comment=CRON_COMMENT)
    cron.write()
    print("All managed scheduling jobs have been cleared from crontab.")

def status_jobs():
    """Lists all currently managed cron jobs."""
    cron = CronTab(user=True)
    jobs = list(cron.find_comment(CRON_COMMENT))

    if not jobs:
        print("No managed jobs are currently running in crontab.")
        return

    print(f"Found {len(jobs)} managed job(s) in crontab:\n")
    for job in jobs:
        print(f"Schedule: {job.slices.render()}")
        print(f"Command:  {job.command}\n")

def sync_jobs(config_path: Path):
    """Reads the YAML config and synchronizes it with the crontab."""
    config = load_config(config_path)

    global_cfg = config.get('global', {})
    jobs_cfg = config.get('jobs', [])

    if not jobs_cfg:
        print("No jobs found in the configuration file.")
        return

    # Resolve paths, expanding user tilde (~)
    base_dir = Path(global_cfg.get('base_dir', '~/Commands')).expanduser()
    uv_command = Path(global_cfg.get('uv_command', '~/.cargo/bin/uv')).expanduser()
    log_file = Path(global_cfg.get('log_file', '~/Commands/schedule.log')).expanduser()

    # Access user crontab
    cron = CronTab(user=True)

    # --- SAFETY FIRST: Backup before modification ---
    backup_crontab(base_dir)

    # Idempotency: clear existing managed jobs before adding new ones
    cron.remove_all(comment=CRON_COMMENT)

    success_count = 0

    for job in jobs_cfg:
        script_name = job.get('script')
        cron_expression = job.get('cron')
        project_id = job.get('project_id')
        instance_id = job.get('instance_id')

        if not all([script_name, cron_expression, project_id, instance_id]):
            print(f"Warning: Skipping incomplete job entry: {job}")
            continue

        script_path = validate_script(base_dir, script_name)

        # Construct the execution command
        command = (
            f"{script_path} "
            f"--project {project_id} "
            f"--instance {instance_id} "
            f"--uv {uv_command} "
            f">> {log_file} 2>&1"
        )

        # Create the new cron job
        new_job = cron.new(command=command, comment=CRON_COMMENT)

        try:
            new_job.setall(cron_expression)
        except ValueError:
            print(f"Error: Invalid cron expression '{cron_expression}' for script {script_name}")
            sys.exit(1)

        success_count += 1

    cron.write()
    print(f"Successfully synced {success_count} managed job(s) to crontab.")
