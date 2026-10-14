# Data dictionary

## teachers.csv
| Column | Meaning |
|---|---|
| TeacherID | Instructor identifier |
| TeacherName | Instructor display name |
| Age | Instructor age |
| Gender | Instructor gender as supplied |
| Expertise | Instructor expertise area |
| YearsOfExperience | Years of teaching experience |
| TeacherRating | Supplied aggregate instructor rating |

## courses.csv
| Column | Meaning |
|---|---|
| CourseID | Course identifier |
| CourseName | Course title |
| CourseCategory | Course subject category |
| CourseType | Course type, e.g. free/paid |
| CourseLevel | Course difficulty level |
| CoursePrice | Listed course price |
| CourseDuration | Course duration as supplied; confirm unit with data owner |
| CourseRating | Supplied aggregate course rating |

## transactions.csv
| Column | Meaning |
|---|---|
| TransactionID | Transaction identifier |
| UserID | User identifier |
| CourseID | Course identifier |
| TransactionDate | Date string, parsed as day/month/year |
| Amount | Recorded transaction amount |
| PaymentMethod | Recorded payment method |
| TeacherID | Instructor identifier associated with transaction |

## users_public.csv
| Column | Meaning |
|---|---|
| UserID | User identifier retained for joins |
| Age | User age |
| Gender | User gender as supplied |

The original Users table also contained names and emails. Those fields are deliberately excluded from this project copy.
