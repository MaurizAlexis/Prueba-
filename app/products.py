from flask import Blueprint, render_template, request, session, redirect

products_bp = Blueprint('products', __name__)

# Panel de administración (solo para usuarios autenticados)
@products_bp.route('/templates')
def admin():
    if 'logeado' in session:
        productos = session.app.db.productos.find()
        return render_template('admin.html', productos=productos)
    else:
        return redirect('/')

# Listar productos
@products_bp.route('/productos')
def listar_productos():
    if 'logeado' in session:
        productos = session.app.db.productos.find()
        return render_template('listar_productos.html', productos=productos)
    else:
        return redirect('/')

# Productos agotados
@products_bp.route('/productos/agotados')
def productos_agotados():
    if 'logeado' in session:
        productos_agotados = session.app.db.productos.find({"stock": 0})
        return render_template('productos_agotados.html', productos=productos_agotados)
    else:
        return redirect('/')

# Productos con stock bajo
@products_bp.route('/productos/stock-bajo')
def productos_stock_bajo():
    if 'logeado' in session:
        productos = session.app.db.productos.find({"stock": {"$lt": 5}})
        return render_template('listar_productos.html', productos=productos)
    else:
        return redirect('/')

# Formulario de registro de productos
@products_bp.route('/formulario/registro')
def formulario_registro():
    if 'logeado' in session:
        return render_template('formulario_registro.html')
    else:
        return redirect('/')

# Ruta para agregar productos y calcular precios
@products_bp.route('/formulario', methods=["GET", "POST"])
def formulario():
    if 'logeado' in session:
        precio_local_calculado = None
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            marca = request.form.get('marca')
            proveedor = request.form.get('proveedor')
            tipo = request.form.get('tipo')
            descripcion = request.form.get('descripcion')
            fecha_compra = request.form.get('fecha_compra')
            precio_extranjero = float(request.form.get('precio_extranjero', 0))
            margen_ganancia = float(request.form.get('margen_ganancia', 0))
            precio_dolar = float(request.form.get('precio_dolar', 0))
            stock = int(request.form.get('stock', 0))
            
            # Cálculo del precio en moneda local
            precio_local_calculado = precio_extranjero * precio_dolar * (1 + margen_ganancia / 100)
            
            if 'guardar_producto' in request.form:
                producto = {
                    'nombre': nombre,
                    'marca': marca,
                    'proveedor': proveedor,
                    'tipo': tipo,
                    'descripcion': descripcion,
                    'fecha_compra': fecha_compra,
                    'precio_local': precio_local_calculado,
                    'precio_extranjero': precio_extranjero,
                    'margen_ganancia': margen_ganancia,
                    'precio_dolar': precio_dolar,
                    'stock': stock
                }
                session.app.db.productos.insert_one(producto)
                precio_local_calculado = None
        
        productos = session.app.db.productos.find()
        return render_template("formulario.html", productos=productos, precio_local_calculado=precio_local_calculado)
    else:
        return redirect('/')
