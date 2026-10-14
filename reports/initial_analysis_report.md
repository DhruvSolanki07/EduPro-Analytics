# EduPro Instructor Performance & Course Quality Analytics
## Initial analysis report

### 1. Executive summary
This project combines four supplied tables to explore instructor ratings, course ratings, learner transaction activity, course attributes, and basic user demographics. The integrated transaction-level dataset contains **10,000 rows and 22 columns**. The supplied files contain **3,000 users, 60 instructors, 60 courses, and 10,000 transactions**.

- Mean instructor rating: **3.12/5**.
- Mean course rating: **3.10/5**.
- The Pearson correlation between teaching experience and teacher rating is **0.598** in the 60-instructor table.
- The highest mean course-rating category is **Marketing** (3.72/5); the lowest is **Machine Learning** (2.66/5).
- All transaction foreign keys checked against the supplied dimension tables resolve: unknown users **0**, unknown courses **0**, unknown teachers **0**.

These are descriptive findings from the supplied dataset. Correlation does not prove causation, and transaction counts should not automatically be interpreted as unique learners or paid enrollments.

### 2. Business problem and objectives
EduPro needs a repeatable way to evaluate instructor performance, course quality, the association between experience and ratings, differences across expertise/category/level, and the distribution of recorded transaction activity. The dashboard supports exploration and helps identify questions for follow-up rather than asserting causal explanations.

### 3. Data and method
| Table | Rows | Key fields |
|---|---:|---|
| Users | 3,000 | UserID, Age, Gender (public version excludes name and email) |
| Teachers | 60 | TeacherID, Expertise, YearsOfExperience, TeacherRating |
| Courses | 60 | CourseID, CourseCategory, CourseType, CourseLevel, CoursePrice, CourseDuration, CourseRating |
| Transactions | 10,000 | TransactionID, UserID, CourseID, TeacherID, TransactionDate, Amount, PaymentMethod |

The tables were joined from Transactions to Users, Courses, and Teachers using their IDs. The joins are many-to-one from each transaction to the relevant dimension table. Dates were parsed with day-first interpretation, matching examples such as `25/10/2025`. Raw user names and email addresses are intentionally excluded from the project data folder.

### 4. Data quality
| Dataset | Rows | Missing cells | Duplicate rows | Duplicate primary keys |
|---|---:|---:|---:|---:|
| Users | 3000 | 0 | 0 | 0 |
| Courses | 60 | 0 | 0 | 0 |
| Teachers | 60 | 0 | 0 | 0 |
| Transactions | 10000 | 0 | 0 | 0 |

No missing cells, duplicate rows, or duplicate primary keys were found in the supplied tables during this initial check. Transaction reference checks found no orphan UserID, CourseID, or TeacherID values. The parsed transaction dates range from **2025-01-01** to **2025-12-30**.

### 5. Instructor experience and rating
The correlation between YearsOfExperience and TeacherRating is **0.598**, a positive association in this sample. This is worth exploring in the dashboard, but the dataset has only 60 instructors and cannot show that experience alone causes higher ratings. Other factors such as expertise, course assignment, rating counts, and audience may matter.

### 6. Course quality and attributes
- Category with the highest mean rating: **Marketing** (3.72/5).
- Category with the lowest mean rating: **Machine Learning** (2.66/5).
- Price–rating correlation across the 60 course records: **-0.032**.
- Duration–rating correlation across the 60 course records: **0.209**.

These correlations are descriptive and based on a small course catalogue. Category comparisons should include course counts and, if available later, the number of ratings behind each course score.

### 7. Recorded transaction activity by instructor rating tier
Rating tiers are defined for exploration as Low (rating ≤ 3), Mid (>3 and ≤4), and High (>4). In the supplied transaction data, the high tier accounts for **6,820** of **10,000** transaction rows. The average recorded transaction count per high-tier instructor is **620.0**, compared with **166.7** across all instructors.

**Important validation note:** this gap is unusually large and may reflect how the synthetic/sample transaction data was generated or assigned. Validate the meaning of TeacherID, whether every transaction is a genuine enrollment, and whether transactions are comparably recorded across instructors before using this as a business claim. The metric is not evidence that high ratings caused higher enrollment.

### 8. KPIs used
- **Average Teacher Rating:** mean TeacherRating across instructors.
- **Average Course Rating:** mean CourseRating across courses.
- **Rating Consistency Index (exploratory):** `max(0, min(1, 1 - SD(CourseRating) / mean(CourseRating)))`. This is a custom descriptive index, not a universal standard; document it when presenting.
- **Experience–Rating Correlation:** Pearson correlation between YearsOfExperience and TeacherRating. This is association, not causation.
- **Enrollment Influence Ratio (exploratory):** average transaction count among instructors rated above 4 divided by average transaction count across all instructors. It is a descriptive ratio, not a causal effect.

### 9. Recommendations
1. Review instructors with low ratings alongside rating counts and qualitative learner feedback before taking action.
2. Investigate categories with lower average course ratings and compare their course levels, durations, pricing, and course-specific sample sizes.
3. Use experience-rating correlation as a hypothesis to test, not as a hiring or promotion rule.
4. Validate transaction definitions and teacher-course mapping. Add explicit enrollment status, refund/cancellation status, and rating counts if available.
5. In future iterations, model course-level rating reliability and use statistical confidence intervals where rating counts are available.
6. Publish only privacy-safe user data. Never commit raw files containing personal email addresses or names to a public repository.

### 10. Limitations
- Ratings are supplied as aggregate values; rating counts and uncertainty intervals are not provided.
- The data may be synthetic or illustrative; operational validity has not been independently verified.
- A transaction row is treated as a transaction record, not necessarily a unique enrollment.
- Association does not imply causation.
- The user table was anonymized for this project by dropping names and emails, but UserID is retained to support joins.

### 11. Reproducibility
Run `python src/analysis.py` from the project root to rebuild the integrated dataset and data-quality report. Run `streamlit run dashboard/app.py` to open the interactive dashboard.
