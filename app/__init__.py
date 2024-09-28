from flask import Flask

def create_app():
    app = Flask(__name__)

    # Importa y registra blueprints u otros módulos
    from .auth import auth_bp
    from .products import products_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)

    return app
