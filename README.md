# bash_scripts_scheduler

This is a solid foundation for a lightweight, declarative cron management system with a YAML file to define schedules. It allows you to manage your system's crontab entries using a simple configuration file and a Makefile.

## Prerequisites

- **Python 3**
- [**uv**](https://github.com/astral-sh/uv) - An extremely fast Python package and project manager.

## Quick Start

### 1. Initialization

First, initialize the scheduler by running:

```bash
make init
```

This command will:
- Create a `~/Commands` directory if it does not exist.
- Copy a template configuration file (`schedule.yaml`) and a sample script (`dummy_task.sh`) to `~/Commands`.
- Set execution permissions for the sample script.

### 2. Configuration

Next, navigate to `~/Commands` and edit the `schedule.yaml` file to define your jobs.

```bash
cd ~/Commands
nano schedule.yaml
```

**Example `schedule.yaml`:**
```yaml
global:
  uv_command: "~/.local/bin/uv" # Adjust this if your uv binary is located elsewhere. (You can check using `which uv`)
  base_dir: "~/Commands"
  log_file: "~/Commands/schedule.log"

jobs:
  - script: "dummy_task.sh"
    cron: "* * * * *"  # Runs every minute
    project_id: "news_weaver"
    instance_id: "dev_local"

  - script: "my_custom_script.sh"
    cron: "0 5 * * *"  # Runs daily at 5:00 AM
    project_id: "analytics"
    instance_id: "prod_server"
```

- **`global`**: Contains global settings such as the path to the `uv` executable, the base directory for scripts, and the log file location.
- **`jobs`**: A list of jobs to schedule. Each job specifies the `script` (must be located in `base_dir`), a `cron` expression, and optional metadata like `project_id` and `instance_id`.

### 3. Execution (Syncing Jobs)

Once your `schedule.yaml` is configured, apply the jobs to your system's crontab by returning to the project directory and running:

```bash
make sync
```

This reads the YAML configuration and updates your crontab automatically.

## Managing Jobs

The included `Makefile` provides several commands to manage your scheduled tasks:

- **`make status`**: List all currently managed jobs in your crontab.
- **`make clear`**: Remove **all** managed jobs from the crontab.
- **`make backup`**: Manually backup the entire current crontab to `~/Commands/crontab_backups`.
- **`make logs`**: Tail the execution log file (`~/Commands/schedule.log`) to monitor job executions.
- **`make help`**: Show the help menu with all available commands.
