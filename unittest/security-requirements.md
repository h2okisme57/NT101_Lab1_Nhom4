# Security Requirements – json_search()

Nhóm 04 – Lab 1

## 1. Security requirements

| ID | Requirement | Chống threat |
|---|---|---|
| SR-1 | Hệ thống chỉ trả về giá trị của `apiKey` cho role `admin`. | T1, T3 |
| SR-2 | Hệ thống chỉ trả về giá trị của `managementIpAddress` cho role `admin` hoặc `operator`. | T2 |
| SR-3 | Khi truy vấn một trường có trong `POLICY` mà role là `None` hoặc không nằm trong danh sách cho phép, hàm trả về list rỗng (deny by default). | T3 |
| SR-4 | Kiểm tra quyền áp dụng cho mọi kết quả, kể cả kết quả tìm thấy trong dict/list lồng nhau. | T4 |
| SR-5 | Role hợp lệ vẫn nhận đủ kết quả được phép (ví dụ viewer vẫn đọc được `issueSummary`), không chặn nhầm. | Bảo toàn chức năng |

## 2. Ánh xạ sang security test

| Test                                    | Kiểm tra   | Kỳ vọng                                  |
| ----------------------------------------| -----------| -----------------------------------------|
| `test_viewer_cannot_read_apikey`        | SR-1       | `[]`                                     |
| `test_operator_cannot_read_apikey`      | SR-1       | `[]`                                     |
| `test_viewer_cannot_read_management_ip` | SR-2       | `[]`                                     |
| `test_no_role_cannot_read_secret`       | SR-3       | `[]`                                     |
| `test_admin_can_read_apikey`            | SR-1, SR-4 | list chứa `SNMP-COMMUNITY-STRING-7f3a9c` |
| `test_viewer_can_read_issue_summary`    | SR-5       | list không rỗng                          |
