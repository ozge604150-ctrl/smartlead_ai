from flask import Flask, jsonify
from flask_cors import CORS
from config import config_by_name
from app.database import init_db, close_db


def create_app(config_name='dev'):
    """Flask Uygulaması Fabrikası (Application Factory)"""
    app = Flask(__name__)

    # Konfigürasyonu yüklüyoruz
    app.config.from_object(config_by_name[config_name])

    # CORS izinlerini açıyoruz
    CORS(app)

    # Veritabanını başlatıyoruz
    init_db(app)

    # Veritabanı bağlantısını otomatik kapatıyoruz
    app.teardown_appcontext(close_db)

    # Rotaları import edip kaydediyoruz
    from app.routes import main_bp, api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    # Health check
    @app.route('/health')
    def health_check():
        return jsonify({
            'durum': 'aktif',
            'mesaj': 'Backend sunucusu sorunsuz calisiyor!'
        }), 200

    return app
