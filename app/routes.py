from flask import Blueprint, render_template, request, jsonify
from app.database import lead_ekle, tum_leadler
from app.services.ai_service import ai_service, AIServiceError

# İki ayrı Blueprint oluşturuyoruz (Sayfalar ve API Rotaları)
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

# ==================== SAYFA ROTALARI ====================

@main_bp.route('/')
def index():
    """Karşılama Sayfası (B2C)"""
    return render_template('index.html')

@main_bp.route('/dashboard')
def dashboard():
    """Yönetim Paneli (B2B)"""
    return render_template('dashboard.html')

# ==================== API ROTALARI ====================

@api_bp.route('/sohbet', methods=['POST'])
def sohbet():
    """Yapay Zekâ ile mesajlaşma uç noktası"""
    data = request.get_json() or {}
    mesaj = data.get('mesaj', '').strip()
    gecmis = data.get('gecmis', [])

    if not mesaj:
        return jsonify({'basari': False, 'hata': 'Mesaj alanı boş olamaz.'}), 400

    try:
        yanit = ai_service.yanit_uret(mesaj, gecmis)
        return jsonify({'basari': True, 'yanit': yanit}), 200
    except AIServiceError as e:
        return jsonify({'basari': False, 'hata': str(e)}), 503
    except Exception as e:
        return jsonify({'basari': False, 'hata': 'Sunucu tarafında beklenmeyen bir hata oluştu.'}), 500

@api_bp.route('/leads', methods=['POST'])
def yeni_lead():
    """Yeni Müşteri Adayı Kaydetme uç noktası"""
    data = request.get_json() or {}
    isim = data.get('isim', '').strip()
    telefon = data.get('telefon', '').strip()
    mesaj = data.get('mesaj', '').strip()
    belge_turu = data.get('belge_turu', 'Genel').strip()

    if not isim or not telefon:
        return jsonify({'basari': False, 'hata': 'İsim ve Telefon zorunludur.'}), 400

    try:
        lead_id = lead_ekle(isim, telefon, mesaj, belge_turu)
        return jsonify({
            'basari': True,
            'mesaj': 'Kaydınız başarıyla alındı.',
            'id': lead_id
        }), 201
    except Exception as e:
        return jsonify({'basari': False, 'hata': 'Veritabanı kaydı sırasında hata oluştu.'}), 500

@api_bp.route('/leads', methods=['GET'])
def lead_listesi():
    """Tüm Müşteri Adaylarını Listeleme uç noktası"""
    try:
        kayitlar = tum_leadler()
        return jsonify({'basari': True, 'data': kayitlar}), 200
    except Exception as e:
        return jsonify({'basari': False, 'hata': 'Kayıtlar getirilirken hata oluştu.'}), 500