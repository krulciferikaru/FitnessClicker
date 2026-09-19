# FitnessClicker

A browser-based idle/incremental "clicker" game built with Django. Click to earn points, buy upgrades to boost your click power, watch your character progress through fitness stages, and prestige once you've maxed everything out.

## Gameplay

- **Click** the button to earn clicks (points).
- **Upgrades** (Yoga Mat, Jump Rope, Dumbbells, Kettlebell, Barbell) each add to your clicks-per-click. Upgrades unlock in order — you must buy one before the next becomes available — and each level costs more than the last (cost scales by 1.5x per level).
- **Player image** changes as your total clicks climb through milestones (100 / 500 / 1,500 / 3,000+).
- **Notifications** show a running log of your recent purchases and milestones.
- **Prestige** resets your clicks and upgrades but permanently boosts your click power by 10%, once all upgrades have been purchased.
- **Reset** wipes your progress back to zero.

## Tech stack

- [Django](https://www.djangoproject.com/) 5.2 (Python)
- SQLite (default Django database)
- Tailwind CSS (via CDN) + vanilla JavaScript on the frontend

Game state (clicks, upgrade levels, notifications) currently lives in an in-memory dictionary on the server (see [clicker/views.py](clicker/views.py)), so it resets whenever the server restarts and is shared across all visitors rather than being tracked per-user/session.

## Project structure

```
demo/        # Django project settings, root URLconf
clicker/     # Main app: views, urls, templates, static images
  templates/       # welcome.html (landing page), index.html (game)
  static/images/   # player character images (belly1.png - belly5.png)
manage.py    # Django management entry point
db.sqlite3   # SQLite database
```

## Getting started

### Prerequisites

- Python 3.10+
- Django 5.2 (`pip install django`)

### Run locally

```bash
python manage.py migrate
python manage.py runserver
```

Then open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Routes

| Path                 | Description                          |
|-----------------------|---------------------------------------|
| `/`                    | Welcome/landing page                 |
| `/index/`              | Main game screen                     |
| `/click/`              | POST — register a click              |
| `/purchase_upgrade/`   | POST — buy/level up an upgrade       |
| `/reset/`               | Reset game state                     |
| `/prestige/`            | Prestige (requires all upgrades)     |
| `/admin/`               | Django admin                         |
