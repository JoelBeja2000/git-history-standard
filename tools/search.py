#!/usr/bin/env python3
"""
GHS Vector Search - Searches ChromaDB or Qdrant.
Supports --json flag for AI agent consumption.
"""
import os
import sys
import json
import argparse
import re
import yaml
import chromadb
try:
    from qdrant_client import QdrantClient
except ImportError:
    QdrantClient = None

def load_ghs_config(project_path):
    skill_path = os.path.join(project_path, '.agents/skills/git-history/SKILL.md')
    default_config = {"vector_store": {"provider": "chroma"}}
    if os.path.exists(skill_path):
        try:
            with open(skill_path, 'r') as f:
                content = f.read()
                match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
                if match:
                    frontmatter = yaml.safe_load(match.group(1))
                    return frontmatter.get('config', default_config)
        except Exception: pass
    return default_config

def search_index(project_path, query, n_results=5):
    config = load_ghs_config(project_path)
    vstore = config.get('vector_store', {})
    provider = vstore.get('provider', 'chroma')
    results_all = []

    if provider == 'qdrant':
        if QdrantClient is None: return [{"type": "❌ Error", "content": "qdrant-client not installed"}]
        client = QdrantClient(url=vstore.get('url', 'http://localhost:6333'))
        for col in [vstore.get('collection_history', 'ghs_history'), vstore.get('collection_code', 'ghs_code')]:
            try:
                hits = client.search(collection_name=col, query_vector=[0.0]*768, limit=n_results) 
                for hit in hits:
                    results_all.append({"type": f"🔍 {col}", "content": hit.payload.get("content", ""), "source": hit.payload.get("source", ""), "score": hit.score})
            except: pass
    else:
        index_dir = os.path.join(project_path, '.ai-index')
        client = chromadb.PersistentClient(path=os.path.join(index_dir, 'chroma_db'))
        for col_name in ["project_history", "source_code"]:
            try:
                col = client.get_collection(col_name)
                res = col.query(query_texts=[query], n_results=n_results)
                for i, doc in enumerate(res['documents'][0]):
                    results_all.append({"type": f"📜 {col_name}", "content": doc, "source": res['metadatas'][0][i].get('source', '')})
            except: pass
    return results_all

def print_results(results, query):
    print(f"\n🔎 Search: \"{query}\"\n{'─' * 40}")
    for i, r in enumerate(results, 1):
        print(f"\n {i}. {r['type']} — {r['source']}\n    📝 {r['content'][:150]}...")
    print(f"\n{'─' * 40}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format for AI agents")
    args = parser.parse_args()
    results = search_index(os.getcwd(), args.query)
    
    if args.json:
        print(json.dumps({"query": args.query, "results": results}, indent=2, ensure_ascii=False))
    else:
        print_results(results, args.query)
