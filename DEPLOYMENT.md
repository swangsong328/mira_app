# Deployment Guide

This guide covers deploying the Beauty Salon booking system to production.

## Table of Contents
- [Pre-Deployment Checklist](#pre-deployment-checklist)
- [Environment Setup](#environment-setup)
- [Deployment Options](#deployment-options)
- [Post-Deployment](#post-deployment)
- [Troubleshooting](#troubleshooting)

## Pre-Deployment Checklist

### Security
- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS` with your domain(s)
- [ ] Enable HTTPS/SSL
- [ ] Set all `SECURE_*` settings to `True`
- [ ] Review and restrict CORS settings

### Database
- [ ] Set up PostgreSQL database
- [ ] Configure database backups
- [ ] Run migrations
- [ ] Create superuser account

### Email & SMS
- [ ] Configure production email backend
- [ ] Set up SMTP credentials
- [ ] Configure SMS provider (if using)
- [ ] Test email/SMS delivery

### Static Files & Media
- [ ] Run `collectstatic`
- [ ] Configure CDN (optional but recommended)
- [ ] Set up media file storage (S3 recommended)

### Monitoring & Logging
- [ ] Set up Sentry (error tracking)
- [ ] Configure log aggregation
- [ ] Set up uptime monitoring
- [ ] Configure health check endpoint monitoring

## Environment Setup

### Production Environment Variables

Create `.env.production` with:

```bash
# Django Core
DJANGO_SETTINGS_MODULE=config.settings.production
SECRET_KEY=<generate-strong-secret-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@hostname:5432/database

# Domain
SITE_DOMAIN=yourdomain.com
SITE_NAME=Your Beauty Salon

# Email (Example with SendGrid)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=<sendgrid-api-key>
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# SMS (Example with Twilio)
SMS_BACKEND=twilio
TWILIO_ACCOUNT_SID=<your-account-sid>
TWILIO_AUTH_TOKEN=<your-auth-token>
TWILIO_PHONE_NUMBER=<your-twilio-number>

# Redis
REDIS_URL=redis://redis-host:6379/0
CELERY_BROKER_URL=redis://redis-host:6379/0

# Security
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# API
API_RATE_LIMIT_ANON=100/hour
API_RATE_LIMIT_USER=1000/hour

# SEO
ENABLE_SEO_OPTIMIZATIONS=True

# Error Tracking (optional)
SENTRY_DSN=<your-sentry-dsn>

# Storage (optional - AWS S3)
AWS_ACCESS_KEY_ID=<your-key>
AWS_SECRET_ACCESS_KEY=<your-secret>
AWS_STORAGE_BUCKET_NAME=<your-bucket>
```

## Deployment Options

### Option 1: Render.com (Easiest)

**Pros**: Zero DevOps, free tier available, automatic HTTPS  
**Cons**: Can be expensive at scale

#### Steps:

1. **Create Account** at https://render.com

2. **Create PostgreSQL Database**
   - Go to Dashboard → New → PostgreSQL
   - Note the connection string

3. **Create Redis Instance** (optional)
   - Dashboard → New → Redis
   - Note the connection string

4. **Create Web Service**
   - Dashboard → New → Web Service
   - Connect your Git repository
   - Configure:
     - **Name**: beauty-salon
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
     - **Start Command**: `gunicorn config.wsgi:application`
     - **Plan**: Select appropriate plan

5. **Add Environment Variables**
   - Add all variables from `.env.production`
   - Use the Database and Redis URLs from Render

6. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete

7. **Run Migrations**
   - Open Shell from Render dashboard
   - Run: `python manage.py migrate`
   - Run: `python manage.py createsuperuser`
   - Run: `python manage.py seed_demo` (optional)

### Option 2: Fly.io (Modern, Cost-Effective)

**Pros**: Good pricing, global deployment, great DX  
**Cons**: Requires fly CLI

#### Steps:

1. **Install Fly CLI**
```bash
curl -L https://fly.io/install.sh | sh
```

2. **Login**
```bash
fly auth login
```

3. **Launch App**
```bash
fly launch
# Follow prompts, select region, create PostgreSQL
```

4. **Set Secrets**
```bash
fly secrets set SECRET_KEY=<your-secret>
fly secrets set DATABASE_URL=<postgres-url>
# Set other secrets...
```

5. **Deploy**
```bash
fly deploy
```

6. **Run Migrations**
```bash
fly ssh console
python manage.py migrate
python manage.py createsuperuser
exit
```

### Option 3: Hetzner VPS (Most Control)

**Pros**: Cheapest at scale, full control  
**Cons**: Requires server management

#### Steps:

1. **Create VPS**
   - Sign up at https://www.hetzner.com/
   - Create Ubuntu 22.04 server
   - Note IP address

2. **SSH into Server**
```bash
ssh root@your-ip
```

3. **Install Docker & Docker Compose**
```bash
# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y
```

4. **Clone Repository**
```bash
cd /opt
git clone <your-repo-url> beauty-salon
cd beauty-salon
```

5. **Configure Environment**
```bash
cp .env.example .env.production
nano .env.production
# Edit with production values
```

6. **Start Services**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

7. **Run Migrations**
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

8. **Set Up Nginx**
```bash
apt install nginx -y
nano /etc/nginx/sites-available/beauty-salon
```

Add configuration:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /opt/beauty-salon/staticfiles/;
    }

    location /media/ {
        alias /opt/beauty-salon/media/;
    }
}
```

Enable site:
```bash
ln -s /etc/nginx/sites-available/beauty-salon /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

9. **Set Up SSL with Let's Encrypt**
```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## Post-Deployment

### 1. Verify Deployment

```bash
# Check health endpoint
curl https://yourdomain.com/healthz/

# Check admin access
# Visit https://yourdomain.com/admin/

# Check API
curl https://yourdomain.com/api/v1/
```

### 2. Create Admin User

```bash
# If using Render/Fly
python manage.py createsuperuser

# If using Docker
docker-compose exec web python manage.py createsuperuser
```

### 3. Seed Demo Data (Optional)

```bash
python manage.py seed_demo
```

### 4. Configure DNS

Point your domain to your server:
- **A Record**: `yourdomain.com` → `your-server-ip`
- **A Record**: `www.yourdomain.com` → `your-server-ip`

### 5. Set Up Backups

#### Database Backups
```bash
# PostgreSQL backup script
#!/bin/bash
BACKUP_DIR="/backups/postgres"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
pg_dump $DATABASE_URL > $BACKUP_DIR/backup_$TIMESTAMP.sql
# Upload to S3 or backup service
```

#### Media Files Backup
- Use S3 or similar object storage
- Enable versioning
- Set up lifecycle policies

### 6. Configure Monitoring

#### Uptime Monitoring
- Set up monitoring at https://uptimerobot.com/
- Monitor: `/healthz/` endpoint
- Alert on: Down, slow response

#### Error Tracking (Sentry)
```python
# Already configured in settings.production.py
# Just add SENTRY_DSN to environment variables
```

#### Log Monitoring
```bash
# View logs
docker-compose logs -f web

# Or with systemd
journalctl -u beauty-salon -f
```

## Troubleshooting

### Static Files Not Loading

```bash
# Collect static files
python manage.py collectstatic --noinput --clear

# Check STATIC_ROOT setting
# Verify nginx/webserver configuration
```

### Database Connection Issues

```bash
# Check DATABASE_URL format
# postgresql://user:password@host:port/database

# Test connection
python manage.py dbshell
```

### Email Not Sending

```bash
# Test email configuration
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
```

### 500 Server Error

```bash
# Check logs
docker-compose logs web

# Enable debug temporarily (NEVER in production for long!)
# DEBUG=True python manage.py runserver

# Check Sentry for error details
```

### Performance Issues

```bash
# Enable Redis caching
# Add REDIS_URL to environment

# Enable query logging to find slow queries
# Add django-debug-toolbar in development

# Check database indexes
python manage.py sqlmigrate booking 0001

# Use database query profiling
```

## Scaling

### Horizontal Scaling
- Add more web workers (Gunicorn workers)
- Use load balancer (Nginx, HAProxy, or cloud load balancer)
- Database read replicas

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Add caching layer (Redis)

### Async Tasks
- Use Celery for:
  - Sending emails
  - Sending SMS
  - Generating reports
  - Cleanup tasks

### CDN
- Use CDN for static files
- Configure `STATICFILES_STORAGE` for CDN
- Options: CloudFront, Cloudflare, BunnyCDN

## Security Hardening

### Server Security
```bash
# Set up firewall
ufw allow 22
ufw allow 80
ufw allow 443
ufw enable

# Disable root login
nano /etc/ssh/sshd_config
# Set: PermitRootLogin no

# Set up fail2ban
apt install fail2ban -y
```

### Application Security
- Keep dependencies updated
- Regular security audits
- Monitor for vulnerabilities
- Use strong passwords
- Enable 2FA for admin accounts

## Maintenance

### Regular Tasks
- [ ] Update dependencies monthly
- [ ] Review logs weekly
- [ ] Check backups daily
- [ ] Monitor performance
- [ ] Review security advisories

### Update Procedure
```bash
# Pull latest code
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart service
docker-compose restart web
# or
systemctl restart beauty-salon
```

---

**Need help?** Check the [README.md](README.md) or review the code comments.


