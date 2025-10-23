# Beauty Salon Booking System

A complete, production-ready beauty salon website with booking system, built with Django and optimized for SEO and scalability.

## 🎯 Features

### Core Functionality
- ✅ **Homepage** with featured services and stylists
- ✅ **Services Catalog** with detailed descriptions and pricing
- ✅ **Staff Profiles** with bio and services offered
- ✅ **Multi-Step Booking System** (Service → Stylist → Date/Time → Confirm)
- ✅ **Customer Dashboard** to view and manage bookings
- ✅ **Contact Form** with email notifications
- ✅ **About Page** with team and opening hours

### Authentication & Notifications
- ✅ **Email Authentication** via django-allauth
- ✅ **Phone Verification** via OTP (SMS)
- ✅ **Magic Link** login support
- ✅ **Booking Confirmations** via Email & SMS
- ✅ **Appointment Reminders**

### Admin Features
- ✅ **Comprehensive Admin Panel** with Django Admin
- ✅ **Service Management** (CRUD operations)
- ✅ **Staff Management** with service assignments
- ✅ **Booking Management** with status tracking
- ✅ **Customer Management** with verification status
- ✅ **Opening Hours Configuration**
- ✅ **Time Slot Management**

### API (REST)
- ✅ **RESTful API** with Django REST Framework
- ✅ **JWT Authentication** for secure API access
- ✅ **API Endpoints** for services, staff, bookings, time slots
- ✅ **Rate Limiting** (100/hour anonymous, 1000/hour authenticated)
- ✅ **API Documentation** (auto-generated)

### SEO Optimization
- ✅ **Server-Side Rendering** (SEO-friendly)
- ✅ **Meta Tags** (Title, Description, Keywords)
- ✅ **Open Graph** tags for social media
- ✅ **Twitter Card** support
- ✅ **Canonical URLs**
- ✅ **Sitemap.xml** (dynamic)
- ✅ **Robots.txt** configuration
- ✅ **JSON-LD** structured data (schema.org)
- ✅ **Semantic URLs** (slug-based)

### Design & UX
- ✅ **Responsive Design** (mobile-first)
- ✅ **Minimalist UI** with Pico.css
- ✅ **HTMX** for enhanced interactivity (optional)
- ✅ **Accessible** design principles
- ✅ **Loading States** and error handling
- ✅ **Custom 404/500** error pages

### Technical Features
- ✅ **Modular Architecture** (easily extendable)
- ✅ **Type Hints** (Python 3.8+)
- ✅ **Adapter Pattern** for email/SMS (swappable backends)
- ✅ **Concurrency Handling** (booking conflicts)
- ✅ **Database Transactions**
- ✅ **Middleware** for logging
- ✅ **Health Check** endpoint
- ✅ **Caching** support (Redis optional)
- ✅ **Celery** task queue (optional)
- ✅ **Docker** support
- ✅ **Environment-based** configuration

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL (or SQLite for local development)
- Redis (optional, for caching and Celery)

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd mira_app
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Copy environment variables:**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run migrations:**
```bash
python manage.py migrate
```

6. **Seed demo data:**
```bash
python manage.py seed_demo
```

7. **Create superuser (if not using seed_demo):**
```bash
python manage.py createsuperuser
```

8. **Run development server:**
```bash
python manage.py runserver
```

Visit http://localhost:8000 to see your application!

### Using Makefile

Alternatively, use the provided Makefile:

```bash
# Install dependencies
make install

# Run migrations and seed data
make migrate
make seed

# Start development server
make dev

# Run tests
make test

# Format code
make format

# Run linters
make lint
```

### Using Docker

1. **Build and run with Docker Compose:**
```bash
docker-compose up --build
```

2. **Run migrations:**
```bash
docker-compose exec web python manage.py migrate
```

3. **Seed demo data:**
```bash
docker-compose exec web python manage.py seed_demo
```

Visit http://localhost:8000

## 📁 Project Structure

```
beauty_salon/
├── config/                 # Django configuration
│   ├── settings/           # Environment-specific settings
│   │   ├── base.py         # Base settings
│   │   ├── local.py        # Development settings
│   │   └── production.py   # Production settings
│   ├── urls.py             # Main URL configuration
│   ├── wsgi.py             # WSGI entry point
│   └── asgi.py             # ASGI entry point
├── apps/                   # Django applications
│   ├── core/               # Core utilities
│   │   ├── adapters/       # Email/SMS adapters
│   │   ├── seo/            # SEO utilities and JSON-LD
│   │   ├── middleware.py   # Custom middleware
│   │   └── health.py       # Health check endpoint
│   ├── accounts/           # User authentication
│   │   ├── models.py       # Customer model with OTP
│   │   ├── views.py        # Auth views
│   │   └── forms.py        # Auth forms
│   ├── booking/            # Booking system
│   │   ├── models.py       # Service, Staff, Booking models
│   │   ├── views.py        # Booking flow views
│   │   └── admin.py        # Admin customizations
│   ├── sitecontent/        # Static pages
│   │   ├── views.py        # Home, About, Contact
│   │   └── models.py       # Contact form model
│   └── api/                # REST API
│       ├── views.py        # API viewsets
│       ├── serializers.py  # DRF serializers
│       └── urls.py         # API routes
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   ├── components/         # Reusable components
│   ├── booking/            # Booking templates
│   ├── sitecontent/        # Static page templates
│   ├── accounts/           # Account templates
│   ├── emails/             # Email templates
│   └── errors/             # Error pages
├── static/                 # Static files
│   └── css/                # Custom CSS
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── Makefile                # Automation commands
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

Key environment variables in `.env`:

```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password

# SMS (optional)
SMS_BACKEND=console  # or 'twilio'
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
TWILIO_PHONE_NUMBER=your-number

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# SEO
SITE_DOMAIN=localhost:8000
SITE_NAME=Beauty Salon
```

## 🧪 Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps

# Run specific app tests
pytest apps/booking/

# Generate HTML coverage report
pytest --cov=apps --cov-report=html
```

## 📊 API Documentation

### Authentication

The API uses JWT authentication:

```bash
# Get access token
POST /api/v1/auth/token/
{
  "email": "user@example.com",
  "password": "password"
}

# Response
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

# Use token in requests
Authorization: Bearer <access_token>
```

### Key Endpoints

```
GET    /api/v1/                    # API root
GET    /api/v1/services/           # List services
GET    /api/v1/services/{slug}/    # Service detail
GET    /api/v1/staff/              # List staff
GET    /api/v1/staff/{slug}/       # Staff detail
GET    /api/v1/staff/{slug}/available_slots/  # Available time slots
GET    /api/v1/time-slots/         # List time slots
GET    /api/v1/bookings/           # List user's bookings
POST   /api/v1/bookings/           # Create booking
POST   /api/v1/bookings/{id}/cancel/  # Cancel booking
GET    /api/v1/profile/            # Get user profile
PUT    /api/v1/profile/            # Update user profile
POST   /api/v1/register/           # Register new user
POST   /api/v1/auth/token/         # Get JWT token
POST   /api/v1/auth/token/refresh/ # Refresh JWT token
```

### API Rate Limits
- Anonymous: 100 requests/hour
- Authenticated: 1000 requests/hour

## 🎨 Customization

### Branding

Update branding in templates and settings:

1. **Site Name**: Edit `SITE_NAME` in `.env`
2. **Colors**: Modify `:root` variables in `static/css/theme.css`
3. **Logo**: Replace logo in `templates/components/navbar.html`
4. **Favicon**: Replace `static/favicon.ico`

### Email Templates

Email templates are in `templates/emails/`:
- `booking_confirmation.{txt,html}`
- `booking_cancellation.{txt,html}`
- `booking_reminder.{txt,html}`
- `verification_email.{txt,html}`

### SMS Messages

SMS messages are defined in model methods:
- `apps/booking/models.py` - Booking model
- `apps/accounts/models.py` - Customer model

## 🚢 Deployment

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure `SECRET_KEY` (use strong random key)
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Configure PostgreSQL database
- [ ] Set up Redis for caching
- [ ] Configure email backend (SMTP)
- [ ] Set up SMS provider (Twilio, etc.)
- [ ] Enable HTTPS (set security settings)
- [ ] Configure static files CDN (optional)
- [ ] Set up Sentry for error tracking (optional)
- [ ] Configure backup strategy
- [ ] Set up monitoring/health checks

### Deployment Options

#### 1. Render.com (Recommended for MVP)

1. Create new Web Service
2. Connect repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn config.wsgi:application`
5. Add environment variables
6. Add PostgreSQL database
7. Deploy!

#### 2. Fly.io

```bash
fly launch
fly deploy
```

#### 3. Hetzner (Self-hosted)

1. Create VPS
2. Install Docker & Docker Compose
3. Clone repository
4. Configure .env
5. Run `docker-compose up -d`
6. Set up Nginx reverse proxy
7. Configure SSL with Let's Encrypt

### Docker Production

```bash
# Build production image
docker build -t beauty-salon .

# Run with environment variables
docker run -d \
  -p 8000:8000 \
  --env-file .env.production \
  beauty-salon
```

## 🔐 Security

- ✅ CSRF protection enabled
- ✅ Secure password hashing (PBKDF2)
- ✅ SQL injection protection (ORM)
- ✅ XSS protection (template auto-escaping)
- ✅ Clickjacking protection
- ✅ SSL redirect in production
- ✅ HSTS headers
- ✅ Secure cookies
- ✅ Rate limiting on API

## 📈 Performance

- ✅ Database query optimization (select_related, prefetch_related)
- ✅ Static file compression (WhiteNoise)
- ✅ Caching support (Redis)
- ✅ CDN-ready static files
- ✅ Async task support (Celery)
- ✅ Connection pooling
- ✅ Lightweight CSS framework
- ✅ Minimal JavaScript

## 🤝 Contributing

This is a complete MVP. To extend:

1. **Add Payment Processing**: Integrate Stripe/PayPal
2. **Add Blog**: Create blog app for SEO content
3. **Add Reviews**: Customer review system
4. **Add Loyalty Program**: Points and rewards
5. **Add Multi-Location**: Support multiple salon branches
6. **Add Inventory**: Product sales and inventory
7. **Add Reporting**: Analytics dashboard
8. **Add Mobile App**: Use existing API

## 📝 License

This project is provided as-is for educational and commercial use.

## 🙋 Support

For questions or issues:
1. Check this README
2. Review code comments (fully documented)
3. Check Django/DRF documentation
4. Review deployment guides

## 🎓 Learning Resources

- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Pico.css: https://picocss.com/
- HTMX: https://htmx.org/
- Schema.org: https://schema.org/

## ✅ Credits

Built with:
- Django 4.2
- Django REST Framework
- django-allauth
- Pico.css
- HTMX

---

**Built with ❤️ for beauty professionals**
