Ghost Shop — Django E-Commerce Platform

Ghost Shop is a full-featured responsive Django-based e-commerce platform developed by Frantsysk Boika. 
It showcases dynamic product filtering, secure checkout, user authentication and cart management — ideal for demonstrating backend proficiency in Django and scalable architecture.

---

Features:

- Dynamic product browsing by brand, category, and variants (size/color)
- Cart with single or bulk checkout, and session persistence
- Secure authentication, address management, and payment options, password management
- Promo code support with discount calculation
- Order confirmation, order history
- Wishlist with detailed product information
- All product images are hosted via [Cloudinary](https://cloudinary.com), enabling fast delivery and optimized media rendering.
- URLs are served directly from Cloudinary’s CDN — making the app scalable and media-efficient.
- Clean modular structure using Django best practices

---

Database Hosting:

This project uses a cloud-hosted PostgreSQL instance powered by [Neon]([https://neon.com]), allowing data persistence across all users and sessions.

- Centralized database accessible by deployed backend
- No local setup required — just clone and run
- Fully integrated with Django environment variables


Quick Start with Docker

Кequirements

- Docker installed on your machine
- Git clone access to this repository

Run the project

1. Clone the repository:

git clone https://github.com/yanchik-boika/ghost-shop.git
cd ghost-shop

Build and run the Docker container:
docker-compose up --build

Visit the site at http://localhost:8000

---

Test user:

- Username: testUser
- Password: asdfasdf2@

---

Project Structure

- ghost/ — Django app containing core logic (views, models, templates)
- templates/ghost/ — HTML pages (checkout, cart, orders)
- static/ — Custom CSS, icons, and images
- requirements.txt — Python package dependencies
- docker-compose.yml — Docker setup for local development

---

Technologies Used

- Python 3.10+
- Django 4.2+
- PostgreSQL (neon.com via Docker)
- Bootstrap 5
- Docker & Docker Compose








