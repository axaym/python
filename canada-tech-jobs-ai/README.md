# Did Canadian tech job demand change after generative AI went mainstream?

How did Canadian software job postings move relative to all postings after ChatGPT's public release (Nov 30, 2022), and does an independent government source show the same pattern?

## Key findings

- **Timing:** Software Development postings peaked on May 23, 2022 (index 229.3) and were already falling well before ChatGPT's Nov 30, 2022 release; the AI-mentions share of postings stayed flat around 2% until early 2024. The drop in software postings predates the rise in AI mentions — this is not an "AI caused the drop" story. See [`figures/fig1_postings_and_ai_share.png`](figures/fig1_postings_and_ai_share.png).
- **Indeed postings:** average postings in the 12 months after the cutoff were 53.7% lower than in the 12 months before, for Software Development, versus 17.2% lower for all Canadian postings (a 36.4-point larger drop). The gap has the same direction at the 6- and 24-month windows too. See [`figures/fig2_before_after_indeed.png`](figures/fig2_before_after_indeed.png) (all three windows, bar chart) and [`figures/fig1_postings_and_ai_share.png`](figures/fig1_postings_and_ai_share.png) (full timeline against the AI-mentions share).
- **Statistics Canada cross-check:** job vacancies in natural & applied sciences occupations (a broad proxy that includes but isn't limited to tech) were 30.4% lower from Q4 2021-Q3 2022 to Q1-Q4 2023, versus 21.4% lower for the rest of the labour market excluding sciences — an independent source, built from a different method (employer vacancy counts, not ad postings), pointing the same direction as the Indeed data. See [`figures/fig3_statcan_crosscheck.png`](figures/fig3_statcan_crosscheck.png).
- **The two sources disagree after 2023:** in StatCan, sciences vacancies converge back toward the rest of the market from 2024 onward, so that gap isn't permanent. In Indeed, it is — Software Development is still well below all postings as of Sep 2026 (78 vs. 101 on the Feb 2020 = 100 index), with no sign of closing. Compare [`figures/fig3_statcan_crosscheck.png`](figures/fig3_statcan_crosscheck.png) (converges) against [`figures/fig1_postings_and_ai_share.png`](figures/fig1_postings_and_ai_share.png) (doesn't).

## Data sources

| Source | Licence | Downloaded |
| --- | --- | --- |
| [Indeed Hiring Lab, Job Postings Index](https://github.com/hiring-lab/job_postings_tracker) | CC-BY-4.0 | 2026-11-10 |
| [Indeed Hiring Lab, AI Tracker](https://github.com/hiring-lab/ai-tracker) | CC-BY-4.0 | 2026-11-10 |
| [Statistics Canada, Table 14-10-0416-01](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410041601) (employment by occupation) | Statistics Canada Open Licence | 2026-11-10 |
| [Statistics Canada, Table 14-10-0443-01](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410044301) (job vacancies by occupation) | Statistics Canada Open Licence | 2026-11-10 |

See `data/DATA_LOG.md` for exactly what each file contains, known data-quality flags, and caveats — including a documented revision in the Indeed AI Tracker's methodology that affects how the 2025-26 AI-share numbers should be read.

## How to run it

Requires Python 3.10+ (the code uses `int | None` and `list[...]` type hints).

```bash
pip install -r requirements.txt
```

Then, from the project root, in order:

1. `python src/01_clean.py` — cleans the raw Statistics Canada exports in `data/raw/statcan/` into tidy long tables, written to `data/processed/`.
2. `python src/02_analysis.py` — computes the before/after comparisons (Indeed and StatCan), printed to the console and written to `data/analysis/`.
3. `python src/03_figures.py` — builds the three figures from the cleaned/analyzed data, written to `figures/`.

## Folder layout

```
canada-tech-jobs-ai/
├── data/
│   ├── raw/          # downloaded source files, never edited
│   ├── processed/    # cleaned StatCan tables (output of 01_clean.py)
│   ├── analysis/     # before/after comparison tables (output of 02_analysis.py)
│   └── DATA_LOG.md   # one entry per downloaded file: source, contents, caveats
├── src/
│   ├── 01_clean.py
│   ├── 02_analysis.py
│   └── 03_figures.py
├── figures/           # output of 03_figures.py
├── README.md
└── requirements.txt
```

## Limitations

- The decline in software postings started before ChatGPT's release, during the unwinding of the 2020-2022 pandemic hiring boom — the 12-month "before" window itself sits near that boom's peak, so part of the post-cutoff drop isn't specific to AI.
- The Indeed AI Tracker's series has been revised upward on every release since mid-2025, more so for recent dates; the early flat period (AI mentions ~2% through 2023) is stable across revisions, but the steepness of the 2025-26 rise is partly a measurement artifact, not only demand (see `data/DATA_LOG.md`).
- Both comparisons show correlation, not causation — rate hikes, tech layoffs, and immigration/population shifts happened over the same period and aren't separated out here.

## AI-use note

I used Claude to help plan the study, suggest data sources and methods, write and review code, and review data and figures. The analysis, results and writing are my own.
