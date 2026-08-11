import sqlite3
from flask import current_app, g

def get_db():
    """Veritabanı bağlantısını getirir veya yeni bağlantı açar."""
    if 'db' not in g:
        # Config'den veritabanı dosya yolunu alıp bağlanıyoruz
        db_path = current_app.config['DATABASE_URL']
        g.db = sqlite3.connect(db_path)
        # Satırlara sütun isimleriyle erişim imkanı sağlar
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """İstek bitince veritabanı bağlantısını kapatır."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    """Veritabanı tablosunu yoksa otomatik oluşturur."""
    with app.app_context():
        db = get_db()
        # 'leads' tablosunu güvenli şekilde oluşturuyoruz
        db.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                belge_turu TEXT,
                tarih DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()

def lead_ekle(isim, telefon, mesaj="", belge_turu="Genel"):
    """
    Yeni müşteri adayını veritabanına ekler.
    Güvenlik Uyarısı: SQL Injection koruması için '?' yer tutucusu kullanılmıştır.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        '''
        INSERT INTO leads (isim, telefon, mesaj, belge_turu)
        VALUES (?, ?, ?, ?)
        ''',
        (isim, telefon, mesaj, belge_turu)
    )
    db.commit()
    return cursor.lastrowid

def tum_leadler():
    """Tüm kayıtları en yeniden eskiye sıralı olarak getirir."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM leads ORDER BY tarih DESC')
    rows = cursor.fetchall()
    
    # SQLite Row nesnelerini Python sözlüğüne (dict) çeviriyoruz
    result = []
    for row in rows:
        result.append({
            'id': row['id'],
            'isim': row['isim'],
            'telefon': row['telefon'],
            'mesaj': row['mesaj'],
            'belge_turu': row['belge_turu'],
            'tarih': row['tarih']
        })
    return result