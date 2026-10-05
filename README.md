# BÀI TẬP LỚN 1 - NHẬP MÔN TRÍ TUỆ NHÂN TẠO (CO3061)

## TRƯỜNG ĐẠI HỌC BÁCH KHOA - ĐHQG TP.HCM (HCMUT)

### TOPIC 1: MINESWEEPER GAME & AI SOLVER WITH HEURISTICS

---

## 👥 THÔNG TIN NHÓM THỰC HIỆN

| STT | Họ và tên | MSSV | Nhiệm vụ đảm nhiệm | Đóng góp (%) |
| :---: | :--- | :---: | :--- | :---: |
| 1 | **Trần Bá Minh Quân** | **2353015** | Thiết kế Giao diện (GUI), Tích hợp hệ thống & Viết Báo cáo PDF | **20%** |
| 2 | **Đặng Thế Lâm Anh** | **2352027** | Thiết kế Game Logic, Bàn cờ & Thuật toán loang (BFS/DFS) | **20%** |
| 3 | **Nguyễn Trần Hoàng Khánh** | **2352530** | Cài đặt tối ưu thuật toán BFS/DFS & Kiểm thử bàn cờ | **20%** |
| 4 | **Hồng Chấn Phước** | **2352963** | Nghiên cứu Heuristic xác suất & Cài đặt AI Auto-Solver | **20%** |
| 5 | **Hồ Gia Bảo** | **2352089** | Xây dựng Benchmark thực nghiệm tự động & Đánh giá hiệu năng | **20%** |

- **Giảng viên hướng dẫn:** TS. Nguyễn Quốc Minh
- **Học kỳ:** HK261

---

## 📂 CẤU TRÚC THƯ MỤC

```text
BTL_1/
├── src/
│   ├── game_logic.py        # Logic bàn cờ, rải mìn an toàn (First-click safe), BFS/DFS Flood Fill
│   ├── ai_solver.py         # AI Solver: Suy luận tất định, suy luận CSP tập hợp, Heuristic xác suất & độ lợi thông tin
│   ├── gui.py               # Giao diện đồ họa Tkinter (5x5, 9x9, 16x16, tùy biến, Timer, Cờ, Gợi ý, AI Step, Auto-Play)
│   └── benchmark.py         # Kiểm thử tự động hàng trăm ván đấu để thu thập thống kê Win Rate và Thời gian
├── main.py                  # File khởi động chính của ứng dụng
├── generate_report.py       # Mã nguồn tự động xuất báo cáo học thuật chuẩn PDF (ReportLab)
├── BaoCao_BTL1_Minesweeper_TranBaMinhQuan.pdf # Báo cáo PDF hoàn chỉnh theo chuẩn môn học
└── README.md                # Tài liệu hướng dẫn cài đặt và sử dụng
```

---

## 🚀 HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY CHƯƠNG TRÌNH

### 1. Yêu cầu môi trường

- Python 3.8 trở lên (đã được kiểm nghiệm hoàn hảo trên Python 3.11).
- Thư viện đồ họa: `tkinter` (mặc định đã có sẵn khi cài Python trên Windows/macOS/Linux).
- Thư viện xuất PDF (tùy chọn): `reportlab` (đã có sẵn trong môi trường).

### 2. Khởi chạy trò chơi Minesweeper

Mở Terminal/Command Prompt tại thư mục dự án và chạy:

```bash
python main.py
```

### 3. Các tính năng nổi bật trên giao diện (GUI)

- **Chọn kích thước bàn cờ:**
  - Nút bấm nhanh: `5x5 Mini (3 mìn)`, `9x9 Chuẩn (10 mìn)`, `16x16 (40 mìn)`.
  - Menu `Trò chơi -> Tùy chỉnh kích thước...` để tạo bàn cờ kích thước bất kỳ.
- **Tùy chọn thuật toán loang ô trống:**
  - Chọn Radio button `BFS` hoặc `DFS` ngay trên thanh công cụ để trải nghiệm cách mở loang ô.
- **Thanh trạng thái LCD:**
  - `🚩 010`: Bộ đếm số mìn còn lại.
  - `😊`: Mặt cười biểu cảm (bấm vào để chơi ván mới hoặc nhấn phím `F2`).
  - `⏱️ 000`: Đồng hồ đếm thời gian thực hiện.
- **Tác tử AI thông minh:**
  - `💡 Gợi ý AI (AI Hint)`: AI tính toán và bôi xanh ô có xác suất an toàn cao nhất kèm thông báo phân tích nguyên do.
  - `⚡ AI Đi 1 Bước`: AI tự động thực hiện 1 nước đi tối ưu (Cắm cờ hoặc Mở ô).
  - `🤖 AI Tự Giải (Auto-Play)`: AI tự động chơi liên tục từ đầu đến cuối với hoạt họa trực quan.

### 4. Chạy thực nghiệm tự động (Benchmark)

Để đo đạc tỷ lệ thắng và thời gian thực thi của AI trên 100 ván đấu:

```bash
python src/benchmark.py
```

### 5. Tạo lại file Báo cáo PDF (Nếu muốn)

```bash
python generate_report.py
```

File PDF đầu ra: `BaoCao_BTL1_Minesweeper_TranBaMinhQuan.pdf`.
