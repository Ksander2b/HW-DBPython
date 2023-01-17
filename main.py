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


def _find_client_by_name(conn, first_name):
    with conn.cursor() as cur:
        cur.execute('''
        SELECT c.name, c.surname, c.email, p.phone FROM Clients c
        JOIN Clients_phones cp ON c.id = cp.client_id
        JOIN Phones p ON cp.phone_id = p.id
        WHERE c.name = %s;''',
        (first_name, ))
        return print(cur.fetchone())

def _find_client_by_surname(conn, last_name):
    with conn.cursor() as cur:
        cur.execute(
            '''SELECT c.name, c.surname, c.email, p.phone FROM Clients c
            JOIN Clients_phones cp ON c.id = cp.client_id
            JOIN Phones p ON cp.phone_id = p.id
            WHERE c.surname = %s;''',
            (last_name, ))
        return print(cur.fetchone())

def _find_client_by_email(conn, email):
    with conn.cursor() as cur:
        cur.execute(
            '''SELECT c.name, c.surname, c.email, p.phone FROM Clients c
            JOIN Clients_phones cp ON c.id = cp.client_id
            JOIN Phones p ON cp.phone_id = p.id
            WHERE c.email = %s;''',
            (email, ))
        return print(cur.fetchone())

def _find_client_by_phone(conn, phone):
    with conn.cursor() as cur:
        cur.execute('''
        SELECT c.name, c.surname, c.email, p.phone FROM Clients c
        JOIN Clients_phones cp ON c.id = cp.client_id
        JOIN Phones p ON cp.phone_id = p.id
        WHERE p.phone = %s;''',
        (phone, ))
        return print(cur.fetchone())
            

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    if first_name != None:
        _find_client_by_name(conn, first_name)
    if last_name != None:
        _find_client_by_surname(conn, last_name)
    if email != None:
        _find_client_by_email(conn, email)
    if phone != None: 
        _find_client_by_phone(conn, phone)

        


    pass

if __name__ == '__main__':
    conn = psycopg2.connect(database = 'client_management', user = 'postgres', password = 'Fozeqwxu23')
    # create_db(conn)
    # add_client(conn,'Alex', 'Bogatyrev', 'ssss@kfd.com', '+79250466002')
    # add_client(conn,'Ann', 'Chernavina', 'anchem@jdf.com', '+7945900456')
    # add_phone(conn, '+7945678456', '2')
    # change_client(conn,'2', 'Anncher', 'Cher', 'anchem@jdf.com', '+7000000000')
    # delete_phone (conn, '+7000000000')
    # delete_client(conn, 1)
    find_client(conn, 'Сher')
