#!/usr/bin/env python3
"""Split the base-game English master XML into translatable JSON batches.

Preserves keys byte-for-byte (internal whitespace included) and emits the
decoded source text so translations are easy to read. Stdlib only.
"""
import argparse
import json
import os
import xml.etree.ElementTree as ET

SECTIONS = (("entry", "regular"), ("table_shipLog", "shiplog"), ("table_ui", "ui"))
CHILD = {"table_shipLog": "TranslationTableEntry", "table_ui": "TranslationTableEntryUI"}


def iter_entries(root):
    for tag, table in SECTIONS:
        nodes = root.findall(tag) if tag == "entry" else root.find(tag).findall(CHILD[tag])
        for i, node in enumerate(nodes):
            key = node.findtext("key") or ""
            source = node.findtext("value") or ""
            yield {
                "id": f"{table}:{i}",
                "table": table,
                "key": key.strip(),
                "source": source.strip(),
                "translation": "",
            }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--master", default="data/english-master.xml")
    ap.add_argument("--out", default="data/batches")
    ap.add_argument("--size", type=int, default=60)
    ap.add_argument("--limit", type=int, default=0, help="only emit the first N entries (0 = all)")
    args = ap.parse_args()

    root = ET.parse(args.master).getroot()
    entries = list(iter_entries(root))
    if args.limit:
        entries = entries[: args.limit]

    os.makedirs(args.out, exist_ok=True)
    for f in os.listdir(args.out):
        os.remove(os.path.join(args.out, f))

    n = 0
    for start in range(0, len(entries), args.size):
        batch = entries[start : start + args.size]
        path = os.path.join(args.out, f"batch_{n:03d}.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"batch": n, "entries": batch}, fh, ensure_ascii=False, indent=1)
        n += 1

    print(f"{len(entries)} entries -> {n} batches in {args.out}")
    for table in ("regular", "shiplog", "ui"):
        print(f"  {table}: {sum(1 for e in entries if e['table'] == table)}")


if __name__ == "__main__":
    main()
