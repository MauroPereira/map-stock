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
   Note: The text before the keyword will be used as the issue title exactly as written.

2. Move an existing issue:
   ```bash
   python3 github_project_automation.py "Update documentation #done #123"
   ```
   Note: When moving an existing issue, only the issue number and keyword matter. The text before the keyword is ignored.
   This allows you to use the commit message to describe why the issue is being moved, without affecting the issue title.
   Example: "Fixed all bugs and completed testing, ready for production #done #123"

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

4. Move an issue with descriptive commit message:
   ```bash
   python3 github_project_automation.py "Completed all requirements, added unit tests, and documented the changes #done #789"
   ```

Git Hook Setup
-------------
The automation can be triggered automatically using a Git post-commit hook. This hook runs after each commit and processes the commit message to create or move issues.

To set up the hook:
1. Copy the post-commit script to your .git/hooks directory:
   ```bash
   cp map-stock/scripts/post-commit .git/hooks/
   chmod +x .git/hooks/post-commit
   ```

2. After setup, simply use git commit normally:
   ```bash
   git commit -m "Implement new feature #in-progress"
   ```

Important Note: The hook will only run if there are actual changes to commit. If you try to commit without any changes (git add + git commit), the hook won't execute and no issue will be created or moved.

The hook will automatically:
- Read the commit message
- Detect keywords (#backlog, #ready, #in-progress, #review, #done)
- Create a new issue or move an existing one to the corresponding column

Notes
-----
- The script requires a GitHub token with permissions to manage issues and projects
- The token must be configured in the .env file
- The columns must exist in your GitHub project
- The project number must be configured in the script 