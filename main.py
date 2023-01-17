import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
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
            phone VARCHAR NOT NULL);'''
            )
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS Clients_phones
            (client_id INTEGER REFERENCES Clients(id),
            phone_id INTEGER REFERENCES Phones(id),
            CONSTRAINT cp PRIMARY KEY(client_id, phone_id));'''
            )
        conn.commit()
    pass


def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute(
            '''INSERT INTO Clients(name, surname, email) 
            VALUES(%s, %s, %s);''', 
            (first_name, last_name, email, )
            )
        cur.execute(
            '''INSERT INTO Phones(phone)
            VALUES (%s);''',
            (phones, )
            )
        cur.execute(
            '''INSERT INTO Clients_phones (client_id, phone_id)
            VALUES(
                (SELECT id FROM Clients WHERE name = %s),
                (SELECT id FROM Phones WHERE phone = %s)
                );''',
            (first_name, phones, )
            )
        conn.commit()
    pass


def add_phone(conn, phone, client_id):
    with conn.cursor() as cur:
        cur.execute(
            '''INSERT INTO Phones (phone)
            VALUES(%s);''',
            (phone, )
            )
        cur.execute(
            '''INSERT INTO Clients_phones(client_id, phone_id)
            VALUES(%s, (SELECT id FROM Phones WHERE phone = %s));''',
            (client_id, phone, )
            )
        conn.commit()
    pass


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        cur.execute(
            '''UPDATE Clients
            SET name = %s, surname = %s, email = %s
            WHERE id = %s;''',
            (first_name, last_name, email, client_id, )
            )
        cur.execute(
            '''UPDATE Phones
            SET phone = %s
            WHERE id = (
            SELECT ph.id FROM Phones ph
            JOIN Clients_phones cp ON ph.id = cp.phone_id
            JOIN Clients c ON cp.client_id = c.id
            WHERE c.id = %s
            LIMIT 1);''',
            (phones, client_id, )
            )
        conn.commit()
    pass


def delete_phone(conn, phone):
    with conn.cursor() as cur:
        cur.execute(
            '''DELETE FROM Clients_Phones
            WHERE phone_id = (
                SELECT cp.phone_id FROM Clients_Phones cp
                JOIN Phones p ON cp.phone_id = p.id
                WHERE p.phone = %s);''',
            (phone, )
            )
        cur.execute(
            '''DELETE FROM Phones 
            WHERE phone = %s;''',
            (phone, )
            )
        conn.commit()
    pass


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute(
            '''DELETE FROM Clients_Phones
            WHERE client_id = (
                SELECT cp.client_id FROM Clients_Phones cp
                JOIN Clients c ON cp.client_id = c.id
                WHERE c.id = %s);''',
                (client_id, )
                )
        cur.execute(
            '''DELETE FROM Clients 
            WHERE id = %s;''',
            (client_id, )
            )
        conn.commit()
    pass
            

def find_client(conn, data):
     with conn.cursor() as cur:
        cur.execute(
            '''SELECT c.name, c.surname, c.email, p.phone FROM Clients c
            JOIN Clients_phones cp ON c.id = cp.client_id
            JOIN Phones p ON cp.phone_id = p.id
            WHERE c.name = %s;''',
            (data, )
            )
        result = cur.fetchall()
        if len(result) > 0:
            print(result)
        cur.execute(
            '''SELECT c.name, c.surname, c.email, p.phone FROM Clients c
            JOIN Clients_phones cp ON c.id = cp.client_id
            JOIN Phones p ON cp.phone_id = p.id
            WHERE c.surname = %s;''',
            (data, )
            )
        result = cur.fetchall()
        if len(result) > 0:
            print(result)
        cur.execute(
            '''SELECT c.name, c.surname, c.email, p.phone FROM Clients c
            JOIN Clients_phones cp ON c.id = cp.client_id
            JOIN Phones p ON cp.phone_id = p.id
            WHERE c.email = %s;''',
            (data, )
            )
        result = cur.fetchall()
        if len(result) > 0:
            print(result)
        cur.execute(
            '''SELECT c.name, c.surname, c.email, p.phone FROM Clients c
            JOIN Clients_phones cp ON c.id = cp.client_id
            JOIN Phones p ON cp.phone_id = p.id
            WHERE p.phone = %s;''',
            (data, )
            )
        result = cur.fetchall()
        if len(result) > 0:
            print(result)
     pass

if __name__ == '__main__':
    conn = psycopg2.connect(database = 'client_management', user = 'postgres', password = '')
    
