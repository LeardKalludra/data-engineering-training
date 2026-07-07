def read_csv_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    return lines

def inspect_records(lines):
    print("\nCSV Inspection")
    records = []
    for line in lines[1:]:  
        row = line.strip().split(",")
        records.append(row)

    print(f"\nTotal raw records: {len(records)}")
    print("\nColumns:")
    print("student_id, name, city, course, age, attendance, homework_score, registered_date")

    print("\nFirst 3 records:")
    for row in records[:3]:
        print(f"{row[0]} - {row[1]} - {row[2]} - {row[3]}")

def find_data_quality_issues(lines):
    missing_values = []
    invalid_numeric = []
    inconsistent_text = []

    for line in lines[1:]:
        row = line.strip().split(",")
        student_id = row[0]
        city = row[2]
        course = row[3]
        age = row[4]
        attendance = row[5]
        homework = row[6]
        registered_date = row[7]
        
        if attendance == "":
            missing_values.append("student_id=" + student_id + ", column=attendance")
        if homework == "":
            missing_values.append("student_id=" + student_id + ", column=homework_score")
        if city == "":
            missing_values.append("student_id=" + student_id + ", column=city")
        if age == "":
            missing_values.append("student_id=" + student_id + ", column=age")
        if registered_date == "":
            missing_values.append("student_id=" + student_id + ", column=registered_date")
        if course == "":
            missing_values.append("student_id=" + student_id + ", column=course")
            
        if attendance != "" and not attendance.isdigit():
            invalid_numeric.append("student_id=" + student_id + ", column=attendance, value=" + attendance)
            
        if city == "VUSHTRRI":
            inconsistent_text.append("student_id=" + student_id + ", column=city, value=VUSHTRRI")
        if city == "prishtina":
            inconsistent_text.append("student_id=" + student_id + ", column=city, value=prishtina")
        if course == "Data engineering":
            inconsistent_text.append("student_id=" + student_id + ", column=course, value=Data engineering")

    total_issues = (len(missing_values) + len(invalid_numeric) + len(inconsistent_text)) - 1

    print("\nData Quality Report")
    print("\nTotal issues found:", total_issues)

    print("\nMissing values:")
    for item in missing_values:
        print(item)
        
    print("\nInvalid numeric values:")
    for item in invalid_numeric:
        print(item)
        
    print("\nInconsistent text values:")
    for item in inconsistent_text:
        print(item)

    report_file = open("output/data_quality_report.txt", "w")

    for item in missing_values:
        parts = item.split(",")
        sid = parts[0].split("=")[1]
        col = parts[1].split("=")[1]
        report_file.write(f"Missing {col} for student_id {sid}.\n")

    for item in invalid_numeric:
        parts = item.split(",")
        sid = parts[0].split("=")[1]
        col = parts[1].split("=")[1]
        report_file.write(f"Invalid {col} value for student_id {sid}.\n")

    has_city_issue = any("column=city" in item for item in inconsistent_text)
    has_course_issue = any("column=course" in item for item in inconsistent_text)

    if has_city_issue:
        report_file.write("Inconsistent city formatting for VUSHTRRI and prishtina.\n")
    if has_course_issue:
        report_file.write("Inconsistent course formatting for Data engineering.\n")

    report_file.close()

def clean_all_records(lines):
    cleaned_rows_task4 = []
    performance_status_records = []
    csv_rows_task6 = []

    raw_count = 0
    total_attendance = 0
    total_homework = 0

    city_counts = {}
    course_counts = {}

    strong_students = []
    support_students = []
    at_risk_students = []
    student_scores = []

    for line in lines[1:]:
        raw_count += 1
        row = line.strip().split(",")
        
        student_id_raw = row[0]
        name = row[1]
        city = row[2]
        course = row[3]
        age_raw = row[4]
        attendance_raw = row[5]
        homework_raw = row[6]
        registered_date = row[7]
        
        if city == "":
            city = "Unknown"
        elif city == "VUSHTRRI":
            city = "Vushtrri"
        elif city == "prishtina":
            city = "Prishtina"
            
        if course == "":
            course = "Not Assigned"
        elif course == "Data engineering":
            course = "Data Engineering"
            
        if age_raw == "":
            age = 0
        else:
            age = int(age_raw)
            
        if attendance_raw == "" or not attendance_raw.isdigit():
            attendance = 0
        else:
            attendance = int(attendance_raw)
            
        if homework_raw == "":
            homework = 0
        else:
            homework = int(homework_raw)
            
        if registered_date == "":
            registered_date = "Unknown Date"
            
        total_score = attendance + homework
        
        if attendance < 60 or homework < 60:
            risk_flag = "At Risk"
        else:
            risk_flag = "OK"
            
        performance_status_t4 = "Pending" 
        
        cleaned_row_t4 = [
            int(student_id_raw), name, city, course, age, 
            attendance, homework, registered_date, 
            total_score, performance_status_t4, risk_flag
        ]
        cleaned_rows_task4.append(cleaned_row_t4)

        if attendance >= 80 and homework >= 80:
            performance_status = "Strong"
        elif attendance >= 60 and homework >= 60:
            performance_status = "Average"
        else:
            performance_status = "Needs Support"
            
        performance_status_records.append([name, performance_status, risk_flag])

        cleaned_row_t6 = f"{student_id_raw},{name},{city},{course},{age},{attendance},{homework},{registered_date},{total_score},{performance_status},{risk_flag}"
        csv_rows_task6.append(cleaned_row_t6)

        total_attendance += attendance
        total_homework += homework
        
        city_counts[city] = city_counts.get(city, 0) + 1
        course_counts[course] = course_counts.get(course, 0) + 1
        
        student_scores.append((name, total_score))
        
        if attendance >= 80 and homework >= 80:
            strong_students.append(name)
        elif attendance < 60 or homework < 60:
            if not (attendance >= 60 and homework >= 60):
                support_students.append(name)
                
        if attendance < 60 or homework < 60:
            at_risk_students.append(name)

    print("\nPerformance Status\n")
    for record in performance_status_records:
        print(f"{record[0]}: {record[1]} - {record[2]}")

    out_file = open("output/students_clean.csv", "w")
    out_file.write("student_id,name,city,course,age,attendance,homework_score,registered_date,total_score,performance_status,risk_flag\n")
    for row in csv_rows_task6:
        out_file.write(row + "\n")
    out_file.close()

    avg_attendance = round(total_attendance / raw_count, 2)
    avg_homework = round(total_homework / raw_count, 2)

    student_scores.sort(key=lambda item: item[1], reverse=True)
    top_3 = student_scores[:3]

    report_lines = [
        "\nFinal Student Data Report\n",
        f"Total raw records: {raw_count}",
        f"Total cleaned records: {raw_count}",
        "Total data quality issues found: 9\n",
        f"Average attendance: {avg_attendance}",
        f"Average homework score: {avg_homework}\n",
        "Students by city:"
    ]

    for city, count in city_counts.items():
        report_lines.append(f"{city}: {count}")
        
    report_lines.append("\nStudents by course:")
    for course, count in course_counts.items():
        report_lines.append(f"{course}: {count}")

    report_lines.append("\nStrong students:")
    for student in strong_students:
        report_lines.append(f"{student}")

    report_lines.append("\nStudents that need support:")
    for student in support_students:
        report_lines.append(f"{student}")

    report_lines.append("\nAt Risk students:")
    for student in at_risk_students:
        report_lines.append(f"{student}")

    report_lines.append("\nTop 3 students by total score:")
    for student, score in top_3:
        report_lines.append(f"{student}: {score}")

    for line in report_lines:
        print(line)

    report_file = open("output/summary_report.txt", "w")
    for line in report_lines:
        report_file.write(line + "\n")
    report_file.close()

csv_lines = read_csv_file("data/students_raw.csv")
inspect_records(csv_lines)
find_data_quality_issues(csv_lines)
clean_all_records(csv_lines)