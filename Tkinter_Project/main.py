from tkinter import Tk, Frame, Button, Label, Entry, Toplevel, messagebox

# Backend Classes
class Student:
    def __init__(self, student_id, name, level, password, gpa=0.0, group=None):
        self.student_id = student_id
        self.name = name
        self.level = level
        self.password = password
        self.gpa = gpa
        self.group = group
        self.courses = []

class Course:
    def __init__(self, course_code, course_name):
        self.course_code = course_code
        self.course_name = course_name

class Control:
    def __init__(self):
        self.students = {}
        self.courses = {}

    def authenticate_student(self, student_id, password):
        student = self.students.get(student_id)
        return student and student.password == password

    def add_student(self, student_id, name, level, password, gpa=0.0, group=None):
        if student_id in self.students:
            raise ValueError("Student ID already exists")
        self.students[student_id] = Student(student_id, name, level, password, gpa, group)

    def remove_student(self, student_id):
        if student_id not in self.students:
            raise ValueError("Student not found")
        del self.students[student_id]

    def update_student_info(self, student_id, **kwargs):
        if student_id not in self.students:
            raise ValueError("Student not found")
        student = self.students[student_id]
        for key, value in kwargs.items():
            setattr(student, key, value)
            
    def change_student_password(self, student_id, new_password):
        if student_id not in self.students:
            raise ValueError("Student not found")
        self.students[student_id].password = new_password
        
    def get_student_info(self, student_id):
        if student_id not in self.students:
            raise ValueError("Student not found")
        student = self.students[student_id]
        info = f"ID: {student.student_id}, Name: {student.name}, Level: {student.level}, GPA: {student.gpa}, Group: {student.group}, Courses: {', '.join(student.courses)}"
        return info
    
    def register_student_for_course(self, student_id, course_code):
        if student_id not in self.students:
            raise ValueError("Student not found")
        if course_code not in self.courses:
            raise ValueError("Course does not exist")
        if course_code in self.students[student_id].courses:
            raise ValueError("Already registered for this course")
        self.students[student_id].courses.append(course_code)
    
    def add_course(self, course_code, course_name):
        if course_code in self.courses:
            raise ValueError("Course code already exists")
        self.courses[course_code] = Course(course_code, course_name)
    
    def drop_student_course(self, student_id, course_code):
        if student_id not in self.students:
            raise ValueError("Student not found")
        if course_code not in self.courses:
            raise ValueError("Course does not exist")
        if course_code not in self.students[student_id].courses:
            raise ValueError("Student not registered for this course")
        self.students[student_id].courses.remove(course_code)



# GUI Application
class StudentManagementSystemGUI:
    def __init__(self, master):
        self.master = master
        self.control = Control()
        master.title("Student Management System")

        self.main_frame = Frame(master)
        self.main_frame.pack(padx=10, pady=10)

        Label(self.main_frame, text="Welcome to the Student Management System", font=("Arial", 14)).pack(pady=10)

        Button(self.main_frame, text="Student Login", command=self.open_student_login).pack(pady=5)
        Button(self.main_frame, text="Control Panel", command=self.open_control_panel).pack(pady=5)

    def open_student_login(self):
        StudentLogin(self.master, self.control)

    def open_control_panel(self):
        ControlPanel(self.master, self.control)
        



class StudentLogin:
    def __init__(self, parent, control):
        self.control = control
        self.top = Toplevel(parent)
        self.top.title("Student Login")

        Label(self.top, text="Student ID").pack(pady=(10, 0))
        self.student_id_entry = Entry(self.top)
        self.student_id_entry.pack(pady=(0, 10))

        Label(self.top, text="Password").pack(pady=(10, 0))
        self.password_entry = Entry(self.top, show="*")
        self.password_entry.pack(pady=(0, 10))

        Button(self.top, text="Login", command=self.authenticate_student).pack(pady=10)

    def authenticate_student(self):
        student_id = self.student_id_entry.get()
        password = self.password_entry.get()
        if self.control.authenticate_student(student_id, password):
            messagebox.showinfo("Login Successful", "You are now logged in.")
            self.top.destroy()
            StudentDashboard(student_id=student_id, control=self.control)
        else:
            messagebox.showerror("Login Failed", "Invalid student ID or password.")

class ControlPanel:
    def __init__(self, parent, control):
        self.control = control
        self.top = Toplevel(parent)
        self.top.title("Control Panel")

        Button(self.top, text="Add Student", command=self.add_student).pack(fill='x', padx=50, pady=5)
        Button(self.top, text="Remove Student", command=self.remove_student).pack(fill='x', padx=50, pady=5)
        Button(self.top, text="Edit Student Information", command=self.edit_student_info).pack(fill='x', padx=50, pady=5)
        Button(self.top, text="Add Course", command=self.add_course_form).pack(fill='x', padx=50, pady=5)
        Button(self.top, text="Show Student Info", command=self.show_student_info_form).pack(fill='x', padx=50, pady=5)

    def add_student(self):
        AddStudentForm(self.control)

    def remove_student(self):
        RemoveStudentForm(self.control)

    def edit_student_info(self):
        EditStudentInfoForm(self.control)
        
    def add_course_form(self):
        AddCourseForm(self.control)
    
    def show_student_info_form(self):
        ShowStudentInfoForm(self.control)

class AddStudentForm:
    def __init__(self, control):
        self.top = Toplevel()
        self.control = control
        self.top.title("Add New Student")

        Label(self.top, text="Student ID").pack(pady=(10, 0))
        self.student_id_entry = Entry(self.top)
        self.student_id_entry.pack(pady=(0, 10))

        Label(self.top, text="Name").pack(pady=(10, 0))
        self.name_entry = Entry(self.top)
        self.name_entry.pack(pady=(0, 10))

        Label(self.top, text="Level").pack(pady=(10, 0))
        self.level_entry = Entry(self.top)
        self.level_entry.pack(pady=(0, 10))

        Label(self.top, text="Password").pack(pady=(10, 0))
        self.password_entry = Entry(self.top)
        self.password_entry.pack(pady=(0, 10))

        Label(self.top, text="GPA").pack(pady=(10, 0))
        self.gpa_entry = Entry(self.top)
        self.gpa_entry.pack(pady=(0, 10))

        Label(self.top, text="Group").pack(pady=(10, 0))
        self.group_entry = Entry(self.top)
        self.group_entry.pack(pady=(0, 10))

        Button(self.top, text="Add Student", command=self.add_student).pack(pady=10)

    def add_student(self):
        # Collect and validate form data
        student_id = self.student_id_entry.get()
        name = self.name_entry.get()
        level = self.level_entry.get()
        password = self.password_entry.get()
        gpa = self.gpa_entry.get()
        group = self.group_entry.get()

        if not (student_id and name and level and password and gpa and group):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            gpa = float(gpa)  # Validate GPA is a number
        except ValueError:
            messagebox.showerror("Error", "GPA must be a valid number.")
            return

        # Attempt to add student
        try:
            self.control.add_student(student_id, name, level, password, gpa, group)
            messagebox.showinfo("Success", "Student added successfully.")
            self.top.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

class AddCourseForm:
    def __init__(self, control):
        self.top = Toplevel()
        self.control = control
        self.top.title("Add New Course")

        Label(self.top, text="Course Code").pack(pady=(10, 0))
        self.course_code_entry = Entry(self.top)
        self.course_code_entry.pack(pady=(0, 10))

        Label(self.top, text="Course Name").pack(pady=(10, 0))
        self.course_name_entry = Entry(self.top)
        self.course_name_entry.pack(pady=(0, 10))

        Button(self.top, text="Add Course", command=self.add_course).pack(pady=10)

    def add_course(self):
        course_code = self.course_code_entry.get()
        course_name = self.course_name_entry.get()

        if not (course_code and course_name):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            self.control.add_course(course_code, course_name)
            messagebox.showinfo("Success", "Course added successfully.")
            self.top.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    

class ShowStudentInfoForm:
    def __init__(self, control):
        self.top = Toplevel()
        self.control = control
        self.top.title("Show Student Information")

        Label(self.top, text="Student ID").pack(pady=(10, 0))
        self.student_id_entry = Entry(self.top)
        self.student_id_entry.pack(pady=(0, 10))

        Button(self.top, text="Show Info", command=self.show_info).pack(pady=10)

    def show_info(self):
        student_id = self.student_id_entry.get()
        try:
            info = self.control.get_student_info(student_id)
            messagebox.showinfo("Student Information", info)
            self.top.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

class StudentDashboard:
    def __init__(self, control, student_id):
        self.control = control
        self.student_id = student_id
        self.student = self.control.students[student_id]
        
        self.dashboard = Toplevel()
        self.dashboard.title(f"{self.student.name}'s Dashboard")
        
        Label(self.dashboard, text=f"Welcome, {self.student.name}", font=("Arial", 16)).pack(pady=10)

        # Button to view registered courses
        Button(self.dashboard, text="View Registered Courses", command=self.view_registered_courses).pack(pady=5)

        # Button to view GPA
        Button(self.dashboard, text="View GPA", command=self.view_gpa).pack(pady=5)

        # Button to change password (assuming implementation exists)
        Button(self.dashboard, text="Change Password", command=self.change_password).pack(pady=5)

        # Buttons for course registration and dropping (assuming implementations exist)
        Button(self.dashboard, text="Register for New Course", command=self.register_for_course).pack(pady=5)
        Button(self.dashboard, text="Drop a Course", command=self.drop_course).pack(pady=5)

    def view_registered_courses(self):
        registered_courses = "\n".join([f"{code}: {self.control.courses[code].course_name}" for code in self.student.courses])
        messagebox.showinfo("Registered Courses", registered_courses if registered_courses else "No courses registered.")

    def view_gpa(self):
        messagebox.showinfo("GPA", f"Your current GPA is: {self.student.gpa}")

    def change_password(self):
        ChangePasswordForm(self.control, self.student_id)
        
    
    def register_for_course(self):
        RegisterForCourseForm(self.control, self.student_id)

    def drop_course(self):
        DropCourseForm(self.control, self.student_id)
        
class ChangePasswordForm:
    def __init__(self, control, student_id):
        self.control = control
        self.student_id = student_id
        
        self.form = Toplevel()
        self.form.title("Change Password")
        
        Label(self.form, text="New Password:").pack(pady=5)
        self.new_password_entry = Entry(self.form, show="*")
        self.new_password_entry.pack(pady=5)
        
        Button(self.form, text="Change Password", command=self.change_password).pack(pady=10)

    def change_password(self):
        new_password = self.new_password_entry.get()
        if not new_password:
            messagebox.showerror("Error", "Password cannot be empty.")
            return
        try:
            self.control.change_student_password(self.student_id, new_password)
            messagebox.showinfo("Success", "Password changed successfully.")
            self.form.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))


        
class RegisterForCourseForm:
    def __init__(self, control, student_id):
        self.control = control
        self.student_id = student_id
        
        self.form = Toplevel()
        self.form.title("Register for New Course")
        
        Label(self.form, text="Course Code:").pack(pady=5)
        self.course_code_entry = Entry(self.form)
        self.course_code_entry.pack(pady=5)
        
        Button(self.form, text="Register", command=self.register_course).pack(pady=10)

    def register_course(self):
        course_code = self.course_code_entry.get()
        if course_code in self.control.courses:
            self.control.students[self.student_id].courses.append(course_code)
            messagebox.showinfo("Success", "Course registered successfully.")
            self.form.destroy()
        else:
            messagebox.showerror("Error", "Course does not exist.")
            
class DropCourseForm:
    def __init__(self, control, student_id):
        self.control = control
        self.student_id = student_id
        
        self.form = Toplevel()
        self.form.title("Drop a Course")
        
        Label(self.form, text="Course Code:").pack(pady=5)
        self.course_code_entry = Entry(self.form)
        self.course_code_entry.pack(pady=5)
        
        Button(self.form, text="Drop Course", command=self.drop_course).pack(pady=10)

    def drop_course(self):
        course_code = self.course_code_entry.get()
        try:
            self.control.drop_student_course(self.student_id, course_code)
            messagebox.showinfo("Success", "Course dropped successfully.")
            self.form.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))



class RemoveStudentForm:
    def __init__(self, control):
        self.top = Toplevel()
        self.control = control
        self.top.title("Remove Student")

        Label(self.top, text="Student ID").pack(pady=(10, 0))
        self.student_id_entry = Entry(self.top)
        self.student_id_entry.pack(pady=(0, 10))

        Button(self.top, text="Remove Student", command=self.remove_student).pack(pady=10)

    def remove_student(self):
        student_id = self.student_id_entry.get()
        try:
            self.control.remove_student(student_id)
            messagebox.showinfo("Success", "Student removed successfully.")
            self.top.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

class EditStudentInfoForm:
    def __init__(self, control):
        self.top = Toplevel()
        self.control = control
        self.top.title("Edit Student Information")

        Label(self.top, text="Student ID").pack(pady=(10, 0))
        self.student_id_entry = Entry(self.top)
        self.student_id_entry.pack(pady=(0, 10))

        Label(self.top, text="Name").pack(pady=(10, 0))
        self.name_entry = Entry(self.top)
        self.name_entry.pack(pady=(0, 10))

        Label(self.top, text="Level").pack(pady=(10, 0))
        self.level_entry = Entry(self.top)
        self.level_entry.pack(pady=(0, 10))

        Label(self.top, text="GPA").pack(pady=(10, 0))
        self.gpa_entry = Entry(self.top)
        self.gpa_entry.pack(pady=(0, 10))

        Button(self.top, text="Update Information", command=self.edit_info).pack(pady=10)

    def edit_info(self):
        student_id = self.student_id_entry.get()
        try:
            self.control.update_student_info(student_id, 
                                            name=self.name_entry.get(), 
                                            level=self.level_entry.get(), 
                                            gpa=float(self.gpa_entry.get()) if self.gpa_entry.get() else 0.0)
            messagebox.showinfo("Success", "Student information updated successfully.")
            self.top.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))


def main():
    root = Tk()
    app = StudentManagementSystemGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()