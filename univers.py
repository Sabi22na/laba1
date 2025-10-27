from datetime import datetime
from typing import List, Optional

class Person:
    def __init__(self, name: str, surname: str, birth_date: str):
        self.name = name
        self.surname = surname
        self.birth_date = birth_date

    def full_name(self) -> str:
        return f"{self.name} {self.surname}"

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.full_name()}>"

class Professor(Person):
    def __init__(self, name: str, surname: str, birth_date: str, employee_id: str):
        super().__init__(name, surname, birth_date)
        self.employee_id = employee_id
        self.courses: List['Course'] = []
        self.lessons: List['Lesson'] = []

    def assign_course(self, course: 'Course'):
        if course not in self.courses:
            self.courses.append(course)
            course.set_professor(self)

    def add_lesson(self, lesson: 'Lesson'):
        if lesson not in self.lessons:
            self.lessons.append(lesson)
            lesson.set_professor(self)

class Student(Person):
    def __init__(self, name: str, surname: str, birth_date: str, student_id: str):
        super().__init__(name, surname, birth_date)
        self.student_id = student_id
        self.enrollments: List['Enrollment'] = []
        self.groups: List['Group'] = []

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "first_name": self.name,
            "last_name": self.surname,
            "birth_date": self.birth_date,
            "enrollments": [
                {
                    "course_code": e.course.course_code,
                    "enrollment_date": e.enrollment_date.isoformat(),
                    "grade": e.grade
                }
                for e in self.enrollments
            ],
            "groups": [g.group_name for g in self.groups]
        }

    def enroll_in_course(self, course: 'Course'):
        enrollment = Enrollment(self, course)
        self.enrollments.append(enrollment)
        course.add_student(self)

    def join_group(self, group: 'Group'):
        if group not in self.groups:
            self.groups.append(group)
            group.add_student(self)

class Department:
    def __init__(self, name: str):
        self.name = name
        self.faculties: List['Faculty'] = []

    def add_faculty(self, faculty: 'Faculty'):
        if faculty not in self.faculties:
            self.faculties.append(faculty)
            faculty.set_department(self)

class Faculty:
    def __init__(self, name: str):
        self.name = name
        self.department: Optional['Department'] = None
        self.courses: List['Course'] = []

    def set_department(self, department: 'Department'):
        self.department = department

    def add_course(self, course: 'Course'):
        if course not in self.courses:
            self.courses.append(course)
            course.set_faculty(self)

class Course:
    def __init__(self, course_code: str, title: str, credits: int):
        self.course_code = course_code
        self.title = title
        self.credits = credits
        self.professor: Optional[Professor] = None
        self.students: List[Student] = []
        self.faculty: Optional[Faculty] = None
        self.enrollments: List['Enrollment'] = []

    def set_professor(self, professor: Professor):
        self.professor = professor

    def set_faculty(self, faculty: Faculty):
        self.faculty = faculty

    def add_student(self, student: Student):
        if student not in self.students:
            self.students.append(student)

class Enrollment:
    def __init__(self, student: Student, course: Course):
        self.student = student
        self.course = course
        self.enrollment_date = datetime.now()
        self.grade: Optional[int] = None  # Оценка по курсу

    def set_grade(self, grade: int):
        if 0 <= grade <= 54:
            self.grade = grade
        else:
            raise ValueError("Оценка должна быть от 0 до 54")

class Group:
    def __init__(self, group_name: str):
        self.group_name = group_name
        self.students: List[Student] = []
        self.schedule: Optional['Schedule'] = None

    def add_student(self, student: Student):
        if student not in self.students:
            self.students.append(student)
            student.join_group(self)

    def set_schedule(self, schedule: 'Schedule'):
        self.schedule = schedule
        schedule.add_group(self)

class Room:
    def __init__(self, room_number: str, capacity: int):
        self.room_number = room_number
        self.capacity = capacity
        self.lessons: List['Lesson'] = []

    def add_lesson(self, lesson: 'Lesson'):
        if lesson not in self.lessons:
            self.lessons.append(lesson)
            lesson.set_room(self)

class Lesson:
    def __init__(self, lesson_time: str, duration_minutes: int):
        self.lesson_time = lesson_time  # Например, "09:00"
        self.duration_minutes = duration_minutes
        self.professor: Optional[Professor] = None
        self.room: Optional[Room] = None
        self.course: Optional[Course] = None

    def set_professor(self, professor: Professor):
        self.professor = professor
        professor.add_lesson(self)

    def set_room(self, room: Room):
        self.room = room
        room.add_lesson(self)

    def set_course(self, course: Course):
        self.course = course

class Schedule:
    def __init__(self):
        self.groups: List[Group] = []
        self.professors: List[Professor] = []
        self.rooms: List[Room] = []
        self.lessons: List[Lesson] = []

    def add_group(self, group: Group):
        if group not in self.groups:
            self.groups.append(group)
            group.set_schedule(self)

    def add_professor(self, professor: Professor):
        if professor not in self.professors:
            self.professors.append(professor)

    def add_room(self, room: Room):
        if room not in self.rooms:
            self.rooms.append(room)

    def add_lesson(self, lesson: Lesson):
        if lesson not in self.lessons:
            self.lessons.append(lesson)

    def get_lessons_for_group(self, group: Group) -> List[Lesson]:
        return [l for l in self.lessons if l.course and any(s in group.students for s in l.course.students)]

    def get_lessons_for_professor(self, professor: Professor) -> List[Lesson]:
        return [l for l in self.lessons if l.professor == professor]

    def get_lessons_for_room(self, room: Room) -> List[Lesson]:
        return [l for l in self.lessons if l.room == room]
