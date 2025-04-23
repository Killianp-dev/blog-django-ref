# Blog Django Ref

A ready-to-use backend for a blog built with Django 5 and Python 3.12, configured to use PostgreSQL for data storage.

## Features

- Django 5
- Python 3.12
- PostgreSQL integration
- Environment variables (.env file)
- Structured Django project

## Project Structure

```
blog-django-ref/
├── .env                   # Environment variables (database settings, secret keys)
├── src/                   # Project source code
│   ├── blog/              # Django app for blog functionality
│   └── config/            # Project configuration (settings, URLs, etc.)
└── README.md              # This file
```

## Setup Instructions

### Prerequisites

- Python 3.12 installed
- PostgreSQL installed and running

### Installation

Clone the repository:

```bash
git clone https://github.com/Killianp-dev/blog-django-ref
cd blog-django-ref
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure your database settings in `.env`:

```env
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
SECRET_KEY=your_secret_key
```

Apply migrations:

```bash
cd src
python manage.py migrate
```

Create an admin user:

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

Your blog backend is now accessible at `http://localhost:8000/`.

## Contributing

Contributions are welcome! Please submit pull requests or issues for any bugs or improvements.

## License

Distributed under the MIT License.


