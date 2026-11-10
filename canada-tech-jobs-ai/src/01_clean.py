"""Clean raw StatCan CSV exports into tidy, one-row-per-value tables.

For each CSV in data/raw/statcan/: trim the title/metadata preamble and the
legend/footnotes footer, strip footnote-reference numbers (e.g. "Job
vacancies 8") and NOC-selection tags (e.g. "[2]") off of row/column labels,
split any trailing data-quality letter (e.g. "408,405E") off of numeric
values into its own "flag" column, and melt the result into a long table
with columns: occupation, characteristic, statistic, unit, period, value, flag.

Output goes to data/processed/, one file per input, same name.
"""
import csv
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_ROOT / "data" / "raw" / "statcan"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

HEADER_LINES = 8  # fixed StatCan title/frequency/table/release/geography preamble
FOOTER_MARKERS = {"Symbol legend:", "Table Corrections:", "Footnotes:"}

QUALITY_RE = re.compile(r"^(-?[\d,]*\.?\d+)([A-F])$")
LETTER_ONLY_RE = re.compile(r"^[A-F]$")
NUMERIC_RE = re.compile(r"^-?[\d,]*\.?\d+$")
PERIOD_RE = re.compile(r"^(?:Q[1-4]\s?\d{4}|\d{4})$")
BRACKET_RE = re.compile(r"(\s*\[\d+\])+$")
FOOTNOTE_NUMS_RE = re.compile(r"(\s+\d{1,2})+$")

LONG_COLUMNS = ["occupation", "characteristic", "statistic", "unit", "period", "value", "flag"]


def read_rows(path: Path) -> list[list[str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.reader(f))


def extract_table(rows: list[list[str]]) -> list[list[str]]:
    footer_idx = next(
        i for i, row in enumerate(rows) if row and row[0].strip() in FOOTER_MARKERS
    )
    table = rows[HEADER_LINES:footer_idx]
    while table and all(cell.strip() == "" for cell in table[-1]):
        table.pop()
    return table


def strip_footnotes(cell: str) -> str:
    if not re.search(r"[A-Za-z]", cell):
        return cell
    s = BRACKET_RE.sub("", cell)
    s = FOOTNOTE_NUMS_RE.sub("", s)
    return s.rstrip()


def find_header_row(table: list[list[str]]) -> int | None:
    for i, row in enumerate(table):
        if sum(1 for cell in row if PERIOD_RE.match(cell.strip())) >= 3:
            return i
    return None


def parse_value(raw: str) -> tuple[str, str]:
    s = raw.strip()
    if s == "..":
        return "", ""
    match = QUALITY_RE.match(s)
    if match:
        return match.group(1).replace(",", ""), match.group(2)
    if LETTER_ONLY_RE.match(s):
        return "", s
    if NUMERIC_RE.match(s):
        return s.replace(",", ""), ""
    return s, ""


def melt_simple_table(table: list[list[str]], header_idx: int) -> list[list[str]]:
    """Annual employment/labour-force tables: one occupation per row, periods
    start right after the row-label column, with a single unit/statistic for
    the whole file."""
    statistic = table[1][1].strip()
    periods = [c.strip() for c in table[header_idx][1:]]
    unit = table[header_idx + 1][1].strip()

    out_rows = []
    for row in table[header_idx + 2:]:
        occupation = row[0].strip()
        if not occupation:
            continue
        for period, raw in zip(periods, row[1:]):
            value, flag = parse_value(raw)
            out_rows.append([occupation, "", statistic, unit, period, value, flag])
    return out_rows


def melt_characteristic_table(table: list[list[str]], header_idx: int) -> list[list[str]]:
    """Quarterly vacancies tables: a single occupation per file, with nested
    characteristic -> statistic blocks and a unit row ahead of each statistic
    row, periods starting two columns in."""
    occupation = table[1][2].strip()
    periods = [c.strip() for c in table[header_idx][2:]]

    out_rows = []
    current_characteristic = ""
    current_unit = ""
    for row in table[header_idx + 1:]:
        label0 = row[0].strip()
        statistic = row[1].strip()
        if not statistic:
            if label0:
                current_characteristic = label0
            current_unit = row[2].strip() if len(row) > 2 else ""
            continue
        for period, raw in zip(periods, row[2:]):
            value, flag = parse_value(raw)
            out_rows.append(
                [occupation, current_characteristic, statistic, current_unit, period, value, flag]
            )
    return out_rows


def clean_file(path: Path) -> None:
    rows = read_rows(path)
    table = extract_table(rows)
    table = [[strip_footnotes(cell) for cell in row] for row in table]

    header_idx = find_header_row(table)
    if header_idx is None:
        raise ValueError(f"no period header row found in {path.name}")

    if PERIOD_RE.match(table[header_idx][1].strip()):
        long_rows = melt_simple_table(table, header_idx)
    else:
        long_rows = melt_characteristic_table(table, header_idx)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / path.name
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(LONG_COLUMNS)
        writer.writerows(long_rows)

    print(f"{path.name}: {len(long_rows)} rows -> {out_path}")


def main() -> None:
    if not INPUT_DIR.exists():
        print(f"warning: input directory not found: {INPUT_DIR}")
        return
    files = sorted(INPUT_DIR.glob("*.csv"))
    if not files:
        print(f"warning: no CSV files found in {INPUT_DIR}")
        return
    for path in files:
        clean_file(path)


if __name__ == "__main__":
    main()
