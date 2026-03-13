import bcrypt
from sqlalchemy.orm import Session
from app import models


def seed_database(db: Session) -> str:
    """
    Seeds the database with dummy data.
    Returns a message indicating what happened.
    Skips if data already exists.
    """
    existing_users = db.query(models.User).first()
    if existing_users:
        return "Database already has data, skipping seed"

    # ── Dummy users ───────────────────────────────────────────
    users_data = [
        {"name": "Alice Johnson", "email": "alice@example.com", "password": "alice123"},
        {"name": "Bob Smith",     "email": "bob@example.com",   "password": "bob123"},
        {"name": "Carol Davis",   "email": "carol@example.com", "password": "carol123"},
    ]

    users = []
    for u in users_data:
        hashed = bcrypt.hashpw(u["password"].encode("utf-8")[:72], bcrypt.gensalt())
        user = models.User(name=u["name"], email=u["email"], password=hashed.decode("utf-8"))
        db.add(user)
        users.append(user)

    db.flush()  # get IDs without committing

    # ── Dummy blogs ───────────────────────────────────────────
    blogs_data = [
        {
            "title": "Getting Started with FastAPI",
            "content": "FastAPI is a modern, fast web framework for building APIs with Python 3.9+. "
                       "It leverages type hints and async support to deliver high performance.",
            "published": True,
            "author": users[0],
        },
        {
            "title": "Python Best Practices in 2024",
            "content": "Writing clean, maintainable Python code requires consistent use of type hints, "
                       "virtual environments, linting tools, and proper project structure.",
            "published": True,
            "author": users[0],
        },
        {
            "title": "Building REST APIs the Right Way",
            "content": "A well-designed REST API follows resource-based URLs, uses proper HTTP methods, "
                       "and returns consistent JSON responses with meaningful status codes.",
            "published": True,
            "author": users[1],
        },
        {
            "title": "PostgreSQL Tips and Tricks",
            "content": "PostgreSQL is one of the most powerful open-source databases. "
                       "Indexing, query planning, and connection pooling are key to great performance.",
            "published": True,
            "author": users[1],
        },
        {
            "title": "Introduction to Docker for Developers",
            "content": "Docker allows you to package your application and its dependencies into a container, "
                       "ensuring it runs the same way on every machine.",
            "published": True,
            "author": users[2],
        },
    ]

    for b in blogs_data:
        blog = models.Blog(
            title=b["title"],
            content=b["content"],
            published=b["published"],
            author_id=b["author"].id,
        )
        db.add(blog)

    db.commit()
    return "Database seeded with dummy data"
