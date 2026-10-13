# Student Course Management System

A console application for managing students, courses, and enrollments. Students can register, enroll in courses, and view their summaries. Instructors can add courses, grade students, and view course averages and rosters.

**Demo video:** [Watch on Loom](https://www.loom.com/share/8566dac01a2e406bbeeab5db7183b1a5)

## Setup

**Requirements:** Python 3.14 or newer, and [Poetry](https://python-poetry.org/docs/#installation).

1. Clone the repository:
```
   git clone <YOUR-REPO-URL>
   cd student_course_management_system
```
2. Install the project:
```
   poetry install
```

## Usage

Run the program from the project's top folder:

```
poetry run python src/student_course_management_system/main.py
```

**Student menu**
1. **Register:** enter a name and choose Undergraduate or Graduate.
2. **Enroll in a course:** enter your ID and pick from the courses available at your level (courses you are already in are hidden).
3. **View summaries:** enter your ID to see your courses, grades, and average.

**Instructor menu**
1. **Add course:** enter a name and choose Undergraduate or Graduate.
2. **Grade a student:** enter a student ID, pick one of their enrollments, and enter a grade from 0 to 100.
3. **View average:** see the average grade of every course.
4. **View roster:** see which students are enrolled in a course.

Data is kept in memory only, so it is lost when the program closes.

## Sample Output

Student summary:

```
==============================
             Ana
==============================
Course                   Grade
------------------------------
Math                        80
Biology                    N/A
------------------------------
Average                   80.0
```

Course averages:

```
=================================
Courses                   Average
=================================
Math                         80.0
Biology             No grades yet
```

## Project Structure

```
student_course_management_system/
├── pyproject.toml
├── README.md
├── src/student_course_management_system/
│   ├── main.py         # interactive menus and in-memory storage
│   ├── student.py      # Student (abstract), GraduateStudent, UndergraduateStudent
│   ├── course.py       # Course class and add_course()
│   ├── enrollment.py   # Enrollment class, enroll_student(), grade_student()
│   └── utils.py        # helper functions (screen clearing)
└── tests/
```

## Design Notes

- **Abstract base class:** `Student` is abstract; each child (`GraduateStudent`, `UndergraduateStudent`) overrides `welcome()` and sets its own level.
- **Encapsulation:** the student's level is a private class value exposed through a read-only `@property`.
- **Level rule:** students only see courses that match their level.
- **Data structures:** dictionaries map IDs to students and courses; a `defaultdict(set)` holds each student's enrollments, so a student cannot enroll in the same course twice.
- **Magic methods:** `__repr__` on the main classes, and `__eq__` / `__hash__` on `Course` (compared by name).
- **`@classmethod`:** `Student.from_text()` builds a student from text like `"Ana,1"`.
- **`@staticmethod`:** `Enrollment.is_valid_grade()` checks that a grade is between 0 and 100.
- **`*args` / `**kwargs`:** used in `calculate_average()`, `enroll_student()`, `add_student()`, and `add_course()`.
- **Comprehensions:** used to build rosters and to collect grades for averages.