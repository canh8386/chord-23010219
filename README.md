# chord-23010219
Chord DHT simulation (Python) - key-value store
# Báo cáo
 Triển khai và kiểm thử thuật toán Chord (DHT) — mô phỏng lưu trữ key–value
## 1.	Mô tả bài toán và ứng dụng
### Bài toán
Trong hệ thống phân tán P2P, cần có một cơ chế ánh xạ từ khóa (key) đến nút (node) để lưu trữ và truy xuất dữ liệu mà không cần sử dụng bảng trung tâm. Cơ chế này phải đảm bảo hiệu quả ngay cả khi số lượng nút trong mạng lớn. Chord là một giao thức Distributed Hash Table (DHT) cung cấp khả năng ánh xạ này thông qua việc sử dụng hàm băm và vòng định danh modulo 2m2m. Mỗi nút trong mạng giữ một bảng ngón tay (finger table) để tăng tốc quá trình tìm kiếm, với độ phức tạp là O(logN)
### Ứng Dụng
Chord có thể được ứng dụng trong nhiều lĩnh vực, bao gồm:
•	Hệ thống lưu trữ phân tán
•	Mạng chia sẻ file
•	Hệ thống lưu trữ khóa-giá trị (caching)
•	Nền tảng blockchain và các ứng dụng phi tập trung (DApps)
## 2.	Thiết kế hệ thống

### 2.1.Không Gian Định Danh
•	Thiết kế không gian định danh từ 00 đến 2m−12m−1 cho phép ánh xạ các khóa vào một không gian có cấu trúc rõ ràng, giúp dễ dàng quản lý và tìm kiếm.
### 2.2.Cấu Trúc Node:
•	Mỗi nút trong mạng được thiết kế với các thành phần như ID, finger table, successor, predecessor và data. Điều này giúp tổ chức dữ liệu và thông tin về các nút một cách hiệu quả.

### 2.3.Các Thao Tác Chính:
•	Các thao tác như add_node, remove_node, store(key, value), lookup(key), và update_finger_tables được thiết kế để đảm bảo rằng hệ thống có thể quản lý các nút và dữ liệu một cách linh hoạt và hiệu quả.
•	Việc cập nhật finger tables và chuyển dữ liệu khi thêm hoặc xóa nút là rất quan trọng để duy trì tính nhất quán và độ tin cậy của hệ thống.
### 2.4.Tính Mở Rộng và Hiệu Quả:
•	Thiết kế của Chord cho phép hệ thống mở rộng dễ dàng khi có thêm nút mới mà không làm giảm hiệu suất tìm kiếm.
•	Độ phức tạp tìm kiếm O(logN) cho phép hệ thống xử lý hiệu quả ngay cả khi số lượng nút lớn.

## 3.	Cách tính toán ra kết quả
### 3.1. Băm khóa
Cách tính ID của khóa
Mỗi khóa được ánh xạ vào không gian định danh theo công thức:
id(key) = SHA1(key) mod (2^m)
Trong đó:
•	SHA1(key) là giá trị băm của khóa bằng thuật toán SHA-1.
•	m là số bit của không gian định danh.
•	Giá trị id(key) nằm trong khoảng từ 0 đến (2^m - 1).

Ví dụ với m = 5 (không gian định danh từ 0 đến 31):
•	Khóa "user1"
•	id("user1") = SHA1("user1") mod 32 = 14
•	Khóa "user2"
•	id("user2") = SHA1("user2") mod 32 = 4
•	Khóa "fileA"
•	id("fileA") = SHA1("fileA") mod 32 = 21

### 3.2. Xác định successor
Successor của một khóa kkk là node có id ≥ k nhỏ nhất trong vòng tròn.
Nếu không có node nào ≥ k thì successor chính là node nhỏ nhất trong hệ thống.
Ví dụ với tập node {1, 5, 9, 12, 16}:
•	Khóa "user1" có id = 14 → successor = 16 (vì 16 ≥ 14).
•	Khóa "user2" có id = 4 → successor = 5 (vì 5 ≥ 4).
•	Khóa "fileA" có id = 21 → successor = vòng tròn quay lại 1 (vì không node nào ≥ 21).

### 3.3. Finger table
Cách tính Finger Table
Finger table của một node n được tính theo công thức:
finger[i] = successor( (n + 2^i) mod (2^m) ), với i = 0..m-1
Trong đó:
•	n là ID của node.
•	m là số bit định danh.
•	successor(x) là node có ID lớn nhất >= x, hoặc quay vòng về node nhỏ nhất nếu không có node nào thoả mãn.

Ví dụ với node 1, m = 5 (không gian từ 0 đến 31):
•	finger[0] = successor((1 + 1) mod 32) = successor(2) = 5
•	finger[1] = successor((1 + 2) mod 32) = successor(3) = 5
•	finger[2] = successor((1 + 4) mod 32) = successor(5) = 5
•	finger[3] = successor((1 + 8) mod 32) = successor(9) = 9
•	finger[4] = successor((1 + 16) mod 32) = successor(17) = 1 (quay vòng về 1)


### 3.4. Khi thêm node
Ví dụ thêm node 7:
•	Một số khóa trước đó có successor là 9, nhưng nếu id(key) ≤ 7 thì successor mới sẽ là 7.
•	Finger table của các node được tính lại theo công thức trên.

### 3.5. Khi xóa node
Ví dụ xóa node 5:
•	Tất cả dữ liệu mà 5 quản lý (các key có id trong khoảng (1, 5]) sẽ chuyển cho successor = 7 hoặc 9 tùy topology.
•	Finger table cập nhật lại cho đúng.

 
 


