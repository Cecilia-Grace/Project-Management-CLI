from models.project import Project
from utils.storage import save_projects, load_projects
from datetime import date, datetime

# 1. Create a dummy project
new_proj = Project("Build CLI Tool", "user_abc123", date(2026, 12, 31), "Using Python!")

# 2. Save it
save_projects([new_proj])
print("Saved successfully!")

# 3. Try to load it back
loaded_stuff = load_projects()
print(f"Loaded project: {loaded_stuff[0]}")