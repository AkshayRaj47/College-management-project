"""
=============================================================================
COLLEGE MANAGEMENT SYSTEM WITH ATTENDANCE & LIBRARY TIMING LOGS
=============================================================================
Python Modules Covered:
- Module 4: Input / Output Operations & String Formatting
- Module 8: Control Flow Statements (Loops, Conditionals)
- Module 9: Functions, Exception Handling & Modules (datetime)
- Module 11: Array Data Structure (from array import array)
- Module 12: Object-Oriented Programming (Classes, Inheritance, Encapsulation)
=============================================================================
"""

import os
from array import array  # Module 11: Array data structure for numeric marks/counts
from datetime import datetime  # Module 10: Date and time tracking module

# =============================================================================
# 1. OOP CLASSES & INHERITANCE (Module 12)
# =============================================================================


class Person:
    """Base Class representing general person attributes across the college."""

    def __init__(self, name, age, mobile, address):
        self.name = name
        self.age = age
        self.mobile = mobile
        self.address = address


class Student(Person):
    """Child Class representing a Student, inheriting from Person."""

    def __init__(
        self, student_id, name, department, age, mobile, address, fees, marks_list
    ):
        super().__init__(name, age, mobile, address)
        self.student_id = student_id
        self.department = department
        self.fees = fees
        # Native Python array structure ('d' = double float) for numerical marks
        self.marks = array("d", [float(m) for m in marks_list if str(m).strip()])

    def calculate_average(self):
        """Calculates average marks using the array structure."""
        if len(self.marks) == 0:
            return 0.0
        return sum(self.marks) / len(self.marks)

    def calculate_grade(self):
        """Determines academic letter grade."""
        avg = self.calculate_average()
        if avg >= 90:
            return "A+"
        elif avg >= 80:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 60:
            return "C"
        elif avg >= 50:
            return "D"
        else:
            return "F"

    def to_file_string(self):
        """Formats student object into a CSV row string."""
        marks_str = ";".join([str(m) for m in self.marks])
        return f"{self.student_id},{self.name},{self.department},{self.age},{self.mobile},{self.address},{self.fees},{marks_str}\n"


class Faculty(Person):
    """Child Class representing Faculty / Teachers."""

    def __init__(self, faculty_id, name, age, department, mobile, address):
        super().__init__(name, age, mobile, address)
        self.faculty_id = faculty_id
        self.department = department

    def to_file_string(self):
        return f"{self.faculty_id},{self.name},{self.age},{self.department},{self.mobile},{self.address}\n"


class Staff(Person):
    """Child Class representing Non-Teaching Staff."""

    def __init__(self, staff_id, name, age, department, mobile, address):
        super().__init__(name, age, mobile, address)
        self.staff_id = staff_id
        self.department = department

    def to_file_string(self):
        return f"{self.staff_id},{self.name},{self.age},{self.department},{self.mobile},{self.address}\n"


# =============================================================================
# 2. CORE COLLEGE MANAGEMENT SYSTEM LOGIC
# =============================================================================


class CollegeManager:
    """Master Orchestrator Class handling operations and persistence files."""

    # Storage File Names
    STUDENTS_FILE = "students.txt"
    FACULTY_FILE = "faculty.txt"
    STAFF_FILE = "staff.txt"
    BOOKS_FILE = "library_books.txt"
    BORROWERS_FILE = "borrowers.txt"

    # Attendance & Timing Logs Storage Files
    STUDENT_ATT_FILE = "student_attendance.txt"
    FACULTY_ATT_FILE = "faculty_attendance.txt"
    STAFF_ATT_FILE = "staff_attendance.txt"
    LIBRARY_LOG_FILE = "library_entry_exit.txt"

    # -------------------------------------------------------------------------
    # HELPER VALIDATION METHODS
    # -------------------------------------------------------------------------
    def _is_valid_id(self, entity_type, entity_id):
        """Checks if a given ID exists in the respective file database."""
        file_map = {
            "student": self.STUDENTS_FILE,
            "faculty": self.FACULTY_FILE,
            "staff": self.STAFF_FILE,
        }
        file_path = file_map.get(entity_type)
        if not file_path or not os.path.exists(file_path):
            return False

        with open(file_path, "r") as f:
            for line in f:
                if line.strip().startswith(entity_id + ","):
                    return True
        return False

    # -------------------------------------------------------------------------
    # 1. STUDENT MANAGEMENT SUB-SYSTEM
    # -------------------------------------------------------------------------
    def manage_students(self):
        while True:
            print("\n--- Student Management Sub-System ---")
            print("1. Add Student")
            print("2. View All Students")
            print("3. Update Student Details")
            print("4. Delete Student")
            print("5. Back to Main Menu")
            choice = input("Enter choice (1-5): ").strip()

            if choice == "1":
                sid = input("Enter Student ID: ").strip()
                name = input("Enter Name: ").strip()
                dept = input("Enter Department/Branch: ").strip()
                age = input("Enter Age: ").strip()
                mobile = input("Enter Mobile: ").strip()
                addr = input("Enter Address: ").strip()
                fees = input("Enter Fees: ").strip()
                raw_marks = input(
                    "Enter Subject Marks (separated by spaces): "
                ).split()

                student = Student(
                    sid, name, dept, age, mobile, addr, fees, raw_marks
                )
                with open(self.STUDENTS_FILE, "a") as f:
                    f.write(student.to_file_string())
                print("Student added successfully!")

            elif choice == "2":
                if not os.path.exists(self.STUDENTS_FILE):
                    print("No student records found.")
                    continue
                with open(self.STUDENTS_FILE, "r") as f:
                    lines = f.readlines()
                if not lines:
                    print("No student records found.")
                    continue

                print("\nList of College Students:")
                for line in lines:
                    p = line.strip().split(",")
                    marks_arr = array(
                        "d", [float(m) for m in p[7].split(";") if m]
                    )
                    avg = (
                        sum(marks_arr) / len(marks_arr) if marks_arr else 0.0
                    )
                    print(
                        f"ID: {p[0]} | Name: {p[1]} | Dept: {p[2]} | Age: {p[3]} | "
                        f"Mobile: {p[4]} | Address: {p[5]} | Fees: ₹{p[6]} | Avg Marks: {avg:.2f}"
                    )

            elif choice == "3":
                sid = input("Enter Student ID to update: ").strip()
                if not os.path.exists(self.STUDENTS_FILE):
                    print("No records found.")
                    continue
                with open(self.STUDENTS_FILE, "r") as f:
                    lines = f.readlines()

                found = False
                with open(self.STUDENTS_FILE, "w") as f:
                    for line in lines:
                        if line.startswith(sid + ","):
                            found = True
                            p = line.strip().split(",")

                            print("\n--- Update Student Details ---")
                            print("(Press ENTER to leave option unchanged)")

                            new_name = input(
                                f"Enter New Name [{p[1]}]: "
                            ).strip()
                            name = new_name if new_name != "" else p[1]

                            new_dept = input(
                                f"Enter New Department [{p[2]}]: "
                            ).strip()
                            dept = new_dept if new_dept != "" else p[2]

                            new_age = input(f"Enter New Age [{p[3]}]: ").strip()
                            age = new_age if new_age != "" else p[3]

                            new_mobile = input(
                                f"Enter New Mobile [{p[4]}]: "
                            ).strip()
                            mobile = new_mobile if new_mobile != "" else p[4]

                            new_addr = input(
                                f"Enter New Address [{p[5]}]: "
                            ).strip()
                            addr = new_addr if new_addr != "" else p[5]

                            new_fees = input(
                                f"Enter New Fees [{p[6]}]: "
                            ).strip()
                            fees = new_fees if new_fees != "" else p[6]

                            current_marks = p[7].replace(";", " ")
                            new_marks_str = input(
                                f"Enter New Marks [{current_marks}]: "
                            ).strip()
                            raw_marks = (
                                new_marks_str.split()
                                if new_marks_str != ""
                                else p[7].split(";")
                            )

                            student = Student(
                                sid,
                                name,
                                dept,
                                age,
                                mobile,
                                addr,
                                fees,
                                raw_marks,
                            )
                            f.write(student.to_file_string())
                            print("Student updated successfully!")
                        else:
                            f.write(line)
                if not found:
                    print("Invalid ID! Student does not exist.")

            elif choice == "4":
                sid = input("Enter Student ID to delete: ").strip()
                if not os.path.exists(self.STUDENTS_FILE):
                    print("No records found.")
                    continue
                with open(self.STUDENTS_FILE, "r") as f:
                    lines = f.readlines()

                found = False
                with open(self.STUDENTS_FILE, "w") as f:
                    for line in lines:
                        if line.startswith(sid + ","):
                            found = True
                            print("Student record deleted!")
                        else:
                            f.write(line)
                if not found:
                    print("Invalid ID! Student does not exist.")

            elif choice == "5":
                break

    # -------------------------------------------------------------------------
    # 2. FACULTY MANAGEMENT SUB-SYSTEM
    # -------------------------------------------------------------------------
    def manage_faculty(self):
        while True:
            print("\n--- Faculty / Professor Management Sub-System ---")
            print("1. Add Faculty Member")
            print("2. View All Faculty Members")
            print("3. Update Faculty Member")
            print("4. Delete Faculty Member")
            print("5. Back to Main Menu")
            choice = input("Enter choice (1-5): ").strip()

            if choice == "1":
                fid = input("Enter Faculty ID: ").strip()
                name = input("Enter Name: ").strip()
                age = input("Enter Age: ").strip()
                dept = input("Enter Department: ").strip()
                mobile = input("Enter Mobile: ").strip()
                addr = input("Enter Address: ").strip()

                fac = Faculty(fid, name, age, dept, mobile, addr)
                with open(self.FACULTY_FILE, "a") as f:
                    f.write(fac.to_file_string())
                print("Faculty added successfully!")

            elif choice == "2":
                if not os.path.exists(self.FACULTY_FILE):
                    print("No faculty records found.")
                    continue
                with open(self.FACULTY_FILE, "r") as f:
                    lines = f.readlines()
                if not lines:
                    print("No faculty records found.")
                    continue

                print("\nList of Faculty Members:")
                for line in lines:
                    fid, name, age, dept, mob, addr = line.strip().split(",")
                    print(
                        f"ID: {fid} | Name: {name} | Age: {age} | Department: {dept} | Mobile: {mob} | Address: {addr}"
                    )

            elif choice == "3":
                fid = input("Enter Faculty ID to update: ").strip()
                if not os.path.exists(self.FACULTY_FILE):
                    print("No records found.")
                    continue
                with open(self.FACULTY_FILE, "r") as f:
                    lines = f.readlines()

                found = False
                with open(self.FACULTY_FILE, "w") as f:
                    for line in lines:
                        if line.startswith(fid + ","):
                            found = True
                            p = line.strip().split(",")

                            print("\n--- Update Faculty Details ---")
                            print("(Press ENTER to leave option unchanged)")

                            new_name = input(
                                f"Enter New Name [{p[1]}]: "
                            ).strip()
                            name = new_name if new_name != "" else p[1]

                            new_age = input(f"Enter New Age [{p[2]}]: ").strip()
                            age = new_age if new_age != "" else p[2]

                            new_dept = input(
                                f"Enter New Department [{p[3]}]: "
                            ).strip()
                            dept = new_dept if new_dept != "" else p[3]

                            new_mob = input(
                                f"Enter New Mobile [{p[4]}]: "
                            ).strip()
                            mob = new_mob if new_mob != "" else p[4]

                            new_addr = input(
                                f"Enter New Address [{p[5]}]: "
                            ).strip()
                            addr = new_addr if new_addr != "" else p[5]

                            fac = Faculty(fid, name, age, dept, mob, addr)
                            f.write(fac.to_file_string())
                            print("Faculty details updated successfully!")
                        else:
                            f.write(line)
                if not found:
                    print("Invalid ID! Faculty member does not exist.")

            elif choice == "4":
                fid = input("Enter Faculty ID to delete: ").strip()
                if not os.path.exists(self.FACULTY_FILE):
                    print("No records found.")
                    continue
                with open(self.FACULTY_FILE, "r") as f:
                    lines = f.readlines()

                found = False
                with open(self.FACULTY_FILE, "w") as f:
                    for line in lines:
                        if line.startswith(fid + ","):
                            found = True
                            print("Faculty record deleted successfully!")
                        else:
                            f.write(line)
                if not found:
                    print("Invalid ID! Faculty member does not exist.")

            elif choice == "5":
                break

    # -------------------------------------------------------------------------
    # 3. STAFF MANAGEMENT SUB-SYSTEM
    # -------------------------------------------------------------------------
    def manage_staff(self):
        while True:
            print("\n--- Non-Teaching Staff Management Sub-System ---")
            print("1. Add Staff Member")
            print("2. View All Staff Members")
            print("3. Update Staff Member")
            print("4. Delete Staff Member")
            print("5. Back to Main Menu")
            choice = input("Enter choice (1-5): ").strip()

            if choice == "1":
                sid = input("Enter Staff ID: ").strip()
                name = input("Enter Name: ").strip()
                age = input("Enter Age: ").strip()
                dept = input("Enter Department: ").strip()
                mobile = input("Enter Mobile: ").strip()
                addr = input("Enter Address: ").strip()

                stf = Staff(sid, name, age, dept, mobile, addr)
                with open(self.STAFF_FILE, "a") as f:
                    f.write(stf.to_file_string())
                print("Staff member added successfully!")

            elif choice == "2":
                if not os.path.exists(self.STAFF_FILE):
                    print("No staff records found.")
                    continue
                with open(self.STAFF_FILE, "r") as f:
                    lines = f.readlines()
                if not lines:
                    print("No staff records found.")
                    continue

                print("\nList of Staff Members:")
                for line in lines:
                    sid, name, age, dept, mob, addr = line.strip().split(",")
                    print(
                        f"ID: {sid} | Name: {name} | Age: {age} | Department: {dept} | Mobile: {mob} | Address: {addr}"
                    )

            elif choice == "3":
                sid = input("Enter Staff ID to update: ").strip()
                if not os.path.exists(self.STAFF_FILE):
                    print("No records found.")
                    continue
                with open(self.STAFF_FILE, "r") as f:
                    lines = f.readlines()

                found = False
                with open(self.STAFF_FILE, "w") as f:
                    for line in lines:
                        if line.startswith(sid + ","):
                            found = True
                            p = line.strip().split(",")

                            print("\n--- Update Staff Details ---")
                            print("(Press ENTER to leave option unchanged)")

                            new_name = input(
                                f"Enter New Name [{p[1]}]: "
                            ).strip()
                            name = new_name if new_name != "" else p[1]

                            new_age = input(f"Enter New Age [{p[2]}]: ").strip()
                            age = new_age if new_age != "" else p[2]

                            new_dept = input(
                                f"Enter New Department [{p[3]}]: "
                            ).strip()
                            dept = new_dept if new_dept != "" else p[3]

                            new_mob = input(
                                f"Enter New Mobile [{p[4]}]: "
                            ).strip()
                            mob = new_mob if new_mob != "" else p[4]

                            new_addr = input(
                                f"Enter New Address [{p[5]}]: "
                            ).strip()
                            addr = new_addr if new_addr != "" else p[5]

                            stf = Staff(sid, name, age, dept, mob, addr)
                            f.write(stf.to_file_string())
                            print("Staff record updated successfully!")
                        else:
                            f.write(line)
                if not found:
                    print("Invalid ID! Staff member does not exist.")

            elif choice == "4":
                sid = input("Enter Staff ID to delete: ").strip()
                if not os.path.exists(self.STAFF_FILE):
                    print("No records found.")
                    continue
                with open(self.STAFF_FILE, "r") as f:
                    lines = f.readlines()

                found = False
                with open(self.STAFF_FILE, "w") as f:
                    for line in lines:
                        if line.startswith(sid + ","):
                            found = True
                            print("Staff member deleted successfully!")
                        else:
                            f.write(line)
                if not found:
                    print("Invalid ID! Staff member does not exist.")

            elif choice == "5":
                break

    # -------------------------------------------------------------------------
    # 4. LIBRARY MANAGEMENT SUB-SYSTEM
    # -------------------------------------------------------------------------
    def manage_library(self):
        while True:
            print("\n--- College Library Management Sub-System ---")
            print("1. Add Book")
            print("2. View Books in Library")
            print("3. Borrow Book")
            print("4. View Borrowed Books")
            print("5. Update Book Details")
            print("6. Return Book")
            print("7. Delete Book")
            print("8. Back to Main Menu")
            choice = input("Enter choice (1-8): ").strip()

            if choice == "1":
                bid = input("Enter Book ID: ").strip()
                title = input("Enter Book Title: ").strip()
                author = input("Enter Author: ").strip()
                pub = input("Enter Publisher: ").strip()
                year = input("Enter Publication Year: ").strip()
                price = input("Enter Price: ").strip()

                with open(self.BOOKS_FILE, "a") as f:
                    f.write(f"{bid},{title},{author},{pub},{year},{price}\n")
                print("Book added successfully!")

            elif choice == "2":
                if not os.path.exists(self.BOOKS_FILE):
                    print("No books found.")
                    continue
                with open(self.BOOKS_FILE, "r") as f:
                    lines = f.readlines()
                if not lines:
                    print("No books found.")
                    continue

                print("\nLibrary Books Catalog:")
                for line in lines:
                    bid, title, author, pub, yr, price = line.strip().split(",")
                    print(
                        f"ID: {bid} | Title: {title} | Author: {author} | Publisher: {pub} | Year: {yr} | Price: ₹{price}"
                    )

            elif choice == "3":
                sid = input("Enter Student ID: ").strip()
                if not self._is_valid_id("student", sid):
                    print("Invalid ID! Student does not exist.")
                    continue
                sname = input("Enter Student Name: ").strip()
                dept = input("Enter Department: ").strip()
                bid = input("Enter Book ID to borrow: ").strip()

                with open(self.BORROWERS_FILE, "a") as f:
                    f.write(f"{sid},{sname},{dept},{bid}\n")
                print(f"Book ID {bid} issued to Student {sname} successfully!")

            elif choice == "4":
                if not os.path.exists(self.BORROWERS_FILE):
                    print("No borrowing records found.")
                    continue
                with open(self.BORROWERS_FILE, "r") as f:
                    lines = f.readlines()
                if not lines:
                    print("No borrowing records found.")
                    continue

                print("\nBorrowed Books Log:")
                for line in lines:
                    sid, sname, dept, bid = line.strip().split(",")
                    print(
                        f"Student ID: {sid} | Student Name: {sname} | Department: {dept} | Book ID: {bid}"
                    )

            elif choice == "5":
                bid = input("Enter Book ID to update: ").strip()
                if not os.path.exists(self.BOOKS_FILE):
                    print("No books found.")
                    continue
                with open(self.BOOKS_FILE, "r") as f:
                    lines = f.readlines()

                found = False
                with open(self.BOOKS_FILE, "w") as f:
                    for line in lines:
                        if line.startswith(bid + ","):
                            found = True
                            p = line.strip().split(",")

                            print("\n--- Update Book Details ---")
                            print("(Press ENTER to leave option unchanged)")

                            new_title = input(
                                f"Enter New Title [{p[1]}]: "
                            ).strip()
                            title = new_title if new_title != "" else p[1]

                            new_author = input(
                                f"Enter New Author [{p[2]}]: "
                            ).strip()
                            author = new_author if new_author != "" else p[2]

                            new_pub = input(
                                f"Enter New Publisher [{p[3]}]: "
                            ).strip()
                            pub = new_pub if new_pub != "" else p[3]

                            new_yr = input(f"Enter New Year [{p[4]}]: ").strip()
                            yr = new_yr if new_yr != "" else p[4]

                            new_price = input(
                                f"Enter New Price [{p[5]}]: "
                            ).strip()
                            price = new_price if new_price != "" else p[5]

                            f.write(
                                f"{bid},{title},{author},{pub},{yr},{price}\n"
                            )
                            print("Book details updated successfully!")
                        else:
                            f.write(line)
                if not found:
                    print("Invalid ID! Book does not exist.")

            elif choice == "6":
                sid = input("Enter Student ID: ").strip()
                bid = input("Enter Book ID to return: ").strip()

                if not os.path.exists(self.BORROWERS_FILE):
                    print("No borrowing records found.")
                    continue
                with open(self.BORROWERS_FILE, "r") as f:
                    lines = f.readlines()

                found = False
                with open(self.BORROWERS_FILE, "w") as f:
                    for line in lines:
                        details = line.strip().split(",")
                        if details[0] == sid and details[3] == bid:
                            found = True
                            print("Book returned successfully!")
                        else:
                            f.write(line)
                if not found:
                    print("No matching borrow record found.")

            elif choice == "7":
                bid = input("Enter Book ID to delete: ").strip()
                if not os.path.exists(self.BOOKS_FILE):
                    print("No books found.")
                    continue
                with open(self.BOOKS_FILE, "r") as f:
                    lines = f.readlines()

                found = False
                with open(self.BOOKS_FILE, "w") as f:
                    for line in lines:
                        if line.startswith(bid + ","):
                            found = True
                            print("Book removed from catalog!")
                        else:
                            f.write(line)
                if not found:
                    print("Invalid ID! Book does not exist.")

            elif choice == "8":
                break

    # -------------------------------------------------------------------------
    # 5. ATTENDANCE & LIBRARY TIMINGS MANAGEMENT SUB-SYSTEM
    # -------------------------------------------------------------------------
    def manage_attendance_and_logs(self):
        while True:
            print(
                "\n=========================================================="
            )
            print("       ATTENDANCE & LIBRARY TIMING MARKER SYSTEM        ")
            print("==========================================================")
            print("1. Mark Attendance (Student / Faculty / Staff)")
            print("2. View Attendance Record (by ID)")
            print("3. Log Library Entry / Exit Timings")
            print("4. View Library Timing Logs (by ID)")
            print("5. Back to Main Menu")
            choice = input("Enter your choice (1-5): ").strip()

            if choice == "1":
                print("\nSelect Category to Mark Attendance:")
                print("1. Student | 2. Faculty | 3. Non-Teaching Staff")
                cat = input("Enter choice (1-3): ").strip()

                cat_map = {"1": "student", "2": "faculty", "3": "staff"}
                file_map = {
                    "student": self.STUDENT_ATT_FILE,
                    "faculty": self.FACULTY_ATT_FILE,
                    "staff": self.STAFF_ATT_FILE,
                }

                entity_type = cat_map.get(cat)
                if not entity_type:
                    print("Invalid selection.")
                    continue

                entity_id = input(f"Enter {entity_type.capitalize()} ID: ").strip()

                # ID Existence Check
                if not self._is_valid_id(entity_type, entity_id):
                    print("Invalid ID! Person does not exist in system.")
                    continue

                today_date = datetime.now().strftime("%Y-%m-%d")

                # Record attendance entry
                with open(file_map[entity_type], "a") as f:
                    f.write(f"{entity_id},{today_date}\n")
                print(
                    f"Attendance marked successfully for {entity_type.capitalize()} ID {entity_id} on {today_date}!"
                )

            elif choice == "2":
                print("\nSelect Category to View Attendance:")
                print("1. Student | 2. Faculty | 3. Non-Teaching Staff")
                cat = input("Enter choice (1-3): ").strip()

                cat_map = {"1": "student", "2": "faculty", "3": "staff"}
                file_map = {
                    "student": self.STUDENT_ATT_FILE,
                    "faculty": self.FACULTY_ATT_FILE,
                    "staff": self.STAFF_ATT_FILE,
                }

                entity_type = cat_map.get(cat)
                if not entity_type:
                    print("Invalid selection.")
                    continue

                entity_id = input(f"Enter {entity_type.capitalize()} ID: ").strip()

                # ID Existence Check
                if not self._is_valid_id(entity_type, entity_id):
                    print("Invalid ID! Person does not exist in system.")
                    continue

                att_file = file_map[entity_type]
                if not os.path.exists(att_file):
                    print("No attendance records logged yet.")
                    continue

                dates_present = []
                with open(att_file, "r") as f:
                    for line in f:
                        parts = line.strip().split(",")
                        if parts[0] == entity_id:
                            dates_present.append(parts[1])

                # Array Data Structure storing numeric counts (Module 11)
                days_count_array = array("i", [len(dates_present)])

                print(
                    f"\n--- ATTENDANCE REPORT FOR ID: {entity_id} ({entity_type.upper()}) ---"
                )
                print(f"Total Days Present: {days_count_array[0]}")
                if dates_present:
                    print("Dates Present:")
                    for d in dates_present:
                        print(f"  - {d}")
                else:
                    print("No attendance records logged for this ID.")

            elif choice == "3":
                print("\nSelect Category for Library Visit:")
                print("1. Student | 2. Faculty | 3. Non-Teaching Staff")
                cat = input("Enter choice (1-3): ").strip()

                cat_map = {"1": "student", "2": "faculty", "3": "staff"}
                entity_type = cat_map.get(cat)
                if not entity_type:
                    print("Invalid selection.")
                    continue

                entity_id = input(f"Enter {entity_type.capitalize()} ID: ").strip()

                # ID Validation
                if not self._is_valid_id(entity_type, entity_id):
                    print("Invalid ID! Person does not exist in system.")
                    continue

                now = datetime.now()
                current_date = now.strftime("%Y-%m-%d")
                current_time = now.strftime("%H:%M:%S")

                print(f"1. Log Entry Time (Current Time: {current_time})")
                print("2. Log Exit Time")
                sub_choice = input("Select Option (1-2): ").strip()

                if sub_choice == "1":
                    with open(self.LIBRARY_LOG_FILE, "a") as f:
                        f.write(
                            f"{entity_id},{entity_type},{current_date},{current_time},IN-PROGRESS\n"
                        )
                    print(
                        f"Entry logged successfully for {entity_id} at {current_time} on {current_date}."
                    )

                elif sub_choice == "2":
                    if not os.path.exists(self.LIBRARY_LOG_FILE):
                        print("No active entry logs found.")
                        continue

                    with open(self.LIBRARY_LOG_FILE, "r") as f:
                        lines = f.readlines()

                    found = False
                    with open(self.LIBRARY_LOG_FILE, "w") as f:
                        for line in lines:
                            p = line.strip().split(",")
                            # Matching active entry without exit log
                            if (
                                p[0] == entity_id
                                and p[2] == current_date
                                and p[4] == "IN-PROGRESS"
                                and not found
                            ):
                                found = True
                                f.write(
                                    f"{p[0]},{p[1]},{p[2]},{p[3]},{current_time}\n"
                                )
                                print(
                                    f"Exit logged successfully for {entity_id} at {current_time}."
                                )
                            else:
                                f.write(line)
                    if not found:
                        print("No active entry log found for today to exit.")

            elif choice == "4":
                entity_id = input("Enter Person ID to view library logs: ").strip()

                # Validate across all groups
                is_valid = (
                    self._is_valid_id("student", entity_id)
                    or self._is_valid_id("faculty", entity_id)
                    or self._is_valid_id("staff", entity_id)
                )

                if not is_valid:
                    print("Invalid ID! Person does not exist in system.")
                    continue

                if not os.path.exists(self.LIBRARY_LOG_FILE):
                    print("No library logs found.")
                    continue

                print(
                    f"\n--- LIBRARY ENTRY & EXIT TIMING LOGS FOR ID: {entity_id} ---"
                )
                logs_found = False
                with open(self.LIBRARY_LOG_FILE, "r") as f:
                    for line in f:
                        p = line.strip().split(",")
                        if p[0] == entity_id:
                            logs_found = True
                            print(
                                f"Date: {p[2]} | Role: {p[1].capitalize()} | Entry Time: {p[3]} | Exit Time: {p[4]}"
                            )
                if not logs_found:
                    print("No library timing records found for this ID.")

            elif choice == "5":
                break


# =============================================================================
# 3. MAIN APPLICATION ENTRYPOINT
# =============================================================================


def main():
    manager = CollegeManager()

    while True:
        print("\n==========================================")
        print("     COLLEGE MANAGEMENT SYSTEM (CLI)     ")
        print("==========================================")
        print("1. Manage Students")
        print("2. Manage Faculty / Teachers")
        print("3. Manage Non-Teaching Staff")
        print("4. Manage Library System")
        print("5. Attendance & Library Entry/Exit Logs")
        print("6. Exit Program")
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            manager.manage_students()
        elif choice == "2":
            manager.manage_faculty()
        elif choice == "3":
            manager.manage_staff()
        elif choice == "4":
            manager.manage_library()
        elif choice == "5":
            manager.manage_attendance_and_logs()
        elif choice == "6":
            print("\nExiting College Management System. Goodbye!")
            break
        else:
            print("Invalid selection! Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()