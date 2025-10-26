# IntellEvalPro - Faculty Evaluation System

> ⚠️ **IMPORTANT**: Use `python app_old.py` to run the application.  
> The modular `app.py` is incomplete. See [WHICH_APP_TO_USE.md](WHICH_APP_TO_USE.md) for details.

A comprehensive, mobile-responsive web application for faculty evaluation and academic performance management built with Flask and MySQL.

## 🌟 Features

### Core Functionality
- **Role-based Access Control**: Admin, Student, and Guidance Counselor roles
- **Faculty Evaluation System**: Complete evaluation workflow management
- **Automated Email Notifications**: Students receive emails when evaluation periods start (includes deadline)
- **Student Dashboard**: Track evaluations, view progress, and manage profile
- **Admin Panel**: User management, evaluation periods, and system settings
- **Guidance Dashboard**: Analytics, questionnaire management, and performance tracking

### Technical Features
- **Mobile-First Responsive Design**: Optimized for all devices (phone, tablet, desktop)
- **Modern UI/UX**: Built with Tailwind CSS and interactive JavaScript
- **Secure Authentication**: Custom password hashing and session management
- **Database Integration**: MySQL with comprehensive academic data model
- **API Endpoints**: RESTful APIs for data exchange

## 📋 Prerequisites

1. **XAMPP 8.2+** - For Apache and MySQL services
2. **Python 3.9+** - Programming language runtime
3. **pip** - Python package manager
4. **Modern Web Browser** - Chrome, Firefox, Safari, or Edge

## 🚀 Quick Start

### 1. Database Setup

1. Start XAMPP control panel and ensure **Apache** and **MySQL** services are running
2. Open phpMyAdmin: http://localhost/phpmyadmin
3. Import the database schema:
   ```sql
   -- In phpMyAdmin: Import > Choose file > database/bscs4a_db.sql > Go
   ```
   
   Or via command line:
   ```cmd
   mysql -u root -p < database\bscs4a_db.sql
   ```

### 2. Python Environment Setup

1. Navigate to project directory:
   ```cmd
   cd path\to\IntellEvalPro
   ```

2. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
   
   Or using virtual environment:
   ```cmd
   env\Scripts\pip.exe install -r requirements.txt
   ```

3. **Configure Email Notifications** (Optional but Recommended):
   
   Create a `.env` file in the project root:
   ```cmd
   copy .env.example .env
   ```
   
   Edit `.env` and add your email credentials:
   ```env
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```
   
   **For Gmail**: Enable 2FA and generate an App Password in Google Account settings.
   
   See [docs/EMAIL_NOTIFICATIONS.md](docs/EMAIL_NOTIFICATIONS.md) for detailed setup.

### 3. Run the Application

1. Start the Flask server:
   ```cmd
   python app_old.py
   ```
   
   Or with virtual environment:
   ```cmd
   env\Scripts\python.exe app_old.py
   ```

2. Open your browser and navigate to: **http://localhost:5000**

## 🔐 Default Login Credentials

| Role | Username | Password | Email |
|------|----------|----------|-------|
| **Admin** | `admin` | `12345` | admin@intellevalpro.com |
| **Student** | `2022-0215` | `12345` | aaronjosephjimenezz@gmail.com |
| **Guidance** | `guidance` | `12345` | guidance@intellevalpro.com |

## 📱 Mobile Responsiveness

The system is fully optimized for mobile devices with:
- **Touch-friendly navigation** with hamburger menu
- **Responsive layouts** that adapt to any screen size
- **Mobile-optimized forms** and interactions
- **Performance optimizations** for smooth mobile experience

## � Email Notification System

The system includes automated email notifications to keep students informed:

### Features
- **Automatic notifications** when evaluation periods become Active
- **Personalized emails** with student name and period details
- **Deadline prominently displayed** to encourage timely completion
- **Professional HTML templates** with Norzagaray College branding
- **Mobile-responsive** email design

### When Notifications Are Sent
1. **Immediate**: When creating a period with today's start date
2. **Scheduled**: When "Upcoming" periods automatically become "Active"

### Email Content Includes
- Student's personalized greeting
- Evaluation period title
- Start date and **deadline (end date)**
- Direct link to evaluation dashboard
- Anonymous evaluation reminder

### Setup Requirements
Configure email settings in `.env` file:
```env
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

For detailed setup instructions, see [docs/EMAIL_NOTIFICATIONS.md](docs/EMAIL_NOTIFICATIONS.md)

## �🛠️ Project Structure

```
IntellEvalPro/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── database/             # SQL schema and seed data
│   └── bscs4a_db.sql    # Main database file
├── assets/               # Static assets
│   ├── css/             # Stylesheets (including mobile-responsive.css)
│   └── images/          # Images and logos
├── js/                   # JavaScript files
│   ├── mobile-responsive.js
│   ├── navigation.js
│   └── *-navigation.js  # Role-specific navigation
├── admin/                # Admin interface templates
├── student/              # Student interface templates
├── guidance/             # Guidance interface templates
├── env/                  # Python virtual environment
└── *.html               # Authentication pages
```

## 🔧 Configuration

### Database Configuration
Update the database settings in `app.py`:
```python
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Set your MySQL password
    'database': 'IntellEvalPro_db'
}
```

### Security Settings
For production deployment:
1. Change the `secret_key` in `app.py`
2. Update default passwords
3. Configure HTTPS
4. Set up proper error handling

## 📚 User Roles & Permissions

### 👤 **Admin**
- Complete system management
- User account creation and management
- Evaluation period configuration
- System settings and analytics

### 🎓 **Student** 
- View and complete evaluations
- Track evaluation progress
- Manage personal profile
- Access help and support

### 🧭 **Guidance Counselor**
- Faculty performance analytics
- Questionnaire management
- Student feedback oversight
- Evaluation insights and reporting

## 🌐 API Endpoints

### Authentication
- `GET /login` - Login page
- `POST /login` - Process login
- `GET /logout` - Logout user

### User Management
- `GET /create-admin` - Create admin user
- `GET /create-guidance` - Create guidance user

### Dashboards
- `GET /admin/admin-dashboard` - Admin dashboard
- `GET /student/student-dashboard` - Student dashboard
- `GET /guidance/guidance-dashboard` - Guidance dashboard

### API Data
- `GET /api/students` - Student data API
- `GET /api/faculty` - Faculty data API

## 📊 Database Schema

The system uses a comprehensive academic database model with:
- **Users & Authentication**: Role-based user management
- **Academic Structure**: Colleges, departments, courses, sections
- **Faculty Management**: Faculty records and assignments
- **Student Management**: Student information and enrollments
- **Evaluation System**: Periods, evaluations, responses, comments

## 🛡️ Security Features

- **Custom Password Hashing**: Secure password storage
- **Session Management**: Secure user sessions
- **Role-based Access Control**: Proper permission handling
- **CSRF Protection**: (Recommended for production)
- **Input Validation**: Form data sanitization

## 📱 Browser Support

### Desktop
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

### Mobile
- iOS Safari 12+
- Chrome Mobile 80+
- Firefox Mobile 75+
- Samsung Internet 12+

## 🔄 Development

### Adding New Features
1. Update database schema if needed
2. Create/modify templates in appropriate role folders
3. Add routes in `app.py`
4. Update navigation files
5. Test on multiple devices

### Mobile Optimization
- Use existing CSS classes from `mobile-responsive.css`
- Include `mobile-responsive.js` for enhanced functionality
- Follow mobile-first design principles
- Test on various screen sizes

## 🚨 Troubleshooting

### Common Issues

**Database Connection Error**
- Ensure XAMPP MySQL is running
- Check database credentials in `app.py`
- Verify database exists in phpMyAdmin

**Module Import Errors**
- Install requirements: `pip install -r requirements.txt`
- Activate virtual environment if using one

**Mobile Display Issues**
- Clear browser cache
- Ensure viewport meta tag is present
- Check mobile-responsive.css is loaded

## 📝 Version History

- **v2.0** - Added mobile responsiveness and guidance role
- **v1.0** - Initial release with basic functionality

## 📄 License

This project is developed for educational purposes. All rights reserved.

## 🤝 Support

For support and questions:
- Check the troubleshooting section
- Review the database schema
- Ensure all prerequisites are met

---

**IntellEvalPro** - Modernizing Faculty Evaluation with Technology 🎓✨
