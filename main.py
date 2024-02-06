import argparse
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from models import Teacher, Group, Student, Subject, Grade


DATABASE_URI = 'sqlite:///university.db'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)


def create_model(model, **kwargs):
    session = Session()
    instance = None
    if model == 'Teacher':
        instance = Teacher(**kwargs)
    elif model == 'Group':
        instance = Group(**kwargs)
    elif model == 'Student':
        instance = Student(**kwargs)
    elif model == 'Subject':
        instance = Subject(**kwargs)
    elif model == 'Grade':
        instance = Grade(**kwargs)

    if instance:
        try:
            session.add(instance)
            session.commit()
            print(f'{model} created with ID: {instance.id}')
        except exc.SQLAlchemyError as e:
            print(f'Error creating {model}: {e}')
    else:
        print(f'Model {model} is not supported.')
    session.close()


def list_models(model):
    session = Session()
    result = None
    try:
        result = session.query(eval(model)).all()
    except exc.SQLAlchemyError as e:
        print(f'Error listing {model}: {e}')

    if result:
        for item in result:
            print(item.id, item.name)
    else:
        print(f'No entries found for {model}')
    session.close()


def update_model(model, model_id, **kwargs):
    session = Session()
    model_class = eval(model)
    try:
        instance = session.query(model_class).get(model_id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            session.commit()
            print(f'{model} with ID {model_id} updated.')
        else:
            print(f'{model} with ID {model_id} not found.')
    except exc.SQLAlchemyError as e:
        print(f'Error updating {model}: {e}')
    finally:
        session.close()


def remove_model(model, model_id):
    session = Session()
    model_class = eval(model)
    try:
        instance = session.query(model_class).get(model_id)
        if instance:
            session.delete(instance)
            session.commit()
            print(f'{model} with ID {model_id} removed.')
        else:
            print(f'{model} with ID {model_id} not found.')
    except exc.SQLAlchemyError as e:
        print(f'Error removing {model}: {e}')
    finally:
        session.close()


def main():
    parser = argparse.ArgumentParser(description="CLI for interacting with the university database")
    parser.add_argument('-a', '--action', choices=['create', 'list', 'update', 'remove'],
                        help="CRUD operations: create, list, update, remove")
    parser.add_argument('-m', '--model', help="Model to interact with: Teacher, Group, Student, Subject, Grade")
    parser.add_argument('--name', help="Name of the object for creation or update")
    parser.add_argument('--id', type=int, help="ID of the object for update or removal")

    args = parser.parse_args()

    if args.action == 'create' and args.model:
        create_model(args.model, name=args.name)
    elif args.action == 'list' and args.model:
        list_models(args.model)
    elif args.action == 'update' and args.model and args.id:
        update_model(args.model, args.id, name=args.name)  # Add more fields as needed
    elif args.action == 'remove' and args.model and args.id:
        remove_model(args.model, args.id)


if __name__ == "__main__":
    main()
