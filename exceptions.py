from typing import List, Optional
from datetime import datetime

class UniversityError(Exception):
    """Базовое исключение для университетской системы"""
    pass

class InvalidGradeError(UniversityError):
    """Оценка вне допустимого диапазона (0–54)"""
    pass

class DuplicateEnrollmentError(UniversityError):
    """Студент уже записан на курс"""
    pass

class ProfessorAlreadyAssignedError(UniversityError):
    """Преподаватель уже назначен на курс"""
    pass

class GroupAlreadyJoinedError(UniversityError):
    """Студент уже состоит в группе"""
    pass

# ========================
# Базовый класс Person
# ========================

class Person:
    def __init__(self, name: str, surname: str, birth_date: str):
        self.name = name
        self.surname = surname
        self.birth_date = birth_date

    def full_name(self) -> str:
        return f"{self.name} {self.surname}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.surname})"


# ========================
# Professor
# ========================

class Professor(Person):
    def __init__(self, name: str, surname: str, birth_date: str, employee_id: str):
        super().__init__(name, surname, birth_date)
        self.employee_id = employee_id
        self.courses: List['Course'] = []
        self.lessons: List['Lesson'] = []

    def assign_course(self, course: 'Course'):
        try:
            if course in self.courses:
                raise ProfessorAlreadyAssignedError(
                    f"Преподаватель {self.full_name()} уже ведёт курс '{course.title}'"
                )
            self.courses.append(course)
            course.set_professor(self)
        except ProfessorAlreadyAssignedError as e:
            print(f"[Ошибка назначения] {e}")
        except Exception as e:
            print(f"[Неизвестная ошибка] {e}")

    def add_lesson(self, lesson: 'Lesson'):
        try:
            if lesson not in self.lessons:
                self.lessons.append(lesson)
                lesson.set_professor(self)
        except Exception as e:
            print(f"[Ошибка добавления занятия] {e}")


# ========================
# Student
# ========================

class Student(Person):
    def __init__(self, name: str, surname: str, birth_date: str, student_id: str):
        super().__init__(name, surname, birth_date)
        self.student_id = student_id
        self.enrollments: List['Enrollment'] = []
        self.groups: List['Group'] = []

    def enroll_in_course(self, course: 'Course'):
        try:
            for e in self.enrollments:
                if e.course == course:
                    raise DuplicateEnrollmentError(
                        f"Студент {self.full_name()} уже записан на курс '{course.title}'"
                    )
            enrollment = Enrollment(self, course)
            self.enrollments.append(enrollment)
            course.add_student(self)
            print(f"✅ {self.full_name()} успешно записан на курс '{course.title}'")
        except DuplicateEnrollmentError as e:
            print(f"[Ошибка записи] {e}")
        except Exception as e:
            print(f"[Системная ошибка записи] {e}")

    def join_group(self, group: 'Group'):
        try:
            if group in self.groups:
                raise GroupAlreadyJoinedError(
                    f"Студент {self.full_name()} уже состоит в группе '{group.group_name}'"
                )
            self.groups.append(group)
            group.add_student(self)
            print(f"✅ {self.full_name()} вступил в группу '{group.group_name}'")
        except GroupAlreadyJoinedError as e:
            print(f"[Ошибка добавления в группу] {e}")
        except Exception as e:
            print(f"[Системная ошибка группы] {e}")


# ========================
# Department, Faculty, Course
# ========================

class Department:
    def __init__(self, name: str):
        self.name = name
        self.faculties: List['Faculty'] = []

    def add_faculty(self, faculty: 'Faculty'):
        try:
            if faculty not in self.faculties:
                self.faculties.append(faculty)
                faculty.set_department(self)
        except Exception as e:
            print(f"[Ошибка добавления факультета в кафедру] {e}")


class Faculty:
    def __init__(self, name: str):
        self.name = name
        self.department: Optional[Department] = None
        self.courses: List['Course'] = []

    def set_department(self, department: 'Department'):
        self.department = department

    def add_course(self, course: 'Course'):
        try:
            if course not in self.courses:
                self.courses.append(course)
                course.set_faculty(self)
        except Exception as e:
            print(f"[Ошибка добавления курса на факультет] {e}")


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
        try:
            if self.professor and self.professor != professor:
                print(f"Курс '{self.title}' уже имел преподавателя {self.professor.full_name()}. Заменён на {professor.full_name()}.")
            self.professor = professor
        except Exception as e:
            print(f"[Ошибка назначения преподавателя] {e}")

    def set_faculty(self, faculty: Faculty):
        self.faculty = faculty

    def add_student(self, student: Student):
        if student not in self.students:
            self.students.append(student)


# ========================
# Enrollment
# ========================

class Enrollment:
    def __init__(self, student: Student, course: Course):
        self.student = student
        self.course = course
        self.enrollment_date = datetime.now()
        self.grade: Optional[int] = None

    def set_grade(self, grade: int):
        try:
            if not (0 <= grade <= 54):
                raise InvalidGradeError(f"Оценка {grade} недопустима. Должна быть от 0 до 54.")
            self.grade = grade
            print(f"✅ Оценка {grade} успешно установлена для {self.student.full_name()} по курсу '{self.course.title}'")
        except InvalidGradeError as e:
            print(f"[Ошибка оценки] {e}")
        except Exception as e:
            print(f"[Системная ошибка оценки] {e}")


# ========================
# Group, Room, Lesson, Schedule
# ========================

class Group:
    def __init__(self, group_name: str):
        self.group_name = group_name
        self.students: List[Student] = []
        self.schedule: Optional['Schedule'] = None

    def add_student(self, student: Student):
        if student not in self.students:
            self.students.append(student)

    def set_schedule(self, schedule: 'Schedule'):
        self.schedule = schedule
        schedule.add_group(self)


class Room:
    def __init__(self, room_number: str, capacity: int):
        self.room_number = room_number
        self.capacity = capacity
        self.lessons: List['Lesson'] = []

    def add_lesson(self, lesson: 'Lesson'):
        try:
            # Проверка вместимости УДАЛЕНА (т.к. исключение RoomCapacityExceededError удалено)
            if lesson not in self.lessons:
                self.lessons.append(lesson)
                lesson.set_room(self)
                course_title = lesson.course.title if lesson.course else 'N/A'
                print(f"✅ Занятие по курсу '{course_title}' добавлено в аудиторию {self.room_number}")
        except Exception as e:
            print(f"[Ошибка добавления занятия в аудиторию] {e}")


class Lesson:
    def __init__(self, lesson_time: str, duration_minutes: int):
        self.lesson_time = lesson_time
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

    def add_professor(self, professor: Professor):
        if professor not in self.professors:
            self.professors.append(professor)

    def add_room(self, room: Room):
        if room not in self.rooms:
            self.rooms.append(room)

    def add_lesson(self, lesson: Lesson):
        if lesson not in self.lessons:
            self.lessons.append(lesson)


# ========================
# Демонстрация работы (с ошибками и без)
# ========================

if __name__ == "__main__":
    print("=== Университетская система (с обработкой исключений) ===\n")

    # Создание объектов
    dept = Department("Computer Science")
    fac = Faculty("Engineering")
    prof = Professor("Alice", "Johnson", "2006-09-21","prof21053")
    stud1 = Student("Sabina","Babaeva","2005-03-22","124017")
    stud2 = Student("Charlie", "Green", "2006-11-30","123067")
    course = Course("09.03.03","Introduction to Programming", 5)
    group = Group("ИДБ-24-11")
    room = Room("305", 2)  # Вместимость 2, но проверка отключена
    lesson = Lesson("10:20",90)
    schedule = Schedule()

    # Настройка структуры
    dept.add_faculty(fac)
    fac.add_course(course)
    prof.assign_course(course)
    stud1.enroll_in_course(course)
    stud2.enroll_in_course(course)
    stud1.join_group(group)
    stud2.join_group(group)
    group.set_schedule(schedule)
    lesson.set_course(course)
    lesson.set_professor(prof)
    schedule.add_lesson(lesson)

    print("\n--- Попытка повторной записи студента на тот же курс ---")
    stud1.enroll_in_course(course)  # Должна быть ошибка

    print("\n--- Попытка поставить некорректную оценку ---")
    if stud1.enrollments:
        stud1.enrollments[0].set_grade(150)  # Ошибка

    print("\n--- Добавление занятия в аудиторию (проверка вместимости отключена) ---")
    # Добавим третьего студента — ошибки не будет
    stud3 = Student("David", "White", "2006-09-05", "124143")
    course.add_student(stud3)
    room.add_lesson(lesson)  # Успешно

    print("\n--- Успешная постановка корректной оценки ---")
    if stud1.enrollments:
        stud1.enrollments[0].set_grade(48)  # Успех

    print("\n=== Работа программы завершена корректно (без аварийного выхода) ===")