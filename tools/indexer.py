#!/usr/bin/env python3
"""
GHS Vector Indexer - Indexes HISTORY.md, BUGS.md, and source code.
Supports: ChromaDB (Local) and Qdrant (Server/Docker).
"""
import os
import sys
import json
import hashlib
import argparse
import re
import yaml
import chromadb
try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models as qmodels
except ImportError:
    QdrantClient = None

def get_project_path(args_path=None):
    return args_path or os.getcwd()

def compute_hash(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def load_ghs_config(project_path):
    """Load configuration from SKILL.md frontmatter."""
    skill_path = os.path.join(project_path, '.agents/skills/git-history/SKILL.md')
    default_config = {
        "languages": ["en", "es"],
        "history_file": "HISTORY.md",
        "bug_file": "BUGS.md",
        "ai_tags": {"history": "#ai-history", "bug": "#ai-bug"},
        "vector_store": {"provider": "chroma"}
    }
    
    if os.path.exists(skill_path):
        try:
            with open(skill_path, 'r') as f:
                content = f.read()
                match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
                if match:
                    frontmatter = yaml.safe_load(match.group(1))
                    return frontmatter.get('config', default_config)
        except Exception as e:
            print(f"⚠️  Could not parse SKILL.md config: {e}")
            
    return default_config

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
    chunks = []
    if not os.path.exists(filepath):
        return chunks
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    current_section = ""
    section_title = "General"
    
    for line in lines:
        if line.startswith('## ') or line.startswith('### '):
            if current_section.strip():
                chunks.append({"id": compute_hash(current_section)[:16], "content": current_section.strip(), "metadata": {"source": os.path.basename(filepath), "section": section_title, "type": "history"}})
            section_title = line.lstrip('#').strip()
            current_section = line + "\n"
        elif line.startswith('| ') and not line.startswith('| :') and not line.startswith('| #'):
            chunks.append({"id": compute_hash(line)[:16], "content": line, "metadata": {"source": os.path.basename(filepath), "section": section_title, "type": "commit_entry"}})
        else:
            current_section += line + "\n"
    
    if current_section.strip():
        chunks.append({"id": compute_hash(current_section)[:16], "content": current_section.strip(), "metadata": {"source": os.path.basename(filepath), "section": section_title, "type": "history"}})
    return chunks

def chunk_source_files(project_path):
    extensions = ['.ts', '.tsx', '.js', '.jsx', '.py', '.rs', '.css', '.html']
    chunks = []
    ignore_dirs = {'.git', 'node_modules', '.venv', '.ai-index', 'target', 'dist', 'build'}
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            if not any(file.endswith(ext) for ext in extensions): continue
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, project_path)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except Exception: continue
            if len(content) > 50000: continue
            lines = content.split('\n')
            block_size = 80
            for i in range(0, len(lines), block_size):
                block = '\n'.join(lines[i:i + block_size])
                if block.strip():
                    chunks.append({"id": compute_hash(f"{rel_path}:{i}")[:16], "content": block, "metadata": {"source": rel_path, "line_start": i + 1, "line_end": min(i + block_size, len(lines)), "type": "source_code"}})
    return chunks

def index_project(project_path):
    index_dir = os.path.join(project_path, '.ai-index')
    os.makedirs(index_dir, exist_ok=True)
    config = load_ghs_config(project_path)
    vstore = config.get('vector_store', {})
    provider = vstore.get('provider', 'chroma')
    
    history_path = os.path.join(project_path, config.get('history_file', 'HISTORY.md'))
    bugs_path = os.path.join(project_path, config.get('bug_file', 'BUGS.md'))
    history_chunks = chunk_history_file(history_path)
    bugs_chunks = chunk_history_file(bugs_path)
    all_history_chunks = history_chunks + bugs_chunks
    code_chunks = chunk_source_files(project_path)

    if provider == 'qdrant':
        if QdrantClient is None:
            print("❌ error: qdrant-client not installed."); return
        client = QdrantClient(url=vstore.get('url', 'http://localhost:6333'))
        col_history = vstore.get('collection_history', 'ghs_history')
        col_code = vstore.get('collection_code', 'ghs_code')
        try:
            client.recreate_collection(collection_name=col_history, vectors_config=qmodels.VectorParams(size=768, distance=qmodels.Distance.COSINE))
            client.recreate_collection(collection_name=col_code, vectors_config=qmodels.VectorParams(size=768, distance=qmodels.Distance.COSINE))
        except Exception as e: print(f"⚠️ Qdrant error: {e}"); return
        
        if all_history_chunks:
            client.upsert(collection_name=col_history, points=[qmodels.PointStruct(id=i, vector=[0.0]*768, payload={"content": c["content"], **c["metadata"]}) for i, c in enumerate(all_history_chunks)])
            print(f"  ✅ Indexed {len(all_history_chunks)} history entries (Qdrant)")
        if code_chunks:
            client.upsert(collection_name=col_code, points=[qmodels.PointStruct(id=i+10000, vector=[0.0]*768, payload={"content": c["content"], **c["metadata"]}) for i, c in enumerate(code_chunks)])
            print(f"  ✅ Indexed {len(code_chunks)} code chunks (Qdrant)")
    else:
        client = chromadb.PersistentClient(path=os.path.join(index_dir, 'chroma_db'))
        history_col = client.get_or_create_collection(name="project_history")
        code_col = client.get_or_create_collection(name="source_code")
        
        if all_history_chunks:
            try: client.delete_collection("project_history"); history_col = client.create_collection("project_history")
            except: pass
            history_col.add(ids=[c["id"] for c in all_history_chunks], documents=[c["content"] for c in all_history_chunks], metadatas=[c["metadata"] for c in all_history_chunks])
            print(f"  ✅ Indexed {len(all_history_chunks)} history entries (Chroma)")
        if code_chunks:
            try: client.delete_collection("source_code"); code_col = client.create_collection("source_code")
            except: pass
            batch_size = 100
            for i in range(0, len(code_chunks), batch_size):
                batch = code_chunks[i:i + batch_size]
                code_col.add(ids=[c["id"] for c in batch], documents=[c["content"] for c in batch], metadatas=[c["metadata"] for c in batch])
            print(f"  ✅ Indexed {len(code_chunks)} code chunks (Chroma)")
    
    manifest = load_manifest(index_dir)
    manifest["indexed_files"] = {"history": len(all_history_chunks), "code": len(code_chunks)}
    save_manifest(index_dir, manifest)
    print(f"\n🎉 Indexing complete! Provider: {provider.upper()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GHS Vector Indexer")
    parser.add_argument("--project-path", default=os.getcwd())
    args = parser.parse_args()
    index_project(args.project_path)
