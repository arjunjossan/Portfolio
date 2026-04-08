# Django Portfolio Website

A modern Django portfolio with an admin-managed content system, project showcase pages, a contact workflow, and a light/dark theme toggle. The project is built to work well for local development with SQLite while staying ready for containerized or PostgreSQL-backed deployment.

## Highlights

- Admin-managed sections for hero, about, skills, projects, experience, education, certifications, contact details, and social links
- Home page with featured content, theme toggle, subscription flow, and compact contact form
- Project detail pages with image galleries, tech stacks, lessons learned, and related projects
- Reusable templates and structured content models for fast updates through Django admin
- Docker and PostgreSQL support for deployment
- GitHub Actions CI for Django checks and test runs

## Tech Stack

- Python 3.13
- Django 5.2
- SQLite for local development
- PostgreSQL-ready database configuration
- Tailwind utility classes plus custom CSS
- Gunicorn for production serving

## Project Structure

```text
portfolio_project/   Django project settings and URL config
portfolio_app/       Models, views, admin, forms, and app logic
templates/           Page templates and reusable template partials
static/              CSS, JavaScript, and static design assets
tests/               Test suite for models and views
media/               Local uploaded content during development
```

## Local Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy the example environment file:

```bash
cp .env.example .env
```

4. Apply migrations:

```bash
python3 manage.py migrate
```

5. Create an admin user:

```bash
python3 manage.py createsuperuser
```

6. Start the development server:

```bash
python3 manage.py runserver
```

7. Open:
- App: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

## Content Management Flow

- Create one active `Site configuration` entry to define global branding, labels, and theme toggle visibility.
- Create one active `Hero section`, `About section`, and `Contact information` entry to power shared page content.
- Add repeatable records for projects, skills, education, experience, certifications, and social links.
- Review incoming contact submissions in Django admin.

## Environment Variables

Core variables from [.env.example](/Users/arjunsingh/Desktop/PortFolio/.env.example):

- `DJANGO_SECRET_KEY`: required for production
- `DJANGO_DEBUG`: `True` for local development, `False` for production
- `DJANGO_ALLOWED_HOSTS`: comma-separated host list
- `DJANGO_CSRF_TRUSTED_ORIGINS`: comma-separated trusted origins for deployments behind HTTPS
- `DJANGO_TIME_ZONE`: defaults to `Asia/Kolkata`
- `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: database config
- `DJANGO_EMAIL_BACKEND`, `DEFAULT_FROM_EMAIL`, `CONTACT_NOTIFICATION_EMAIL`: email config
- `SECURE_SSL_REDIRECT`, `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE`: secure cookie and redirect controls
- `SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS`, `SECURE_HSTS_PRELOAD`: optional HSTS settings

## Production Notes

- When `DJANGO_DEBUG=False`, the app now requires a non-default `DJANGO_SECRET_KEY`.
- `SECURE_SSL_REDIRECT` defaults to enabled in production.
- `SECURE_PROXY_SSL_HEADER` is configured for deployments behind a reverse proxy.
- Set `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS` explicitly before deployment.
- Run `python3 manage.py collectstatic --noinput` during your build or release step.

Example production-style `.env` values:

```env
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=replace-with-a-real-secret
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
SECURE_SSL_REDIRECT=True
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

## Docker

Build and run with Docker Compose:

```bash
docker compose up --build
```

Then apply migrations inside the container:

```bash
docker compose exec web python manage.py migrate
```

## Testing

Run the Django checks:

```bash
python3 manage.py check
```

Run the test suite:

```bash
python3 manage.py test
```

## GitHub Workflow

This repository includes a GitHub Actions workflow that runs on pushes and pull requests to `main`. It installs Python, installs dependencies, runs `python manage.py check`, and then runs `python manage.py test`.

## Recommended Git Workflow

For future updates:

```bash
git status
git add .
git commit -m "Describe the change"
git push
```

For larger features:

```bash
git checkout -b feature/short-name
git push -u origin feature/short-name
```

Then open a pull request into `main`.

## Screenshots

Add repository screenshots here later for a stronger GitHub landing page:

- Home page hero
- Projects section
- Project detail page
- Admin content management view
