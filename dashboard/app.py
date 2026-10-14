from pathlib import Path
import sys
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
sys.path.insert(0, str(ROOT / "src"))

st.set_page_config(page_title="EduPro Analytics", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    users = pd.read_csv(DATA / "users_public.csv")
    courses = pd.read_csv(DATA / "courses.csv")
    teachers = pd.read_csv(DATA / "teachers.csv")
    tx = pd.read_csv(DATA / "transactions.csv")
    tx["TransactionDate"] = pd.to_datetime(tx["TransactionDate"], dayfirst=True, errors="coerce")
    master = (tx
        .merge(users.rename(columns={"Age": "UserAge", "Gender": "UserGender"}),
               on="UserID", how="left", validate="many_to_one")
        .merge(courses, on="CourseID", how="left", validate="many_to_one")
        .merge(teachers, on="TeacherID", how="left", validate="many_to_one"))
    counts = tx.groupby("TeacherID").size().rename("Enrollments").reset_index()
    performance = teachers.merge(counts, on="TeacherID", how="left")
    performance["Enrollments"] = performance["Enrollments"].fillna(0).astype(int)
    performance["PerformanceTier"] = pd.cut(
        performance["TeacherRating"], [-np.inf, 3, 4, np.inf],
        labels=["Low (<3)", "Mid (3–4)", "High (>4)"]
    ).astype(str)
    return users, courses, teachers, tx, master, performance

users, courses, teachers, tx, master, performance = load_data()

st.title("EduPro Instructor Performance & Course Quality Analytics")
st.caption("Interactive analysis of instructor ratings, course quality, enrollment patterns, and course attributes.")

with st.sidebar:
    st.header("Filters")
    expertise_options = sorted(teachers["Expertise"].dropna().unique().tolist())
    selected_expertise = st.multiselect("Instructor expertise", expertise_options, default=expertise_options)
    category_options = sorted(courses["CourseCategory"].dropna().unique().tolist())
    selected_categories = st.multiselect("Course category", category_options, default=category_options)
    level_options = sorted(courses["CourseLevel"].dropna().unique().tolist())
    selected_levels = st.multiselect("Course level", level_options, default=level_options)
    rating_range = st.slider("Teacher rating range", 0.0, 5.0, (0.0, 5.0), 0.1)
    exp_range = st.slider(
        "Years of experience", int(teachers["YearsOfExperience"].min()),
        int(teachers["YearsOfExperience"].max()),
        (int(teachers["YearsOfExperience"].min()), int(teachers["YearsOfExperience"].max()))
    )

filtered_teachers = teachers[
    teachers["Expertise"].isin(selected_expertise)
    & teachers["TeacherRating"].between(*rating_range)
    & teachers["YearsOfExperience"].between(*exp_range)
]
filtered_courses = courses[
    courses["CourseCategory"].isin(selected_categories)
    & courses["CourseLevel"].isin(selected_levels)
]
filtered_master = master[
    master["Expertise"].isin(selected_expertise)
    & master["TeacherRating"].between(*rating_range)
    & master["YearsOfExperience"].between(*exp_range)
    & master["CourseCategory"].isin(selected_categories)
    & master["CourseLevel"].isin(selected_levels)
]
filtered_perf = performance[performance["TeacherID"].isin(filtered_teachers["TeacherID"])]

tab_overview, tab_instructors, tab_courses, tab_experience, tab_transactions, tab_data = st.tabs([
    "Executive Overview", "Instructor Performance", "Course Quality",
    "Experience & Expertise", "Transactions", "Data Quality"
])

with tab_overview:
    total_revenue = float(tx["Amount"].sum())
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Transactions", f"{len(tx):,}")
    k2.metric("Unique learners", f"{tx['UserID'].nunique():,}")
    k3.metric("Instructors", f"{len(filtered_teachers):,}")
    k4.metric("Avg teacher rating", f"{filtered_teachers['TeacherRating'].mean():.2f}" if len(filtered_teachers) else "N/A")
    k5.metric("Avg course rating", f"{filtered_courses['CourseRating'].mean():.2f}" if len(filtered_courses) else "N/A")
    k6, k7, k8 = st.columns(3)
    k6.metric("Courses in filter", f"{len(filtered_courses):,}")
    k7.metric("Recorded transaction amount", f"{total_revenue:,.2f}")
    k8.metric("Paid-amount transactions", f"{(tx['Amount'] > 0).sum():,}")
    st.info("Transaction amount is the sum recorded in the supplied transaction file. Zero-amount records may represent free courses or other platform rules; verify the business meaning before calling the sum revenue.")
    c1, c2 = st.columns(2)
    with c1:
        if len(filtered_courses):
            fig = px.bar(
                filtered_courses.groupby("CourseCategory", as_index=False)["CourseRating"].mean()
                .sort_values("CourseRating", ascending=False),
                x="CourseCategory", y="CourseRating", title="Average course rating by category",
                labels={"CourseCategory": "Course category", "CourseRating": "Average rating"}
            )
            fig.update_layout(xaxis_tickangle=-35)
            st.plotly_chart(fig, width='stretch')
    with c2:
        if len(filtered_perf):
            fig = px.scatter(
                filtered_perf, x="YearsOfExperience", y="TeacherRating",
                size="Enrollments", color="Expertise", hover_name="TeacherName",
                title="Instructor experience, rating & enrollment volume"
            )
            st.plotly_chart(fig, width='stretch')
    st.subheader("Top instructors by recorded transaction count")
    st.dataframe(
        filtered_perf.sort_values(["Enrollments", "TeacherRating"], ascending=False)
        [["TeacherName", "Expertise", "YearsOfExperience", "TeacherRating", "Enrollments"]]
        .head(10), width='stretch', hide_index=True
    )

with tab_instructors:
    st.subheader("Instructor leaderboard")
    st.dataframe(
        filtered_perf.sort_values("TeacherRating", ascending=False)
        [["TeacherName", "Gender", "Expertise", "Age", "YearsOfExperience", "TeacherRating", "Enrollments"]],
        width='stretch', hide_index=True
    )
    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(filtered_teachers, x="TeacherRating", nbins=12,
                           title="Instructor rating distribution")
        st.plotly_chart(fig, width='stretch')
    with c2:
        if len(filtered_perf):
            tier = filtered_perf.groupby("PerformanceTier", as_index=False, observed=False)["Enrollments"].mean()
            fig = px.bar(tier, x="PerformanceTier", y="Enrollments",
                         title="Average transaction count by rating tier")
            st.plotly_chart(fig, width='stretch')

with tab_courses:
    st.subheader("Course quality")
    st.dataframe(
        filtered_courses.sort_values("CourseRating", ascending=False),
        width='stretch', hide_index=True
    )
    if len(filtered_courses):
        heat = filtered_courses.pivot_table(
            index="CourseCategory", columns="CourseLevel", values="CourseRating", aggfunc="mean"
        )
        fig = px.imshow(heat, text_auto=".2f", aspect="auto",
                        labels=dict(x="Course level", y="Course category", color="Average rating"),
                        title="Average course rating: category × level")
        st.plotly_chart(fig, width='stretch')
        c1, c2 = st.columns(2)
        with c1:
            fig = px.scatter(filtered_courses, x="CoursePrice", y="CourseRating",
                             color="CourseType", hover_name="CourseName",
                             title="Course price vs rating")
            st.plotly_chart(fig, width='stretch')
        with c2:
            fig = px.scatter(filtered_courses, x="CourseDuration", y="CourseRating",
                             color="CourseLevel", hover_name="CourseName",
                             title="Course duration vs rating")
            st.plotly_chart(fig, width='stretch')

with tab_experience:
    st.subheader("Experience and expertise")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.scatter(filtered_teachers, x="YearsOfExperience", y="TeacherRating",
                         color="Expertise", hover_name="TeacherName",
                         trendline="ols", title="Experience vs teacher rating")
        st.plotly_chart(fig, width='stretch')
        corr = filtered_teachers["YearsOfExperience"].corr(filtered_teachers["TeacherRating"])
        st.metric("Experience–teacher-rating correlation", f"{corr:.3f}" if pd.notna(corr) else "N/A")
    with c2:
        exp = filtered_perf.groupby("Expertise", as_index=False).agg(
            AvgRating=("TeacherRating", "mean"), InstructorCount=("TeacherID", "nunique"),
            Enrollments=("Enrollments", "sum")
        ).sort_values("AvgRating", ascending=False)
        fig = px.bar(exp, x="Expertise", y="AvgRating", color="InstructorCount",
                     title="Average teacher rating by expertise")
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(fig, width='stretch')
    st.caption("Correlation describes association in this dataset; it does not establish that experience causes higher ratings.")

with tab_transactions:
    st.subheader("Transaction trends")
    dated = filtered_master.dropna(subset=["TransactionDate"]).copy()
    if len(dated):
        daily = dated.set_index("TransactionDate").resample("MS").agg(
            Transactions=("TransactionID", "count"), RecordedAmount=("Amount", "sum")
        ).reset_index()
        c1, c2 = st.columns(2)
        with c1:
            fig = px.line(daily, x="TransactionDate", y="Transactions",
                          markers=True, title="Transactions by month")
            st.plotly_chart(fig, width='stretch')
        with c2:
            fig = px.line(daily, x="TransactionDate", y="RecordedAmount",
                          markers=True, title="Recorded transaction amount by month")
            st.plotly_chart(fig, width='stretch')
    st.subheader("Payment methods")
    method = tx["PaymentMethod"].value_counts().rename_axis("PaymentMethod").reset_index(name="Transactions")
    st.plotly_chart(px.bar(method, x="PaymentMethod", y="Transactions", title="Transactions by payment method"),
                    width='stretch')
    st.caption("Transaction counts are not necessarily unique enrollments unless each row represents one enrollment. Confirm the transaction grain before using that label in formal reporting.")

with tab_data:
    st.subheader("Dataset inventory")
    inventory = pd.DataFrame([
        {"Dataset": "Users (privacy-safe)", "Rows": len(users), "Columns": len(users.columns)},
        {"Dataset": "Courses", "Rows": len(courses), "Columns": len(courses.columns)},
        {"Dataset": "Teachers", "Rows": len(teachers), "Columns": len(teachers.columns)},
        {"Dataset": "Transactions", "Rows": len(tx), "Columns": len(tx.columns)},
        {"Dataset": "Integrated master", "Rows": len(master), "Columns": len(master.columns)}
    ])
    st.dataframe(inventory, width='stretch', hide_index=True)
    checks = []
    for name, df, key in [
        ("Users", users, "UserID"), ("Courses", courses, "CourseID"),
        ("Teachers", teachers, "TeacherID"), ("Transactions", tx, "TransactionID")
    ]:
        checks.append({"Dataset": name, "Missing cells": int(df.isna().sum().sum()),
                       "Duplicate rows": int(df.duplicated().sum()),
                       "Duplicate IDs": int(df[key].duplicated().sum())})
    st.dataframe(pd.DataFrame(checks), width='stretch', hide_index=True)
    st.write("Orphan transaction references")
    st.json({
        "Unknown UserID values": int((~tx["UserID"].isin(users["UserID"])).sum()),
        "Unknown CourseID values": int((~tx["CourseID"].isin(courses["CourseID"])).sum()),
        "Unknown TeacherID values": int((~tx["TeacherID"].isin(teachers["TeacherID"])).sum()),
        "Unparsed transaction dates": int(pd.to_datetime(tx["TransactionDate"], dayfirst=True, errors="coerce").isna().sum())
    })
    st.download_button("Download filtered master CSV", filtered_master.to_csv(index=False).encode("utf-8"),
                       file_name="edupro_filtered_master.csv", mime="text/csv")

st.divider()
st.caption("Portfolio project. Findings are descriptive and based on the supplied datasets; confirm data definitions before making operational or causal claims.")
