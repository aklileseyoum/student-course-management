"""Define the Course class and a factory function for creating courses."""

class Course():
    """A course with a name, an ID number, and a level."""

    def __init__(self, name, id_no, level):
        """Save the course's name, ID number, and level."""
        self.name = name
        self.id_no = id_no
        self.level = level

    def __str__(self):
        """Return the course's name as readable text."""
        return f"{self.name}"

    def __repr__(self):
        """Return a developer-friendly description of the course."""
        return f"Course(name={self.name},id_no={self.id_no},level={self.level})"

    def __eq__(self, other):
        """Return True if both courses have the same name."""
        return self.name == other.name

    def __hash__(self):
        """Hash on the course name, the same field __eq__ is meant to compare."""
        return hash(self.name)
    


def add_course(**kwargs):
    """Create and return a course; level "1" is Undergraduate, anything else is Graduate."""
    if kwargs["level"] == "1":
        return Course(kwargs["name"], kwargs["id_no"], "Undergraduate")

    return Course(kwargs["name"], kwargs["id_no"], "Graduate")