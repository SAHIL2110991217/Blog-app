# Mini Blog Application

## Overview
A simple mini blog application using Flask for the backend and PostgreSQL for the database.

## Setup
1. Create a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`.
3. Set up environment variables in a `.env` file.
4. Run the application: `python run.py`.

## Endpoints
- POST `/api/register`: Register a new user.
- POST `/api/login`: Login a user (placeholder).
- POST `/api/posts`: Create a new blog post.
- GET `/api/posts/<post_id>`: Get details of a blog post.
- POST `/api/comments`: Add a comment to a blog post.
