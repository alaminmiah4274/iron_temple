# 🏋️ Iron Temple - Gym Management System API

![Django REST Framework](https://img.shields.io/badge/Django-REST%20Framework-green)
![JWT Authentication](https://img.shields.io/badge/JWT-Authentication-orange)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)

A complete gym management system backend built with Django REST Framework, featuring membership subscriptions, class bookings, payment processing, and analytics.

## ✨ Features

- 🧘‍♂️ Fitness Classes Management
- 💳 Membership Plans
- 🔁 Subscriptions Tracking
- 📅 Booking System
- 👥 Attendance Tracking
- 💰 Payment Handling & Reports
- 📊 Comprehensive Reporting System
- ✉️ User Feedback
- 🔐 JWT Authentication with Djoser
- 📄 Swagger API Documentation with `drf_yasg`
- 📅 Role Based Access Control: Admin, Staff, Member

## 📦 Tech Stack

- **Backend**: Django, Django REST Framework
- **Authentication**: JWT (via Djoser)
- **API Documentation**: Swagger UI (via drf_yasg)
- **Database**: PostgreSQL
- **Other Tools**: Django Admin, DRF Browsable API

## API Documentation

Swagger documentation is available at:

```
https://127.0.0.1:8000/swagger/
```

Redoc documentation is available at:

```
https://127.0.0.1:8000/swagger/
```

## Environment Variables

Create a `.env` file in the root directory and add the following:

```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
ALLOWED_HOST=*
EMAIL_HOST=your_email
```

## 🚀 Installation

#### Prerequisites

- Python 3.10+
- PostgreSQL 12+

#### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/iron-temple.git
   cd iron-temple
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the project
2.  Create your feature branch (git checkout -b feature/AmazingFeature)
3.  Commit your changes (git commit -m 'Add some AmazingFeature')
4.  Push to the branch (git push origin feature/AmazingFeature)
5.  Open a Pull Request

## License

    Distributed under the MIT License. See LICENSE for more information.

## Contact

Project Maintainer - Al Amin Miah <br>
Email: alaminmiah4274@gmail.com <br>
Linkedin: https://www.linkedin.com/in/al-amin-miah-71552a1b1 <br>
