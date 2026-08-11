import sys
import os

# Mevcut dizini Python arama yoluna ekliyoruz
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app

# Gunicorn / Render'ın uygulamayı bulabilmesi için app değişkeni dışarıda tanımlanmalıdır
app = create_app('dev')

if __name__ == '__main__':
    # Yerel geliştirmede (Localhost) çalıştırma
    app.run(host='0.0.0.0', port=5000, debug=True)