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
