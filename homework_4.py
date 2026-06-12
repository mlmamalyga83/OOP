import functools


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
        """Выставляет оценку лектору за лекцию."""
        if not isinstance(lecturer, Lecturer):
            return 'Ошибка'
        if course not in self.courses_in_progress or course not in lecturer.courses_attached:
            return 'Ошибка'
        if course in lecturer.grades:
            lecturer.grades[course] += [grade]
        else:
            lecturer.grades[course] = [grade]

    def _average_grade(self):
        """Внутренний метод: средняя оценка за все домашние задания."""
        if not self.grades:
            return 0.0
        total = sum(sum(grades) for grades in self.grades.values())
        count = sum(len(grades) for grades in self.grades.values())
        return total / count if count else 0.0

    @functools.total_ordering
    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() < other._average_grade()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() == other._average_grade()

    def __str__(self):
        avg = self._average_grade()
        courses_progress = ', '.join(self.courses_in_progress) or 'Нет'
        finished = ', '.join(self.finished_courses) or 'Нет'
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {avg:.1f}\n"
                f"Курсы в процессе изучения: {courses_progress}\n"
                f"Завершенные курсы: {finished}")


class Mentor:
    """Родительский класс для преподавателей."""
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


class Lecturer(Mentor):
    """Класс лекторов."""
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def _average_grade(self):
        """Внутренний метод: средняя оценка за все лекции."""
        if not self.grades:
            return 0.0
        total = sum(sum(grades) for grades in self.grades.values())
        count = sum(len(grades) for grades in self.grades.values())
        return total / count if count else 0.0

    @functools.total_ordering
    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_grade() < other._average_grade()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_grade() == other._average_grade()

    def __str__(self):
        base = super().__str__()
        avg = self._average_grade()
        return f"{base}\nСредняя оценка за лекции: {avg:.1f}"


class Reviewer(Mentor):
    """Класс экспертов, проверяющих домашние задания."""
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


# --- Функции для подсчёта средних оценок по курсу ---
def average_homework_grade(students, course):
    """Подсчитывает среднюю оценку за ДЗ по указанному курсу среди списка студентов.
    Учитываются только студенты, у которых есть оценки по данному курсу.
    Возвращает среднее значение или 0.0, если оценок нет."""
    total = 0
    count = 0
    for student in students:
        if course in student.grades and student.grades[course]:
            total += sum(student.grades[course])
            count += len(student.grades[course])
    return total / count if count else 0.0


def average_lecture_grade(lecturers, course):
    """Подсчитывает среднюю оценку за лекции по указанному курсу среди списка лекторов.
    Учитываются только лекторы, у которых есть оценки по данному курсу.
    Возвращает среднее значение или 0.0, если оценок нет."""
    total = 0
    count = 0
    for lecturer in lecturers:
        if course in lecturer.grades and lecturer.grades[course]:
            total += sum(lecturer.grades[course])
            count += len(lecturer.grades[course])
    return total / count if count else 0.0


# --- Демонстрация работы (полевые испытания) ---
if __name__ == "__main__":
    # Создаём по 2 экземпляра каждого класса
    student1 = Student('Анна', 'Смирнова', 'Ж')
    student2 = Student('Олег', 'Кузнецов', 'М')

    lecturer1 = Lecturer('Иван', 'Иванов')
    lecturer2 = Lecturer('Сергей', 'Сергеев')

    reviewer1 = Reviewer('Пётр', 'Петров')
    reviewer2 = Reviewer('Мария', 'Сидорова')

    # Назначаем курсы
    student1.courses_in_progress = ['Python', 'Git']
    student1.finished_courses = ['Введение в программирование']
    student2.courses_in_progress = ['Python', 'Java']
    student2.finished_courses = ['Математика']

    lecturer1.courses_attached = ['Python', 'Git']
    lecturer2.courses_attached = ['Python', 'Java']

    reviewer1.courses_attached = ['Python', 'Git']
    reviewer2.courses_attached = ['Python', 'Java']

    # Вызываем методы: Reviewer.rate_hw, Student.rate_lecture
    reviewer1.rate_hw(student1, 'Python', 10)
    reviewer1.rate_hw(student1, 'Python', 9)
    reviewer2.rate_hw(student2, 'Python', 8)
    reviewer2.rate_hw(student2, 'Python', 7)

    student1.rate_lecture(lecturer1, 'Python', 10)
    student1.rate_lecture(lecturer1, 'Python', 9)
    student2.rate_lecture(lecturer2, 'Python', 8)
    student2.rate_lecture(lecturer2, 'Python', 7)
    # Ошибка: студент пытается оценить лектора не на своём курсе
    print(student1.rate_lecture(lecturer2, 'Java', 6))  # 'Ошибка', т.к. student1 не на Java

    # Демонстрация __str__
    print("=== Студенты ===")
    print(student1)
    print()
    print(student2)
    print()
    print("=== Лекторы ===")
    print(lecturer1)
    print()
    print(lecturer2)
    print()
    print("=== Проверяющие ===")
    print(reviewer1)
    print()
    print(reviewer2)
    print()

    # Сравнения
    print("Сравнение студентов:", student1 > student2)   # True (9.5 > 7.5)
    print("Сравнение лекторов:", lecturer1 < lecturer2)  # True (9.5 < 7.5? На самом деле lecturer1 средний 9.5, lecturer2 7.5, значит lecturer1 > lecturer2)

    # Вызов функций подсчёта средней оценки по курсу
    students_list = [student1, student2]
    lecturers_list = [lecturer1, lecturer2]

    print("\nСредняя оценка за ДЗ по Python:",
          average_homework_grade(students_list, 'Python'))
    print("Средняя оценка за лекции по Python:",
          average_lecture_grade(lecturers_list, 'Python'))
    # Курс Git: у student1 нет оценок, функция вернёт 0.0
    print("Средняя оценка за ДЗ по Git:",
          average_homework_grade(students_list, 'Git'))
    # У лекторов по Java: lecturer1 не ведёт Java, lecturer2 ведёт, но у него нет оценок, т.к. student2 Java не оценивал – вернёт 0.0
    print("Средняя оценка за лекции по Java:",
          average_lecture_grade(lecturers_list, 'Java'))