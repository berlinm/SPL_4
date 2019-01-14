import sqlite3
import os.path
import sys

"""
this class is responsible to the creation of the db: establishes a connection to the db, creating tables, 
insertion to the tables
@Author: berlin
 """


def main():
    # if db does not exists it will be created
    if os.path.isfile("classes.db"):
        return
    db_connection = sqlite3.connect("classes.db")
    with db_connection:
        cursor = db_connection.cursor()
        sql_create_students = """ CREATE TABLE students(grade TEXT PRIMARY KEY,
                                  count INTEGER NOT NULL);"""

        sql_create_courses = """CREATE TABLE courses (id INTEGER PRIMARY KEY,
                            course_name TEXT NOT NULL,
                            student TEXT NOT NULL,
                            number_of_students INTEGER NOT NULL,
                            class_id INTEGER REFERENCES classrooms(id),
                            course_length INTEGER NOT NULL);"""

        sql_create_classrooms = """CREATE TABLE classrooms(id INTEGER PRIMARY KEY,
                                location TEXT NOT NULL,
                                current_course_id INTEGER NOT NULL,
                                current_course_time_left INTEGER NOT NULL);"""
        cursor.execute(sql_create_classrooms)
        cursor.execute(sql_create_courses)
        cursor.execute(sql_create_students)
        read_from_file(sys.argv[1], cursor)
        cursor.execute("SELECT * FROM courses")
        list_of_courses = cursor.fetchall()
        print_table(list_of_courses, "courses")

        cursor.execute("SELECT * FROM classrooms")
        list_of_classes = cursor.fetchall()
        print_table(list_of_classes, "classrooms")

        cursor.execute("SELECT * FROM students")
        list_of_students = cursor.fetchall()
        print_table(list_of_students, "students")


def print_table(table, name):
    print(name)
    for item in table:
        print(item)


def read_from_file(path_to_file, cursor):
    with open(path_to_file) as input_file:
        for line in input_file:
            if line[0] == 'R':
                insert_rooms(line[2:], cursor)
            elif line[0] == 'C':
                insert_course(line[2:], cursor)
            elif line[0] == 'S':
                insert_students(line[2:], cursor)


def insert_rooms(room, cursor):
    # assumes that room
    id, location = room.split(",")
    id = id.strip()
    location = location.strip()
    cursor.execute("""INSERT INTO classrooms
                    VALUES(?, ?, ?, ?)""", (id, location, 0, 0))


def insert_course(course, cursor):
    # assumes that course
    id, course_name, student, number_of_students, class_id, course_length = course.split(",")
    id = id.strip()
    course_name = course_name.strip()
    student = student.strip()
    number_of_students = number_of_students.strip()
    class_id = class_id.strip()
    course_length = course_length.strip()
    cursor.execute("""INSERT INTO courses
                    VALUES(?, ?, ?, ?, ?, ?)""",
                   (id, course_name, student, number_of_students, class_id, course_length))


def insert_students(student, cursor):
    # assumes that student
    grade, count = student.split(",")
    grade = grade.strip()
    count = count.strip()
    cursor.execute("""INSERT INTO students
                    VALUES(?, ?)""", (grade, count))


if __name__ == '__main__':
    main()
