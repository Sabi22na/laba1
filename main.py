from univers import Department, Faculty, Professor, Student, Course, Group, Room, Lesson, Schedule
from serializers import save_students_to_json, save_students_to_xml

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

all_students = [stud1, stud2]
save_students_to_json(all_students, "university.json")
save_students_to_xml(all_students, "university.xml")

print("Данные успешно сохранены!")