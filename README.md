# Blog

This repository contains a simple blog authentication starter built with Flask. It includes registration, login, logout, and a basic dashboard to extend with blog-specific features.

## Getting started

1. **Install dependencies**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run the app**

   ```bash
   flask --app app run --debug
   ```

   The app will automatically create an SQLite database in the `instance/` directory on first run.

3. **Create a user**

   Visit `http://localhost:5000/register` to create your first account. After signing up you will be redirected to the dashboard.

## Testing

Run the automated authentication flow checks with:

```bash
pytest
```

Tests use an in-memory database and validate registration, login, and dashboard access.
