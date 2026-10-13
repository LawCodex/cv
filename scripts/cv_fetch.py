#!/usr/bin/env python3
"""Cabo Verde: Constitution and the legislation offered for download by the Constitutional Court
(tribunalconstitucional.cv, "Legislação" — WP File Download categories): constitutional laws, laws on the
Constitutional Court, judicial organisation laws, codes. PDFs from the Boletim Oficial; files without a usable text
layer are skipped and reported.
Usage: python3 cv_fetch.py [--no-download]"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cv_text as T  # noqa

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(os.path.dirname(REPO), "_raw", "cv")
RETRIEVED = os.environ.get("LC_RETRIEVED", "2026-10-13")
NODL = "--no-download" in sys.argv
SITE = "https://www.tribunalconstitucional.cv"
AJAX = SITE + "/wp-admin/admin-ajax.php?juwpfisadmin=false&action=wpfd&"
CATS = {  # category id -> (listing page, target dir)
    199: (SITE + "/index.php/leis-constitucionais/", "leis-constitucionais"),
    48: (SITE + "/index.php/tribunal-constitucional/", "leis"),
    56: (SITE + "/index.php/complementar/", "codigos"),
    57: (SITE + "/index.php/complementar/", "leis-organicas"),
}
DELAY = 3


def list_cat(cid):
    dest = os.path.join(RAW, "cat%d.json" % cid)
    if not NODL:
        T.fetch(AJAX + "task=files.display&view=files&id=%d" % cid, dest, delay=DELAY)
    return json.load(open(dest)).get("files") or []


def main():
    os.makedirs(os.path.join(RAW, "pdf"), exist_ok=True)
    rep = {"ok": [], "skipped": []}
    for cid, (record, d) in CATS.items():
        for f in list_cat(cid):
            fid, title = f["ID"], T.norm(f["post_title"])
            if cid == 48 and re.sub(r"^\d+\s*-\s*", "", title).startswith("Constituição"):
                continue  # Assembly booklet edition (with index) of the same text as the Boletim Oficial file below
            if cid == 199 and fid != 3369:
                continue  # historical constitutional laws (1975-1999): only the current consolidated text is kept
            url = AJAX + "task=file.download&wpfd_category_id=%d&wpfd_file_id=%d" % (cid, fid)
            pdf = os.path.join(RAW, "pdf", "%d.pdf" % fid)
            if not NODL:
                T.fetch(url, pdf, delay=DELAY, check_pdf=True, timeout=300)
            if not os.path.exists(pdf) or not T.pdf_ok(pdf):
                rep["skipped"].append("%s (download failed)" % title)
                continue
            pages, _ = T.pdf_text_columns(pdf, "por", tmpdir=RAW, ocr=False)
            txt = "\n".join(pages)
            if len(re.sub(r"\s", "", txt)) / max(1, len(pages)) < 400 or T.text_quality(txt) < 0.8:
                rep["skipped"].append("%s (scanned, no usable text layer)" % title)
                continue
            lines = T.clean_pages(pages)
            body = T.structure(lines, "pt")
            clean = re.sub(r"^\d+\s*-\s*", "", title)
            if cid == 199 or (cid == 48 and clean.startswith("Constituição")):
                rel, typ = "constituicao/" + ("constituicao-2010.md" if cid == 199 else T.slug(clean) + ".md"), "constitution"
            else:
                rel, typ = "%s/%s.md" % (d, T.slug(clean, 80)), ("code" if cid == 56 else "act")
            meta = {"title": clean, "type": typ, "jurisdiction": "cv", "language": "pt", "status": "unknown",
                    "source": url, "record": record, "retrieved": RETRIEVED,
                    "note": "PDF (Boletim Oficial) offered by the Constitutional Court; two-column pages split automatically"}
            if cid == 199:
                meta.update({"title": "Constituição da República de Cabo Verde",
                             "identifier": "Lei Constitucional n.º 1/VII/2010, de 3 de Maio (3.ª revisão da Constituição de 1992)",
                             "date": "2010-05-03", "status": "in_force",
                             "note": "Boletim Oficial I Série n.º 17 of 3 May 2010: the revision law (amended articles) followed by the "
                                     "republished full text of the Constitution; two-column pages split automatically"})
            T.write_md(os.path.join(REPO, rel), meta, meta["title"], body)
            print("OK", rel, sum(1 for x in body if x.startswith("#")))
            rep["ok"].append(rel)
    json.dump(rep, open(os.path.join(RAW, "report.json"), "w"), indent=1, ensure_ascii=False)
    print({k: len(v) for k, v in rep.items()})
    for x in rep["skipped"]:
        print("SKIPPED", x)


if __name__ == "__main__":
    main()
