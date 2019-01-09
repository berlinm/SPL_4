import create_db


def main():
    create_db.createdb()
    x = 0
    # needs to be replaced with the condition: database still exists & the courses table is empty
    while True:
        x = x + 1
        # foreach class, should check if it is free etc.


if __name__ == '__main__':
    main()
