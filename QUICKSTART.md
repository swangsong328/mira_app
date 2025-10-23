# Quick Start Guide

Get the Beauty Salon booking system up and running in 5 minutes!

## Prerequisites

- Python 3.8+
- Git
- Virtual environment support

## Installation (Local Development)

### 1. Clone and Setup

```bash
# Clone the repository (or extract the files)
cd mira_app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
copy .env.example .env   # Windows
# or
cp .env.example .env     # macOS/Linux

# Edit .env if needed (optional for local development)
# Default SQLite database will work out of the box
```

### 3. Initialize Database

```bash
# Run migrations
python manage.py migrate

# Seed demo data (includes admin user and sample data)
python manage.py seed_demo
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Visit **http://localhost:8000** 🎉

## Default Login Credentials

After running `seed_demo`:

- **Admin Panel**: http://localhost:8000/admin/
  - Email: `admin@beautysalon.com`
  - Password: `admin123`

- **Customer Account**:
  - Email: `customer@example.com`
  - Password: `password123`

## Quick Tour

### Frontend (User-Facing)
- **Homepage**: http://localhost:8000/
- **Services**: http://localhost:8000/booking/services/
- **Stylists**: http://localhost:8000/booking/staff/
- **Book Appointment**: http://localhost:8000/booking/new/step1/
- **About Us**: http://localhost:8000/about/
- **Contact**: http://localhost:8000/contact/

### Admin Panel
- **Dashboard**: http://localhost:8000/admin/
- Manage services, staff, bookings, customers, opening hours

### API Endpoints
- **API Root**: http://localhost:8000/api/v1/
- **Services API**: http://localhost:8000/api/v1/services/
- **Staff API**: http://localhost:8000/api/v1/staff/
- **Bookings API**: http://localhost:8000/api/v1/bookings/
- **Get JWT Token**: POST http://localhost:8000/api/v1/auth/token/

## Using Make Commands

If you have `make` installed:

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

# Check code quality
make check
```

## Using Docker

For a containerized setup:

```bash
# Start all services (web, database, redis)
docker-compose up

# In another terminal, run migrations
docker-compose exec web python manage.py migrate

# Seed demo data
docker-compose exec web python manage.py seed_demo

# View logs
docker-compose logs -f web
```

Visit **http://localhost:8000**

## Next Steps

### 1. Customize Branding

Edit these files:
- `static/css/theme.css` - Colors and styling
- `templates/components/navbar.html` - Site name and logo
- `.env` - SITE_NAME and SITE_DOMAIN

### 2. Configure Email

For development, emails are logged to console by default.

For production, update in `.env`:
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 3. Configure SMS (Optional)

Update in `.env`:
```bash
SMS_BACKEND=twilio
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_PHONE_NUMBER=your-twilio-number
```

### 4. Add Your Content

Via Admin Panel (http://localhost:8000/admin/):
1. **Services** - Add/edit your salon services
2. **Staff** - Add your team members with photos
3. **Opening Hours** - Configure your business hours
4. **Time Slots** - Will be auto-generated based on opening hours

### 5. Test Booking Flow

1. Create an account or login as customer
2. Click "Book Now"
3. Select service → stylist → date/time → confirm
4. Check console for confirmation email
5. View booking in "My Bookings"

## Troubleshooting

### Port Already in Use

```bash
# Use a different port
python manage.py runserver 8001
```

### Database Errors

```bash
# Reset database (WARNING: Deletes all data)
rm db.sqlite3
python manage.py migrate
python manage.py seed_demo
```

### Import Errors

```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Static Files Not Loading

```bash
# Collect static files
python manage.py collectstatic --noinput
```

## Testing the System

### Run Test Suite

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=apps

# Run specific tests
pytest apps/booking/tests/
```

### Test API with curl

```bash
# Get JWT token
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "customer@example.com", "password": "password123"}'

# List services
curl http://localhost:8000/api/v1/services/

# Create booking (with token)
curl -X POST http://localhost:8000/api/v1/bookings/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"service": 1, "staff": 1, "time_slot": 123}'
```

## Features to Explore

### 1. Multi-Step Booking
- Service selection
- Stylist selection
- Date/time picker
- Confirmation with notes

### 2. User Dashboard
- View all bookings
- Cancel bookings
- Profile management
- Phone verification

### 3. Admin Features
- Booking management
- Customer management
- Service/staff CRUD
- Contact form submissions

### 4. SEO Features
- Sitemap: http://localhost:8000/sitemap.xml
- Robots.txt: http://localhost:8000/robots.txt
- Schema.org markup (view page source)
- OpenGraph meta tags

### 5. API Features
- RESTful endpoints
- JWT authentication
- Rate limiting
- Pagination
- Filtering

## Common Customizations

### Change Primary Color

Edit `static/css/theme.css`:
```css
:root {
    --primary: #YOUR_COLOR;
}
```

### Add New Service

Admin → Booking → Services → Add Service

Or via Django shell:
```python
python manage.py shell
>>> from apps.booking.models import Service
>>> from decimal import Decimal
>>> Service.objects.create(
...     name="New Service",
...     description="Description here",
...     duration=60,
...     price=Decimal("75.00")
... )
```

### Generate More Time Slots

```bash
# Run seed_demo again (won't duplicate existing data)
python manage.py seed_demo
```

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed production deployment instructions.

Quick options:
- **Render.com** - Easiest (1-click deploy)
- **Fly.io** - Modern and cost-effective
- **Hetzner VPS** - Most control, cheapest at scale

## Documentation

- **README.md** - Full project documentation
- **DEPLOYMENT.md** - Production deployment guide
- **API.md** - Complete API documentation
- **Code Comments** - Every file is fully documented

## Support & Learning

- Review code comments (every file is documented)
- Check Django documentation: https://docs.djangoproject.com/
- Check DRF documentation: https://www.django-rest-framework.org/
- Review test files for usage examples

## What's Included

✅ Complete booking system  
✅ User authentication (email + OTP)  
✅ Admin panel with full CRUD  
✅ RESTful API with JWT  
✅ Email/SMS notifications  
✅ SEO optimization  
✅ Responsive design  
✅ Test suite  
✅ Docker support  
✅ Production-ready configuration  

## Project Structure Overview

```
mira_app/
├── apps/
│   ├── accounts/      # User auth & profiles
│   ├── booking/       # Booking system
│   ├── core/          # Utilities & SEO
│   ├── sitecontent/   # Static pages
│   └── api/           # REST API
├── templates/         # HTML templates
├── static/           # CSS, images
├── config/           # Django settings
└── manage.py         # Django CLI
```

---

**🎉 You're all set!** Start customizing and building your beauty salon website.

Need help? Check the documentation or review the code comments.
