"""Figures for the paper.

Fig 1 -- timeline: Indeed job postings (Software Development vs. all postings)
and the AI share of postings, Feb 2020 onward, with Nov 30, 2022 (ChatGPT's
release) marked. The postings index and the AI share are different units (an
index vs. a %) and move on very different scales (AI share grew ~9x over the
period, Feb 2020 to Sep 2026), so they're drawn as two panels sharing a time
axis rather than as a single plot with two y-scales -- a dual-axis chart
would let an arbitrary choice of axis scaling invent a correlation that
isn't really in the data.

Fig 2 -- before-and-after: % change in average postings index, Software
Development vs. all postings, at the 6/12/24-month windows computed by
02_analysis.py. Reads that script's saved before_after_indeed.csv rather than
recomputing, so the figure can't drift from the reported numbers.

Fig 3 -- Statistics Canada cross-check: quarterly job vacancies, sciences
vs. the rest of the market (all occupations minus sciences, matching
02_analysis.py), each indexed to 100 at its own 2019 average so the two
differently-sized series compare fairly. Starts at Q2 2015 (Q1 2015 is
graded E/F -- too unreliable, see DATA_LOG.md); Q2-Q3 2020 is left as a gap
rather than connected, since Statistics Canada didn't publish those
quarters. Not seasonally adjusted, so the within-year zig-zag is expected.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_INDEED_DIR = PROJECT_ROOT / "data" / "raw" / "indeed"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
ANALYSIS_DIR = PROJECT_ROOT / "data" / "analysis"
FIGURES_DIR = PROJECT_ROOT / "figures"

CUTOFF = pd.Timestamp("2022-11-30")
START = pd.Timestamp("2020-02-01")  # earliest date the postings series cover
END = pd.Timestamp("2026-09-30")  # latest date the AI share series covers
POSTING_VARIABLE = "total postings"  # matches 02_analysis.py

STATCAN_ALL_OCCUPATIONS_FILE = "1410044301-eng_vacancies-all-occupations_2015Q1-2026Q2.csv"
STATCAN_SCIENCES_FILE = "1410044301-eng_vacancies-natural-applied-sciences-NOC2_2015Q1-2026Q2.csv"
STATCAN_FIRST_QUARTER = "2015Q2"
STATCAN_LAST_QUARTER = "2026Q2"
STATCAN_BASE_QUARTERS = ["Q1 2019", "Q2 2019", "Q3 2019", "Q4 2019"]
STATCAN_BEFORE_QUARTERS = ["Q4 2021", "Q1 2022", "Q2 2022", "Q3 2022"]  # matches 02_analysis.py
STATCAN_AFTER_QUARTERS = ["Q1 2023", "Q2 2023", "Q3 2023", "Q4 2023"]  # matches 02_analysis.py
COLOR_SPAN = "#c3c2b7"

COLOR_SOFTWARE = "#2a78d6"  # categorical slot 1 (blue)
COLOR_NATIONAL = "#eb6834"  # categorical slot 2 (orange)
COLOR_AI_SHARE = "#1baf7a"  # categorical slot 3 (aqua)
COLOR_GRID = "#e1e0d9"
COLOR_AXIS = "#c3c2b7"
COLOR_INK_SECONDARY = "#52514e"
COLOR_INK_MUTED = "#898781"
COLOR_SURFACE = "#fcfcfb"


def fmt_pct(value: float) -> str:
    return f"{value:.1f}%".replace("-", "−")


def load_series(path: Path, filters: dict, value_col: str) -> pd.Series:
    df = pd.read_csv(path)
    for col, val in filters.items():
        df = df[df[col] == val]
    df["date"] = pd.to_datetime(df["date"])
    series = df.set_index("date")[value_col].sort_index()
    return series.loc[START:END]


def style_axis(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COLOR_AXIS)
    ax.spines["bottom"].set_color(COLOR_AXIS)
    ax.tick_params(colors=COLOR_INK_MUTED, labelsize=9)
    ax.yaxis.grid(True, color=COLOR_GRID, linewidth=1, zorder=0)
    ax.set_axisbelow(True)


def mark_cutoff(ax: plt.Axes, label: bool) -> None:
    ax.axvline(CUTOFF, color=COLOR_INK_MUTED, linestyle="--", linewidth=1, zorder=1)
    if label:
        ax.annotate(
            "Nov 30, 2022\nChatGPT released",
            xy=(CUTOFF, 1),
            xycoords=("data", "axes fraction"),
            xytext=(6, -4),
            textcoords="offset points",
            fontsize=8,
            color=COLOR_INK_MUTED,
            va="top",
        )


def endpoint_label(ax: plt.Axes, series: pd.Series, color: str, fmt: str) -> None:
    x, y = series.index[-1], series.iloc[-1]
    ax.plot([x], [y], marker="o", markersize=4, color=color, zorder=3, clip_on=False)
    ax.annotate(
        fmt.format(y),
        xy=(x, y),
        xytext=(6, 0),
        textcoords="offset points",
        fontsize=9,
        color=COLOR_INK_SECONDARY,
        va="center",
    )


def build_fig1_timeline() -> None:
    software = load_series(
        RAW_INDEED_DIR / "job_postings_by_sector_CA_2026-11-10.csv",
        {"display_name": "Software Development", "variable": POSTING_VARIABLE},
        "indeed_job_postings_index",
    )
    national = load_series(
        RAW_INDEED_DIR / "aggregate_job_postings_CA_2026-11-10.csv",
        {"variable": POSTING_VARIABLE},
        "indeed_job_postings_index_SA",
    )
    ai_share = load_series(
        RAW_INDEED_DIR / "AI_posting_2026-11-10.csv",
        {"jobcountry": "CA"},
        "AI_share_postings",
    )

    fig, (ax_postings, ax_ai) = plt.subplots(
        2, 1, figsize=(9, 6), sharex=True, height_ratios=[2, 1],
        facecolor=COLOR_SURFACE,
    )

    ax_postings.set_facecolor(COLOR_SURFACE)
    ax_postings.plot(software.index, software.values, color=COLOR_SOFTWARE, linewidth=2, label="Software Development")
    ax_postings.plot(national.index, national.values, color=COLOR_NATIONAL, linewidth=2, label="All postings (national)")
    ax_postings.axhline(100, color=COLOR_AXIS, linewidth=1, zorder=1)
    endpoint_label(ax_postings, software, COLOR_SOFTWARE, "{:.0f}")
    endpoint_label(ax_postings, national, COLOR_NATIONAL, "{:.0f}")
    mark_cutoff(ax_postings, label=True)
    style_axis(ax_postings)
    ax_postings.set_ylabel("Postings index\n(Feb 1, 2020 = 100)", fontsize=9, color=COLOR_INK_SECONDARY)
    ax_postings.set_title(
        "Canadian job postings and AI mentions, 2020-2026",
        fontsize=12, color="#0b0b0b", loc="left", pad=10,
    )
    legend = ax_postings.legend(loc="upper left", frameon=False, fontsize=9, labelcolor=COLOR_INK_SECONDARY)

    ax_ai.set_facecolor(COLOR_SURFACE)
    ax_ai.plot(ai_share.index, ai_share.values, color=COLOR_AI_SHARE, linewidth=2)
    endpoint_label(ax_ai, ai_share, COLOR_AI_SHARE, "{:.1f}%")
    mark_cutoff(ax_ai, label=False)
    style_axis(ax_ai)
    ax_ai.set_ylabel("AI share of\npostings (%)", fontsize=9, color=COLOR_INK_SECONDARY)
    ax_ai.set_ylim(bottom=0)
    ax_ai.set_xlim(pd.Timestamp("2020-01-01"), END)  # start before the first tick (2020) so it's labelled

    ax_ai.xaxis.set_major_locator(mdates.YearLocator())
    ax_ai.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.text(
        0.01, 0.02,
        "Source: Indeed Hiring Lab, Job Postings Index and AI Tracker (CC-BY-4.0), through Sep 30, 2026.\n"
        "Postings index is a 7-day trailing average, seasonally adjusted; AI share is a 7-day trailing average, Canada only.",
        fontsize=7, color=COLOR_INK_MUTED,
    )

    fig.subplots_adjust(left=0.11, right=0.90, top=0.93, bottom=0.12, hspace=0.12)
    out_path = FIGURES_DIR / "fig1_postings_and_ai_share.png"
    fig.savefig(out_path, dpi=300)
    print(f"wrote {out_path}")


def build_fig2_before_after() -> None:
    results = pd.read_csv(ANALYSIS_DIR / "before_after_indeed.csv").sort_values("window_months")
    groups = [f"{m}-month" for m in results["window_months"]]
    x = range(len(groups))
    bar_width = 0.32
    gap = 0.02  # surface gap between the two bars in a group

    fig, ax = plt.subplots(figsize=(7.5, 5), facecolor=COLOR_SURFACE)
    ax.set_facecolor(COLOR_SURFACE)

    bars_software = ax.bar(
        [i - bar_width / 2 - gap / 2 for i in x], results["pct_change"], width=bar_width,
        color=COLOR_SOFTWARE, label="Software Development", zorder=3,
    )
    bars_national = ax.bar(
        [i + bar_width / 2 + gap / 2 for i in x], results["baseline_pct_change"], width=bar_width,
        color=COLOR_NATIONAL, label="All postings (national)", zorder=3,
    )

    for bars in (bars_software, bars_national):
        for bar in bars:
            ax.annotate(
                fmt_pct(bar.get_height()),
                xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, -4),
                textcoords="offset points",
                ha="center", va="top",
                fontsize=9, color=COLOR_INK_SECONDARY,
            )

    ax.axhline(0, color=COLOR_AXIS, linewidth=1, zorder=2)
    style_axis(ax)
    ax.xaxis.grid(False)
    # Headroom above 0 for the gap labels (bar "sticky edges" pin the top at 0 otherwise)
    # and below the lowest bar so its value label doesn't sit on the axis line.
    ax.set_ylim(bottom=-60, top=6)

    for i, row in enumerate(results.itertuples()):
        ax.annotate(
            f"{abs(row.gap_pct_points):.1f} pts larger drop",
            xy=(i, 1),
            ha="center", va="bottom",
            fontsize=8, color=COLOR_INK_MUTED,
        )

    ax.set_xticks(list(x))
    ax.set_xticklabels([f"{m}-month window" for m in results["window_months"]], fontsize=9, color=COLOR_INK_SECONDARY)
    ax.set_ylabel("% change in average postings index\n(before vs. after Nov 30, 2022)", fontsize=9, color=COLOR_INK_SECONDARY)
    ax.set_title(
        "Software Development postings fell further than all postings",
        fontsize=12, color="#0b0b0b", loc="left", pad=14,
    )
    ax.legend(
        loc="upper center", bbox_to_anchor=(0.5, -0.12), frameon=False,
        fontsize=9, labelcolor=COLOR_INK_SECONDARY, ncols=2,
    )

    fig.text(
        0.01, 0.02,
        "Source: Indeed Hiring Lab, Job Postings Index (CC-BY-4.0), total postings, seasonally adjusted. Windows:\n"
        "6 months: Jun-Nov 2022 vs. Dec 2022-May 2023; 12 months: Dec 2021-Nov 2022 vs. Dec 2022-Nov 2023;\n"
        "24 months: Dec 2020-Nov 2022 vs. Dec 2022-Nov 2024.",
        fontsize=7, color=COLOR_INK_MUTED,
    )

    fig.subplots_adjust(left=0.14, right=0.97, top=0.90, bottom=0.22)
    out_path = FIGURES_DIR / "fig2_before_after_indeed.png"
    fig.savefig(out_path, dpi=300)
    print(f"wrote {out_path}")


def quarter_to_timestamp(period: str) -> pd.Timestamp:
    q, year = period.split()
    month = (int(q[1]) - 1) * 3 + 1
    return pd.Timestamp(year=int(year), month=month, day=1)


def quarter_mid_timestamp(period: str) -> pd.Timestamp:
    start = quarter_to_timestamp(period)
    return start + (start + pd.DateOffset(months=3) - start) / 2


def load_statcan_vacancies(filename: str) -> pd.Series:
    df = pd.read_csv(PROCESSED_DIR / filename, dtype={"period": str})
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    mask = (df["statistic"] == "Job vacancies") & (df["characteristic"] == "Type of work, all types")
    return df.loc[mask, ["period", "value"]].set_index("period")["value"]


def build_fig3_statcan_crosscheck() -> None:
    quarters = [f"Q{p.quarter} {p.year}" for p in pd.period_range(STATCAN_FIRST_QUARTER, STATCAN_LAST_QUARTER, freq="Q")]
    dates = [quarter_mid_timestamp(q) for q in quarters]

    sciences_raw = load_statcan_vacancies(STATCAN_SCIENCES_FILE)
    all_occ_raw = load_statcan_vacancies(STATCAN_ALL_OCCUPATIONS_FILE)
    rest_of_market_raw = all_occ_raw - sciences_raw  # nets out sciences, matching 02_analysis.py

    sciences_base = sciences_raw.reindex(STATCAN_BASE_QUARTERS).mean()
    rest_base = rest_of_market_raw.reindex(STATCAN_BASE_QUARTERS).mean()
    sciences = (sciences_raw.reindex(quarters) / sciences_base * 100).values
    rest_of_market = (rest_of_market_raw.reindex(quarters) / rest_base * 100).values

    fig, ax = plt.subplots(figsize=(9, 5), facecolor=COLOR_SURFACE)
    ax.set_facecolor(COLOR_SURFACE)

    before_start, before_end = quarter_to_timestamp(STATCAN_BEFORE_QUARTERS[0]), quarter_to_timestamp("Q4 2022")
    after_start, after_end = quarter_to_timestamp(STATCAN_AFTER_QUARTERS[0]), quarter_to_timestamp("Q1 2024")
    ax.axvspan(before_start, before_end, color=COLOR_SPAN, alpha=0.25, zorder=0, lw=0)
    ax.axvspan(after_start, after_end, color=COLOR_SPAN, alpha=0.25, zorder=0, lw=0)

    ax.annotate("before", xy=(before_start + (before_end - before_start) / 2, 1), xycoords=("data", "axes fraction"),
                xytext=(0, -14), textcoords="offset points", ha="center", fontsize=8, color=COLOR_INK_MUTED)
    ax.annotate("after", xy=(after_start + (after_end - after_start) / 2, 1), xycoords=("data", "axes fraction"),
                xytext=(0, -14), textcoords="offset points", ha="center", fontsize=8, color=COLOR_INK_MUTED)
    ax.annotate(
        "Q4 2022\nexcluded", xy=(before_end + (after_start - before_end) / 2, 0.03), xycoords=("data", "axes fraction"),
        ha="center", va="bottom", fontsize=7, color=COLOR_INK_MUTED, zorder=4,
        bbox=dict(facecolor=COLOR_SURFACE, edgecolor="none", pad=1),
    )

    ax.axvline(CUTOFF, color=COLOR_INK_MUTED, linestyle="--", linewidth=1, zorder=1)  # Nov 30, 2022, matches Figs 1-2

    ax.plot(dates, sciences, color=COLOR_SOFTWARE, linewidth=2, marker="o", markersize=3, label="Sciences")
    ax.plot(dates, rest_of_market, color=COLOR_NATIONAL, linewidth=2, marker="o", markersize=3, label="Rest of market (all occupations minus sciences)")
    ax.axhline(100, color=COLOR_AXIS, linewidth=1, zorder=1)

    style_axis(ax)
    # Set after plotting, and both bounds explicitly: an index doesn't need a zero
    # baseline, and setting only `top` before any data is plotted would lock the
    # bottom in at matplotlib's pre-autoscale default (0) instead of the data range.
    ax.set_ylim(40, 215)
    ax.set_xlim(quarter_to_timestamp("Q2 2015"), pd.Period(STATCAN_LAST_QUARTER, freq="Q").end_time)
    ax.set_ylabel("Job vacancies index\n(2019 average = 100)", fontsize=9, color=COLOR_INK_SECONDARY)
    ax.set_title(
        "Sciences vacancies fell further through 2023, then converged with the rest of the market",
        fontsize=11.5, color="#0b0b0b", loc="left", pad=16,
    )
    ax.legend(loc="upper left", frameon=False, fontsize=9, labelcolor=COLOR_INK_SECONDARY)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    fig.text(
        0.01, 0.02,
        "Source: Statistics Canada, table 14-10-0443-01, job vacancies, \"Type of work, all types\", not seasonally\n"
        "adjusted (expect within-year zig-zags). Gap: Q2-Q3 2020 not published. Shaded: before = Q4 2021-Q3 2022,\n"
        "after = Q1-Q4 2023 (Q4 2022 excluded as a transition quarter); Q1 2015 omitted (graded E/F, too unreliable).",
        fontsize=7, color=COLOR_INK_MUTED,
    )

    fig.subplots_adjust(left=0.11, right=0.97, top=0.85, bottom=0.21)
    out_path = FIGURES_DIR / "fig3_statcan_crosscheck.png"
    fig.savefig(out_path, dpi=300)
    print(f"wrote {out_path}")


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    build_fig1_timeline()
    build_fig2_before_after()
    build_fig3_statcan_crosscheck()


if __name__ == "__main__":
    main()
