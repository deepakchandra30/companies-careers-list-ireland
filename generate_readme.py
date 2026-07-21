#!/usr/bin/env python3
import csv
from pathlib import Path
from datetime import date

CSV_FILE = Path("companies.csv")
README_FILE = Path("README.md")

START_MARKER = "<!-- COMPANIES:START -->"
END_MARKER = "<!-- COMPANIES:END -->"

HEADER = """# Companies Careers Pages Ireland (IT)

A curated, searchable list of **company careers page links in Ireland** for people looking for **IT, tech, software, and engineering jobs**.

## Why this repo exists

Finding Ireland careers pages is often surprisingly hard because company job links are buried across websites, job boards, and regional pages. This repo brings those links together in one place so you can quickly search by company name or careers URL.

## What you'll find

- 380+ companies with direct careers pages
- Ireland-focused and Ireland-relevant employers
- Searchable HTML index for quick browsing
- A CSV file you can reuse or import into spreadsheets

## Search terms this page is designed for

- companies career pages links ireland
- ireland company careers page
- ireland tech jobs companies
- careers page links ireland
- it jobs ireland companies
- software companies hiring in ireland

## How to use

- Open the HTML page and search by company name or URL
- Use the CSV file if you want to filter, sort, or reuse the data elsewhere
- Check back often because the list is periodically updated

## Data format

- `companies.csv` is the source file
- Columns: `company_name`, `careers_page_link`

## Notes

- Links are periodically validated
- If you find a broken link, please open an issue
- If a company is missing, feel free to suggest it via Issues

## Stats

- Total companies listed: **380**

## Companies and Career Links (Ireland IT)

<!-- COMPANIES:START -->
<!-- COMPANIES:END -->
"""

def read_companies(csv_path: Path):
    rows = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        required = {"company_name", "careers_page_link"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing columns in CSV: {missing}")
        for r in reader:
            name = (r.get("company_name") or "").strip()
            link = (r.get("careers_page_link") or "").strip()
            if not name or not link:
                continue
            rows.append((name, link))

    # dedupe by (name, link), then sort by name case-insensitive
    rows = sorted(set(rows), key=lambda x: x[0].casefold())
    return rows

def build_company_section(rows):
    lines = []
    for name, link in rows:
        lines.append(f"- **{name}**: [Career Page]({link})")
    lines.append("")
    lines.append(f"_Last generated: {date.today().isoformat()}_")
    return "\n".join(lines)

def replace_between_markers(text, start_marker, end_marker, new_block):
    start = text.find(start_marker)
    end = text.find(end_marker)
    if start == -1 or end == -1 or end < start:
        return None
    start_content = start + len(start_marker)
    return text[:start_content] + "\n" + new_block + "\n" + text[end:]

def main():
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"{CSV_FILE} not found")

    rows = read_companies(CSV_FILE)
    generated_block = build_company_section(rows)

    if README_FILE.exists():
        readme_text = README_FILE.read_text(encoding="utf-8")
    else:
        readme_text = HEADER

    updated = replace_between_markers(readme_text, START_MARKER, END_MARKER, generated_block)

    if updated is None:
        # If markers missing, create a fresh README with markers + content
        updated = HEADER.replace(
            f"{START_MARKER}\n{END_MARKER}",
            f"{START_MARKER}\n{generated_block}\n{END_MARKER}",
        )

    README_FILE.write_text(updated, encoding="utf-8")
    print(f"✅ README updated with {len(rows)} companies.")

if __name__ == "__main__":
    main()