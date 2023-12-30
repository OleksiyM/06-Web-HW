db_file_name = './db.sqlite3'

MIN_GRADE = 1
MAX_GRADE = 5

DAYS_DELTA = 120

students_in_a_group_count = 15
# random groups names
groups = ('group_1', 'group_2', 'group_3')
groups_list = [('group_1',), ('group_2',), ('group_3',)]

# random subjects
subjects = ('math', 'physics', 'chemistry', 'biology', 'history')

# random professors name
professors = ('Professor Emily Thompson', 'Professor William Smith', 'Professor Jessica Zhang',
              'Professor Charles Harris', 'Professor Nicole Wilson')

sql_create_groups_table = """
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(50) NOT NULL
    );

"""

sql_create_students_table = """
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(50) NOT NULL,
    group_id INTEGER NOT NULL,
    FOREIGN KEY (group_id) REFERENCES groups (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    );
"""


sql_create_professors_table = """
CREATE TABLE IF NOT EXISTS professors (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(50) NOT NULL
    );
"""

sql_create_subjects_table = """
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(50) NOT NULL,
    professor_id INTEGER NOT NULL,
    FOREIGN KEY (professor_id) REFERENCES professors (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
    );
"""

sql_grades_table = """
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    grade INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE    
    );
"""
# Insert data SQL

sql_insert_data_groups = """
    INSERT INTO groups (name) VALUES (?);
"""

sql_insert_data_students = """
    INSERT INTO students (name, group_id) VALUES (?, ?);
"""

sql_insert_data_subjects = """
    INSERT INTO subjects (name, professor_id) VALUES (?, ?);
"""

sql_insert_data_professors = """
    INSERT INTO professors (name) VALUES (?);
"""

sql_insert_data_grades = """
    INSERT INTO grades (grade, student_id, subject_id, date) VALUES (?, ?, ?, ?);
"""
