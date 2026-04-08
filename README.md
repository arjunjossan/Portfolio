# Django Portfolio Website

A modern, responsive Django portfolio designed for Master's admissions storytelling, with all major content managed through the Django admin.

## Features

- Dynamic home page sections powered by database models
- Custom admin configuration for hero, about, skills, projects, experience, education, certifications, contact details, social links, and contact submissions
- Project detail pages with related projects
- Responsive landing page with section-based navigation, theme toggle, project filtering, and contact form handling
- Docker and PostgreSQL-ready configuration for deployment
- SQLite-friendly local development defaults

## Quick Start

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and adjust values if needed.
4. Run `python manage.py migrate`.
5. Create an admin user with `python manage.py createsuperuser`.
6. Start the development server with `python manage.py runserver`.
7. Open `http://127.0.0.1:8000/` and `http://127.0.0.1:8000/admin/`.

## Content Management

- Add one active `Site configuration`, `Hero section`, `About section`, and `Contact information` entry to power the shared page content.
- Manage repeatable content such as skills, projects, education, experience, certifications, and social links from the admin.
- Contact form submissions are stored in admin as read-only records for follow-up.

## Database Notes

- Development defaults to SQLite.
- For PostgreSQL, set `DB_ENGINE=django.db.backends.postgresql` and configure `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT`.

## Docker

- Copy `.env.example` to `.env`.
- Start services with `docker compose up --build`.
- Run migrations inside the container with `docker compose exec web python manage.py migrate`.

## Testing

Run the test suite with:

```bash
python manage.py test
```
