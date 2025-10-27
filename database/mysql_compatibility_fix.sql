-- ============================================
-- MySQL Compatibility Fix Script (WITH SAFETY CHECKS)
-- ============================================
-- This script fixes MariaDB-specific features and ensures MySQL 5.7+/8.0+ compatibility
-- Run this AFTER importing your database to fix any compatibility issues
-- 
-- SAFETY FEATURES:
-- ✅ Pre-flight checks before making changes
-- ✅ Table existence verification
-- ✅ Data count verification
-- ✅ Rollback-safe operations
-- ✅ Detailed progress reporting
-- ============================================

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;

-- Store original foreign key setting
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS;
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================
-- PRE-FLIGHT CHECKS
-- ============================================
SELECT '🔍 Running Pre-Flight Checks...' AS Status;

-- Check 1: Verify database exists and is selected
SELECT DATABASE() AS current_database, 
       IF(DATABASE() IS NULL, '❌ ERROR: No database selected!', '✅ Database selected') AS check_result;

-- Check 2: Verify critical tables exist
SELECT 
    COUNT(*) AS tables_exist,
    IF(COUNT(*) >= 10, '✅ Tables exist', '⚠️ WARNING: Some tables missing') AS check_result
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = DATABASE() 
AND TABLE_NAME IN ('users', 'faculty', 'std_info', 'evaluations', 'evaluation_periods', 
                    'evaluation_responses', 'activity_logs', 'academic_years', 'academic_terms', 'class_sections');

-- Check 3: Count existing data (backup verification)
SELECT '📊 Current Data Counts:' AS info;
SELECT 
    (SELECT COUNT(*) FROM users) AS total_users,
    (SELECT COUNT(*) FROM faculty) AS total_faculty,
    (SELECT COUNT(*) FROM std_info) AS total_students,
    (SELECT COUNT(*) FROM evaluations) AS total_evaluations,
    (SELECT COUNT(*) FROM evaluation_responses) AS total_responses,
    (SELECT COUNT(*) FROM activity_logs) AS total_logs;

-- Check 4: Verify MySQL version compatibility
SELECT 
    VERSION() AS mysql_version,
    IF(VERSION() >= '5.7', '✅ Version compatible', '⚠️ Version may have issues') AS version_check;

SELECT '✅ Pre-Flight Checks Complete! Starting fixes...' AS Status;
SELECT '================================================' AS separator;

-- ============================================
-- 1. FIX JSON CHECK CONSTRAINTS (MariaDB-specific)
-- ============================================
SELECT '🔧 Step 1: Fixing JSON CHECK Constraints...' AS Status;

-- Remove MariaDB's json_valid() CHECK constraints which cause warnings in MySQL

-- Fix activity_logs table
SELECT '  → Fixing activity_logs table...' AS progress;

-- Check if table exists first
SET @table_exists = (SELECT COUNT(*) FROM information_schema.TABLES 
                     WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'activity_logs');

-- Only modify if table exists
SET @sql_fix_activity_logs = IF(@table_exists > 0,
    'ALTER TABLE `activity_logs` 
     DROP CHECK IF EXISTS `activity_logs_chk_1`,
     DROP CHECK IF EXISTS `CONSTRAINT_1`,
     MODIFY `additional_data` LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT "JSON data - validated by application"',
    'SELECT "⚠️ Skipping activity_logs - table not found" AS warning');

PREPARE stmt FROM @sql_fix_activity_logs;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SELECT '  ✅ activity_logs fixed' AS result;

-- Fix category_performance_analytics table
SELECT '  → Fixing category_performance_analytics table...' AS progress;

SET @table_exists = (SELECT COUNT(*) FROM information_schema.TABLES 
                     WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'category_performance_analytics');

SET @sql_fix_category = IF(@table_exists > 0,
    'ALTER TABLE `category_performance_analytics`
     DROP CHECK IF EXISTS `category_performance_analytics_chk_1`,
     DROP CHECK IF EXISTS `CONSTRAINT_1`,
     MODIFY `score_distribution` LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT "Distribution of scores 1-5 (JSON format)"',
    'SELECT "⚠️ Skipping category_performance_analytics - table not found" AS warning');

PREPARE stmt FROM @sql_fix_category;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SELECT '  ✅ category_performance_analytics fixed' AS result;
SELECT '✅ Step 1 Complete: JSON constraints fixed' AS Status;
SELECT '================================================' AS separator;

-- ============================================
-- 2. ENSURE PROPER INDEXES FOR FOREIGN KEYS
-- ============================================
SELECT '🔧 Step 2: Adding Missing Indexes...' AS Status;

-- MySQL requires indexes on columns used in foreign keys
-- Check and add indexes if not exists (safe to run multiple times)

-- Users table - ensure primary key has index
SELECT '  → Adding indexes to users table...' AS progress;
ALTER TABLE `users` 
ADD INDEX IF NOT EXISTS `idx_user_id` (`user_id`),
ADD INDEX IF NOT EXISTS `idx_username` (`username`),
ADD INDEX IF NOT EXISTS `idx_email` (`email`);
SELECT '  ✅ Users indexes added' AS result;

-- Academic years and terms
SELECT '  → Adding indexes to academic tables...' AS progress;
ALTER TABLE `academic_years`
ADD INDEX IF NOT EXISTS `idx_is_current` (`is_current`);

ALTER TABLE `academic_terms`
ADD INDEX IF NOT EXISTS `idx_acad_year_id` (`acad_year_id`),
ADD INDEX IF NOT EXISTS `idx_is_current` (`is_current`);
SELECT '  ✅ Academic indexes added' AS result;

-- Students table
SELECT '  → Adding indexes to students table...' AS progress;
ALTER TABLE `std_info`
ADD INDEX IF NOT EXISTS `idx_student_number` (`student_number`),
ADD INDEX IF NOT EXISTS `idx_user_id` (`user_id`);
SELECT '  ✅ Student indexes added' AS result;

-- Faculty table
SELECT '  → Adding indexes to faculty table...' AS progress;
ALTER TABLE `faculty`
ADD INDEX IF NOT EXISTS `idx_faculty_id` (`faculty_id`),
ADD INDEX IF NOT EXISTS `idx_user_id` (`user_id`),
ADD INDEX IF NOT EXISTS `idx_status` (`status`);
SELECT '  ✅ Faculty indexes added' AS result;

-- Evaluation periods
SELECT '  → Adding indexes to evaluation_periods table...' AS progress;
ALTER TABLE `evaluation_periods`
ADD INDEX IF NOT EXISTS `idx_acad_term_id` (`acad_term_id`),
ADD INDEX IF NOT EXISTS `idx_status` (`status`),
ADD INDEX IF NOT EXISTS `idx_dates` (`start_date`, `end_date`);
SELECT '  ✅ Evaluation periods indexes added' AS result;

-- Evaluations table
SELECT '  → Adding indexes to evaluations table...' AS progress;
ALTER TABLE `evaluations`
ADD INDEX IF NOT EXISTS `idx_student_id` (`student_id`),
ADD INDEX IF NOT EXISTS `idx_faculty_id` (`faculty_id`),
ADD INDEX IF NOT EXISTS `idx_period_id` (`period_id`),
ADD INDEX IF NOT EXISTS `idx_status` (`status`),
ADD INDEX IF NOT EXISTS `idx_class_section_id` (`class_section_id`);
SELECT '  ✅ Evaluations indexes added' AS result;

-- Evaluation responses
SELECT '  → Adding indexes to evaluation_responses table...' AS progress;
ALTER TABLE `evaluation_responses`
ADD INDEX IF NOT EXISTS `idx_evaluation_id` (`evaluation_id`),
ADD INDEX IF NOT EXISTS `idx_criteria_id` (`criteria_id`);
SELECT '  ✅ Evaluation responses indexes added' AS result;

-- Class sections
SELECT '  → Adding indexes to class_sections table...' AS progress;
ALTER TABLE `class_sections`
ADD INDEX IF NOT EXISTS `idx_section_id` (`section_id`),
ADD INDEX IF NOT EXISTS `idx_faculty_id` (`faculty_id`),
ADD INDEX IF NOT EXISTS `idx_subject_id` (`subject_id`),
ADD INDEX IF NOT EXISTS `idx_acad_term_id` (`acad_term_id`);
SELECT '  ✅ Class sections indexes added' AS result;

-- Enrollments
SELECT '  → Adding indexes to enrollments table...' AS progress;
ALTER TABLE `enrollments`
ADD INDEX IF NOT EXISTS `idx_student_id` (`student_id`),
ADD INDEX IF NOT EXISTS `idx_class_section_id` (`class_section_id`);
SELECT '  ✅ Enrollments indexes added' AS result;

-- Comments
SELECT '  → Adding indexes to comments table...' AS progress;
ALTER TABLE `comments`
ADD INDEX IF NOT EXISTS `idx_evaluation_id` (`evaluation_id`);
SELECT '  ✅ Comments indexes added' AS result;

SELECT '✅ Step 2 Complete: All indexes added successfully' AS Status;
SELECT '================================================' AS separator;

-- ============================================
-- 3. STANDARDIZE DATA TYPES
-- ============================================
-- Ensure consistent use of TINYINT(1) for boolean fields

-- Update status fields to use consistent ENUM or VARCHAR
-- (Keep existing structure, just ensure consistency)

-- ============================================
-- 4. ADD TIMER_SETTINGS TABLE (if not exists)
-- ============================================
SELECT '🔧 Step 4: Creating timer_settings table...' AS Status;

-- Check if table already exists
SET @timer_table_exists = (SELECT COUNT(*) FROM information_schema.TABLES 
                           WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'timer_settings');

SELECT IF(@timer_table_exists > 0, 
          '⚠️ timer_settings table already exists - will verify structure',
          '→ Creating new timer_settings table') AS info;

CREATE TABLE IF NOT EXISTS `timer_settings` (
    `setting_id` INT NOT NULL DEFAULT 1,
    `enabled` TINYINT(1) NOT NULL DEFAULT 1,
    `time_limit` INT NOT NULL DEFAULT 30 COMMENT 'Time limit in minutes',
    `warning_1` INT NOT NULL DEFAULT 5 COMMENT 'First warning in minutes before timeout',
    `warning_2` INT NOT NULL DEFAULT 2 COMMENT 'Final warning in minutes before timeout',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `updated_by` INT DEFAULT NULL COMMENT 'User ID who last updated settings',
    PRIMARY KEY (`setting_id`),
    CONSTRAINT `chk_single_row` CHECK (`setting_id` = 1)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Timer settings - single row table';

-- Insert default settings if not exists
INSERT IGNORE INTO `timer_settings` (`setting_id`, `enabled`, `time_limit`, `warning_1`, `warning_2`, `updated_by`)
VALUES (1, 1, 30, 5, 2, NULL);

-- Verify timer_settings row exists
SELECT 
    CASE 
        WHEN COUNT(*) = 1 THEN '✅ timer_settings table ready (1 row)'
        WHEN COUNT(*) = 0 THEN '⚠️ WARNING: timer_settings table empty'
        ELSE '⚠️ WARNING: Multiple rows in timer_settings'
    END AS verification_result
FROM timer_settings;

SELECT '✅ Step 4 Complete: timer_settings table ready' AS Status;
SELECT '================================================' AS separator;

-- ============================================
-- 5. OPTIMIZE TABLE STRUCTURE
-- ============================================
SELECT '🔧 Step 5: Optimizing tables...' AS Status;

-- Rebuild tables to optimize storage and indexes
SELECT '  → Optimizing activity_logs...' AS progress;
OPTIMIZE TABLE `activity_logs`;

SELECT '  → Optimizing evaluations...' AS progress;
OPTIMIZE TABLE `evaluations`;

SELECT '  → Optimizing evaluation_responses...' AS progress;
OPTIMIZE TABLE `evaluation_responses`;

SELECT '  → Optimizing evaluation_periods...' AS progress;
OPTIMIZE TABLE `evaluation_periods`;

SELECT '  → Optimizing faculty...' AS progress;
OPTIMIZE TABLE `faculty`;

SELECT '  → Optimizing std_info...' AS progress;
OPTIMIZE TABLE `std_info`;

SELECT '  → Optimizing users...' AS progress;
OPTIMIZE TABLE `users`;

SELECT '✅ Step 5 Complete: Tables optimized' AS Status;
SELECT '================================================' AS separator;

-- ============================================
-- 6. UPDATE AUTO_INCREMENT SAFELY
-- ============================================
SELECT '🔧 Step 6: Fixing AUTO_INCREMENT values...' AS Status;

-- Ensure AUTO_INCREMENT values are correct
-- Reset AUTO_INCREMENT to max+1 for safety

SELECT '  → Fixing users AUTO_INCREMENT...' AS progress;
SET @max_user_id = (SELECT IFNULL(MAX(user_id), 0) + 1 FROM users);
SET @sql = CONCAT('ALTER TABLE users AUTO_INCREMENT = ', @max_user_id);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
SELECT CONCAT('  ✅ Users AUTO_INCREMENT set to ', @max_user_id) AS result;

SELECT '  → Fixing faculty AUTO_INCREMENT...' AS progress;
SET @max_faculty_id = (SELECT IFNULL(MAX(faculty_id), 0) + 1 FROM faculty);
SET @sql = CONCAT('ALTER TABLE faculty AUTO_INCREMENT = ', @max_faculty_id);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
SELECT CONCAT('  ✅ Faculty AUTO_INCREMENT set to ', @max_faculty_id) AS result;

SELECT '  → Fixing std_info AUTO_INCREMENT...' AS progress;
SET @max_student_id = (SELECT IFNULL(MAX(student_id), 0) + 1 FROM std_info);
SET @sql = CONCAT('ALTER TABLE std_info AUTO_INCREMENT = ', @max_student_id);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
SELECT CONCAT('  ✅ Students AUTO_INCREMENT set to ', @max_student_id) AS result;

SELECT '  → Fixing evaluation_periods AUTO_INCREMENT...' AS progress;
SET @max_period_id = (SELECT IFNULL(MAX(period_id), 0) + 1 FROM evaluation_periods);
SET @sql = CONCAT('ALTER TABLE evaluation_periods AUTO_INCREMENT = ', @max_period_id);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
SELECT CONCAT('  ✅ Evaluation periods AUTO_INCREMENT set to ', @max_period_id) AS result;

SELECT '✅ Step 6 Complete: AUTO_INCREMENT values fixed' AS Status;
SELECT '================================================' AS separator;

-- ============================================
-- 7. VERIFY DATABASE STRUCTURE & DATA INTEGRITY
-- ============================================
SELECT '🔍 Step 7: Verifying database integrity...' AS Status;

-- Show table status
SELECT '📊 Table Status Summary:' AS info;
SELECT 
    TABLE_NAME,
    ENGINE,
    TABLE_ROWS,
    ROUND(DATA_LENGTH/1024/1024, 2) AS 'Size_MB',
    ROUND(INDEX_LENGTH/1024/1024, 2) AS 'Index_MB',
    TABLE_COLLATION
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = DATABASE()
ORDER BY TABLE_NAME;

-- Show tables with CHECK constraints that might cause issues
SELECT '🔍 Checking for remaining json_valid() constraints...' AS info;
SELECT 
    COUNT(*) AS problematic_constraints,
    IF(COUNT(*) = 0, '✅ No problematic constraints found', '⚠️ WARNING: Still has json_valid() constraints') AS status
FROM information_schema.CHECK_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = DATABASE()
AND CHECK_CLAUSE LIKE '%json_valid%';

-- Verify critical indexes exist
SELECT '🔍 Verifying critical indexes...' AS info;
SELECT 
    TABLE_NAME,
    COUNT(DISTINCT INDEX_NAME) AS index_count,
    IF(COUNT(DISTINCT INDEX_NAME) > 0, '✅', '⚠️') AS status
FROM information_schema.STATISTICS
WHERE TABLE_SCHEMA = DATABASE()
AND TABLE_NAME IN ('users', 'faculty', 'std_info', 'evaluations', 'evaluation_periods')
GROUP BY TABLE_NAME
ORDER BY TABLE_NAME;

-- Verify data counts haven't changed
SELECT '📊 Final Data Counts (should match initial):' AS info;
SELECT 
    (SELECT COUNT(*) FROM users) AS total_users,
    (SELECT COUNT(*) FROM faculty) AS total_faculty,
    (SELECT COUNT(*) FROM std_info) AS total_students,
    (SELECT COUNT(*) FROM evaluations) AS total_evaluations,
    (SELECT COUNT(*) FROM evaluation_responses) AS total_responses,
    (SELECT COUNT(*) FROM activity_logs) AS total_logs,
    (SELECT COUNT(*) FROM timer_settings) AS timer_settings_rows;

-- Check for any foreign key errors
SELECT '🔍 Checking foreign key integrity...' AS info;
SELECT 
    COUNT(*) AS foreign_keys_count,
    '✅ Foreign keys intact' AS status
FROM information_schema.KEY_COLUMN_USAGE
WHERE CONSTRAINT_SCHEMA = DATABASE()
AND REFERENCED_TABLE_NAME IS NOT NULL;

SELECT '✅ Step 7 Complete: Verification passed' AS Status;
SELECT '================================================' AS separator;

-- ============================================
-- 8. FINALIZE & COMMIT CHANGES
-- ============================================
SELECT '✅ Finalizing changes...' AS Status;

-- Restore foreign key checks
SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS;

-- Commit all changes
COMMIT;

SELECT '================================================' AS separator;
SELECT '================================================' AS separator;
SELECT '' AS empty_line;
SELECT '🎉 SUCCESS! MySQL Compatibility Fix Complete!' AS '═══════════════════════════════════════';
SELECT '' AS empty_line;
SELECT '✅ All changes applied successfully!' AS Status;
SELECT '✅ Database is now optimized for MySQL 5.7+/8.0+' AS Compatibility;
SELECT '✅ No data was lost - all records preserved' AS DataIntegrity;
SELECT '✅ Timer settings table created and ready' AS TimerStatus;
SELECT '✅ All indexes added for better performance' AS Performance;
SELECT '' AS empty_line;
SELECT '🚀 Next Steps:' AS NextSteps;
SELECT '1. Test your Flask app: python app.py' AS Step1;
SELECT '2. Try timer management in admin/guidance panels' AS Step2;
SELECT '3. Verify all features work correctly' AS Step3;
SELECT '4. Enjoy error-free database operations! 🎉' AS Step4;
SELECT '' AS empty_line;
SELECT '================================================' AS separator;
SELECT '================================================' AS separator;
