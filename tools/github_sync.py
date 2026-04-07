import os
import subprocess
import re
import sys

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(command)}")
        print(f"Error message: {e.stderr}")
        return None

def get_git_branches():
    branches = run_command(["git", "branch", "-a"])
    if not branches:
        return []
    return [b.strip() for b in branches.split("\n")]

def get_git_stash():
    stash_list = run_command(["git", "stash", "list"])
    if not stash_list:
        return []
    return [s.strip() for s in stash_list.split("\n")]

def parse_bugs(bugs_file):
    if not os.path.exists(bugs_file):
        return []
    
    with open(bugs_file, "r") as f:
        content = f.read()
    
    # Simple regex to extract table rows from BUGS.md
    rows = re.findall(r"\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]*)\s*\|", content)
    
    bugs = []
    for row in rows:
        bug_id = row[0].strip()
        # Skip header and separator rows
        if "Bug ID" in bug_id or re.match(r"^:?-+:?$", bug_id):
            continue
        
        bugs.append({
            "id": bug_id,
            "author": row[1].strip(),
            "description": row[2].strip(),
            "details": row[3].strip()
        })
    return bugs

def sync_bugs_with_github(bugs):
    if not bugs:
        print("No bugs found to sync.")
        return
    print("Syncing bugs with GitHub Issues...")
    for bug in bugs:
        # Check if issue already exists
        search_query = f"{bug['id']} in:title"
        existing_issues = run_command(["gh", "issue", "list", "--search", search_query, "--json", "number,title"])
        
        if existing_issues and existing_issues != "[]":
            # Update existing issue if needed (TBD)
            print(f"Issue for bug {bug['id']} already exists.")
            continue
        
        # Create new issue
        title = f"[BUG] {bug['id']}: {bug['description']}"
        body = f"**Author:** {bug['author']}\n\n**Details:** {bug['details']}\n\n*Automatically synced by GHS.*"
        
        print(f"Creating issue: {title}")
        run_command(["gh", "issue", "create", "--title", title, "--body", body, "--label", "bug"])

def sync_dev_status():
    print("Syncing development status...")
    branches = get_git_branches()
    stash = get_git_stash()
    
    status_body = "## 🌿 Development Status (GHS)\n\n"
    
    status_body += "### Branches\n"
    for b in branches:
        if b.startswith("*"):
            status_body += f"- **{b}** (Current)\n"
        else:
            status_body += f"- {b}\n"
    
    status_body += "\n### Stash\n"
    if not stash:
        status_body += "No stashed changes.\n"
    for s in stash:
        status_body += f"- {s}\n"
    
    status_body += "\n*Updated automatically by GHS.*"
    
    # Check if a Dev Status issue exists
    search_query = "GHS Development Status in:title"
    existing_status = run_command(["gh", "issue", "list", "--search", search_query, "--json", "number,title"])
    
    if existing_status and existing_status != "[]":
        import json
        issue_num = json.loads(existing_status)[0]["number"]
        print(f"Updating existing status issue #{issue_num}...")
        run_command(["gh", "issue", "edit", str(issue_num), "--body", status_body])
    else:
        print("Creating new status issue...")
        run_command(["gh", "issue", "create", "--title", "GHS Development Status", "--body", status_body, "--label", "documentation"])

def is_github_sync_enabled():
    skill_file = ".agents/skills/git-history/SKILL.md"
    if not os.path.exists(skill_file):
        # Fallback to current dir if not in standard path
        skill_file = "SKILL.md"
        if not os.path.exists(skill_file):
            return True # Default to True if file missing
    
    try:
        with open(skill_file, "r") as f:
            content = f.read()
            # More flexible search for enabled status
            match = re.search(r"github:[\s\S]*?enabled:\s*(true|false)", content, re.IGNORECASE)
            if match:
                return match.group(1).lower() == "true"
    except Exception as e:
        print(f"Warning: Could not parse SKILL.md for config: {e}")
    
    return True # Default to True

def main():
    if not is_github_sync_enabled():
        print("GitHub synchronization is disabled in SKILL.md.")
        return

    # Check if gh is authenticated
    auth_status = run_command(["gh", "auth", "status"])
    if not auth_status or "Logged in" not in auth_status:
        print("Error: GitHub CLI (gh) is not authenticated. Please run 'gh auth login'.")
        # return # Proceed anyway for now or fail? 

    bugs_file = "BUGS.md"
    bugs = parse_bugs(bugs_file)
    
    if "--bugs" in sys.argv:
        sync_bugs_with_github(bugs)
    elif "--dev" in sys.argv:
        sync_dev_status()
    else:
        # Default behavior
        sync_bugs_with_github(bugs)
        sync_dev_status()

if __name__ == "__main__":
    main()
