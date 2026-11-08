#!/usr/bin/env python3
"""Verification tests for sell-your-car-calm-guide.

Run:  python3 tests/run_tests.py
No dependencies beyond the Python standard library.

Checks structure, the license line, internal links, basic HTML hygiene,
secret-free content, and that the site is plainly buildable (i.e., it is
static HTML/CSS with no external asset dependencies).
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "STATUS.md",
    "docs/00-start-here.md",
    "docs/01-pricing-your-car.md",
    "docs/02-title-and-bill-of-sale.md",
    "docs/03-safe-test-drives.md",
    "docs/04-payment-safety.md",
    "docs/05-notify-dmv-and-insurer.md",
    "docs/06-checklists.md",
    "docs/07-templates.md",
    "site/index.html",
    "site/checklists.html",
    "site/styles.css",
    "tests/run_tests.py",
]

EXACT_LICENSE_LINE = "Copyright (c) 2026 Asdale Dynamics, LLC"

SECRET_PATTERNS = [
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key block"),
    (re.compile(r"\b(sk|pk)_[A-Za-z0-9]{20,}\b"), "Stripe-style API key"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"), "GitHub token"),
    (re.compile(r"\bBearer [A-Za-z0-9\-_.]{30,}\b"), "Bearer token"),
]

CJK = re.compile(r"[\u4e00-\u9fff\u3040-\u30ff]")


class TestFailure(Exception):
    pass


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def check(name: str, ok: bool, detail: str = "") -> None:
    if ok:
        print(f"  PASS  {name}")
    else:
        msg = f"  FAIL  {name}" + (f" — {detail}" if detail else "")
        raise TestFailure(msg)


def check_required_files():
    print("Structure:")
    for rel in REQUIRED_FILES:
        check(f"file exists: {rel}", (ROOT / rel).is_file())


def check_license():
    print("License:")
    text = read(ROOT / "LICENSE")
    check("LICENSE contains exact copyright line", EXACT_LICENSE_LINE in text)
    check("LICENSE is MIT", "MIT License" in text and "Permission is hereby granted" in text)
    readme = read(ROOT / "README.md")
    check("README credits Asdale Dynamics, LLC", "Asdale Dynamics, LLC" in readme)


def check_no_user_content_in_readme():
    print("Privacy:")
    # The README must credit the LLC but never contain personal profile details.
    readme = read(ROOT / "README.md")
    check("README does not name private individuals",
          "Dylan Asdale" not in readme)
    for rel in REQUIRED_FILES:
        text = read(ROOT / rel)
        for rx, label in SECRET_PATTERNS:
            check(f"no {label}: {rel}", not rx.search(text))


def check_markdown_links():
    print("Docs internal links:")
    for md in sorted((ROOT / "docs").glob("*.md")):
        text = read(md)
        for target in re.findall(r"\]\(([^)#\s]+)\)", text):
            if target.startswith(("http://", "https://")):
                continue
            dest = (md.parent / target).resolve()
            check(f"link target in {md.name}", dest.is_file(), target)


def check_html_links():
    print("Site internal links:")
    site_dir = ROOT / "site"
    for html in sorted(site_dir.glob("*.html")):
        text = read(html)
        for target in re.findall(r'(?:href|src)="([^"]+)"', text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            dest = (site_dir / target.split("#")[0]).resolve()
            check(f"link target in {html.name}", dest.is_file(), target)
        for anchor in re.findall(r'href="#([\w-]+)"', text):
            check(f"anchor #{anchor} in {html.name}",
                  f'id="{anchor}"' in text, f'#{anchor}')


def check_html_hygiene():
    print("HTML hygiene:")
    for name in ("index.html", "checklists.html"):
        html = read(ROOT / "site" / name)
        check(f"{name} has doctype", html.lstrip().lower().startswith("<!doctype html"))
        check(f"{name} declares utf-8", 'charset="utf-8"' in html)
        for tag in ("html", "head", "body", "title", "main"):
            opens = len(re.findall(rf"<{tag}[\s>]", html, re.I))
            closes = len(re.findall(rf"</{tag}>", html, re.I))
            check(f"{name} <{tag}> tags balanced", opens == closes and opens >= 1,
                  f"{opens} open / {closes} close")
        check(f"{name} links stylesheet", 'href="styles.css"' in html)
        check(f"{name} references no external assets",
              not re.search(r'(?:src|href)="https?://', html),
              "external URL found — site must be fully local")
        check(f"{name} contains no CJK characters", not CJK.search(html))
    css = read(ROOT / "site" / "styles.css")
    check("styles.css has a print media block", "@media print" in css)
    check("styles.css contains no CJK characters", not CJK.search(css))


def check_printable_checklists():
    print("Printable checklists:")
    html = read(ROOT / "site" / "checklists.html")
    check("checklists page has checkbox items",
          'class="checks"' in html and html.count("<li>") >= 25,
          "expected class=\"checks\" list with 25+ checkbox items")
    for anchor in ("stage1", "stage2", "stage3", "stage4", "stage5"):
        check(f"checklist section #{anchor} present", f'id="{anchor}"' in html)


def main() -> int:
    try:
        check_required_files()
        check_license()
        check_no_user_content_in_readme()
        check_markdown_links()
        check_html_links()
        check_html_hygiene()
        check_printable_checklists()
    except TestFailure as e:
        print(e, file=sys.stderr)
        print("\nRESULT: FAIL", file=sys.stderr)
        return 1
    print("\nRESULT: all tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
