import csv
import argparse
import logging

class NameDescriptor:
    def __set__(self, instance, value):
        if not all(part.istitle() and part.isalpha() for part in value.split()):
            raise ValueError("ФИО должно состоять только из букв и начинаться с заглавной буквы")
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name

class Student:
    name = NameDescriptor()

    def __init__(self, name, subjects_file):
        self.name = name
        self.subjects = {}
        self.load_subjects(subjects_file)

    def load_subjects(self, subjects_file):
        with open(subjects_file, 'r') as file:
            reader = csv.reader(file)
            subjects_from_file = next(reader)
            for subject in subjects_from_file:
                self.subjects[subject.strip()] = {'grades': [], 'test_scores': []}

    def __getattr__(self, name):
        if name in self.subjects:
            return self.subjects[name]
        else:
            raise AttributeError(f"Предмет {name} не найден")

    def __str__(self):
        subjects_with_grades = [subject for subject, info in self.subjects.items() if info['grades']]
        return f"Студент: {self.name}\nПредметы: {', '.join(subjects_with_grades)}"

    def add_grade(self, subject, grade):
        if subject not in self.subjects:
            raise ValueError(f"Предмет {subject} не найден")
        if not isinstance(grade, int) or grade < 2 or grade > 5:
            raise ValueError("Оценка должна быть целым числом от 2 до 5")
        self.subjects[subject]['grades'].append(grade)

    def add_test_score(self, subject, test_score):
        if subject not in self.subjects:
            raise ValueError(f"Предмет {subject} не найден")
        if not isinstance(test_score, int) or test_score < 0 or test_score > 100:
            raise ValueError("Результат теста должен быть целым числом от 0 до 100")
        self.subjects[subject]['test_scores'].append(test_score)

    def get_average_test_score(self, subject):
        if subject not in self.subjects:
            raise ValueError(f"Предмет {subject} не найден")
        test_scores = self.subjects[subject]['test_scores']
        return sum(test_scores) / len(test_scores) if test_scores else 0

    def get_average_grade(self):
        total_grades = sum(sum(info['grades']) for info in self.subjects.values())
        total_subjects = sum(1 for info in self.subjects.values() if info['grades'])
        return total_grades / total_subjects if total_subjects else 0

def main():
    parser = argparse.ArgumentParser(description='Обработка студентов и их предметов.')
    parser.add_argument('subjects_file', type=str, help='CSV файл с предметами')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        student = Student("Иван Иванов", args.subjects_file)

        student.add_grade("Математика", 4)
        student.add_test_score("Математика", 85)

        student.add_grade("История", 5)
        student.add_test_score("История", 92)

        average_grade = student.get_average_grade()
        logging.info(f"Средний балл: {average_grade}")

        average_test_score = student.get_average_test_score("Математика")
        logging.info(f"Средний результат по тестам по математике: {average_test_score}")

        logging.info(student)
    except ValueError as e:
        logging.error(e)

if __name__ == "__main__":
    main()