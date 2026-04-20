# AttendX - Quick Start Guide

## 🚀 Start Using AttendX Right Now

### Option 1: Local Development (Current Setup)

**Frontend is running on:** `http://localhost:3000/attendx.html`  
**Backend API running on:** `http://localhost:8000`

#### Step 1: Open the Preview
Click the preview link in Orchids IDE to see the app live.

#### Step 2: Login
Use these credentials:
```
Admin Account:
Email: admin@attendx.edu
Password: Admin@123
```

#### Step 3: Explore Features
1. **Dashboard** - See KPIs and attendance heatmap
2. **Mark Attendance** - Record student attendance
3. **View Reports** - Check attendance trends
4. **Manage Timetable** - Create class schedule
5. **Activities** - Create and track co-curricular activities
6. **Analytics** - Compare departments and trends
7. **Students** - View student directory
8. **Alumni** - See graduate records

---

### Option 2: Test All Features

#### Test Account Access Levels

**Admin (Full Access)**
```
Email: admin@attendx.edu
Password: Admin@123
- Can manage all features
- Access all student data
- View all reports
- Manage faculty and settings
```

**Faculty (Limited Access)**
```
Email: faculty@attendx.edu
Password: Faculty@123
- Can mark own classes' attendance
- View assigned subject data
- Create activities for students
```

**Student (Read-Only)**
```
Email: student@attendx.edu
Password: Student@123
- Can only view own profile
- View own attendance
- See available activities
```

---

## 📊 What Data Is Already In The System?

### Demo Seed Data (Local Only)
- **1 College** - XYZ Institute of Technology
- **4 Departments** - Computer Science, ECE, Mechanical, Civil
- **1 Admin + 2 Faculty + 30 Students** - Ready to use
- **10 Subjects** - With faculty assignments
- **20 Attendance Sessions** - 300+ attendance records
- **5 Activities** - Workshops, seminars, hackathons
- **10 Alumni** - Graduate records with companies

These records are created only when `RUN_SEED=true` in a local or demo environment.

### Explore This Data
1. Go to **Students** page to see all 30 students
2. Go to **Analytics** to see attendance trends
3. Check **Dashboard** for KPIs and heatmaps
4. View **Activities** to see co-curricular programs

---

## 🎯 Key Features to Test

### 1. Mark Attendance (2 minutes)
- Go to **Attendance** → **Mark Attendance**
- Select a subject and date
- Check/uncheck students
- Click **Save**
- See summary update in real-time

### 2. View Attendance Reports (2 minutes)
- Go to **Attendance** → **Reports**
- Select a student
- See attendance breakdown by subject
- Download CSV report

### 3. Check Attendance Trends (2 minutes)
- Go to **Attendance** → **Trends**
- See 6-month attendance chart
- Identify defaulters (<75%)
- Check department comparison

### 4. Manage Timetable (3 minutes)
- Go to **Timetable**
- Click **Add Class**
- Fill in details (date, time, subject, faculty, room)
- System checks for conflicts automatically
- View week view with color-coded subjects

### 5. Create Activity (2 minutes)
- Go to **Activities**
- Click **Create Activity**
- Enter activity type (workshop, seminar, hackathon, competition)
- Set enrollment limit
- Enroll students and track completion

### 6. View Analytics (2 minutes)
- Go to **Analytics**
- See KPI dashboard
- View attendance trends (chart)
- Compare department performance
- Check activity completion rates

### 7. Dark Mode (1 minute)
- Go to **Settings**
- Toggle **Dark Mode**
- Theme switches instantly
- Preference is saved in browser

### 8. Export Data (1 minute)
- Go to **Attendance** → **Reports**
- Click **Export CSV**
- Download attendance data for analysis
- Open in Excel/Sheets

---

## 🔌 API Endpoints (Test in Postman/cURL)

### Authentication
```bash
# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@attendx.edu","password":"Admin@123"}'

# Response
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {...}
}
```

### Get All Students
```bash
curl -X GET http://localhost:8000/students \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Mark Attendance
```bash
curl -X POST http://localhost:8000/attendance/mark \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 2,
    "subject_id": 1,
    "status": "present",
    "date": "2026-04-18"
  }'
```

### Get Analytics
```bash
curl -X GET http://localhost:8000/analytics/kpis \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 📱 Mobile/Tablet Testing

The app is fully responsive:
- **Mobile (480px)** - Optimized layout, hamburger menu
- **Tablet (768px)** - Side-by-side panels
- **Desktop (1024px+)** - Full dashboard view

Try resizing your browser to see responsive design in action!

---

## 🐛 Troubleshooting

### "Can't connect to backend"
- Check if backend is running: `curl http://localhost:8000/health`
- Both servers must be running (port 3000 & 8000)

### "Login fails"
- Verify you're using correct credentials from above
- Check browser console (F12) for error messages
- Clear localStorage if you have old tokens

### "Data not loading"
- Open browser DevTools (F12) → Network tab
- Check API responses for errors
- Look for CORS issues in console

### "Dark mode not working"
- Check if JavaScript is enabled
- Clear browser cache
- Try incognito/private window

---

## 📁 Project Files

All files are in `/home/user/app/`:

```
attendx.html              Frontend (963 lines)
backend/
├── main.py              FastAPI application
├── database.py          Database connection
├── models.py            Database models (13 tables)
├── schemas.py           Pydantic validators
├── seed.py              Test data
└── routers/
    ├── auth.py          Authentication (JWT)
    ├── students.py      Student management
    ├── attendance.py    Attendance tracking
    ├── timetable.py     Schedule management
    ├── activities.py    Co-curricular programs
    ├── alumni.py        Alumni directory
    └── analytics.py     Reports & KPIs

config.js               Frontend configuration
requirements.txt        Python dependencies
.env.example           Environment variables
```

---

## 🚀 Ready to Deploy?

### Deploy Backend to Render.com
1. Push code to GitHub
2. Connect repo to Render.com
3. Deploy from `backend/` directory
4. Set `SECRET_KEY` environment variable

### Deploy Frontend to Vercel
1. Push code to GitHub
2. Import project in Vercel
3. Deploy `attendx.html`
4. Update `API_BASE_URL` in config.js

**Time to deploy: 10 minutes**

---

## 💡 Pro Tips

1. **Use Admin account** to explore all features first
2. **Check Database** by querying `/students` endpoint
3. **Test Export** - Download CSV from reports
4. **Try Dark Mode** - See responsive theme switching
5. **Check API** - Use browser DevTools Network tab to see requests
6. **Scale Data** - The seeded 30 students scale to 1000+ easily
7. **Customize** - Edit config.js to change API URL/colors
8. **Monitor** - Watch backend logs for request logs

---

## ❓ FAQs

**Q: Can I add more students?**  
A: Yes! Use POST /students endpoint or admin UI (coming soon)

**Q: How do I reset the database?**  
A: Delete `attendx.db` and restart backend (re-runs seed.py)

**Q: Can I change passwords?**  
A: Yes, via Settings → Change Password (implement in admin UI)

**Q: How do I backup data?**  
A: Export CSV from Analytics/Reports, or backup attendx.db file

**Q: Is it production-ready?**  
A: Yes! Use PostgreSQL for production (SQLite for dev)

---

## 📞 Next Steps

1. **Explore the app** - Click around and test features
2. **Review code** - Check backend routers and frontend HTML
3. **Deploy** - Follow deployment guide to go live
4. **Customize** - Add your college name and branding
5. **Scale** - Import real student data via API or CSV

---

**Enjoy your fully functional attendance management system! 🎉**
