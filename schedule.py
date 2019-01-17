from os.path import isfile
import sqlite3


def main():
    db_connection = sqlite3.connect("schedule.db")
    cursor = db_connection.cursor()
    x = 0
    sql_get_courses = """SELECT * FROM courses"""
    cursor.execute(sql_get_courses)
    list_of_courses = cursor.fetchall()

    while isfile("schedule.db") and len(list_of_courses) > 0:
        sql_get_classes = """SELECT * FROM classrooms"""
        cursor.execute(sql_get_classes)
        list_of_classes = cursor.fetchall()

        for currclass in list_of_classes:
            if currclass[3] == 0:
                sql_courses_by_id = """ SELECT * FROM courses WHERE class_id = ? """
                cursor.execute(sql_courses_by_id, (str(currclass[0])),)
                list_of_courses = cursor.fetchall()

                if len(list_of_courses) > 0:
                    print("(" + str(x) + ")" + " " + str(currclass[1]) + ":" + " " + str(list_of_courses[0][1]) +
                          " is schedule to start")

                    task1 = (list_of_courses[0][0], list_of_courses[0][5], currclass[0])
                    sql_update_classes = """UPDATE classrooms SET current_course_id=? , current_course_time_left=? 
                    WHERE id=?"""
                    cursor.execute(sql_update_classes, task1)
                    db_connection.commit()

                    task2 = (list_of_courses[0][3], list_of_courses[0][2])

                    sql_update_students = """UPDATE students SET count = count - ? WHERE grade = ? """
                    cursor.execute(sql_update_students, task2)
                    db_connection.commit()

            elif currclass[3] > 0 and currclass[2] != 0:

                task3 = (1, currclass[0])
                sql_update_class_time = """UPDATE classrooms SET current_course_time_left = current_course_time_left -? 
                WHERE id =?"""

                cursor.execute(sql_update_class_time, task3)
                db_connection.commit()

            cursor.execute(sql_get_classes)
            list_of_classes = cursor.fetchall()

        for currclass in list_of_classes:
            if currclass[3] == 0 and currclass[2] != 0:
                sql_get_name_by_id = """SELECT course_name FROM courses WHERE id = ?"""
                cursor.execute(sql_get_name_by_id, str(currclass[2]),)
                name1 = cursor.fetchall()

                print("(" + str(x) + ")" + " " + str(currclass[1]) + ":" + " " + str(name1[0][0]) + " is done")
                cursor.execute("DELETE FROM courses WHERE id =?", str(currclass[2]),)
                cursor.execute("SELECT * FROM courses WHERE class_id = ?", (str(currclass[0])),)
                list_of_courses = cursor.fetchall()
                if len(list_of_courses) > 0:
                    print("(" + str(x) + ")" + " " + str(currclass[1]) + ":" + " " + str(list_of_courses[0][1]) +
                             " is schedule to start")
                    task4 = (list_of_courses[0][0], list_of_courses[0][5], currclass[0])
                    cursor.execute(sql_update_classes, task4)
                    db_connection.commit()

                    task5 = (list_of_courses[0][3], list_of_courses[0][2])
                    cursor.execute(sql_update_students, task5)
                    db_connection.commit()

                else:
                    query = """UPDATE classrooms SET current_course_id = 0 
                    WHERE id =?"""
                    cursor.execute(query, str(currclass[0]))
                    db_connection.commit()

            else:
                cursor.execute("SELECT course_length FROM courses WHERE id =?", (str(currclass[2])),)
                time = cursor.fetchone()
                if time is not None:
                    if time[0] != currclass[3] and time[0] != 0:
                        cursor.execute("SELECT course_name FROM courses WHERE id =?", (str(currclass[2])),)
                        name1 = cursor.fetchall()
                        print("(" + str(x) + ")" + " " + str(currclass[1]) + ":" + " occupied by " + str(
                            name1[0][0]))

        x = x + 1

        cursor.execute("SELECT * FROM courses")
        list_of_courses = cursor.fetchall()
        print_table(list_of_courses, "courses")

        cursor.execute("SELECT * FROM classrooms")
        list_of_classes = cursor.fetchall()
        print_table(list_of_classes, "classrooms")

        cursor.execute("SELECT * FROM students")
        list_of_students = cursor.fetchall()
        print_table(list_of_students, "students")

    db_connection.commit()


def print_table(table, name):
    print(name)
    for item in table:
        print(item)


if __name__ == '__main__':
    main()
