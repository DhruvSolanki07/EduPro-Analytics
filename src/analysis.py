from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

def load_data():
    users = pd.read_csv(DATA / "users_public.csv")
    courses = pd.read_csv(DATA / "courses.csv")
    teachers = pd.read_csv(DATA / "teachers.csv")
    transactions = pd.read_csv(DATA / "transactions.csv")
    transactions["TransactionDate"] = pd.to_datetime(
        transactions["TransactionDate"], dayfirst=True, errors="coerce"
    )
    return users, courses, teachers, transactions

def build_master(users, courses, teachers, transactions):
    users = users.rename(columns={"Age": "UserAge", "Gender": "UserGender"})
    master = (transactions
        .merge(users, on="UserID", how="left", validate="many_to_one")
        .merge(courses, on="CourseID", how="left", validate="many_to_one")
        .merge(teachers, on="TeacherID", how="left", validate="many_to_one"))
    return master

def data_quality(users, courses, teachers, transactions):
    checks = []
    for name, df, key in [
        ("Users", users, "UserID"), ("Courses", courses, "CourseID"),
        ("Teachers", teachers, "TeacherID"),
        ("Transactions", transactions, "TransactionID")
    ]:
        checks.append({
            "Dataset": name, "Rows": len(df), "Columns": len(df.columns),
            "MissingCells": int(df.isna().sum().sum()),
            "DuplicateRows": int(df.duplicated().sum()),
            "DuplicatePrimaryKeys": int(df[key].duplicated().sum())
        })
    return pd.DataFrame(checks)

def main():
    users, courses, teachers, transactions = load_data()
    master = build_master(users, courses, teachers, transactions)
    master.to_csv(DATA / "edupro_master.csv", index=False)
    quality = data_quality(users, courses, teachers, transactions)
    quality.to_csv(REPORTS / "data_quality_summary.csv", index=False)

    enrollments = transactions.groupby("TeacherID").size().rename("Enrollments")
    performance = teachers.merge(enrollments, on="TeacherID", how="left").fillna({"Enrollments": 0})
    performance["PerformanceTier"] = pd.cut(
        performance["TeacherRating"], [-np.inf, 3, 4, np.inf],
        labels=["Low (<3)", "Mid (3–4)", "High (>4)"]
    )
    performance.to_csv(DATA / "instructor_performance.csv", index=False)

    print("Data quality")
    print(quality.to_string(index=False))
    print(f"\nMaster dataset: {master.shape[0]:,} rows × {master.shape[1]} columns")
    print(f"Experience / teacher-rating Pearson correlation: "
          f"{teachers['YearsOfExperience'].corr(teachers['TeacherRating']):.3f}")
    print(f"Average teacher rating: {teachers['TeacherRating'].mean():.2f}")
    print(f"Average course rating: {courses['CourseRating'].mean():.2f}")
    print(f"Orphan transaction references — users: "
          f"{(~transactions['UserID'].isin(users['UserID'])).sum()}, courses: "
          f"{(~transactions['CourseID'].isin(courses['CourseID'])).sum()}, teachers: "
          f"{(~transactions['TeacherID'].isin(teachers['TeacherID'])).sum()}")

if __name__ == "__main__":
    main()
