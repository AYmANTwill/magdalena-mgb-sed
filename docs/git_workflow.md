# Git workflow (quick reference)

This repo is a **living** record — commit at every step so the history documents the project.

## The routine (each work step)

Easiest in **VS Code → Source Control** (`Ctrl+Shift+G`): stage the changed files (`+`), type a short message, **Commit**, then **Sync**.

Or in the terminal, from the repo root:
```
git add -A
git commit -m "Short, imperative message"
git push
```

Good messages: `"Add hydrology notebook"`, `"Q1: IDEAM sediment stations found"`, `"Reclassify soils/land cover -> URH"`.
Commit **small and often** (one block = one commit) — the history then doubles as a progress log for the report.

## At each new understanding/realization step
1. Add a dated entry at the **top** of `docs/progress_journal.md`.
2. Update the relevant `docs/*.md` and the status table in `README.md`.
3. Commit + push.

## Rules of thumb / gotchas learned
- **Never commit secrets.** `cds_keys.txt` and `.cdsapirc` are gitignored — keep them that way.
- **Data isn't versioned.** `data/raw/*` and `data/processed/*` are gitignored (too large); only docs, notebooks and
  `src/` are tracked. Record how to re-obtain data in `docs/08_download_guide.md`.
- **Don't mix VS Code Git and the terminal at the same time** — it can leave a stale `.git/*.lock`. If you see
  "another git process is running", close the other tool and delete the lock: `Remove-Item .git\*.lock`.
- Work in a **short, real path** (e.g. `C:\dev\...`), not inside an app cache folder — long/virtualized paths break git.
- Branch is **`main`**; remote is **`origin`** (`https://github.com/AYmANTwill/magdalena-mgb-sed`).
