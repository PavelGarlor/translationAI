# translationAI

Certified-translation assistant that runs in Claude Code. `CLAUDE.md` holds the role and
workflow; `rules/`, `glossary/` and `doc-types/` hold the knowledge base, which grows as you
confirm corrections.

## What is in git and what is not
| In git (generic, safe) | Only in `confidential/` (gitignored) |
|---|---|
| `CLAUDE.md`, scripts | Source documents, translations (`orders/`) |
| Rules, glossary, country conventions | Example translation pairs (`examples/`) |
| Doc-type rules | Corrections log (`corrections/log.md`) |

`.gitignore` excludes `confidential/` and every document/image type (pdf, docx, jpg, png,
heic, …). A pre-commit hook (`scripts/check_confidential.sh`) blocks them even if forced.

## Set up on a new laptop
```bash
git clone <your-private-repo-url> translationAI
```
```bash
cd translationAI && git config core.hooksPath .githooks
```
```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```
Then copy your `confidential/` folder (moved by your own secure means) into the repo root.
If you start fresh, Claude creates an empty skeleton on first use.

Check nothing confidential is tracked:
```bash
scripts/check_confidential.sh --tracked
```

## Use
1. Open this folder in Claude Code.
2. Put originals in `confidential/orders/<YYYY-MM-DD>-<ref>/source/`.
3. Ask, e.g.: "Translate the birth certificate in order 2026-10-21-smith from Ukrainian into
   German for Germany."
4. Get `output/<doc>_<tgt>.docx`; review; tell Claude your corrections. Confirmed rules are
   written to `rules/` / `glossary/` — commit and push them so the other laptop gets them.
