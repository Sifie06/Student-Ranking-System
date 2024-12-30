class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks
        self.percentage = self.calculate_percentage()

    def calculate_percentage(self):
        return (self.marks / 100) * 100  # Assuming total marks are out of 100


def rank_students(students):
    # Sort students based on percentage in descending order
    return sorted(students, key=lambda student: student.percentage, reverse=True)


def main():
    students = []
    num_students = int(input("Enter the number of students: "))

    for _ in range(num_students):
        name = input("Enter student's name: ")
        marks = float(input(f"Enter marks for {name}: "))
        students.append(Student(name, marks))

    ranked_students = rank_students(students)

    print("\nRanked Students:")
    for rank, student in enumerate(ranked_students, start=1):
        print(f"Rank {rank}: {student.name}, Marks: {student.marks}, Percentage: {student.percentage:.2f}%")


if __name__ == "__main__":
    main()
