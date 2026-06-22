# Terminal Project Management CLI Tool

A lightweight, self-contained, relational project management engine built entirely in Python. This tool features a custom object-relational layer that interacts directly with local JSON flat-files, complete with data validation, cross-file integrity checks, and a dynamic Command Line Interface (CLI).

## 🚀 Key Features

* **Zero Dependencies:** Runs entirely on native Python standard libraries (`json`, `argparse`, `os`, `uuid`).
* **Relational Integrity:** Implements cascading deletes and validation checks (e.g., tasks cannot be assigned to non-existent users or projects).
* **Schema-Immune Serialization:** Custom models filter out legacy or corrupted JSON keys automatically during hydration.
* **Robust Date & Status Controls:** Automatic type handling for tracking project deadlines and task workflows.

---

## 📂 Project Architecture

```text
command_line_project_management_tool/
│
├── data/
│   ├── users.json          # Database flat-file for team members
│   ├── projects.json       # Database flat-file for project tracking
│   └── tasks.json          # Database flat-file for task states
│
├── models/
│   ├── __init__.py
│   ├── user.py             # User schema and formatting logic
│   ├── project.py          # Project schema and date parsing bounds
│   └── task.py             # Task schema and state bounds
│
├── utils/
│   ├── __init__.py
│   └── storage.py          # Serialization engine and file-I/O layers
│
├── main.py                 # CLI Argument parser mapping and controller routing
└── README.md

🛠️ Installation & Setup
Clone the repository to your local environment.

Ensure you have Python 3.8+ installed.

Set up your local database files by running the following commands in your project root folder to ensure empty JSON arrays exist:

Bash
mkdir -p data
echo "[]" > data/users.json
echo "[]" > data/projects.json
echo "[]" > data/tasks.json
💻 CLI Usage Guide
The application uses an explicit sub-command architecture. Run commands from the project root directory.

👤 User Management
Register a new user:

Bash
python3 main.py create-user "alice" "alice@code.com"
Generates a 6-character unique identifier used for referencing associations.

List all registered team members:

Bash
python3 main.py list-users
Delete a user:

Bash
python3 main.py delete-user "<user_id>"
Note: Deleting a user will automatically cleanly unassign them from any tasks they currently own.

📁 Project Management
Create a project workspace:

Bash
python3 main.py create-project "Backend Infrastructure" "<user_id>" --due "2026-12-31" --desc "Setup JSON storage workflows"
Checks for duplicate project naming variations to protect data accuracy.

List all project dashboards:

Bash
python3 main.py list-projects
Delete a project workspace:

Bash
python3 main.py delete-project "<project_id>"
Triggers a cascading delete sequence that automatically purges all orphaned tasks linked to that project.

📋 Task Management
Add a task to a project workspace:

Bash
python3 main.py create-task "<project_id>" "Design Database Schema" --assigned-to "<user_id>" --status "To Do"
List tasks (with optional workspace filters):

Bash
# View all tasks globally
python3 main.py list-tasks

# View tasks scoped to a specific project
python3 main.py list-tasks --project-id "<project_id>"
Update task progress:

Bash
python3 main.py update-task "<task_id>" "In Progress"
Enforces configuration choices strictly via argparse limiting inputs to To Do, In Progress, or Done.