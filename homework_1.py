class Student:
    """Класс, представляющий студента."""
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        """Добавляет завершённый курс."""
        self.finished_courses.append(course_name)


class Mentor:
    """Родительский класс для всех преподавателей."""
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def rate_hw(self, student, course, grade):
        """Выставляет оценку студенту за домашнее задание."""
        if isinstance(student, Student) and course in self.courses_attached \
                and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


class Lecturer(Mentor):
    """Класс лекторов, наследующий от Mentor."""
    pass


class Reviewer(Mentor):
    """Класс проверяющих экспертов, наследующий от Mentor."""
    pass

lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')

print(isinstance(lecturer, Mentor))   # True
print(isinstance(reviewer, Mentor))   # True
print(lecturer.courses_attached)      # []
print(reviewer.courses_attached)      # []
