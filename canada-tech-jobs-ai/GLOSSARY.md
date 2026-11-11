# Glossary of terms

Terms used throughout `paper/draft.md` and this repo.

**Seasonally adjusted (SA) / not seasonally adjusted (NSA).** A seasonally adjusted series has predictable, recurring calendar patterns (postings reliably dip every December, pick up every spring) statistically removed, so month-to-month or quarter-to-quarter changes reflect the underlying trend rather than the normal seasonal rhythm. A non-seasonally-adjusted (NSA) series reports the raw numbers, including those predictable ups and downs. Indeed's postings index is SA; Statistics Canada's vacancies table is NSA, which is why that comparison matches the same quarter a year apart (e.g., Q2 2022 vs. Q2 2023) rather than consecutive quarters.

**7-day trailing average.** A separate, simpler smoothing step Indeed applies on top of seasonal adjustment: each day's value is the average of that day and the previous six, which removes day-of-week noise (e.g., fewer new postings appear on weekends). Not to be confused with seasonal adjustment — one removes weekly noise, the other removes yearly patterns.

**Index vs. count.** An index measures change relative to a fixed starting point (set to 100 at that point), not an absolute level. Indeed's postings index is set to 100 on Feb 1, 2020, so a value of 78 means postings are 22% below that date's level — it says nothing about how many job ads exist. A count (e.g., Statistics Canada's vacancy and employment figures) is an absolute number of people or jobs.

**Postings vs. vacancies vs. employment.** Three different things, often confused: *postings* (Indeed) are job ads placed online, which can overstate demand if employers post the same role in multiple places or leave ads up after filling them; *vacancies* (Statistics Canada) are positions employers report as open and actively being filled, surveyed directly; *employment* (Statistics Canada) is a count of people currently working, which lags both of the above since it only moves once a position is filled.

**NOC.** National Occupational Classification — Statistics Canada's official system for grouping jobs. Used in this paper only at broad levels: "Natural and applied sciences and related occupations" for vacancies, and "Professional occupations in applied sciences (except engineering)" for employment — both include software and IT roles alongside engineers, scientists, and technicians, broader than "tech jobs" alone.

**Cutoff / before-after window.** The cutoff is Nov 30, 2022 (ChatGPT's public release). A "before" or "after" window of *N* months is the *N* full calendar months immediately preceding or following that date (e.g., the 12-month "before" window is Dec 2021–Nov 2022).

**Data-quality grade.** Statistics Canada flags each published number with a letter from A (excellent) to F (too unreliable to publish); E means "use with caution." This paper treats E and F together as unusable, which is stricter than Statistics Canada's own guidance, out of caution. Q1 2015 in the vacancies tables is graded E/F, which is why that quarter is excluded from this analysis.
