GitHub Projects Automation
=========================

This script automates GitHub Projects issue management, allowing you to create new issues and move them between columns using keywords in commit messages.

Keywords
--------
- #backlog  -> Moves the issue to "Backlog" column
- #ready    -> Moves the issue to "Ready" column
- #in-progress -> Moves the issue to "In progress" column
- #review   -> Moves the issue to "In review" column
- #done     -> Moves the issue to "Done" column

Usage
-----
1. Create a new issue:
   ```bash
   python3 github_project_automation.py "Implement new feature #in-progress"
   ```

2. Move an existing issue:
   ```bash
   python3 github_project_automation.py "Update documentation #done #123"
   ```

Examples
--------
1. Create a new issue and move it to "In progress":
   ```bash
   python3 github_project_automation.py "Implement authentication system #in-progress"
   ```

2. Move an existing issue to "Done":
   ```bash
   python3 github_project_automation.py "Complete task #done #456"
   ```

3. Create an issue and move it to "Backlog":
   ```bash
   python3 github_project_automation.py "New feature idea #backlog"
   ```

Notes
-----
- The script requires a GitHub token with permissions to manage issues and projects
- The token must be configured in the .env file
- The columns must exist in your GitHub project
- The project number must be configured in the script 