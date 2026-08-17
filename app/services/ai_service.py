import requests
from flask import current_app

class AIServiceError(Exception):
    """Yapay Zekâ Servisine özel hata sınıfı"""
    pass

class AIService:
    """Yapay Zekâ (Groq) çağrılarını yöneten servis sınıfı."""

    def _get_system_prompt(self):
        """Config dosyasından BUSINESS_CONTEXT metnini okur."""
        return current_app.config.get('BUSINESS_CONTEXT', '')

    def yanit_uret(self, mesaj, gecmis=None):
        """
        Kullanıcı mesajını ve geçmiş sohbeti alarak Groq API'sine gönderir,
        yapay zekâ yanıtını döndürür.
        """
        api_key = current_app.config.get('GROQ_API_KEY')
        
        # Eğer API Anahtarı girilmediyse çökme yaşanmaması için Demo Modu yanıtı dönüyoruz
        if not api_key or api_key == 'gsk_BURAYA_KENDI_GROQ_API_ANAHTARINI_YAPISTIR':
            return "Demo Modu: Groq API anahtarınız henüz ayarlanmadığı için bu otomatik yanıttır. Lütfen .env dosyanızı kontrol edin."

        if gecmis is None:
            gecmis = []

        # Groq API istek adresi (Endpoint)
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Sistem talimatı (System Role) öncelikli olacak şekilde mesaj dizisi hazırlanıyor
        messages = [
            {"role": "system", "content": self._get_system_prompt()}
        ]

        # Geçmiş sohbet mesajlarını ekliyoruz
        for msg in gecmis:
            messages.append(msg)

        # Yeni kullanıcı mesajını dizinin sonuna ekliyoruz
        messages.append({"role": "user", "content": mesaj})

        payload = { 
    "model": "openai/gpt-oss-20b", 
    "messages": messages, 
    "temperature": 0.7, 
    "max_tokens": 500 
}

        try:
            # API'ye POST isteği atılıyor
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code != 200:
                raise AIServiceError(f"Groq API Hatası: Status {response.status_code} - {response.text}")
            
            data = response.json()
            ai_message = data['choices'][0]['message']['content']
            return ai_message

        except requests.exceptions.RequestException as e:
            raise AIServiceError(f"Yapay zekâ servisine bağlanırken ağ hatası oluştu: {str(e)}")
        except (KeyError, IndexError) as e:
            raise AIServiceError(f"Yapay zekâ yanıtı işlenirken hata oluştu: {str(e)}")

# Dışarıdan kolayca çağrılabilmesi için tekil örnek (Instance) oluşturuyoruz
ai_service = AIService()