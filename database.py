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

        mensajes_table = """CREATE TABLE IF NOT EXISTS Mensajes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenido TEXT NOT NULL,
            usuario_id INTEGER NOT NULL,
            hora_envio DATETIME DEFAULT (datetime('now', '-6 hours')),
            FOREIGN KEY(usuario_id) REFERENCES Usuarios(Id)
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
        cursor.execute(mensajes_table)
        cursor.execute(medicamentos_table)
        cursor.execute(recordatorios_table)
        self._get_connection().commit()
    
    def get_all_messages(self):
        cursor = self._get_cursor() 
        query = """
            SELECT m.id, m.contenido, u.Username, u.Type, m.hora_envio, u.Id as usuario_id
            FROM Mensajes m
            INNER JOIN Usuarios u ON m.usuario_id = u.Id
            ORDER BY m.hora_envio ASC
        """
        cursor.execute(query)
        messages = cursor.fetchall()
        
        return [
            {
                'id': msg[0],
                'contenido': msg[1],
                'username': msg[2],
                'tipo_usuario': msg[3],
                'hora_envio': msg[4],
                'usuario_id': msg[5]
            }
            for msg in messages
        ]

    def create_message(self, contenido, usuario_id):
        cursor = self._get_cursor()
        
        # Insertar el mensaje
        cursor.execute(
            "INSERT INTO Mensajes (contenido, usuario_id) VALUES (?, ?)",
            (contenido, usuario_id)
        )
        self._get_connection().commit()
        
        # Obtener el ID del mensaje recién creado
        message_id = cursor.lastrowid
        
        # Obtener los datos completos del mensaje con información del usuario
        cursor.execute("""
            SELECT m.id, m.contenido, u.Username, u.Type, m.hora_envio, u.Id as usuario_id
            FROM Mensajes m
            INNER JOIN Usuarios u ON m.usuario_id = u.Id
            WHERE m.id = ?
        """, (message_id,))
        
        message_data = cursor.fetchone()
        
        if message_data:
            return {
                'id': message_data[0],
                'contenido': message_data[1],
                'username': message_data[2],
                'tipo_usuario': message_data[3],
                'hora_envio': message_data[4],
                'usuario_id': message_data[5]
            }
        
        return None

    def create_user(self, username, email, password, number, type):
        cursor = self._get_cursor()
        cursor.execute("INSERT INTO Usuarios(Username, Email, Password, Number, Type) VALUES (?, ?, ?, ?, ?)", 
                    (username, email, password, number, type))
        self._get_connection().commit()
        cursor.execute("SELECT * FROM Usuarios WHERE Email=? AND Password=?", (email, password))
        return cursor.fetchone()

    def change_password(self, email, new_password):
        cursor = self._get_cursor()
        cursor.execute("UPDATE usuarios SET password = ? WHERE email = ?", (new_password, email))
        self._get_connection().commit()
        print(new_password)
        cursor.close()

    def add_recordatorio(self, paciente_id, dia, hora, nombre, user_email):
        cursor = self._get_cursor()
        cursor.execute("INSERT INTO Recordatorios(paciente_id, nombre, dia,hora, user_email) VALUES (?,?,?,?,?)",
        (paciente_id, nombre, dia, hora, user_email))
        self._get_connection().commit()
        print("Añadido el recordatorio")
        
    def get_recordatorio_by_id(self, id_paciente):
        cursor = self._get_cursor()
        cursor.execute("SELECT dia, hora, nombre, id FROM Recordatorios WHERE paciente_id = ?", (id_paciente,))
        return cursor.fetchall()
    
    def get_recordatorios_por_fecha(self, fecha):
        cursor = self._get_cursor()
        cursor.execute("SELECT hora, nombre, user_email FROM Recordatorios WHERE dia = ?", (fecha,))
        return cursor.fetchall()
    
    def delete_recordatorio_by_id(self, id):
        try:
            print(f"[DB] Conectando a la base de datos para eliminar ID: {id}")
            cursor = self._get_cursor()
            cursor.execute("DELETE FROM Recordatorios WHERE id = ?", (id,))
            self._get_connection().commit()
            print(f"[DB] Recordatorio con ID {id} eliminado con éxito.")
        except Exception as e:
            print(f"[DB] Error al eliminar recordatorio con ID {id}: {e}")
            raise

    
    def delete_recordatorio(self, dia, hora, nombre):
        cursor = self._get_cursor()
        cursor.execute("DELETE FROM Recordatorios WHERE dia = ? AND hora = ? AND nombre = ?", (dia, hora, nombre))
        self._get_connection().commit()
        return True
    
    def get_username_by_email(self, email):
        cursor = self._get_cursor()
        cursor.execute("SELECT Username FROM Usuarios WHERE Email = ?", (email, ))
        return cursor.fetchone()
    def get_user_by_email(self, email):
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM Usuarios WHERE Email = ?", (email, ))
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
            "telefono": usuario_data[3],  # Asumiendo que el teléfono está en la posición 4
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