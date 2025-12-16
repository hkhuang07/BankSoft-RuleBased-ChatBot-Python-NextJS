"""
Bank Customer Service Chatbot API 
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import re

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  

# Cấu trúc dữ liệu cho các dịch vụ hỗ trợ khách hàng
SUPPORT_SERVICES = {
    "chuyển tiền": {
        "chuyển tiền ngay": "Dịch vụ chuyển tiền ngay lập tức - Nhanh chóng, bảo mật cao với tỷ giá cạnh tranh",
        "thay đổi hạn mức": "Dịch vụ điều chỉnh hạn mức chuyển tiền - Tăng/giảm giới hạn theo nhu cầu cá nhân",
        "chuyển nhầm/ lỗi": {
            "chuyển tiền trong VCB": "Xử lý chuyển tiền nhầm trong hệ thống VCB nội bộ - Quy trình nhanh chóng, hỗ trợ 24/7",
            "chuyển tiền nhanh 24/7": "Xử lý chuyển tiền nhầm qua dịch vụ 24/7 - Hỗ trợ khẩn cấp bất cứ lúc nào",
            "chuyển qua ngân hàng nước ngoài": "Xử lý chuyển tiền nhầm quốc tế - Hỗ trợ quy trình phức tạp với tư vấn chuyên sâu",
            "chuyển tiền mặt": "Xử lý chuyển tiền nhầm dịch vụ tiền mặt - Hướng dẫn chi tiết các bước khắc phục",
        },
    },
    "nạp tiền điện thoại": "Dịch vụ nạp tiền điện thoại - Hỗ trợ tất cả nhà mạng với nhiều mệnh giá, tự động hoá hoàn toàn",
    "thanh toán hóa đơn": {
        "thanh toán hóa đơn ngay": "Dịch vụ thanh toán hóa đơn trực tuyến - Điện, nước, internet, viễn thông, bảo hiểm",
        "đăng ký trích nợ tự động": "Dịch vụ đăng ký trích nợ tự động - Tự động thanh toán định kỳ, tiết kiệm thời gian",
    },
    "cập nhật sinh trắc học": {
        "cập nhật qua CCCD gắn chip": "Cập nhật thông tin sinh trắc học qua CCCD gắn chip - Công nghệ hiện đại, an toàn cao",
        "cập nhật qua VNeID": "Cập nhật thông tin sinh trắc học qua ứng dụng VNeID - Tiện lợi, nhanh chóng trên mobile",
    },
    "tạm biệt": "Cảm ơn quý khách đã tin tưởng sử dụng dịch vụ ngân hàng của chúng tôi. Chúc quý khách một ngày tốt lành!",
}

# Từ đồng nghĩa mở rộng cho từng lựa chọn - Hỗ trợ nhận diện nhiều biến thể
SYNONYMS = {
    # Greeting - Chào hỏi
    "greeting": [
        "hi", "hello", "helo", "helllo", "hii", "hiiiii", "chào", "xin chào", "chào bạn", "chào mừng", 
        "hey", "yo", "helo", "hola", "bonjour", "chào cậu", "chào anh", "chào chị", "chào em", 
        "xin chào bạn", "chào sếp", "chào cô", "chào thầy", "chào bác", "chào cô chú",
        "greet", "greeting", "chào hỏi", "lời chào", "xin chào", "kính chào",
        "你好", "こんにちは", "안녕하세요", "guten tag", "hola", "bonjour"
    ],
    
    # Transfer Money - Chuyển tiền tổng quát
    "chuyển tiền": [
        "gửi tiền", "gửi khoản", "chuyển khoản", "transfer", "remit", "send money", 
        "money transfer", "transfer money", "remit money", "bank transfer", "chuyển tổng",
        "tiền gửi", "tiền chuyển", "tiền chuyển khoản", "giao dịch chuyển tiền",
        "chuyển tiền ngân hàng", "chuyển khoản ngân hàng", "chuyển tiền online",
        "chuyển tiền trực tuyến", "chuyển tiền số", "tiền mã hóa", "crypto transfer",
        "chuyển từ", "chuyển đến", "nạp tiền", "rút tiền", "nạp", "rút",
        "transfer online", "e-transfer", "instant transfer", "same day transfer",
        "immediate transfer", "urgent transfer", "chuyển gấp", "chuyển khẩn",
        "汇款", "송금", " transfert", "überweisung", "transferencia"
    ],
    
    # Instant Transfer - Chuyển tiền ngay
    "chuyển tiền ngay": [
        "gửi tiền ngay", "chuyển khoản ngay", "chuyển tiền gấp", "chuyển tiền khẩn",
        "transfer money now", "send money now", "remit money now", "instant transfer",
        "immediate transfer", "quick transfer", "fast transfer", "urgent transfer",
        "chuyển tiền tức thì", "chuyển tiền ngay lập tức", "chuyển tiền nhanh",
        "chuyển tiền realtime", "chuyển tiền real time", "chuyển tiền live",
        "chuyển tiền ngay hôm nay", "chuyển tiền hôm nay", "chuyển ngay",
        "chuyển nhanh", "chuyển nhanh nhất", "chuyển siêu nhanh",
        "immediately transfer", "now transfer", "now remit", "instant remit",
        "urgent remit", "quick remit", "immediate remit", "fast remit",
        "立即汇款", "今すぐ送金", "지금 송금", "sofortige überweisung"
    ],
    
    # Change Limit - Thay đổi hạn mức
    "thay đổi hạn mức": [
        "thay đổi giới hạn", "thay đổi hạn mức", "điều chỉnh hạn mức", "điều chỉnh giới hạn",
        "change limit", "adjust limit", "modify limit", "increase limit", "decrease limit",
        "tăng hạn mức", "giảm hạn mức", "nâng hạn mức", "hạ hạn mức",
        "thay đổi số tiền", "điều chỉnh số tiền", "chỉnh hạn mức", "set limit",
        "hạn mức chuyển tiền", "giới hạn chuyển tiền", "limit transfer", "transfer limit",
        "daily limit", "monthly limit", "transaction limit", "hạn mức giao dịch",
        "giới hạn giao dịch", "maximum transfer", "minimum transfer", "default limit",
        "custom limit", "personalized limit", "individual limit", "personal limit",
        "更改限制", "制限を変更する", "한도 변경", "limit ändern", "limite modifier"
    ],
    
    # Wrong Transfer / Errors - Chuyển nhầm/lỗi
    "chuyển nhầm/ lỗi": [
        "chuyển nhầm", "lỗi chuyển tiền", "sai người nhận", "sai số tài khoản", "sai họ tên",
        "wrong transfer", "transfer error", "mistaken transfer", "incorrect transfer", 
        "erroneous transfer", "failed transfer", "problem transfer", "issue transfer",
        "sai người nhận", "nhầm người nhận", "sai tài khoản", "nhầm tài khoản",
        "sai họ tên", "nhầm họ tên", "số tiền nhầm", "sai số tiền", "nhầm số tiền",
        "reversal transfer", "retrieve transfer", "recall transfer", "stop transfer",
        "追溯转帐", "误送金", "잘못된 송금", "falscher transfer", "erreur transfert"
    ],
    
    # Internal VCB Transfer Error
    "chuyển tiền trong VCB": [
        "VCB nội bộ", "chuyển trong VCB", "VCB transfer", "VCB internal", "VCB inside",
        "VCB chuyển nhầm", "nội bộ VCB", "cùng ngân hàng VCB", "ngân hàng VCB nội bộ",
        "internal VCB transfer", "within VCB", "same bank VCB", "VCB intra-bank",
        "VCB internal transfer", "VCB same bank", "VCB internal", "VCB inner transfer",
        "VCB内部转账", "VCB内送金", "VCB内の送金", "VCB interner Transfer", "transfert VCB interne"
    ],
    
    # 24/7 Fast Service Transfer Error
    "chuyển tiền nhanh 24/7": [
        "chuyển nhanh", "chuyển 24/7", "dịch vụ 24/7", "24/7 service", "round the clock",
        "chuyển siêu nhanh", "chuyển tức thì", "chuyển 24/24", "chuyển 7/7", "chuyển cuối tuần",
        "fast transfer", "quick transfer", "24/7 transfer", "instant transfer 24/7",
        "immediate transfer", "urgent transfer", "emergency transfer", "priority transfer",
        "real-time transfer", "live transfer", "continuous service", "non-stop service",
        "随时服务", "24시간 서비스", "연중무휴 서비스", "24-Stunden-Service", "service 24/7"
    ],
    
    # International/Foreign Bank Transfer Error
    "chuyển qua ngân hàng nước ngoài": [
        "chuyển quốc tế", "ngân hàng nước ngoài", "chuyển ra nước ngoài", "chuyển sang ngoại quốc",
        "international transfer", "foreign bank transfer", "overseas transfer", "global transfer",
        "chuyển quốc tế nhầm", "chuyển quốc tế lỗi", "ngân hàng quốc tế", "ngân hàng nước ngoài",
        "swift transfer", "wire transfer", "bank wire", "international wire", "overseas wire",
        "cross-border transfer", "inter-bank transfer", "international remittance", "foreign remittance",
        "chuyển SWIFT", "chuyện điện tử", "chuyển điện tử", "chuyển ngoại tệ", "chuyển USD",
        "跨国转账", "外国銀行送金", "국제 송금", "internationaler Transfer", "transfert international"
    ],
    
    # Cash Transfer Error
    "chuyển tiền mặt": [
        "gửi tiền mặt", "tiền mặt", "tiền giấy", "cash", "money cash", "cash transfer",
        "physical cash transfer", "in-person cash transfer", "hand-to-hand transfer", "face-to-face transfer",
        "chuyển tiền mặt nhầm", "tiền mặt lỗi", "sai tiền mặt", "nhầm tiền mặt",
        "money counter transfer", "branch transfer", "counter transfer", "bank counter",
        "personal handover", "cash delivery", "cash pick-up", "cash in hand",
        "tiền mặt tại quầy", "chuyển tiền tại quầy", "giao dịch tiền mặt", "transact cash",
        "现金转账", "现金送金", "현금 송금", "Bartransfer", "transfert en espèces"
    ],
    
    # Phone Top-up
    "nạp tiền điện thoại": [
        "nạp thẻ điện thoại", "nạp sim", "nạp mobile", "top up điện thoại", "phone top up", 
        "mobile top up", "recharge phone", "recharge mobile", "phone recharge", "mobile recharge",
        "nạp tiền sim", "nạp viettel", "nạp mobifone", "nạp vinaphone", "nạp vietnamobile",
        "nạp itel", "nạp redi", "nạp vsmart", "nạp gmobile", "nạp cmc",
        "mobile card", "prepaid card", "credit card mobile", "phone credit", "mobile credit",
        "nạp tiền tự động", "auto top up", "scheduled top up", "regular top up", "weekly top up",
        "monthly top up", "top up package", "data package", "internet package", "data bundle",
        "充值手机", "携帯電話をチャージする", "휴대폰 충전", "Handy-Aufladung", "rechargement téléphone"
    ],
    
    # Bill Payment General
    "thanh toán hóa đơn": [
        "trả hóa đơn", "tính tiền", "thanh toán hóa đơn", "pay bill", "bill payment",
        "settle bill", "invoice payment", "pay invoice", "pay utilities", "pay service",
        "thanh toán điện", "thanh toán nước", "thanh toán internet", "thanh toán điện thoại",
        "thanh toán bảo hiểm", "thanh toán thuế", "thanh toán phí", "thanh toán lệ phí",
        "utility bill", "electricity bill", "water bill", "internet bill", "phone bill",
        "insurance bill", "tax bill", "fee payment", "charge payment", "service payment",
        "thanh toán online", "online payment", "digital payment", "e-payment", "auto payment",
        "bill online", "invoice online", "电子支付", "請求書の支払い", "청구서 지불"
    ],
    
    # Instant Bill Payment
    "thanh toán hóa đơn ngay": [
        "trả hóa đơn ngay", "thanh toán ngay", "pay bill immediately", "instant payment",
        "immediate payment", "quick payment", "urgent payment", "same day payment", "today payment",
        "thanh toán tức thì", "thanh toán ngay lập tức", "thanh toán nhanh", "thanh toán gấp",
        "thanh toán hôm nay", "pay now", "bill now", "pay today", "immediate bill payment",
        "quick bill payment", "fast bill payment", "instant bill payment", "real-time payment",
        "live payment", "online instant", "immediate online", "same day online",
        "立即支付账单", "今すぐ請求書を支払う", "지금 청구서 지불", "sofortige Rechnungszahlung", "paiement facture immédiat"
    ],
    
    # Auto Debit Registration
    "đăng ký trích nợ tự động": [
        "đăng ký tự động trích nợ", "auto debit", "automatic debit", "auto payment", "automatic payment",
        "tự động thanh toán", "auto settlement", "automatic settlement", "recurring payment", "periodic payment",
        "standing order", "auto collect", "auto debit service", "automatic collection", "regular payment",
        "monthly payment", "yearly payment", "weekly payment", "daily payment", "scheduled payment",
        "setup auto pay", "enable auto pay", "activate auto debit", "register auto payment", "enroll auto debit",
        "thanh toán định kỳ", "thanh toán chu kỳ", "thanh toán lặp lại", "thanh toán đầy đủ", "thanh toán hoàn toàn",
        "trích nợ tự động", "auto transfer", "automatic transfer", "regular transfer", "scheduled transfer",
        "自动扣款注册", "自動引き落とし登録", "자동 이체 등록", "automatischer Lastschriftabzug", "inscription débit automatique"
    ],
    
    # Biometric Update
    "cập nhật sinh trắc học": [
        "cập nhật biometric", "cập nhật sinh trắc", "cập nhật dấu vân tay", "cập nhật vân tay",
        "cập nhật nhận diện khuôn mặt", "cập nhật khuôn mặt", "cập nhật móng mắt", "cập nhật mắt",
        "update biometric", "biometric update", "fingerprint update", "face update", "eye update",
        "sinhh trắc học", "biometric information", "biological information", "identification data",
        "dấu sinh trắc", "dấu vân tay sinh học", "nhận diện sinh học", "xác thực sinh trắc học",
        "digital fingerprint", "digital face", "biometric authentication", "biometric verification",
        "voice recognition", "gesture recognition", "behavioral biometrics", "physiological biometrics",
        "更新生物识别信息", "生体認証の更新", "생체 인식 업데이트", "biometrisches Update", "mise à jour biométrique"
    ],
    
    # CCCD Update
    "cập nhật qua CCCD gắn chip": [
        "cập nhật qua căn cước công dân", "cập nhật thẻ căn cước", "update via citizen ID",
        "cập nhật qua thẻ CCCD", "cập nhật qua chip", "cập nhật CCCD", "cập nhật CCCD chip",
        "update via chip ID", "chip ID card", "chip citizen card", "chip card", "smart card",
        "update via person card", "personal ID card", "identity card", "ID card", "citizen card",
        "căn cước công dân", "thẻ căn cước", "thẻ công dân", "thẻ ID", "thẻ căn cước chip",
        "thẻ thông minh", "chip thẻ", "dữ liệu chip", "RFID", "NFC", "contactless",
        "cập nhật dấu vân tay", "cập nhật khuôn mặt", "xác thực CCCD", "verify CCCD",
        "通过芯片身份证更新", "チップ付きIDカードで更新", "칩 ID 카드로 업데이트", "Chip-Ausweis-Update", "mise à jour carte d'identité à puce"
    ],
    
    # VNeID Update
    "cập nhật qua VNeID": [
        "cập nhật qua VNeID app", "cập nhật qua ứng dụng VNeID", "cập nhật VNeID", 
        "cập nhật VneID", "cập nhật app VNeID", "cập nhật ứng dụng VNeID",
        "update via VNeID application", "VNeID app", "VNeID application", "VNeID mobile",
        "VNeID digital", "digital ID", "digital identity", "electronic ID", "e-ID",
        "ứng dụng CCCD", "app CCCD", "mobile CCCD", "digital CCCD", "electronic CCCD",
        "VNeID service", "VNeID platform", "VNeID system", "VNeID solution", "VNeID integration",
        "đăng nhập VNeID", "login VNeID", "access VNeID", "use VNeID", "open VNeID",
        "VNeID tải xuống", "download VNeID", "install VNeID", "cài đặt VNeID",
        "通过VNeID应用程序更新", "VNeIDアプリで更新", "VNeID 앱으로 업데이트", "VNeID-Anwendungs-Update", "mise à jour application VNeID"
    ],
    
    # Farewell
    "tạm biệt": [
        "tạm biệt", "bye", "bye bye", "byebye", "see you", "see you later", "see ya",
        "catch you later", "catch to you later", "smell you later", "see you soon",
        "good bye", "goodbye", "farewell", "so long", "au revoir", "ciao", "sayonara",
        "quit", "exit", "stop", "end", "finish", "done", "hoàn thành", "xong",
        "kết thúc", "dừng", "ngừng", "thoát", "ra về", "good night", "see tomorrow",
        "take care", "care", "bye for now", "talk to you later", "later", "talking soon",
        "再见", "回头见", "나중에 봐요", "안녕히 가세요", "さようなら", "auf wiedersehen", "au revoir"
    ]
}

# Session storage cho các trạng thái chat
chat_sessions = {}

def get_main_service_keys():
    """Lấy danh sách các key dịch vụ chính theo thứ tự hiển thị"""
    return [key for key, value in SUPPORT_SERVICES.items() if (isinstance(value, dict) or isinstance(value, str)) and key != "tạm biệt"]

def fuzzy_match(text, target):
    
    text_clean = re.sub(r'[^\w\s]', '', text.lower())
    target_clean = re.sub(r'[^\w\s]', '', target.lower())
    
    if text_clean == target_clean:
        return True
    
    if len(text_clean) >= 3 and len(target_clean) >= 3:
        if text_clean in target_clean or target_clean in text_clean:
            return True
    
    if abs(len(text_clean) - len(target_clean)) <= 2:
        common_chars = sum(1 for a, b in zip(text_clean, target_clean) if a == b)
        if common_chars >= max(len(text_clean), len(target_clean)) * 0.7:
            return True
    
    return False

def find_partial_keyword(services, text):
   
    text_lower = text.lower()
    found_keys = []
    
    def recursive_search(services_dict):
        for key, value in services_dict.items():
            key_lower = key.lower()
            
            if key_lower in text_lower:
                found_keys.append(key)
            
            elif fuzzy_match(text_lower, key_lower):
                found_keys.append(key)
            
            if key in SYNONYMS:
                for synonym in SYNONYMS[key]:
                    synonym_lower = synonym.lower()
                    if synonym_lower in text_lower or fuzzy_match(text_lower, synonym_lower):
                        found_keys.append(key)
                        break
            
            if isinstance(value, dict):
                recursive_search(value)
    
    recursive_search(services)
    
    # Trả về keyword có độ ưu tiên cao nhất
    if found_keys:
        exact_matches = [key for key in found_keys if key.lower() in text_lower]
        if exact_matches:
            return exact_matches[0]
        return found_keys[0]    
    
    return None

def normalize_input(text):
    text = text.lower().strip()
    standard_input = "".join(text.lower().split())  # Remove all spaces
    
    # 1. Tìm trong cấu trúc service
    def find_key_in_service_structure(services):
        if isinstance(services, dict):
            for key, value in services.items():
                standard_key = "".join(key.lower().split())
                if standard_key == standard_input:
                    return key

                result = find_key_in_service_structure(value)
                if result:
                    return result
        return None

    found_key = find_key_in_service_structure(SUPPORT_SERVICES)
    if found_key:
        return found_key 

    # 2. Tìm trong SYNONYMS với fuzzy matching
    for key, values in SYNONYMS.items():
        for value in values:
            value_lower = value.lower().strip()
            
            # Exact match
            if value_lower == text:
                return key
            
            # Substring match
            if text in value_lower or value_lower in text:
                return key
            
            # Fuzzy match
            if fuzzy_match(text, value_lower):
                return key
    
    # 3. Tìm số thứ tự menu
    if text.isdigit():
        try:
            index = int(text) - 1
            main_services = get_main_service_keys()
            if 0 <= index < len(main_services):
                return main_services[index]
        except:
            pass
    
    # 4. Tìm partial keyword trong service structure
    partial_key = find_partial_keyword(SUPPORT_SERVICES, text)
    if partial_key:
        return partial_key
    
    # 5. Fallback 
    for key in SUPPORT_SERVICES.keys():
        if key in text or fuzzy_match(text, key):
            return key
            
    return text.lower().strip()

# Hàm xây dựng tin nhắn chào hỏi khách hàng 
def get_greeting():
    main_services = get_main_service_keys()
    choices = "\n".join([f" {i}. {n.title()}" for i, n in enumerate(main_services, 1 )])   
    return f"""🎯 Xin chào quý khách! 
    
Tôi là Bank-Soft BaSo - Trợ lý ảo hỗ trợ khách hàng ngân hàng chuyên nghiệp.

📋 Tôi có thể hỗ trợ quý khách các dịch vụ sau:
{choices}

🔍 Quý khách có thể nhập số thứ tự hoặc tên dịch vụ, tôi sẽ hỗ trợ ngay lập tức!

📞 Hoặc liên hệ Hotline: 1900 1579 để được tư vấn trực tiếp."""

# Hàm lấy thông tin về dịch vụ hỗ trợ khách hàng
def get_service_info():
    return "Vui lòng chọn dịch vụ bạn cần hỗ trợ: " + ", ".join([service.title() for service in SUPPORT_SERVICES.keys()]) + "."
    
# CHUYỂN TIỀN - Responses chi tiết hơn
def get_transfer_info():
    transfer_services = SUPPORT_SERVICES["chuyển tiền"]
    return """💳 CHUYỂN TIỀN NGÂN HÀNG

Tôi hỗ trợ quý khách các dịch vụ chuyển tiền sau:

📍 Chuyển tiền ngay - Dịch vụ chuyển tiền tức thì
🔧 Thay đổi hạn mức - Điều chỉnh giới hạn chuyển tiền
⚠️ Xử lý chuyển nhầm/lỗi - Hỗ trợ khắc phục sự cố

Vui lòng chọn dịch vụ mong muốn hoặc nhập yêu cầu cụ thể."""

def get_instant_transfer_response():
    return """✅ DỊCH VỤ CHUYỂN TIỀN NGAY

🏦 Chuyển tiền trong và ngoài nước với tỷ giá cạnh tranh

🌟 Ưu điểm vượt trội:
• Chuyển tiền ngay lập tức 24/7
• Tỷ giá minh bạch, cập nhật real-time  
• Phí chuyển tiền hợp lý, giảm thiểu chi phí
• Bảo mật cao với xác thực 2FA
• Hỗ trợ nhiều loại tiền tệ (VND, USD, EUR...)

📱 THỰC HIỆN:
1. Đăng nhập ứng dụng ngân hàng Mobile Banking
2. Chọn "Chuyển tiền" → "Chuyển tiền ngay"
3. Nhập thông tin người nhận và số tiền
4. Xác nhận giao dịch bằng vân tay/face ID

💰 Hạn mức: Tối đa 500 triệu VNĐ/giao dịch
⏰ Thời gian: Ngay lập tức đến 5 phút

📞 Cần hỗ trợ: Hotline 1900 1579"""

def get_change_limit_response():
    return """⚙️ DỊCH VỤ THAY ĐỔI HẠN MỨC CHUYỂN TIỀN

🔐 Điều chỉnh giới hạn giao dịch theo nhu cầu

📊 Các loại hạn mức có thể điều chỉnh:
• Hạn mức chuyển tiền/ngày
• Hạn mức chuyển tiền/tháng  
• Hạn mức giao dịch duy nhất
• Hạn mức tích lũy trong kỳ

📈 Tăng hạn mức - Thuận tiện cho giao dịch lớn
📉 Giảm hạn mức - Bảo vệ an toàn tài khoản

📋 YÊU CẦU CẦN THIẾT:
• Xác thực danh tính sinh trắc học
• Cung cấp lý do thay đổi hạn mức
• Xác nhận qua ứng dụng/ATM

⚡ XỬ LÝ NHANH: 15-30 phút
📱 THỰC HIỆN: Ứng dụng Mobile Banking → Cài đặt → Hạn mức

💡 MẸO: Thiết lập hạn mức phù hợp với nhu cầu thực tế để tối ưu bảo mật!"""

def get_wrong_transfer_info():
    wrong_transfer_services = SUPPORT_SERVICES["chuyển tiền"]["chuyển nhầm/ lỗi"]
    return """⚠️ XỬ LÝ CHUYỂN TIỀN NHẦM/LỖI

🚨 Quý khách không cần lo lắng, chúng tôi sẽ hỗ trợ ngay!

🛠️ CÁC TRƯỜNG HỢP XỬ LÝ:

• Chuyển tiền trong VCB nội bộ - Quy trình nhanh nhất
• Chuyển tiền nhanh 24/7 - Hỗ trợ khẩn cấp  
• Chuyển qua ngân hàng nước ngoài - Tư vấn chuyên sâu
• Chuyển tiền mặt - Hướng dẫn chi tiết

📞 Liên hệ ngay: 1900 1579 (24/7)
🕐 Thời gian xử lý: 30-120 phút

Vui lòng chọn loại chuyển tiền để được hướng dẫn chi tiết."""

def get_wrong_transfer_vcb_response():
    return """🏦 XỬ LÝ CHUYỂN TIỀN NHẦM TRONG VCB NỘI BỘ

✅ CƠ HỘI THÀNH CÔNG CAO - Tỷ lệ hoàn tiền >95%

📋 CÁC TRƯỜNG HỢP HỖ TRỢ:
• Gửi nhầm số tài khoản cùng ngân hàng
• Gửi nhầm họ tên người nhận
• Gửi sai số tiền
• Giao dịch trùng lặp

⏰ THỜI GIAN XỬ LÝ:
• Trong giờ làm việc: 30-60 phút
• Ngoài giờ làm việc: 2-4 giờ
• Cuối tuần: 4-8 giờ

📱 CÁCH THỰC HIỆN:
1. Gọi Hotline 1900 1579 ngay lập tức
2. Cung cấp: Mã giao dịch, Số tài khoản, Họ tên
3. Xác nhận danh tính bằng OTP
4. Chờ xác nhận từ người nhận hoặc phong tỏa tài khoản

💡 TỈ LỆ THÀNH CÔNG CAO khi liên hệ trong vòng 30 phút!

🚫 LƯU Ý: Không được tự ý gọi điện người nhận để tránh bị lừa đảo!"""

def get_wrong_transfer_247_response():
    return """⏰ XỬ LÝ CHUYỂN TIỀN NHẦM DỊCH VỤ 24/7

🆘 HỖ TRỢ KHẨN CẤP 24 GIỜ TRONG NGÀY

🌙 DỊCH VỤ CHUYỂN TIỀN 24/7:
• Chuyển tiền nhanh mọi lúc mọi nơi
• Ngày lễ, cuối tuần vẫn hoạt động
• Giao dịch tức thì không cần chờ đợi
• Phí dịch vụ cao hơn nhưng tiện lợi

⚠️ XỬ LÝ NHẦM DỊCH VỤ 24/7:
📞 Hotline 24/7: 1900 1579
🕐 Phản hồi: Ngay lập tức trong 15 phút

🔄 QUY TRÌNH XỬ LÝ:
1. Liên hệ hotline ngay khi phát hiện lỗi
2. Cung cấp mã giao dịch và thông tin chi tiết  
3. Phong tỏa tài khoản tạm thời
4. Liên hệ người nhận để hoàn tiền
5. Giải phóng phong tỏa sau khi xử lý xong

💰 Chi phí xử lý: Theo quy định ngân hàng
⚡ Trường hợp khẩn: Phí cao hơn nhưng xử lý nhanh

🕰️ THỜI GIAN: 2-6 giờ (tùy trường hợp)"""

def get_wrong_transfer_foreign_response():
    return """🌍 XỬ LÝ CHUYỂN TIỀN NHẦM QUỐC TẾ

🏦 HỖ TRỢ CHUYỂN TIỀN QUỐC TẾ VÀ NGÂN HÀNG NƯỚC NGOÀI

💱 CÁC DỊCH VỤ CHUYỂN QUỐC TẾ:
• SWIFT Transfer - Chuyển qua hệ thống SWIFT
• TT Transfer - Telegraphic Transfer điện tử
• RTGS - Real Time Gross Settlement
• Corabank Transfer - Chuyển qua mạng ngân hàng liên kết

⚠️ XỬ LÝ CHUYỂN NHẦM QUỐC TẾ:

🏢 QUY TRÌNH PHỨC TẠP:
1. Ngân hàng Việt Nam thông báo cho ngân hàng nước ngoài
2. Ngân hàng nước ngoài liên hệ với người nhận
3. Người nhận xác nhận và đồng ý hoàn tiền
4. Quy trình hoàn tiền từ ngân hàng nước ngoài

⏰ THỜI GIAN XỬ LÝ:
• Liên lạc ngân hàng: 1-2 ngày làm việc
• Xử lý quốc tế: 3-7 ngày làm việc  
• Hoàn thành: 7-15 ngày làm việc

📋 THÔNG TIN CẦN THIẾT:
• Mã giao dịch SWIFT/TT
• Tên ngân hàng nước ngoài
• Mã SWIFT ngân hàng nhận
• Thông tin người nhận đầy đủ

💰 Chi phí: Theo biểu phí quốc tế + phí xử lý"""

def get_wrong_transfer_cash_response():
    return """💵 XỬ LÝ CHUYỂN TIỀN NHẦM DỊCH VỤ TIỀN MẶT

🏪 DỊCH VỤ CHUYỂN TIỀN MẶT:
• Chuyển tiền qua bưu điện
• Chuyển tiền qua Western Union
• Chuyển tiền qua MoneyGram  
• Chuyển tiền qua các điểm giao dịch

⚠️ XỬ LÝ CHUYỂN NHẦM TIỀN MẶT:

📞 LIÊN HỆ NGAY:
• Ngân hàng: 1900 1579
• Bưu điện: 1800 1234
• Western Union: 1900 1567

🕐 THỜI GIAN QUAN TRỌNG:
⏰ Trong vòng 2 giờ: Tỷ lệ hủy giao dịch cao
⏰ 2-24 giờ: Phụ thuộc vào việc người nhận có nhận tiền chưa
⏰ Sau 24 giờ: Rất khó xử lý, cần liên hệ người nhận trực tiếp

📋 CÁCH THỨC HOẠT ĐỘNG:
1. Người gửi kiểm tra mã nhận tiền (MTCN)
2. Liên hệ điểm giao dịch để hủy giao dịch  
3. Nếu chưa nhận: Hủy thành công 100%
4. Nếu đã nhận: Cần người nhận đồng ý hoàn tiền

💡 MẸO: Lưu giữ biên lai giao dịch và mã MTCN để tiện xử lý!

⚠️ LƯU Ý: Sau khi người nhận đã nhận tiền, việc hoàn tiền phụ thuộc hoàn toàn vào sự đồng ý của họ."""

# NẠP TIỀN ĐIỆN THOẠI
def get_phone_topup_response():
    return """📱 DỊCH VỤ NẠP TIỀN ĐIỆN THOẠI

💰 NẠP TIỀN THUẬN TIỆN VÀ NHANH CHÓNG

🌟 HỖ TRỢ TẤT CẢ NHÀ MẠNG:
• Viettel - Nạp từ 10,000đ
• Vinaphone - Nạp từ 20,000đ  
• MobiFone - Nạp từ 50,000đ
• Vietnamobile - Nạp từ 10,000đ
• iTel - Nạp từ 5,000đ
• Redi - Nạp từ 5,000đ
• GMobile - Nạp từ 10,000đ

💳 CÁC MỆNH GIÁ PHỔ BIẾN:
• 10,000đ - 50,000đ (Top-up nhỏ)
• 100,000đ - 500,000đ (Top-up trung bình)
• 1,000,000đ - 5,000,000đ (Top-up lớn)

⚡ THỰC HIỆN NGAY:
1. Ứng dụng Mobile Banking
2. Chọn "Nạp tiền điện thoại"  
3. Nhập số điện thoại và mệnh giá
4. Xác nhận giao dịch

🎯 TỰ ĐỘNG HÓA:
• Auto Top-up: Tự động nạp khi tài khoản < 50,000đ
• Lịch nạp: Hàng ngày/tuần/tháng
• Gói data: Kèm theo gói internet

💡 ƯU ĐIỂM:
• Hoàn tất trong 30 giây
• Không phí giao dịch
• Thanh toán từ tài khoản ngân hàng
• Thông báo kết quả ngay lập tức

📞 Hỗ trợ: 1900 1579"""

# THANH TOÁN HÓA ĐƠN
def get_bill_payment_info():
    bill_services = SUPPORT_SERVICES["thanh toán hóa đơn"]
    return """💳 DỊCH VỤ THANH TOÁN HÓA ĐƠN

🏦 THANH TOÁN ĐA DẠNG, TIỆN LỢI VÀ AN TOÀN

📊 CÁC LOẠI HÓA ĐƠN HỖ TRỢ:
• Thanh toán ngay lập tức - Giao dịch tức thì
• Đăng ký trích nợ tự động - Thanh toán định kỳ tự động

💡 Chọn dịch vụ mong muốn hoặc cho biết loại hóa đơn cần thanh toán!"""

def get_instant_bill_payment_response():
    return """⚡ THANH TOÁN HÓA ĐƠN NGAY LẬP TỨC

🏆 DỊCH VỤ THANH TOÁN TRỰC TUYẾN TOÀN DIỆN

📋 CÁC LOẠI HÓA ĐƠN HỖ TRỢ:
• ⚡ Điện - EVN (Hà Nội, HCM, Đà Nẵng...)
• 💧 Nước - SAWACO, CII, Cấp nước sạch
• 🌐 Internet - FPT, Viettel, VNPT, CMC...
• 📞 Điện thoại cố định - VNPT, Viettel, FPT
• 📱 Viễn thông di động - Tất cả nhà mạng
• 🏥 Bảo hiểm y tế, xã hội, thất nghiệp
• 🚗 Phí đăng ký xe, xe máy, ô tô
• 🏠 Phí dịch vụ chung cư, bãi xe
• 💳 Phí thẻ tín dụng
• 🎓 Học phí, lệ phí thi cử

📱 CÁCH THỨC HOẠT ĐỘNG:
1. Đăng nhập Mobile Banking
2. Chọn "Thanh toán hóa đơn"
3. Quét mã QR hoặc nhập mã khách hàng
4. Kiểm tra thông tin và số tiền
5. Xác nhận bằng vân tay/face ID

💰 GIỚI HẠN GIAO DỊCH:
• Tối thiểu: 1,000đ
• Tối đa: 1 tỷ đồng/ngày
• Phí: MIỄN PHÍ

⏰ THỜI GIAN: Thanh toán ngay lập tức

💡 ƯU ĐIỂM:
• Không cần photo hóa đơn
• Lưu lịch sử thanh toán
• Thông báo kết quả real-time
• Hỗ trợ 24/7"""

def get_auto_debit_registration_response():
    return """🔄 DỊCH VỤ TRÍCH NỢ TỰ ĐỘNG

⏰ TIẾT KIỆM THỜI GIAN - THANH TOÁN ĐỊNH KỲ TỰ ĐỘNG

🎯 DỊCH VỤ TRÍCH NỢ TỰ ĐỘNG:
• Điện, nước, internet cố định
• Bảo hiểm xã hội, y tế, thất nghiệp  
• Phí quản lý tài khoản ngân hàng
• Phí thẻ tín dụng
• Gói cước điện thoại, internet

📅 CHU KỲ THANH TOÁN:
• Hàng ngày - Dành cho phí dịch vụ nhỏ
• Hàng tuần - Phí tuần
• Hàng tháng - Hầu hết các loại phí
• Hàng quý - Phí quý
• Hàng năm - Bảo hiểm, phí dịch vụ lớn

⚙️ THIẾT LẬP:
1. Đăng nhập Mobile Banking
2. Chọn "Thanh toán tự động"
3. Chọn hóa đơn muốn đăng ký
4. Thiết lập chu kỳ và ngày thanh toán
5. Xác nhận bằng OTP

💰 THÔNG TIN CHI TIẾT:
• Miễn phí đăng ký và hủy
• Thay đổi thiết lập mọi lúc
• Nhận thông báo trước khi trích nợ
• Có thể tạm dừng hoặc hủy bất cứ lúc nào

🛡️ BẢO MẬT:
• Xác thực sinh trắc học
• Thông báo SMS/Email mỗi lần trích nợ
• Tra cứu lịch sử giao dịch chi tiết

⏰ THỜI GIAN: Đăng ký trong 5 phút"""

# CẬP NHẬT SINH TRẮC HỌC
def get_biometric_update_info():
    biometric_services = SUPPORT_SERVICES["cập nhật sinh trắc học"]
    return """👆 CẬP NHẬT SINH TRẮC HỌC

🔐 CÔNG NGHỆ BẢO MẬT HIỆN ĐẠI - AN TOÀN TUYỆT ĐỐI

🆔 DỊCH VỤ CẬP NHẬT SINH TRẮC HỌC:
• Cập nhật qua CCCD gắn chip - Công nghệ NFC hiện đại
• Cập nhật qua VNeID - Ứng dụng di động tiện lợi

💡 Chọn phương thức cập nhật phù hợp với bạn!"""

def get_cccd_update_response():
    return """🆔 CẬP NHẬT SINH TRẮC HỌC QUA CCCD GẮN CHIP

💳 THẺ CĂN CƯỚC CÔNG DÂN GẮN CHIP - CÔNG NGHỆ TIÊN TIẾN

🔍 THÔNG TIN CCCD GẮN CHIP:
• Chip điện tử tích hợp dữ liệu sinh trắc
• Công nghệ NFC (Near Field Communication)
• Lưu trữ: Vân tay, khuôn mặt, thông tin cá nhân
• Mã hóa dữ liệu theo chuẩn quốc tế

📱 QUY TRÌNH CẬP NHẬT:
1. Chuẩn bị CCCD gắn chip còn hiệu lực
2. Mở ứng dụng ngân hàng
3. Chọn "Cập nhật sinh trắc học"
4. Chạm CCCD vào mặt sau điện thoại
5. Đọc thông tin từ chip và xác nhận

⚡ THỜI GIAN: 2-5 phút
🎯 ĐỘ CHÍNH XÁC: >99.9%

🔒 BẢO MẬT DỮ LIỆU:
• Mã hóa AES 256-bit
• Không lưu trữ trên máy chủ
• Xóa dữ liệu sau khi hoàn thành
• Tuân thủ chuẩn bảo mật ISO 27001

💡 ƯU ĐIỂM:
• Cập nhật nhanh chóng
• Độ bảo mật cao nhất
• Không cần đến chi nhánh
• Sử dụng lâu dài, không cần cập nhật lại

⚠️ LƯU Ý:
• CCCD phải còn hiệu lực
• Điện thoại hỗ trợ NFC
• Kết nối internet ổn định"""

def get_vneid_update_response():
    return """📱 CẬP NHẬT SINH TRẮC HỌC QUA VN EID

🏛️ ỨNG DỤNG ĐỊNH DANH ĐIỆN TỬ QUỐC GIA

📋 THÔNG TIN VỀ VNEID:
• Ứng dụng chính thức của Bộ Công an
• Tích hợp thông tin căn cước công dân
• Xác thực danh tính online
• Hỗ trợ nhiều dịch vụ công

📲 CÁCH TẢI VÀ SỬ DỤNG:

📱 TẢI ỨNG DỤNG:
• iOS: App Store tìm "VNeID"
• Android: Google Play tìm "VNeID"  
• Website: https://dinhdien.so.gov.vn

🔑 KÍCH HOẠT TÀI KHOẢN:
1. Tải và cài đặt ứng dụng VNeID
2. Đăng ký tài khoản với thông tin CCCD
3. Xác thực bằng SMS OTP
4. Hoàn thiết hồ sơ cá nhân

⚡ CẬP NHẬT SINH TRẮC HỌC:
1. Mở ứng dụng ngân hàng
2. Chọn "Cập nhật qua VNeID"
3. Chọn "Đồng bộ từ VNeID"
4. Đăng nhập VNeID trong ứng dụng
5. Ủy quyền và xác nhận

🛡️ BẢO MẬT:
• Chứng thư số cá nhân
• Xác thực đa yếu tố
• Mã hóa end-to-end
• Log audit đầy đủ

💡 TIỆN ÍCH:
• Sử dụng cho nhiều dịch vụ khác
• Không cần mang theo CCCD
• Cập nhật thông tin tự động
• Hỗ trợ online 24/7

🎯 THỜI GIAN: 3-7 phút (tùy mạng)"""

def get_farewell_response():
    return SUPPORT_SERVICES["tạm biệt"]

def get_unknown_response(service=None):
    if service and service in SUPPORT_SERVICES:
        if isinstance(SUPPORT_SERVICES[service], dict):
            options = [key.title() for key in SUPPORT_SERVICES[service].keys()]
            return f"""❓ Xin lỗi, tôi chưa hiểu rõ yêu cầu của quý khách về "{service.title()}".

🤔 Tôi có thể hỗ trợ quý khách các tùy chọn sau:
{', '.join(options)}

📝 HOẶC quý khách có thể:
• Mô tả cụ thể hơn về nhu cầu
• Gõ "Hi" để bắt đầu lại
• Liên hệ Hotline: 1900 1579 (24/7)

Tôi sẵn sàng hỗ trợ quý khách một cách tốt nhất! 😊"""
        return f"""❓ Xin lỗi, tôi chưa hiểu rõ yêu cầu về "{service.title()}".

💡 Quý khách có thể:
• Chọn một mục trong menu chính
• Mô tả chi tiết hơn về nhu cầu
• Gõ "Hi" để bắt đầu lại

📞 Hỗ trợ trực tiếp: 1900 1579

Xin cảm ơn quý khách! 🙏"""
    return """❓ Xin lỗi quý khách, Bank-Soft BaSo chưa hiểu yêu cầu của quý khách.

🔍 Tôi có thể hỗ trợ:
• Chuyển tiền (ngay, hạn mức, xử lý nhầm)
• Nạp tiền điện thoại
• Thanh toán hóa đơn (ngay, tự động)
• Cập nhật sinh trắc học (CCCD, VNeID)

📝 CÁCH SỬ DỤNG:
• Gõ "Hi" để bắt đầu
• Nhập số thứ tự từ menu
• Mô tả cụ thể dịch vụ cần hỗ trợ

📞 Hỗ trợ trực tiếp: 1900 1579 (24/7)

Cảm ơn quý khách! 🙏"""

FINAL_RESPONSE_MAP = {
    "chuyển tiền ngay": get_instant_transfer_response,
    "thay đổi hạn mức": get_change_limit_response,
    "chuyển tiền trong VCB": get_wrong_transfer_vcb_response,
    "chuyển tiền nhanh 24/7": get_wrong_transfer_247_response,
    "chuyển qua ngân hàng nước ngoài": get_wrong_transfer_foreign_response,
    "chuyển tiền mặt": get_wrong_transfer_cash_response,
    "nạp tiền điện thoại": get_phone_topup_response,
    "thanh toán hóa đơn ngay": get_instant_bill_payment_response,
    "đăng ký trích nợ tự động": get_auto_debit_registration_response,
    "cập nhật qua CCCD gắn chip": get_cccd_update_response,
    "cập nhật qua VNeID": get_vneid_update_response,
}

def process_input(text, state):
    
    normalized = normalize_input(text)
    current_state = state["current_state"]
    
    logger.info(f"Processing input: '{text}' -> normalized: '{normalized}', current_state: '{current_state}'")
    
    # Farewell
    if normalized == "tạm biệt":
        state["current_state"] = "wait" 
        return get_farewell_response(), state
    
    # Greeting
    if normalized == "greeting":
        state["current_state"] = "main_menu"
        return get_greeting(), state
    
    # Direct service response
    if normalized in FINAL_RESPONSE_MAP:
        state["current_state"] = "wait" 
        return FINAL_RESPONSE_MAP[normalized](), state

    # Main menu or waiting state - allow any level navigation
    if current_state == "wait" or current_state == "main_menu":
        if normalized in SUPPORT_SERVICES and normalized != "tạm biệt":
            
            if normalized == "chuyển tiền":
                state["current_state"] = "transfer_menu"
                return get_transfer_info(), state
            elif normalized == "thanh toán hóa đơn":
                state["current_state"] = "bill_menu"
                return get_bill_payment_info(), state
            elif normalized == "cập nhật sinh trắc học":
                state["current_state"] = "biometric_menu"
                return get_biometric_update_info(), state
                
        return get_unknown_response(), state
    
    # Sub-menu navigation - allow going back to main or deeper levels
    if current_state != "wait" and current_state != "main_menu":
        if normalized in get_main_service_keys():
            state["current_state"] = "main_menu"
            return process_input(text, state)
            
        if current_state == "transfer_menu":
            if normalized == "chuyển nhầm/ lỗi":
                state["current_state"] = "wrong_transfer_menu"
                return get_wrong_transfer_info(), state
            elif "chuyển tiền" in normalized or "ngay" in normalized or "hạn mức" in normalized:
                transfer_services = SUPPORT_SERVICES["chuyển tiền"]
                for service_key in transfer_services.keys():
                    if service_key in normalized or any(word in normalized for word in normalized.split()):
                        if service_key in FINAL_RESPONSE_MAP:
                            state["current_state"] = "wait"
                            return FINAL_RESPONSE_MAP[service_key](), state
        
        elif current_state == "bill_menu":
            bill_services = SUPPORT_SERVICES["thanh toán hóa đơn"]
            for service_key in bill_services.keys():
                if service_key in normalized or any(word in normalized for word in normalized.split()):
                    if service_key in FINAL_RESPONSE_MAP:
                        state["current_state"] = "wait"
                        return FINAL_RESPONSE_MAP[service_key](), state
        
        elif current_state == "biometric_menu":
            biometric_services = SUPPORT_SERVICES["cập nhật sinh trắc học"]
            for service_key in biometric_services.keys():
                if service_key in normalized or any(word in normalized for word in normalized.split()):
                    if service_key in FINAL_RESPONSE_MAP:
                        state["current_state"] = "wait"
                        return FINAL_RESPONSE_MAP[service_key](), state

        elif current_state == "wrong_transfer_menu":
            wrong_transfer_services = SUPPORT_SERVICES["chuyển tiền"]["chuyển nhầm/ lỗi"]
            for service_key in wrong_transfer_services.keys():
                if service_key in normalized or any(word in normalized for word in normalized.split()):
                    if service_key in FINAL_RESPONSE_MAP:
                        state["current_state"] = "wait"
                        return FINAL_RESPONSE_MAP[service_key](), state

        return get_unknown_response(current_state.replace("_menu", "")), state
    
    return get_unknown_response(), state

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "Bank Chatbot API is running - Updated Version",
        "version": "2.0.0",
        "features": [
            "Professional responses",
            "Enhanced NLP recognition", 
            "Cross-menu navigation",
            "Fuzzy matching",
            "Comprehensive synonym support"
        ]
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Tin nhắn không được để trống"}), 400
        
        message = data['message']
        session_id = data.get('session_id', 'default')
        
        # Khởi tạo session nếu chưa có
        if session_id not in chat_sessions:
            chat_sessions[session_id] = {
                "current_state": "wait",
                "conversation_history": []
            }
        
        # Thêm vào lịch sử conversation
        chat_sessions[session_id]["conversation_history"].append({
            "user_message": message,
            "timestamp": "2025-11-19 20:37:18"
        })
        
        # Xử lý tin nhắn
        response, new_state = process_input(message, chat_sessions[session_id])
        chat_sessions[session_id] = new_state
        
        # Thêm bot response vào lịch sử
        chat_sessions[session_id]["conversation_history"].append({
            "bot_response": response,
            "timestamp": "2025-11-19 20:37:18"
        })
        
        logger.info(f"Session {session_id}: User '{message}' -> Bot response length: {len(response)} chars")
        
        # Lấy gợi ý trả lời cho state mới
        suggestions = get_quick_replies_for_state(new_state["current_state"])
        
        return jsonify({
            "response": response,
            "session_id": session_id,
            "state": new_state["current_state"],
            "suggestions": suggestions,
            "version": "2.0.0"
        })
        
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        return jsonify({"error": "Có lỗi xảy ra, vui lòng thử lại"}), 500

@app.route('/api/reset', methods=['POST'])
def reset_session():
    """Reset session chat"""
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default')
        
        if session_id in chat_sessions:
            chat_sessions[session_id] = {
                "current_state": "wait",
                "conversation_history": []
            }
        
        return jsonify({
            "message": "Session đã được reset",
            "session_id": session_id,
            "new_state": "wait"
        })
        
    except Exception as e:
        logger.error(f"Error resetting session: {str(e)}")
        return jsonify({"error": "Có lỗi xảy ra"}), 500

@app.route('/api/conversation/<session_id>', methods=['GET'])
def get_conversation_history(session_id):
    try:
        if session_id in chat_sessions:
            return jsonify({
                "session_id": session_id,
                "conversation_history": chat_sessions[session_id]["conversation_history"],
                "current_state": chat_sessions[session_id]["current_state"]
            })
        else:
            return jsonify({
                "session_id": session_id,
                "conversation_history": [],
                "current_state": "wait",
                "message": "Session not found"
            }), 404
            
    except Exception as e:
        logger.error(f"Error getting conversation history: {str(e)}")
        return jsonify({"error": "Có lỗi xảy ra"}), 500

@app.route('/api/suggestions/<state>', methods=['GET'])
def get_suggestions_for_state(state):
    try:
        suggestions = get_quick_replies_for_state(state)
        return jsonify({
            "state": state,
            "suggestions": suggestions
        })
    except Exception as e:
        logger.error(f"Error getting suggestions for state {state}: {str(e)}")
        return jsonify({"error": "Có lỗi xảy ra"}), 500

def get_quick_replies_for_state(state):
    """Trả về gợi ý trả lời dựa trên state hiện tại"""
    suggestions = []
    
    # Main menu suggestions
    if state == "main_menu":
        suggestions = [
            {"text": " Chuyển tiền", "value": "chuyển tiền", "icon": "🏦"},
            {"text": " Nạp tiền điện thoại", "value": "nạp tiền điện thoại", "icon": "📱"},
            {"text": " Thanh toán hóa đơn", "value": "thanh toán hóa đơn", "icon": "📄"},
            {"text": " Cập nhật sinh trắc học", "value": "cập nhật sinh trắc học", "icon": "👆"},
            {"text": " Tạm biệt", "value": "tạm biệt", "icon": "👋"}
        ]
    
    # Transfer menu suggestions
    elif state == "transfer_menu":
        suggestions = [
            {"text": "  Chuyển tiền ngay", "value": "chuyển tiền ngay", "icon": "⚡"},
            {"text": "  Thay đổi hạn mức", "value": "thay đổi hạn mức", "icon": "📈"},
            {"text": "  Chuyển nhầm/lỗi", "value": "chuyển nhầm/ lỗi", "icon": "⚠️"},
            {"text": "  Về menu chính", "value": "main_menu", "icon": "🏠"}
        ]
    
    # Wrong transfer menu suggestions
    elif state == "wrong_transfer_menu":
        suggestions = [
            {"text": "   Chuyển tiền trong VCB", "value": "chuyển tiền trong VCB", "icon": "🏦"},
            {"text": "   Chuyển tiền nhanh 24/7", "value": "chuyển tiền nhanh 24/7", "icon": "🕰️"},
            {"text": "   Chuyển qua ngân hàng nước ngoài", "value": "chuyển qua ngân hàng nước ngoài", "icon": "🌍"},
            {"text": "   Chuyển tiền mặt", "value": "chuyển tiền mặt", "icon": "💵"},
            {"text": "   Quay lại", "value": "transfer_menu", "icon": "🔙"}
        ]
    
    # Bill payment menu suggestions
    elif state == "bill_menu":
        suggestions = [
            {"text": "   Thanh toán hóa đơn ngay", "value": "thanh toán hóa đơn ngay", "icon": "⚡"},
            {"text": "   Đăng ký trích nợ tự động", "value": "đăng ký trích nợ tự động", "icon": "🤖"},
            {"text": "   Về menu chính", "value": "main_menu", "icon": "🏠"}
        ]
    
    # Biometric menu suggestions
    elif state == "biometric_menu":
        suggestions = [
            {"text": "   Cập nhật qua CCCD gắn chip", "value": "cập nhật qua CCCD gắn chip", "icon": "💳"},
            {"text": "   Cập nhật qua VNeID", "value": "cập nhật qua VNeID", "icon": "📱"},
            {"text": "   Về menu chính", "value": "main_menu", "icon": "🏠"}
        ]
    
    # Default suggestions for any state
    else:
        suggestions = [
            {"text": " Về menu chính", "value": "main_menu", "icon": "🏠"},
            {"text": " Bắt đầu lại", "value": "Hi", "icon": "🔄"},
            {"text": " Tạm biệt", "value": "tạm biệt", "icon": "👋"}
        ]
    
    return suggestions

if __name__ == '__main__':
    logger.info("🚀 Starting Enhanced Bank Chatbot API...")
    logger.info("✅ Features: Professional responses, Enhanced NLP, Cross-menu navigation")
    app.run(host='0.0.0.0', port=5000, debug=True)