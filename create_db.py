import sqlite3


# TODO: need to figure out why <NOT> NULL does not compile
def main():
    # if db does not exists it will be created
    dbcon = sqlite3.connect("classes.db")
    with dbcon:
        cursor = dbcon.cursor()
        sql_create_students = """ CREATE TABLE IF NOT EXISTS
                              Students(grade TEXT PRIMARY KEY,
                              count INTEGER NOT NULL);"""

        sql_create_courses = """CREATE TABLE IF NOT EXISTS
                            courses (id INTEGER PRIMARY KEY,
                            course_name TEXT NOT NULL,
                            student TEXT NOT NULL,
                            number_of_students INTEGER NOT NULL)"""

        sql_create_classrooms = """CREATE TABLE IF NOT EXISTS
                                classrooms(id INTEGER PRIMARY KEY,
                                location TEXT NOT NULL,
                                current_course_id INTEGER NOT NULL,
                                current_course_time_left INTEGER NOT NULL)"""
        cursor.execute(sql_create_classrooms)
        cursor.execute(sql_create_courses)
        cursor.execute(sql_create_students)


if __name__ == '__main__':
    main()
