# EduPro Instructor Performance & Course Quality Analytics

A portfolio-ready data analytics project using the supplied EduPro online-learning platform data. It combines instructor, course, user-demographic, and transaction records to explore teaching ratings, course quality, experience, expertise, and recorded transaction activity.

## Current dataset
- **3,000** users (public project version excludes names and email addresses)
- **60** instructors
- **60** courses
- **10,000** transaction rows
- Integrated dataset: **10,000** rows × **22** columns

## Main questions
- How are instructor and course ratings distributed?
- Is teaching experience associated with teacher ratings?
- Which course categories have higher/lower mean ratings?
- How do course price and duration relate to course ratings?
- How does recorded transaction volume differ across instructor-rating tiers?
- Are the joins complete and the source tables internally consistent?

## Tech stack
Python, Pandas, NumPy, Streamlit, Plotly, SciPy-ready workflow, Git, CSV.

## Project structure
```text
EduPro-Instructor-Analytics/
├── data/
│   ├── users_public.csv
│   ├── teachers.csv
│   ├── courses.csv
│   ├── transactions.csv
│   └── edupro_master.csv
├── src/
│   └── analysis.py
├── dashboard/
│   └── app.py
├── reports/
│   ├── initial_analysis_report.md
│   └── data_quality_summary.csv
├── requirements.txt
├── .gitignore
└── README.md
```

## Run locally (Windows / VS Code)
1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. Open a terminal in the project root and create a virtual environment:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```
4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
5. Rebuild analysis outputs:
   ```powershell
   python src/analysis.py
   ```
6. Start the dashboard:
   ```powershell
   streamlit run dashboard/app.py
   ```

## Initial findings from the supplied files
- Average teacher rating: **3.12/5**.
- Average course rating: **3.10/5**.
- Experience–teacher-rating correlation: **0.598**.
- Highest-rated course category by mean: **Marketing** (3.72/5).
- Lowest-rated course category by mean: **Machine Learning** (2.66/5).

See [`reports/initial_analysis_report.md`](reports/initial_analysis_report.md) for methods, detailed results, cautions, and recommendations.

## Data privacy
The original Users table contains names and email addresses. This project intentionally publishes only `UserID`, `Age`, and `Gender` in `data/users_public.csv`. Do not add or commit the raw Users.csv file to a public repository. Review whether the remaining user demographics and IDs are appropriate for your intended publication context.

## Interpretation notes
This is descriptive analysis. Correlation does not establish causation. The recorded `Amount` field includes zero-valued rows, so do not describe the sum as recognized revenue until the data definitions are confirmed. Likewise, transaction rows are not automatically unique enrollments.

## Next improvements
- Add automated tests and a formal data dictionary.
- Add confidence intervals when course/instructor rating counts become available.
- Add a SQL-based analysis layer.
- Add deployment instructions and screenshots after validating the dashboard locally.
- Extend the report with visualizations and a reviewed business interpretation.

## Author
Portfolio project — EduPro Instructor Performance & Course Quality Analytics.
