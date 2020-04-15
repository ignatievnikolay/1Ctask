import sqlite3
import uuid


conn = sqlite3.connect('1Ctask.db')
c = conn.cursor()


def book_room(room_id: str, time_begin, time_end, booker_id: str, num_people: int):
    """
    Бронирует комнату с указанными данными (создаёт соответствующую запись в таблице Booking в базе данных)
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

    Как проверяется, подходит комната или нет:
    1. Время начала и время конца не должны накладываться на уже существующую брони
    2. Уже существующая бронь не должна целиком содержаться в нашей брони
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
    return set(c.fetchall())


def get_users():
    """
    Возвращает множество айдищников пользователей
    """
    c.execute('SELECT User.id from User')
    return set(c.fetchall())


def user_valid(sign_in_id: str):
    """
    Возвращает TRUE, если польщователь с указанным sign_in_id существует
    FALSE, если не существует
    """
    if sign_in_id in get_users():
        return True
    return False


def add_user(name: str, surname: str):
    """
    Регистрирует нового пользователя в системе
    Добавляет в таблицу User в БД запись о пользователе
    Генерирует и возвращает уникальный id пользователя
    """
    user_id = str(uuid.uuid4())
    c.execute('INSERT INTO User '
              'VALUES (%s, %s, %s)' %
              (user_id, name, surname))
    return user_id


def main():
    cur_user_id = -1
    print('sign_in or create user')
    while True:
        cmd = str(input()).split(' ')
        if cmd[0] == 'sign_in':
            if user_valid(sign_in_id=cmd[1]):
                cur_user_id = cmd[1]
                print('successfully signed in')
                break
        if cmd[0] == 'create':
            new_user_id = add_user(name=cmd[1], surname=cmd[2])
            print('your user id is:', new_user_id)
    if cur_user_id == -1:
        return 0

    while True:
        cmd = input().split(' ')
        if cmd[0] == 'exit':
            break
        if cmd[0] == 'recommend':
            recommend(cmd[1], cmd[2], int(cmd[3]))
        if cmd[0] == 'book':
            book_room(cmd[1], cmd[2], cmd[3], cur_user_id, int(cmd[4]))


if __name__ == '__main__':
    main()
