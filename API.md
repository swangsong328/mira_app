# API Documentation

RESTful API documentation for the Beauty Salon booking system.

## Base URL

```
Development: http://localhost:8000/api/v1/
Production: https://yourdomain.com/api/v1/
```

## Authentication

The API uses JWT (JSON Web Token) authentication.

### Get Access Token

**Endpoint:** `POST /api/v1/auth/token/`

**Request:**
```json
{
  "email": "customer@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Refresh Access Token

**Endpoint:** `POST /api/v1/auth/token/refresh/`

**Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Using Token

Include the access token in the Authorization header:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## Rate Limiting

- **Anonymous users:** 100 requests/hour
- **Authenticated users:** 1000 requests/hour

Exceeding rate limits returns `429 Too Many Requests`.

## Endpoints

### Services

#### List Services

**Endpoint:** `GET /api/v1/services/`

**Query Parameters:**
- `staff_id` (optional): Filter by staff member

**Response:**
```json
{
  "count": 6,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Classic Haircut",
      "slug": "classic-haircut",
      "description": "Professional haircut tailored to your style...",
      "short_description": "Professional haircut with wash and style",
      "duration": 45,
      "duration_hours": 0.75,
      "price": "50.00",
      "image": "http://example.com/media/services/haircut.jpg",
      "is_active": true,
      "display_order": 1
    }
  ]
}
```

#### Get Service Detail

**Endpoint:** `GET /api/v1/services/{slug}/`

**Response:**
```json
{
  "id": 1,
  "name": "Classic Haircut",
  "slug": "classic-haircut",
  "description": "Professional haircut tailored to your style...",
  "short_description": "Professional haircut with wash and style",
  "duration": 45,
  "duration_hours": 0.75,
  "price": "50.00",
  "image": "http://example.com/media/services/haircut.jpg",
  "is_active": true,
  "display_order": 1
}
```

### Staff

#### List Staff Members

**Endpoint:** `GET /api/v1/staff/`

**Query Parameters:**
- `service_id` (optional): Filter by service

**Response:**
```json
{
  "count": 4,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "first_name": "Sarah",
      "last_name": "Johnson",
      "full_name": "Sarah Johnson",
      "slug": "sarah-johnson",
      "avatar": "http://example.com/media/staff/sarah.jpg"
    }
  ]
}
```

#### Get Staff Detail

**Endpoint:** `GET /api/v1/staff/{slug}/`

**Response:**
```json
{
  "id": 1,
  "first_name": "Sarah",
  "last_name": "Johnson",
  "full_name": "Sarah Johnson",
  "slug": "sarah-johnson",
  "bio": "Senior stylist with 10+ years of experience...",
  "avatar": "http://example.com/media/staff/sarah.jpg",
  "is_active": true,
  "services": [
    {
      "id": 1,
      "name": "Classic Haircut",
      "slug": "classic-haircut",
      "description": "...",
      "short_description": "...",
      "duration": 45,
      "duration_hours": 0.75,
      "price": "50.00",
      "image": "...",
      "is_active": true,
      "display_order": 1
    }
  ]
}
```

#### Get Available Time Slots for Staff

**Endpoint:** `GET /api/v1/staff/{slug}/available_slots/`

**Query Parameters:**
- `days` (optional, default: 14): Number of days to look ahead

**Response:**
```json
[
  {
    "id": 123,
    "staff": 1,
    "staff_name": "Sarah Johnson",
    "start_time": "2025-10-24T09:00:00Z",
    "end_time": "2025-10-24T10:00:00Z",
    "capacity": 1,
    "is_blocked": false,
    "is_available": true
  }
]
```

### Time Slots

#### List Available Time Slots

**Endpoint:** `GET /api/v1/time-slots/`

**Query Parameters:**
- `staff_id` (optional): Filter by staff
- `start_date` (optional): Filter by start date (YYYY-MM-DD)
- `end_date` (optional): Filter by end date (YYYY-MM-DD)

**Response:**
```json
{
  "count": 50,
  "next": "http://example.com/api/v1/time-slots/?page=2",
  "previous": null,
  "results": [
    {
      "id": 123,
      "staff": 1,
      "staff_name": "Sarah Johnson",
      "start_time": "2025-10-24T09:00:00Z",
      "end_time": "2025-10-24T10:00:00Z",
      "capacity": 1,
      "is_blocked": false,
      "is_available": true
    }
  ]
}
```

### Bookings

#### List My Bookings

**Endpoint:** `GET /api/v1/bookings/`

**Authentication:** Required

**Response:**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "customer": 5,
      "customer_email": "customer@example.com",
      "service": 1,
      "service_name": "Classic Haircut",
      "staff": 1,
      "staff_name": "Sarah Johnson",
      "time_slot": 123,
      "start_time": "2025-10-24T09:00:00Z",
      "end_time": "2025-10-24T09:45:00Z",
      "status": "confirmed",
      "notes": "",
      "price": "50.00",
      "confirmation_code": "a1b2c3d4e5f6",
      "confirmed_at": "2025-10-23T15:30:00Z",
      "created_at": "2025-10-23T15:30:00Z"
    }
  ]
}
```

#### Create Booking

**Endpoint:** `POST /api/v1/bookings/`

**Authentication:** Required

**Request:**
```json
{
  "service": 1,
  "staff": 1,
  "time_slot": 123,
  "notes": "Please use organic products"
}
```

**Response:**
```json
{
  "id": 1,
  "customer": 5,
  "customer_email": "customer@example.com",
  "service": 1,
  "service_name": "Classic Haircut",
  "staff": 1,
  "staff_name": "Sarah Johnson",
  "time_slot": 123,
  "start_time": "2025-10-24T09:00:00Z",
  "end_time": "2025-10-24T09:45:00Z",
  "status": "confirmed",
  "notes": "Please use organic products",
  "price": "50.00",
  "confirmation_code": "a1b2c3d4e5f6",
  "confirmed_at": "2025-10-23T15:30:00Z",
  "created_at": "2025-10-23T15:30:00Z"
}
```

**Errors:**
- `400`: Validation error (e.g., time slot not available, staff doesn't provide service)
- `401`: Authentication required
- `404`: Service, staff, or time slot not found

#### Get Booking Detail

**Endpoint:** `GET /api/v1/bookings/{id}/`

**Authentication:** Required (can only view own bookings)

**Response:** Same as create booking response

#### Cancel Booking

**Endpoint:** `POST /api/v1/bookings/{id}/cancel/`

**Authentication:** Required

**Response:**
```json
{
  "id": 1,
  "status": "canceled",
  ...
}
```

**Errors:**
- `400`: Booking cannot be canceled (already canceled/completed)
- `401`: Authentication required
- `404`: Booking not found

### User Management

#### Register New User

**Endpoint:** `POST /api/v1/register/`

**Request:**
```json
{
  "email": "newuser@example.com",
  "password": "securePassword123",
  "password_confirm": "securePassword123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890"
}
```

**Response:**
```json
{
  "customer": {
    "id": 6,
    "email": "newuser@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "email_verified": false,
    "phone_verified": false,
    "sms_notifications": true,
    "email_notifications": true,
    "created_at": "2025-10-23T15:30:00Z"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

#### Get My Profile

**Endpoint:** `GET /api/v1/profile/`

**Authentication:** Required

**Response:**
```json
{
  "id": 5,
  "email": "customer@example.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "phone": "+1234567890",
  "email_verified": true,
  "phone_verified": true,
  "sms_notifications": true,
  "email_notifications": true,
  "created_at": "2025-10-20T10:00:00Z"
}
```

#### Update My Profile

**Endpoint:** `PUT /api/v1/profile/` or `PATCH /api/v1/profile/`

**Authentication:** Required

**Request:**
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "sms_notifications": false
}
```

**Response:** Same as get profile response

## Error Responses

### Standard Error Format

```json
{
  "detail": "Error message here"
}
```

Or for field-specific errors:

```json
{
  "field_name": [
    "Error message for this field"
  ]
}
```

### HTTP Status Codes

- `200 OK`: Success
- `201 Created`: Resource created successfully
- `400 Bad Request`: Validation error
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

## Examples

### Booking Flow Example

```bash
# 1. Register or login
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "customer@example.com", "password": "password123"}'

# Save the access token
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGc..."

# 2. Get available services
curl http://localhost:8000/api/v1/services/

# 3. Get staff for selected service
curl "http://localhost:8000/api/v1/staff/?service_id=1"

# 4. Get available time slots for selected staff
curl http://localhost:8000/api/v1/staff/sarah-johnson/available_slots/

# 5. Create booking
curl -X POST http://localhost:8000/api/v1/bookings/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "service": 1,
    "staff": 1,
    "time_slot": 123,
    "notes": "First time customer"
  }'

# 6. View my bookings
curl http://localhost:8000/api/v1/bookings/ \
  -H "Authorization: Bearer $TOKEN"
```

## Pagination

API responses are paginated with 20 items per page by default.

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (max: 100)

**Response includes:**
- `count`: Total number of items
- `next`: URL for next page (null if last page)
- `previous`: URL for previous page (null if first page)
- `results`: Array of items

## Filtering & Searching

Some endpoints support filtering:

```bash
# Filter bookings by status
GET /api/v1/bookings/?status=confirmed

# Search services
GET /api/v1/services/?search=haircut

# Multiple filters
GET /api/v1/time-slots/?staff_id=1&start_date=2025-10-24
```

## Mobile App Integration

This API is designed to be mobile-app ready:

1. **Authentication**: Use JWT tokens
2. **Offline Support**: Cache responses locally
3. **Push Notifications**: Integrate with FCM/APNS for booking reminders
4. **Image Optimization**: Request appropriate image sizes
5. **Error Handling**: Handle 429 rate limits gracefully

---

**Need more help?** Check the [README.md](README.md) or deployment guide.


