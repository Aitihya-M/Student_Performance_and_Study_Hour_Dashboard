import csv
import json
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# PROJECT: STUDENT PERFORMANCE AND STUDY-HOURS DASHBOARD
CSV_FILE = "student_data.csv"
JSON_FILE = "student_data.json"


# 1. SCORE AND GRADE FUNCTIONS (CO1)
def calculate_percentage(score, total=100):
    return (score / total) * 100


def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    return "F"


# 2. STUDENT RECORD CLASS (CO3)
class StudentRecord:
    def __init__(self, student_id, course, study_hours, score):
        self.student_id = int(student_id)
        self.course = str(course)
        self.study_hours = float(study_hours)
        self.score = float(score)

    def get_grade(self):
        return calculate_grade(calculate_percentage(self.score))

    def to_dict(self):
        return {
            "Student_ID": self.student_id,
            "Course": self.course,
            "Study_Hours": self.study_hours,
            "Score": self.score,
        }

    def __repr__(self):
        return (
            f"StudentRecord(ID={self.student_id}, "
            f"Course='{self.course}', Hours={self.study_hours}, "
            f"Score={self.score})"
        )


# 3. STUDENT DATABASE CLASS (CO2, CO3)
class StudentDatabase:
    def __init__(self):
        self.records = []

    def __len__(self):
        return len(self.records)

    def __iter__(self):
        return iter(self.records)

    def __getitem__(self, index):
        return self.records[index]

    def find(self, student_id):
        for student in self.records:
            if student.student_id == int(student_id):
                return student
        return None

    def add(self, student):
        if self.find(student.student_id):
            raise ValueError("Duplicate Student ID.")
        self.records.append(student)

    def insert(self, position, student):
        if self.find(student.student_id):
            raise ValueError("Duplicate Student ID.")
        if position < 0 or position > len(self.records):
            raise IndexError("Invalid insertion position.")
        self.records.insert(position, student)

    def delete(self, student_id):
        student = self.find(student_id)
        if student is None:
            raise ValueError("Student ID not found.")
        self.records.remove(student)

    def modify(self, student_id, course=None, study_hours=None, score=None):
        student = self.find(student_id)
        if student is None:
            raise ValueError("Student ID not found.")
        if course is not None:
            student.course = course
        if study_hours is not None:
            student.study_hours = float(study_hours)
        if score is not None:
            student.score = float(score)


database = StudentDatabase()


# 4. FILE HANDLING: CSV AND JSON (CO2, CO5)
def save_data():
    fields = ["Student_ID", "Course", "Study_Hours", "Score"]
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for student in database:
            writer.writerow(student.to_dict())

    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump([student.to_dict() for student in database], file, indent=4)

    print("Data saved successfully in CSV and JSON formats.")


def load_data():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            required_columns = {"Student_ID", "Course", "Study_Hours", "Score"}
            if not required_columns.issubset(df.columns):
                raise ValueError("CSV file has missing columns.")
            loaded_records = [
                StudentRecord(row["Student_ID"], row["Course"],
                              row["Study_Hours"], row["Score"])
                for _, row in df.iterrows()
            ]
            ids = [record.student_id for record in loaded_records]
            if len(ids) != len(set(ids)):
                raise ValueError("CSV file contains duplicate Student IDs.")
            database.records = loaded_records
            print("Student records loaded from CSV.")
        except (ValueError, KeyError, TypeError, pd.errors.ParserError) as error:
            print("CSV loading failed:", error)
            print("Please check the CSV file.")
    elif os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, list):
                raise ValueError("JSON root must be a list.")
            loaded_records = [
                StudentRecord(row["Student_ID"], row["Course"],
                              row["Study_Hours"], row["Score"])
                for row in data
            ]
            ids = [record.student_id for record in loaded_records]
            if len(ids) != len(set(ids)):
                raise ValueError("JSON file contains duplicate Student IDs.")
            database.records = loaded_records
            print("Student records loaded from JSON.")
        except (ValueError, KeyError, TypeError) as error:
            print("JSON loading failed:", error)
    else:
        print("No existing dataset found.")
        print("You can start by entering student records.")


# 5. INPUT VALIDATION
def get_integer(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Invalid input. Enter an integer.")


def get_positive_id():
    while True:
        student_id = get_integer("Enter Student ID: ")
        if student_id > 0:
            return student_id
        print("Student ID must be positive.")


def get_course():
    while True:
        course = input("Enter Course Name: ").strip()
        if course:
            return course
        print("Course name cannot be empty.")


def get_hours():
    while True:
        try:
            hours = float(input("Enter Study Hours: "))
            if np.isfinite(hours) and hours >= 0:
                return hours
            print("Study hours must be a non-negative number.")
        except ValueError:
            print("Enter a valid number.")


def get_score():
    while True:
        try:
            score = float(input("Enter Assessment Score (0-100): "))
            if np.isfinite(score) and 0 <= score <= 100:
                return score
            print("Score must be between 0 and 100.")
        except ValueError:
            print("Enter a valid number.")


def get_record_count():
    while True:
        n = get_integer("How many records do you want to process? ")
        if n > 0:
            return n
        print("Enter a number greater than zero.")


def get_unique_id():
    while True:
        student_id = get_positive_id()
        if database.find(student_id) is None:
            return student_id
        print("This ID already exists. Try another ID.")


def create_student():
    return StudentRecord(get_unique_id(), get_course(), get_hours(), get_score())


# 6. ADD MULTIPLE RECORDS
def add_student():
    print("\n--- ADD STUDENT RECORDS ---")
    n = get_record_count()
    for i in range(n):
        print("\nEntering Student", i + 1)
        database.add(create_student())
    save_data()
    print(n, "records added successfully.")


# 7. INSERT MULTIPLE RECORDS
def insert_student():
    print("\n--- INSERT STUDENT RECORDS ---")
    n = get_record_count()
    print("Current records:", len(database))
    while True:
        position = get_integer("Enter starting position (starting from 1): ")
        if 1 <= position <= len(database) + 1:
            break
        print("Invalid position.")
    for i in range(n):
        print("\nEntering Student", i + 1)
        database.insert(position - 1 + i, create_student())
    save_data()
    print(n, "records inserted successfully.")


# 8. DELETE MULTIPLE RECORDS
def delete_student():
    print("\n--- DELETE STUDENT RECORDS ---")
    n = get_record_count()
    count = 0
    for i in range(n):
        print("\nDeleting Student", i + 1)
        student_id = get_positive_id()
        try:
            database.delete(student_id)
            count += 1
            print("Record deleted.")
        except ValueError as error:
            print(error)
    if count:
        save_data()
    print(count, "records deleted successfully.")


# 9. MODIFY MULTIPLE RECORDS
def modify_student():
    print("\n--- MODIFY STUDENT RECORDS ---")
    n = get_record_count()
    count = 0
    for i in range(n):
        print("\nModifying Student", i + 1)
        student_id = get_positive_id()
        student = database.find(student_id)
        if student is None:
            print("Student not found. Skipping.")
            continue

        print("\nCurrent Details:", student)
        print("Press ENTER to retain an existing value.")
        course = input(f"New Course [{student.course}]: ").strip() or None

        while True:
            value = input(f"New Study Hours [{student.study_hours}]: ").strip()
            if value == "":
                hours = None
                break
            try:
                hours = float(value)
                if np.isfinite(hours) and hours >= 0:
                    break
                print("Enter a non-negative number.")
            except ValueError:
                print("Enter a valid number.")

        while True:
            value = input(f"New Score [{student.score}]: ").strip()
            if value == "":
                score = None
                break
            try:
                score = float(value)
                if np.isfinite(score) and 0 <= score <= 100:
                    break
                print("Score must be between 0 and 100.")
            except ValueError:
                print("Enter a valid number.")

        database.modify(student_id, course, hours, score)
        count += 1
        print("Record modified successfully.")

    if count:
        save_data()
    print(count, "records modified successfully.")


# 10. DISPLAY STUDENT RECORDS
def display_students():
    print("\n--- STUDENT RECORDS ---")
    if len(database) == 0:
        print("No records available.")
        return
    print("-" * 70)
    print(f"{'ID':<12}{'Course':<15}{'Hours':<12}{'Score':<10}Grade")
    print("-" * 70)
    for student in database:
        print(f"{student.student_id:<12}{student.course:<15}"
              f"{student.study_hours:<12}{student.score:<10}{student.get_grade()}")
    print("-" * 70)
    print("Total records:", len(database))


# 11. NUMPY ANALYSIS
def performance_analysis():
    print("\n--- NUMPY PERFORMANCE ANALYSIS ---")
    if len(database) == 0:
        print("No data available.")
        return
    scores = np.array([s.score for s in database])
    hours = np.array([s.study_hours for s in database])
    print("Total Students:", len(database))
    print("Average Score:", round(np.mean(scores), 2))
    print("Median Score:", round(np.median(scores), 2))
    print("Average Study Hours:", round(np.mean(hours), 2))
    print("Score Standard Deviation:", round(np.std(scores), 2))
    print("Highest Score:", np.max(scores))
    print("Lowest Score:", np.min(scores))


# 12. PANDAS COURSE-WISE ANALYSIS
def course_analysis():
    print("\n--- COURSE-WISE ANALYSIS ---")
    if len(database) == 0:
        print("No data available.")
        return
    df = pd.DataFrame([s.to_dict() for s in database])
    result = df.groupby("Course").agg(
        Average_Score=("Score", "mean"),
        Average_Study_Hours=("Study_Hours", "mean"),
        Maximum_Score=("Score", "max"),
        Minimum_Score=("Score", "min"),
        Student_Count=("Student_ID", "count"),
    )
    print(result.round(2))


# 13. STUDENT GRADE ANALYSIS
def display_grades():
    print("\n--- STUDENT GRADES ---")
    if len(database) == 0:
        print("No records available.")
        return
    for student in database:
        print("Student ID:", student.student_id,
              "| Score:", student.score, "| Grade:", student.get_grade())


# 14. MATPLOTLIB VISUALIZATION
def display_graphs():
    print("\n--- GRAPHICAL ANALYSIS ---")
    if len(database) == 0:
        print("No data available for graphs.")
        return
    df = pd.DataFrame([s.to_dict() for s in database])

    plt.figure(figsize=(9, 5))
    plt.scatter(df["Study_Hours"], df["Score"], alpha=0.8)
    plt.xlabel("Study Hours per Student")
    plt.ylabel("Assessment Score (0-100)")
    plt.title("Relationship Between Study Hours and Assessment Scores")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(9, 5))
    plt.hist(df["Score"], bins=10, edgecolor="black")
    plt.xlabel("Assessment Score (0-100)")
    plt.ylabel("Number of Students")
    plt.title("Distribution of Student Assessment Scores")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.show()


# 15. OUTLIER AND CORRELATION ANALYSIS
def outlier_analysis():
    print("\n--- OUTLIER AND CORRELATION ANALYSIS ---")
    if len(database) < 3:
        print("At least 3 records are recommended for analysis.")
        return

    df = pd.DataFrame([s.to_dict() for s in database])
    scores = df["Score"]
    q1, q3 = scores.quantile(0.25), scores.quantile(0.75)
    iqr = q3 - q1
    lower_limit = q1 - 1.5 * iqr
    upper_limit = q3 + 1.5 * iqr

    iqr_outliers = df[(scores < lower_limit) | (scores > upper_limit)]
    print("\nIQR OUTLIER DETECTION")
    print("Q1:", q1, "\nQ3:", q3, "\nIQR:", iqr)
    print("Lower Limit:", lower_limit, "\nUpper Limit:", upper_limit)
    print("Number of IQR outliers:", len(iqr_outliers))
    print(iqr_outliers)

    median_score = scores.median()
    mad = np.median(np.abs(scores - median_score))
    print("\nMAD OUTLIER DETECTION")
    if mad == 0:
        print("MAD is zero. Alternative detection is inconclusive.")
    else:
        modified_z = 0.6745 * (scores - median_score) / mad
        mad_outliers = df[np.abs(modified_z) > 3.5]
        print("Number of MAD outliers:", len(mad_outliers))
        print(mad_outliers)

    correlation_before = df["Study_Hours"].corr(df["Score"])
    clean_data = df[(scores >= lower_limit) & (scores <= upper_limit)]
    print("\nCORRELATION ANALYSIS")
    print("Correlation before outlier removal:", correlation_before)
    if len(clean_data) >= 2:
        correlation_after = clean_data["Study_Hours"].corr(clean_data["Score"])
        print("Correlation after IQR removal:", correlation_after)
    else:
        print("Not enough records after outlier removal.")
    print("\nEVALUATION: Correlation describes association, not causation.")


# 16. REPRODUCIBLE DEMO DATASET
def generate_demo_data():
    if len(database) > 0:
        print("Database is not empty.")
        print("Demo data will not overwrite existing records.")
        return
    demo_records = [
        (101, "ECE", 5, 85), (102, "ECE", 7, 92),
        (103, "CSE", 3, 65), (104, "CSE", 6, 80),
        (105, "EEE", 4, 70), (106, "EEE", 8, 95),
        (107, "ECE", 2, 55), (108, "CSE", 5, 75),
        (109, "EEE", 6, 82), (110, "ECE", 10, 100),
        (111, "CSE", 1, 40), (112, "EEE", 3, 60),
        (113, "ECE", 4, 78), (114, "CSE", 8, 90),
        (115, "EEE", 12, 45),
    ]
    for record in demo_records:
        database.add(StudentRecord(*record))
    save_data()
    print("Synthetic demonstration dataset generated.")
    print("These records are not real student observations.")


# 17. MAIN MENU
def main():
    load_data()
    while True:
        print("\n" + "=" * 48)
        print("       STUDENT PERFORMANCE DASHBOARD")
        print("=" * 48)
        print("1.  Add Student Records")
        print("2.  Insert Student Records")
        print("3.  Delete Student Records")
        print("4.  Modify Student Records")
        print("5.  Display All Student Records")
        print("6.  Display Student Grades")
        print("7.  NumPy Performance Analysis")
        print("8.  Pandas Course-wise Analysis")
        print("9.  Display Graphs")
        print("10. Outlier and Correlation Analysis")
        print("11. Save Data")
        print("12. Generate Demo Dataset")
        print("13. Exit")
        print("=" * 48)

        choice = input("Enter your choice (1-13): ").strip()
        if choice == "1":
            add_student()
        elif choice == "2":
            insert_student()
        elif choice == "3":
            delete_student()
        elif choice == "4":
            modify_student()
        elif choice == "5":
            display_students()
        elif choice == "6":
            display_grades()
        elif choice == "7":
            performance_analysis()
        elif choice == "8":
            course_analysis()
        elif choice == "9":
            display_graphs()
        elif choice == "10":
            outlier_analysis()
        elif choice == "11":
            save_data()
        elif choice == "12":
            generate_demo_data()
        elif choice == "13":
            save_data()
            print("Thank you for using the dashboard!")
            break
        else:
            print("Invalid choice. Select between 1 and 13.")


if __name__ == "__main__":
    main()
