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

Additional Fields
---------------
You can set additional fields in your commit message using the following format:

1. Priority: #priority:P0, P1, or P2
   Example: #priority:P1

2. Size: #size:XS, S, M, L, or XL
   Example: #size:L

3. Estimate: #estimate:N (where N is a number)
   Example: #estimate:3

4. Start Date: #start:YYYY-MM-DD
   Example: #start:2024-03-20

5. End Date: #end:YYYY-MM-DD
   Example: #end:2024-03-25

6. Assignees: #assign:@user1,@user2
   Example: #assign:@MauroPereira,@otherUser
   Note: You can specify multiple users separated by commas

7. Labels: #label:label1,label2
   Example: #label:bug,feature
   Note: You can specify multiple labels separated by commas

You can combine multiple fields in a single commit message:
git commit -m "Implement new feature #priority:P1 #size:M #estimate:3 #start:2024-03-20 #end:2024-03-25 #assign:@MauroPereira #label:feature,frontend"

Debug Mode
---------
Add #debug-hook to your commit message to see detailed output about what the script is doing. Without this keyword, the script will only show the final result (e.g., "Issue #20 movida a Done").

Usage
-----
1. Create a new issue:
   ```bash
   python3 github_project_automation.py "Implement new feature #in-progress #priority:P0 #size:M #assign:@user1 #label:feature"
   ```
   Note: The text before the keyword will be used as the issue title exactly as written.

2. Move an existing issue:
   ```bash
   python3 github_project_automation.py "Update documentation #done #123"
   ```
   Note: When moving an existing issue, only the issue number and keyword matter. The text before the keyword is ignored.
   This allows you to use the commit message to describe why the issue is being moved, without affecting the issue title.
   Example: "Fixed all bugs and completed testing, ready for production #done #123"

3. Update issue fields:
   ```bash
   python3 github_project_automation.py "Update issue fields #123 #priority:P1 #size:L #estimate:3 #start:2024-03-20 #end:2024-03-25 #assign:@user1,@user2 #label:bug,enhancement"
   ```

4. Debug mode:
   ```bash
   python3 github_project_automation.py "Update issue #done #123 #debug-hook"
   ```

Examples
--------
1. Create a new issue and move it to "In progress":
   ```bash
   python3 github_project_automation.py "Implement authentication system #in-progress #assign:@developer"
   ```

2. Move an existing issue to "Done":
   ```bash
   python3 github_project_automation.py "Complete task #done #456 #label:completed"
   ```

3. Create an issue and move it to "Backlog":
   ```bash
   python3 github_project_automation.py "New feature idea #backlog #assign:@product-owner #label:enhancement"
   ```

4. Move an issue with descriptive commit message:
   ```bash
   python3 github_project_automation.py "Completed all requirements, added unit tests, and documented the changes #done #789 #assign:@tester #label:tested"
   ```

5. Create an issue with all fields:
   ```bash
   python3 github_project_automation.py "Implement new feature #in-progress #priority:P0 #size:M #estimate:2 #start:2024-03-20 #end:2024-03-25 #assign:@developer,@designer #label:feature,frontend"
   ```

6. Debug mode example:
   ```bash
   python3 github_project_automation.py "Update issue with debug info #done #123 #priority:P1 #assign:@reviewer #label:reviewed #debug-hook"
   ```

7. Create an issue with multiple assignees and labels:
   ```bash
   python3 github_project_automation.py "Team task #backlog #assign:@lead,@developer,@designer #label:team,planning,high-priority"
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
- Update any additional fields specified in the commit message

Notes
-----
- The script requires a GitHub token with permissions to manage issues and projects
- The token must be configured in the .env file
- The columns must exist in your GitHub project
- The project number must be configured in the script 