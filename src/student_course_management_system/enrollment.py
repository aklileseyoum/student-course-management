"""Define the Enrollment class and the functions that create and grade enrollments."""

class Enrollment():
    """One student's enrollment in one course, with an optional grade."""

    def __init__(self, student, course, grade=None):
        """Save the student, the course, and the grade (None until graded)."""
        self.student = student
        self.course = course
        self.grade = grade

    def __str__(self):
        """Return the student's name, course, and grade as readable text."""
        return f"Student name: {self.student.name}, course: {self.course.name}, grade: {self.grade}"

    def __repr__(self):
        """Return a developer-friendly description of the enrollment."""
        return f"Enrollment(Student:{repr(self.student)}, course:{repr(self.course)}, grade:{self.grade})"

    @staticmethod
    def is_valid_grade(grade):
        """Return True if the grade is a number from 0 to 100."""
        return 0 <= grade <= 100

    def change_grade(self, grade):
        """Set the grade if it is between 0 and 100 and return a status message."""
        if Enrollment.is_valid_grade(grade):
            self.grade = grade
            return "Grade Successfully Changed"
        
        return "Please enter the grade between 0 and 100."

        


def enroll_student(*args):
    """Create and return an Enrollment from (student, course) or (student, course, grade)."""
    if len(args) == 3:
        return Enrollment(args[0], args[1], args[2])
    else:
        return Enrollment(args[0], args[1])

def grade_student(enrollment: Enrollment, grade):
    """Set the grade on the given enrollment and return the status message."""
    return enrollment.change_grade(grade)