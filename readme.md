# Sistema de Gestión de Medicamentos con Flask

Este proyecto consiste en una aplicación web desarrollada con Flask que permite la gestión de medicamentos, interacciones entre ellos, y alarmas para recordatorios de toma de medicación.

![Estructura del Proyecto](https://raw.githubusercontent.com/IsaacCorrales03/medical/refs/heads/main/estructura.jpg)

## Estructura del Proyecto

El proyecto está organizado en carpetas para separar el código del servidor, la base de datos, y los recursos estáticos:

- `app.py`: Archivo principal de Flask
- `database.py`: Gestor de base de datos
- `database.db`: Base de datos SQLite
- `static/`: Archivos estáticos (CSS, JS, imágenes)
- `templates/`: Plantillas HTML con Jinja2

## Explicación del Código
## Archivo Principal (app.py)

```python
from flask import * 
from database import DataBaseManager
app = Flask("__main__")
app.static_folder = 'static'

my_db = DataBaseManager()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        pass
        # lógica para el inicio de sesión 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        pass
        # lógica de registro

@app.route('/medicamentos', methods=['GET'])
def medicamentos():
    if request.args:
        name = request.args.get('name')
        medicamentos = my_db.get_medicamento_by_name(name)
    else:
        medicamentos = my_db.get_all_medicamentos()
    return render_template('medicamentos.html', medicamentos=medicamentos)

app.run(port=1010, debug=True)
```

Este archivo es el punto de entrada de la aplicación Flask. Define cuatro rutas principales:

- **/** - La página de inicio que renderiza `index.html`
- **/login** - Maneja tanto la visualización del formulario de inicio de sesión (GET) como el procesamiento del formulario enviado (POST)
- **/register** - Similar a login, maneja la visualización y procesamiento del formulario de registro
- **/medicamentos** - Muestra todos los medicamentos o permite filtrar por nombre mediante un parámetro de consulta

El servidor se ejecuta en el puerto 1010 con el modo de depuración activado.

## Gestión de calendario (medicamentos.js)

## Descripción General

Este archivo JavaScript implementa un calendario interactivo para visualizar y gestionar medicamentos programados. El calendario muestra el mes actual, resalta el día de hoy y marca visualmente los días que tienen medicamentos asignados, permitiendo al usuario ver detalles al pasar el cursor por encima.

## Estructura y Funcionalidades Principales

### Inicialización y Carga de Datos

```javascript
document.addEventListener('DOMContentLoaded', function () {
    // Código de inicialización...
    fetch('/get_medication')
        .then(response => response.json())
        .then(medications => {
            generateCalendarWithMedications(today, medications);
        })
        .catch(error => {
            generateCalendar(today);
        });
});
```

- **Evento DOMContentLoaded**: Asegura que el código se ejecute después de que la página haya cargado completamente
- **Visualización del Mes**: Muestra el mes y año actual en español (ej. "Mayo 2025")
- **Carga de Medicamentos**: Realiza una petición AJAX para obtener los medicamentos del usuario
- **Manejo de Errores**: Si falla la carga de medicamentos, genera un calendario básico sin ellos

### Generación del Calendario con Medicamentos

```javascript
function generateCalendarWithMedications(date, medications) {
    // Código para generar el calendario con medicamentos...
}
```

Esta función:

1. **Calcula la Estructura del Mes**:
   - Determina el primer día del mes y su posición en la semana
   - Calcula el número total de días en el mes

2. **Genera las Celdas del Calendario**:
   - Crea celdas vacías para los días antes del inicio del mes
   - Genera una celda para cada día del mes

3. **Procesamiento de Medicamentos**:
   - Para cada día, determina qué medicamentos deben mostrarse según su frecuencia:
     - `diario`: Se muestra todos los días
     - `semanal`: Se muestra en días específicos de la semana
     - `mensual`: Se muestra en días específicos del mes
     - `varias_veces`: Se muestra todos los días

4. **Visualización de Días con Medicamentos**:
   - Añade un indicador visual (punto rojo) a los días con medicamentos
   - Aplica un borde rojo a estos días
   - Crea un tooltip que muestra al pasar el cursor:
     - Nombre del medicamento
     - Dosis
     - Hora de administración

### Versión Básica del Calendario

```javascript
function generateCalendar(date) {
    // Código para generar un calendario básico...
}
```

- Versión simplificada del calendario sin información de medicamentos
- Se utiliza como fallback si falla la carga de datos de medicamentos
- Mantiene la misma estructura visual básica

### Modal para Añadir Medicamentos

El código implementa un sistema modal para añadir nuevos medicamentos:

```javascript
// Modal functionality
const addMedicationBtn = document.getElementById('addMedicationBtn');
const medicationModal = document.getElementById('medicationModal');
// Más código del modal...
```

1. **Control de Visibilidad**:
   - Muestra el modal al hacer clic en el botón "Añadir Medicamento"
   - Oculta el modal al hacer clic en el botón de cierre o fuera del contenido

2. **Funcionalidad Dinámica**:
   - Muestra u oculta el selector de día dependiendo del ciclo seleccionado
   - Si se selecciona ciclo "semanal", se muestra el selector de día específico

3. **Envío del Formulario**:
   - Intercepta el envío del formulario para usar AJAX
   - Envía los datos al endpoint `/add_medication` mediante POST
   - Procesa la respuesta:
     - Muestra mensaje de éxito y recarga la página si todo va bien
     - Muestra mensaje de error si algo falla

## Aspectos Visuales

- Utiliza clases de **Tailwind CSS** para estilizar elementos
- Días con medicamentos:
  - Tienen borde rojo (`border-red-300`)
  - Muestran un indicador (punto rojo)
- Día actual:
  - Resaltado con fondo azul claro (`bg-blue-100`)
- Tooltips:
  - Aparecen al pasar el cursor sobre días con medicamentos
  - Contienen información detallada sobre cada medicamento
  - Incluyen una flecha visual que apunta al día

## Interacciones del Usuario

- **Visualización de Información**: Pasar el cursor sobre días con medicamentos muestra detalles
- **Añadir Medicamentos**: Abrir modal → Rellenar formulario → Enviar datos
- **Ciclo de Medicamentos**: Cambiar el tipo de ciclo muestra u oculta opciones relevantes

## Dependencias

- Requiere elementos HTML con IDs específicos:
  - `currentMonth`: Para mostrar el mes y año actual
  - `calendarDays`: Contenedor para las celdas del calendario
  - `addMedicationBtn`: Botón para abrir el modal
  - `medicationModal`: El modal en sí
  - `closeModalBtn`: Botón para cerrar el modal
  - `cicloSelect`: Selector de tipo de ciclo
  - `diaContainer`: Contenedor para el selector de día
  - `medicationForm`: Formulario para añadir medicamentos

# DataBaseManager

## Descripción General

`DataBaseManager` es una implementación de gestión de base de datos SQLite que utiliza el patrón Singleton con seguridad para múltiples hilos. Esta implementación garantiza que las conexiones a la base de datos se manejen correctamente en entornos multi-hilo, evitando problemas de concurrencia.

## Características Principales

### Patrón Singleton Thread-Safe
- Mantiene una única instancia de la clase a nivel de aplicación
- Proporciona conexiones independientes para cada hilo
- Utiliza bloqueos para evitar condiciones de carrera durante la inicialización

### Gestión de Conexiones
- Inicialización perezosa: las conexiones se crean solo cuando son necesarias
- Cada hilo obtiene su propia conexión aislada
- Cierre explícito de conexiones para liberar recursos

### Estructura de la Base de Datos
La clase gestiona tres tablas principales:

1. **Usuarios**:
   - `Id`: Identificador único autoincremental
   - `Username`: Nombre de usuario (limitado a 25 caracteres)
   - `Email`: Correo electrónico (limitado a 100 caracteres)
   - `Number`: Número telefónico (limitado a 100 caracteres)
   - `Type`: Tipo de usuario (limitado a 100 caracteres)
   - `Password`: Contraseña almacenada (hasta 255 caracteres)

2. **Medicamentos**:
   - `Id`: Identificador único autoincremental
   - `Nombre`: Nombre del medicamento
   - `Uso`: Descripción del uso terapéutico
   - `Dosis`: Información sobre la posología
   - `Efectos_Secundarios`: Posibles efectos adversos
   - `Recomendaciones_Alimenticias`: Consejos sobre alimentación relacionados con el medicamento

3. **Medicamentos_Usuarios**:
   - `id`: Identificador único autoincremental
   - `paciente_id`: Clave foránea referenciando al ID del usuario
   - `nombre`: Nombre del medicamento asignado
   - `dia`: Día para tomar el medicamento
   - `hora`: Hora para tomar el medicamento
   - `ciclo`: Ciclo de administración del medicamento

## Métodos Disponibles

### Gestión de Usuarios
- `create_user(username, email, password, number, type)`: Registra un nuevo usuario en la base de datos
- `login_user(email, password)`: Autentica un usuario existente
- `get_usuario(usuario_id)`: Obtiene información de un usuario y sus medicamentos asignados

### Gestión de Medicamentos
- `add_medicamento(nombre, uso, dosis, efectos_secundarios, recomendaciones_alimenticias)`: Añade un nuevo medicamento
- `get_medicamento_by_name(nombre)`: Busca medicamentos que coincidan parcialmente con el nombre proporcionado
- `get_all_medicamentos()`: Obtiene todos los medicamentos almacenados
- `update_medicamento(id, nombre, uso, dosis, efectos_secundarios, recomendaciones_alimenticias)`: Actualiza la información de un medicamento existente
- `delete_medicamento(id)`: Elimina un medicamento de la base de datos

### Gestión de Medicamentos de Usuario
- `add_medicamento_usuario(paciente_id, nombre, dia, hora, ciclo)`: Asigna un medicamento a un usuario específico
- `get_medicamento_usuario(paciente_id)`: Obtiene los medicamentos asignados a un usuario

### Utilidades
- `create_tables()`: Crea las tablas necesarias si no existen
- `close_connection()`: Cierra la conexión del hilo actual a la base de datos

## Ejemplo de Uso

```python
# Crear instancia y tablas
db = DataBaseManager()
db.create_tables()

# Registrar un nuevo usuario
user = db.create_user("usuario1", "usuario1@ejemplo.com", "contraseña123", "123456789", "paciente")

# Añadir un medicamento a la base de datos
db.add_medicamento("Paracetamol", "Analgésico y antipirético", 
                  "500-1000mg cada 6-8 horas", 
                  "Náuseas, dolor abdominal en dosis altas", 
                  "No tomar con alcohol")

# Asignar un medicamento a un usuario
db.add_medicamento_usuario(1, "Paracetamol", "Lunes", "8:00", "Diario")

# Obtener información de un usuario con sus medicamentos
usuario_info = db.get_usuario(1)
```

## Notas de Implementación

- La implementación utiliza `threading.local()` para garantizar que cada hilo tenga su propia conexión.
- El patrón Singleton asegura que solo exista una instancia de `DataBaseManager` en toda la aplicación.
- Las conexiones se crean bajo demanda y se pueden cerrar explícitamente cuando no son necesarias.
## Ejemplo de Uso

```python
# Inicializar el gestor de base de datos
db = DataBaseManager()
db.create_tables()

# Añadir un medicamento
db.add_medicamento(
    nombre="Paracetamol",
    uso="Alivio del dolor y reducción de la fiebre.",
    dosis="500 mg cada 6 horas, no exceder 4 g al día.",
    efectos_secundarios="Raras veces, daño hepático en dosis altas.",
    recomendaciones_alimenticias="Puede tomarse con o sin alimentos."
)

# Buscar medicamentos por nombre
resultados = db.get_medicamento_by_name("Para")

# Cerrar la conexión cuando termine
db.close_connection()
```

## Front-end con Tailwind CSS

El proyecto utiliza Tailwind CSS como framework de diseño, lo que permite un desarrollo rápido y responsivo con clases de utilidad predefinidas. Esto facilita mantener un diseño coherente en toda la aplicación sin necesidad de escribir CSS personalizado extenso.

Los archivos de estilo se encuentran en la carpeta `static/styles/`, y se vinculan a las plantillas HTML.

## Plantillas con Jinja2

Las plantillas HTML utilizan el motor de plantillas Jinja2, que viene integrado con Flask. Esto permite:

- Extender plantillas base (layouts)
- Pasar datos desde Flask a las plantillas
- Uso de condicionales y bucles en el HTML
- Reutilización de componentes

## Métodos HTTP: GET y POST

- **GET**: Utilizado cuando el usuario accede a una página para visualizar información. Por ejemplo, al cargar el formulario de inicio de sesión o registro.
- **POST**: Utilizado cuando el usuario envía datos al servidor. Por ejemplo, al enviar credenciales de inicio de sesión o datos de registro.

En el código actual, la lógica para procesar los datos POST está pendiente de implementar.

## Base de Datos

Actualmente, el proyecto utiliza SQLite como sistema de gestión de base de datos, ideal para desarrollo y aplicaciones pequeñas a medianas. Hay planes de migrar a PostgreSQL en el futuro para mayor escalabilidad y funcionalidades avanzadas.

## Estado Actual del Proyecto



### Páginas Pendientes:
- ⏳ **Interacciones**: Análisis de interacciones entre medicamentos
- ⏳ **Blog**: Artículos informativos sobre salud y medicamentos
- ⏳ **Categorías**: Clasificación de medicamentos

## Enfoque del Proyecto

El proyecto ha priorizado el diseño y la experiencia de usuario, utilizando Tailwind CSS para lograr una interfaz atractiva y responsiva. 

El desarrollo del backend está en sus etapas iniciales, con la implementación básica de rutas y la estructura de la base de datos, pero con varios aspectos pendientes de completar como la autenticación de usuarios y la lógica de negocio para la gestión de medicamentos e interacciones.

La migración planeada de SQLite a PostgreSQL representa un paso hacia una aplicación más robusta y escalable, indicando la intención de evolucionar el proyecto hacia un sistema más completo y profesional.

## Como instalar
```bash
git clone "https://github.com/IsaacCorrales03/medical.git"
pip install -r requirements.txt
python server.py
```