import sqlite3
from contextlib import contextmanager

db_file_name = './db.sqlite3'

students_in_a_group_count = 15
# random groups names
students_groups = ['group_1', 'group_2', 'group_3']

# random subjects
subjects = ['math', 'physics', 'chemistry', 'biology', 'history']

# random professors name
professors = ['Professor Emily Thompson', 'Professor William Smith', 'Professor Jessica Zhang',
              'Professor Charles Harris', 'Professor Nicole Wilson']

sql_create_students_table = """

"""

sql_create_groups_table = """

"""

sql_create_professors_table = """

"""

sql_create_subjects_table = """
"""

sql_grades_table = """

"""


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
            print("Error! cannot create the database connection.")
            return 'Error! cannot create the database connection.'

        else:
            # create students table
            create_table(connect, sql_create_students_table)

            # create groups table
            create_table(connect, sql_create_groups_table)

            # create professors table
            create_table(connect, sql_create_professors_table)

            # create subjects tabl
            create_table(connect, sql_create_subjects_table)

            # create grades table
            create_table(connect, sql_grades_table)

    return 'DB was created'


def drop_db() -> str:
    print('Dropping db...')

    return 'DB was dropped'


def insert_data() -> str:
    print('Inserting test data...')

    return 'Test data was inserted'


def show_data() -> str:
    print('Showing data...')

    return 'Data was shown'


def select_function(inp: str):
    inp = inp.lower()

    functions = {
        'c': create_db_tables,
        'd': drop_db,
        'i': insert_data,
        's': show_data,
        'h': print_commands
    }

    if inp not in ['c', 'd', 'i', 's', 'h']:
        print('Wrong command!\n')
        return print_commands

    return functions.get(inp)


def print_commands():
    print('Data base interactive handler:')
    print('press letter and Enter, all other keys - exit')
    print('c - create db')
    print('d - drop db')
    print('i - insert test data to db')
    print('s - show data in db')
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
