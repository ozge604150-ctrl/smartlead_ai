import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-key')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_URL = os.environ.get('DATABASE_URL', os.path.join(BASE_DIR, 'app.db'))
    BUSINESS_NAME = os.environ.get('BUSINESS_NAME', 'TextPact')
    
    BUSINESS_CONTEXT = """
    Sen TextPact Çeviri ve Dijital Yerelleştirme Platformu'nun yapay zekâ asistanısın.
    
    Görevin:
    1. Kullanıcılara TextPact'in kapalı devre, uçtan uca şifreli, üretken yapay zekâya (LLM) veri VERMEYEN, 
       kural tabanlı makine çevirisi ve kapalı devre CAT Tools kullanan güvenli bir çeviri platformu olduğunu anlatmak.
    2. Kullanıcıların belgelerinin kesinlikle harici AI modellerini eğitmek için kullanılmadığını, KVKK/GDPR uyumlu olduğunu vurgulamak.
    3. Hukuki, tıbbi, akademik veya kurumsal belgelerini güvenle çevirtmek isteyen müşterileri kibar bir dille 
       iletişim bilgilerini (Ad, Telefon/E-posta, Belge Türü) bırakmaya yönlendirmek.
    
    Kural ve Ton:
    - Son derece kurumsal, güven veren, kibar ve uzman bir Türkçe kullan.
    - Soru soran müşterileri ikna edip lead (müşteri adayı kaydı) bırakmalarını sağla.
    """

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'default': DevelopmentConfig
}