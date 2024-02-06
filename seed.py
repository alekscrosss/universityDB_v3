from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Group, Student, Teacher, Subject, Grade
from faker import Faker
import random

faker = Faker()

DATABASE_URI = 'sqlite:///university.db'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)


def seed_data():
    Base.metadata.create_all(engine)
    session = Session()

    # Создание учителей
    teachers = [Teacher(name=faker.name()) for _ in range(3)]
    session.add_all(teachers)

    # Создание групп
    groups = [Group(name=f"Group {chr(65+i)}") for i in range(3)]
    session.add_all(groups)

    subjects = [Subject(name=faker.word(), teacher=random.choice(teachers)) for _ in range(5)]
    session.add_all(subjects)

    for _ in range(50):
        group = random.choice(groups)
        student = Student(name=faker.name(), group=group)
        session.add(student)
        for subject in subjects:
            for _ in range(random.randint(5, 20)):
                grade = Grade(student=student, subject=subject, grade=random.uniform(2, 5),
                              date_received=faker.date_between(start_date='-1y', end_date='today'))
                session.add(grade)

    session.commit()
    session.close()


if __name__ == '__main__':
    seed_data()
