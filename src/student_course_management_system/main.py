"""Run the Student Course Management System, an interactive console menu.

Students can register, enroll in courses, and view their summaries.
Instructors can add courses, grade students, and view course averages.
"""

from student import add_student
from course import add_course
from utils import wipe
from enrollment import grade_student, enroll_student
from collections import defaultdict

# Next ID numbers to hand out
stud_id = 1
cour_id = 1

# Storage: IDs map to objects; each student maps to a set of their enrollments
courses = {}
students = {}
enrollment = defaultdict(set)

def calculate_average(*grades):
    """Return the average of the given grades, or None if there are none."""
    if not grades:
        return None
    return sum(grades) / len(grades)

def calculate_averages(enrollment):
    """Return {course name: average grade} across all students.

    The value is None for a course that has no grades yet.
    """
    # Collect every graded mark under its course name
    grades_by_course = defaultdict(list)
    for enrolls in enrollment.values():         
        for e in enrolls:
            grades = grades_by_course[e.course.name]   
            if e.grade is not None:
                grades.append(e.grade)
    return {name: calculate_average(*grades)
            for name, grades in grades_by_course.items()}

def view_summary(st_obj):
    """Print a student's courses and grades, with the average of graded courses."""
    print("=" * 30)
    print(f"{st_obj.name:^30}")                   
    print("=" * 30)
    print(f"{'Course':<20}{'Grade':>10}") 
    print("-" * 30)
    total = 0
    graded = 0
    for each in enrollment[st_obj]:
        # Ungraded courses show "N/A" and are left out of the average
        grade = each.grade if each.grade is not None else "N/A"
        if grade != "N/A":
            total += grade
            graded += 1
        course = each.course
        print(f"{course.name:<20}{grade:>10}") 
    print("-" * 30)
    avg_text = f"{total / graded:.1f}" if graded else "N/A"
    print(f"{'Average':<20}{avg_text:>10}")

# Main menu loop: runs until the user exits
while True:
    wipe()
    print("=" * 60)
    print(f"{'Welcome to Student Course Management System':^60}")
    print("=" * 60)

    print("Are you: ")
    print("1. Student")
    print("2. Instructor")
    print("3. Exit\n")

    choice = input("Choose: ")

    # ---------- Student menu ----------
    if choice == "1":
        wipe()
        print("Do you want to: ")
        print("1. Register")
        print("2. Enroll in a course")
        print("3. View Summaries\n")

        choize = input("Choose: ")

        # Register a new student
        if choize == "1":
            wipe()
            name = input("Please enter your name: ").strip()

            # Reject an empty name
            if name == "":
                print("Name can't be empty.")
                to_continue = input("Press enter to go back or 0 to exit: ")
                if to_continue == "0":
                    break
                continue

            print("Are you: ")
            print("1. Undergraduate Student")
            print("2. Graduate Student\n")

            level = input("Choose: ")

            if level == "1" or level == "2":
                # Create the right student type and store it by ID
                stud_obj = add_student(name=name, id_no=stud_id, level=level)
                print(stud_obj.welcome())
                students[stud_id] = stud_obj
                stud_id += 1

            else:
                print("Wrong input please try again.")

            # Pause so the message can be read; 0 exits the program
            to_continue = input("Press enter to go back or 0 to exit: ")
            if to_continue == "0":
                break


        # Enroll in a course
        elif choize == "2":
            wipe()
            id_no = input("Please enter your ID number: ")

            # The ID must be a number that belongs to a registered student
            if not id_no.isdigit() or int(id_no) not in students:
                print("Student not found.")
                to_continue = input("\nPress enter to go back or 0 to exit: ")
                if to_continue == "0":
                    break
                continue

            stud_obj = students[int(id_no)]
            viable_courses = []
            enrolled_courses = set()
            
            if enrollment:
                enrolled_courses = enrollment[stud_obj]
            
            # Offer only courses of the student's level that they aren't already in
            for course in courses.values():
                if course.level == stud_obj.level and not any(e.course.id_no == course.id_no for e in enrolled_courses):
                    viable_courses.append(course)

            # Nothing to enroll in
            if not viable_courses:
                print("No courses available to enroll in.")
                to_continue = input("\nPress enter to go back or 0 to exit: ")
                if to_continue == "0":
                    break
                continue

            print("Choose the course you want to enroll in")
            for index in range(len(viable_courses)):
                print(f"{index+1}. {viable_courses[index].name}")

            course = input("\nChoose: ")

            # The pick must be a number within the list
            if not course.isdigit() or not 1 <= int(course) <= len(viable_courses):
                print("Wrong input please try again.")
                to_continue = input("\nPress enter to go back or 0 to exit: ")
                if to_continue == "0":
                    break
                continue

            # Create the enrollment and add it to this student's set
            enroll_obj = enroll_student(stud_obj, viable_courses[int(course) -  1], None)
            enrollment[stud_obj].add(enroll_obj)
            print("\nYou have succesfully enrolled.")
            to_continue = input("\nPress enter to go back or 0 to exit: ")
            if to_continue == "0":
                break

        # View a student's summary
        elif choize == "3":
            wipe()
            id_no = input("Please enter your ID number: ")

            # The ID must be a number that belongs to a registered student
            if not id_no.isdigit() or int(id_no) not in students:
                print("Student not found.")
                to_continue = input("\nPress enter to go back or 0 to exit: ")
                if to_continue == "0":
                    break
                continue

            stud_obj = students[int(id_no)]
            # A student with no enrollments has nothing to summarize
            if not enrollment.get(stud_obj):
                print("\nYou are not enrolled in any course yet.")
            else:
                view_summary(stud_obj)
            to_continue = input("\nPress enter to go back or 0 to exit: ")
            if to_continue == "0":
                break

        # Any other student-menu input
        else:
            print("Wrong input please try again.")
            to_continue = input("\nPress enter to go back or 0 to exit: ")
            if to_continue == "0":
                break

    # ---------- Instructor menu ----------
    elif choice == "2":
        wipe()
        print("Do you want to: ")
        print("1. Add course")
        print("2. Grade a student")
        print("3. View Average")
        print("4. View Roster")

        choize = input("Choose: ")

        # Add a new course
        if choize == "1":
            wipe()
            name = input("Write the name of the course: ").strip()

            # Reject an empty course name
            if name == "":
                print("Course name can't be empty.")
                to_continue = input("Press enter to go back or 0 to exit: ")
                if to_continue == "0":
                    break
                continue

            # Reject a duplicate name (case-insensitive)
            if any(c.name.lower() == name.lower() for c in courses.values()):
                print("A course with that name already exists.")
                to_continue = input("Press enter to go back or 0 to exit: ")
                if to_continue == "0":
                    break
                continue

            print("Is the course: ")
            print("1. Undergraduate Course")
            print("2. Graduate Course\n")

            level = input("Choose: ")
            if level == "1" or level == "2":    
                # Create the course and store it by ID
                cour_obj = add_course(name=name, id_no=cour_id, level=level)
                courses[cour_id] = cour_obj
                cour_id += 1
                print(f"Course {name} got added successfully.")
            else:
                print("Wrong input")
            to_continue = input("Press enter to go back or 0 to exit: ")
            if to_continue == "0":
                break

        # Grade a student
        elif choize == "2":
            wipe()
            st_id = input("Enter the id number of the student you want to grade: ")

            # The ID must be a number that belongs to a registered student
            if not st_id.isdigit() or int(st_id) not in students:
                print("Student not found.")
                to_continue = input("\nPress enter to go back or 0 to exit: ")
                if to_continue == "0":
                    break
                continue

            st_obj = students[int(st_id)]
            enrolls = list(enrollment.get(st_obj, []))

            # Only enrolled students can be graded
            if not enrolls:
                print("This student is not enrolled in any course yet.")
                to_continue = input("\nPress enter to go back or 0 to exit: ")
                if to_continue == "0":
                    break
                continue
            
            print("Please select the course you want to change grade for")
            for index in range(len(enrolls)):
                print(f"{index+1}. {enrolls[index].course.name}")

            enroll = input("Choose: ")

            # The pick must be a number within the list
            if not enroll.isdigit() or not 1 <= int(enroll) <= len(enrolls):
                print("Wrong input please try again.")
                to_continue = input("\nPress enter to go back or 0 to exit: ")
                if to_continue == "0":
                    break
                continue

            grade = input("Enter the grade: ")

            # The grade must be a whole number from 0 to 100
            if not grade.isdigit() or not 0 <= int(grade) <= 100:
                print("Grade must be a whole number between 0 and 100.")
                to_continue = input("\nPress enter to go back or 0 to exit: ")
                if to_continue == "0":
                    break
                continue

            # Save the grade; show the error if the setter rejects it
            try:
                print(grade_student(enrolls[int(enroll) - 1], int(grade)))
            except ValueError as error:
                print(error)
            to_continue = input("\nPress enter to go back or 0 to exit: ")
            if to_continue == "0":
                break

        # View each course's average grade
        elif choize == "3":
            print()
            averages = calculate_averages(enrollment)
            # No enrollments means nothing to average
            if not averages:
                print("No enrollments yet.")
            else:
                print("=" * 33)
                print(f"{'Courses':<20}{'Average':>13}")
                print("=" * 33)
                for name, avg in averages.items():
                    text = "No grades yet" if avg is None else f"{avg:.1f}"
                    print(f"{name:<20}{text:>13}")
            to_continue = input("\nPress enter to go back or 0 to exit: ")
            if to_continue == "0":
                break

        # View the roster (enrolled students) of a course
        elif choize == "4":
            wipe()
            if not courses:
                print("No courses yet.")
            else:
                for cid, c in courses.items():
                    print(f"{cid}. {c.name}")
                cid = input("\nChoose course: ")
                if not cid.isdigit() or int(cid) not in courses:
                    print("Wrong input please try again.")
                else:
                    # Collect the names of students enrolled in this course
                    roster = [e.student.name
                              for enrolls in enrollment.values()
                              for e in enrolls
                              if e.course.id_no == int(cid)]
                    print("\nRoster for", courses[int(cid)].name)
                    if not roster:
                        print("No students enrolled yet.")
                    else:
                        for i, student_name in enumerate(roster, 1):
                            print(f"{i}. {student_name}")
            to_continue = input("\nPress enter to go back or 0 to exit: ")
            if to_continue == "0":
                break

        # Any other instructor-menu input
        else:
            print("Wrong input please try again.")
            to_continue = input("\nPress enter to go back or 0 to exit: ")
            if to_continue == "0":
                break

    
    # ---------- Exit ----------
    elif choice == "3":
        print("\nBye.")
        break

    # Any other main-menu input
    else:
        print("Wrong input please try again.")
        to_continue = input("\nPress enter to go back or 0 to exit: ")
        if to_continue == "0":
            break