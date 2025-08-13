# 🛒 E-commerce API Pro

A **production-ready** E-commerce REST API built with **Django**, **Django REST Framework (DRF)**, **JWT Authentication**, and modern integrations like **Celery**, and **Redis**.  
This API provides endpoints for **user management, products, cart, orders, payments, reviews, notifications, and search** with rate-limiting and API documentation.

---

## 🚀 Features

### 🔐 Authentication & Authorization
- **JWT Authentication** (Access + Refresh tokens) using `djangorestframework-simplejwt`
- Token lifetime customization 
- Automatic token rotation & blacklist support

### 👤 Accounts
- User registration, login, logout
- Profile management

### 📦 Products
- Create, update, delete, and list products
- Product filtering, sorting, and search
- Category & tag-based browsing

### 🛒 Cart
- Add, update, and remove cart items
- Manage cart for authenticated users

### 📜 Orders
- Place and manage orders
- Order status tracking
- Integration with cart and payment system

### 💳 Payments
- **Payment Gateway** integration
- Secure server-to-server payment verification
- Configurable keys via `.env`

### ⭐ Reviews
- Add product reviews
- Ratings and comments
- Review moderation support

### 🔔 Notifications
- Real-time notifications via Celery
- Email/SMS/Push notifications (configurable)

### 🔍 Search
- Search products using `django-filter` and DRF filters
- Pagination and ordering

### 📄 API Documentation
- **Swagger UI** at `/api/docs/`
- **OpenAPI Schema** at `/api/schema/`

### ⚡ Performance & Security
- **Rate limiting** (60 requests/min for anonymous, 300 requests/min for authenticated)
- **CORS support**
- **Celery + Redis** for background tasks

---

## 🛠 Tech Stack
- **Backend**: Django, Django REST Framework
- **Auth**: JWT (djangorestframework-simplejwt)
- **Payments**: Khalti API
- **Background Tasks**: Celery + Redis
- **Database**: PostgreSQL / SQLite (dev)
- **Docs**: drf-spectacular (Swagger, OpenAPI)
- **Search & Filtering**: django-filter

---
