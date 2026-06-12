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

    def rate_lecture(self, lecturer, course, grade):
        """Выставляет оценку лектору за лекцию.
        Проверяет, что лектор прикреплён к курсу, а студент записан на него.
        Возвращает None при успехе или 'Ошибка'."""
        if not isinstance(lecturer, Lecturer):
            return 'Ошибка'
        if course not in self.courses_in_progress or course not in lecturer.courses_attached:
            return 'Ошибка'
        if course in lecturer.grades:
            lecturer.grades[course] += [grade]
        else:
            lecturer.grades[course] = [grade]


class Mentor:
    """Родительский класс для всех преподавателей."""
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    """Класс лекторов, получающих оценки за лекции."""
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}


class Reviewer(Mentor):
    """Класс экспертов, проверяющих домашние задания."""
    def rate_hw(self, student, course, grade):
        """Выставляет оценку студенту за домашнее задание.
        Проверяет, что эксперт и студент связаны с курсом."""
        if isinstance(student, Student) and course in self.courses_attached \
                and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

# Пример из задания
lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')
student = Student('Алёхина', 'Ольга', 'Ж')

student.courses_in_progress += ['Python', 'Java']
lecturer.courses_attached += ['Python', 'C++']
reviewer.courses_attached += ['Python', 'C++']

print(student.rate_lecture(lecturer, 'Python', 7))   # None
print(student.rate_lecture(lecturer, 'Java', 8))     # Ошибка (лектор не прикреплён к Java)
print(student.rate_lecture(lecturer, 'С++', 8))      # Ошибка (кириллица vs латиница)
print(student.rate_lecture(reviewer, 'Python', 6))   # Ошибка (reviewer не Lecturer)

print(lecturer.grades)  # {'Python': [7]}