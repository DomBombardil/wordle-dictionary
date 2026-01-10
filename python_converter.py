import csv
import json
from pathlib import Path

INPUT_FILE = Path("wordle.csv")          # your file
OUTPUT_FILE = Path("translations.json")  # output json

ARTICLES = {"der", "die", "das"}
NO_ARTICLE = {"–", "-", "—", ""}

data = {}

with INPUT_FILE.open("r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f, delimiter="\t")  # because it's tab-separated

    for row in reader:
        rod = (row.get("Rod") or "").strip()
        de_word = (row.get("Njemačka riječ") or "").strip()
        hr = (row.get("Hrvatski prijevod") or "").strip()

        if not de_word or not hr:
            continue  # skip empty/broken rows

        # Join column A + B only if A is an article
        if rod.lower() in ARTICLES:
            key = f"{rod} {de_word}"
        elif rod in NO_ARTICLE:
            key = de_word
        else:
            # If something unexpected appears in Rod, keep it but don't break
            key = f"{rod} {de_word}".strip()

        # Avoid silent overwrites
        if key in data and data[key] != hr:
            print(f"Duplicate key with different value: {key!r}")
            print(f"  Existing: {data[key]!r}")
            print(f"  New:      {hr!r}")
            continue

        data[key] = hr

OUTPUT_FILE.write_text(
    json.dumps(data, ensure_ascii=False, indent=4),
    encoding="utf-8"
)

print(f"Saved {len(data)} entries to {OUTPUT_FILE}")
