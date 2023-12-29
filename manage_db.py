import sqlite3
from contextlib import contextmanager
from random import randint
from datetime import datetime, timedelta
from faker import Faker

from constants import db_file_name, sql_create_students_table, sql_create_groups_table, \
    sql_create_professors_table, sql_create_subjects_table, sql_grades_table, \
    sql_insert_data_groups, sql_insert_data_students, sql_insert_data_subjects, \
    sql_insert_data_professors, sql_insert_data_grades, \
    students_in_a_group_count, groups, subjects, professors, groups_list


@contextmanager
def db_connection(db_file):
    connection = sqlite3.connect(db_file)
    yield connection
    connection.rollback()
    connection.close()


def create_table(connection, create_table_sql):
    try:
        c = connection.cursor()
        c.execute(create_table_sql)
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()


def create_db_tables() -> str:
    print('Creating db...')

    db_connection(db_file_name)

    with db_connection(db_file_name) as connect:
        if connect is None:
            # print("Error! cannot create the database connection.")
            return 'Error! cannot create the database connection.'

        else:
            # create groups table
            create_table(connect, sql_create_groups_table)

            # create students table
            create_table(connect, sql_create_students_table)

            # create subjects table
            create_table(connect, sql_create_subjects_table)

            # create professors table
            create_table(connect, sql_create_professors_table)

            # create grades table
            create_table(connect, sql_grades_table)

    return 'DB was created'


def insert_data() -> str:
    print('Inserting test data...')
    db_connection(db_file_name)

    f = Faker()

    # generate student list
    students_list = []

    for gr_id in range(1, len(groups) + 1):
        for i in range(students_in_a_group_count):
            students_list.append((f.name(), gr_id))

    # generate grades list
    grades_list = []
    for _ in students_list:
        for grade in range(10, randint(11, 20)):
            random_grade = randint(1, 5)
            valid_random_date = (datetime.now() - timedelta(days=randint(1, 120))).date()
            grades_list.append((random_grade, randint(1, len(students_list)),
                                randint(1, len(subjects)), valid_random_date))

    with db_connection(db_file_name) as connect:
        if connect is None:
            # print("Error! cannot create the database connection.")
            return 'Error! cannot create the database connection.'

        else:

            c = connect.cursor()
            try:
                for group in groups:
                    c.execute(sql_insert_data_groups, (group,))
                    print(f'Group {group} was inserted')
                print(f'Total {len(groups)} groups records were inserted')

                for professor in professors:
                    c.execute(sql_insert_data_professors, (professor,))
                    print(f'{professor} was inserted')
                print(f'Total {len(professors)} professors records were inserted')

                for subject in subjects:
                    c.execute(sql_insert_data_subjects, (subject, randint(1, len(professors))))
                    print(f'Subject {subject} was inserted')
                print(f'Total {len(subjects)} subjects records were inserted')

                c.executemany(sql_insert_data_students, students_list)
                print(f'Total {len(students_list)} students records were inserted')

                c.executemany(sql_insert_data_grades, grades_list)
                print(f'Total {len(grades_list)} grades records were inserted')

                connect.commit()
                # insert groups list
                # c.executemany(sql_insert_data_groups, groups_list)
                # print('Groups were inserted')
                # connect.commit()
                # c.executemany(sql_insert_data_students,)

            except Exception as e:
                print(e)
                connect.rollback()

    return 'Test data was inserted'


def show_data() -> str:
    print('Showing data...')

    return 'Data was shown'


def execute_all_sql():
    print('Executing all sql files...')

    return 'SQL files were executed'


def select_function(inp: str):
    inp = inp.lower()

    functions = {
        'c': create_db_tables,
        'i': insert_data,
        's': show_data,
        'h': print_commands,
        'q': execute_all_sql
    }

    if inp not in ['c', 'i', 's', 'h', 'q']:
        print('Wrong command!\n')
        return print_commands

    return functions.get(inp)


def print_commands():
    print('Data base interactive handler:')
    print('press letter and Enter, all other keys - exit')
    print('c - create all tables in db (after drop if tables already exist')
    print('i - insert test data to all tables in db')
    print('s - show data in all tables in db')
    print('q - execute all sql files in the SQL subdirectory')
    print('h - show available commands')
    print('x - exit')
    return 'Make you choice'


def main():
    print_commands()
    while True:
        command = input('Enter command: ')
        if not command or command == 'x':
            print('Bye!')
            break

        func = select_function(command)

        print(func())


if __name__ == '__main__':
    main()
