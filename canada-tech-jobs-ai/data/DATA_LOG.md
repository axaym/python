# Data log: AI and Canadian tech jobs

One entry per downloaded file. Raw files in `raw/` are never edited; cleaned versions go in `processed/`.

| File | Source | Table / repo | Downloaded | What's in it | Notes |
| --- | --- | --- | --- | --- | --- |
| `raw/statcan/1410041601-eng_employment-by-occupation_2015-2025.csv` | Statistics Canada | [14-10-0416-01](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410041601), release 2026-01-09 | 2026-11-10 | **Employment** by occupation (NOC 2021), Canada, total gender, annual 2015–2025, persons in thousands | **Main file to use.** Filters: Reference period 2015–2025; Labour force characteristics = Employment |
| `raw/statcan/1410041601-eng_labour-force-by-occupation_2021-2025.csv` | Statistics Canada | [14-10-0416-01](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410041601), release 2026-01-09 | 2026-11-10 | Labour force by occupation (NOC 2021), Canada, total gender, annual 2021–2025, persons in thousands | Default view; superseded by the Employment file above, kept for the record |
| `raw/statcan/1410044301-eng_vacancies-natural-applied-sciences-NOC2_2015Q1-2026Q2.csv` | Statistics Canada | [14-10-0443-01](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410044301), release 2026-09-15 | 2026-11-10 | Job vacancies, share and average offered hourly wage, Canada, **"Natural and applied sciences and related occupations" (NOC broad category 2)**, all characteristics, Q1 2015–Q2 2026 | The tech-side comparison file. Broad category: includes computer and IT occupations but also engineers, scientists and technicians. Q1 2015 graded E/F in every block; otherwise grades A–D apart from one more cell ("No minimum education", Q4 2016) |
| `raw/statcan/1410044301-eng_vacancies-all-occupations_2015Q1-2026Q2.csv` | Statistics Canada | [14-10-0443-01](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410044301), release 2026-09-15 | 2026-11-10 | Job vacancies, share of vacancies and average offered hourly wage, Canada, **total of all occupations only**, all characteristics, Q1 2015–Q2 2026 (46 quarters) | Gives the all-occupations baseline over time. Q2 and Q3 2020 are "..". Q1 2015 is graded E (use with caution). Still needs an occupation breakdown for the tech comparison |
| `raw/statcan/1410044301-eng_vacancies-all-occupations_2025Q2-2026Q2.csv` | Statistics Canada | [14-10-0443-01](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410044301), release 2026-09-15 | 2026-11-10 | Job vacancies, share of vacancies and average offered hourly wage, Canada, **total of all occupations only**, by characteristics (full/part-time, education, experience, duration, recruitment), Q2 2025–Q2 2026 | Default view; superseded by the 2015–2026 file above, kept for the record |

### Indeed Hiring Lab, job postings tracker ([repo, CA folder](https://github.com/hiring-lab/job_postings_tracker/tree/master/CA)), CC-BY-4.0

All four downloaded 2026-11-10; daily data from 2020-02-01 to 2026-10-30. Index = 100 on Feb 1, 2020 (e.g. 102.58 means 2.58% above that level), 7-day trailing average.

| File | Columns | What's in it | Notes |
| --- | --- | --- | --- |
| `raw/indeed/aggregate_job_postings_CA_2026-11-10.csv` | date, jobcountry, indeed_job_postings_index_SA, indeed_job_postings_index_NSA, variable | All Canada postings | Seasonally adjusted (SA) and not adjusted (NSA) columns; `variable` = total postings or new postings (on Indeed 7 days or fewer). **The national baseline.** |
| `raw/indeed/job_postings_by_sector_CA_2026-11-10.csv` | date, jobcountry, indeed_job_postings_index, variable, display_name | 47 occupational sectors, total and new postings | Seasonally adjusted. Tech-related sectors: **Software Development**, Data & Analytics, IT Systems & Solutions, IT Infrastructure, Operations & Support; also Scientific Research & Development and engineering sectors as comparisons |
| `raw/indeed/provincial_postings_ca_2026-11-10.csv` | date, province, indeed_job_postings_index | All postings by province (two-letter lowercase codes, e.g. ab, on) | Seasonally adjusted; all sectors combined, so no software split by province |
| `raw/indeed/metro_job_postings_CA_2026-11-10.csv` | date, Metro, indeed_job_postings_index | All postings by metro area (e.g. "Abbotsford, BC") | Not described in the repo README; all sectors combined |

| `raw/indeed/sector-job-title-examples_2026-11-10.csv` | sector, job_titles | Two example job titles per sector (e.g. Software Development = "software engineer, full stack developer") | From the [job_postings_tracker repo root](https://github.com/hiring-lab/job_postings_tracker/blob/master/sector-job-title-examples.csv). Use it to describe sectors in the Data section |

### Indeed Hiring Lab, AI tracker ([repo](https://github.com/hiring-lab/ai-tracker)), CC-BY-4.0

| File | Columns | What's in it | Notes |
| --- | --- | --- | --- |
| `raw/indeed/AI_posting_2026-11-10.csv` | date, jobcountry, AI_share_postings | % of all postings that mention AI-related terms, 7-day average, 9 countries (AU, CA, DE, FR, GB, IE, IT, NL, US) | Downloaded 2026-11-10; daily, 2019-01-01 to 2026-09-30. **Country level only**: no split by sector or province |

**Canada AI share, selected dates** (for orientation, not analysis): 1.80% (2019-01-01), 2.22% (2022-11-30), 2.27% (2023-11-30), 3.41% (2024-11-30), 8.01% (2025-11-30), 18.97% (2026-09-30).

## Caveats on the Indeed data

- **An index, not counts:** each series shows change relative to its own Feb 1, 2020 level. You can compare the direction and size of change between sectors, but not how many jobs each sector has.
- **Sectors are Indeed's own groups,** based on job titles (see `sector-job-title-examples.csv` in the repo), not Statistics Canada's NOC. Matching "Software Development" to a NOC group is approximate.
- **Total vs new postings:** new postings react faster to employer demand; total postings include ads still open. Pick one and say why.
- **Baseline timing:** Feb 2020 is just before the pandemic, so post-2020 swings partly reflect the pandemic boom and its unwinding.
- **Method changes:** Indeed revised its seasonal adjustment in Nov 2024 and restated history. Re-downloading later may change past values, so cite the download date.
- **Sector names don't fully match:** the job-title list uses some older names. Seven sectors in the data have no example row (Agriculture & Forestry, Aviation, **Data & Analytics**, **IT Infrastructure, Operations & Support**, **IT Systems & Solutions**, Mechanical Engineering, Social Science). Seven example rows have no matching sector in the data (Driving, **IT Operations & Helpdesk**, **Information Design & Documentation**, Loading & Stocking, **Mathematics**, Sports, Veterinary). Software Development matches in both. Don't assume the renamed IT and data sectors map one-to-one; say so in the paper.
- **AI share rose very steeply recently, and part of that rise is a measurement artifact, not just demand (checked 2026-11-10, github.com/hiring-lab/ai-tracker/commits/main; cross-checked independently):** the series goes from about 3.4% (Nov 2024) to about 19% (Sep 2026) in the file we downloaded, but comparing the raw `AI_posting.csv` as published in successive monthly commits shows the reported share for a *fixed* past date keeps getting revised upward, release after release, and the revision is bigger the newer the date is:

    | Canada AI share for... | Jun 2025 (`4155b28c`) | Aug 2025 (`b5ca4d3d`) | Dec 2025 (`ce09d2ec`) | Oct 2026 (`bca9fe51`) | Total revision |
    | --- | --- | --- | --- | --- | --- |
    | 2022-11-30 | 2.19% | 2.19% | 2.21% | 2.22% | +1% |
    | 2023-11-30 | 2.20% | 2.20% | 2.23% | 2.27% | +3% |
    | 2024-11-30 | 3.09% | 3.09% | 3.25% | 3.41% | +10% |
    | 2025-11-30 | — | — | 5.86% | 8.01% | +37% |

  - `bca9fe51` (2026-10-08) is the version closest to our 2026-11-10 download, so our file matches that column.
  - The drift starts right after PR #4 ("remove-genai", merged 2025-08-15), which deleted `GenAI_posting.csv` from the repo. The README's methodology section still describes two separate keyword categories (AI and generative AI) feeding two files, and was never updated after the GenAI file was dropped — so it no longer matches what's in the repo.
  - **Conclusion:** this is consistent with generative-AI-related keywords being folded into the single remaining `AI_posting.csv` series starting around Aug-Sep 2025, with history restated under the broadened definition on every subsequent release (the actual keyword list isn't in the repo, so this can't be confirmed beyond the timing and the revision pattern). The 2022-2023 values barely moved (+1-3%), consistent with generative-AI keywords being rare before ChatGPT; 2024-2025 values were revised far more (+10%, +37%), since adding those keywords has much more to catch in later postings.
  - **For the paper:** the early flat period ("AI mentions held around 2% through 2023") is robust across versions and safe to lean on for the before/after timing argument. The 2025-2026 surge is real in direction but its *steepness* is partly an artifact of the later dates being revised up the most — say the shape of the 2025-26 rise depends on the series' definition, not only on demand. `02_analysis.py` never uses the AI share numerically (it only appears in Fig. 1), so this doesn't affect the before/after results, only how the chart should be described.
- **AI share is country-wide:** it can't tell you whether AI mentions are growing in software postings specifically. Any link to software demand is a comparison of trends over the same period, not a direct measure.
- **Citation:** Indeed Hiring Lab, Job Postings Index, github.com/hiring-lab/job_postings_tracker; Indeed Hiring Lab, AI Tracker, github.com/hiring-lab/ai-tracker (both CC-BY-4.0).

## Caveats on 14-10-0416-01

- **Measure:** the Employment file counts people who were working; the Labour force file adds unemployed people. Use Employment for "jobs".
- **Years:** the Employment file covers 2015–2025, so it includes a pre-pandemic baseline. The 2020 dip (pandemic) affects most occupations; treat 2020 carefully in any before/after comparison.
- **Annual only:** this table can't show monthly timing around Nov 2022. The Indeed daily data or monthly Labour Force Survey tables are needed for that.
- **Unclassified occupations:** shown as ".." (not available) for Employment, which is expected, since that row covers people without a recent job.
- **Occupation detail:** there is no separate "computer and information systems" row. The closest is "Professional occupations in applied sciences (except engineering)" (employment 490.7 thousand in 2015, 883.8 thousand in 2025), which may also include other occupations. Check what this group contains in the NOC 2021 structure before using it as "tech jobs".
- **Geography:** Canada only in this download; provinces are available in the same table.
- **Citation:** Statistics Canada. Table 14-10-0416-01 Labour force characteristics by occupation, annual.

## Caveats on 14-10-0443-01 (job vacancies)

- **Occupation files:** the all-occupations file is the baseline; the "Natural and applied sciences" file (NOC 2) is the tech-side series. NOC 2 is broad, so a tech result from it is "science and tech occupations", not "software jobs" specifically. A more detailed group (e.g. computer and information systems) would sharpen it, if the table offers one with usable quality grades.
- **Start the analysis at Q2 2015:** Q1 2015 is graded E or F in the sciences file and E in the all-occupations file.
- **Period:** the 2015–2026 file covers Q1 2015 to Q2 2026, the latest quarter released (2026-09-15); there is no Q3 2026 yet.
- **Suggested re-download** with Customize table:
  - National Occupational Classification: "Total, all occupations" plus "Natural and applied sciences and related occupations", and the most detailed computer-related group the table offers
  - Reference period: Q1 2015 to the latest quarter
  - Job vacancy characteristics: "Type of work, all types" (optionally also the "Minimum experience level sought" rows, to look at entry-level demand)
  - Statistics: Job vacancies and Average offered hourly wage
- **Not seasonally adjusted:** compare the same quarter across years (e.g. Q2 2022 vs Q2 2023), not consecutive quarters.
- **Missing quarters:** Q2 and Q3 2020 aren't available (pandemic).
- **Occupation codes changed:** data before Q4 2023 were converted from older NOC versions. Statistics Canada advises using broader groups where codes were split, so detailed tech codes before 2023 need care.
- **Quality flags:** letters after numbers (e.g. "545,910A") are data-quality grades (A = excellent to F = too unreliable). Strip them when cleaning, but keep them in a separate column, because detailed occupations may get lower grades.
- **Wages:** the offered wage is the lowest of any advertised range, not the wage actually paid.
- **Citation:** Statistics Canada. Table 14-10-0443-01 Job vacancies, proportion of job vacancies and average offered hourly wage by occupation and selected characteristics, quarterly, unadjusted for seasonality.

## Still to collect

- [x] Statistics Canada 14-10-0416-01 with Employment, 2015–2025, Canada (2026-11-10)
- [ ] Statistics Canada 14-10-0416-01 by province (optional)
- [ ] A more detailed occupation table that separates computer and information systems occupations (optional, if one exists)
- [x] Statistics Canada 14-10-0443-01, default view (2026-11-10)
- [x] Statistics Canada 14-10-0443-01, all occupations, Q1 2015–Q2 2026 (2026-11-10)
- [x] Statistics Canada 14-10-0443-01, Natural and applied sciences (NOC 2), Q1 2015–Q2 2026 (2026-11-10)
- [ ] Statistics Canada 14-10-0443-01, a more detailed computer/IT occupation group (optional, check quality grades)
- [ ] Statistics Canada 14-10-0399-01 (job vacancies by broad occupation, seasonally adjusted)
- [x] Indeed `CA/job_postings_by_sector_CA.csv` (2026-11-10)
- [x] Indeed `CA/aggregate_job_postings_CA.csv` (2026-11-10)
- [x] Indeed `CA/provincial_postings_ca.csv` (2026-11-10)
- [x] Indeed `CA/metro_job_postings_CA.csv` (2026-11-10, extra)
- [x] Indeed `sector-job-title-examples.csv` (2026-11-10)
- [x] Indeed `ai-tracker/AI_posting.csv` (2026-11-10)
