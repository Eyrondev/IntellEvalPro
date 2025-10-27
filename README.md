# IntellEvalPro - Faculty Evaluation System

A comprehensive, mobile-responsive web application for faculty evaluation and academic performance management built with Flask and MySQL using modern blueprint architecture.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-Educational-yellow.svg)](LICENSE)

---

## 📖 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Default Login Credentials](#-default-login-credentials)
- [Mobile Responsiveness](#-mobile-responsiveness)
- [Email Notification System](#-email-notification-system)
- [Project Structure](#️-project-structure)
- [Configuration](#-configuration)
- [User Roles & Permissions](#-user-roles--permissions)
- [API Endpoints](#-api-endpoints)
- [Database Schema](#-database-schema)
- [Security Features](#️-security-features)
- [Browser & Device Support](#-browser--device-support)
- [Development Workflow](#-development-workflow)
- [Deployment Guide](#-deployment-guide)
- [Troubleshooting](#-troubleshooting)
- [Version History & Changelog](#-version-history--changelog)
- [License](#-license)
- [Contributing](#-contributing)
- [Support & Contact](#-support--contact)

---

## 🌟 Features

### Core Functionality
- **Role-based Access Control**: Admin, Student, and Guidance Counselor roles with secure authentication
- **Faculty Evaluation System**: Complete evaluation workflow with timer controls and progress tracking
- **Automated Email Notifications**: Students receive personalized emails when evaluation periods start
- **Real-time Analytics**: Advanced performance analytics with Chart.js visualizations
- **Questionnaire Management**: Dynamic questionnaire creation with multiple question types
- **AI-Powered Insights**: Google Gemini integration for intelligent evaluation analysis
- **Comprehensive Reporting**: PDF and Excel export functionality using ReportLab and OpenPyXL
- **Academic Year Management**: Multi-year evaluation tracking with period-based organization

### Dashboard Features

#### 👤 Admin Dashboard
- User management (students, faculty, guidance counselors)
- Academic year and evaluation period configuration
- Faculty assignment to departments and subjects
- Class, section, and subject management
- Activity logs and system monitoring
- Archive management for historical data

#### 🎓 Student Dashboard
- View and complete faculty evaluations with countdown timer
- Track evaluation progress and completion status
- Manage personal profile and account settings
- Help and support resources
- Anonymous evaluation guarantee

#### 🧭 Guidance Counselor Dashboard
- Faculty performance analytics with interactive charts
- Evaluation results and insights dashboard
- Questionnaire template management
- Student and faculty management
- AI-powered analytics dashboard
- Comprehensive reporting tools

### Technical Features
- **Blueprint Architecture**: Modular Flask design with separated routes
- **Mobile-First Responsive Design**: Optimized for 390px minimum to ultrawide displays
- **Modern UI/UX**: Built with Tailwind CSS 3.x and smooth animations
- **Secure Authentication**: Custom password hashing and role-based decorators
- **RESTful API**: Clean API endpoints for data exchange
- **Session Management**: Secure session handling with timeout protection
- **Database Models**: SQLAlchemy ORM with optimized queries
- **Error Handling**: Comprehensive error handling and logging

## � Screenshots

### Admin Dashboard
![Admin Dashboard](docs/screenshots/admin-dashboard.png)
*Comprehensive system management with user analytics and quick actions*

### Student Dashboard
![Student Dashboard](docs/screenshots/student-dashboard.png)
*Clean interface for viewing and completing faculty evaluations*

### Guidance Analytics
![Guidance Analytics](docs/screenshots/guidance-analytics.png)
*Interactive charts and performance insights with AI-powered recommendations*

### Evaluation Form
![Evaluation Form](docs/screenshots/evaluation-form.png)
*Mobile-responsive evaluation form with countdown timer*

### Mobile Responsiveness
![Mobile View](docs/screenshots/mobile-view.png)
*Fully optimized for mobile devices from 390px minimum width*

> **Note**: Screenshots are available in the `docs/screenshots/` folder. To add your own screenshots, capture images and place them in that directory.

## �📋 Prerequisites

1. **XAMPP 8.2+** or any MySQL server - For database management
2. **Python 3.9+** - Programming language runtime
3. **pip** - Python package manager (included with Python)
4. **Modern Web Browser** - Chrome 80+, Firefox 75+, Safari 13+, or Edge 80+
5. **Git** - Version control (optional but recommended)

## 🚀 Quick Start

### 1. Clone the Repository

```cmd
git clone https://github.com/Eyrondev/IntellEvalPro.git
cd IntellEvalPro
```

### 2. Database Setup

#### Option A: Using phpMyAdmin (Recommended for beginners)

1. Start XAMPP control panel and ensure **MySQL** service is running
2. Open phpMyAdmin: http://localhost/phpmyadmin
3. Create new database named `intellevalpro_db`
4. Import the schema:
   - Click on the database → Import tab
   - Choose file: `database/intellevalpro_db.sql`
   - Click "Go" to import

#### Option B: Using MySQL Command Line

```cmd
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS intellevalpro_db;"
mysql -u root -p intellevalpro_db < database\intellevalpro_db.sql
```

#### MySQL Compatibility Fix (If needed)

If you encounter MySQL 8.0+ compatibility issues, run:

```cmd
cd database
mysql_compatibility_fix.bat
```

Or manually:
```cmd
mysql -u root -p intellevalpro_db < database\mysql_compatibility_fix.sql
```

See `database/MYSQL_COMPATIBILITY_GUIDE.md` for detailed troubleshooting.

### 3. Python Environment Setup

#### Option A: Using Virtual Environment (Recommended)

```cmd
# Create virtual environment (if not exists)
python -m venv env

# Activate virtual environment
env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Option B: Global Installation

```cmd
pip install -r requirements.txt
```

### 4. Environment Configuration

1. Create `.env` file in project root:

```cmd
copy .env.example .env
```

2. Edit `.env` file with your settings:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True

# Database Configuration (Local Development)
DATABASE_URL=mysql+pymysql://root:@localhost:3306/intellevalpro_db

# Server Configuration
HOST=0.0.0.0
PORT=5000
APP_URL=http://localhost:5000

# Email Configuration (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_REPLY_TO=your-email@gmail.com
```

#### Email Setup (Optional but Recommended)

For automated student notifications:

**Gmail Setup:**
1. Enable 2-Factor Authentication on your Google Account
2. Generate App Password: Google Account → Security → 2-Step Verification → App passwords
3. Use the generated 16-character password in `.env`

See `docs/GMAIL_APP_PASSWORD_SETUP.md` for detailed instructions.

**AWS SES Setup (Production):**
See `docs/AWS_EMAIL_SETUP.md` for production email configuration.

### 5. Run the Application

```cmd
# With virtual environment activated
python app.py

# Or directly
python app.py
```

The application will start at: **http://localhost:5000**

**Note**: The application uses modular blueprint architecture with automatic database initialization.

## 🔐 Default Login Credentials

After importing the database, use these credentials to access the system:

| Role | Username | Password | Features |
|------|----------|----------|----------|
| **Admin** | `admin` | `admin123` | Full system management, user creation, evaluation periods |
| **Student** | `2022-0215` | `student123` | Complete evaluations, track progress, view assigned faculty |
| **Guidance** | `guidance` | `guidance123` | Analytics dashboard, questionnaire management, reporting |

⚠️ **Security Note**: Change these default passwords immediately after first login in production environments.

## 📱 Mobile Responsiveness

IntellEvalPro is built with a **mobile-first approach** ensuring perfect functionality across all devices:

### Supported Screen Sizes
- **Mobile Portrait**: 390px minimum width (iPhone 12/13/14 baseline)
- **Mobile Landscape**: 640px+ (large phones)
- **Tablet**: 768px+ (iPad, Android tablets)
- **Laptop**: 1024px+ (standard laptops)
- **Desktop**: 1440px+ (desktop monitors)
- **Ultrawide**: 1920px+ (large displays)

### Mobile Features
- **Touch-Optimized Navigation**: Hamburger menu with smooth animations
- **Responsive Tables**: Horizontal scroll or card transformation on mobile
- **Touch-Friendly Interactions**: Minimum 44×44px tap targets
- **Adaptive Typography**: Scalable text sizes for readability
- **Optimized Forms**: Stack layouts on mobile, inline on desktop
- **Mobile-First Modals**: Full-screen on mobile, centered on desktop
- **Performance Optimized**: Lazy loading, efficient CSS, minimal JavaScript

### Responsive Components
- Navigation bars with role-specific menus
- Evaluation forms with countdown timers
- Interactive charts and analytics
- Data tables with mobile-friendly layouts
- Modals and dialogs
- Profile management interfaces

All pages tested and optimized across Chrome DevTools device emulation and real devices.

## 📧 Email Notification System

Automated email system to keep students informed about evaluation deadlines:

### Features
- **Automatic Triggers**: Emails sent when evaluation periods become "Active"
- **Personalized Content**: Student name, period title, deadline prominently displayed
- **Professional Design**: Norzagaray College branding, mobile-responsive HTML templates
- **Bulk Sending**: Efficient batch email delivery to all enrolled students
- **Status Tracking**: Email delivery confirmation and error logging

### When Emails Are Sent
1. **Immediate**: Creating a period with today's start date (status: Active)
2. **Scheduled**: Automatic transition from "Upcoming" to "Active" status
3. **Manual**: Admin can manually trigger notifications

### Email Content Includes
- Personalized greeting with student's full name
- Evaluation period title and academic year
- **Start date and deadline** (end date) clearly displayed
- Direct link to evaluation dashboard
- Anonymous evaluation reminder
- Help and support contact information

### Supported Email Providers
- **Gmail**: Via SMTP with App Password (recommended for development)
- **AWS SES**: For production environments (see `docs/AWS_EMAIL_SETUP.md`)
- **Custom SMTP**: Any SMTP server compatible with Flask-Mail

### Configuration
Configure in `.env` file:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_REPLY_TO=guidance@norzagaraycollege.edu.ph
```

See `docs/GMAIL_APP_PASSWORD_SETUP.md` for detailed Gmail setup instructions.

## 🛠️ Project Structure

IntellEvalPro uses a **modular blueprint architecture** for clean separation of concerns:

```
IntellEvalPro/
├── app.py                      # Main Flask application factory
├── config.py                   # Configuration management (dev/prod/test)
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .env                        # Environment variables (create from .env.example)
├── .gitignore                 # Git ignore rules
│
├── models/                     # Database models and business logic
│   ├── __init__.py            # Model initialization
│   ├── database.py            # Database connection and SQLAlchemy setup
│   ├── user.py                # User model and authentication
│   ├── student.py             # Student model and queries
│   ├── faculty.py             # Faculty model and queries
│   ├── evaluation.py          # Evaluation model and logic
│   └── analytics.py           # Analytics queries and calculations
│
├── routes/                     # Flask blueprints (route handlers)
│   ├── __init__.py            # Blueprint registration
│   ├── auth.py                # Authentication routes (login, logout, signup)
│   ├── admin.py               # Admin dashboard and management
│   ├── student.py             # Student dashboard and evaluations
│   ├── guidance.py            # Guidance counselor features
│   ├── api.py                 # RESTful API endpoints
│   └── analytics.py           # Analytics and reporting routes
│
├── templates/                  # Jinja2 HTML templates
│   ├── admin/                 # Admin interface pages
│   │   ├── components/        # Reusable admin components
│   │   ├── admin-dashboard.html
│   │   ├── user-management.html
│   │   ├── evaluation-periods.html
│   │   ├── faculty-list.html
│   │   ├── student-list.html
│   │   ├── academic-years.html
│   │   ├── classes.html
│   │   ├── sections.html
│   │   ├── subjects.html
│   │   ├── activity-logs.html
│   │   └── archives.html
│   │
│   ├── student/               # Student interface pages
│   │   ├── components/        # Reusable student components
│   │   ├── student-dashboard.html
│   │   ├── evaluation-form.html
│   │   ├── profile.html
│   │   └── help-support.html
│   │
│   ├── guidance/              # Guidance counselor pages
│   │   ├── components/        # Reusable guidance components
│   │   ├── guidance-dashboard.html
│   │   ├── evaluation-results.html
│   │   ├── questionnaire-management.html
│   │   ├── faculty-management.html
│   │   ├── student-management.html
│   │   ├── evaluation-periods.html
│   │   ├── ai-analytics-dashboard.html
│   │   └── help-support.html
│   │
│   ├── auth/                  # Authentication pages
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── forgot-password.html
│   │   └── reset-password.html
│   │
│   └── public/                # Public pages (landing, about)
│
├── static/                     # Static assets
│   ├── css/                   # Stylesheets
│   │   └── mobile-responsive.css
│   ├── js/                    # JavaScript files
│   │   ├── admin-navigation.js
│   │   ├── student-navigation-unified.js
│   │   ├── guidance-navigation.js
│   │   ├── evaluation-timer.js
│   │   ├── loading-animation.js
│   │   ├── mobile-responsive.js
│   │   ├── session-timeout.js
│   │   ├── prevent-back-logout.js
│   │   └── initialize-navigation.js
│   ├── images/                # Images and logos
│   │   └── nclogo.png
│   └── reports/               # Generated PDF/Excel reports
│
├── utils/                      # Utility functions and helpers
│   ├── __init__.py            # Utility initialization
│   ├── decorators.py          # Custom decorators (auth, role-based)
│   ├── security.py            # Password hashing and security
│   ├── validators.py          # Input validation functions
│   ├── email_utils.py         # Email sending utilities
│   ├── json_encoder.py        # Custom JSON encoder for Decimal
│   ├── ai_support.py          # Google Gemini AI integration
│   └── expired_evaluations.py # Evaluation expiration logic
│
├── database/                   # Database schemas and scripts
│   ├── intellevalpro_db.sql   # Main database schema
│   ├── intellevalpro_db (19).sql  # Latest backup
│   ├── mysql_compatibility_fix.sql # MySQL 8.0+ compatibility
│   ├── mysql_compatibility_fix.bat # Automated fix script
│   ├── MYSQL_COMPATIBILITY_GUIDE.md
│   ├── QUICK_START.md
│   └── TESTING_GUIDE.md
│
├── docs/                       # Documentation
│   ├── GMAIL_APP_PASSWORD_SETUP.md
│   ├── AWS_EMAIL_SETUP.md
│   ├── AWS_SECRETS_MANAGEMENT.md
│   ├── VIDEO_SCRIPT_ADMIN.md
│   ├── VIDEO_SCRIPT_STUDENT.md
│   └── VIDEO_SCRIPT_GUIDANCE.md
│
└── env/                        # Python virtual environment (excluded from git)
    ├── Scripts/
    └── Lib/
```

### Architecture Highlights

- **Blueprint Pattern**: Modular routes for scalability
- **SQLAlchemy ORM**: Database abstraction with models
- **Jinja2 Templates**: Component-based UI rendering
- **Role-Based Components**: Separate navigation and UI per role
- **Utility Layer**: Reusable functions and decorators
- **Configuration Management**: Environment-based config (dev/prod/test)

## 🔧 Configuration

### Database Configuration

The application uses SQLAlchemy with MySQL. Configure in `.env`:

```env
# Local Development
DATABASE_URL=mysql+pymysql://root:@localhost:3306/intellevalpro_db

# Production (AWS RDS example)
DATABASE_URL=mysql+pymysql://admin:password@host.region.rds.amazonaws.com/intellevalpro_db
```

Or update `config.py` directly:

```python
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:@localhost:3306/intellevalpro_db'
    )
```

### Application Configuration

Key settings in `config.py`:

```python
# Flask Configuration
SECRET_KEY = 'your-secret-key'  # Change in production!
DEBUG = True  # False in production

# Session Configuration
PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
SESSION_COOKIE_SECURE = False  # True with HTTPS
SESSION_COOKIE_HTTPONLY = True

# Upload Configuration
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
```

### Environment Variables

Create `.env` file with these variables:

```env
# Flask
SECRET_KEY=change-this-to-random-string
DEBUG=True

# Database
DATABASE_URL=mysql+pymysql://root:@localhost:3306/intellevalpro_db

# Server
HOST=0.0.0.0
PORT=5000
APP_URL=http://localhost:5000

# Email (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_REPLY_TO=guidance@norzagaraycollege.edu.ph

# AI (Optional - Google Gemini)
GOOGLE_API_KEY=your-gemini-api-key
```

### Security Configuration (Production)

For production deployment:

1. **Change SECRET_KEY**: Generate random secret
   ```python
   import secrets
   secrets.token_hex(32)
   ```

2. **Disable DEBUG mode**: Set `DEBUG=False` in `.env`

3. **Enable HTTPS**: Set `SESSION_COOKIE_SECURE=True`

4. **Update default passwords**: Change all default user passwords

5. **Configure CORS**: Add trusted domains only

6. **Set up firewalls**: Restrict database access

7. **Enable logging**: Configure production error logging

8. **Regular backups**: Automate database backups

## 📚 User Roles & Permissions

### 👤 **Admin** (System Administrator)

**Access Level**: Full system control

**Key Features**:
- Complete user management (create, edit, delete users)
- Academic year and evaluation period configuration
- Faculty assignment to departments, subjects, and classes
- Manage classes, sections, and subject offerings
- System-wide settings and configuration
- Activity logs monitoring
- Archive management for historical data
- View all analytics and reports

**Typical Workflows**:
1. Set up academic year structure
2. Create evaluation periods (Midterm, Finals)
3. Assign faculty to subjects and classes
4. Monitor evaluation completion rates
5. Archive old data at year end

---

### 🎓 **Student**

**Access Level**: Personal evaluations only

**Key Features**:
- View assigned faculty for evaluation
- Complete faculty evaluations with countdown timer
- Track evaluation completion status and progress
- View evaluation history
- Manage personal profile and account settings
- Access help and support resources
- Guaranteed anonymous evaluation responses

**Typical Workflows**:
1. Log in and view dashboard
2. See list of faculty to evaluate
3. Complete evaluation before deadline
4. Receive email notifications about evaluation periods
5. Track which evaluations are pending/completed

---

### 🧭 **Guidance Counselor**

**Access Level**: Analytics and management

**Key Features**:
- View comprehensive faculty performance analytics
- Access evaluation results and detailed insights
- Create and manage questionnaire templates
- Student and faculty information management
- Evaluation period management
- AI-powered analytics dashboard (Google Gemini integration)
- Generate PDF and Excel reports
- Department and course-level analysis

**Typical Workflows**:
1. Monitor evaluation completion rates
2. Analyze faculty performance trends
3. Generate reports for academic departments
4. Create/update questionnaire templates
5. Use AI insights for data-driven recommendations

---

### Role Comparison Table

| Feature | Admin | Student | Guidance |
|---------|-------|---------|----------|
| User Management | ✅ Full | ❌ | ✅ View |
| Evaluation Periods | ✅ Create/Edit | ❌ | ✅ View/Edit |
| Complete Evaluations | ❌ | ✅ | ❌ |
| View Analytics | ✅ | ❌ | ✅ Advanced |
| Questionnaire Management | ✅ | ❌ | ✅ |
| Generate Reports | ✅ | ❌ | ✅ |
| System Settings | ✅ | ❌ | ❌ |
| Activity Logs | ✅ | ❌ | ❌ |
| Archives | ✅ | ❌ | ✅ View |
| AI Analytics | ❌ | ❌ | ✅ |

## 🌐 API Endpoints

IntellEvalPro provides RESTful API endpoints for data exchange:

### Authentication Routes (`auth_bp`)
```
POST   /login                  # User login
GET    /logout                 # User logout
GET    /signup                 # Student self-registration page
POST   /signup                 # Process student registration
GET    /forgot-password        # Password recovery page
POST   /forgot-password        # Send recovery email
GET    /reset-password/<token> # Password reset page
POST   /reset-password/<token> # Update password
```

### Admin Routes (`admin_bp`)
```
GET    /admin/admin-dashboard           # Admin main dashboard
GET    /admin/user-management           # User CRUD operations
GET    /admin/evaluation-periods        # Evaluation period management
GET    /admin/faculty-list              # Faculty management
GET    /admin/student-list              # Student management
GET    /admin/academic-years            # Academic year configuration
GET    /admin/classes                   # Class management
GET    /admin/sections                  # Section management
GET    /admin/subjects                  # Subject management
GET    /admin/activity-logs             # System activity monitoring
GET    /admin/archives                  # Historical data management
```

### Student Routes (`student_bp`)
```
GET    /student/student-dashboard       # Student main dashboard
GET    /student/evaluation-form         # Faculty evaluation form
POST   /student/submit-evaluation       # Submit evaluation responses
GET    /student/profile                 # Student profile management
GET    /student/help-support            # Help resources
```

### Guidance Routes (`guidance_bp`)
```
GET    /guidance/guidance-dashboard              # Guidance main dashboard
GET    /guidance/evaluation-results              # View evaluation results
GET    /guidance/questionnaire-management        # Manage questionnaires
GET    /guidance/faculty-management              # Faculty information
GET    /guidance/student-management              # Student information
GET    /guidance/evaluation-periods              # Period management
GET    /guidance/ai-analytics-dashboard          # AI-powered insights
GET    /guidance/help-support                    # Help resources
```

### Analytics Routes (`analytics_bp`)
```
GET    /analytics/dashboard                      # Analytics overview
GET    /analytics/faculty/<id>                   # Faculty-specific analytics
GET    /analytics/department/<id>                # Department analytics
GET    /analytics/export/pdf                     # Export PDF report
GET    /analytics/export/excel                   # Export Excel report
```

### API Data Endpoints (`api_bp`)
```
GET    /api/students                   # Get all students (JSON)
GET    /api/faculty                    # Get all faculty (JSON)
GET    /api/evaluations                # Get evaluation data
GET    /api/evaluation-responses       # Get evaluation responses
GET    /api/analytics/summary          # Analytics summary data
POST   /api/questionnaire/create       # Create new questionnaire
PUT    /api/questionnaire/update/<id>  # Update questionnaire
DELETE /api/questionnaire/delete/<id>  # Delete questionnaire
GET    /api/period-status              # Get evaluation period status
```

### Response Format

All API endpoints return JSON responses:

**Success Response:**
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": { /* result data */ }
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "Error description",
  "error": "Detailed error message"
}
```

### Authentication

API endpoints use session-based authentication with role-based access control via decorators:

```python
@login_required      # Requires any authenticated user
@admin_required      # Requires admin role
@student_required    # Requires student role
@guidance_required   # Requires guidance role
@role_required(['admin', 'guidance'])  # Multiple roles
```

## 📊 Database Schema

IntellEvalPro uses a comprehensive relational database with 30+ tables:

### Core Tables

#### Users & Authentication
- **`users`** - User accounts (user_id, username, password_hash, role, email, etc.)
- **`students`** - Extended student information
- **`faculty`** - Faculty records and department assignments
- **`guidance_counselors`** - Guidance counselor details

#### Academic Structure
- **`colleges`** - College/Department divisions
- **`departments`** - Academic departments
- **`courses`** - Degree programs (BSCS, BSIT, etc.)
- **`academic_years`** - Academic year definitions
- **`year_levels`** - Year level classification (1st, 2nd, 3rd, 4th)
- **`sections`** - Class sections
- **`subjects`** - Subject offerings
- **`classes`** - Class instances (subject + section + faculty)

#### Evaluation System
- **`evaluation_periods`** - Evaluation period definitions (Midterm, Finals)
- **`evaluations`** - Individual evaluation records
- **`evaluation_responses`** - Student responses to questionnaire items
- **`evaluation_comments`** - Text feedback from students
- **`questionnaires`** - Questionnaire templates
- **`questionnaire_items`** - Individual questions/criteria
- **`response_drafts`** - Saved draft responses

#### Faculty Assignments
- **`faculty_assignments`** - Faculty-to-class mappings
- **`faculty_schedules`** - Faculty teaching schedules

#### System Management
- **`activity_logs`** - System activity tracking
- **`email_logs`** - Email notification history
- **`system_settings`** - Application configuration

### Key Relationships

```
users (1) ──→ (N) students
users (1) ──→ (N) faculty
users (1) ──→ (N) guidance_counselors

faculty (1) ──→ (N) faculty_assignments
subjects (1) ──→ (N) classes
sections (1) ──→ (N) classes
faculty (1) ──→ (N) classes

evaluation_periods (1) ──→ (N) evaluations
students (1) ──→ (N) evaluations
faculty (1) ──→ (N) evaluations

evaluations (1) ──→ (N) evaluation_responses
questionnaire_items (1) ──→ (N) evaluation_responses

evaluations (1) ──→ (1) evaluation_comments
```

### Database Features

- **Foreign Key Constraints**: Referential integrity maintained
- **Indexes**: Optimized for common queries
- **Default Values**: Sensible defaults for all fields
- **Timestamps**: Created/updated tracking on key tables
- **Cascade Deletes**: Proper cleanup of related records
- **Check Constraints**: Data validation at database level

### Sample Queries

**Get all evaluations for a student:**
```sql
SELECT e.*, f.first_name, f.last_name, s.subject_name
FROM evaluations e
JOIN faculty f ON e.faculty_id = f.faculty_id
JOIN classes c ON e.class_id = c.class_id
JOIN subjects s ON c.subject_id = s.subject_id
WHERE e.student_id = ?
```

**Calculate faculty average rating:**
```sql
SELECT f.faculty_id, AVG(er.rating) as avg_rating
FROM faculty f
JOIN evaluations e ON f.faculty_id = e.faculty_id
JOIN evaluation_responses er ON e.evaluation_id = er.evaluation_id
GROUP BY f.faculty_id
```

### Database Files

- **`intellevalpro_db.sql`** - Main database schema with sample data
- **`intellevalpro_db (19).sql`** - Latest backup version
- **`mysql_compatibility_fix.sql`** - MySQL 8.0+ compatibility patch

See `database/MYSQL_COMPATIBILITY_GUIDE.md` for troubleshooting.

## 🛡️ Security Features

IntellEvalPro implements multiple layers of security:

### Authentication & Authorization
- **Custom Password Hashing**: Secure password storage using `werkzeug.security`
- **Session Management**: HTTP-only cookies with configurable lifetime
- **Role-Based Access Control (RBAC)**: Decorator-based permission system
- **Login Protection**: Failed login attempt tracking
- **Password Recovery**: Secure token-based password reset

### Decorators (from `utils.decorators`)
```python
@login_required           # Requires authenticated user
@admin_required           # Admin role only
@student_required         # Student role only
@guidance_required        # Guidance role only
@role_required(['admin', 'guidance'])  # Multiple roles
```

### Input Validation
- **Form Validation**: Server-side validation for all inputs
- **SQL Injection Prevention**: Parameterized queries with SQLAlchemy
- **XSS Protection**: Automatic escaping in Jinja2 templates
- **File Upload Validation**: Type and size restrictions
- **Email Validation**: RFC-compliant email format checking

### Session Security
```python
SESSION_COOKIE_SECURE = True      # HTTPS only (production)
SESSION_COOKIE_HTTPONLY = True    # JavaScript access blocked
SESSION_COOKIE_SAMESITE = 'Lax'   # CSRF protection
PERMANENT_SESSION_LIFETIME = 3600 # 1-hour timeout
```

### Database Security
- **Prepared Statements**: All queries use parameterized binding
- **Connection Pooling**: Secure connection reuse
- **Least Privilege**: Database user permissions minimized
- **Connection Encryption**: SSL/TLS for production databases

### Password Requirements
- Minimum 8 characters (recommended)
- Mix of letters and numbers encouraged
- Stored as bcrypt hashes (never plain text)
- Default passwords must be changed

### Additional Security Measures
- **CSRF Protection**: Recommended for production (Flask-WTF)
- **Rate Limiting**: Prevent brute force attacks (future enhancement)
- **Activity Logging**: Track all user actions in `activity_logs`
- **Email Verification**: Account activation via email (optional)
- **Two-Factor Authentication**: Planned for future release

### Security Checklist for Production

✅ Change `SECRET_KEY` to random 32+ character string  
✅ Set `DEBUG=False` in production  
✅ Enable `SESSION_COOKIE_SECURE=True` with HTTPS  
✅ Change all default passwords  
✅ Use strong database password  
✅ Enable firewall rules for database  
✅ Regular security updates for dependencies  
✅ Implement CSRF protection (Flask-WTF)  
✅ Set up SSL/TLS certificates  
✅ Configure CORS properly  
✅ Enable rate limiting  
✅ Regular database backups  
✅ Monitor activity logs  
✅ Disable directory listing  
✅ Remove debug endpoints  

### Reporting Security Issues

If you discover a security vulnerability, please email: security@norzagaraycollege.edu.ph

Do not open public GitHub issues for security concerns.

## 📱 Browser & Device Support

### Desktop Browsers
| Browser | Minimum Version | Recommended | Status |
|---------|----------------|-------------|--------|
| Chrome | 80+ | 120+ | ✅ Fully Supported |
| Firefox | 75+ | 115+ | ✅ Fully Supported |
| Safari | 13+ | 17+ | ✅ Fully Supported |
| Edge | 80+ | 120+ | ✅ Fully Supported |
| Opera | 70+ | 100+ | ✅ Supported |

### Mobile Browsers
| Browser | Minimum Version | Status |
|---------|----------------|--------|
| iOS Safari | 12+ | ✅ Fully Supported |
| Chrome Mobile | 80+ | ✅ Fully Supported |
| Firefox Mobile | 75+ | ✅ Fully Supported |
| Samsung Internet | 12+ | ✅ Supported |

### Tested Devices
- **iPhone**: 12, 13, 14, 15 series (390×844 baseline)
- **iPad**: Air, Pro (768×1024, 1024×1366)
- **Android**: Samsung Galaxy S21+, Google Pixel 6+
- **Tablets**: Android tablets (800×1280+)
- **Laptops**: 1024×768 to 1920×1080
- **Desktop**: 1440×900 to 2560×1440

### Features Required
- JavaScript enabled
- Cookies enabled
- Modern CSS3 support (Flexbox, Grid)
- ES6+ JavaScript support
- LocalStorage support
- Fetch API support

### Responsive Breakpoints
```css
/* Mobile (default) */
@media (min-width: 390px) { /* Mobile portrait */ }

/* Large Mobile / Small Tablet */
@media (min-width: 640px) { /* sm: */ }

/* Tablet */
@media (min-width: 768px) { /* md: */ }

/* Laptop */
@media (min-width: 1024px) { /* lg: */ }

/* Desktop */
@media (min-width: 1280px) { /* xl: */ }

/* Large Desktop */
@media (min-width: 1536px) { /* 2xl: */ }
```

## 🔄 Development Workflow

### Setting Up Development Environment

1. **Fork and Clone Repository**
   ```cmd
   git clone https://github.com/Eyrondev/IntellEvalPro.git
   cd IntellEvalPro
   ```

2. **Create Feature Branch**
   ```cmd
   git checkout -b feature/your-feature-name
   ```

3. **Set Up Virtual Environment**
   ```cmd
   python -m venv env
   env\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```cmd
   copy .env.example .env
   # Edit .env with your local settings
   ```

5. **Run Development Server**
   ```cmd
   python app.py
   ```

### Adding New Features

#### 1. Create New Route/Page

**Step 1**: Add route in appropriate blueprint (`routes/blueprint_name.py`)
```python
from flask import render_template
from utils.decorators import role_required

@blueprint_bp.route('/new-feature')
@role_required(['admin', 'guidance'])
def new_feature():
    return render_template('role/new-feature.html')
```

**Step 2**: Create template (`templates/role/new-feature.html`)
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>New Feature | IntellEvalPro</title>
  <link rel="icon" type="image/png" href="{{ url_for('static', filename='images/nclogo.png') }}">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
  <!-- Content -->
  <script src="{{ url_for('static', filename='js/role-navigation.js') }}"></script>
  <script>loadRoleNavigation('new-feature');</script>
</body>
</html>
```

**Step 3**: Update navigation (`templates/role/components/navigation.html`)
```html
<a href="{{ url_for('blueprint.new_feature') }}" 
   class="nav-link" 
   data-page="new-feature">
  <i class="fas fa-icon"></i>
  <span>New Feature</span>
</a>
```

**Step 4**: Update navigation script (`static/js/role-navigation.js`)
```javascript
const pageMap = {
  'new-feature': '/blueprint/new-feature',
  // ... other pages
};
```

#### 2. Create New API Endpoint

Add to `routes/api.py`:
```python
@api_bp.route('/api/new-endpoint', methods=['GET', 'POST'])
@login_required
def new_endpoint():
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database error'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        # Your logic here
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
```

#### 3. Add New Database Model

Create in `models/` directory:
```python
from models.database import db

class NewModel(db.Model):
    __tablename__ = 'new_table'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
```

#### 4. Mobile Responsiveness Checklist

When creating new pages:

✅ Include viewport meta tag  
✅ Use Tailwind responsive classes (`md:`, `lg:`, etc.)  
✅ Test at 390px minimum width  
✅ Ensure navigation works on mobile (hamburger menu)  
✅ Make buttons touch-friendly (min 44×44px)  
✅ Stack forms vertically on mobile  
✅ Test tables (add horizontal scroll or transform to cards)  
✅ Verify modals work on mobile  
✅ Check text readability without zooming  
✅ Test on Chrome DevTools device emulation  

### Code Style Guidelines

#### Python (Backend)
- Follow PEP 8 style guide
- Use descriptive variable names
- Add docstrings to functions
- Use type hints where appropriate
- Keep functions focused (single responsibility)

```python
def calculate_faculty_rating(faculty_id: int, period_id: int) -> float:
    """
    Calculate average rating for a faculty member in a specific period.
    
    Args:
        faculty_id: The faculty member's ID
        period_id: The evaluation period ID
        
    Returns:
        Float representing average rating (0.0 to 5.0)
    """
    # Implementation
```

#### HTML/Templates
- Use semantic HTML5 elements
- Follow Tailwind CSS conventions
- Keep templates DRY (use components)
- Add ARIA labels for accessibility
- Use `url_for()` for all links

#### JavaScript
- Use ES6+ features
- Add comments for complex logic
- Use `const` and `let` (avoid `var`)
- Follow jQuery patterns consistently
- Handle errors gracefully

### Testing

#### Manual Testing
```cmd
# Run development server
python app.py

# Test in browser
http://localhost:5000
```

#### Database Testing
```cmd
# Use test database
set DATABASE_URL=mysql+pymysql://root:@localhost:3306/intellevalpro_db_test
python app.py
```

#### Responsive Testing
1. Open Chrome DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Test at breakpoints: 390px, 768px, 1024px, 1440px
4. Test portrait and landscape orientations

### Git Workflow

```cmd
# Make changes and commit
git add .
git commit -m "feat: add new feature description"

# Push to your branch
git push origin feature/your-feature-name

# Create pull request on GitHub
```

### Commit Message Convention

Follow conventional commits format:

- `feat:` - New features
- `fix:` - Bug fixes
- `refactor:` - Code refactoring
- `style:` - UI/formatting changes
- `docs:` - Documentation updates
- `test:` - Adding tests
- `chore:` - Maintenance tasks

Examples:
```
feat: add AI analytics dashboard for guidance counselors
fix: resolve mobile navigation overlay issue on iOS
refactor: optimize database queries in analytics module
style: improve responsive layout for evaluation form
docs: update API endpoint documentation
```

## 🚨 Troubleshooting

### Common Issues & Solutions

#### Database Connection Errors

**Problem**: `Can't connect to MySQL server` or `Access denied`

**Solutions**:
1. Ensure XAMPP MySQL service is running
2. Check database credentials in `.env`:
   ```env
   DATABASE_URL=mysql+pymysql://root:@localhost:3306/intellevalpro_db
   ```
3. Verify database exists:
   ```cmd
   mysql -u root -p -e "SHOW DATABASES;"
   ```
4. Test connection:
   ```cmd
   mysql -u root -p intellevalpro_db -e "SELECT 1;"
   ```

#### MySQL 8.0+ Compatibility Issues

**Problem**: `Authentication plugin 'caching_sha2_password' cannot be loaded`

**Solution**: Run compatibility fix
```cmd
cd database
mysql_compatibility_fix.bat
```

Or manually:
```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '';
FLUSH PRIVILEGES;
```

See `database/MYSQL_COMPATIBILITY_GUIDE.md` for details.

#### Module Import Errors

**Problem**: `ModuleNotFoundError: No module named 'flask'`

**Solutions**:
1. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

2. Activate virtual environment:
   ```cmd
   env\Scripts\activate
   pip install -r requirements.txt
   ```

3. Verify installation:
   ```cmd
   pip list
   ```

#### Email Sending Fails

**Problem**: `SMTPAuthenticationError` or emails not sending

**Solutions**:
1. **Gmail**: Generate App Password (not regular password)
   - Enable 2FA: Google Account → Security → 2-Step Verification
   - Create App Password: Security → App passwords → Select app (Mail) → Generate
   - Use 16-character password in `.env`

2. Check `.env` configuration:
   ```env
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-16-char-app-password
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   ```

3. Test email sending:
   ```python
   from utils.email_utils import send_evaluation_notification
   # Test function
   ```

See `docs/GMAIL_APP_PASSWORD_SETUP.md` for detailed Gmail setup.

#### Port Already in Use

**Problem**: `Address already in use` when running `python app.py`

**Solutions**:
1. Kill process using port 5000:
   ```cmd
   netstat -ano | findstr :5000
   taskkill /PID <process_id> /F
   ```

2. Change port in `.env`:
   ```env
   PORT=5001
   ```

3. Run on different port:
   ```cmd
   set PORT=5001
   python app.py
   ```

#### Session Timeout Issues

**Problem**: Users logged out too quickly

**Solution**: Adjust session lifetime in `config.py`:
```python
PERMANENT_SESSION_LIFETIME = 7200  # 2 hours (3600 = 1 hour)
```

#### Mobile Display Issues

**Problem**: Page not responsive on mobile

**Solutions**:
1. Verify viewport meta tag:
   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1">
   ```

2. Check Tailwind responsive classes:
   ```html
   <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
   ```

3. Clear browser cache (Ctrl+Shift+R)

4. Test in Chrome DevTools responsive mode (F12 → Device Toolbar)

#### Navigation Not Highlighting Active Page

**Problem**: Current page not highlighted in navigation

**Solutions**:
1. Verify page identifier in template:
   ```javascript
   loadRoleNavigation('correct-page-id');
   ```

2. Check `pageMap` in navigation JS:
   ```javascript
   const pageMap = {
     'page-id': '/route/path',
     // ...
   };
   ```

3. Ensure navigation script loads:
   ```html
   <script src="{{ url_for('static', filename='js/role-navigation.js') }}"></script>
   ```

#### Evaluation Timer Not Working

**Problem**: Countdown timer doesn't start or display

**Solutions**:
1. Ensure `evaluation-timer.js` is loaded:
   ```html
   <script src="{{ url_for('static', filename='js/evaluation-timer.js') }}"></script>
   ```

2. Check timer initialization:
   ```javascript
   startEvaluationTimer(timeLimit);
   ```

3. Verify time limit from backend:
   ```python
   return render_template('evaluation-form.html', time_limit=3600)
   ```

#### Static Files Not Loading (404 Errors)

**Problem**: CSS, JS, images return 404 errors

**Solutions**:
1. Check file path in `static/` folder

2. Use `url_for()` for all static files:
   ```html
   <script src="{{ url_for('static', filename='js/script.js') }}"></script>
   <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
   <img src="{{ url_for('static', filename='images/logo.png') }}">
   ```

3. Clear browser cache

4. Restart Flask server

#### Database Schema Mismatch

**Problem**: Column or table doesn't exist errors

**Solutions**:
1. Re-import database:
   ```cmd
   mysql -u root -p intellevalpro_db < database\intellevalpro_db.sql
   ```

2. Check table structure:
   ```sql
   DESCRIBE table_name;
   ```

3. Run compatibility fix if needed

#### Permission Denied Errors

**Problem**: `403 Forbidden` or access denied

**Solutions**:
1. Check user role in session:
   ```python
   print(session.get('role'))
   ```

2. Verify route decorators:
   ```python
   @admin_required  # Correct decorator for admin-only routes
   ```

3. Re-login to refresh session

### Getting Help

If you encounter issues not listed here:

1. **Check Logs**: Look at Flask console output for error details
2. **Browser Console**: Check for JavaScript errors (F12 → Console)
3. **Database Logs**: Check MySQL error logs in XAMPP
4. **Documentation**: Review `docs/` folder for specific guides
5. **GitHub Issues**: Search existing issues or create new one

### Debug Mode

Enable detailed error messages (development only):

```env
DEBUG=True
```

Then restart the server:
```cmd
python app.py
```

**⚠️ Never enable DEBUG in production!**

## � Deployment Guide

### Local Network Deployment

Deploy IntellEvalPro on your local network for institutional use:

#### 1. Prepare Production Environment

```cmd
# Update .env file
DEBUG=False
HOST=0.0.0.0
PORT=5000
SESSION_COOKIE_SECURE=False  # Set True only with HTTPS
```

#### 2. Find Your Local IP Address

```cmd
ipconfig
```

Look for `IPv4 Address` (e.g., `192.168.1.100`)

#### 3. Configure Windows Firewall

Allow incoming connections on port 5000:

```cmd
netsh advfirewall firewall add rule name="IntellEvalPro" dir=in action=allow protocol=TCP localport=5000
```

#### 4. Update APP_URL

Edit `.env`:
```env
APP_URL=http://192.168.1.100:5000  # Your local IP address
```

#### 5. Run the Application

```cmd
python app.py
```

#### 6. Access from Other Devices

On the same network, open browser and navigate to:
```
http://192.168.1.100:5000
```

Replace `192.168.1.100` with your actual IP address.

---

### Cloud Deployment (Production)

For detailed cloud deployment guides, see:

- **AWS Deployment**: See `docs/AWS_DEPLOYMENT_GUIDE.md` (coming soon)
- **Heroku Deployment**: See `docs/HEROKU_DEPLOYMENT_GUIDE.md` (coming soon)
- **DigitalOcean Deployment**: See `docs/DIGITALOCEAN_GUIDE.md` (coming soon)

#### Quick AWS Elastic Beanstalk Deployment

1. Install AWS CLI and EB CLI
2. Configure AWS credentials
3. Initialize EB application:
   ```cmd
   eb init -p python-3.9 intellevalpro
   ```
4. Create environment:
   ```cmd
   eb create intellevalpro-prod
   ```
5. Deploy:
   ```cmd
   eb deploy
   ```

See AWS documentation for detailed production deployment steps.

---

### Production Deployment Checklist

Before deploying to production:

#### Security ✅
- [ ] Change `SECRET_KEY` to random 32+ character string
- [ ] Set `DEBUG=False` in production
- [ ] Enable `SESSION_COOKIE_SECURE=True` with HTTPS
- [ ] Change all default user passwords
- [ ] Use strong database password
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure firewall rules
- [ ] Disable unnecessary ports
- [ ] Set up CORS properly
- [ ] Remove debug endpoints

#### Database ✅
- [ ] Use production database server (not localhost)
- [ ] Enable automated daily backups
- [ ] Set up connection pooling
- [ ] Optimize database indexes
- [ ] Configure max connections
- [ ] Enable SSL for database connections

#### Email ✅
- [ ] Use production SMTP server (AWS SES, SendGrid)
- [ ] Configure proper sender domain
- [ ] Set up DKIM and SPF records
- [ ] Test email delivery
- [ ] Monitor email bounce rates

#### Performance ✅
- [ ] Enable caching where appropriate
- [ ] Optimize static file serving
- [ ] Minify CSS/JavaScript
- [ ] Use CDN for assets (optional)
- [ ] Configure load balancer (if scaling)
- [ ] Set up database query optimization

#### Monitoring ✅
- [ ] Set up error logging (Sentry, CloudWatch)
- [ ] Configure performance monitoring
- [ ] Enable activity logging
- [ ] Set up uptime monitoring (UptimeRobot, Pingdom)
- [ ] Configure alerts for critical errors
- [ ] Monitor server resources (CPU, RAM, disk)

#### Backup & Recovery ✅
- [ ] Automated database backups (daily)
- [ ] Code repository backup
- [ ] Test database restoration process
- [ ] Document disaster recovery plan
- [ ] Store backups in separate location
- [ ] Retention policy defined

---

## �📝 Version History & Changelog

### Version 3.0.0 (October 2025) - Current
**Major Features**:
- ✨ Blueprint architecture refactoring for modular design
- 🤖 AI-powered analytics using Google Gemini API
- 📊 Advanced reporting (PDF/Excel export)
- 📧 Enhanced email notification system
- 🔒 Improved security with custom decorators
- 🗄️ SQLAlchemy ORM integration
- ⏱️ Evaluation countdown timer with auto-submit
- 💾 Draft saving functionality
- 📱 Enhanced mobile responsiveness (390px minimum)
- 🎨 Modern UI refresh with Tailwind CSS 3.x

**Technical Improvements**:
- Separated routes into blueprints (auth, admin, student, guidance, api, analytics)
- Database model layer with SQLAlchemy
- Utility layer for reusable functions
- Configuration management with environment variables
- MySQL 8.0+ compatibility fixes
- Connection pooling optimization
- Custom JSON encoder for Decimal types
- Activity logging system

**New Pages**:
- AI Analytics Dashboard (Guidance)
- Academic Years Management (Admin)
- Archives Management (Admin)
- Activity Logs (Admin)
- Enhanced Help & Support pages

---

### Version 2.0.0 (September 2025)
**Major Features**:
- 👥 Added Guidance Counselor role
- 📊 Analytics and reporting system
- 📱 Complete mobile responsiveness overhaul
- 📧 Automated email notifications
- 📋 Questionnaire management system
- 🎨 UI/UX redesign with Tailwind CSS

**New Features**:
- Role-specific navigation systems
- Evaluation period management
- Faculty performance analytics
- Student progress tracking
- Department-level reporting

---

### Version 1.0.0 (Initial Release)
**Core Features**:
- 🔐 Basic authentication system
- 👤 Admin and Student roles
- 📝 Faculty evaluation functionality
- 🗄️ MySQL database integration
- 📊 Basic dashboard views

---

## 🚀 Upcoming Features (Roadmap)

### Version 3.1.0 (Planned)
- [ ] Two-Factor Authentication (2FA)
- [ ] Email verification for new accounts
- [ ] Password strength meter
- [ ] CSV import for bulk user creation
- [ ] Advanced filtering and search
- [ ] Real-time notifications using WebSockets
- [ ] Dark mode theme
- [ ] Multi-language support (English/Filipino)

### Version 3.2.0 (Planned)
- [ ] Mobile app (React Native)
- [ ] Push notifications
- [ ] Calendar integration
- [ ] SMS notifications
- [ ] Automated report scheduling
- [ ] Faculty self-evaluation module
- [ ] Peer evaluation system

### Version 4.0.0 (Future)
- [ ] Microservices architecture
- [ ] Docker containerization
- [ ] Kubernetes deployment
- [ ] GraphQL API
- [ ] Advanced AI insights (sentiment analysis)
- [ ] Blockchain-based evaluation verification
- [ ] Integration with Learning Management Systems (LMS)

**Want to contribute?** Check out `CONTRIBUTING.md` (coming soon) for guidelines.

## 📄 License

This project is developed for **educational purposes** as part of an academic capstone project.

**Copyright © 2025 IntellEvalPro Development Team**

### Usage Terms
- ✅ Educational use and learning
- ✅ Non-commercial deployment for academic institutions
- ✅ Modification and customization for educational purposes
- ❌ Commercial use without permission
- ❌ Redistribution without attribution

For commercial licensing inquiries, please contact: eyron.dev@gmail.com

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute
- 🐛 Report bugs and issues
- 💡 Suggest new features or improvements
- 📝 Improve documentation
- 🔧 Submit pull requests
- 🎨 Design improvements
- 🌐 Translations

### Contribution Guidelines
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code of Conduct
- Be respectful and inclusive
- Write clean, documented code
- Test your changes thoroughly
- Follow the project's coding standards
- Provide clear PR descriptions

## 🙏 Acknowledgments

### Technologies Used
- **Flask** - Web framework
- **MySQL** - Database management
- **Tailwind CSS** - UI framework
- **Chart.js** - Data visualization
- **Google Gemini** - AI analytics
- **ReportLab** - PDF generation
- **OpenPyXL** - Excel export

### Inspiration & Resources
- Norzagaray College faculty and administration
- Open-source community
- Flask and Python documentation
- Tailwind CSS team

### Special Thanks
- **Norzagaray College** for the opportunity and support
- **Faculty members** who provided valuable feedback
- **Beta testers** who helped refine the system
- **Open-source contributors** whose libraries made this possible

## 🤝 Support & Contact

### Technical Support

**For Bugs and Issues**:
- 🐛 [GitHub Issues](https://github.com/Eyrondev/IntellEvalPro/issues)
- 📧 Email: eyron.dev@gmail.com

**For Feature Requests**:
- 💡 [GitHub Discussions](https://github.com/Eyrondev/IntellEvalPro/discussions)
- 📧 Email: eyron.dev@gmail.com

**For Documentation**:
- 📚 Check `docs/` folder for detailed guides
- 📖 Review `database/QUICK_START.md` for quick setup
- 🔧 See `database/MYSQL_COMPATIBILITY_GUIDE.md` for database issues

### Institutional Contact

**Norzagaray College**
- 🌐 Website: [www.norzagaraycollege.edu.ph](https://www.norzagaraycollege.edu.ph)
- 📧 Email: guidance@norzagaraycollege.edu.ph
- 📍 Address: Norzagaray, Bulacan, Philippines

### Developer

**Eyron (Lead Developer)**
- 💼 GitHub: [@Eyrondev](https://github.com/Eyrondev)
- 📧 Email: eyron.dev@gmail.com
- 🌐 Portfolio: [Coming Soon]

### Community

- 💬 Join our discussions on GitHub
- ⭐ Star the repository if you find it helpful
- 🔔 Watch for updates and new releases
- 📣 Share with others who might benefit

---

<div align="center">

## ⭐ Show Your Support

If you find this project helpful, please consider:
- ⭐ Starring the repository
- 🍴 Forking for your own use
- 📢 Sharing with others
- 💬 Providing feedback

**Made with ❤️ for education and innovation**

---

**IntellEvalPro** - Modernizing Faculty Evaluation with Technology 🎓✨

[![GitHub stars](https://img.shields.io/github/stars/Eyrondev/IntellEvalPro?style=social)](https://github.com/Eyrondev/IntellEvalPro/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Eyrondev/IntellEvalPro?style=social)](https://github.com/Eyrondev/IntellEvalPro/network/members)
[![GitHub issues](https://img.shields.io/github/issues/Eyrondev/IntellEvalPro)](https://github.com/Eyrondev/IntellEvalPro/issues)

**[⬆ Back to Top](#intellevalpro---faculty-evaluation-system)**

</div>
