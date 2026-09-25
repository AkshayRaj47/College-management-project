# College-management-project
A comprehensive Python Command-Line Interface (CLI) application designed to manage college administrative tasks—including Students, Faculty, Non-Teaching Staff, and Library Catalog—along with a dedicated Attendance and Library Entry/Exit Timing Tracker.

---

## Key Features

- **Student Management**: Add, view, update, and delete student records. Tracks academic marks, calculates individual averages, and determines academic letter grades ($A+$, $A$, $B$, etc.) dynamically.
- **Faculty & Staff Management**: Separate workflows to maintain personnel details for both teaching faculty and non-teaching staff.
- **Library Catalog & Borrowing**: Maintain book inventories, issue books to validated IDs, track borrowed items, and process returns.
- **Attendance Tracking**: Mark attendance for Students, Faculty, and Non-Teaching Staff. View aggregated days present and specific attendance dates logged by ID.
- **Library Entry/Exit Timing Tracker**: Log timestamped check-ins and check-outs for library visitors (Students, Faculty, or Staff).
- **ID Validation & Record Safeguards**: 
  - Prevents orphan or invalid records by checking system IDs prior to issuing books or logging attendance.
  - Interactive details updater allows users to press `ENTER` to retain existing records without re-keying data.

---

## Technical Stack & Modules Covered

The application is written in **Python 3** using standard library modules with zero third-party dependencies:

- **Module 4 (Input/Output & String Formatting)**: Custom CLI prompts and string formatting for records.
- **Module 8 (Control Flow)**: Loops and nested conditionals driving system logic and menu routing.
- **Module 9 (Functions, Exception Handling & Modules)**: Modular structure using native modules (`os`, `datetime`).
- **Module 11 (Array Data Structure)**: Leverages Python's native `array` module (`from array import array`) for storing numerical values (student marks, attendance counts).
- **Module 12 (Object-Oriented Programming)**: Demonstrates Class Inheritance, Methods, and Encapsulation (`Person` base class inherited by `Student`, `Faculty`, and `Staff`).

---

## Project Structure & Data Storage

All data is automatically persisted across sessions in plain text files in the project root directory:

```text
├── main.py                     # Main application entry point and logic
├── students.txt                # Student records database
├── faculty.txt                 # Faculty records database
├── staff.txt                   # Staff records database
├── library_books.txt           # Library book catalog
├── borrowers.txt               # Borrowed books record log
├── student_attendance.txt      # Student attendance log
├── faculty_attendance.txt      # Faculty attendance log
├── staff_attendance.txt        # Staff attendance log
└── library_entry_exit.txt      # Library check-in/check-out timestamp log
```
Installation & Running the Application
Prerequisites
Python 3.7 or higher installed on your system.

Running the Program
Clone or download the source file main.py into a folder.

Open a terminal or command prompt in that directory.

Run the following command:

Bash
python main.py
Usage Guide
Main Menu
Upon starting, choose from the main options:

```Plaintext
COLLEGE MANAGEMENT SYSTEM     
1. Manage Students
2. Manage Faculty / Teachers
3. Manage Non-Teaching Staff
4. Manage Library System
5. Attendance & Library Entry/Exit Logs
6. Exit Program
```
Updating Records
When updating an entity (Student, Faculty, Staff, or Book), the system displays the current stored value inside square brackets [...].

To change a value: Type the new value and press ENTER.

To keep existing value: Simply press ENTER without typing anything.

Attendance & Library Tracking
Choose option 5 from the main menu.

Mark Attendance: Select the entity role (Student, Faculty, or Staff) and enter their ID. The system captures the current date (YYYY-MM-DD).

Library Timings: Log Entry or Exit. Check-ins capture real-time timestamps (HH:MM:SS).
