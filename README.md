# ChatGPT used for creating above backend system

prompt used :
```

help me Build a simple transaction backend system that maintains a wallet for each client in django. make it role based where only admin can call certain apis and user can call only his apis. In this system admin can credit and debit wallet balance. user can create an order from available balance from his wallet. 

apis to create
1. POST /admin/wallet/credit
2. POST /admin/wallet/debit
3. POST /orders - create order
4. GET /orders/{order_id} - get order details
5. GET /wallet/balance - get wallet balance

make the system scalable, reliable with proper error handling.

````


# 💳 Wallet & Order Management Backend (Django)

A simple, scalable, and role-based backend system built with Django & Django REST Framework that manages user wallets and order transactions.

---

# 🚀 Features

* Role-based access control (Admin & User)
* Wallet management (credit/debit)
* Order creation using wallet balance
* Transaction logging
* JWT-based authentication
* Atomic operations to prevent race conditions

---

# 🧠 System Roles

### 👨‍💼 Admin

* Credit user wallet
* Debit user wallet

### 👤 User

* Create orders using wallet balance
* View own orders
* Check wallet balance

---

# ⚙️ Tech Stack

* Django
* Django REST Framework (DRF)
* JWT Authentication (`simplejwt`)

---

# 📁 Project Structure

```
wallet_system/
 ├── accounts/     # Custom user model
 ├── wallet/       # Wallet & transactions
 ├── orders/       # Order management
 ├── walletSystem/       # Order management
```

---

# 🔐 Authentication

This project uses **JWT (JSON Web Token)** authentication.

## Get Token

```
POST /api/token/
```

### Request Body

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

### Response

```json
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}
```

---

# 📡 API Endpoints

---

## 1️⃣ Admin: Credit Wallet

```
POST /api/admin/wallet/credit
```

### Headers

```
Authorization: Bearer <admin_token>
```

### Request Body

```json
{
  "user_id": 2,
  "amount": 1000
}
```

### Response

```json
{
  "message": "Wallet credited successfully"
}
```

---

## 2️⃣ Admin: Debit Wallet

```
POST /api/admin/wallet/debit
```

### Headers

```
Authorization: Bearer <admin_token>
```

### Request Body

```json
{
  "user_id": 2,
  "amount": 500
}
```

### Response

```json
{
  "message": "Wallet debited successfully"
}
```

### Error

```json
{
  "error": "Insufficient balance"
}
```

---

## 3️⃣ User: Create Order

```
POST /api/orders
```

### Headers

```
Authorization: Bearer <user_token>
```

### Request Body

```json
{
  "amount": 200
}
```

### Response

```json
{
  "order_id": 1
}
```

### Error

```json
{
  "error": "Insufficient balance"
}
```

---

## 4️⃣ User: Get Order Details

```
GET /api/orders/{order_id}
```

### Headers

```
Authorization: Bearer <user_token>
```

### Response

```json
{
  "id": 1,
  "amount": 200,
  "status": "CREATED"
}
```

### Error

```json
{
  "error": "Order not found"
}
```

---

## 5️⃣ User: Get Wallet Balance

```
GET /api/wallet/balance
```

### Headers

```
Authorization: Bearer <user_token>
```

### Response

```json
{
  "balance": 800
}
```

---

# 🧱 Database Models

### User

* Custom user model with `is_admin` flag

### Wallet

* One-to-one with user
* Stores current balance

### Transaction

* Tracks credit/debit history

### Order

* Stores user orders and amount

---

# 🔄 Transaction Safety

To ensure consistency and avoid race conditions:

* Uses `transaction.atomic()`
* Uses `select_for_update()` for row-level locking
* Prevents double spending

---

# ⚠️ Error Handling

| Status Code | Meaning      |
| ----------- | ------------ |
| 400         | Bad Request  |
| 401         | Unauthorized |
| 403         | Forbidden    |
| 404         | Not Found    |
| 500         | Server Error |

---

# 🧪 Setup Instructions

## 1. Install Dependencies

```
pip install django djangorestframework djangorestframework-simplejwt
```

---

## 2. Run Migrations

```
python manage.py makemigrations
python manage.py migrate
```

---

## 3. Create Admin User

```
python manage.py createsuperuser
```

Then set:

* `is_admin = True`

---

## 4. Run Server

```
python manage.py runserver
```

---

# 🔐 Authentication Flow

1. Get JWT token
2. Pass token in headers:

```
Authorization: Bearer <token>
```

---
