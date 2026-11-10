"""Before-and-after comparison of tech-sector labour demand around the
Nov 30, 2022 ChatGPT release, cross-checked across two independent sources:

  - Indeed Hiring Lab sector postings (daily, seasonally adjusted index):
    Software Development vs. all postings nationally.
  - Statistics Canada job vacancies (quarterly, table 14-10-0443-01):
    Natural and applied sciences occupations vs. all occupations.

Each comparison reports the average level before and after the cutoff, the
% change, and the gap between the tech series and its baseline. Results are
printed and written to data/analysis/.
"""
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_INDEED_DIR = PROJECT_ROOT / "data" / "raw" / "indeed"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "data" / "analysis"

CUTOFF = pd.Timestamp("2022-11-30")  # ChatGPT's public release
POSTING_VARIABLE = "total postings"  # fixed throughout; "new postings" is the alternative
INDEED_WINDOWS_MONTHS = [6, 12, 24]  # 12 is the headline window; 6/24 are the robustness check
SUPPORTING_SECTORS = ["Data & Analytics", "IT Systems & Solutions", "IT Infrastructure, Operations & Support"]

STATCAN_BEFORE_QUARTERS = ["Q4 2021", "Q1 2022", "Q2 2022", "Q3 2022"]
STATCAN_AFTER_QUARTERS = ["Q1 2023", "Q2 2023", "Q3 2023", "Q4 2023"]
# Q4 2022 (the cutoff's own quarter) is deliberately excluded as a transition quarter.

STATCAN_ALL_OCCUPATIONS_FILE = "1410044301-eng_vacancies-all-occupations_2015Q1-2026Q2.csv"
STATCAN_SCIENCES_FILE = "1410044301-eng_vacancies-natural-applied-sciences-NOC2_2015Q1-2026Q2.csv"
STATCAN_EMPLOYMENT_FILE = "1410041601-eng_employment-by-occupation_2015-2025.csv"


def indeed_window(cutoff: pd.Timestamp, months: int) -> tuple[pd.Timestamp, pd.Timestamp, pd.Timestamp, pd.Timestamp]:
    # Snap to month-end before offsetting: DateOffset(months=...) preserves the day
    # NUMBER (30), not "end of month", so e.g. Nov 30 - 6 months gives May 30 even
    # though May has 31 days. Rolling forward to the true month-end keeps the
    # before/after windows the same number of whole calendar months for any cutoff
    # that is itself a month-end -- not necessarily the same day count (months have
    # different lengths, and leap years add a day to some 24-month windows).
    before_pivot = (cutoff - pd.DateOffset(months=months)) + pd.offsets.MonthEnd(0)
    after_pivot = (cutoff + pd.DateOffset(months=months)) + pd.offsets.MonthEnd(0)
    before_start = before_pivot + pd.Timedelta(days=1)
    before_end = cutoff
    after_start = cutoff + pd.Timedelta(days=1)
    after_end = after_pivot
    return before_start, before_end, after_start, after_end


def window_avg(series: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> float:
    mask = (series["date"] >= start) & (series["date"] <= end)
    window = series.loc[mask, "value"]
    expected_days = (end - start).days + 1
    if window.notna().sum() != expected_days:
        raise ValueError(
            f"expected {expected_days} daily observations in [{start.date()}, {end.date()}], "
            f"found {window.notna().sum()}"
        )
    return window.mean()


def pct_change(before: float, after: float) -> float:
    return (after - before) / before * 100


def change_phrase(pct: float) -> str:
    verb = "grew" if pct > 0 else "fell" if pct < 0 else "was unchanged"
    return f"{verb} {abs(pct):.1f}%"


def relative_to_phrase(value: float, baseline: float, label: str) -> str:
    position = "above" if value > baseline else "below" if value < baseline else "at"
    return f"{position} its {label}"


def load_indeed_sector(sector: str) -> pd.DataFrame:
    df = pd.read_csv(RAW_INDEED_DIR / "job_postings_by_sector_CA_2026-11-10.csv")
    df = df[(df["display_name"] == sector) & (df["variable"] == POSTING_VARIABLE)]
    df = df.rename(columns={"indeed_job_postings_index": "value"})
    df["date"] = pd.to_datetime(df["date"])
    return df[["date", "value"]]


def load_indeed_national() -> pd.DataFrame:
    df = pd.read_csv(RAW_INDEED_DIR / "aggregate_job_postings_CA_2026-11-10.csv")
    df = df[df["variable"] == POSTING_VARIABLE]
    df = df.rename(columns={"indeed_job_postings_index_SA": "value"})
    df["date"] = pd.to_datetime(df["date"])
    return df[["date", "value"]]


def indeed_comparison(tech: pd.DataFrame, baseline: pd.DataFrame, months: int) -> dict:
    before_start, before_end, after_start, after_end = indeed_window(CUTOFF, months)
    tech_before, tech_after = window_avg(tech, before_start, before_end), window_avg(tech, after_start, after_end)
    base_before, base_after = window_avg(baseline, before_start, before_end), window_avg(baseline, after_start, after_end)
    tech_pct, base_pct = pct_change(tech_before, tech_after), pct_change(base_before, base_after)
    return {
        "window_months": months,
        "before_avg": tech_before,
        "after_avg": tech_after,
        "pct_change": tech_pct,
        "baseline_before_avg": base_before,
        "baseline_after_avg": base_after,
        "baseline_pct_change": base_pct,
        "gap_pct_points": tech_pct - base_pct,
    }


def load_statcan_long(filename: str) -> pd.DataFrame:
    df = pd.read_csv(PROCESSED_DIR / filename, dtype={"period": str})
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df


def statcan_vacancies(df: pd.DataFrame) -> pd.DataFrame:
    mask = (df["statistic"] == "Job vacancies") & (df["characteristic"] == "Type of work, all types")
    return df.loc[mask, ["period", "value"]].set_index("period")["value"]


def statcan_vacancy_avg(vacancies: pd.Series, quarters: list[str]) -> float:
    window = vacancies.reindex(quarters)
    if window.isna().any():
        missing = window[window.isna()].index.tolist()
        raise ValueError(f"missing or non-numeric vacancy count for quarter(s): {missing}")
    return window.mean()


def statcan_comparison() -> dict:
    tech = statcan_vacancies(load_statcan_long(STATCAN_SCIENCES_FILE))
    all_occ = statcan_vacancies(load_statcan_long(STATCAN_ALL_OCCUPATIONS_FILE))
    rest_of_market = all_occ - tech  # all occupations includes the sciences group; net it out

    tech_before, tech_after = statcan_vacancy_avg(tech, STATCAN_BEFORE_QUARTERS), statcan_vacancy_avg(tech, STATCAN_AFTER_QUARTERS)
    base_before, base_after = statcan_vacancy_avg(all_occ, STATCAN_BEFORE_QUARTERS), statcan_vacancy_avg(all_occ, STATCAN_AFTER_QUARTERS)
    rest_before, rest_after = statcan_vacancy_avg(rest_of_market, STATCAN_BEFORE_QUARTERS), statcan_vacancy_avg(rest_of_market, STATCAN_AFTER_QUARTERS)

    tech_pct = pct_change(tech_before, tech_after)
    base_pct = pct_change(base_before, base_after)
    rest_pct = pct_change(rest_before, rest_after)

    return {
        "before_avg": tech_before,
        "after_avg": tech_after,
        "pct_change": tech_pct,
        "baseline_before_avg": base_before,
        "baseline_after_avg": base_after,
        "baseline_pct_change": base_pct,
        "gap_pct_points": tech_pct - base_pct,
        "rest_of_market_before_avg": rest_before,
        "rest_of_market_after_avg": rest_after,
        "rest_of_market_pct_change": rest_pct,
        "gap_vs_rest_of_market_pct_points": tech_pct - rest_pct,
    }


def employment_sentence() -> str:
    df = load_statcan_long(STATCAN_EMPLOYMENT_FILE)
    tech_occ = "Professional occupations in applied sciences (except engineering)"

    def value_for(occupation: str, year: str) -> float:
        mask = (df["occupation"] == occupation) & (df["period"] == year)
        return df.loc[mask, "value"].iloc[0]

    tech_2022, tech_2023 = value_for(tech_occ, "2022"), value_for(tech_occ, "2023")
    base_2022, base_2023 = value_for("Total, all occupations", "2022"), value_for("Total, all occupations", "2023")
    tech_pct, base_pct = pct_change(tech_2022, tech_2023), pct_change(base_2022, base_2023)

    return (
        f"Descriptive only: annual employment in '{tech_occ}' "
        f"{change_phrase(tech_pct)} from 2022 to 2023, while all occupations {change_phrase(base_pct)} "
        f"(this NOC group is a broad proxy for tech jobs, not a direct measure; see DATA_LOG.md)."
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    software = load_indeed_sector("Software Development")
    national = load_indeed_national()

    indeed_results = pd.DataFrame([indeed_comparison(software, national, m) for m in INDEED_WINDOWS_MONTHS])
    indeed_results.to_csv(OUTPUT_DIR / "before_after_indeed.csv", index=False)

    print("Indeed: Software Development vs. all postings (national, SA), % change in average index level")
    print(indeed_results.round(1).to_string(index=False))
    print()

    headline = indeed_results[indeed_results["window_months"] == 12].iloc[0]
    headline_sign = headline["gap_pct_points"] > 0
    holds = ((indeed_results["gap_pct_points"] > 0) == headline_sign).all()
    print(
        f"Headline (12-month window): Software Development {headline['pct_change']:.1f}% vs. "
        f"national {headline['baseline_pct_change']:.1f}% (gap {headline['gap_pct_points']:.1f} points).\n"
        f"Gap direction holds across 6/12/24-month windows: {holds}.\n"
        "Limitation: the 12-month 'before' window (Dec 2021-Nov 2022) sits near the peak of the pandemic "
        "tech-hiring boom, so part of any post-cutoff drop reflects that boom unwinding, not AI specifically.\n"
        f"Pre-pandemic framing (index = 100 on Feb 1, 2020, so this doesn't depend on the boom peak): "
        f"after the cutoff, Software Development averaged {headline['after_avg']:.1f} "
        f"({relative_to_phrase(headline['after_avg'], 100, 'pre-pandemic level')}), while all postings "
        f"stayed at {headline['baseline_after_avg']:.1f} "
        f"({relative_to_phrase(headline['baseline_after_avg'], 100, 'pre-pandemic level')}).\n"
        "Caveat: the national 'all postings' baseline includes Software Development itself; unlike the "
        "Statistics Canada counts below, an index can't be netted out, so the Indeed gap likely understates "
        "how much more software fell than the rest of the market."
    )
    print()

    supporting = pd.DataFrame(
        [indeed_comparison(load_indeed_sector(s), national, 12) for s in SUPPORTING_SECTORS],
        index=SUPPORTING_SECTORS,
    )
    supporting.to_csv(OUTPUT_DIR / "before_after_indeed_supporting_sectors.csv")
    print("Supporting sectors (12-month window):")
    print(supporting.round(1).to_string())
    print()

    statcan_results = pd.DataFrame([statcan_comparison()])
    statcan_results.to_csv(OUTPUT_DIR / "before_after_statcan.csv", index=False)
    print("Statistics Canada: job vacancies, natural & applied sciences vs. all occupations")
    print("(4 quarters before Q4 2021-Q3 2022 vs. 4 quarters after Q1-Q4 2023; Q4 2022 excluded)")
    print(statcan_results.round(1).to_string(index=False))
    row = statcan_results.iloc[0]
    sciences_share = row["before_avg"] / row["baseline_before_avg"] * 100
    print(
        f"'All occupations' includes the sciences group itself (about {sciences_share:.1f}% of vacancies "
        f"before the cutoff); netting it out gives a rest-of-market gap of "
        f"{row['gap_vs_rest_of_market_pct_points']:.1f} points "
        f"(vs. {row['gap_pct_points']:.1f} against the unadjusted all-occupations baseline)."
    )
    print()

    print(employment_sentence())


if __name__ == "__main__":
    main()
