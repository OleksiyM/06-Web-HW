import sqlite3
from contextlib import contextmanager
from random import randint
from datetime import datetime, timedelta
from faker import Faker

from constants import db_file_name, sql_create_students_table, sql_create_groups_table, \
    sql_create_professors_table, sql_create_subjects_table, sql_grades_table, \
    sql_insert_data_groups, sql_insert_data_students, sql_insert_data_subjects, \
    sql_insert_data_professors, sql_insert_data_grades, \
    students_in_a_group_count, groups, subjects, professors, table_list, groups_list

from constants import MIN_GRADE, MAX_GRADE, DAYS_DELTA


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
    tables_str = ', '.join(table_list)
    return f'DB was created with tables {tables_str}'


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
            random_grade = randint(MIN_GRADE, MAX_GRADE)
            random_student_id = randint(1, len(students_list))
            random_subject_id = randint(1, len(subjects))
            random_date = (datetime.now() -
                           timedelta(days=randint(1, DAYS_DELTA))).date()
            grades_list.append((random_grade, random_student_id,
                                random_subject_id, random_date))

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
                print(
                    f'Total {len(professors)} professors records were inserted')

                for subject in subjects:
                    c.execute(sql_insert_data_subjects,
                              (subject, randint(1, len(professors))))
                    print(f'Subject {subject} was inserted')
                print(f'Total {len(subjects)} subjects records were inserted')

                c.executemany(sql_insert_data_students, students_list)
                print(
                    f'Total {len(students_list)} students records were inserted')

                c.executemany(sql_insert_data_grades, grades_list)
                print(f'Total {len(grades_list)} grades records were inserted')

                connect.commit()
                # insert groups list
                # c.executemany(sql_insert_data_groups, groups_list)
                # print('Groups were inserted')
                # connect.commit()
                # c.executemany(sql_insert_data_students,)

            except Exception as e:
                print(f'Error: {e}')
                connect.rollback()
                return 'Error! cannot create the database connection.'
    tables_str = ', '.join(table_list)
    return f'Test data was inserted into tables {tables_str}'


def show_data() -> str:
    print('Showing data...')

    db_connection(db_file_name)
    with db_connection(db_file_name) as connect:
        if connect is None:
            return 'Error! cannot create the database connection.'

        else:
            c = connect.cursor()
            try:
                for base in table_list:
                    c.execute(f'select * from {base}')
                    print(f'\nTable {base}:')
                    print('-' * 50)
                    # print table header
                    for i in c.description:
                        print(f'{i[0]:<7}', end=' ')
                    print('', end='\n')
                    print('-' * 50)
                    for row in c.fetchall():
                        print(row)
                    # print(c.fetchall())
            except sqlite3.OperationalError as e:
                print(f'Error: {e}, create tables first.')
                return 'Error! cannot create the database connection.'

            except Exception as e:
                print(e)
                connect.close()
                connect.rollback()
    tables_str = ', '.join(table_list)
    return f'All data was shown in the tables {tables_str}'


def drop_all_tables():
    print('Dropping all tables...')

    db_connection(db_file_name)
    with db_connection(db_file_name) as connect:
        if connect is None:
            return 'Error! cannot create the database connection.'

        else:
            c = connect.cursor()
            try:
                for base in table_list:
                    c.execute(f'DROP TABLE {base}')
                    c.execute(f'VACUUM;')
                    print(f'Table {base} dropped.')
                    # print('-' * 50)
                connect.commit()
            except sqlite3.OperationalError as e:
                print(f'Error: {e}, create tables first.')
                return 'Error! cannot create the database connection.'

            except Exception as e:
                print(e)
                connect.close()
                connect.rollback()

    tables_str = ', '.join(table_list)
    return f'Tables were dropped: {tables_str}'


def execute_all_sql():
    print('Executing all sql files...')

    return 'SQL files were executed'


def select_function(inp: str):
    inp = inp.lower()

    functions = {
        'c': create_db_tables,
        'd': drop_all_tables,
        'i': insert_data,
        's': show_data,
        'h': print_commands,
        'q': execute_all_sql
    }

    if inp not in ['c', 'd', 'i', 's', 'h', 'q']:
        print('Wrong command!\n')
        return print_commands

    return functions.get(inp)


def print_commands():
    print('Data base interactive handler:')
    print('choose letter from and press Enter to confirm')
    print('c - create all tables in db, if tables not exist')
    print('d - drop all tables in db')
    print('i - insert test data to all tables in db')
    print('s - show all data in all tables in db')
    print('q - execute all sql files in the SQL subdirectory')
    print('h - show available commands (this list)')
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
