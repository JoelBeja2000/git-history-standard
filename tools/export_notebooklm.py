import os

# Configuration: Files and directories to include/exclude
INCLUDE_EXTENSIONS = {'.md', '.py', '.yaml', '.yml', '.json', '.txt'}
EXCLUDE_DIRS = {'.git', '.venv', '.ai-index', '__pycache__', 'node_modules', 'assets'}
OUTPUT_FILE = 'ghs_context_for_notebooklm.txt'

def generate_notebook_context(root_dir):
    context = []
    
    # Add a global header
    context.append("# PROJECT CONTEXT EXPORT FOR NOTEBOOKLM\n")
    context.append(f"Project Name: {os.path.basename(root_dir)}")
    context.append("Description: Full documentation and source code for the Git History Standard (GHS).\n")
    context.append("="*80 + "\n\n")

    for root, dirs, files in os.walk(root_dir):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            file_ext = os.path.splitext(file)[1]
            if file_ext in INCLUDE_EXTENSIONS:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, root_dir)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    context.append(f"FILE: {relative_path}")
                    context.append("-" * (len(relative_path) + 6))
                    context.append(content)
                    context.append("\n" + "="*80 + "\n")
                except Exception as e:
                    print(f"Skipping {relative_path}: {e}")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(context))
        
    print(f"✅ Success! Context exported to: {OUTPUT_FILE}")
    print(f"👉 Drag and drop this file into your NotebookLM source panel.")

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    generate_notebook_context(project_root)
