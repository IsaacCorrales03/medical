import sqlite3



class DataBaseManager:
    def __init__(self):
        print("Iniciando base de datos...")
        self.my_connection = sqlite3.connect('database.db')
        self.my_cursor = self.my_connection.cursor()
        self.create_tables()
    
    def create_tables(self):
        users_table = """CREATE TABLE IF NOT EXISTS Usuarios(Id INTEGER PRIMARY KEY AUTOINCREMENT,  Username VARCHAR(25) NOT NULL, Email VARCHAR(100) NOT NULL, Password VARCHAR(255) NOT NULL)"""
        self.my_cursor.execute(users_table)
        self.my_connection.commit()
        print("Tablas creadas...")

    
    def create_user(self, username, email, password):
        self.my_cursor.execute("INSERT INTO Usuarios(Username, Email, Password) VALUES(?, ?, ?)", (username, email, password))
        self.my_connection.commit()
        print("Usuario creado...")
