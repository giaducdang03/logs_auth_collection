# 📄 Database Schema – SSH Log Monitoring System

## 1. Overview

Hệ thống sử dụng **PostgreSQL** để lưu trữ:

* Thông tin user đăng nhập hệ thống
* Log SSH từ Ubuntu
* Session đăng nhập portal

---

## 2. Tables

---

## 2.1 `users`

### Description

Lưu thông tin tài khoản đăng nhập hệ thống.

### Schema

| Column        | Type                     | Nullable | Default           | Description      |
| ------------- | ------------------------ | -------- | ----------------- | ---------------- |
| id            | UUID                     | ❌        | gen_random_uuid() | Primary key      |
| username      | TEXT                     | ❌        |                   | Tên đăng nhập    |
| password_hash | TEXT                     | ❌        |                   | Mật khẩu đã hash |
| is_active     | BOOLEAN                  | ❌        | TRUE              | Trạng thái user  |
| created_at    | TIMESTAMP WITH TIME ZONE | ❌        | now()             | Thời gian tạo    |

### Constraints

* `username` UNIQUE

---

## 2.2 `ssh_logs`

### Description

Lưu log đăng nhập SSH từ hệ thống Ubuntu (`/var/log/auth.log`).

### Schema

| Column      | Type                     | Nullable | Default           | Description                    |
| ----------- | ------------------------ | -------- | ----------------- | ------------------------------ |
| id          | UUID                     | ❌        | gen_random_uuid() | Primary key                    |
| username    | TEXT                     | ✅        |                   | User SSH                       |
| ip_address  | INET                     | ✅        |                   | IP remote                      |
| login_time  | TIMESTAMP WITH TIME ZONE | ❌        |                   | Thời gian login                |
| status      | TEXT                     | ❌        |                   | success / failed               |
| auth_method | TEXT                     | ✅        |                   | password / publickey / unknown |
| ssh_key     | TEXT                     | ✅        |                   | Public key nếu dùng key        |
| raw_log     | TEXT                     | ❌        |                   | Nội dung log gốc               |
| created_at  | TIMESTAMP WITH TIME ZONE | ❌        | now()             | Thời gian insert               |

---

### Constraints

* `status` ∈ ('success', 'failed')
* `auth_method` ∈ ('password', 'publickey', 'unknown')

---

### Indexes

| Index Name                    | Columns                        | Purpose           |
| ----------------------------- | ------------------------------ | ----------------- |
| idx_ssh_logs_username         | (username)                     | Search theo user  |
| idx_ssh_logs_ip               | (ip_address)                   | Filter theo IP    |
| idx_ssh_logs_login_time       | (login_time DESC)              | Filter time range |
| idx_ssh_logs_status           | (status)                       | Filter trạng thái |
| idx_ssh_logs_user_time        | (username, login_time DESC)    | Query phổ biến    |
| idx_ssh_logs_user_status_time | (username, status, login_time) | Dashboard         |

---

### Unique Constraint

Ngăn duplicate log:

| Constraint Name | Columns                                    |
| --------------- | ------------------------------------------ |
| uniq_ssh_log    | (username, ip_address, login_time, status) |

---

## 2.3 `user_sessions`

### Description

Lưu session login vào portal.

### Schema

| Column     | Type                     | Nullable | Default           | Description        |
| ---------- | ------------------------ | -------- | ----------------- | ------------------ |
| id         | UUID                     | ❌        | gen_random_uuid() | Primary key        |
| user_id    | UUID                     | ❌        |                   | FK → users.id      |
| login_time | TIMESTAMP WITH TIME ZONE | ❌        | now()             | Thời gian login    |
| ip_address | INET                     | ✅        |                   | IP client          |
| user_agent | TEXT                     | ✅        |                   | Trình duyệt/device |

---

### Relationships

* `user_sessions.user_id` → `users.id` (Many-to-One)

---

## 3. ERD (Entity Relationship Diagram)

```text
users
  └── id (PK)
       ↑
       │
user_sessions
  └── user_id (FK)

ssh_logs
  (independent)
```

---

## 4. Data Flow

### Log ingestion flow

1. Read `/var/log/auth.log`
2. Parse log
3. Insert vào `ssh_logs`
4. Skip nếu duplicate (unique constraint)

---

## 5. Query Use Cases

### 5.1 Search logs

* Theo username
* Theo IP
* Theo time range
* Theo status

---

### 5.2 Dashboard

#### Login frequency per user

```sql
SELECT username, COUNT(*)
FROM ssh_logs
WHERE status = 'success'
GROUP BY username;
```

#### Top IP

```sql
SELECT ip_address, COUNT(*)
FROM ssh_logs
GROUP BY ip_address
ORDER BY COUNT(*) DESC;
```

#### Timeline

```sql
SELECT date_trunc('hour', login_time), COUNT(*)
FROM ssh_logs
GROUP BY 1;
```

---

## 6. Scaling Strategy

### Khi dữ liệu lớn:

* Partition theo `login_time` (monthly)
* Archive log cũ
* Dùng materialized view cho dashboard

---

## 7. Notes

* Không liên kết `ssh_logs` với `users`:

  * vì SSH user ≠ hệ thống user
* `INET` được dùng để tối ưu query IP
* `raw_log` giúp debug parsing

---

## 8. Future Enhancements

* GeoIP:

  * country
  * city
* Suspicious detection:

  * brute-force login
* Alert system

---