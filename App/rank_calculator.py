import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class Student:
    def __init__(self, name, marks, total_marks):
        self.name = name
        self.marks = marks
        self.percentage = self.calculate_percentage(total_marks)

    def calculate_percentage(self, total_marks):
        return (self.marks / total_marks) * 100

def rank_students(students):
    return sorted(students, key=lambda student: student.percentage, reverse=True)

def add_student():
    name = name_entry.get().strip()
    try:
        marks = float(marks_entry.get().strip())
        if marks < 0 or marks > total_marks:
            raise ValueError(f"Marks must be between 0 and {total_marks}.")
        students.append(Student(name, marks, total_marks))
        name_entry.delete(0, tk.END)
        marks_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Student added successfully!")
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def edit_student():
    ranked_students = rank_students(students)
    if not ranked_students:
        messagebox.showwarning("Edit Student", "No students available to edit.")
        return

    names = [f"{student.name} (Marks: {student.marks})" for student in ranked_students]
    selected_name = simpledialog.askstring("Edit Student", "Select student to edit:\n" + "\n".join(names))

    for student in ranked_students:
        if student.name == selected_name:
            new_name = simpledialog.askstring("Edit Name", "Enter new name:", initialvalue=student.name)
            new_marks = simpledialog.askfloat("Edit Marks", "Enter new marks (0-{}):".format(total_marks),
                                              initialvalue=student.marks)
            if new_marks is not None and (0 <= new_marks <= total_marks):
                student.name = new_name if new_name else student.name
                student.marks = new_marks
                messagebox.showinfo("Success", "Student updated successfully!")
                return
            else:
                messagebox.showerror("Error", "Invalid marks entered.")
            break
    else:
        messagebox.showerror("Error", "Student not found.")

def delete_student():
    ranked_students = rank_students(students)
    if not ranked_students:
        messagebox.showwarning("Delete Student", "No students available to delete.")
        return

    names = [f"{student.name} (Marks: {student.marks})" for student in ranked_students]
    selected_name = simpledialog.askstring("Delete Student", "Select student to delete:\n" + "\n".join(names))

    for student in ranked_students:
        if student.name == selected_name:
            students.remove(student)
            messagebox.showinfo("Success", "Student deleted successfully!")
            return
    messagebox.showerror("Error", "Student not found.")

def display_ranked_students():
    ranked_students = rank_students(students)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Ranked Students:\n")
    for rank, student in enumerate(ranked_students, start=1):
        result_text.insert(tk.END,
                           f"Rank {rank}: {student.name}, Marks: {student.marks}, Percentage: {student.percentage:.2f}%\n")

def generate_pdf():
    ranked_students = rank_students(students)
    if not ranked_students:
        messagebox.showwarning("PDF Generation", "No students available to print.")
        return

    pdf_filename = "students_ranking_report.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    c.drawString(100, height - 100, "Students Ranking Report")
    c.drawString(100, height - 120, "Ranked Students:")

    for rank, student in enumerate(ranked_students, start=1):
        c.drawString(100, height - (140 + rank * 20), f"Rank {rank}: {student.name}, Marks: {student.marks}, Percentage: {student.percentage:.2f}%")

    c.save()
    messagebox.showinfo("Success", f"PDF generated: {pdf_filename}")

# Prompt the teacher to enter total marks
total_marks = simpledialog.askinteger("Total Marks", "Enter the total marks for students (1-100):", minvalue=1,
                                      maxvalue=100)

students = []

# Create the main window
root = tk.Tk()
root.title("Student Ranking System")
root.geometry("600x500")
root.config(bg="#f0f0f0")

# Set the title font to Bold and Heavy
title_label = tk.Label(root, text="Student Ranking System", font=("Arial", 16, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

# Create and place the widgets
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(padx=20, pady=20)

tk.Label(frame, text="Student Name:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5)
name_entry = tk.Entry(frame)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame, text="Marks (0-{}):".format(total_marks), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5)
marks_entry = tk.Entry(frame)
marks_entry.grid(row=1, column=1, padx=10, pady=5)

# Buttons with specified colors
button_style = {
    'fg': 'white',
    'activeforeground': 'white',
    'padx': 10,
    'pady': 5
}

add_button = tk.Button(frame, text="Add Student", command=add_student, bg='blue', **button_style)
add_button.grid(row=2, column=0, columnspan=2, pady=10)

edit_button = tk.Button(frame, text="Edit Student", command=edit_student, bg='yellow', **button_style)
edit_button.grid(row=3, column=0, columnspan=2, pady=5)

delete_button = tk.Button(frame, text="Delete Student", command=delete_student, bg='red', **button_style)
delete_button.grid(row=4, column=0, columnspan=2, pady=5)

display_button = tk.Button(frame, text="Display Ranked Students", command=display_ranked_students, bg='green', **button_style)
display_button.grid(row=5, column=0, columnspan=2, pady=10)

pdf_button = tk.Button(frame, text="Generate PDF", command=generate_pdf, bg='seagreen', **button_style)
pdf_button.grid(row=6, column=0, columnspan=2, pady=10)

# Result text area
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15, bg="#ffffff", font=("Arial", 10))
result_text.pack(padx=20, pady=10)

# Start the application
root.mainloop()
