#!/usr/bin/env python3
"""
GHS Vector Search - Searches the local ChromaDB for relevant history, bugs, or code.
Usage: python3 tools/search.py "your query here" [--project-path /path/to/project] [--collection history|code|all]
"""
import os
import sys
import json
import argparse
import chromadb

def search_index(project_path, query, collection_name="all", n_results=5):
    """Search the vector index for relevant results."""
    index_dir = os.path.join(project_path, '.ai-index')
    db_path = os.path.join(index_dir, 'chroma_db')
    
    if not os.path.exists(db_path):
        print("❌ No index found. Run 'python3 tools/indexer.py' first.")
        sys.exit(1)
    
    client = chromadb.PersistentClient(path=db_path)
    
    results_all = []
    
    # Search History
    if collection_name in ("history", "all"):
        try:
            history_col = client.get_collection("project_history")
            results = history_col.query(
                query_texts=[query],
                n_results=min(n_results, history_col.count())
            )
            if results and results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    results_all.append({
                        "type": "📜 History/Bug",
                        "content": doc,
                        "source": results['metadatas'][0][i].get('source', 'unknown'),
                        "section": results['metadatas'][0][i].get('section', ''),
                        "distance": results['distances'][0][i] if results.get('distances') else 0
                    })
        except Exception as e:
            if collection_name == "history":
                print(f"⚠️  History collection not found: {e}")
    
    # Search Code
    if collection_name in ("code", "all"):
        try:
            code_col = client.get_collection("source_code")
            results = code_col.query(
                query_texts=[query],
                n_results=min(n_results, code_col.count())
            )
            if results and results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    meta = results['metadatas'][0][i]
                    results_all.append({
                        "type": "💻 Code",
                        "content": doc[:300] + "..." if len(doc) > 300 else doc,
                        "source": meta.get('source', 'unknown'),
                        "lines": f"L{meta.get('line_start', '?')}-L{meta.get('line_end', '?')}",
                        "distance": results['distances'][0][i] if results.get('distances') else 0
                    })
        except Exception as e:
            if collection_name == "code":
                print(f"⚠️  Code collection not found: {e}")
    
    # Sort by relevance (lower distance = more relevant)
    results_all.sort(key=lambda x: x.get('distance', 999))
    
    return results_all

def print_results(results, query):
    """Pretty-print search results."""
    print(f"\n🔎 Search: \"{query}\"")
    print(f"{'─' * 60}")
    
    if not results:
        print("  No results found.")
        return
    
    for i, r in enumerate(results, 1):
        print(f"\n  {i}. {r['type']} — {r['source']}")
        if r.get('section'):
            print(f"     📂 Section: {r['section']}")
        if r.get('lines'):
            print(f"     📍 Lines: {r['lines']}")
        print(f"     📝 {r['content'][:200]}")
        print(f"     🎯 Relevance: {1 - r.get('distance', 0):.1%}")
    
    print(f"\n{'─' * 60}")
    print(f"  Total: {len(results)} results")

def export_json(results, query):
    """Export results as JSON (for AI agent consumption)."""
    output = {
        "query": query,
        "results": results
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GHS Vector Search")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--project-path", default=os.getcwd(), help="Path to the project root")
    parser.add_argument("--collection", choices=["history", "code", "all"], default="all", help="Which collection to search")
    parser.add_argument("--json", action="store_true", help="Output as JSON (for AI agents)")
    parser.add_argument("--limit", type=int, default=5, help="Max results")
    args = parser.parse_args()
    
    results = search_index(args.project_path, args.query, args.collection, args.limit)
    
    if args.json:
        export_json(results, args.query)
    else:
        print_results(results, args.query)
