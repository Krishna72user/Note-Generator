# Note Generation API

A FastAPI-based web application that generates comprehensive study notes from prompts using Google Gemini AI, converts them to PDF format, and stores them in a PostgreSQL database. Includes user authentication with JWT tokens.

## Features

- **User Authentication**: Register and login with email/password
  - Password hashing with bcrypt
  - JWT token-based authentication (36-hour expiration)
  - Secure HTTP-only cookies for token storage

- **AI-Powered Note Generation**: Generate study notes using Google Gemini 3.5 Flash
  - Specialized for technical topics (Digital Electronics, Computer Architecture)
  - Generates exam-oriented, structured notes
  - Automatic summarization of generated notes

- **PDF Export**: Convert generated markdown notes to professional PDF documents
  - Formatted with proper margins and typography
  - Uses Playwright for HTML-to-PDF conversion

- **Database Storage**: Persist notes and user information
  - PostgreSQL database (Supabase)
  - Track user notes with titles and summaries

## Tech Stack

- **Framework**: FastAPI with standard extensions
- **Database**: PostgreSQL (via psycopg)
- **AI Model**: Google Generative AI (Gemini 3.5 Flash)
- **Authentication**: PyJWT for token generation, bcrypt for password hashing
- **PDF Generation**: Playwright (with Chromium)
- **Markup Processing**: Markdown library
- **Containerization**: Docker

## Prerequisites

- Python 3.12+
- PostgreSQL database (or Supabase PostgreSQL instance)
- Google Generative AI API key
- Docker

## Installation

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Note-generation
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the project root with:
   ```env
   GEMINI_API_KEY=your_google_api_key_here
   SECRET_KEY=your_jwt_secret_key_here
   ALGORITHM=HS256
   DATABASE_URL=postgresql://username:password@host:port/database_name
   ```

5. **Set up database schema**
   
   Ensure your PostgreSQL database has the following tables:
   
   ```sql
   CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       name VARCHAR(255) NOT NULL,
       email VARCHAR(255) UNIQUE NOT NULL,
       password_hash VARCHAR(255) NOT NULL
   );

   CREATE TABLE notes (
       id SERIAL PRIMARY KEY,
       title VARCHAR(255) NOT NULL,
       summary TEXT,
       user_email VARCHAR(255) NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (user_email) REFERENCES users(email)
   );
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

   The API will be available at `http://localhost:8000`

### Docker Setup

1. **Build the Docker image**
   ```bash
   docker build -t <image_name> .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 \
     -e GEMINI_API_KEY=your_key \
     -e SECRET_KEY=your_secret \
     -e ALGORITHM=your_algorithm \
     -e DATABASE_URL=your_database_url \
     <>
   ```

## API Endpoints

### Authentication

- **POST** `/api/auth/register`
  - Register a new user
  - Body:
    ```json
    {
      "name": "John Doe",
      "email": "john@example.com",
      "password": "secure_password"
    }
    ```
  - Returns: User info and sets access token cookie

- **POST** `/api/auth/login`
  - Login existing user
  - Body:
    ```json
    {
      "email": "john@example.com",
      "password": "secure_password"
    }
    ```
  - Returns: User info and sets access token cookie

- **GET** `/api/auth/user`
  - Get current authenticated user info
  - Requires: Valid access token cookie
  - Returns: `{"email": "user@example.com"}`

### Notes

- **POST** `/api/notes/generate`
  - Generate study notes from a prompt
  - Requires: Valid access token cookie
  - Body:
    ```json
    {
      "title": "Sequential Circuits",
      "prompt": "Explain the fundamentals of sequential circuits..."
    }
    ```
  - Returns: PDF file as binary response
  - Side effect: Stores note title and summary in database

## Project Structure

```
Note-generation/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── db/
│   │   └── database.py      # Database connection setup
│   ├── routers/
│   │   ├── auth.py          # Authentication endpoints
│   │   └── notes.py         # Note generation endpoints
│   ├── schemas/
│   │   ├── user.py          # User request models
│   │   └── prompt.py        # Prompt request models
│   ├── services/
│   │   ├── generator.py     # AI note generation logic
│   │   └── user_service.py  # User registration/login logic
│   └── utils/
│       └── jwt_util.py      # JWT token utilities
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── .env                    # Environment variables (not in git)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Dependencies

- **fastapi[standard]** - Web framework
- **google-genai** - Google Generative AI client
- **markdown** - Markdown processing with table and code block support
- **playwright** - Browser automation for HTML-to-PDF conversion
- **psycopg** - PostgreSQL database driver
- **bcrypt** - Password hashing
- **pyjwt** - JWT token management

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Generative AI API key | `AIza...` |
| `SECRET_KEY` | JWT secret key for token signing | `your-secret-key` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |

## Security Considerations

- **Passwords**: Hashed using bcrypt with salt
- **Tokens**: JWT with 36-hour expiration, stored in HTTP-only cookies
- **Database**: Credentials managed via environment variables
- **API Keys**: Never commit API keys to version control

## Error Handling

The application includes a universal error handler that returns:
```json
{
  "success": false,
  "message": "Internal Server Error",
  "error": "Error details"
}
```

## Performance Notes

- Playwright downloads Chromium browser on first run (handled in Docker)
- Note generation depends on Google Gemini API response time
- PDF generation is synchronous; consider async processing for high load

## Future Improvements

- Async PDF generation
- Rate limiting on API endpoints
- Note editing and deletion endpoints
- User dashboard/note history
- Caching for frequently generated notes
- Support for multiple AI models

## License

This project is private. Contact the maintainer for usage permissions.

## Support

For issues or questions, please open an issue in the repository.
