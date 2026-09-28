#!/usr/bin/env python3
"""Merge translated batch JSON back into a Polyglot TranslationTable_XML.

Untranslated entries fall back to the English source so the mod always loads.
--validate reports coverage and tag/placeholder parity between source and value.
"""
import argparse
import glob
import json
import os
import re
import xml.etree.ElementTree as ET
from collections import Counter

from prepare_batches import iter_entries
from apply_names import apply_names

TAG_RE = re.compile(r"</?[^<>]+?>")


def tag_counts(s):
    c = Counter(TAG_RE.findall(s))
    c["\\n"] = s.count("\\n")
    return c


def load_translations(folder):
    out = {}
    for path in sorted(glob.glob(os.path.join(folder, "*.json"))):
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        entries = data.get("entries", data) if isinstance(data, dict) else data
        for e in entries:
            if e.get("translation"):
                out[e["id"]] = e["translation"].strip()
    return out


def add_entry(parent, tag, key, value):
    node = ET.SubElement(parent, tag)
    # The game's runtime lookup keys use Windows CRLF internally; XML line-ending
    # normalisation would turn a literal \r into \n, so normalise to CRLF here.
    ET.SubElement(node, "key").text = key.replace("\r\n", "\n").replace("\n", "\r\n")
    ET.SubElement(node, "value").text = value


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--master", default="data/english-master.xml")
    ap.add_argument("--translations", default="data/translations")
    ap.add_argument("--out", default="mod/assets/Translation.xml")
    ap.add_argument("--validate", action="store_true")
    args = ap.parse_args()

    root = ET.parse(args.master).getroot()
    entries = list(iter_entries(root))
    tr = load_translations(args.translations) if os.path.isdir(args.translations) else {}

    out_root = ET.Element("TranslationTable_XML")
    out_root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
    out_root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")

    missing, bad_tags = [], []
    for e in entries:
        value = tr.get(e["id"], e["source"])
        if e["id"] not in tr:
            missing.append(e["id"])
        elif tag_counts(e["source"]) != tag_counts(value):
            bad_tags.append(e["id"])

    for e in entries:
        if e["table"] == "regular":
            add_entry(out_root, "entry", e["key"], tr.get(e["id"], e["source"]))

    ship = ET.SubElement(out_root, "table_shipLog")
    for e in entries:
        if e["table"] == "shiplog":
            add_entry(ship, "TranslationTableEntry", e["key"], tr.get(e["id"], e["source"]))

    ui = ET.SubElement(out_root, "table_ui")
    for e in entries:
        if e["table"] == "ui":
            add_entry(ui, "TranslationTableEntryUI", e["key"], tr.get(e["id"], e["source"]))

    for el in out_root.iter("value"):
        el.text = apply_names(el.text)

    ET.indent(out_root, space="\t")
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    ET.ElementTree(out_root).write(args.out, encoding="utf-8", xml_declaration=True)

    # Preserve the CR in multi-line keys: XML normalises a literal CRLF to LF,
    # so emit the CR as a character reference (&#13;) which the game's XmlDocument
    # reads back as \r, matching the runtime keys.
    with open(args.out, "rb") as fh:
        data = fh.read()
    data = data.replace(b"\r\n", b"&#13;\n")
    with open(args.out, "wb") as fh:
        fh.write(data)

    translated = len(entries) - len(missing)
    print(f"wrote {args.out}: {len(entries)} entries, {translated} translated, {len(missing)} fallback EN")
    if args.validate:
        if bad_tags:
            print(f"TAG/PARITY FAILURES ({len(bad_tags)}):")
            for i in bad_tags[:20]:
                print("  ", i)
        else:
            print("tag/placeholder parity: OK")


if __name__ == "__main__":
    main()
