# 📸 PhotoJournal

**PhotoJournal** — is mini-version of Instagram, made on Django + DRF.
Allows users to create posts with images, to like, to comment, and to view profiles
as well as using JWT-authentication.

---

## 🚀 Technologies

- Python 3.11+
- Django 5.2
- Django REST Framework
- Simple JWT (access/refresh tokens)
- SQLite
- drf-yasg (Swagger UI)
- Pillow (for images)
<!-- - Celery + Redis -->

---

## 🔧 Instalation

1. Copy repository:
```bash
git clone https://github.com/0MAVM0/PhotoJournal.git
cd photojunior
```
2. Create and activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```
3. Download requirements:
```bash
pip install -r requirements.txt
```
4. Make migrations:
```bash
python manage.py migrate
```
5. Create super user:
```bash
python manage.py createsuperuser
```
6. Run server:
```bash
python manage.py runserver
```

---

## 📁 Structure

| Applications | Purpose |
|:-----------|:-----------|
| users | Registrations, profiles |
| posts | Posts with photoes |
| comments | Comments on posts |
| likes | Likes |
| follows | Follows |
| web | Web-site based on API |

---

## 🧪 Swagger documentation

- After running server:
    1. go through → http://127.0.0.1:8000/swagger/
    2. or → /redoc/
