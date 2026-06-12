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
        """Вычисляет среднюю оценку за домашние задания."""
        if not self.grades:
            return 0.0
        total = sum(sum(grades) for grades in self.grades.values())
        count = sum(len(grades) for grades in self.grades.values())
        return total / count if count else 0.0

    @functools.total_ordering
    def __lt__(self, other):
        """Сравнение студентов по средней оценке (меньше)."""
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() < other._average_grade()

    def __eq__(self, other):
        """Сравнение студентов на равенство средней оценки."""
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() == other._average_grade()

    def __str__(self):
        """Вывод информации о студенте."""
        avg = self._average_grade()
        courses_progress = ', '.join(self.courses_in_progress) or 'Нет'
        finished = ', '.join(self.finished_courses) or 'Нет'
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {avg:.1f}\n"
                f"Курсы в процессе изучения: {courses_progress}\n"
                f"Завершенные курсы: {finished}")


class Mentor:
    """Родительский класс для всех преподавателей."""
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        """Базовый вывод имени и фамилии."""
        return f"Имя: {self.name}\nФамилия: {self.surname}"


class Lecturer(Mentor):
    """Класс лекторов, получающих оценки за лекции."""
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def _average_grade(self):
        """Вычисляет среднюю оценку за лекции."""
        if not self.grades:
            return 0.0
        total = sum(sum(grades) for grades in self.grades.values())
        count = sum(len(grades) for grades in self.grades.values())
        return total / count if count else 0.0

    @functools.total_ordering
    def __lt__(self, other):
        """Сравнение лекторов по средней оценке (меньше)."""
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_grade() < other._average_grade()

    def __eq__(self, other):
        """Сравнение лекторов на равенство средней оценки."""
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_grade() == other._average_grade()

    def __str__(self):
        """Вывод информации о лекторе."""
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


# Демонстрация работы (можно скопировать для проверки)
if __name__ == "__main__":
    # Создаём экземпляры
    lecturer1 = Lecturer('Иван', 'Иванов')
    lecturer2 = Lecturer('Сергей', 'Сергеев')
    reviewer = Reviewer('Пётр', 'Петров')
    student1 = Student('Анна', 'Смирнова', 'Ж')
    student2 = Student('Олег', 'Кузнецов', 'М')

    # Настраиваем курсы
    student1.courses_in_progress += ['Python', 'Git']
    student1.finished_courses += ['Введение в программирование']
    student2.courses_in_progress += ['Python']
    student2.finished_courses += ['Математика']

    lecturer1.courses_attached += ['Python', 'Git']
    lecturer2.courses_attached += ['Python']
    reviewer.courses_attached += ['Python']

    # Выставляем оценки
    reviewer.rate_hw(student1, 'Python', 10)
    reviewer.rate_hw(student1, 'Python', 9)
    reviewer.rate_hw(student2, 'Python', 8)

    student1.rate_lecture(lecturer1, 'Python', 10)
    student1.rate_lecture(lecturer1, 'Python', 9)
    student2.rate_lecture(lecturer2, 'Python', 7)

    # Вывод информации
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

    print("=== Проверяющий ===")
    print(reviewer)
    print()

    # Сравнения
    print("Сравнение студентов:")
    print(student1 > student2)   # True (9.5 > 8.0)
    print(student1 == student2)  # False
    print(student1 < student2)   # False

    print("\nСравнение лекторов:")
    print(lecturer1 > lecturer2) # True (9.5 > 7.0)
    print(lecturer1 == lecturer2) # False