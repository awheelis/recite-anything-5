# Recite Anything

A scripture memorization app based on Dr. Andrew Davis's "An Approach to Extended Memorization of Scripture."
It guides users through structured daily recitation phases, weekly review sessions, and long-term retention cycles.

## Environment Setup

```bash
cd backend
pip install -r requirements.txt
```

Optionally create a `.env` file in `backend/` to override defaults:

```
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite+aiosqlite:///./recite.db
```

## Run

```bash
cd backend
uvicorn app.main:app --reload
```

## API

- `POST /api/auth/register` — create account, returns JWT
- `POST /api/auth/login` — login, returns JWT
- `GET /api/auth/me` — current user (requires `Authorization: Bearer <token>`)
- `GET /api/bible/books` — list all books
- `GET /api/bible/books/{book}` — book info
- `GET /api/bible/verse/{book}/{chapter}/{verse}` — single verse
- `GET /api/bible/verses/{book}?start_index=0&end_index=5` — verse range

## Tests

```bash
cd backend
pytest
```
