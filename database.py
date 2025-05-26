import sqlite3
import threading

class DataBaseManager:
    _instance = None
    _lock = threading.Lock()
    _local = threading.local()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DataBaseManager, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self):
        if not self._initialized:
            print("Inicializando clase DataBaseManager...")
            self._initialized = True
            # No inicializamos la conexión aquí, solo cuando se necesite
    
    def _get_connection(self):
        # Crear conexión por hilo si no existe
        if not hasattr(self._local, 'connection'):
            print(f"Creando conexión para hilo: {threading.current_thread().ident}")
            self._local.connection = sqlite3.connect('database.db')
        return self._local.connection
    
    def _get_cursor(self):
        return self._get_connection().cursor()
    
    def create_tables(self):
        cursor = self._get_cursor()
        users_table = """CREATE TABLE IF NOT EXISTS Usuarios(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Username VARCHAR(25) NOT NULL, 
            Email VARCHAR(100) NOT NULL, 
            Number VARCHAR(100) NOT NULL,
            Type VARCHAR(100) NOT NULL,
            Password VARCHAR(255) NOT NULL

        );"""

        
        medicamentos_table = """CREATE TABLE IF NOT EXISTS Medicamentos(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre VARCHAR(100) NOT NULL,
            Uso TEXT,
            Dosis TEXT,
            Categoria TEXT,
            Efectos_Secundarios TEXT,
            Recomendaciones_Alimenticias TEXT
        )"""

        recordatorios_table = """
            CREATE TABLE IF NOT EXISTS Recordatorios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                nombre TEXT NOT NULL,
                dia TEXT NOT NULL,          
                hora TEXT NOT NULL,       
                user_email TEXT NOT NULL,  
                FOREIGN KEY(paciente_id) REFERENCES Usuarios(id)
            );"""
        
        cursor.execute(users_table)
        cursor.execute(medicamentos_table)
        cursor.execute(recordatorios_table)

        self._get_connection().commit()
        print("Tablas creadas...")

    def create_user(self, username, email, password, number, type):
        cursor = self._get_cursor()
        cursor.execute("INSERT INTO Usuarios(Username, Email, Password, Number, Type) VALUES (?, ?, ?, ?, ?)", 
                    (username, email, password, number, type))
        self._get_connection().commit()
        cursor.execute("SELECT * FROM Usuarios WHERE Email=? AND Password=?", (email, password))
        return cursor.fetchone()
    
    def add_recordatorio(self, paciente_id, dia, hora, nombre, user_email):
        cursor = self._get_cursor()
        cursor.execute("INSERT INTO Recordatorios(paciente_id, nombre, dia,hora, user_email) VALUES (?,?,?,?,?)",
        (paciente_id, nombre, dia, hora, user_email))
        self._get_connection().commit()
        print("Añadido el recordatorio")
        
    def get_recordatorio_by_id(self, id_paciente):
        cursor = self._get_cursor()
        cursor.execute("SELECT dia, hora, nombre FROM Recordatorios WHERE paciente_id = ?", (id_paciente,))
        return cursor.fetchall()
    def get_recordatorios_por_fecha(self, fecha):
        cursor = self._get_cursor()
        cursor.execute("SELECT hora, nombre, user_email FROM Recordatorios WHERE dia = ?", (fecha,))
        return cursor.fetchall()
    def delete_recordatorio(self, dia, hora, nombre):
        cursor = self._get_cursor()
        cursor.execute("DELETE FROM Recordatorios WHERE dia = ? AND hora = ? AND nombre = ?", (dia, hora, nombre))
        self._get_connection().commit()
        return True
    
    def get_username_by_email(self, email):
        cursor = self._get_cursor()
        cursor.execute("SELECT Username FROM Usuarios WHERE Email = ?", (email, ))
        return cursor.fetchone()
    
    def add_medicamento(self, nombre, uso, dosis, categoria, efectos_secundarios, recomendaciones_alimenticias):
        cursor = self._get_cursor()
        cursor.execute("""
            INSERT INTO Medicamentos(
                Nombre, 
                Uso, 
                Dosis, 
                Categoria, 
                Efectos_Secundarios, 
                Recomendaciones_Alimenticias
            ) VALUES(?, ?, ?, ?, ?, ?)
        """, (nombre, uso, dosis, categoria, efectos_secundarios, recomendaciones_alimenticias))
        self._get_connection().commit()
        print(f"Medicamento '{nombre}' añadido correctamente...")
    
    def get_medicamento_by_name(self, nombre):
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM Medicamentos WHERE Nombre LIKE ?", ('%' + nombre + '%',))
        return cursor.fetchall()
        
    def get_medicamento_by_categoria(self, categoria):
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM Medicamentos WHERE Categoria LIKE ?", ('%' + categoria + '%',))
        return cursor.fetchall()
    def get_all_categorias(self):
        cursor = self._get_cursor()
        cursor.execute("""
            SELECT DISTINCT Categoria 
            FROM Medicamentos 
            WHERE Categoria IS NOT NULL 
            AND Categoria != ''
            ORDER BY Categoria
        """)
        categorias = cursor.fetchall()
        
        # Extraer solo los valores de la tupla y filtrar valores vacíos
        categorias_lista = [categoria[0] for categoria in categorias if categoria[0] and categoria[0].strip()]
        
        print(f"Se encontraron {len(categorias_lista)} categorías únicas...")
        return categorias_lista

    def login_user(self, email, password):
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM Usuarios WHERE Email=? AND Password=?", (email, password))
        return cursor.fetchone()


    def get_all_medicamentos(self):
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM Medicamentos")
        return cursor.fetchall()
    
    
    def delete_medicamento(self, id):
        cursor = self._get_cursor()
        cursor.execute("DELETE FROM Medicamentos WHERE Id=?", (id,))
        self._get_connection().commit()
        print(f"Medicamento ID {id} eliminado correctamente...")
    
    def close_connection(self):
        if hasattr(self._local, 'connection'):
            self._local.connection.close()
            delattr(self._local, 'connection')
            print("Conexión a la base de datos cerrada...")

    def get_usuario(self, usuario_id):
        cursor = self._get_cursor()

        # Obtener info del usuario
        cursor.execute("SELECT * FROM Usuarios WHERE Id=?", (usuario_id,))
        usuario_data = cursor.fetchone()
        if not usuario_data:
            return None

        # Crear diccionario de usuario 
        usuario = {
            "id": usuario_data[0],
            "nombre": usuario_data[1],
            "email": usuario_data[2],
            "telefono": usuario_data[5],  # Asumiendo que el teléfono está en la posición 4
            "tipo": usuario_data[4]       # Asumiendo que el tipo está en la posición 5
        }

        # Obtener medicamentos asociados
        cursor.execute("""
            SELECT nombre, dia, hora
            FROM Recordatorios
            WHERE paciente_id=?
        """, (usuario_id,))
        medicamentos = cursor.fetchall()

        # Convertir medicamentos a lista de diccionarios
        medicamentos_info = [
            {"Recordatorio": nombre, "Día": dia, "Hora del día": hora}
            for nombre, dia, hora in medicamentos
        ]

        # Agregar medicamentos al diccionario del usuario
        usuario["recordatorios"] = medicamentos_info

        return usuario


    def add_medicamento_usuario(self, paciente_id, nombre, dia, hora,ciclo):
        cursor = self._get_cursor()
        cursor.execute("""
            INSERT INTO Medicamentos_Usuarios(paciente_id, nombre, dia, hora,ciclo)
            VALUES (?, ?, ?, ?,?)
        """, (paciente_id, nombre, dia, hora, ciclo))
        self._get_connection().commit()
        print(f"Medicamento '{nombre}' asignado al paciente ID {paciente_id}")
        return 1
        

    def get_medicamento_usuario(self, paciente_id):
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM Medicamentos_Usuarios WHERE paciente_id = ?", (paciente_id,))
        return cursor.fetchall()
if __name__ == '__main__':
    db = DataBaseManager()
    db.create_tables()