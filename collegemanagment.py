"""COLLEGE MANAGEMENT SYSTEM WITH ATTENDANCE & LIBRARY TIMING LOGS
Python Modules Covered:
- Module 4: Input / Output Operations & String Formatting
- Module 8: Control Flow Statements (Loops, Conditionals)
- Module 9: Functions, Exception Handling & Modules (datetime)
- Module 11: Array Data Structure (from array import array)
- Module 12: Object-Oriented Programming (Classes, Inheritance, Encapsulation)"""
import os
from array import array  # Module 11: Array data structure for numeric marks/counts
from datetime import datetime  # Module 10: Date and time tracking module
class Person:
    def __init__(self,name,age,mobile,address):
        self.name=name
        self.age=age
        self.mobile=mobile
        self.address=address
class Student(Person):
    def __init__(self,studentId,name,department,age,mobile,address,fees,marksList):
        super().__init__(name,age,mobile,address)
        self.studentId = studentId
        self.department = department
        self.fees = fees
        # Native Python array structure ('d' = double float) for numerical marks
        self.marks = array("d", [float(m) for m in marksList if str(m).strip()])
    def calculateAverage(self):
        if len(self.marks)==0:
            return 0.0
        return sum(self.marks)/len(self.marks)
    def calculateGrade(self):
        avg=self.calculateAverage()
        if avg>=90:
            return "A+"
        elif avg>=80:
            return "A"
        elif avg>=70:
            return "B"
        elif avg>=60:
            return "C"
        elif avg>=50:
            return "D"
        else:
            return "F"
    def toFileString(self):
        marksStr=";".join([str(m) for m in self.marks])
        return f"{self.studentId},{self.name},{self.department},{self.age},{self.mobile},{self.address},{self.fees},{marksStr}\n"
class Faculty(Person):
    def __init__(self,facultyId,name,age,department,mobile,address):
        super().__init__(name,age,mobile,address)
        self.facultyId=facultyId
        self.department=department
    def toFileString(self):
        return f"{self.facultyId},{self.name},{self.age},{self.department},{self.mobile},{self.address}\n"
class Staff(Person):
    def __init__(self, staffId,name,age,department,mobile,address):
        super().__init__(name,age,mobile,address)
        self.staffId=staffId
        self.department=department

    def toFileString(self):
        return f"{self.staffId},{self.name},{self.age},{self.department},{self.mobile},{self.address}\n"
class CollegeManager:
    # Storage File Names
    studentsFile="students.txt"
    facultyFile="faculty.txt"
    staffFile="staff.txt"
    booksFile="library_books.txt"
    borrowersFile="borrowers.txt"
    # Attendance & Timing Logs Storage Files
    studentAttFile="student_attendance.txt"
    facultyAttFile="faculty_attendance.txt"
    staffAttFile="staff_attendance.txt"
    libraryLogFile="library_entry_exit.txt"
    def isValidId(self, entityType, entityId):
        fileMap = {"student": self.studentsFile,"faculty": self.facultyFile,"staff": self.staffFile,}
        filePath = fileMap.get(entityType)
        if not filePath or not os.path.exists(filePath):
            return False
        with open(filePath, "r") as f:
            for line in f:
                if line.strip().startswith(entityId + ","):
                    return True
        return False
    def manageStudents(self):
        while True:
            print("\nStudent Management Sub-System")
            print("1.Add Student")
            print("2.View All Students")
            print("3.Update Student Details")
            print("4.Delete Student")
            print("5.Back to Main Menu")
            choice = input("Enter choice (1-5):").strip()
            if choice=="1":
                sid=input("Enter Student ID:").strip()
                name=input("Enter Name:").strip()
                dept=input("Enter Department/Branch:").strip()
                age=input("Enter Age:").strip()
                mobile=input("Enter Mobile:").strip()
                addr=input("Enter Address:").strip()
                fees=input("Enter Fees:").strip()
                rawMarks=input("Enter Subject Marks (separated by spaces):").split()
                student=Student(sid, name, dept, age, mobile, addr, fees, rawMarks)
                with open(self.studentsFile,"a") as f:
                    f.write(student.toFileString())
                print("Student added successfully!")
            elif choice=="2":
                if not os.path.exists(self.studentsFile):
                    print("No student records found.")
                    continue
                with open(self.studentsFile,"r") as f:
                    lines = f.readlines()
                if not lines:
                    print("No student records found.")
                    continue
                print("\nList of College Students:")
                for line in lines:
                    p=line.strip().split(",")
                    marksArr=array("d", [float(m) for m in p[7].split(";") if m])
                    avg=(sum(marksArr) / len(marksArr) if marksArr else 0.0)
                    print(f"ID: {p[0]} | Name: {p[1]} | Dept: {p[2]} | Age: {p[3]} | Mobile: {p[4]} | Address: {p[5]} | Fees: ₹{p[6]} | Avg Marks: {avg:.2f}")
            elif choice=="3":
                sid=input("Enter Student ID to update: ").strip()
                if not os.path.exists(self.studentsFile):
                    print("No records found.")
                    continue
                with open(self.studentsFile,"r") as f:
                    lines = f.readlines()
                found=False
                with open(self.studentsFile,"w") as f:
                    for line in lines:
                        if line.startswith(sid + ","):
                            found=True
                            p=line.strip().split(",")
                            print("\nUpdate Student Details")
                            print("(Press ENTER to leave option unchanged)")
                            newName=input(f"Enter New Name [{p[1]}]:").strip()
                            name=newName if newName != "" else p[1]
                            newDept=input(f"Enter New Department [{p[2]}]:").strip()
                            dept=newDept if newDept != "" else p[2]
                            newAge=input(f"Enter New Age [{p[3]}]:").strip()
                            age=newAge if newAge != "" else p[3]
                            newMobile=input(f"Enter New Mobile [{p[4]}]:").strip()
                            mobile=newMobile if newMobile != "" else p[4]
                            newAddr=input(f"Enter New Address [{p[5]}]:").strip()
                            addr=newAddr if newAddr != "" else p[5]
                            newFees=input(f"Enter New Fees [{p[6]}]:").strip()
                            fees=newFees if newFees != "" else p[6]
                            currentMarks=p[7].replace(";", " ")
                            newMarksStr=input(f"Enter New Marks [{currentMarks}]:").strip()
                            rawMarks=(newMarksStr.split() if newMarksStr != "" else p[7].split(";"))
                            student=Student(sid, name, dept, age, mobile, addr, fees, rawMarks)
                            f.write(student.toFileString())
                            print("Student updated successfully!")
                        else:
                            f.write(line)
                if not found:
                    print("Invalid ID! Student does not exist.")
            elif choice=="4":
                sid=input("Enter Student ID to delete:").strip()
                if not os.path.exists(self.studentsFile):
                    print("No records found.")
                    continue
                with open(self.studentsFile,"r") as f:
                    lines = f.readlines()
                found=False
                with open(self.studentsFile,"w") as f:
                    for line in lines:
                        if line.startswith(sid + ","):
                            found=True
                            print("Student record deleted!")
                        else:
                            f.write(line)
                if not found:
                    print("Invalid ID! Student does not exist.")
            elif choice=="5":
                break
    def manageFaculty(self):
        while True:
            print("\nFaculty/Professor Management Sub-System")
            print("1.Add Faculty Member")
            print("2.View All Faculty Members")
            print("3.Update Faculty Member")
            print("4.Delete Faculty Member")
            print("5.Back to Main Menu")
            choice=input("Enter choice (1-5):").strip()
            if choice=="1":
                fid=input("Enter Faculty ID:").strip()
                name=input("Enter Name:").strip()
                age=input("Enter Age:").strip()
                dept=input("Enter Department:").strip()
                mobile=input("Enter Mobile:").strip()
                addr=input("Enter Address:").strip()
                fac=Faculty(fid, name, age, dept, mobile, addr)
                with open(self.facultyFile,"a") as f:
                    f.write(fac.toFileString())
                print("Faculty added successfully!")
            elif choice=="2":
                if not os.path.exists(self.facultyFile):
                    print("No faculty records found.")
                    continue
                with open(self.facultyFile,"r") as f:
                    lines = f.readlines()
                if not lines:
                    print("No faculty records found.")
                    continue
                print("\nList of Faculty Members:")
                for line in lines:
                    fid, name, age, dept, mob, addr = line.strip().split(",")
                    print(f"ID: {fid} | Name: {name} | Age: {age} | Department: {dept} | Mobile: {mob} | Address: {addr}")
            elif choice=="3":
                fid=input("Enter Faculty ID to update:").strip()
                if not os.path.exists(self.facultyFile):
                    print("No records found.")
                    continue
                with open(self.facultyFile,"r") as f:
                    lines = f.readlines()
                found=False
                with open(self.facultyFile,"w") as f:
                    for line in lines:
                        if line.startswith(fid + ","):
                            found=True
                            p=line.strip().split(",")
                            print("\nUpdate Faculty Details")
                            print("(Press ENTER to leave option unchanged)")
                            newName=input(f"Enter New Name [{p[1]}]:").strip()
                            name=newName if newName != "" else p[1]
                            newAge=input(f"Enter New Age [{p[2]}]:").strip()
                            age=newAge if newAge != "" else p[2]
                            newDept=input(f"Enter New Department [{p[3]}]:").strip()
                            dept=newDept if newDept != "" else p[3]
                            newMob=input(f"Enter New Mobile [{p[4]}]:").strip()
                            mob=newMob if newMob != "" else p[4]
                            newAddr=input(f"Enter New Address [{p[5]}]:").strip()
                            addr=newAddr if newAddr != "" else p[5]
                            fac=Faculty(fid, name, age, dept, mob, addr)
                            f.write(fac.toFileString())
                            print("Faculty details updated successfully!")
                        else:
                            f.write(line)
                if not found:
                    print("Invalid ID! Faculty member does not exist.")
            elif choice=="4":
                fid=input("Enter Faculty ID to delete:").strip()
                if not os.path.exists(self.facultyFile):
                    print("No records found.")
                    continue
                with open(self.facultyFile,"r") as f:
                    lines=f.readlines()
                found=False
                with open(self.facultyFile,"w") as f:
                    for line in lines:
                        if line.startswith(fid + ","):
                            found=True
                            print("Faculty record deleted successfully!")
                        else:
                            f.write(line)
                if not found:
                    print("Invalid ID! Faculty member does not exist.")
            elif choice=="5":
                break
    def manageStaff(self):
        while True:
            print("\nNon-Teaching Staff Management Sub-System")
            print("1.Add Staff Member")
            print("2.View All Staff Members")
            print("3.Update Staff Member")
            print("4.Delete Staff Member")
            print("5.Back to Main Menu")
            choice=input("Enter choice (1-5):").strip()
            if choice=="1":
                sid=input("Enter Staff ID:").strip()
                name=input("Enter Name:").strip()
                age=input("Enter Age:").strip()
                dept=input("Enter Department:").strip()
                mobile=input("Enter Mobile:").strip()
                addr=input("Enter Address:").strip()
                stf=Staff(sid, name, age, dept, mobile, addr)
                with open(self.staffFile,"a") as f:
                    f.write(stf.toFileString())
                print("Staff member added successfully!")
            elif choice=="2":
                if not os.path.exists(self.staffFile):
                    print("No staff records found.")
                    continue
                with open(self.staffFile,"r") as f:
                    lines=f.readlines()
                if not lines:
                    print("No staff records found.")
                    continue
                print("\nList of Staff Members:")
                for line in lines:
                    sid,name,age,dept,mob,addr = line.strip().split(",")
                    print(f"ID: {sid} | Name: {name} | Age: {age} | Department: {dept} | Mobile: {mob} | Address: {addr}")
            elif choice=="3":
                sid=input("Enter Staff ID to update:").strip()
                if not os.path.exists(self.staffFile):
                    print("No records found.")
                    continue
                with open(self.staffFile,"r") as f:
                    lines=f.readlines()
                found=False
                with open(self.staffFile,"w") as f:
                    for line in lines:
                        if line.startswith(sid + ","):
                            found=True
                            p = line.strip().split(",")
                            print("\nUpdate Staff Details")
                            print("(Press ENTER to leave option unchanged)")
                            newName=input(f"Enter New Name [{p[1]}]: ").strip()
                            name=newName if newName != "" else p[1]
                            newAge=input(f"Enter New Age [{p[2]}]: ").strip()
                            age=newAge if newAge != "" else p[2]
                            newDept=input(f"Enter New Department [{p[3]}]: ").strip()
                            dept=newDept if newDept != "" else p[3]
                            newMob=input(f"Enter New Mobile [{p[4]}]: ").strip()
                            mob=newMob if newMob != "" else p[4]
                            newAddr=input(f"Enter New Address [{p[5]}]: ").strip()
                            addr=newAddr if newAddr != "" else p[5]
                            stf=Staff(sid, name, age, dept, mob, addr)
                            f.write(stf.toFileString())
                            print("Staff record updated successfully!")
                        else:
                            f.write(line)
                if not found:
                    print("Invalid ID! Staff member does not exist.")
            elif choice=="4":
                sid=input("Enter Staff ID to delete:").strip()
                if not os.path.exists(self.staffFile):
                    print("No records found.")
                    continue
                with open(self.staffFile,"r") as f:
                    lines=f.readlines()
                found=False
                with open(self.staffFile,"w") as f:
                    for line in lines:
                        if line.startswith(sid + ","):
                            found=True
                            print("Staff member deleted successfully!")
                        else:
                            f.write(line)
                if not found:
                    print("Invalid ID! Staff member does not exist.")
            elif choice=="5":
                break
    def manageLibrary(self):
        while True:
            print("\nCollege Library Management Sub-System")
            print("1.Add Book")
            print("2.View Books in Library")
            print("3.Borrow Book")
            print("4.View Borrowed Books")
            print("5.Update Book Details")
            print("6.Return Book")
            print("7.Delete Book")
            print("8.Back to Main Menu")
            choice=input("Enter choice (1-8):").strip()
            if choice=="1":
                bid=input("Enter Book ID:").strip()
                title=input("Enter Book Title:").strip()
                author=input("Enter Author:").strip()
                pub=input("Enter Publisher:").strip()
                year=input("Enter Publication Year:").strip()
                price=input("Enter Price:").strip()
                with open(self.booksFile,"a") as f:
                    f.write(f"{bid},{title},{author},{pub},{year},{price}\n")
                print("Book added successfully!")
            elif choice=="2":
                if not os.path.exists(self.booksFile):
                    print("No books found.")
                    continue
                with open(self.booksFile,"r") as f:
                    lines=f.readlines()
                if not lines:
                    print("No books found.")
                    continue
                print("\nLibrary Books Catalog:")
                for line in lines:
                    bid, title, author, pub, yr, price = line.strip().split(",")
                    print(f"ID: {bid} | Title: {title} | Author: {author} | Publisher: {pub} | Year: {yr} | Price: ₹{price}")
            elif choice=="3":
                sid=input("Enter Student ID:").strip()
                if not self.isValidId("student", sid):
                    print("Invalid ID! Student does not exist.")
                    continue
                sname=input("Enter Student Name:").strip()
                dept=input("Enter Department:").strip()
                bid=input("Enter Book ID to borrow:").strip()
                with open(self.borrowersFile,"a") as f:
                    f.write(f"{sid},{sname},{dept},{bid}\n")
                print(f"Book ID {bid} issued to Student {sname} successfully!")
            elif choice=="4":
                if not os.path.exists(self.borrowersFile):
                    print("No borrowing records found.")
                    continue
                with open(self.borrowersFile,"r") as f:
                    lines=f.readlines()
                if not lines:
                    print("No borrowing records found.")
                    continue
                print("\nBorrowed Books Log:")
                for line in lines:
                    sid, sname, dept, bid = line.strip().split(",")
                    print(f"Student ID: {sid} | Student Name: {sname} | Department: {dept} | Book ID: {bid}")
            elif choice=="5":
                bid=input("Enter Book ID to update:").strip()
                if not os.path.exists(self.booksFile):
                    print("No books found.")
                    continue
                with open(self.booksFile,"r") as f:
                    lines = f.readlines()
                found=False
                with open(self.booksFile,"w") as f:
                    for line in lines:
                        if line.startswith(bid + ","):
                            found=True
                            p = line.strip().split(",")
                            print("\nUpdate Book Details")
                            print("(Press ENTER to leave option unchanged)")
                            newTitle=input(f"Enter New Title [{p[1]}]:").strip()
                            title=newTitle if newTitle != "" else p[1]
                            newAuthor=input(f"Enter New Author [{p[2]}]:").strip()
                            author=newAuthor if newAuthor != "" else p[2]
                            newPub=input(f"Enter New Publisher [{p[3]}]:").strip()
                            pub=newPub if newPub != "" else p[3]
                            newYr=input(f"Enter New Year [{p[4]}]:").strip()
                            yr=newYr if newYr != "" else p[4]
                            newPrice=input(f"Enter New Price [{p[5]}]:").strip()
                            price=newPrice if newPrice != "" else p[5]
                            f.write(f"{bid},{title},{author},{pub},{yr},{price}\n")
                            print("Book details updated successfully!")
                        else:
                            f.write(line)
                if not found:
                    print("Invalid ID! Book does not exist.")
            elif choice=="6":
                sid = input("Enter Student ID:").strip()
                bid = input("Enter Book ID to return:").strip()
                if not os.path.exists(self.borrowersFile):
                    print("No borrowing records found.")
                    continue
                with open(self.borrowersFile,"r") as f:
                    lines=f.readlines()
                found=False
                with open(self.borrowersFile,"w") as f:
                    for line in lines:
                        details=line.strip().split(",")
                        if details[0]==sid and details[3]==bid:
                            found=True
                            print("Book returned successfully!")
                        else:
                            f.write(line)
                if not found:
                    print("No matching borrow record found.")
            elif choice=="7":
                bid=input("Enter Book ID to delete:").strip()
                if not os.path.exists(self.booksFile):
                    print("No books found.")
                    continue
                with open(self.booksFile,"r") as f:
                    lines=f.readlines()
                found=False
                with open(self.booksFile,"w") as f:
                    for line in lines:
                        if line.startswith(bid + ","):
                            found=True
                            print("Book removed from catalog!")
                        else:
                            f.write(line)
                if not found:
                    print("Invalid ID! Book does not exist.")
            elif choice=="8":
                break
    def manageAttendanceAndLogs(self):
        while True:
            print("ATTENDANCE & LIBRARY TIMING MARKER SYSTEM")
            print("1.Mark Attendance (Student / Faculty / Staff)")
            print("2.View Attendance Record (by ID)")
            print("3.Log Library Entry / Exit Timings")
            print("4.View Library Timing Logs (by ID)")
            print("5.Back to Main Menu")
            choice=input("Enter your choice (1-5):").strip()
            if choice=="1":
                print("\nSelect Category to Mark Attendance:")
                print("1. Student | 2. Faculty | 3. Non-Teaching Staff")
                cat=input("Enter choice (1-3):").strip()
                catMap={"1": "student", "2": "faculty", "3": "staff"}
                fileMap={"student": self.studentAttFile,"faculty": self.facultyAttFile,"staff": self.staffAttFile,}
                entityType=catMap.get(cat)
                if not entityType:
                    print("Invalid selection.")
                    continue
                entityId=input(f"Enter {entityType.capitalize()} ID:").strip()
                if not self.isValidId(entityType, entityId):
                    print("Invalid ID! Person does not exist in system.")
                    continue
                todayDate=datetime.now().strftime("%Y-%m-%d")
                with open(fileMap[entityType],"a") as f:
                    f.write(f"{entityId},{todayDate}\n")
                print(f"Attendance marked successfully for {entityType.capitalize()} ID {entityId} on {todayDate}!")
            elif choice == "2":
                print("\nSelect Category to View Attendance:")
                print("1.Student | 2.Faculty | 3.Non-Teaching Staff")
                cat=input("Enter choice (1-3):").strip()
                catMap={"1": "student", "2": "faculty", "3": "staff"}
                fileMap={"student": self.studentAttFile,"faculty": self.facultyAttFile,"staff": self.staffAttFile,}
                entityType=catMap.get(cat)
                if not entityType:
                    print("Invalid selection.")
                    continue
                entityId=input(f"Enter {entityType.capitalize()} ID:").strip()
                if not self.isValidId(entityType, entityId):
                    print("Invalid ID! Person does not exist in system.")
                    continue
                attFile=fileMap[entityType]
                if not os.path.exists(attFile):
                    print("No attendance records logged yet.")
                    continue
                datesPresent=[]
                with open(attFile,"r") as f:
                    for line in f:
                        parts=line.strip().split(",")
                        if parts[0]==entityId:
                            datesPresent.append(parts[1])
                daysCountArray=array("i", [len(datesPresent)])
                print(f"\nATTENDANCE REPORT FOR ID: {entityId} ({entityType.upper()})")
                print(f"Total Days Present: {daysCountArray[0]}")
                if datesPresent:
                    print("Dates Present:")
                    for d in datesPresent:
                        print(f"  - {d}")
                else:
                    print("No attendance records logged for this ID.")
            elif choice=="3":
                print("\nSelect Category for Library Visit:")
                print("1. Student | 2. Faculty | 3. Non-Teaching Staff")
                cat=input("Enter choice (1-3): ").strip()
                catMap={"1": "student", "2": "faculty", "3": "staff"}
                entityType=catMap.get(cat)
                if not entityType:
                    print("Invalid selection.")
                    continue
                entityId=input(f"Enter {entityType.capitalize()} ID:").strip()
                if not self.isValidId(entityType, entityId):
                    print("Invalid ID! Person does not exist in system.")
                    continue
                now=datetime.now()
                currentDate=now.strftime("%Y-%m-%d")
                currentTime=now.strftime("%H:%M:%S")
                print(f"1. Log Entry Time (Current Time: {currentTime})")
                print("2. Log Exit Time")
                subChoice = input("Select Option (1-2): ").strip()
                if subChoice=="1":
                    with open(self.libraryLogFile,"a") as f:
                        f.write(f"{entityId},{entityType},{currentDate},{currentTime},Active\n")
                    print(f"Entry logged successfully for {entityId} at {currentTime} on {currentDate}.")

                elif subChoice=="2":
                    if not os.path.exists(self.libraryLogFile):
                        print("No active entry logs found.")
                        continue
                    with open(self.libraryLogFile,"r") as f:
                        lines=f.readlines()
                    found=False
                    with open(self.libraryLogFile,"w") as f:
                        for line in lines:
                            p=line.strip().split(",")
                            if p[0]==entityId and p[2]==currentDate and p[4]=="Active" and not found:
                                found=True
                                f.write(f"{p[0]},{p[1]},{p[2]},{p[3]},{currentTime}\n")
                                print(f"Exit logged successfully for {entityId} at {currentTime}.")
                            else:
                                f.write(line)
                    if not found:
                        print("No active entry log found for today to exit.")
            elif choice=="4":
                entityId=input("Enter Person ID to view library logs:").strip()
                isValid=(self.isValidId("student", entityId) or self.isValidId("faculty", entityId) or self.isValidId("staff", entityId))
                if not isValid:
                    print("Invalid ID! Person does not exist in system.")
                    continue
                if not os.path.exists(self.libraryLogFile):
                    print("No library logs found.")
                    continue
                print(f"\nLIBRARY ENTRY & EXIT TIMING LOGS FOR ID: {entityId}")
                logsFound=False
                with open(self.libraryLogFile,"r") as f:
                    for line in f:
                        p = line.strip().split(",")
                        if p[0]==entityId:
                            logsFound=True
                            print(f"Date: {p[2]} | Role: {p[1].capitalize()} | Entry Time: {p[3]} | Exit Time: {p[4]}")
                if not logsFound:
                    print("No library timing records found for this ID.")
            elif choice=="5":
                break
def main():
    manager=CollegeManager()
    while True:
        print("COLLEGE MANAGEMENT SYSTEM")
        print("1.Manage Students")
        print("2.Manage Faculty / Teachers")
        print("3.Manage Non-Teaching Staff")
        print("4.Manage Library System")
        print("5.Attendance & Library Entry/Exit Logs")
        print("6.Exit Program")
        choice=input("Enter your choice (1-6):").strip()
        if choice=="1":
            manager.manageStudents()
        elif choice=="2":
            manager.manageFaculty()
        elif choice=="3":
            manager.manageStaff()
        elif choice=="4":
            manager.manageLibrary()
        elif choice=="5":
            manager.manageAttendanceAndLogs()
        elif choice=="6":
            print("\nExiting College Management System. Goodbye!")
            break
        else:
            print("Invalid selection! Please enter a number between 1 and 6.")
if __name__=="__main__":
    main()
