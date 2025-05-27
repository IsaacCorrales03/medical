from flask import * 
from database import DataBaseManager
from flask_mail import Message, Mail
from dotenv import load_dotenv
from reminder import Reminder
import os
import random
import string

load_dotenv()

verification_codes = {}

app = Flask("__main__")
reminder_system = Reminder()

app.static_folder = 'static'

# Configuración desde variables de entorno
app.secret_key = os.getenv('SECRET_KEY')

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT')) 
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)


url_service = ''

@app.route('/email')
def enviar_correo():
    tipo = request.args.get('tipo')  # novedades, suscripcion, medicamento, password_code
    correo_destinatario = request.args.get('correo')
    
    if tipo == 'novedades':
        if not correo_destinatario:
            return "Falta el parámetro 'correo' para novedades.", 400

        html_content = render_template('correo_novedades.html')
        asunto = '¡Novedades de Meditime!'

    elif tipo == 'suscripcion':
        if not correo_destinatario:
            return "Falta el parámetro 'correo' para aviso de suscripción.", 400

        html_content = render_template('correo_suscripcion.html')
        asunto = '¡Gracias por suscribirte a Meditime!'

    elif tipo == 'recordatorio':
        nombre = request.args.get('nombre')
        hora = request.args.get('hora')
        user_email = correo_destinatario
        nombre_usuario = my_db.get_username_by_email(user_email)[0]
        print(nombre_usuario)
        
        # Validar que todos los campos requeridos estén presentes
        if not nombre:
            return jsonify({'error': 'El campo nombre es requerido'}), 400
        
        if not hora:
            return jsonify({'error': 'El campo hora es requerido'}), 400
        
        if not user_email:
            return jsonify({'error': 'El campo user_email es requerido'}), 400

        html_content = render_template(
            'correo_recordatorio.html',
            hora=hora,
            nombre_usuario=nombre_usuario,
            medicamento=nombre,
            url_service=url_service
        )
        asunto = 'Recordatorio de Medicación'
    
    elif tipo == 'password_code':
        codigo = request.args.get('codigo')
        
        if not correo_destinatario:
            return "Falta el parámetro 'correo' para código de verificación.", 400
        
        if not codigo:
            return "Falta el parámetro 'codigo' para código de verificación.", 400

        html_content = render_template(
            'correo_password_code.html',
            codigo=codigo
        )
        asunto = 'Código de Verificación - Meditime'
    
    else:
        return "Tipo de correo no válido. Usa 'novedades', 'suscripcion', 'recordatorio' o 'password_code'.", 400
    
    # Enviar correo
    msg = Message(asunto,
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[correo_destinatario])
    msg.html = html_content
    mail.send(msg)

    return {"Success": True}

my_db = DataBaseManager()
my_db.create_tables()
@app.route('/')
def index():
    categorias = my_db.get_all_categorias()
    return render_template("index.html", categorias=categorias)


import random
import string
from flask import request, render_template, redirect, url_for, flash, session

# Diccionario temporal para almacenar códigos de verificación
verification_codes = {}

def generate_verification_code():
    """Genera un código de verificación de 6 dígitos"""
    return ''.join(random.choices(string.digits, k=6))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('forgot_password.html')
    
    elif request.method == 'POST':
        email = request.form.get('email')
        
        if not email:
            flash('El campo email es requerido', 'error')
            return render_template('forgot_password.html')
        
        # Verificar si el email está registrado
        user = my_db.get_user_by_email(email)
        if not user:
            flash('No existe una cuenta asociada a este email', 'error')
            return render_template('forgot_password.html')
        
        # Generar código de verificación
        verification_code = generate_verification_code()
        verification_codes[email] = verification_code
        
        # Enviar correo con código de verificación
        try:
            html_content = render_template(
                'correo_password_code.html',
                codigo=verification_code,
                email=email
            )
            
            msg = Message('Código de Verificación - Meditime',
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[email])
            msg.html = html_content
            mail.send(msg)
            
            # Guardar email en sesión para el siguiente paso
            session['reset_email'] = email
            flash('Se ha enviado un código de verificación a tu email', 'success')
            return redirect(url_for('verify_reset_code'))
            
        except Exception as e:
            flash('Error al enviar el correo. Inténtalo de nuevo.', 'error')
            return render_template('forgot_password.html')

@app.route('/verify_reset_code', methods=['GET', 'POST'])
def verify_reset_code():
    if 'reset_email' not in session:
        flash('Sesión expirada. Inicia el proceso nuevamente.', 'error')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'GET':
        return render_template('verify_reset_code.html')
    
    elif request.method == 'POST':
        email = session.get('reset_email')
        entered_code = request.form.get('verification_code')
        
        if not entered_code:
            flash('Ingresa el código de verificación', 'error')
            return render_template('verify_reset_code.html')
        
        # Verificar código
        if email not in verification_codes or verification_codes[email] != entered_code:
            flash('Código de verificación incorrecto', 'error')
            return render_template('verify_reset_code.html')
        
        # Código correcto, proceder al cambio de contraseña
        session['code_verified'] = True
        return redirect(url_for('change_password'))

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'reset_email' not in session or not session.get('code_verified'):
        flash('Acceso no autorizado. Inicia el proceso nuevamente.', 'error')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'GET':
        return render_template('change_password.html')
    
    elif request.method == 'POST':
        email = session.get('reset_email')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not new_password or not confirm_password:
            flash('Todos los campos son requeridos', 'error')
            return render_template('change_password.html')
        
        if new_password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('change_password.html')
        
        if len(new_password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'error')
            return render_template('change_password.html')
        
        try:
            # Cambiar contraseña en la base de datos
            print(email)
            my_db.change_password(email, new_password)
            
            # Limpiar datos de sesión y códigos de verificación
            verification_codes.pop(email, None)
            session.pop('reset_email', None)
            session.pop('code_verified', None)
            
            flash('Contraseña cambiada exitosamente', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            flash('Error al cambiar la contraseña. Inténtalo de nuevo.', 'error')
            return render_template('change_password.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validate required fields
        if not email or not password:
            flash('Por favor, complete todos los campos.', 'error')
            return render_template("login.html")
        
        # Attempt to login the user
        user = my_db.login_user(email, password)
        
        # Check if user exists
        if user:
            # Store user ID in session
            session['user_id'] = user[0]  # First index of the returned row
            
            # Redirect to dashboard or home page
            return redirect(url_for('dashboard'))
        else:
            # Authentication failed
            flash('Correo electrónico o contraseña incorrectos.', 'error')
            return render_template("login.html")
    
    # If something unexpected happens
    return render_template("login.html")

@app.route('/logout')
def logout():
    session['user_id'] = None
    return url_for('index')

@app.route('/delete_recordatorio_by_id', methods=['DELETE'])
def delete_rec_by_id():
    try:
        data = request.get_json()
        print(f"[Flask] Solicitud DELETE recibida con datos: {data}")

        if not data or 'id' not in data:
            print("[Flask] Error: No se proporcionó un ID.")
            return jsonify({'status': 'error', 'message': 'ID faltante'}), 400

        id = data['id']
        print(f"[Flask] Procediendo a eliminar el recordatorio con ID: {id}")
        my_db.delete_recordatorio_by_id(id)

        print(f"[Flask] Recordatorio con ID {id} eliminado correctamente.")
        reminder_system.restart_daily_system()

        return jsonify({'status': 'ok'}), 200

    except Exception as e:
        print(f"[Flask] Excepción al eliminar recordatorio: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        # Obtener datos del formulario usando request.form en lugar de request.args
        username = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        number = request.form.get('telefono')
        tipo = request.form.get('type')

        # Validaciones simples
        if not username or not email or not password:
            flash("Todos los campos son obligatorios", "error")
            return redirect(url_for('register'))

        try:
            user = my_db.create_user(username, email, password, number, tipo)
            session['user_id'] = user[0]  # Guardamos el ID del usuario en sesión
            flash("Registro exitoso", "success")
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f"Error al registrar: {str(e)}", "error")
            return redirect(url_for('register'))
        
@app.route('/dashboard')
def dashboard():
    user = session.get('user_id')
    userdata = my_db.get_usuario(user)
    print(userdata)
    return render_template('dashboard.html', userdata=userdata)


@app.route('/add_medication', methods=['POST'])
def add_medication():
    # Check if user is logged in
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'No ha iniciado sesión'})
    
    try:
        # Get form data
        paciente_id = session['user_id']
        nombre = request.form.get('nombre_medicamento')
        hora = request.form.get('hora')
        ciclo = request.form.get('ciclo')
        
        # Set dia based on ciclo
        if ciclo == 'semanal':
            dia = request.form.get('dia')
        elif ciclo == 'mensual':
            # For monthly, dia is the day of the month (1-31)
            dia = request.form.get('dia', '1')  # Default to 1st day if not specified
        else:
            # For daily or multiple times, dia is not relevant
            dia = '0'
        
        # Add medication to database
        result = my_db.add_medicamento_usuario(
            paciente_id=paciente_id,
            nombre=nombre,
            dia=dia,
            hora=hora,
            ciclo=ciclo
        )
        
        if result:
            return jsonify({'success': True, 'message': 'Medicamento añadido correctamente'})
        else:
            return jsonify({'success': False, 'message': 'Error al añadir el medicamento'})
            
    except Exception as e:
        print(f"Error al añadir medicamento: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/get_medication')
def get_medication():
    medicamentos_raw = my_db.get_medicamento_usuario(session['user_id'])
    
    # Transform each medication entry to a dictionary with named keys
    medicamentos = []
    for med in medicamentos_raw:
        medicamento_dict = {
            "id": med[0],
            "user_id": med[1],
            "nombre": med[2],
            "dosis": med[3],
            "hora": med[4],
            "frecuencia": med[5]
        }
        medicamentos.append(medicamento_dict)
    
    return jsonify(medicamentos)

@app.route('/condiciones')
def condiciones():
    return render_template('condiciones.html')

@app.route('/.well-known/appspecific/com.chrome.devtools.json')
def devtools_json():
    return ('', 200)

@app.route('/add_recordatorio', methods=['POST'])
def add_recordatorio():
    
    data = request.get_json()
    paciente_id = data.get('paciente_id')
    dia = data.get('dia')
    hora = data.get('hora')
    nombre = data.get('nombre')
    user_email = data.get('user_email')

    my_db.add_recordatorio(paciente_id=paciente_id,dia=dia, hora=hora, nombre=nombre, user_email=user_email)
    reminder_system.restart_daily_system()
    return {'status': 'Ok'}

@app.route('/check')
def check():
    data = request.args
    nombre = data.get('nombre')
    dia = data.get('dia')
    hora = data.get('hora')
    my_db.delete_recordatorio(dia, hora, nombre)
    return 200

@app.route('/get_recordatorios', methods=['POST'])
def get_recordatios():
    data = request.get_json()
    paciente_id = data.get('paciente_id')
    recordatorios = my_db.get_recordatorio_by_id(paciente_id)
    return recordatorios

@app.route('/medicamentos', methods=['GET'])
def medicamentos():
    if request.args:
        name = request.args.get('name')
        categoria = request.args.get('categoria')
        if name:
            medicamentos = my_db.get_medicamento_by_name(name)
        if categoria:
            medicamentos = my_db.get_medicamento_by_categoria(categoria)
    else:
        medicamentos = my_db.get_all_medicamentos()
    return render_template('medicamentos.html', medicamentos=medicamentos)

if __name__ == '__main__':

    reminder_system.start_daily_reminder_system()
    app.run(host='0.0.0.0',debug=True, port=1010)
