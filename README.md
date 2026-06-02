# potential‑tribbleTouristguide‑haris‑finalcode  

A Django‑based web application that serves as a **Tourist Guide** platform.  Users can explore destinations, view activities, discover events, and manage personal travel plans—all presented with clean HTML templates.

---

## Overview  

The project showcases a full‑stack solution for a travel‑oriented website:

- **Destinations** – detailed pages with images and geographic data.  
- **Activities & Events** – searchable listings (e.g., `activities/cs202.png`, `events/cs201.png`).  
- **User Profiles** – avatar uploads stored under `media/profile_pics/`.  
- **Travel Planner** – users can create itineraries, book trips, and receive reminders.  

The codebase is organized as a standard Django project (`myapp`) with migrations, forms, admin customisations, and static/media handling.

---

## Features  

| Feature | Description |
|---------|-------------|
| **Destination catalogue** | Rich pages with images, latitude/longitude, and travel tips. |
| **Activity & event listings** | Filterable by category, date, and location. |
| **User authentication** | Registration, login, and profile picture support. |
| **Travel planner** | Create, edit, and delete travel plans; view booking history. |
| **Reminders & notifications** | Email/SMS reminders for upcoming trips (placeholder API key). |
| **Reviews & replies** | Users can post reviews, like replies, and engage with the community. |
| **Responsive UI** | HTML templates styled for desktop and mobile devices. |

---

## Tech Stack  

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.9, Django 4.x |
| **Database** | SQLite (default) – can be swapped for PostgreSQL/MySQL |
| **Frontend** | HTML5, CSS3 (static files), optional JavaScript |
| **Media storage** | Local `media/` directory (profile pictures, activity images) |
| **Version control** | Git (GitHub) |
| **Deployment** | Any WSGI‑compatible server (e.g., Gunicorn + Nginx) |

---

## Installation  

> **Prerequisites** – Python 3.9+, `git`, and a virtual‑environment tool (`venv` or `conda`).

```bash
# 1. Clone the repository
git clone https://github.com/your-username/potential-tribbleTouristguide-haris-finalcode.git
cd potential-tribbleTouristguide-haris-finalcode

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install Django==4.*   # Adjust version as needed
# If a requirements.txt file exists, use:
# pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Create a superuser (optional, for admin access)
python manage.py createsuperuser

# 6. Collect static files (for production)
python manage.py collectstatic
```

### Environment variables  

Create a `.env` file in the project root (or export variables in your shell) with at least:

```env
SECRET_KEY=YOUR_DJANGO_SECRET_KEY
DEBUG=True               # Set to False in production
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST=smtp.example.com
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=YOUR_OWN_API_KEY   # Replace with real credentials
```

> **NOTE:**