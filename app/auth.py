from flask import Blueprint, render_template, redirect, request, session

auth_bp = Blueprint('auth', __name__)

# Página de login
@auth_bp.route('/templates')
def home():
    return render_template('index.html')

@auth_bp.route('/acceso-login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['txtCorreo']
        contraseña = request.form['txtPassword']
        
        # Buscar usuario en MongoDB
        usuario = session.app.db.usuarios.find_one({"correo": correo, "password": contraseña})
        
        if usuario:
            session['logeado'] = True
            session['id'] = str(usuario['_id'])
            return redirect('/admin')
        else:
            return render_template('index.html', error="Usuario o contraseña incorrectos")
    
    return render_template('index.html')

# Ruta para cerrar sesión
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')
