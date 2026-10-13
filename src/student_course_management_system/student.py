"""Define the Student base class, its child classes, and a factory function."""

from abc import ABC, abstractmethod

class Student(ABC):
    """Abstract base class for all students, holding the shared data."""

    _level = None

    @property
    def level(self):
        """Return the student's level."""
        return self._level
    
    def __init__(self, name, id_no):
        """Save the student's name and ID number."""
        self.name = name
        self.id_no = id_no

    def __str__(self):
        """Return the student's details as readable text."""
        return f"Student name: {self.name}, Id_no: {self.id_no}, Level: {self.level}"

    def __repr__(self):
        """Return a developer-friendly description of the student."""
        return f"Student(name={self.name}, Id_no={self.id_no}, level={self.level})"

    @classmethod
    def from_text(cls, text):
        """Create a student from text like "Ana,1" (name,id_no)."""
        name, id_no = text.split(",")
        return cls(name.strip(), int(id_no))

    @abstractmethod
    def welcome(self):
        """Return a welcome message; every child class must override this."""
        pass

class GraduateStudent(Student):
    """Student who is enrolled at the graduate level."""

    _level = "Graduate"

    def welcome(self):
        """Return the welcome message for a graduate student."""
        return f"Welcome Graduate Student {self.name}, Your id number is {self.id_no}. You will use it to enroll in courses and view summaries."

class UndergraduateStudent(Student):
    """Student who is enrolled at the undergraduate level."""

    _level = "Undergraduate"

    def welcome(self):
            """Return the welcome message for an undergraduate student."""
            return f"Welcome Undergraduate Student {self.name}, Your id number is {self.id_no}. You will use it to enroll in courses and view summaries."

def add_student(**kwargs):
    """Create and return a student; level "1" is undergraduate, anything else is graduate."""
    if kwargs["level"] == "1":
        stud_obj = UndergraduateStudent(kwargs["name"], kwargs["id_no"])
    else:
        stud_obj = GraduateStudent(kwargs["name"], kwargs["id_no"])
    return stud_obj