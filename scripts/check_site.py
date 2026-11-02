#!/usr/bin/env python3
"""Static checks for the j8d.org root site. Standard library only."""

from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
EXPECTED_DOMAIN = "j8d.org"
REQUIRED_LINKS = {"/nc-trout-stocking/", "/programmerhumor/", "https://github.com/j8d"}
HUMOR_DIR = ROOT / "programmerhumor"
# Uncompressed bytes of the page plus every local file it loads.
HUMOR_BUDGET_BYTES = 150 * 1024


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = None
        self.title = ""
        self.in_title = False
        self.viewport = False
        self.h1_count = 0
        self.links = []
        self.external_resources = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang")
        elif tag == "title":
            self.in_title = True
        elif tag == "meta" and attrs.get("name") == "viewport":
            self.viewport = True
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "a":
            self.links.append(attrs.get("href"))
        elif tag in {"script", "img", "iframe"} and attrs.get("src"):
            self.external_resources.append(attrs["src"])
        elif tag == "link" and attrs.get("rel") != "canonical" and attrs.get("href"):
            self.external_resources.append(attrs["href"])

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def check_humor_page(errors):
    """The /programmerhumor/ page may load its own files, but nothing from elsewhere."""
    html_path = HUMOR_DIR / "index.html"
    page = PageParser()
    page.feed(html_path.read_text())
    if page.lang != "en":
        errors.append("programmerhumor: <html> needs lang=\"en\"")
    if not page.title.strip():
        errors.append("programmerhumor: <title> is empty")
    if not page.viewport:
        errors.append("programmerhumor: viewport meta tag is missing")
    if page.h1_count != 1:
        errors.append(f"programmerhumor: expected exactly one <h1>, found {page.h1_count}")
    if "/" not in page.links:
        errors.append("programmerhumor: missing link back to the directory (/)")

    total = html_path.stat().st_size
    for src in sorted(set(page.external_resources)):
        if src.startswith("data:"):
            continue  # inline, no request
        if "//" in src or src.startswith("/"):
            errors.append(f"programmerhumor: must only load files from its own folder: {src}")
            continue
        asset = HUMOR_DIR / src
        if not asset.is_file():
            errors.append(f"programmerhumor: missing file {src}")
            continue
        total += asset.stat().st_size
    if total > HUMOR_BUDGET_BYTES:
        errors.append(f"programmerhumor: {total} bytes is over the {HUMOR_BUDGET_BYTES} byte budget")
    return total


def main():
    errors = []

    cname = (ROOT / "CNAME").read_text().strip()
    if cname != EXPECTED_DOMAIN:
        errors.append(f"CNAME is {cname!r}, expected {EXPECTED_DOMAIN!r}")
    if not (ROOT / ".nojekyll").exists():
        errors.append(".nojekyll is missing")

    page = PageParser()
    page.feed((ROOT / "index.html").read_text())
    if page.lang != "en":
        errors.append("<html> needs lang=\"en\"")
    if not page.title.strip():
        errors.append("<title> is empty")
    if not page.viewport:
        errors.append("viewport meta tag is missing")
    if page.h1_count != 1:
        errors.append(f"expected exactly one <h1>, found {page.h1_count}")
    if None in page.links or "" in page.links:
        errors.append("every <a> needs a non-empty href")
    missing = REQUIRED_LINKS - set(page.links)
    if missing:
        errors.append(f"missing required links: {sorted(missing)}")
    if page.external_resources:
        errors.append(f"page must not load scripts, styles or media: {page.external_resources}")

    humor_bytes = check_humor_page(errors)

    for error in errors:
        print(f"error: {error}")
    if errors:
        return 1
    print(f"ok: {len(page.links)} links, CNAME {cname}")
    print(f"ok: programmerhumor weighs {humor_bytes} bytes (budget {HUMOR_BUDGET_BYTES})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
