import pytest
from student import Student

def test_student_creation():
    student = Student("Иван Иванов", "subjects.csv")
    assert student.name == "Иван Иванов"

def test_add_grade():
    student = Student("Иван Иванов", "subjects.csv")
    student.add_grade("Математика", 5)
    assert student.subjects["Математика"]["grades"] == [5]

def test_add_test_score():
    student = Student("Иван Иванов", "subjects.csv")
    student.add_test_score("Математика", 90)
    assert student.subjects["Математика"]["test_scores"] == [90]

def test_get_average_grade():
    student = Student("Иван Иванов", "subjects.csv")
    student.add_grade("Математика", 5)
    student.add_grade("Математика", 4)
    assert student.get_average_grade() == 4.5

def test_get_average_test_score():
    student = Student("Иван Иванов", "subjects.csv")
    student.add_test_score("Математика", 90)
    student.add_test_score("Математика", 80)
    assert student.get_average_test_score("Математика") == 85.0

if __name__ == "__main__":
    pytest.main()