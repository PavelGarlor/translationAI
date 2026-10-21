#!/bin/sh
# Fails if any staged (or, with --tracked, any tracked) file is confidential:
# anything under confidential/ or any document/image file type.
# Used by .githooks/pre-commit; can also be run by hand.

if [ "$1" = "--tracked" ]; then
  files=$(git ls-files)
else
  files=$(git diff --cached --name-only --diff-filter=ACMR)
fi

bad=$(printf '%s\n' "$files" | grep -Ei '^confidential/|\.(pdf|docx?|odt|rtf|jpe?g|png|heic|tiff?|gif|webp|zip)$')

if [ -n "$bad" ]; then
  echo "BLOCKED: confidential files must never be committed:" >&2
  printf '  %s\n' $bad >&2
  echo "Unstage them with: git restore --staged <file>" >&2
  exit 1
fi
exit 0
