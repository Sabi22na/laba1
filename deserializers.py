import json
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List
from univers import Student, Course, Group, Enrollment

def load_students_from_json(filename: str) -> List[Student]:
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    students = []
    for item in data:
        student = Student(
            name=item["first_name"],
            surname=item["last_name"],
            birth_date=item["birth_date"],
            student_id=item["student_id"]
        )

        # Группы
        for group_name in item.get("groups", []):
            group = Group(group_name)
            student.groups.append(group)
            group.add_student(student)

        # Записи на курсы
        for en_data in item.get("enrollments", []):
            course = Course(en_data["course_code"], "Unknown Course", 0)
            enrollment = Enrollment(student, course)
            enrollment.enrollment_date = datetime.fromisoformat(en_data["enrollment_date"])
            if en_data.get("grade") is not None:
                enrollment.grade = int(en_data["grade"])
            student.enrollments.append(enrollment)
            course.add_student(student)

        students.append(student)

    return students

def load_students_from_xml(filename: str) -> List[Student]:
    tree = ET.parse(filename)
    root = tree.getroot()
    students = []

    for s_elem in root.findall("student"):
        student_id = s_elem.get("student_id")
        first_name = s_elem.find("first_name").text
        last_name = s_elem.find("last_name").text
        birth_date = s_elem.find("birth_date").text
        student = Student(first_name, last_name, birth_date, student_id)

        # Группы
        groups_elem = s_elem.find("groups")
        if groups_elem is not None:
            for g_elem in groups_elem.findall("group"):
                group = Group(g_elem.text)
                student.groups.append(group)
                group.add_student(student)

        # Записи на курсы
        enrollments_elem = s_elem.find("enrollments")
        if enrollments_elem is not None:
            for en_elem in enrollments_elem.findall("enrollment"):
                course_code = en_elem.find("course_code").text
                course = Course(course_code, "Unknown Course", 0)
                enrollment = Enrollment(student, course)
                date_str = en_elem.find("enrollment_date").text
                enrollment.enrollment_date = datetime.fromisoformat(date_str)
                grade_elem = en_elem.find("grade")
                if grade_elem is not None and grade_elem.text:
                    enrollment.grade = int(grade_elem.text)
                student.enrollments.append(enrollment)
                course.add_student(student)
        students.append(student)

    return students