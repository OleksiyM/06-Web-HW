import sqlite3
from contextlib import contextmanager
from random import randint
from datetime import datetime, timedelta
from faker import Faker

from constants import db_file_name, sql_create_students_table, sql_create_groups_table, \
    sql_create_professors_table, sql_create_subjects_table, sql_grades_table, \
    sql_insert_data_groups, sql_insert_data_students, sql_insert_data_subjects, \
    sql_insert_data_professors, sql_insert_data_grades, \
    students_in_a_group_count, groups, subjects, professors, tables_list, tables_str, groups_list

from constants import MIN_GRADE, MAX_GRADE, DAYS_DELTA


@contextmanager
def db_connection(db_file):
    connection = sqlite3.connect(db_file)
    yield connection
    connection.rollback()
    connection.close()


def execute_create_table_sql(connection, create_table_sql):
    try:
        c = connection.cursor()
        c.execute(create_table_sql)
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()


def create_db_tables() -> str:
    print('Creating db...')

    # db_connection(db_file_name)

    with db_connection(db_file_name) as connect:
        if connect is None:
            # print("Error! cannot create the database connection.")
            return 'Error! cannot create the database connection.'

        else:
            # create groups table
            execute_create_table_sql(connect, sql_create_groups_table)

            # create students table
            execute_create_table_sql(connect, sql_create_students_table)

            # create subjects table
            execute_create_table_sql(connect, sql_create_subjects_table)

            # create professors table
            execute_create_table_sql(connect, sql_create_professors_table)

            # create grades table
            execute_create_table_sql(connect, sql_grades_table)

    return f'DB was created with tables {tables_str}'


def insert_test_data_into_tables() -> str:
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

    return f'Test data was inserted into tables {tables_str}'


def show_data_from_all_tables() -> str:
    print('Showing data...')

    db_connection(db_file_name)
    with db_connection(db_file_name) as connect:
        if connect is None:
            return 'Error! cannot create the database connection.'

        else:
            c = connect.cursor()
            try:
                for base in tables_list:
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
                for base in tables_list:
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

    return f'Tables were dropped: {tables_str}'


def read_from_sql_file(task_number: int) -> str | None:
    # print(f'Executing sql file {num}')
    with open(f'./sql/query_{task_number}.sql', 'r') as f:
        sql_file = f.read()
    return sql_file if sql_file else None


def get_sql_task_description(task_number: int) -> str:
    messages = (
        'Find 5 students with the highest average score in all subjects.',
        'Find the student with the highest grade point average in a particular subject.',
        'Find the average score in groups for a particular subject.',
        'Find the average grade point average in a stream (across the entire grade table).',
        'Find what courses a certain teacher teaches.',
        'Find a list of students in a particular group.',
        'Find the grades of students in a particular group in a particular subject.',
        'Find the average grade given by a certain teacher in his/her subjects.',
        'Find the list of courses a student is taking.',
        'Find the list of courses taught by a certain teacher to a certain student.',
        'Bonus: The average grade that a certain teacher gives to a certain student.',
        'Bonus: Grades of students in a certain group in a certain subject in the last class.'
    )
    return messages[task_number]


def run_all_sql_scripts_from_directory():
    print('Executing all sql files...')
    for num in range(1, 13):
        print(f'#{num}: {get_sql_task_description(num - 1)}')
        sql_file = read_from_sql_file(num)
        if not sql_file:
            return f'Error! cannot read the sql file ./sql/query_{num}.sql.'
        print(f'{sql_file}')
        with db_connection(db_file_name) as connect:
            if connect is None:
                return 'Error! cannot create the database connection.'

            else:
                c = connect.cursor()
                try:
                    c.execute(sql_file)
                    print('-' * 50)
                    # print table header
                    for i in c.description:
                        print(f'{i[0]:<7}', end=' ')
                    print('', end='\n')
                    print('-' * 50)
                    for row in c.fetchall():
                        print(row)

                    print(f'SQL file ./sql/query_{num}.sql was executed')
                except Exception as e:
                    print(f'Error: {e}')
                    connect.rollback()
                    return 'Error! cannot create the database connection.'
        # connect.commit()
        connect.close()
        print('-' * 50)
    return 'SQL files were executed'


def select_function(inp: str):
    inp = inp.lower()

    functions = {
        'c': create_db_tables,
        'd': drop_all_tables,
        'i': insert_test_data_into_tables,
        's': show_data_from_all_tables,
        'h': print_commands,
        'q': run_all_sql_scripts_from_directory
    }

    if inp not in ['c', 'd', 'i', 's', 'h', 'q']:
        print('Wrong command!\n')
        return print_commands

    return functions.get(inp)


def print_commands():

    print('Data base interactive handler:')
    print('choose letter from and press Enter to confirm')
    print('c - Create database tables')
    print('d - Drop all database tables')
    print('i - Insert test data into tables')
    print('s - Show data from all tables')
    print('q - Execute all SQL files in the `SQL` subdirectory')
    print('h - Display this help menu')
    print('x - Exit the application')
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
