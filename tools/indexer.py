#!/usr/bin/env python3
"""
GHS Vector Indexer - Indexes HISTORY.md, BUGS.md, and source code into a local ChromaDB.
Usage: python3 tools/indexer.py [--project-path /path/to/project]
"""
import os
import sys
import json
import hashlib
import argparse
import chromadb

def get_project_path(args_path=None):
    return args_path or os.getcwd()

def compute_hash(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def load_manifest(index_dir):
    manifest_path = os.path.join(index_dir, 'manifest.json')
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r') as f:
            return json.load(f)
    return {"indexed_files": {}, "last_updated": ""}

def save_manifest(index_dir, manifest):
    from datetime import datetime
    manifest["last_updated"] = datetime.now().isoformat()
    with open(os.path.join(index_dir, 'manifest.json'), 'w') as f:
        json.dump(manifest, f, indent=2)

def chunk_history_file(filepath):
    """Split HISTORY.md or BUGS.md into individual entries."""
    chunks = []
    if not os.path.exists(filepath):
        return chunks
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by table rows (| # | message |)
    lines = content.split('\n')
    current_section = ""
    section_title = "General"
    
    for line in lines:
        if line.startswith('## ') or line.startswith('### '):
            if current_section.strip():
                chunks.append({
                    "id": compute_hash(current_section)[:16],
                    "content": current_section.strip(),
                    "metadata": {
                        "source": os.path.basename(filepath),
                        "section": section_title,
                        "type": "history"
                    }
                })
            section_title = line.lstrip('#').strip()
            current_section = line + "\n"
        elif line.startswith('| ') and not line.startswith('| :') and not line.startswith('| #'):
            # This is a table data row (commit entry)
            chunks.append({
                "id": compute_hash(line)[:16],
                "content": line,
                "metadata": {
                    "source": os.path.basename(filepath),
                    "section": section_title,
                    "type": "commit_entry"
                }
            })
        else:
            current_section += line + "\n"
    
    # Add last section
    if current_section.strip():
        chunks.append({
            "id": compute_hash(current_section)[:16],
            "content": current_section.strip(),
            "metadata": {
                "source": os.path.basename(filepath),
                "section": section_title,
                "type": "history"
            }
        })
    
    return chunks

def chunk_source_files(project_path, extensions=None):
    """Split source code files into function-level chunks."""
    if extensions is None:
        extensions = ['.ts', '.tsx', '.js', '.jsx', '.py', '.rs', '.css', '.html']
    
    chunks = []
    ignore_dirs = {'.git', 'node_modules', '.venv', '.ai-index', 'target', 'dist', 'build'}
    
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        for file in files:
            if not any(file.endswith(ext) for ext in extensions):
                continue
            
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, project_path)
            
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except Exception:
                continue
            
            if len(content) > 50000:
                continue
            
            # Simple chunking: split by blocks of ~80 lines
            lines = content.split('\n')
            block_size = 80
            
            for i in range(0, len(lines), block_size):
                block = '\n'.join(lines[i:i + block_size])
                if block.strip():
                    chunks.append({
                        "id": compute_hash(f"{rel_path}:{i}")[:16],
                        "content": block,
                        "metadata": {
                            "source": rel_path,
                            "line_start": i + 1,
                            "line_end": min(i + block_size, len(lines)),
                            "type": "source_code"
                        }
                    })
    
    return chunks

def index_project(project_path):
    """Main indexing function."""
    index_dir = os.path.join(project_path, '.ai-index')
    os.makedirs(index_dir, exist_ok=True)
    
    # Initialize ChromaDB (local persistent storage)
    client = chromadb.PersistentClient(path=os.path.join(index_dir, 'chroma_db'))
    
    # Create or get collections
    history_col = client.get_or_create_collection(
        name="project_history",
        metadata={"description": "Git history, commits, branches, bugs"}
    )
    code_col = client.get_or_create_collection(
        name="source_code",
        metadata={"description": "Source code semantic index"}
    )
    
    manifest = load_manifest(index_dir)
    
    # --- Index HISTORY.md ---
    history_path = os.path.join(project_path, 'HISTORY.md')
    history_chunks = chunk_history_file(history_path)
    
    # --- Index BUGS.md ---
    bugs_path = os.path.join(project_path, 'BUGS.md')
    bugs_chunks = chunk_history_file(bugs_path)
    
    all_history_chunks = history_chunks + bugs_chunks
    
    if all_history_chunks:
        # Clear and re-index history (it's small, so full rebuild is fine)
        try:
            client.delete_collection("project_history")
            history_col = client.create_collection(
                name="project_history",
                metadata={"description": "Git history, commits, branches, bugs"}
            )
        except Exception:
            pass
        
        history_col.add(
            ids=[c["id"] for c in all_history_chunks],
            documents=[c["content"] for c in all_history_chunks],
            metadatas=[c["metadata"] for c in all_history_chunks]
        )
        print(f"  ✅ Indexed {len(all_history_chunks)} history/bug entries")
    
    # --- Index Source Code ---
    code_chunks = chunk_source_files(project_path)
    
    if code_chunks:
        try:
            client.delete_collection("source_code")
            code_col = client.create_collection(
                name="source_code",
                metadata={"description": "Source code semantic index"}
            )
        except Exception:
            pass
        
        # Batch insert (ChromaDB has limits)
        batch_size = 100
        for i in range(0, len(code_chunks), batch_size):
            batch = code_chunks[i:i + batch_size]
            code_col.add(
                ids=[c["id"] for c in batch],
                documents=[c["content"] for c in batch],
                metadatas=[c["metadata"] for c in batch]
            )
        print(f"  ✅ Indexed {len(code_chunks)} code chunks")
    
    # Update manifest
    manifest["indexed_files"] = {
        "HISTORY.md": compute_hash(open(history_path).read()) if os.path.exists(history_path) else "",
        "BUGS.md": compute_hash(open(bugs_path).read()) if os.path.exists(bugs_path) else "",
        "source_files": len(code_chunks)
    }
    save_manifest(index_dir, manifest)
    
    print(f"\n🎉 Indexing complete! Data stored in: {index_dir}/chroma_db")
    print(f"📋 Manifest updated: {index_dir}/manifest.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GHS Vector Indexer")
    parser.add_argument("--project-path", default=os.getcwd(), help="Path to the project root")
    args = parser.parse_args()
    
    print(f"🔍 Indexing project: {args.project_path}")
    index_project(args.project_path)
