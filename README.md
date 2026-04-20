# AttendX - Smart Attendance & Activity Monitoring System

Production-ready full-stack application for curriculum activity and attendance monitoring in educational institutions.

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+ (for Vercel deployment)
- PostgreSQL (for production) or SQLite (for development)

### Development Setup

1. **Clone and install backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Seed database with sample data**
   ```bash
   python seed.py
   ```

3. **Start backend server**
   ```bash
   uvicorn main:app --reload
   ```
   Backend runs at `http://localhost:8000`

4. **Update frontend config**
   Edit `config.js` and set `API_BASE: 'http://localhost:8000'`

5. **Open frontend**
   Open `attendx.html` in browser or serve with Python:
   ```bash
   python -m http.server 8080
   ```
   Frontend at `http://localhost:8080`

6. **Login with demo credentials**
   - Email: `admin@college.edu`
   - Password: `Admin@123`

## Deployment

### Backend (Render)
1. Push `backend/` folder to GitHub
2. Create new Web Service on Render
3. Connect GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables (PostgreSQL URL, SECRET_KEY)
7. Deploy

### Frontend (Vercel)
1. Update `config.js` with production API URL from Render
2. Push repo to GitHub
3. Import project in Vercel
4. Deploy

## API Documentation
- `/docs` - Interactive API docs (Swagger UI)
- `/redoc` - ReDoc documentation

## Environment Variables

### Backend (.env)
```
DATABASE_URL=sqlite+aiosqlite:///./attendx.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
FRONTEND_URL=http://localhost:3000
RUN_SEED=false
```

Set `RUN_SEED=true` only for local development or demo environments. Keep it `false` in production.

### Frontend (config.js)
```javascript
const CONFIG = {
  API_BASE: 'http://localhost:8000',
  APP_NAME: 'AttendX',
  COLLEGE_NAME: 'Your College Name'
};
```

## Features
- **Authentication**: JWT-based with role-based access (admin, faculty, student)
- **Attendance**: Real-time marking, reports, defaulter detection
- **Timetable**: Schedule management with conflict detection
- **Activities**: Track workshops, seminars, competitions, industrial visits
- **Analytics**: Attendance trends, department comparisons, activity completion rates
- **Students**: Manage student records with bulk operations
- **Alumni**: Directory with company and role tracking
- **Reports**: Export attendance and activity data to CSV

## Database Schema
All models with relationships fully implemented:
- Users (authentication & roles)
- Colleges & Departments
- Students & Alumni
- Subjects & Timetable
- Attendance Sessions & Records
- Activities & Enrollments

## Tech Stack
**Backend**: FastAPI, SQLAlchemy, PostgreSQL/SQLite, JWT, Pydantic v2
**Frontend**: Vanilla JavaScript, HTML5, CSS3, Chart.js, Lucide Icons

## License
MIT
