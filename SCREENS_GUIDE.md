# AttendX - Visual Screen Guide

## 🖥️ Application Screens

### 1. LOGIN PAGE
```
┌─────────────────────────────────────┐
│         AttendX Login               │
├─────────────────────────────────────┤
│                                     │
│   📚 Smart Attendance System        │
│                                     │
│   Email:    [________________]      │
│   Password: [________________]      │
│                                     │
│      [  Login  ]   [Register]       │
│                                     │
│   Demo Credentials:                 │
│   admin@attendx.edu / Admin@123    │
│                                     │
└─────────────────────────────────────┘

✓ JWT Token-based authentication
✓ Secure password hashing (Argon2)
✓ Remember me checkbox
✓ Forgot password link
```

---

### 2. DASHBOARD (Main View)
```
┌──────────────────────────────────────────────────┐
│  AttendX  ≡  👤 Admin  🌙 Dark Mode  Logout      │
├──────────────────────────────────────────────────┤
│                                                  │
│  📊 DASHBOARD                                    │
│  ────────────────────────────────────────────    │
│                                                  │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐  │
│  │   Total    │ │ Attendance │ │  Active    │  │
│  │ Students   │ │   Rate     │ │ Activities │  │
│  │    350     │ │   87.5%    │ │     12     │  │
│  └────────────┘ └────────────┘ └────────────┘  │
│                                                  │
│  📈 ATTENDANCE HEATMAP                          │
│  ┌────────────────────────────────────────────┐ │
│  │  Mon  Tue  Wed  Thu  Fri  Sat  Sun         │ │
│  │  🟢   🟢   🟡   🟢   🟢   🟠   🔴         │ │
│  │  🟢   🟢   🟢   🟢   🟡   🟠   🔴         │ │
│  │  🟢   🟡   🟢   🟠   🟢   🔴   🔴         │ │
│  │  🟡   🟢   🟠   🟢   🟢   🔴   🔴         │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  📅 UPCOMING CLASSES                            │
│  ├─ 10:00 AM - Data Structures (Lab)           │
│  ├─ 11:30 AM - Database Design                 │
│  └─ 2:00 PM - Web Development (Lab)            │
│                                                  │
│  🎯 QUICK STATS                                 │
│  ├─ Defaulters: 8 students (<75%)              │
│  ├─ Best Department: Computer Science (92%)    │
│  └─ New Activities: 3 this week                │
│                                                  │
└──────────────────────────────────────────────────┘

✓ Real-time data from API
✓ Interactive heatmap
✓ Color-coded status (green/yellow/red)
✓ Quick action buttons
```

---

### 3. ATTENDANCE MANAGEMENT
```
┌──────────────────────────────────────────────────┐
│  AttendX  ≡  Attendance  ≡  📋  🔍  ⬇️          │
├──────────────────────────────────────────────────┤
│                                                  │
│  Mark Attendance  |  Reports  |  Trends         │
│  ────────────────                               │
│                                                  │
│  Date: [2026-04-18]  Subject: [Select Subject]  │
│                                                  │
│  Students:                                       │
│  ┌─────────────────────────────────────────┐   │
│  │ ☐ John Smith (CS-01)          Present   │   │
│  │ ☑ Sarah Johnson (CS-02)        Present   │   │
│  │ ☐ Mike Brown (CS-03)           Absent    │   │
│  │ ☑ Emily Davis (CS-04)          Present   │   │
│  │ ☐ Alex Wilson (CS-05)          Absent    │   │
│  │ ☑ Jessica Lee (CS-06)          Present   │   │
│  │                                          │   │
│  │   [  Mark All  ]  [  Clear All  ]       │   │
│  │   [  Save  ]  [  Export CSV  ]          │   │
│  └─────────────────────────────────────────┘   │
│                                                  │
│  Attendance Summary:                             │
│  Total: 6/8 | Rate: 75% | Absent: 2            │
│                                                  │
└──────────────────────────────────────────────────┘

✓ Bulk select/deselect
✓ Real-time calculation
✓ CSV export functionality
✓ Attendance history
```

---

### 4. ATTENDANCE REPORTS
```
┌──────────────────────────────────────────────────┐
│  AttendX  ≡  Attendance Reports  📊             │
├──────────────────────────────────────────────────┤
│                                                  │
│  Filter: [Department ▼] [Subject ▼] [Date ▼]  │
│                                                  │
│  Student: John Smith (CS-01)                    │
│  ────────────────────────────────────────────   │
│                                                  │
│  Department: Computer Science                   │
│  Year: 2023-24                                  │
│  Overall Attendance: 85% ✓ (Above 75%)         │
│                                                  │
│  Monthly Breakdown:                              │
│  ┌──────────────────────────────────────────┐  │
│  │ Jan: 90% | Feb: 87% | Mar: 85% | Apr: 82% │
│  │                                          │  │
│  │ [Line Chart showing trend]               │  │
│  │  /‾‾‾‾\  /‾‾\                            │  │
│  │ /      \/    \                           │  │
│  │/             \__                         │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  Subject-wise Breakdown:                         │
│  ├─ Data Structures: 88% (22/25)               │
│  ├─ Database Design: 84% (21/25)               │
│  ├─ Web Development: 82% (20/25)               │
│  └─ Algorithms: 86% (21/25)                    │
│                                                  │
│  [Download Report]  [Print]  [Email]           │
│                                                  │
└──────────────────────────────────────────────────┘

✓ Detailed per-student reports
✓ Subject-wise breakdown
✓ Trend visualization
✓ PDF/CSV export
```

---

### 5. TIMETABLE MANAGEMENT
```
┌──────────────────────────────────────────────────┐
│  AttendX  ≡  Timetable  ➕  📋                   │
├──────────────────────────────────────────────────┤
│                                                  │
│  Week of: [2026-04-18 ▼]                       │
│                                                  │
│  ┌─────────────────────────────────────────┐   │
│  │   Time    │ Mon    │ Tue    │ Wed    │   │   │
│  ├─────────────────────────────────────────┤   │
│  │ 9:00-10:00│ DS    │ DB     │ WEB    │   │   │
│  │ 10:15-11:15│ LAB   │ DS     │ ALG   │   │   │
│  │ 11:30-12:30│ ALGO  │ LAB    │ DB    │   │   │
│  │ 1:00-2:00 │ BREAK │ BREAK  │BREAK  │   │   │
│  │ 2:00-3:00 │ WEB   │ ALGO   │ LAB   │   │   │
│  │ 3:15-4:15 │ LAB   │ WEB    │ DS    │   │   │
│  └─────────────────────────────────────────┘   │
│                                                  │
│  Add New Class:                                  │
│  ┌──────────────────────────────────────┐      │
│  │ Date: [2026-04-18] Time: [09:00-10:00]    │ │
│  │ Subject: [Data Structures]            │      │
│  │ Faculty: [Prof. Johnson]              │      │
│  │ Room: [Lab-01]                        │      │
│  │ Capacity: [40]                        │      │
│  │                                       │      │
│  │ [Check Conflicts]  [Save]  [Cancel]  │      │
│  └──────────────────────────────────────┘      │
│                                                  │
│  ⚠️ Conflict Detection Active                  │
│                                                  │
└──────────────────────────────────────────────────┘

✓ Week/day view toggle
✓ Drag-and-drop (optional)
✓ Conflict detection
✓ Faculty/room assignment
✓ Color-coded subjects
```

---

### 6. ACTIVITIES MANAGEMENT
```
┌──────────────────────────────────────────────────┐
│  AttendX  ≡  Activities  ➕  🔍                  │
├──────────────────────────────────────────────────┤
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │ 🏆 Hackathon 2026                       │    │
│  │ Date: 2026-05-15 | Status: Open        │    │
│  │ Enrolled: 45/50                         │    │
│  │ Completion Rate: 80%                    │    │
│  │                                        │    │
│  │ [View Details] [Enroll] [Mark Complete]│    │
│  └────────────────────────────────────────┘    │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │ 🎓 Industry Talk - Google               │    │
│  │ Date: 2026-04-25 | Status: Upcoming   │    │
│  │ Enrolled: 120/150                       │    │
│  │ Completion Rate: 0% (Pending)           │    │
│  │                                        │    │
│  │ [View Details] [Enroll] [Share]        │    │
│  └────────────────────────────────────────┘    │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │ 📚 Web Development Workshop             │    │
│  │ Date: 2026-04-20 | Status: Completed  │    │
│  │ Enrolled: 35/40                         │    │
│  │ Completion Rate: 97%                    │    │
│  │                                        │    │
│  │ [View Details] [Statistics] [Report]   │    │
│  └────────────────────────────────────────┘    │
│                                                  │
└──────────────────────────────────────────────────┘

✓ Create new activities
✓ Student enrollment tracking
✓ Completion status
✓ Participation analytics
✓ Activity types (workshop, seminar, hackathon, competition)
```

---

### 7. ANALYTICS & REPORTS
```
┌──────────────────────────────────────────────────┐
│  AttendX  ≡  Analytics  📊 📈                   │
├──────────────────────────────────────────────────┤
│                                                  │
│  ┌─────────────────────────────────────┐       │
│  │ Attendance Trends (6 Months)         │       │
│  │                                     │       │
│  │  100%│     ╭─╮                      │       │
│  │   90%│    ╭─╮ ╭─╮                   │       │
│  │   80%│   ╭─╮ ╭─╮ ╭─╮               │       │
│  │   70%│──────────────────            │       │
│  │      └─────────────────────────     │       │
│  │      Jan Feb Mar Apr May Jun        │       │
│  └─────────────────────────────────────┘       │
│                                                  │
│  Department Comparison:                          │
│  ┌─────────────────────────────────────┐       │
│  │ CS:  ██████████░░ 92%               │       │
│  │ ECE: █████████░░░ 88%               │       │
│  │ ME:  ███████░░░░░░ 75%              │       │
│  │ Civil: ██████░░░░░░░ 70%            │       │
│  └─────────────────────────────────────┘       │
│                                                  │
│  Activity Completion:                            │
│  │ Workshops: 85% │ Seminars: 92%              │
│  │ Hackathons: 75% │ Competitions: 88%         │
│                                                  │
│  [Export Report]  [Share]  [Print]             │
│                                                  │
└──────────────────────────────────────────────────┘

✓ Interactive charts (Chart.js)
✓ 6-month historical data
✓ Department-wise analytics
✓ Activity-wise statistics
✓ PDF/Excel export
```

---

### 8. STUDENT DIRECTORY
```
┌──────────────────────────────────────────────────┐
│  AttendX  ≡  Students  🔍  ⬇️  ➕               │
├──────────────────────────────────────────────────┤
│                                                  │
│  Filter: [Dept ▼] [Year ▼] [Status ▼]         │
│  Search: [_____________________]               │
│                                                  │
│  ┌──────────────────────────────────────┐      │
│  │ John Smith (CS-01)                   │      │
│  │ Email: john@attendx.edu              │      │
│  │ Department: Computer Science         │      │
│  │ Attendance: 85% ✓ | Activities: 4    │      │
│  │ [View Profile] [Edit] [Delete]       │      │
│  └──────────────────────────────────────┘      │
│                                                  │
│  ┌──────────────────────────────────────┐      │
│  │ Sarah Johnson (CS-02)                │      │
│  │ Email: sarah@attendx.edu             │      │
│  │ Department: Computer Science         │      │
│  │ Attendance: 92% ✓ | Activities: 6    │      │
│  │ [View Profile] [Edit] [Delete]       │      │
│  └──────────────────────────────────────┘      │
│                                                  │
│  ┌──────────────────────────────────────┐      │
│  │ Mike Brown (CS-03)                   │      │
│  │ Email: mike@attendx.edu              │      │
│  │ Department: Computer Science         │      │
│  │ Attendance: 72% ✗ | Activities: 2    │      │
│  │ [View Profile] [Edit] [Delete]       │      │
│  └──────────────────────────────────────┘      │
│                                                  │
│  Showing 3 of 30 students | [Next Page] [Export]│
│                                                  │
└──────────────────────────────────────────────────┘

✓ Search and filter
✓ Bulk export to CSV
✓ Individual student profiles
✓ Quick attendance view
✓ Activity enrollment status
```

---

### 9. ALUMNI DIRECTORY
```
┌──────────────────────────────────────────────────┐
│  AttendX  ≡  Alumni  🎓  🔍  ⬇️                 │
├──────────────────────────────────────────────────┤
│                                                  │
│  Filter: [Company ▼] [Year ▼]                  │
│  Search: [_____________________]               │
│                                                  │
│  ┌──────────────────────────────────────┐      │
│  │ Rajesh Kumar (2020)                  │      │
│  │ Company: Google                      │      │
│  │ Position: Senior SDE                 │      │
│  │ Email: rajesh@google.com             │      │
│  │ LinkedIn: linkedin.com/in/rajesh     │      │
│  └──────────────────────────────────────┘      │
│                                                  │
│  ┌──────────────────────────────────────┐      │
│  │ Priya Singh (2021)                   │      │
│  │ Company: Microsoft                   │      │
│  │ Position: Product Manager            │      │
│  │ Email: priya@microsoft.com           │      │
│  │ LinkedIn: linkedin.com/in/priya      │      │
│  └──────────────────────────────────────┘      │
│                                                  │
│  ┌──────────────────────────────────────┐      │
│  │ Amit Patel (2019)                    │      │
│  │ Company: Amazon                      │      │
│  │ Position: Tech Lead                  │      │
│  │ Email: amit@amazon.com               │      │
│  │ LinkedIn: linkedin.com/in/amit       │      │
│  └──────────────────────────────────────┘      │
│                                                  │
│  Alumni Statistics:                              │
│  │ Total: 250 | Employed: 240 (96%)            │
│  │ Top Companies: Google (45), Microsoft (38)  │
│                                                  │
└──────────────────────────────────────────────────┘

✓ Alumni profiles
✓ Company tracking
✓ Employment statistics
✓ Filter and search
✓ CSV export
```

---

### 10. SETTINGS PAGE
```
┌──────────────────────────────────────────────────┐
│  AttendX  ≡  Settings  ⚙️                        │
├──────────────────────────────────────────────────┤
│                                                  │
│  👤 PROFILE                                      │
│  ├─ Name: Admin User                           │
│  ├─ Email: admin@attendx.edu                   │
│  ├─ Role: Administrator                        │
│  └─ [Edit Profile] [Change Password]           │
│                                                  │
│  🎨 APPEARANCE                                   │
│  ├─ Theme: [Dark Mode] ☑️  [Light Mode]        │
│  ├─ Font Size: [Normal ▼]                      │
│  └─ Notifications: [Enabled] ☑️                │
│                                                  │
│  🔒 SECURITY                                     │
│  ├─ Two-Factor Auth: [Disabled]                │
│  ├─ Login Activity: [View Logs]                │
│  └─ Active Sessions: 1                         │
│                                                  │
│  📧 NOTIFICATIONS                                │
│  ├─ Email Alerts: ☑️                           │
│  ├─ Attendance Reminders: ☑️                   │
│  └─ Activity Updates: ☑️                       │
│                                                  │
│  ⚠️ DANGER ZONE                                 │
│  ├─ [Export My Data]                           │
│  ├─ [Delete Account]                           │
│  └─ [Logout from All Devices]                  │
│                                                  │
│  [Save Changes]  [Cancel]  [Logout]            │
│                                                  │
└──────────────────────────────────────────────────┘

✓ Profile management
✓ Theme toggle (dark/light)
✓ Security settings
✓ Notification preferences
✓ Data export
```

---

## 🎨 Design System

### Colors
- **Primary**: #2563eb (Blue)
- **Success**: #10b981 (Green)
- **Warning**: #f59e0b (Amber)
- **Danger**: #ef4444 (Red)
- **Dark**: #1f2937 (Dark Gray)
- **Light**: #f3f4f6 (Light Gray)

### Typography
- **Headings**: 24px, 600 weight
- **Body**: 14px, 400 weight
- **Small**: 12px, 400 weight

### Responsive Breakpoints
- **Mobile**: 480px
- **Tablet**: 768px
- **Desktop**: 1024px+
- **Large**: 1440px+

---

## ✨ Interactive Features

✓ Real-time data updates  
✓ Modal dialogs for CRUD operations  
✓ Toast notifications (success/error/info)  
✓ Loading spinners  
✓ Confirmation dialogs  
✓ Data export (CSV)  
✓ Dark/Light theme toggle  
✓ Responsive navigation  
✓ Search and filter  
✓ Pagination  

---

**Ready to explore! Visit the preview in the Orchids IDE.**
