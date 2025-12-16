# Bank Chatbot Website

Một ứng dụng chatbot hỗ trợ khách hàng ngân hàng được xây dựng bằng NextJS (frontend) và Python Flask (backend).

## Tính năng

- **Giao diện hiện đại**: Sử dụng NextJS với Tailwind CSS để tạo giao diện đẹp và responsive
- **Chatbot thông minh**: Hỗ trợ nhiều ngôn ngữ (Tiếng Việt, Tiếng Anh, Tiếng Trung, Tiếng Nhật, Tiếng Hàn)
- **Dịch vụ ngân hàng**:
  - Chuyển tiền (chuyển tiền ngay, thay đổi hạn mức, xử lý chuyển nhầm)
  - Nạp tiền điện thoại
  - Thanh toán hóa đơn (thanh toán ngay, đăng ký trích nợ tự động)
  - Cập nhật sinh trắc học (qua CCCD gắn chip, qua VNeID)
- **Phản hồi nhanh**: Các nút tắt cho các dịch vụ phổ biến
- **Session management**: Quản lý phiên chat để duy trì ngữ cảnh cuộc trò chuyện

## Cấu trúc dự án

```
/workspace/
├── bank_chatbot_api.py          # Backend API Python (Flask)
└── frontend/                    # NextJS Frontend
    ├── app/
    │   ├── layout.tsx          # Layout chính
    │   ├── page.tsx            # Trang chatbot
    │   └── globals.css         # CSS toàn cục
    ├── package.json            # Dependencies
    ├── tailwind.config.js      # Cấu hình Tailwind
    ├── tsconfig.json           # Cấu hình TypeScript
    └── next.config.js          # Cấu hình NextJS
```

## Yêu cầu hệ thống

- **Python 3.8+**
- **Node.js 18+**
- **npm hoặc yarn**

## Hướng dẫn cài đặt và chạy

### Bước 1: Cài đặt backend Python

```bash
# Cài đặt Flask và các dependencies
pip install flask flask-cors

# Chạy backend API
python bank_chatbot_api.py
```

Backend sẽ chạy tại: `http://localhost:5000`

### Bước 2: Cài đặt frontend NextJS

```bash
# Di chuyển vào thư mục frontend
cd frontend

# Cài đặt dependencies
npm install
# hoặc
yarn install

# Chạy development server
npm run dev
# hoặc
yarn dev
```

Frontend sẽ chạy tại: `http://localhost:3000`

### Bước 3: Truy cập ứng dụng

Mở trình duyệt và truy cập `http://localhost:3000` để sử dụng chatbot.

## API Endpoints

### Health Check
```
GET /api/health
```

### Chat
```
POST /api/chat
Content-Type: application/json

{
  "message": "Hi",
  "session_id": "abc123"
}
```

### Reset Session
```
POST /api/reset
Content-Type: application/json

{
  "session_id": "abc123"
}
```

## Tính năng chatbot

### Dịch vụ được hỗ trợ:

1. **Chuyển tiền**
   - Chuyển tiền ngay lập tức
   - Thay đổi hạn mức chuyển tiền
   - Xử lý chuyển tiền nhầm/lỗi (trong VCB, 24/7, quốc tế, tiền mặt)

2. **Nạp tiền điện thoại**
   - Hướng dẫn nạp tiền điện thoại

3. **Thanh toán hóa đơn**
   - Thanh toán hóa đơn ngay lập tức
   - Đăng ký trích nợ tự động

4. **Cập nhật sinh trắc học**
   - Cập nhật qua CCCD gắn chip
   - Cập nhật qua ứng dụng VNeID

### Ngôn ngữ hỗ trợ:
- Tiếng Việt
- Tiếng Anh (English)
- Tiếng Trung (中文)
- Tiếng Nhật (日本語)
- Tiếng Hàn (한국어)

### Lệnh điều khiển:
- `Hi`, `Hello`, `Chào` - Bắt đầu cuộc trò chuyện
- `Tạm biệt`, `Bye`, `Quit` - Kết thúc cuộc trò chuyện
- Số từ 1-4 - Chọn dịch vụ từ menu chính

## Giao diện người dùng

- **Responsive Design**: Hoạt động tốt trên desktop và mobile
- **Real-time Chat**: Hiển thị tin nhắn theo thời gian thực
- **Loading Animation**: Hiệu ứng loading khi chờ phản hồi
- **Quick Replies**: Các nút tắt cho các dịch vụ phổ biến
- **Reset Button**: Nút để bắt đầu lại cuộc trò chuyện

## Công nghệ sử dụng

### Backend:
- **Python 3.8+**
- **Flask** - Web framework
- **Flask-CORS** - CORS support

### Frontend:
- **NextJS 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS
- **Lucide React** - Icons

## Tùy chỉnh

### Thay đổi API URL:
Chỉnh sửa trong `frontend/app/page.tsx`:
```typescript
const API_BASE_URL = 'http://localhost:5000/api'
```

### Thêm dịch vụ mới:
Chỉnh sửa trong `bank_chatbot_api.py`:
```python
SUPPORT_SERVICES = {
    "dịch_vụ_mới": "Mô tả dịch vụ",
    # ...
}
```

### Tùy chỉnh giao diện:
Chỉnh sửa các file trong `frontend/app/` và `tailwind.config.js`

## Production Deployment

### Backend:
- Deploy lên AWS, Google Cloud, hoặc Heroku
- Cấu hình environment variables
- Sử dụng Gunicorn thay vì Flask dev server

### Frontend:
- Build: `npm run build`
- Deploy lên Vercel, Netlify, hoặc AWS Amplify
- Cập nhật API URL cho production

## Giấy phép

Dự án này được tạo cho mục đích học tập và demo.

## Liên hệ

Được phát triển bởi MiniMax Agent.