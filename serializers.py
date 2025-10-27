import json
import xml.etree.ElementTree as ET
from typing import List
from univers import Student

def save_students_to_json(students: List['Student'], filename: str):
    data = [s.to_dict() for s in students]
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_students_to_xml(students: List['Student'], filename: str):
    root = ET.Element("students")
    for student in students:
        s_elem = ET.SubElement(root, "student", student_id=student.student_id)
        ET.SubElement(s_elem, "first_name").text = student.name
        ET.SubElement(s_elem, "last_name").text = student.surname
        ET.SubElement(s_elem, "birth_date").text = student.birth_date

        enrollments_elem = ET.SubElement(s_elem, "enrollments")
        for e in student.enrollments:
            en_elem = ET.SubElement(enrollments_elem, "enrollment")
            ET.SubElement(en_elem, "course_code").text = e.course.course_code
            ET.SubElement(en_elem, "enrollment_date").text = e.enrollment_date.isoformat()
            if e.grade is not None:
                ET.SubElement(en_elem, "grade").text = str(e.grade)

        groups_elem = ET.SubElement(s_elem, "groups")
        for g in student.groups:
            ET.SubElement(groups_elem, "group").text = g.group_name

    tree = ET.ElementTree(root)
    tree.write(filename, xml_declaration=True)