import csv
from pathlib import Path


def clean_text(value):
    return value.strip().strip('"')


def validate_student_row(row):
    required_columns = ["Name", "Score", "Attendance"]

    for column in required_columns:
        if column not in row:
            return False

    name = clean_text(row["Name"])

    if name == "":
        return False

    try:
        score = float(clean_text(row["Score"]))
        attendance = float(clean_text(row["Attendance"]))
    except ValueError:
        return False

    if score < 0 or score > 100:
        return False

    if attendance < 0 or attendance > 100:
        return False

    return True


def load_students(file_path):
    students = []
    invalid_rows = []

    with open(file_path, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row_number, row in enumerate(reader, start=2):
            if validate_student_row(row):
                student = {
                    "name": clean_text(row["Name"]),
                    "score": float(clean_text(row["Score"])),
                    "attendance": float(clean_text(row["Attendance"]))
                }

                students.append(student)
            else:
                invalid_rows.append(row_number)

    return students, invalid_rows


def analyze_students(students):
    total_score = 0
    pass_count = 0
    fail_count = 0

    highest_student = students[0]
    lowest_student = students[0]

    for student in students:
        score = student["score"]
        total_score += score

        if score >= 50:
            student["result"] = "Pass"
            pass_count += 1
        else:
            student["result"] = "Fail"
            fail_count += 1

        if score > highest_student["score"]:
            highest_student = student

        if score < lowest_student["score"]:
            lowest_student = student

    average_score = total_score / len(students)

    return {
        "average_score": average_score,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "highest_student": highest_student,
        "lowest_student": lowest_student
    }


def display_report(students, invalid_rows, analysis):
    print("Robust CSV Student Analyzer")
    print("---------------------------")

    print()
    print("Valid Student Records")
    print("---------------------")

    for student in students:
        print(
            f"Name: {student['name']}, "
            f"Score: {student['score']:.2f}, "
            f"Attendance: {student['attendance']:.2f}%, "
            f"Result: {student['result']}"
        )

    print()
    print("Summary")
    print("-------")
    print(f"Valid records: {len(students)}")
    print(f"Invalid rows skipped: {invalid_rows}")
    print(f"Average score: {analysis['average_score']:.2f}")
    print(f"Students passed: {analysis['pass_count']}")
    print(f"Students failed: {analysis['fail_count']}")

    highest = analysis["highest_student"]
    lowest = analysis["lowest_student"]

    print(f"Highest score: {highest['name']} ({highest['score']:.2f})")
    print(f"Lowest score: {lowest['name']} ({lowest['score']:.2f})")


def main():
    data_file = Path("data") / "students.csv"

    try:
        students, invalid_rows = load_students(data_file)

        if len(students) == 0:
            print("No valid student records found.")
            return

        analysis = analyze_students(students)
        display_report(students, invalid_rows, analysis)

    except FileNotFoundError:
        print("Error: students.csv was not found in the data folder.")
    except KeyError:
        print("Error: The CSV file does not contain the required columns.")
    except Exception as error:
        print("An unexpected error occurred:")
        print(error)


main()
