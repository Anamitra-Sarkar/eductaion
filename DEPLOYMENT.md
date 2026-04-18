# AttendX - Deployment Guide

Complete production-ready deployment instructions.

## Project Structure

```
attendx/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # SQLAlchemy async setup
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic v2 schemas
│   ├── seed.py              # Sample data seeder
│   ├── requirements.txt      # Python dependencies
│   ├── .env.example         # Environment variables template
│   ├── Procfile             # Heroku/Render deployment
│   ├── render.yaml          # Render.com configuration
│   └── routers/
│       ├── auth.py          # Authentication & JWT
│       ├── students.py      # Student management
│       ├── attendance.py    # Attendance tracking
│       ├── timetable.py     # Schedule management
│       ├── activities.py    # Activity management
│       ├── alumni.py        # Alumni directory
│       └── analytics.py     # Reports & analytics
├── attendx.html             # Frontend (single file, ~1737 lines)
├── config.js                # Frontend configuration
├── vercel.json              # Vercel deployment
├── README.md                # Quick start
├── DEPLOYMENT.md            # This file
└── .gitignore               # Git exclusions
```

## Backend Deployment (Render.com)

### Option 1: Using render.yaml (Recommended)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Create PostgreSQL database** (Render)
   - Go to https://render.com
   - Click "New +" → "PostgreSQL"
   - Set name: `attendx-db`
   - Copy connection string

3. **Deploy service** (Render)
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Select the repo
   - Configure:
     - **Name:** `attendx-api`
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Add environment variables:
     ```
     DATABASE_URL=postgresql://user:pass@host:5432/attendx_db
     SECRET_KEY=<generate-random-string>
     ALGORITHM=HS256
     ACCESS_TOKEN_EXPIRE_MINUTES=1440
     FRONTEND_URL=https://attendx.vercel.app
     ```
   - Deploy

4. **Initialize database**
   - Once deployed, run seed script in Render shell:
   ```bash
   python seed.py
   ```

### Option 2: Manual on Render

1. Skip render.yaml, use Web Service directly
2. Connect GitHub
3. Manually configure build/start commands
4. Set environment variables

### Verify deployment
- Visit `https://attendx-api.onrender.com/docs` for Swagger UI
- Check `/health` endpoint

## Frontend Deployment (Vercel)

1. **Update config.js**
   ```javascript
   const CONFIG = {
     API_BASE: 'https://attendx-api.onrender.com',
     APP_NAME: 'AttendX',
     COLLEGE_NAME: 'Your Institution'
   };
   ```

2. **Deploy to Vercel**
   - Go to https://vercel.com
   - Click "Add New..." → "Project"
   - Import GitHub repository
   - Configure:
     - **Framework:** Other
     - **Root Directory:** ./
   - Deploy

3. **Verify**
   - Frontend at `https://attendx.vercel.app`
   - Login with `admin@college.edu` / `Admin@123`

## Local Development

### 1. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Create .env file
```bash
cp .env.example .env
```

### 3. Seed database
```bash
python seed.py
```

This creates:
- 1 admin user: `admin@college.edu` / `Admin@123`
- 2 faculty users
- 4 departments
- 30 students
- 10 subjects
- Weekly timetable
- 5 activities
- 10 alumni records
- Sample attendance & enrollments

### 4. Run backend
```bash
uvicorn main:app --reload
```
Runs at `http://localhost:8000`

### 5. Serve frontend
```bash
# In project root
python -m http.server 8080
```
Open `http://localhost:8080/attendx.html`

## API Documentation

Once running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Database Migrations (Alembic)

### Initialize (already done)
```bash
alembic init -t async migrations
```

### Create migration after model changes
```bash
alembic revision --autogenerate -m "Add new column"
```

### Apply migrations
```bash
alembic upgrade head
```

### Downgrade
```bash
alembic downgrade -1
```

## Environment Variables

### Backend (.env)
| Variable | Default | Description |
|----------|---------|-------------|
| DATABASE_URL | sqlite+aiosqlite:///./attendx.db | Database connection string |
| SECRET_KEY | your-secret-key | JWT secret (change in production) |
| ALGORITHM | HS256 | JWT algorithm |
| ACCESS_TOKEN_EXPIRE_MINUTES | 1440 | Token expiry (24 hours) |
| FRONTEND_URL | http://localhost:3000 | CORS origin |

### Frontend (config.js)
| Variable | Default | Description |
|----------|---------|-------------|
| API_BASE | http://localhost:8000 | Backend API URL |
| APP_NAME | AttendX | Application name |
| COLLEGE_NAME | Institute of Technology Excellence | Institution name |

## Production Checklist

- [ ] Backend deployed to Render with PostgreSQL
- [ ] Frontend deployed to Vercel
- [ ] config.js updated with production API URL
- [ ] Database seeded with initial data
- [ ] SSL certificates auto-configured (Render/Vercel handle this)
- [ ] Email alerts configured (optional)
- [ ] Backup strategy for database
- [ ] Monitor uptime & performance

## Troubleshooting

### "Connection refused" error
- Check if backend is running
- Verify API_BASE in config.js
- Check CORS settings in main.py

### Database errors
- Ensure DATABASE_URL is correct
- Run `python seed.py` to initialize tables
- Check PostgreSQL credentials

### Authentication fails
- Verify SECRET_KEY is set
- Check token expiry in ACCESS_TOKEN_EXPIRE_MINUTES
- Clear browser cache

### Frontend not loading
- Check browser console for errors
- Verify attendx.html is being served
- Ensure Vercel routing is configured

## Performance Optimization

### Database
- Add indexes on frequently queried columns
- Use connection pooling (SQLAlchemy pool_size)
- Archive old attendance records

### Frontend
- Minify CSS/JS for production
- Lazy load charts with intersection observer
- Implement pagination for large tables

### Backend
- Enable async/await for I/O operations
- Cache frequent queries (Redis optional)
- Rate limit API endpoints

## Monitoring

### Render
- Dashboard shows uptime & resource usage
- Logs available in console
- Alerting for crashes

### Vercel
- Analytics for page performance
- Real-time error tracking
- Deployment history

## Support

For issues:
1. Check backend logs: Render dashboard → Logs
2. Check frontend errors: Browser DevTools → Console
3. Verify API connectivity: `curl https://attendx-api.onrender.com/health`
4. Review database: Connect via pgAdmin to PostgreSQL

## Security Notes

- Change `SECRET_KEY` before production
- Use strong PostgreSQL passwords
- Enable HTTPS (automatic on Render/Vercel)
- Keep dependencies updated
- Regularly backup database
- Monitor access logs
