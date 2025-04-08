from flask import Flask
from backend.db_connection import db
from backend.client.client_routes import client
from backend.trainer.products_routes import trainer
from backend.simple.simple_routes import simple_routes
import os
from dotenv import load_dotenv


def create_app():
    app = Flask(__name__)

    # Load environment variables
    load_dotenv()

    # Log all relevant environment variables to diagnose issues
    app.logger.info('Environment variables:')
    app.logger.info(f'DB_USER: {os.getenv("DB_USER")}')
    app.logger.info(f'DB_HOST: {os.getenv("DB_HOST")}')
    app.logger.info(f'DB_PORT: {os.getenv("DB_PORT")}')
    app.logger.info(f'DB_NAME: {os.getenv("DB_NAME")}')

    # Set app configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER', '').strip()
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_ROOT_PASSWORD', '').strip()
    app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST', '').strip()
    app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('DB_PORT', '3306').strip())
    app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME', '').strip()

    # Initialize the database
    app.logger.info('Initializing database connection')
    db.init_app(app)

    # Create a test connection to verify database access
    with app.app_context():
        try:
            # This depends on how your db object is implemented
            # For example with Flask-SQLAlchemy you might do:
            # db.engine.connect()
            app.logger.info('Database connection successful')
        except Exception as e:
            app.logger.error(f'Database connection failed: {str(e)}')
            # Optionally re-raise the exception if you want the app to fail on startup
            # raise e

    # Register blueprints
    app.register_blueprint(simple_routes)
    app.register_blueprint(trainer, url_prefix='/t')
    app.register_blueprint(client, url_prefix='/c')

    return app