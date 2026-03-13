# Blog API

A production-ready FastAPI blog application with PostgreSQL, JWT authentication, and auto-seeding.

## Endpoints

| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| GET | `/` | No | Health check |
| POST | `/auth/login` | No | Login and get JWT token |
| POST | `/users/` | No | Register a new user |
| GET | `/users/` | Yes | List all users |
| GET | `/users/{id}` | Yes | Get user by ID |
| PUT | `/users/{id}` | Yes | Update your profile |
| DELETE | `/users/{id}` | Yes | Delete your account |
| GET | `/blogs/` | No | List all published blogs |
| GET | `/blogs/{id}` | No | Get blog by ID |
| POST | `/blogs/` | Yes | Create a new blog |
| PUT | `/blogs/{id}` | Yes | Update your blog |
| DELETE | `/blogs/{id}` | Yes | Delete your blog |
| POST | `/seed` | No | Manually seed the database |

## Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/prajvalbhardwaj-spec/again-testing.git
cd again-testing
```

### 2. Create your `.env` file
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
SECRET_KEY=your-super-secret-key
```

### 3. Run the app (one command)

**macOS / Linux:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```bat
start.bat
```

This will:
- Install all dependencies
- Auto-create the database and tables
- Seed dummy data (3 users + 5 blogs)
- Start the server at `http://localhost:8000`

### 4. Manual steps (alternative)
```bash
pip install -r requirements.txt
python seed.py
uvicorn app.main:app --reload
```

## API Docs

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Deploy to Render

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New → Blueprint
3. Connect your GitHub repo
4. Set environment variables:
   - `DATABASE_URL` — your PostgreSQL connection string
   - `SECRET_KEY` — a long random string
5. Deploy

The `render.yaml` handles everything automatically.

## Docker

```bash
docker build -t blog-api .
docker run -p 10000:10000 --env-file .env blog-api
```
