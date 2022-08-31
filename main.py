def av_grade_func(objects_list, course):
    all_grades_dict = {course: []}
    for obj in objects_list:
        if course in obj.grades:
            all_grades_dict[course] += obj.grades[course]

    return av_dict_func(all_grades_dict)


def av_dict_func(input_dict):
    sum_all = 0
    len_all = 0
    for k, v in input_dict.items():
        len_all += len(v)
        sum_all += sum(v)

    if len_all == 0:
        average_grade = 'Нет оценок'
    else:
        average_grade = round(sum_all / len_all, 2)

    return average_grade


def grade_check(input_grade):
    if not isinstance(input_grade, int):
        print('Оценка должна быть целым числом!')
        return False
    elif not 1 <= input_grade <= 10:
        print('Оценка должна быть от 1 до 10')
        return False
    else:
        return True


def compare_func(self_grades, other_grades, operand):
    av_grade_self = av_dict_func(self_grades)
    av_grade_other = av_dict_func(other_grades)

    if isinstance(av_grade_self, float) and isinstance(av_grade_other, float):
        if operand == '<':
            return av_grade_self < av_grade_other
        elif operand == '<=':
            return av_grade_self <= av_grade_other
        elif operand == '==':
            return av_grade_self == av_grade_other
    else:
        return 'Сравнение невозможно, т.к. не у всех есть оценки'


class Student:
    student_list = []

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        self.student_list += [self]

    def rate_lecture(self, lecturer, course, grade):

        if not grade_check(grade):
            return

        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and \
                course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        # else:
        #     print('Оценка не выставлена:\n'
        #           'Возможно, лектор не ведет такой курс\n'
        #           'Или студент его не изучает')


    def __str__(self):
        post = ''
        if isinstance(self, Postgraduate): post = 'Postgraduate\n'

        if not self.finished_courses:
            fc_string = 'Нет'
        else:
            fc_string = ", ".join(self.finished_courses)

        res = f'{post}Student:\n{self.name}\n{self.surname}\n' \
              f'Средняя оценка за домашние задания: {av_dict_func(self.grades)}\n' \
              f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n' \
              f'Завершенные курсы: {fc_string}'
        if isinstance(self, Postgraduate):
            res = res + f'\nКурсы, назначенные для проверки ДЗ: ' \
                        f'{", ".join(self.courses_attached)}'

        return res

    def __lt__(self, other):
        if not isinstance(other, Student):
            return 'Нельзя сравнивать студентов и не студентов'
        return compare_func(self.grades, other.grades, '<')

    def __le__(self, other):
        if not isinstance(other, Student):
            return 'Нельзя сравнивать студентов и не студентов'
        return compare_func(self.grades, other.grades, '<=')

    def __eq__(self, other):
        if not isinstance(other, Student):
            return 'Нельзя сравнивать студентов и не студентов'
        return compare_func(self.grades, other.grades, '==')


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    lecturer_list = []

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}
        self.lecturer_list += [self]

    def __str__(self):
        res = f'Lecturer:\n{self.name}\n{self.surname}\n' \
              f'Средняя оценка за лекции: {av_dict_func(self.grades)}\n'
        return res

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return 'Нельзя сравнивать лекторов и не лекторов'
        return compare_func(self.grades, other.grades, '<')

    def __le__(self, other):
        if not isinstance(other, Lecturer):
            return 'Нельзя сравнивать лекторов и не лекторов'
        return compare_func(self.grades, other.grades, '<=')

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return 'Нельзя сравнивать лекторов и не лекторов'
        return compare_func(self.grades, other.grades, '==')


class Reviewer(Mentor):
    reviewer_list = []

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.reviewer_list += [self]


    def rate_hw(self, student, course, grade):

        if not grade_check(grade):
            return

        if isinstance(student, Student) and course in student.courses_in_progress and \
                course in self.courses_attached:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        # else:
        #     print('Оценка не выставлена:\n'
        #           'Возможно, студент не изучает такой курс\n'
        #           'Или проверяющий его не ведет')

    def __str__(self):
        res = f'Reviewer:\n{self.name}\n{self.surname}'
        return res


class Postgraduate(Student, Reviewer):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.reviewer_list += [self]


student_1 = Student('Ваня', 'Петров')
student_1.finished_courses = ['physics', 'math', 'astronomy']
student_1.courses_in_progress = ['Python', 'SQL', 'Git']

student_2 = Student('Петя', 'Иванов')
student_2.finished_courses = ['physics']
student_2.courses_in_progress = ['Python', 'SQL', 'Git']

student_3 = Student('Вася', 'Максимов')
student_3.finished_courses = ['math', 'astronomy']
student_3.courses_in_progress = ['Python', 'SQL', 'Git']

lecturer_1 = Lecturer('Лев', 'Толстой')
lecturer_1.courses_attached = ['Python', 'SQL']

lecturer_2 = Lecturer('Ильф', 'Петров')
lecturer_2.courses_attached = ['Python', 'Git']

lecturer_3 = Lecturer('Александр', 'Хрюшкин')
lecturer_3.courses_attached = ['SQL', 'Python']

reviewer_1 = Reviewer('Иван', 'Проверялкин')
reviewer_1.courses_attached = ['Python', 'SQL', 'Git']

postgraduate_1 = Postgraduate('Петя-аспирант', 'Семёнов')
postgraduate_1.courses_in_progress = ['Python', 'math', 'astronomy']
postgraduate_1.courses_attached = reviewer_1.courses_attached.copy()

for lect in Lecturer.lecturer_list:
    for stud in Student.student_list:
        for elem, course in enumerate(stud.courses_in_progress):
            stud.rate_lecture(lect, stud.courses_in_progress[elem], 5)

student_1.rate_lecture(lecturer_1, student_1.courses_in_progress[0], 4)
student_1.rate_lecture(lecturer_2, student_1.courses_in_progress[1], 5)
postgraduate_1.rate_lecture(lecturer_3, postgraduate_1.courses_in_progress[0], 9)
postgraduate_1.rate_lecture(lecturer_1, student_1.courses_in_progress[0], 1)
student_2.rate_lecture(lecturer_2, student_2.courses_in_progress[2], 8)

for stud in Student.student_list:
    for rev in Reviewer.reviewer_list:
        for elem, course in enumerate(rev.courses_attached):
            rev.rate_hw(stud, stud.courses_in_progress[elem], 6)

postgraduate_1.rate_hw(student_1, student_1.courses_in_progress[0], 3)
postgraduate_1.rate_hw(student_1, student_1.courses_in_progress[1], 4)
postgraduate_1.rate_hw(student_1, student_1.courses_in_progress[2], 5)

reviewer_1.rate_hw(student_3, student_3.courses_in_progress[0], 7)
reviewer_1.rate_hw(student_3, student_3.courses_in_progress[1], 8)
reviewer_1.rate_hw(student_3, student_3.courses_in_progress[2], 9)

print()
print('Количество студентов:', len(Student.student_list))
for obj in Student.student_list:
    print(obj, '\n', sep='')

print(f'Средняя оценка всех студентов:\n'
      f'по курсу Python: {av_grade_func(Student.student_list, "Python")}\n'
      f'по курсу SQL: {av_grade_func(Student.student_list, "SQL")}\n'
      f'по курсу Git: {av_grade_func(Student.student_list, "Git")}\n')

print('Количество лекторов:', len(Lecturer.lecturer_list))
for obj in Lecturer.lecturer_list:
    print(obj)

print(f'Средняя оценка всех лекторов:\n'
      f'по курсу Python: {av_grade_func(Lecturer.lecturer_list, "Python")}\n'
      f'по курсу SQL: {av_grade_func(Lecturer.lecturer_list, "SQL")}\n'
      f'по курсу Git: {av_grade_func(Lecturer.lecturer_list, "Git")}')

print()
print(student_1 < student_2)
print(student_2 >= student_3)
print(student_1 == student_1)
print(student_1 <= postgraduate_1)
print(student_1 <= lecturer_1)
print(lecturer_1 < student_1)
print(lecturer_1 < lecturer_3)
print(lecturer_2 == lecturer_3)