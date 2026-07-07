students = [
    {
        "student_id": 1,
        "name": "Arta",
        "city": "Vushtrri",
        "course": "Python",
        "age": 17,

        "attendance": 90,
        "homework_score": 85
    },
    {
        "student_id": 2,
        "name": "Blend",
        "city": "Prishtina",
        "course": "React",
        "age": 18,
        "attendance": 60,
        "homework_score": 70
    },
    {
        "student_id": 3,
        "name": "Dion",
        "city": "Vushtrri",
        "course": "Python",
        "age": 16,
        "attendance": 75,
        "homework_score": 95
    },
    {
        "student_id": 4,
        "name": "Elira",
        "city": "Mitrovica",
        "course": "React",
        "age": 17,
        "attendance": 80,
        "homework_score": 60
    },
    {
        "student_id": 5,
        "name": "Faton",
        "city": "Vushtrri",
        "course": "Data Engineering",
        "age": 19,
        "attendance": 100,
        "homework_score": 90
    },
    {
        "student_id": 6,
        "name": "Gresa",
        "city": "Prishtina",
        "course": "Python",
        "age": 18,
        "attendance": 55,
        "homework_score": 88
    }
]

print(f"Total Students: {len(students)}")   


def studentsNames():
    print("\nStudent Names:")
    for student in students:
        print(student["name"])


def studentsDetail():
    print("\nStudent Details:")
    for student in students:
        print(f"{student["name"]} is from {student["city"]} and is learning {student["course"]}.")



def studentsFromVushtrri():
    print("\nStudents from Vushtrri:")
    for student in students:
        if student["city"] == "Vushtrri":
            print(f"{student["name"]}")

def studentsLowAttendance():
    print("\nStudents with low attendance:")
    for student in students:
        if student["attendance"] < 70:
            print(f"{student["name"]}")

def studentsHomeworkScore():
    print("\nStudents with homework score above 85:")
    for student in students:
        if student["homework_score"] > 85:
            print(f"{student["name"]}")

def strongStudents():
    print("\nStrong Students:")
    for student in students:
        if student["attendance"] >= 90 :
            print(f"{student["name"]}")


def avarage():
    total_attendance = 0
    total_score = 0
    for student in students:
        total_attendance += student["attendance"]
        total_score += student["homework_score"]
        
    averageAttendance = total_attendance / len(students)
    averageHomework = total_score / len(students)
    print(f"\nAverage attendance: {averageAttendance}")
    print(f"Average homework score: {averageHomework}")

  
def studentsBycity():
    city_counts = {}
    for student in students:
        city = student["city"]
        if city in city_counts:
            city_counts[city] += 1
        else:
            city_counts[city] = 1
    print("\nStudents by city:")
    for city, count in city_counts.items():
        print(f"{city}: {count}")



def studentsBycourse():
    course_counts = {}
    for student in students:
        course = student["course"]
        if course in course_counts:
            course_counts[course] += 1
        else:
            course_counts[course] = 1
    print("\nStudents by course:")
    for course, count in course_counts.items():
        print(f"{course}: {count}")

def studentsNeedSupport():
    print("\nStudents that need support")
    for student in students:
        if student["attendance"] < 60 :
            print(f"{student["name"]}")

def performaceStatus():
    print("\nPerformance status:")
    for student in students:
        if student["attendance"] >= 80 and student["homework_score"] >= 80:
            print(f"{student["name"]}: Strong")
        elif student["attendance"] >= 60 and student["homework_score"] >= 60:
            print(f"{student["name"]}: Avarage")
        else:
            print(f"{student["name"]}: Needs Support")

def cleanReportRecords():
    print("\nClean report records:")
    for student in students:
        if student["attendance"] >= 80 and student["homework_score"] >= 80:
            print(f"{student["student_id"]} - {student["name"]} - {student["course"]} - Strong")
        elif student["attendance"] >= 60 and student["homework_score"] >= 60:
            print(f"{student["student_id"]} - {student["name"]} - {student["course"]} - Avarage")
        else:
            print(f"{student["student_id"]} - { student["name"]} - {student["course"]} - Needs Support")

studentsNames()
studentsDetail()
studentsFromVushtrri()
studentsLowAttendance()
studentsHomeworkScore()
avarage()
studentsBycity()
studentsBycourse()
performaceStatus()
cleanReportRecords()