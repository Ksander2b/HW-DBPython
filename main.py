import psycopg2


def create_db(cur):
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS Clients
        (id SERIAL PRIMARY KEY, 
        name VARCHAR NOT NULL, 
        surname VARCHAR NOT NULL, 
        email VARCHAR NOT NULL);'''
        )
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS Phones
        (id SERIAL PRIMARY KEY, 
        phone VARCHAR NOT NULL,
        client_id INTEGER REFERENCES Clients(id));'''
        )
    conn.commit()
    pass


def add_client(cur, first_name, last_name, email, phones=None):
    cur.execute(
        '''INSERT INTO Clients(name, surname, email) 
        VALUES(%s, %s, %s);''', 
        (first_name, last_name, email, )
        )
    cur.execute(
        '''INSERT INTO Phones(phone, client_id)
        VALUES (%s, (SELECT id FROM Clients WHERE name = %s));''',
        (phones,first_name, )
        )
    conn.commit()
    pass


def add_phone(cur, phone, client_id):
    cur.execute(
        '''INSERT INTO Phones (phone)
        VALUES(%s, %s);''',
        (phone, client_id, )
        )
    conn.commit()
    pass


def change_client(cur):
    client_id = input('Введите id клиента, данные которого хотите поменять: ')
    ans_1= input('Введите один тип данных клиента, который хотите поменять (имя, фамилия, email или телефон): ')
    if ans_1 == 'имя':
        ans_2 = input('Напишите новое имя для выбраного клиента: ')
        cur.execute(
            '''UPDATE Clients
            SET name = %s
            WHERE id = %s;''',
            (ans_2, client_id, )
            )
    if ans_1 == 'фамилия':
        ans_3 = input('Напишите новую фамилию для выбраного клиента: ')
        cur.execute(
            '''UPDATE Clients
            SET surname = %s
            WHERE id = %s;''',
            (ans_3, client_id, )
            )
    if ans_1 == 'email':
        ans_4 = input('Напишите новвый email для выбраного клиента: ')
        cur.execute(
            '''UPDATE Clients
            SET email = %s
            WHERE id = %s;''',
            (ans_4, client_id, )
            )
    if ans_1 == 'телефон':
        ans_5 = input('Напишите новый телефон для выбраного клиента: ')
        cur.execute(
            '''UPDATE Phones
            SET phone = %s
            WHERE client_id = %s;''',
            (ans_5, client_id, )
            )
    conn.commit()
    pass


def delete_phone(cur, phone):
    cur.execute(
        '''DELETE FROM Phones 
        WHERE phone = %s;''',
        (phone, )
        )
    conn.commit()
    pass


def delete_client(cur, client_id):
    cur.execute(
        '''DELETE FROM Phones 
        WHERE client_id = %s;''',
        (client_id, )
        )
    cur.execute(
        '''DELETE FROM Clients 
        WHERE id = %s;''',
        (client_id, )
        )
    conn.commit()
    pass
            

def find_client(cur, data):
    cur.execute(
        '''SELECT c.name, c.surname, c.email, p.phone FROM Clients c
        JOIN Phones p ON c.id = p.client_id
        WHERE c.name = %s;''',
        (data, )
        )
    result = cur.fetchall()
    if len(result) > 0:
        print(result)
    cur.execute(
        '''SELECT c.name, c.surname, c.email, p.phone FROM Clients c
        JOIN Phones p ON c.id = p.client_id
        WHERE c.surname = %s;''',
        (data, )
        )
    result = cur.fetchall()
    if len(result) > 0:
        print(result)
    cur.execute(
        '''SELECT c.name, c.surname, c.email, p.phone FROM Clients c
        JOIN Phones p ON c.id = p.client_id
        WHERE c.email = %s;''',
        (data, )
        )
    result = cur.fetchall()
    if len(result) > 0:
        print(result)
    cur.execute(
        '''SELECT c.name, c.surname, c.email, p.phone FROM Clients c
        JOIN Phones p ON c.id = p.client_id
        WHERE p.phone = %s;''',
        (data, )
        )
    result = cur.fetchall()
    if len(result) > 0:
        print(result)
    pass

if __name__ == '__main__':
   with psycopg2.connect(database = 'client_management', user = 'postgres', password = 'postgres') as conn:
    with conn.cursor() as cur:
        create_db(cur)
        add_client(cur, 'Alex', 'Bogatyrev', 'a.bogatyrev@gmail.com', '+79350466002')
        add_client(cur, 'Paha', 'Bogatyrev', 'p.bogatyrev@gmail.com', '+70000099999')
        add_client(cur, 'Ann', 'Mancher', 'ancher.mancher@fdfd.com', '+72341234232')
        add_client(cur, 'Artiom', 'Bessudnov', 'a.bessudnov@gmail.com', '+79999999990')
        find_client(cur, 'ancher.mancher@fdfd.com')
        find_client(cur, 'Bogatyrev')
        find_client(cur, 'Artiom')
        find_client(cur, '+79999999990')
        change_client(cur)

        




