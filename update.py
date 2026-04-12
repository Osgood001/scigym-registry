#!/usr/bin/env python3
"""
SciGym Registry Updater
Queries GitHub for repos with topic:scigym-research-env,
reads scigym.json manifests, and updates README.md.
"""
import json, os, base64, urllib.request
from datetime import datetime, timezone

GITHUB_API = "https://api.github.com"
TOPIC = "scigym-research-env"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

def gh_get(url):
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "scigym-registry/1.0")
    if GITHUB_TOKEN:
        req.add_header("Authorization", f"Bearer {GITHUB_TOKEN}")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def fetch_scigym_json(owner, repo):
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/scigym.json"
    try:
        data = gh_get(url)
        return json.loads(base64.b64decode(data["content"]).decode())
    except Exception:
        return None

def main():
    url = f"{GITHUB_API}/search/repositories?q=topic:{TOPIC}&sort=updated&per_page=50"
    repos = gh_get(url).get("items", [])

    rows = []
    for r in repos:
        owner = r["owner"]["login"]
        repo  = r["name"]
        sg = fetch_scigym_json(owner, repo)

        rows.append({
            "name":      f"[{repo}]({r['html_url']})",
            "domain":    sg["domain"] if sg else "—",
            "benchmark": "✅" if sg and sg.get("benchmark", {}).get("validated") else "—",
            "fidelity":  "/".join(sg["simulator"]["fidelity_levels"]) if sg else "—",
            "hardware":  "✅" if sg and sg.get("hardware_interface", {}).get("available") else "⚙️",
            "autorun":   "✅" if sg and sg.get("autorun", {}).get("ready") else "—",
            "stars":     r.get("stargazers_count", 0),
            "updated":   r["pushed_at"][:10],
        })

    rows.sort(key=lambda x: x["stars"], reverse=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    header = f"""# SciGym Registry

> Auto-updated index of **SciGym** environments — agent-facing research gyms that combine
> paper/hardware-verified benchmarks, physics-based simulators, real hardware interfaces,
> and optional 24/7 autonomous experimentation via [Cryochamber](https://github.com/nickel-org/cryochamber).
>
> Last updated: {now} · {len(rows)} environments

## Add Your Gym

1. Add `scigym.json` to your repo root — [template →](scigym.json.template)
2. Add GitHub topic **`scigym-research-env`** to your repo settings
3. Your repo appears here automatically within 24 h

```bash
# Quick way via gh CLI:
gh api repos/OWNER/REPO/topics -X PUT \\
  -f 'names[]=scigym-research-env'
```

---

## Environments

| Repo | Domain | Benchmark | Sim Fidelity | Hardware | AutoRun | ⭐ | Updated |
|------|--------|-----------|-------------|----------|---------|-----|---------|
"""
    table = "".join(
        f"| {r['name']} | {r['domain']} | {r['benchmark']} | {r['fidelity']} "
        f"| {r['hardware']} | {r['autorun']} | {r['stars']} | {r['updated']} |\n"
        for r in rows
    )

    footer = """
---

## Column Legend

| Column | Meaning |
|--------|---------|
| Benchmark | ✅ paper/hardware-validated, independent of the sim |
| Sim Fidelity | Available fidelity levels (low / medium / high) |
| Hardware | ✅ real hardware backend available |
| AutoRun | ✅ [Cryochamber](https://github.com/nickel-org/cryochamber)-ready for 24/7 agent experiments |

---

*Auto-maintained via [GitHub Actions](.github/workflows/update.yml).*
"""

    with open("README.md", "w") as f:
        f.write(header + table + footer)
    print(f"README updated: {len(rows)} envs.")

if __name__ == "__main__":
    main()
