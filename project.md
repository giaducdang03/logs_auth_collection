# 📄 SRS – SSH Authentication Log Monitoring System

## 1. Introduction

### 1.1 Purpose

Tài liệu này mô tả yêu cầu cho hệ thống **SSH Authentication Log Monitoring System**, nhằm thu thập, lưu trữ và hiển thị lịch sử đăng nhập SSH trên hệ thống Linux (Ubuntu).

### 1.2 Scope

Hệ thống bao gồm:

* Backend: FastAPI (Python)
* Frontend: React + Vite + TypeScript
* Database: PostgreSQL
* Deployment: Docker & Docker Compose

Chức năng chính:

* Đọc log SSH từ hệ thống Ubuntu
* Lưu log vào database
* Cung cấp API để hiển thị, tìm kiếm, thống kê
* Giao diện dashboard và table log

---

## 2. Overall Description

### 2.1 Product Perspective

Hệ thống là một ứng dụng web gồm:

* 1 service backend (FastAPI)
* 1 service frontend (React)
* 1 database (PostgreSQL)
* 1 worker (có thể tích hợp trong backend hoặc riêng)

Nguồn dữ liệu chính:

* File log: `/var/log/auth.log`

---

### 2.2 Product Functions

#### Backend

* Đọc file log định kỳ (10 phút/lần)
* Parse log SSH
* Lưu record mới vào database
* Cung cấp API:

  * Authentication
  * Query logs (search/filter/sort)
  * Dashboard thống kê

#### Frontend

* Login system
* Hiển thị bảng log
* Search / filter / sort
* Dashboard thống kê user activity

---

### 2.3 User Classes

* **Admin**

  * Xem toàn bộ log
  * Truy cập dashboard
* **User (optional)**

  * Xem log theo quyền (future)

---

## 3. System Features

---

## 3.1 Log Collection Service

### Description

Service đọc log từ hệ thống Ubuntu và lưu vào DB.

### Functional Requirements

* FR-1: Hệ thống phải đọc file `/var/log/auth.log`
* FR-2: Hệ thống phải chạy mỗi 10 phút (cron / background task)
* FR-3: Chỉ lưu log mới (không duplicate)
* FR-4: Parse được các thông tin:

  * user
  * ip address
  * timestamp
  * ssh key (nếu có)
  * status (success / failed)

### Technical Note

* Có thể dùng:

  * file offset tracking
  * hoặc lưu last timestamp

---

## 3.2 Log Storage

### Database: PostgreSQL

#### Table: `ssh_logs`

| Column     | Type      | Description           |
| ---------- | --------- | --------------------- |
| id         | UUID      | Primary key           |
| username   | TEXT      | User SSH              |
| ip_address | TEXT      | IP remote             |
| login_time | TIMESTAMP | Thời gian login       |
| ssh_key    | TEXT      | Public key (optional) |
| status     | TEXT      | success / failed      |
| raw_log    | TEXT      | Raw log               |
| created_at | TIMESTAMP | Insert time           |

#### Constraints

* Unique index: (username, ip_address, login_time)

---

## 3.3 Authentication System

### Functional Requirements

* FR-5: User phải login để sử dụng hệ thống
* FR-6: Sử dụng JWT authentication
* FR-7: Password phải được hash (bcrypt)

### API

* POST `/auth/login`
* POST `/auth/register` (optional)

---

## 3.4 Log Viewer (Frontend + API)

### Functional Requirements

* FR-8: Hiển thị log dạng table
* FR-9: Pagination
* FR-10: Search theo:

  * username
  * ip
* FR-11: Filter:

  * time range
  * status
* FR-12: Sort:

  * login_time
  * username

### API

* GET `/logs`

Query params:

```
?page=
&page_size=
&username=
&ip=
&status=
&from_time=
&to_time=
&sort=
```

---

## 3.5 Dashboard

### Functional Requirements

* FR-13: Thống kê số lần login theo user
* FR-14: Thống kê theo thời gian (day/week/month)
* FR-15: Top IP login nhiều nhất

### API

* GET `/dashboard/user-frequency`
* GET `/dashboard/top-ip`
* GET `/dashboard/timeline`

---

## 4. Non-Functional Requirements

### 4.1 Performance

* Hệ thống phải xử lý tối thiểu:

  * 10k log/day
* API response < 500ms

---

### 4.2 Security

* JWT authentication
* Hash password
* Validate input
* Không expose file log trực tiếp

---

### 4.3 Reliability

* Không mất log khi restart
* Retry khi đọc file lỗi

---

### 4.4 Scalability

* Có thể scale backend bằng Docker
* Database có index tối ưu query

---

### 4.5 Maintainability

* Code tách layer:

  * controller
  * service
  * repository

---

## 5. System Architecture

### 5.1 High-level Architecture

```
+-------------+
|   React FE  |
+------+------+
       |
       v
+------+------+
|  FastAPI BE |
+------+------+
       |
       v
+-------------+
| PostgreSQL  |
+-------------+

       ^
       |
+-------------+
| Log Reader  |
| (Cron Job)  |
+-------------+
```

---

## 6. Deployment

### 6.1 Docker Services

* backend
* frontend
* postgres

### 6.2 Docker Compose

* Mount file:

  * `/var/log/auth.log` → container
* ENV config:

  * DB connection
  * JWT secret

---

## 7. Future Enhancements

* Real-time log (WebSocket)
* Alert khi login bất thường
* GeoIP mapping
* RBAC (role-based access)

---

## 8. Risks & Assumptions

### Risks

* Format log Ubuntu thay đổi
* Permission đọc `/var/log/auth.log`

### Assumptions

* App chạy trên Linux host có quyền đọc log
* Log format chuẩn của SSH

---