# SciGym Registry

> Auto-updated index of **SciGym** environments — agent-facing research gyms that combine
> paper/hardware-verified benchmarks, physics-based simulators, real hardware interfaces,
> and optional 24/7 autonomous experimentation via [Cryochamber](https://github.com/nickel-org/cryochamber).
>
> Last updated: 2026-04-14 08:05 UTC · 0 environments

## Add Your Gym

1. Add `scigym.json` to your repo root — [template →](scigym.json.template)
2. Add GitHub topic **`scigym-research-env`** to your repo settings
3. Your repo appears here automatically within 24 h

```bash
# Quick way via gh CLI:
gh api repos/OWNER/REPO/topics -X PUT \
  -f 'names[]=scigym-research-env'
```

---

## Environments

| Repo | Domain | Benchmark | Sim Fidelity | Hardware | AutoRun | ⭐ | Updated |
|------|--------|-----------|-------------|----------|---------|-----|---------|

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
