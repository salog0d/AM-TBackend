# Athlete Progress Monitoring System

A comprehensive Django-based web application designed to track and monitor athlete performance across multiple sports disciplines. This system enables coaches to manage their athletes, track progress, and make data-driven decisions to optimize athletic performance.

## Features

- **User Role Management**: Three-tier user system with Athletes, Coaches, and Administrators
- **Multi-Sport Support**: Tracking for 18+ different sports disciplines
- **Coach-Athlete Relationship**: Direct connection between coaches and their athletes
- **Profile Management**: Complete user profiles with personal information and profile pictures
- **Performance Tracking**: Monitor progress and athletic development
- **Authentication & Authorization**: Secure role-based access control
- **Responsive Design**: Accessible from any device

## Technology Stack

- **Backend**: Django (Python web framework)
- **Database**: SQLite (development) / PostgreSQL (production)
- **Architecture**: Model-View-Controller (MVC) pattern
- **Authentication**: Django's built-in authentication system with custom extensions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/athlete-monitoring.git
cd athlete-monitoring
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env file with your configurations
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

8. Access the application at http://127.0.0.1:8000/

## Project Structure

```
athlete_monitoring/
│
├── manage.py
├── athlete_monitoring/       # Project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── core/                     # Core application
│   ├── models.py             # Database models (CustomUser, etc.)
│   ├── views.py              # View controllers
│   ├── forms.py              # Form definitions
│   ├── admin.py              # Admin panel customizations
│   ├── urls.py               # URL routing
│   └── templates/            # HTML templates
│
├── static/                   # Static files (CSS, JS, images)
│
└── media/                    # User-uploaded files
    └── profile_pictures/     # User profile images
```

## Data Models

### CustomUser Model

The CustomUser model extends Django's AbstractUser and includes:

- Role-based distinctions (Athlete, Coach, Admin)
- Discipline specification from 18 supported sports
- Profile information (name, date of birth, contact details)
- Coach-athlete relationship through foreign keys
- Validation to ensure proper role relationships

## Usage

### Administrator Tasks
- Manage all users in the system
- Create and assign coaches to disciplines
- Monitor system usage and performance

### Coach Tasks
- Manage a roster of athletes
- Track athlete progress and performance
- Generate reports and analytics

### Athlete Tasks
- View personal progress metrics
- Access training schedules and recommendations
- Update personal profile information

## Development

### Adding New Features

1. Create a feature branch:
```bash
git checkout -b feature/new-feature-name
```

2. Implement your changes
3. Write tests for your feature
4. Submit a pull request

### Running Tests

```bash
python manage.py test
```

## Deployment

### Production Setup

1. Update settings for production environment:
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
```

2. Set up a production database (PostgreSQL recommended)
3. Configure static file serving
4. Set up HTTPS with a valid SSL certificate
5. Deploy using Gunicorn/uWSGI and Nginx

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Submit a pull request
