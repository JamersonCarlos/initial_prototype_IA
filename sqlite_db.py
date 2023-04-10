import _sqlite3

class SqliteDB:
    def __init__(self):
        self.conn = _sqlite3.connect('database.db',check_same_thread=False)
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (idUser TEXT, id_notification TEXT)
        """)
        cursor.close()
        

    def casdastrar_novo_user(self, idUser, id_notification):
        cursor = self.conn.cursor()
        res = cursor.execute("""
        INSERT INTO users (idUser, id_notification) VALUES (?, ?)
        """, (idUser, id_notification))
        self.conn.commit()
        print('Registro inserido com sucesso.')
        cursor.close()
        return True if res else False
     