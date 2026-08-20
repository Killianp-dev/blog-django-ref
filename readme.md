# blog-django-ref

Backend de blog prêt à l’emploi, Django 5.2 et Python 3.12, avec PostgreSQL. CRUD d’articles, slug automatique, publication, et admin Django. Utile comme base de départ ou comme référence d’architecture (`src/` + `.env`).

## Fonctionnalités

- Modèle `BlogPost` : titre unique, slug, auteur, dates, contenu, drapeau `published`
- Liste publique limitée aux articles publiés ; le staff voit tout
- Création / édition / suppression réservées au staff (`staff_member_required`)
- Slug généré depuis le titre si vide
- Variables d’environnement via `django-environ`
- Tests Django (SQLite en mémoire, pas besoin de PostgreSQL pour `manage.py test`)

## Prérequis

- Python 3.12
- PostgreSQL (développement et production ; pas pour les tests)

## Installation

```bash
git clone https://github.com/Killianp-dev/blog-django-ref.git
cd blog-django-ref
python3 -m venv .venv
source .venv/bin/activate   # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

Créez une base PostgreSQL, puis un fichier `.env` à la racine du dépôt (à côté de `src/`, pas dans `src/`) :

```env
SECRET_KEY=remplacez-moi-par-une-clé-secrète
DB_NAME=blog_ref
DB_USER=blog_user
DB_PASSWORD=mot_de_passe
DB_HOST=localhost
DB_PORT=5432
```

Générer une `SECRET_KEY` :

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Migrations et serveur :

```bash
cd src
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

| URL | Rôle |
| --- | --- |
| http://127.0.0.1:8000/ | Page d’accueil |
| http://127.0.0.1:8000/blog/ | Liste des articles |
| http://127.0.0.1:8000/blog/create/ | Nouvel article (staff) |
| http://127.0.0.1:8000/admin/ | Administration Django |

Le fichier `.env` est lu depuis le parent de `src/` (`settings.py` → `BASE_DIR.parent / '.env'`).

## Tests

Les tests basculent automatiquement sur SQLite `:memory:` dès que `test` est dans `sys.argv`. PostgreSQL n’est pas requis.

```bash
cd src
python manage.py test blog
```

Couverture actuelle : génération de slug, `author_or_default`, URLs, vues liste/détail et restrictions staff.

## Structure

```
blog-django-ref/
├── .env                 # non versionné — secrets et Postgres
├── requirements.txt
└── src/
    ├── manage.py
    ├── config/          # settings, urls, wsgi/asgi
    ├── blog/            # modèle, vues, templates, tests
    └── templates/       # layout de base
```

## Production

Ce dépôt est un **référentiel de développement**. Avant une mise en ligne : `DEBUG = False`, `ALLOWED_HOSTS`, HTTPS, un serveur WSGI (Gunicorn) et un reverse proxy. Le code actuel laisse `DEBUG = True` et `ALLOWED_HOSTS = []`.

## Licence

MIT.
