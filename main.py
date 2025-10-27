from univers import Department, Faculty, Professor, Student, Course, Group, Room, Lesson, Schedule
from serializers import save_students_to_json, save_students_to_xml
from deserializers import load_students_from_json, load_students_from_xml

if __name__ == "__main__":
    dept = Department("Computer Science")
    fac = Faculty("Engineering")
    prof = Professor("Alice", "Johnson", "2006-09-21", "prof21053")
    stud1 = Student("Sabina", "Babaeva", "2005-03-22", "124017")
    stud2 = Student("Charlie", "Green", "2006-11-30", "123067")
    course = Course("09.03.03", "Introduction to Programming", 5)
    group = Group("ИДБ-24-11")
    room = Room("305", 2)
    lesson = Lesson("10:20", 90)
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

    # Запись студентов на курс
    stud1.enroll_in_course(course)
    stud2.enroll_in_course(course)

    # Выставление оценок ДО сохранения
    if stud1.enrollments:
        stud1.enrollments[0].set_grade(48)

    # Добавление в группу
    stud1.join_group(group)
    stud2.join_group(group)

    # Сохранение
    all_students = [stud1, stud2]
    save_students_to_json(all_students, "university.json")
    save_students_to_xml(all_students, "university.xml")
    # Сохранение данных
    all_students = [stud1, stud2]
    save_students_to_json(all_students, "university.json")
    save_students_to_xml(all_students, "university.xml")
    print("Данные успешно сохранены в university.json и university.xml")

    # Загрузка данных
    loaded_students_json = load_students_from_json("university.json")
    loaded_students_xml = load_students_from_xml("university.xml")

    # Вывод информации
    for i, s in enumerate(loaded_students_json, 1):
        print(f"\n--- Студент {i} ---")
        print(f"  Имя: {s.full_name()}")
        print(f"  ID: {s.student_id}")
        print(f"  Группа: {s.groups[0].group_name if s.groups else 'Нет'}")
        if s.enrollments:
            e = s.enrollments[0]
            print(f"  Курс: {e.course.title}")
            print(f"  Оценка: {e.grade if e.grade is not None else 'Не выставлена'}")