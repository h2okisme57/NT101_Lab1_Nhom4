# Threat Model – json_search()

Nhóm 04 – Lab 1

## 1. Bối cảnh

`json_search(key, input_object, role=None)` tìm đệ quy một key trong dữ liệu JSON trả về từ API giám sát hạ tầng mạng (`test_data.py`) và trả về list các cặp `{key: value}`. Hàm được nhiều loại người dùng gọi với quyền khác nhau. Mô hình phân tích: STRIDE.

## 2. (a) Actor / role

| Role                    | Mục đích gọi hàm                                   | Được đọc                                        |
| ------------------------| ---------------------------------------------------| ------------------------------------------------|
| admin                   | Quản trị hệ thống, cấu hình thiết bị               | `apiKey`, `managementIpAddress`, `issueSummary` |
| operator                | Vận hành, xử lý sự cố, cần IP để truy cập thiết bị | `managementIpAddress`, `issueSummary`           |
| viewer                  | Theo dõi tổng quan tình trạng sự cố                | `issueSummary`                                  |
| Không có role / role lạ | Không hợp lệ                                       | Không được đọc trường nào                       |

## 3. (b) Asset nhạy cảm trong dữ liệu trả về

| Asset | Ví dụ trong test_data.py | Mức độ | Hậu quả nếu lộ |
|---|---|---|---|
| `apiKey` | `SNMP-COMMUNITY-STRING-7f3a9c` | Cao | Kẻ tấn công dùng SNMP community string để đọc/ghi cấu hình thiết bị |
| `managementIpAddress` | `10.10.20.21` | Trung bình | Lộ sơ đồ mạng quản trị, làm mục tiêu tấn công |
| `serialNumber`, `macAddress`, `hostname` | `FCW1234L0UZ`, `50:60:ab:cd:70:80`, `leaf2.abc.inc` | Thấp–Trung bình | Định danh thiết bị, hỗ trợ trinh sát |

## 4. (c) Trust boundary bị bỏ qua

Ranh giới tin cậy nằm giữa **người gọi hàm** (có thể là viewer, quyền thấp) và **dữ liệu API giám sát** (chứa thông tin xác thực của thiết bị). Phiên bản gốc của `json_search()` bỏ qua ranh giới này:

- Không import `policy.py`, hàm không biết bảng phân quyền.
- Không có tham số `role`, không phân biệt được ai đang gọi.
- `ret_val.append(temp)` thêm kết quả ngay khi gặp key, không kiểm tra quyền.
- `return ret_val` trả toàn bộ dữ liệu cho người gọi mà không qua kiểm soát truy cập nào.

## 5. (d) Threat theo STRIDE

| ID | STRIDE | Mô tả threat | Ví dụ |
|---|---|---|---|
| T1 | Information Disclosure | Viewer đọc được SNMP community string | `json_search("apiKey", data, role="viewer")` trả về secret |
| T2 | Information Disclosure | Viewer đọc được IP quản trị | `json_search("managementIpAddress", data, role="viewer")` |
| T3 | Elevation of Privilege | Gọi hàm không truyền role (`None`) hoặc role giả (`"root"`) để vượt qua kiểm tra, có quyền như admin | `json_search("apiKey", data)` |
| T4 | Information Disclosure | Chỉ kiểm tra ở tầng ngoài, secret nằm trong dict/list lồng sâu vẫn bị trả về | `apiKey` nằm trong `connectedDevice` → `deviceDetails` |
