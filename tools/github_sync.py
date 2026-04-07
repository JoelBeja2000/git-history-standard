import subprocess
import json
import sys
import os
import re
from datetime import datetime

class GitHubSync:
    def __init__(self):
        self.skill_file = ".agents/skills/git-history/SKILL.md"

    def is_enabled(self):
        try:
            with open(self.skill_file, "r") as f:
                content = f.read()
                match = re.search(r"github:[\s\S]*?enabled:\s*(true|false)", content, re.IGNORECASE)
                if match:
                    return match.group(1).lower() == "true"
        except:
            pass
        return True

    def get_repo_info(self):
        try:
            result = subprocess.run(['gh', 'repo', 'view', '--json', 'owner,name'], capture_output=True, text=True)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return data['owner']['login'], data['name']
        except:
            pass
        return None, None

    def ensure_project(self, owner, repo_name):
        title = f"GHS: {repo_name}"
        try:
            # Check for existing project
            print(f"Checking for Project: {title}...")
            result = subprocess.run(['gh', 'project', 'list', '--owner', owner, '--format', 'json'], capture_output=True, text=True)
            if result.returncode == 0:
                projects = json.loads(result.stdout)
                for p in projects:
                    if p['title'] == title:
                        return p['number']
                
            # Try to create project
            print(f"Creating new Project V2: {title}...")
            result = subprocess.run(['gh', 'project', 'create', '--owner', owner, '--title', title], capture_output=True, text=True)
            if result.returncode == 0:
                # Get the number of the newly created project
                result = subprocess.run(['gh', 'project', 'list', '--owner', owner, '--format', 'json'], capture_output=True, text=True)
                projects = json.loads(result.stdout)
                for p in projects:
                    if p['title'] == title:
                        return p['number']
        except Exception as e:
            print(f"Warning: Could not manage Project V2 (Check gh auth scope write:project): {e}")
        return None

    def add_to_project(self, project_number, owner, issue_url):
        try:
            print(f"Adding to Project #{project_number}...")
            subprocess.run(['gh', 'project', 'item-add', str(project_number), '--owner', owner, '--url', issue_url], capture_output=True)
        except:
            pass

    def parse_bugs(self):
        bugs = []
        try:
            with open("BUGS.md", "r") as f:
                content = f.read()
                # Parse markdown table
                lines = content.split('\n')
                for line in lines:
                    if '|' in line and 'Bug ID' not in line and '---' not in line:
                        parts = [p.strip() for p in line.split('|')]
                        if len(parts) >= 5:
                            bugs.append({
                                'id': parts[1],
                                'author': parts[2],
                                'description': parts[3],
                                'fix_details': parts[4]
                            })
        except:
            pass
        return bugs

    def get_issue_number(self, title):
        try:
            result = subprocess.run(['gh', 'issue', 'list', '--search', f'"{title}" in:title', '--json', 'number'], capture_output=True, text=True)
            if result.returncode == 0:
                issues = json.loads(result.stdout)
                if issues:
                    return issues[0]['number']
        except:
            pass
        return None

    def sync(self, bugs_only=False, dev_only=False):
        if not self.is_enabled():
            print("GitHub Sync is disabled.")
            return

        owner, repo_name = self.get_repo_info()
        project_number = self.ensure_project(owner, repo_name) if owner else None

        if not dev_only:
            print("Syncing Bugs...")
            bugs = self.parse_bugs()
            for bug in bugs:
                title = f"BUG: {bug['description'][:50]}"
                body = f"### Description\n{bug['description']}\n\n### Fix Details\n{bug['fix_details'] or 'Pending'}\n\n---\n*Synced by GHS*"
                
                issue_num = self.get_issue_number(title)
                if issue_num:
                    subprocess.run(['gh', 'issue', 'edit', str(issue_num), '--body', body])
                else:
                    print(f"Creating issue: {title}")
                    result = subprocess.run(['gh', 'issue', 'create', '--title', title, '--body', body, '--label', 'bug'], capture_output=True, text=True)
                    if result.returncode == 0 and project_number:
                        issue_url = result.stdout.strip()
                        self.add_to_project(project_number, owner, issue_url)

        if not bugs_only:
            print("Syncing Dev Status...")
            title = "GHS Development Status"
            branches = subprocess.check_output(['git', 'branch', '-a'], text=True)
            stashes = subprocess.check_output(['git', 'stash', 'list'], text=True)
            body = f"## Active Branches\n```\n{branches}\n```\n\n## Stashed Changes\n```\n{stashes}\n```\n\n---\n*Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
            
            issue_num = self.get_issue_number(title)
            if issue_num:
                subprocess.run(['gh', 'issue', 'edit', str(issue_num), '--body', body])
            else:
                result = subprocess.run(['gh', 'issue', 'create', '--title', title, '--body', body, '--label', 'ghs-status'], capture_output=True, text=True)
                if result.returncode == 0 and project_number:
                    issue_url = result.stdout.strip()
                    self.add_to_project(project_number, owner, issue_url)

if __name__ == "__main__":
    sync = GitHubSync()
    bugs_opt = "--bugs" in sys.argv
    dev_opt = "--dev" in sys.argv
    sync.sync(bugs_only=bugs_opt, dev_only=dev_opt)
