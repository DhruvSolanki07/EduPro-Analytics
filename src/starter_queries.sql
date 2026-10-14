-- EduPro SQL starter queries (SQLite-compatible after importing CSVs as tables)

-- 1. Instructor performance and transaction count
SELECT
    t.TeacherID,
    t.TeacherName,
    t.Expertise,
    t.YearsOfExperience,
    t.TeacherRating,
    COUNT(tr.TransactionID) AS transaction_count
FROM teachers AS t
LEFT JOIN transactions AS tr ON tr.TeacherID = t.TeacherID
GROUP BY t.TeacherID, t.TeacherName, t.Expertise,
         t.YearsOfExperience, t.TeacherRating
ORDER BY t.TeacherRating DESC;

-- 2. Course category quality
SELECT
    CourseCategory,
    COUNT(*) AS course_count,
    ROUND(AVG(CourseRating), 2) AS average_course_rating
FROM courses
GROUP BY CourseCategory
ORDER BY average_course_rating DESC;

-- 3. Monthly transaction activity (SQLite date conversion for day/month/year strings)
SELECT
    substr(TransactionDate, -4) AS transaction_year,
    COUNT(*) AS transaction_rows,
    ROUND(SUM(Amount), 2) AS recorded_amount
FROM transactions
GROUP BY transaction_year
ORDER BY transaction_year;

-- 4. Check for transaction records with unknown instructors
SELECT tr.*
FROM transactions AS tr
LEFT JOIN teachers AS t ON tr.TeacherID = t.TeacherID
WHERE t.TeacherID IS NULL;
