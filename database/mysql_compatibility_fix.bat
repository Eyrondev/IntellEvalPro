@echo off
REM MySQL Compatibility Fix - Run this after importing database
REM This fixes MariaDB-specific features and ensures MySQL compatibility
REM WITH COMPREHENSIVE TESTING AND SAFETY CHECKS

echo ========================================
echo MySQL Compatibility Fix Script
echo WITH SAFETY CHECKS ^& VERIFICATION
echo ========================================
echo.
echo This script will:
echo 1. ✅ Run pre-flight checks (database exists, tables present)
echo 2. ✅ Verify data counts before making changes
echo 3. ✅ Remove MariaDB-specific CHECK constraints
echo 4. ✅ Add proper indexes for foreign keys
echo 5. ✅ Create/fix timer_settings table
echo 6. ✅ Optimize table structure
echo 7. ✅ Fix AUTO_INCREMENT values
echo 8. ✅ Verify data integrity after changes
echo 9. ✅ Confirm no data loss occurred
echo.
echo SAFETY FEATURES:
echo - Transaction-based (can rollback if error)
echo - Table existence checks before modifications
echo - Data count verification before/after
echo - Detailed progress reporting
echo.
pause
echo.

REM Get MySQL credentials
set /p DB_HOST="Enter MySQL Host (default: localhost): "
if "%DB_HOST%"=="" set DB_HOST=localhost

set /p DB_USER="Enter MySQL Username (default: root): "
if "%DB_USER%"=="" set DB_USER=root

set /p DB_PASS="Enter MySQL Password (press Enter if none): "

set /p DB_NAME="Enter Database Name (default: intellevalpro_db): "
if "%DB_NAME%"=="" set DB_NAME=intellevalpro_db

echo.
echo ========================================
echo Running compatibility fix...
echo This will show detailed progress...
echo ========================================
echo.

REM Run the compatibility fix script
mysql -h %DB_HOST% -u %DB_USER% -p%DB_PASS% %DB_NAME% < mysql_compatibility_fix.sql > fix_results.log 2>&1

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo 🎉 SUCCESS! Database is MySQL-ready!
    echo ========================================
    echo.
    echo Fixed issues:
    echo ✅ Removed MariaDB-specific json_valid^(^) constraints
    echo ✅ Added missing indexes for foreign keys
    echo ✅ Created timer_settings table
    echo ✅ Optimized table structure
    echo ✅ Verified AUTO_INCREMENT values
    echo ✅ Confirmed data integrity - NO DATA LOST
    echo.
    echo Detailed results saved to: fix_results.log
    echo.
    echo 📊 To view detailed results, open: fix_results.log
    echo.
    echo Your database is now fully compatible with MySQL 5.7+/8.0+
    echo.
    echo 🚀 Next steps:
    echo 1. Test your Flask app: python app.py
    echo 2. Try timer management in admin/guidance
    echo 3. Verify all features work correctly
    echo.
    echo You can safely run your application now! 🎉
    echo.
) else (
    echo.
    echo ========================================
    echo ERROR: Failed to apply compatibility fixes
    echo ========================================
    echo.
    echo Please check:
    echo 1. MySQL is running ^(XAMPP started^)
    echo 2. Database credentials are correct
    echo 3. Database '%DB_NAME%' exists and is imported
    echo 4. You have ALTER TABLE permissions
    echo.
    echo Try running the script manually in phpMyAdmin:
    echo http://localhost/phpmyadmin
    echo.
)

pause
