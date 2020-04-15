import sqlite3
import uuid


conn = sqlite3.connect('TestDB.db')
c = conn.cursor()


def book_room(room_id: str, time_begin, time_end, booker_id: str, num_people: int):
    """
    Бронирует комнату с указанными данными
    """
    if room_id in recommend(time_begin, time_end, num_people):
        c.execute('INSERT INTO Booking VALUES (%s, %s, %s, %s, %s, %d)' %
                  (str(uuid.uuid4()), room_id, time_begin, time_end, booker_id, num_people))



def recommend(desired_begin, desired_end, num_people: int):
    """
    Рекомендует комнату с учётом желаемого времени и количества людей
    Возвращает комнаты:
    1. В которых достаточно места
    2. Которые свободны на всё время бронирования
    """
    c.execute('SELECT Room.id '
              'FROM Room EXCEPT '
              'SELECT r.id '
              'FROM Room AS r INNER JOIN Booking AS b '
              'ON r.id = b.room_id '
              'WHERE r.num_seats < %d AND '
              '((%s BETWEEN b.time_begin AND b.time_end)'
              'OR (%s BETWEEN b.time_begin AND b.time_end)'
              'OR (%s < time_begin AND %s > time_end))' %
              (num_people, desired_begin, desired_end, desired_begin, desired_end))
    return c.fetchall()


def get_users():
    c.execute('SELECT User.id from User')
    return c.fetchall()


def user_valid(sign_in_id: str):
    if sign_in_id in get_users():
        return True
    return False


def main():
    print('Write your user id')
    cur_user_id = -1
    while True:
        sign_in_id = input()
        if user_valid(sign_in_id):
            cur_user_id = sign_in_id
            break
    if cur_user_id == -1:
        return 0
    while True:
        command = input().split(' ')
        if command[0] == 'exit':
            break
        if command[0] == 'recommend':
            recommend(command[1], command[2], int(command[3]))
        if command[0] == 'book':
            book_room(command[1], command[2], command[3], cur_user_id, int(command[4]))


if __name__ == '__main__':
    main()
