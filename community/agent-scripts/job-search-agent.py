#!/usr/bin/env python3
"""
job-search-agent.py — build your own AI agent to search for jobs.

One web-search feed over live LinkedIn job postings (Google-style queries).
Requires ONE free API key (Brave Search): https://brave.com/search/api/
    export BRAVE_API_KEY=*** 
Zero other dependencies (Python 3 stdlib only).

Full guide: https://www.welinktalent.com/post/build-your-agent-to-search-for-jobs
"""
import json, os, urllib.parse, urllib.request

PROFILE = {
    "roles":        ["data analyst", "data engineer", "machine learning", "ai"],
    "locations":    ["singapore", "remote"],
    "must_have":    ["python", "sql"],
    "dealbreakers": ["night shift"],
}

QUERIES = [
    'site:linkedin.com/jobs/view "data analyst" remote',
    'site:linkedin.com/jobs/view "data engineer" Singapore',
]

def search(query, count=20):
    url = "https://api.search.brave.com/res/v1/web/search?" + urllib.parse.urlencode(
        {"q": query, "count": count})
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "X-Subscription-Token": os.environ["BRAVE_API_KEY"]})
    data = json.loads(urllib.request.urlopen(req, timeout=15).read())
    return data.get("web", {}).get("results", [])

def score(job):
    text = (job.get("title", "") + " " + job.get("description", "")).lower()
    if any(d in text for d in PROFILE["dealbreakers"]): return 0
    if not any(l in text for l in PROFILE["locations"]): return 0
    return sum(1 for r in PROFILE["roles"] if r in text) + sum(1 for m in PROFILE["must_have"] if m in text)

def main():
    shortlist = []
    for q in QUERIES:
        for r in search(q):
            shortlist.append((score(r), r))
    shortlist.sort(key=lambda x: x[0], reverse=True)
    shown = 0
    for s, r in shortlist:
        if s >= 1:
            print(f"[{s}] {r.get('title','')}\n      {r.get('url','')}")
            shown += 1
        if shown >= 10: break
    print(f"\n--- {len(shortlist)} results scanned, {shown} shortlisted ---")

if __name__ == "__main__":
    main()
