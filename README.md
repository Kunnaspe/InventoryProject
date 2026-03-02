# Inventory Application

A Django-based inventory management system with admin-controlled product and department management.

## Features

- Admin-controlled inventory management
- Department and product organization
- Search functionality
- AWS deployment ready (EC2, RDS, CloudFront, Auto Scaling)

## Tech Stack

- **Backend:** Django 4.2
- **Database:** SQLite (development) / MySQL/MariaDB (production)
- **Server:** Gunicorn + Nginx
- **Cloud:** AWS (EC2, RDS, S3, CloudFront)

## Quick Start

### Prerequisites

- Python 3.10+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Kunnaspe/InventoryProject.git
   cd InventoryProject
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run database migrations:
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

7. Access the application:
   - Main site: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | Production | dev placeholder | Django secret key |
| `DJANGO_DEBUG` | No | `False` | Enable debug mode |
| `DJANGO_ALLOWED_HOSTS` | No | `localhost,127.0.0.1` | Allowed hosts |
| `DB_HOST` | No | - | Database host (uses SQLite if not set) |
| `DB_NAME` | No | - | Database name |
| `DB_USER` | No | - | Database user |
| `DB_PASSWORD` | No | - | Database password |
| `DB_PORT` | No | `3306` | Database port |

## Project Structure

```
InventoryProject/
├── DjangoProject/       # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── inventory/           # Inventory app
│   ├── models.py
│   ├── views.py
│   └── admin.py
├── templates/
├── manage.py
└── requirements.txt
```

## License

MIT License - see [LICENSE](LICENSE) for details.
