from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker
from models import Student, Grade, Subject, Teacher, Group

DATABASE_URI = 'sqlite:///university.db'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)


def select_1():
    session = Session()
    result = session.query(
        Student.name,
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    ).join(Student.grades).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    session.close()
    return result


def select_2(subject_name):
    session = Session()
    result = session.query(
        Student.name,
        Subject.name,
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    ).join(Grade.student).join(Grade.subject).filter(Subject.name == subject_name).group_by(Student.id).order_by(desc('avg_grade')).first()
    session.close()
    return result


def select_3(subject_name):
    session = Session()
    result = session.query(
        Group.name,
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    ).join(Group.students).join(Student.grades).join(Grade.subject).filter(Subject.name == subject_name).group_by(Group.id).all()
    session.close()
    return result


def select_4():
    session = Session()
    result = session.query(
        func.round(func.avg(Grade.grade), 2).label('average_grade')
    ).scalar()
    session.close()
    return result


def select_5(teacher_name):
    session = Session()
    result = session.query(
        Teacher.name,
        Subject.name
    ).join(Teacher.subjects).filter(Teacher.name == teacher_name).all()
    session.close()
    return result


def select_6(group_name):
    session = Session()
    result = session.query(
        Student.name
    ).join(Student.group).filter(Group.name == group_name).all()
    session.close()
    return result


def select_7(group_name, subject_name):
    session = Session()
    result = session.query(
        Student.name,
        Grade.grade
    ).join(Student.group).join(Student.grades).join(Grade.subject).filter(Group.name == group_name, Subject.name == subject_name).all()
    session.close()
    return result


def select_8(teacher_name):
    session = Session()
    result = session.query(
        Teacher.name,
        func.round(func.avg(Grade.grade), 2).label('average_grade')
    ).join(Teacher.subjects).join(Subject.grades).filter(Teacher.name == teacher_name).group_by(Teacher.id).all()
    session.close()
    return result


def select_9(student_name):
    session = Session()
    result = session.query(
        Student.name,
        Subject.name
    ).join(Student.grades).join(Grade.subject).filter(Student.name == student_name).group_by(Subject.id).all()
    session.close()
    return result


def select_10(student_name, teacher_name):
    session = Session()
    result = session.query(
        Student.name,
        Teacher.name,
        Subject.name
    ).join(Student.grades).join(Grade.subject).join(Subject.teacher).filter(Student.name == student_name, Teacher.name == teacher_name).all()
    session.close()
    return result


def select_11(teacher_name, student_name):
    session = Session()
    result = session.query(
        Teacher.name,
        Student.name,
        func.round(func.avg(Grade.grade), 2).label('average_grade')
    ).join(Subject).join(Grade).join(Student).filter(Teacher.name == teacher_name, Student.name == student_name).group_by(Teacher.name, Student.name).all()
    session.close()
    return result


def select_12(group_name, subject_name):
    session = Session()
    result = session.query(
        Student.name,
        Grade.grade,
        func.max(Grade.date_received).label('last_lecture_date')
    ).join(Group).join(Grade).join(Subject).filter(Group.name == group_name, Subject.name == subject_name).group_by(Student.id).all()
    session.close()
    return result


if __name__ == "__main__":
    print("Top 5 students by average grade:")
    print(select_1())

    subject_name = "Mathematics"
    print(f"\nStudent with the highest average grade in {subject_name}:")
    print(select_2(subject_name))

    print(f"\nAverage grade in groups for {subject_name}:")
    print(select_3(subject_name))

    print("\nAverage grade across all subjects:")
    print(select_4())

    teacher_name = "John Doe"
    print(f"\nCourses taught by {teacher_name}:")
    print(select_5(teacher_name))

    group_name = "Group A"
    print(f"\nList of students in {group_name}:")
    print(select_6(group_name))

    print(f"\nGrades of students in {group_name} for {subject_name}:")
    print(select_7(group_name, subject_name))

    print(f"\nAverage grade given by {teacher_name}:")
    print(select_8(teacher_name))

    student_name = "Alice Johnson"
    print(f"\nList of courses attended by {student_name}:")
    print(select_9(student_name))

    print(f"\nCourses for {student_name} taught by {teacher_name}:")
    print(select_10(student_name, teacher_name))

    print(f"\nAverage grade from {teacher_name} to {student_name}:")
    print(select_11(teacher_name, student_name))

    print(f"\nGrades of students in {group_name} for {subject_name} on the last lecture:")
    print(select_12(group_name, subject_name))
