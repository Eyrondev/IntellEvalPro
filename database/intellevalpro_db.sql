-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 26, 2025 at 11:06 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `intellevalpro_db`
--
CREATE DATABASE IF NOT EXISTS `intellevalpro_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `intellevalpro_db`;

-- --------------------------------------------------------

--
-- Table structure for table `academic_terms`
--

DROP TABLE IF EXISTS `academic_terms`;
CREATE TABLE `academic_terms` (
  `acad_term_id` int(11) NOT NULL,
  `acad_year_id` int(11) NOT NULL,
  `term_name` varchar(50) NOT NULL COMMENT 'e.g., 1st Semester, 2nd Semester',
  `term_code` varchar(20) NOT NULL COMMENT 'e.g., 1ST_SEM, 2ND_SEM',
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `is_current` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Academic terms/semesters within a year';

--
-- Dumping data for table `academic_terms`
--

INSERT INTO `academic_terms` (`acad_term_id`, `acad_year_id`, `term_name`, `term_code`, `start_date`, `end_date`, `is_current`, `created_at`, `updated_at`) VALUES
(1, 1, '1st Semester', '1ST_SEM', '2025-08-15', '2025-12-15', 1, '2025-10-20 16:43:21', '2025-10-25 15:10:41'),
(2, 1, '2nd Semester', '2ND_SEM', '2026-01-15', '2025-12-15', 0, '2025-10-20 16:43:21', '2025-10-20 16:43:21');

-- --------------------------------------------------------

--
-- Table structure for table `academic_years`
--

DROP TABLE IF EXISTS `academic_years`;
CREATE TABLE `academic_years` (
  `acad_year_id` int(11) NOT NULL,
  `year_code` varchar(20) NOT NULL COMMENT 'e.g., 2025-2026, 2026-2027',
  `year_name` varchar(100) NOT NULL COMMENT 'e.g., Academic Year 2025-2026',
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `is_current` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Academic years (e.g., 2025-2026)';

--
-- Dumping data for table `academic_years`
--

INSERT INTO `academic_years` (`acad_year_id`, `year_code`, `year_name`, `start_date`, `end_date`, `is_current`, `created_at`, `updated_at`) VALUES
(1, '2025-2026', 'Academic Year 2025-2026', '2025-07-15', '2025-11-21', 1, '2025-10-20 16:43:21', '2025-10-26 08:53:54');

-- --------------------------------------------------------

--
-- Table structure for table `activity_logs`
--

DROP TABLE IF EXISTS `activity_logs`;
CREATE TABLE `activity_logs` (
  `log_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `user_name` varchar(255) DEFAULT NULL,
  `user_role` varchar(50) DEFAULT NULL,
  `activity_type` varchar(50) NOT NULL,
  `description` text DEFAULT NULL,
  `reason` text DEFAULT NULL,
  `target_user` varchar(255) DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `additional_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`additional_data`)),
  `timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `activity_logs`
--

INSERT INTO `activity_logs` (`log_id`, `user_id`, `user_name`, `user_role`, `activity_type`, `description`, `reason`, `target_user`, `ip_address`, `user_agent`, `additional_data`, `timestamp`) VALUES
(1, 2, 'Dr. Sarah Brooks', 'guidance', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 12:43:43'),
(2, 1, 'Aurum Pascual', 'admin', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 12:43:48'),
(3, 1, 'admin', 'admin', 'create', 'Created student and user account: 2025-0564', NULL, '2025-0564', '192.168.100.85', NULL, NULL, '2025-10-25 15:03:32'),
(4, 1, 'admin', 'admin', 'create', 'Created student and user account: 2022-322', NULL, '2022-322', '192.168.100.85', NULL, NULL, '2025-10-25 15:07:26'),
(5, 1, 'Aurum Pascual', 'admin', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 15:11:10'),
(6, 2, 'Dr. Sarah Brooks', 'guidance', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 15:11:16'),
(7, 2, 'Dr. Sarah Brooks', 'guidance', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 15:13:34'),
(8, 1, 'Aurum Pascual', 'admin', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 15:13:38'),
(9, 1, 'Aurum Pascual', 'admin', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 15:14:23'),
(10, 2, 'Dr. Sarah Brooks', 'guidance', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 15:14:28'),
(11, 2, 'Dr. Sarah Brooks', 'guidance', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 18:44:58'),
(12, 2, 'Dr. Sarah Brooks', 'guidance', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 19:55:24'),
(13, 1, 'Aurum Pascual', 'admin', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 19:55:29'),
(14, 1, 'Aurum Pascual', 'admin', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 19:55:54'),
(15, 2, 'Dr. Sarah Brooks', 'guidance', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 19:55:58'),
(16, 3, 'Aaron Joseph Jimenez', 'student', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.214', NULL, NULL, '2025-10-25 20:05:00'),
(17, 2, 'Dr. Sarah Brooks', 'guidance', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 20:06:09'),
(18, 1, 'Aurum Pascual', 'admin', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 20:06:14'),
(19, 1, 'Aurum Pascual', 'admin', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 20:06:50'),
(20, 2, 'Dr. Sarah Brooks', 'guidance', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 20:06:57'),
(21, 3, 'Aaron Joseph Jimenez', 'student', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 20:08:52'),
(22, 2, 'Dr. Sarah Brooks', 'guidance', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 20:27:27'),
(23, 1, 'Aurum Pascual', 'admin', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 20:27:31'),
(24, 1, 'Aurum Pascual', 'admin', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 20:27:41'),
(25, 2, 'Dr. Sarah Brooks', 'guidance', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 20:27:46'),
(26, 3, 'Aaron Joseph Jimenez', 'student', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 21:48:43'),
(27, 2, 'Dr. Sarah Brooks', 'guidance', 'login', 'User logged in successfully', NULL, NULL, '127.0.0.1', NULL, NULL, '2025-10-25 21:48:48'),
(28, 2, 'Dr. Sarah Brooks', 'guidance', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 22:11:51'),
(29, 2, 'Dr. Sarah Brooks', 'guidance', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 22:11:56'),
(30, 3, 'Aaron Joseph Jimenez', 'student', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 22:48:53'),
(31, 3, 'Aaron Joseph Jimenez', 'student', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 22:55:05'),
(32, 4, 'Rotcher Cadorna', 'student', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 22:55:15'),
(33, 2, 'Dr. Sarah Brooks', 'guidance', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:08:06'),
(34, 1, 'Aurum Pascual', 'admin', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:08:14'),
(35, 1, 'Aurum Pascual', 'admin', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:11:26'),
(36, 2, 'Dr. Sarah Brooks', 'guidance', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:11:31'),
(37, 2, 'Dr. Sarah Brooks', 'guidance', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:11:50'),
(38, 1, 'Aurum Pascual', 'admin', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:11:56'),
(39, 1, 'Aurum Pascual', 'admin', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:13:51'),
(40, 2, 'Dr. Sarah Brooks', 'guidance', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:13:56'),
(41, 4, 'Rotcher Cadorna', 'student', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:23:03'),
(42, 3, 'Aaron Joseph Jimenez', 'student', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:23:06'),
(43, 2, 'Dr. Sarah Brooks', 'guidance', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:26:07'),
(44, 1, 'Aurum Pascual', 'admin', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:26:12'),
(45, 3, 'Aaron Joseph Jimenez', 'student', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:27:09'),
(46, 1, 'Aurum Pascual', 'admin', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:29:03'),
(47, 3, 'Aaron Joseph Jimenez', 'student', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:29:10'),
(48, 3, 'Aaron Joseph Jimenez', 'student', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:29:21'),
(49, 2, 'Dr. Sarah Brooks', 'guidance', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:29:27'),
(50, 2, 'Dr. Sarah Brooks', 'guidance', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:29:51'),
(51, 2, 'Dr. Sarah Brooks', 'guidance', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:36:48'),
(52, 2, 'Dr. Sarah Brooks', 'guidance', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:36:53'),
(53, 2, 'Dr. Sarah Brooks', 'guidance', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:36:56'),
(54, 2, 'Dr. Sarah Brooks', 'guidance', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:37:06'),
(55, 2, 'Dr. Sarah Brooks', 'guidance', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:37:08'),
(56, 3, 'Aaron Joseph Jimenez', 'student', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:37:13'),
(57, 2, 'Dr. Sarah Brooks', 'guidance', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:44:25'),
(58, 4, 'Rotcher Cadorna', 'student', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:44:31'),
(59, 3, 'Aaron Joseph Jimenez', 'student', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:46:12'),
(60, 2, 'Dr. Sarah Brooks', 'guidance', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:46:19'),
(61, 4, 'Rotcher Cadorna', 'student', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:48:50'),
(62, 1, 'Aurum Pascual', 'admin', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-25 23:49:04'),
(63, 1, 'Aurum Pascual', 'admin', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-26 00:17:58'),
(64, 4, 'Rotcher Cadorna', 'student', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-26 00:18:02'),
(65, 2, 'Dr. Sarah Brooks', 'guidance', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-26 16:33:48'),
(66, 3, 'Aaron Joseph Jimenez', 'student', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-26 16:33:52'),
(67, 3, 'Aaron Joseph Jimenez', 'student', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-26 16:34:22'),
(68, 2, 'Dr. Sarah Brooks', 'guidance', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-26 16:34:28'),
(69, 2, 'Dr. Sarah Brooks', 'guidance', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-26 16:37:02'),
(70, 1, 'Aurum Pascual', 'admin', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-26 16:37:08'),
(71, 1, 'Aurum Pascual', 'admin', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-26 16:39:11'),
(72, 2, 'Dr. Sarah Brooks', 'guidance', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-26 16:39:30'),
(73, 1, 'Aurum Pascual', 'admin', 'logout', 'User logged out', NULL, NULL, '192.168.100.214', NULL, NULL, '2025-10-26 16:46:04'),
(74, 3, 'Aaron Joseph Jimenez', 'student', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.214', NULL, NULL, '2025-10-26 16:46:10'),
(75, 2, 'Dr. Sarah Brooks', 'guidance', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-26 17:11:00'),
(76, 1, 'Aurum Pascual', 'admin', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-26 17:11:04'),
(77, 5, 'Mark Allen Fausto', 'student', 'logout', 'User logged out', NULL, NULL, '192.168.100.119', NULL, NULL, '2025-10-26 17:11:38'),
(78, NULL, 'admin', NULL, 'login', 'Failed login attempt for username: admin', NULL, NULL, '192.168.100.119', NULL, NULL, '2025-10-26 17:11:45'),
(79, 1, 'Aurum Pascual', 'admin', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.119', NULL, NULL, '2025-10-26 17:11:51'),
(80, 1, 'Aurum Pascual', 'admin', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-26 17:17:39'),
(81, 6, 'Daniel Mangahas', 'student', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.222', NULL, NULL, '2025-10-26 17:18:35'),
(82, 59, 'Gabrielle Cruz', 'student', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-26 17:19:38'),
(83, 59, 'Gabrielle Cruz', 'student', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-26 17:20:11'),
(84, 58, 'ED ALLISON  DELOS SANTOS', 'student', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-26 17:20:17'),
(85, 58, 'ED ALLISON  DELOS SANTOS', 'student', 'logout', 'User logged out', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-26 17:21:36'),
(86, 2, 'Dr. Sarah Brooks', 'guidance', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.85', NULL, NULL, '2025-10-26 17:21:40'),
(87, 1, 'Aurum Pascual', 'admin', 'logout', 'User logged out', NULL, NULL, '192.168.100.119', NULL, NULL, '2025-10-26 17:48:59'),
(88, 2, 'Dr. Sarah Brooks', 'guidance', 'login', 'User logged in successfully', NULL, NULL, '192.168.100.119', NULL, NULL, '2025-10-26 17:49:09');

-- --------------------------------------------------------

--
-- Table structure for table `analytics_config`
--

DROP TABLE IF EXISTS `analytics_config`;
CREATE TABLE `analytics_config` (
  `config_id` int(11) NOT NULL,
  `config_key` varchar(100) NOT NULL,
  `config_value` text NOT NULL,
  `description` text DEFAULT NULL,
  `data_type` enum('string','number','boolean','json') NOT NULL DEFAULT 'string',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `category_performance_analytics`
--

DROP TABLE IF EXISTS `category_performance_analytics`;
CREATE TABLE `category_performance_analytics` (
  `category_analytics_id` int(11) NOT NULL,
  `analytics_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `average_score` decimal(3,2) NOT NULL DEFAULT 0.00,
  `total_responses` int(11) NOT NULL DEFAULT 0,
  `score_distribution` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'Distribution of scores 1-5' CHECK (json_valid(`score_distribution`)),
  `performance_level` enum('Excellent','Very Good','Good','Satisfactory','Needs Improvement') DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `class_sections`
--

DROP TABLE IF EXISTS `class_sections`;
CREATE TABLE `class_sections` (
  `section_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `faculty_id` int(11) NOT NULL,
  `acad_term_id` int(11) NOT NULL,
  `section_ref_id` int(11) DEFAULT NULL COMMENT 'Reference to sections table',
  `section_name` varchar(20) NOT NULL,
  `schedule` varchar(100) DEFAULT NULL,
  `room` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `class_sections`
--

INSERT INTO `class_sections` (`section_id`, `subject_id`, `faculty_id`, `acad_term_id`, `section_ref_id`, `section_name`, `schedule`, `room`, `created_at`, `updated_at`) VALUES
(120, 28, 22, 1, 7, 'BSCS-4A', 'TBA', 'TBA', '2025-10-25 05:51:43', '2025-10-25 05:51:43'),
(121, 27, 24, 1, 7, 'BSCS-4A', 'TBA', 'TBA', '2025-10-25 05:51:56', '2025-10-25 05:51:56'),
(122, 26, 23, 1, 7, 'BSCS-4A', 'TBA', 'TBA', '2025-10-25 05:52:07', '2025-10-25 05:52:07'),
(123, 25, 21, 1, 7, 'BSCS-4A', 'TBA', 'TBA', '2025-10-25 05:52:15', '2025-10-25 05:52:15'),
(124, 31, 25, 1, 35, 'BSHM-1D', 'TBA', 'TBA', '2025-10-25 07:04:08', '2025-10-25 07:04:08'),
(125, 29, 26, 1, 35, 'BSHM-1D', 'TBA', 'TBA', '2025-10-25 07:04:24', '2025-10-25 07:04:24'),
(126, 30, 27, 1, 35, 'BSHM-1D', 'TBA', 'TBA', '2025-10-25 07:04:36', '2025-10-25 07:04:36'),
(128, 32, 28, 1, 33, 'BEED-4B', 'TBA', 'TBA', '2025-10-25 07:14:21', '2025-10-25 15:17:10');

-- --------------------------------------------------------

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `comment_id` int(11) NOT NULL,
  `evaluation_id` int(11) NOT NULL,
  `comment_text` text NOT NULL,
  `sentiment` enum('Positive','Neutral','Negative') DEFAULT NULL,
  `is_flagged` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `comments`
--

INSERT INTO `comments` (`comment_id`, `evaluation_id`, `comment_text`, `sentiment`, `is_flagged`, `created_at`, `updated_at`) VALUES
(1, 181, 'trtwafasddasdasda', 'Neutral', 0, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(2, 212, 'all goods', 'Neutral', 0, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(3, 208, 'lala', 'Neutral', 0, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(4, 206, 'lala', 'Neutral', 0, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(5, 216, 'okay naman sya mag turo', 'Neutral', 0, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(6, 200, 'Ang galing din po magturo', 'Neutral', 0, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(7, 213, 'all goods naman', 'Neutral', 0, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(8, 198, 'Ang galing nya', 'Neutral', 0, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(9, 197, 'Okay sya', 'Neutral', 0, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(10, 199, 'Ayos', 'Neutral', 0, '2025-10-26 09:23:28', '2025-10-26 09:23:28');

-- --------------------------------------------------------

--
-- Table structure for table `enrollments`
--

DROP TABLE IF EXISTS `enrollments`;
CREATE TABLE `enrollments` (
  `enrollment_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `section_id` int(11) NOT NULL,
  `enrollment_date` datetime NOT NULL DEFAULT current_timestamp(),
  `status` enum('Enrolled','Dropped','Withdrawn','Completed') NOT NULL DEFAULT 'Enrolled',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `evaluations`
--

DROP TABLE IF EXISTS `evaluations`;
CREATE TABLE `evaluations` (
  `evaluation_id` int(11) NOT NULL,
  `period_id` int(11) NOT NULL,
  `section_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `status` enum('Pending','In Progress','Completed','Expired') NOT NULL DEFAULT 'Pending',
  `is_anonymous` tinyint(1) NOT NULL DEFAULT 1,
  `start_time` datetime DEFAULT NULL,
  `completion_time` datetime DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `evaluations`
--

INSERT INTO `evaluations` (`evaluation_id`, `period_id`, `section_id`, `student_id`, `status`, `is_anonymous`, `start_time`, `completion_time`, `created_at`, `updated_at`) VALUES
(193, 12, 120, 2, 'Pending', 1, NULL, NULL, '2025-10-26 08:42:00', '2025-10-26 08:42:00'),
(194, 12, 121, 2, 'Pending', 1, NULL, NULL, '2025-10-26 08:42:00', '2025-10-26 08:42:00'),
(195, 12, 122, 2, 'Pending', 1, NULL, NULL, '2025-10-26 08:42:00', '2025-10-26 08:42:00'),
(196, 12, 123, 2, 'Pending', 1, NULL, NULL, '2025-10-26 08:42:00', '2025-10-26 08:42:00'),
(197, 12, 120, 4, 'Completed', 1, '2025-10-26 17:22:14', '2025-10-26 17:22:48', '2025-10-26 08:42:00', '2025-10-26 09:22:48'),
(198, 12, 121, 4, 'Completed', 1, '2025-10-26 17:21:32', '2025-10-26 17:22:08', '2025-10-26 08:42:00', '2025-10-26 09:22:08'),
(199, 12, 122, 4, 'Completed', 1, '2025-10-26 17:22:55', '2025-10-26 17:23:28', '2025-10-26 08:42:00', '2025-10-26 09:23:28'),
(200, 12, 123, 4, 'Completed', 1, '2025-10-26 17:19:21', '2025-10-26 17:21:07', '2025-10-26 08:42:00', '2025-10-26 09:21:07'),
(201, 12, 120, 5, 'Pending', 1, NULL, NULL, '2025-10-26 08:42:00', '2025-10-26 08:42:00'),
(202, 12, 121, 5, 'Pending', 1, NULL, NULL, '2025-10-26 08:42:00', '2025-10-26 08:42:00'),
(203, 12, 122, 5, 'Pending', 1, NULL, NULL, '2025-10-26 08:42:00', '2025-10-26 08:42:00'),
(204, 12, 123, 5, 'Pending', 1, NULL, NULL, '2025-10-26 08:42:00', '2025-10-26 08:42:00'),
(205, 12, 120, 3, 'Completed', 1, '2025-10-26 17:09:12', '2025-10-26 17:10:03', '2025-10-26 08:42:00', '2025-10-26 09:10:03'),
(206, 12, 121, 3, 'Completed', 1, '2025-10-26 17:08:01', '2025-10-26 17:08:44', '2025-10-26 08:42:00', '2025-10-26 09:08:44'),
(207, 12, 122, 3, 'Completed', 1, '2025-10-26 17:10:11', '2025-10-26 17:11:21', '2025-10-26 08:42:00', '2025-10-26 09:11:21'),
(208, 12, 123, 3, 'Completed', 1, '2025-10-26 17:06:59', '2025-10-26 17:07:49', '2025-10-26 08:42:00', '2025-10-26 09:07:49'),
(209, 12, 120, 1, 'Pending', 1, NULL, NULL, '2025-10-26 08:42:00', '2025-10-26 08:42:00'),
(210, 12, 121, 1, 'Pending', 1, NULL, NULL, '2025-10-26 08:42:00', '2025-10-26 08:42:00'),
(211, 12, 122, 1, 'Pending', 1, NULL, NULL, '2025-10-26 08:42:00', '2025-10-26 08:42:00'),
(212, 12, 123, 1, 'Completed', 1, '2025-10-26 16:46:16', '2025-10-26 16:46:38', '2025-10-26 08:42:00', '2025-10-26 08:46:38'),
(213, 12, 124, 6, 'Completed', 1, '2025-10-26 17:20:44', '2025-10-26 17:21:08', '2025-10-26 08:42:00', '2025-10-26 09:21:08'),
(214, 12, 125, 6, 'Completed', 1, '2025-10-26 17:20:21', '2025-10-26 17:20:40', '2025-10-26 08:42:00', '2025-10-26 09:20:40'),
(215, 12, 126, 6, 'Completed', 1, '2025-10-26 17:21:13', '2025-10-26 17:21:32', '2025-10-26 08:42:00', '2025-10-26 09:21:32'),
(216, 12, 128, 7, 'Completed', 1, '2025-10-26 17:19:42', '2025-10-26 17:20:06', '2025-10-26 08:42:00', '2025-10-26 09:20:06'),
(224, 13, 120, 2, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54'),
(225, 13, 121, 2, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54'),
(226, 13, 122, 2, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54'),
(227, 13, 123, 2, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54'),
(228, 13, 120, 4, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54'),
(229, 13, 121, 4, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54'),
(230, 13, 122, 4, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54'),
(231, 13, 123, 4, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54'),
(232, 13, 120, 5, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54'),
(233, 13, 121, 5, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54'),
(234, 13, 122, 5, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54'),
(235, 13, 123, 5, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54'),
(236, 13, 120, 3, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54'),
(237, 13, 121, 3, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54'),
(238, 13, 122, 3, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54'),
(239, 13, 123, 3, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54'),
(240, 13, 120, 1, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54'),
(241, 13, 121, 1, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54'),
(242, 13, 122, 1, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54'),
(243, 13, 123, 1, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54'),
(244, 13, 124, 6, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54'),
(245, 13, 125, 6, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54'),
(246, 13, 126, 6, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54'),
(247, 13, 128, 7, 'Pending', 1, NULL, NULL, '2025-10-26 09:11:54', '2025-10-26 09:11:54');

-- --------------------------------------------------------

--
-- Table structure for table `evaluation_categories`
--

DROP TABLE IF EXISTS `evaluation_categories`;
CREATE TABLE `evaluation_categories` (
  `category_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `weight` decimal(5,2) NOT NULL DEFAULT 1.00,
  `display_order` int(11) NOT NULL DEFAULT 0,
  `is_archived` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `evaluation_categories`
--

INSERT INTO `evaluation_categories` (`category_id`, `name`, `description`, `weight`, `display_order`, `is_archived`, `created_at`, `updated_at`) VALUES
(2, 'Learning Delivery', 'Performance Indicators', 1.00, 1, 0, '2025-10-14 07:45:45', '2025-10-15 11:50:33'),
(4, 'Assessment of Student Learning', 'Performance Indicators', 1.00, 2, 0, '2025-10-15 11:46:14', '2025-10-15 11:52:09'),
(5, 'Student-Teacher Engagement', 'Performance Indicators', 1.00, 0, 0, '2025-10-15 11:53:01', '2025-10-15 11:53:01');

-- --------------------------------------------------------

--
-- Table structure for table `evaluation_criteria`
--

DROP TABLE IF EXISTS `evaluation_criteria`;
CREATE TABLE `evaluation_criteria` (
  `criteria_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `description` text NOT NULL,
  `order` int(11) NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `evaluation_criteria`
--

INSERT INTO `evaluation_criteria` (`criteria_id`, `category_id`, `description`, `order`, `created_at`, `updated_at`) VALUES
(30, 2, 'Integrates vision, mission, goals, objectives and core values of the school in the learning activities. (Naiuugnay ang vision, mission, goals, objectives, at core values ng paaralan sa mga gawaing pagkatuto)', 1, '2025-10-14 07:45:50', '2025-10-15 11:50:40'),
(32, 4, 'Gives appropriate learning tasks to measure student\'s achievement. (Nagbibigay ng mga gawaing may kinalaman sa asignatura upang sukatin ang kaalaman ng mag-aaral)', 1, '2025-10-15 11:46:21', '2025-10-15 11:52:29'),
(33, 2, 'Uses course content that is up-to-date and relevant to current issues/concern. (Gumagamit ng mga nilalaman ng kurso, napapanahon at may kaugnayan sa kasalukuyang isyu at pangangailangan)', 2, '2025-10-15 11:50:47', '2025-10-15 11:50:47'),
(34, 2, 'Uses the prescribe syllabus. (Gumagamit ng course syllabus sa pagtuturo)', 3, '2025-10-15 11:50:54', '2025-10-15 11:50:54'),
(35, 2, 'States objectives and expected output of the course clearly. (Nabibigay ng malinaw ang mga layunin ng paksang-aralin at dapat matutuhan ng mga mag-aaral pagkatapos ng talakayan)', 4, '2025-10-15 11:51:06', '2025-10-15 11:51:06'),
(36, 2, 'Promotes students\' learning by addressing individual learning differences. (Nagbibigay ng iba\'t-ibang gawain batay sa pagkakaiba-iba ng kaalaman, talento, at hilig ng bawat mag-aaral)', 5, '2025-10-15 11:51:14', '2025-10-15 11:51:14'),
(37, 2, 'Asks questions in learning tasks that make students analyze and think critically. (Nagtatanong habang nagsasagawa ng malayang talakayan na naghihikayat sa mapanuri at kritikal na pag-iisip ng mga mag-aaral)', 6, '2025-10-15 11:51:18', '2025-10-15 11:51:18'),
(38, 2, 'Instructions and directions given in learning tasks were effective and helpful. (Malinaw magbigay ng mga panuto at direksyon ng gawain sa klase', 7, '2025-10-15 11:51:22', '2025-10-15 11:51:22'),
(39, 2, 'Uses the appropriate language in group chat, text messages, and phone calls. (Gumagamit ng mga tamang salita sa pagtuturo at pakikipag-usap sa group chat, text message, at iba pa)', 8, '2025-10-15 11:51:26', '2025-10-15 11:51:26'),
(40, 2, 'Demonstrate high degree of competence in language and grammar. (Naipamamalas ang mataas na antas ng kakayahan sa paggamit ng wika sa paksang-aralin)', 9, '2025-10-15 11:51:30', '2025-10-15 11:51:30'),
(41, 2, 'Answers questions with clarity. (Nagbibigay ng matalino o malinaw na kasagutan sa tanong ng mga mag-aaral)', 10, '2025-10-15 11:51:38', '2025-10-15 11:51:38'),
(42, 2, 'The learning materials and supporting resources were helpful and useful. (Gumagamit ng mga kinakailangang kagamitan na makatutulong sa pagtuturo)', 11, '2025-10-15 11:51:42', '2025-10-15 11:51:42'),
(43, 4, 'Monitors students\' progress through a variety of appropriate evaluation techniques. (Nagbibigay ng iba\'t-ibang gawain (pagsulit, pasalita, presentasyon) upang sukatin ang pagtaas ng kaalaman ng mga mag-aaral)', 2, '2025-10-15 11:52:34', '2025-10-15 11:52:34'),
(44, 4, 'Makes method of evaluation clear and purposeful to students. (Ang mga ibinibigay na gawain ay may malinaw na nilalaman na makatutulong sa lubusang pagkatuto ng mga mag-aaral)', 3, '2025-10-15 11:52:38', '2025-10-15 11:52:38'),
(45, 4, 'Maintains appropriate student records. (Gumagamit ng papel o laptop kung saan inililista ang mga nakuhang iskor sa iba\'t-ibang gawain ng mga mag-aaral)', 4, '2025-10-15 11:52:42', '2025-10-15 11:52:42'),
(46, 4, 'Provides constructive and frequent feedback to students based on his/her performance and informs parents/guardian if necessary. (Nagbibigay ng konstruktibo at madalas na performance feedback patungkol sa pagganap (class standing) ng mga mag-aaral upang lalong mapaunlad ang pag-aaral)', 5, '2025-10-15 11:52:47', '2025-10-15 11:52:47'),
(47, 4, 'Exercise tenancy in giving deadline with submission of learning output. (Nagbibigay ng sapat na panahon bago ipasa ang mga gawain/proyekto sa klase)', 6, '2025-10-15 11:52:51', '2025-10-15 11:52:51'),
(48, 5, 'Establishes clear expectations for study guide and house rule. (Binibigyang pansin ang pagtuturod sa mga patakaran at tuntunin sa klase)', 1, '2025-10-15 11:53:06', '2025-10-15 11:53:06'),
(49, 5, 'Monitors student regularly for feedback and queries. (Nagtatanong sa klase kung may gustong linawin at nais sabihin ng personal)', 2, '2025-10-15 11:53:09', '2025-10-15 11:53:09'),
(50, 5, 'Instills class discipline in accordance with school policies and regulations. (Nagpapakita ng disiplina sa klase alinsunod sa mga patakaran at regulasyon ng paaralan)', 3, '2025-10-15 11:53:13', '2025-10-15 11:53:13'),
(51, 5, 'Pays attention to students\' queries and concerns. (Nakikinig sa mga tanong at mahahalagang mensahe ng mga mag-aaral)', 4, '2025-10-15 11:53:17', '2025-10-15 11:53:17'),
(52, 5, 'Demonstrates fairness and consistency. (Nagpapakita ng pantay-pantay na pagtingin sa lahat ng mga mag-aaral)', 5, '2025-10-15 11:53:21', '2025-10-15 11:53:21'),
(53, 5, 'Provides additional coaching and mentoring beyond class schedules. (Naglalaan ng panahon sa pagtuturo at paggabay sa mga mag-aaral kahit hindi sa oras ng klase)', 6, '2025-10-15 11:53:24', '2025-10-15 11:53:24');

-- --------------------------------------------------------

--
-- Table structure for table `evaluation_drafts`
--

DROP TABLE IF EXISTS `evaluation_drafts`;
CREATE TABLE `evaluation_drafts` (
  `id` int(11) NOT NULL,
  `evaluation_id` int(11) NOT NULL,
  `draft_data` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `evaluation_drafts`
--

INSERT INTO `evaluation_drafts` (`id`, `evaluation_id`, `draft_data`, `created_at`, `updated_at`) VALUES
(2, 181, '{\"evaluation_id\": \"181\", \"section_id\": \"123\", \"period_id\": \"11\", \"criteria_30\": \"4\", \"criteria_33\": \"5\", \"criteria_34\": \"4\", \"criteria_35\": \"5\", \"criteria_36\": \"3\", \"criteria_37\": \"3\", \"criteria_38\": \"3\", \"criteria_39\": \"3\", \"criteria_40\": \"2\", \"criteria_41\": \"2\", \"criteria_42\": \"2\", \"criteria_32\": \"2\", \"criteria_43\": \"2\", \"criteria_44\": \"1\", \"criteria_45\": \"3\", \"criteria_46\": \"2\", \"criteria_47\": \"1\", \"criteria_48\": \"2\", \"criteria_49\": \"3\", \"criteria_50\": \"2\", \"criteria_51\": \"3\", \"criteria_52\": \"2\", \"criteria_53\": \"3\", \"comments\": \"trtwafasddasdasda\"}', '2025-10-26 08:34:19', '2025-10-26 08:34:19');

-- --------------------------------------------------------

--
-- Table structure for table `evaluation_periods`
--

DROP TABLE IF EXISTS `evaluation_periods`;
CREATE TABLE `evaluation_periods` (
  `period_id` int(11) NOT NULL,
  `acad_term_id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `start_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `status` enum('Pending','Active','Closed','Canceled') NOT NULL DEFAULT 'Pending',
  `is_archived` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `time_limit_minutes` int(11) DEFAULT 30 COMMENT 'Time limit for evaluations in minutes (default: 30)'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `evaluation_periods`
--

INSERT INTO `evaluation_periods` (`period_id`, `acad_term_id`, `title`, `start_date`, `end_date`, `status`, `is_archived`, `created_at`, `updated_at`, `time_limit_minutes`) VALUES
(12, 1, '1st Semester Faculty Evaluation', '2025-10-26 00:00:00', '2025-10-28 00:00:00', 'Active', 0, '2025-10-26 08:42:00', '2025-10-26 08:45:02', 30);

-- --------------------------------------------------------

--
-- Table structure for table `evaluation_responses`
--

DROP TABLE IF EXISTS `evaluation_responses`;
CREATE TABLE `evaluation_responses` (
  `response_id` int(11) NOT NULL,
  `evaluation_id` int(11) NOT NULL,
  `criteria_id` int(11) NOT NULL,
  `rating` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `evaluation_responses`
--

INSERT INTO `evaluation_responses` (`response_id`, `evaluation_id`, `criteria_id`, `rating`, `created_at`, `updated_at`) VALUES
(1, 181, 30, 4, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(2, 181, 33, 5, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(3, 181, 34, 4, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(4, 181, 35, 5, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(5, 181, 36, 3, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(6, 181, 37, 3, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(7, 181, 38, 3, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(8, 181, 39, 3, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(9, 181, 40, 2, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(10, 181, 41, 2, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(11, 181, 42, 2, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(12, 181, 32, 2, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(13, 181, 43, 2, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(14, 181, 44, 1, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(15, 181, 45, 3, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(16, 181, 46, 2, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(17, 181, 47, 1, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(18, 181, 48, 2, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(19, 181, 49, 3, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(20, 181, 50, 2, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(21, 181, 51, 3, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(22, 181, 52, 2, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(23, 181, 53, 3, '2025-10-26 08:34:19', '2025-10-26 08:34:19'),
(24, 212, 30, 3, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(25, 212, 33, 4, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(26, 212, 34, 2, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(27, 212, 35, 2, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(28, 212, 36, 2, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(29, 212, 37, 2, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(30, 212, 38, 4, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(31, 212, 39, 4, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(32, 212, 40, 4, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(33, 212, 41, 3, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(34, 212, 42, 4, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(35, 212, 32, 4, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(36, 212, 43, 3, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(37, 212, 44, 4, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(38, 212, 45, 3, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(39, 212, 46, 4, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(40, 212, 47, 3, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(41, 212, 48, 4, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(42, 212, 49, 3, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(43, 212, 50, 4, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(44, 212, 51, 3, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(45, 212, 52, 4, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(46, 212, 53, 3, '2025-10-26 08:46:38', '2025-10-26 08:46:38'),
(47, 208, 30, 5, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(48, 208, 33, 4, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(49, 208, 34, 3, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(50, 208, 35, 1, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(51, 208, 36, 2, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(52, 208, 37, 3, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(53, 208, 38, 2, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(54, 208, 39, 4, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(55, 208, 40, 5, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(56, 208, 41, 5, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(57, 208, 42, 5, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(58, 208, 32, 4, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(59, 208, 43, 3, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(60, 208, 44, 5, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(61, 208, 45, 2, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(62, 208, 46, 1, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(63, 208, 47, 5, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(64, 208, 48, 5, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(65, 208, 49, 4, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(66, 208, 50, 3, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(67, 208, 51, 2, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(68, 208, 52, 1, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(69, 208, 53, 5, '2025-10-26 09:07:49', '2025-10-26 09:07:49'),
(70, 206, 30, 5, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(71, 206, 33, 5, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(72, 206, 34, 4, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(73, 206, 35, 4, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(74, 206, 36, 3, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(75, 206, 37, 3, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(76, 206, 38, 2, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(77, 206, 39, 2, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(78, 206, 40, 1, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(79, 206, 41, 1, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(80, 206, 42, 5, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(81, 206, 32, 1, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(82, 206, 43, 3, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(83, 206, 44, 4, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(84, 206, 45, 3, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(85, 206, 46, 4, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(86, 206, 47, 3, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(87, 206, 48, 5, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(88, 206, 49, 5, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(89, 206, 50, 4, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(90, 206, 51, 1, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(91, 206, 52, 4, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(92, 206, 53, 4, '2025-10-26 09:08:44', '2025-10-26 09:08:44'),
(93, 205, 30, 5, '2025-10-26 09:10:03', '2025-10-26 09:10:03'),
(94, 205, 33, 5, '2025-10-26 09:10:03', '2025-10-26 09:10:03'),
(95, 205, 34, 4, '2025-10-26 09:10:03', '2025-10-26 09:10:03'),
(96, 205, 35, 1, '2025-10-26 09:10:03', '2025-10-26 09:10:03'),
(97, 205, 36, 2, '2025-10-26 09:10:03', '2025-10-26 09:10:03'),
(98, 205, 37, 3, '2025-10-26 09:10:03', '2025-10-26 09:10:03'),
(99, 205, 38, 2, '2025-10-26 09:10:03', '2025-10-26 09:10:03'),
(100, 205, 39, 4, '2025-10-26 09:10:03', '2025-10-26 09:10:03'),
(101, 205, 40, 5, '2025-10-26 09:10:03', '2025-10-26 09:10:03'),
(102, 205, 41, 4, '2025-10-26 09:10:03', '2025-10-26 09:10:03'),
(103, 205, 42, 5, '2025-10-26 09:10:03', '2025-10-26 09:10:03'),
(104, 205, 32, 5, '2025-10-26 09:10:03', '2025-10-26 09:10:03'),
(105, 205, 43, 5, '2025-10-26 09:10:03', '2025-10-26 09:10:03'),
(106, 205, 44, 4, '2025-10-26 09:10:03', '2025-10-26 09:10:03'),
(107, 205, 45, 2, '2025-10-26 09:10:03', '2025-10-26 09:10:03'),
(108, 205, 46, 3, '2025-10-26 09:10:03', '2025-10-26 09:10:03'),
(109, 205, 47, 1, '2025-10-26 09:10:03', '2025-10-26 09:10:03'),
(110, 205, 48, 5, '2025-10-26 09:10:03', '2025-10-26 09:10:03'),
(111, 205, 49, 4, '2025-10-26 09:10:03', '2025-10-26 09:10:03'),
(112, 205, 50, 2, '2025-10-26 09:10:03', '2025-10-26 09:10:03'),
(113, 205, 51, 3, '2025-10-26 09:10:03', '2025-10-26 09:10:03'),
(114, 205, 52, 2, '2025-10-26 09:10:03', '2025-10-26 09:10:03'),
(115, 205, 53, 2, '2025-10-26 09:10:03', '2025-10-26 09:10:03'),
(116, 207, 30, 5, '2025-10-26 09:11:21', '2025-10-26 09:11:21'),
(117, 207, 33, 1, '2025-10-26 09:11:21', '2025-10-26 09:11:21'),
(118, 207, 34, 1, '2025-10-26 09:11:21', '2025-10-26 09:11:21'),
(119, 207, 35, 3, '2025-10-26 09:11:21', '2025-10-26 09:11:21'),
(120, 207, 36, 4, '2025-10-26 09:11:21', '2025-10-26 09:11:21'),
(121, 207, 37, 2, '2025-10-26 09:11:21', '2025-10-26 09:11:21'),
(122, 207, 38, 1, '2025-10-26 09:11:21', '2025-10-26 09:11:21'),
(123, 207, 39, 5, '2025-10-26 09:11:21', '2025-10-26 09:11:21'),
(124, 207, 40, 4, '2025-10-26 09:11:21', '2025-10-26 09:11:21'),
(125, 207, 41, 5, '2025-10-26 09:11:21', '2025-10-26 09:11:21'),
(126, 207, 42, 4, '2025-10-26 09:11:21', '2025-10-26 09:11:21'),
(127, 207, 32, 4, '2025-10-26 09:11:21', '2025-10-26 09:11:21'),
(128, 207, 43, 5, '2025-10-26 09:11:21', '2025-10-26 09:11:21'),
(129, 207, 44, 3, '2025-10-26 09:11:21', '2025-10-26 09:11:21'),
(130, 207, 45, 4, '2025-10-26 09:11:21', '2025-10-26 09:11:21'),
(131, 207, 46, 2, '2025-10-26 09:11:21', '2025-10-26 09:11:21'),
(132, 207, 47, 5, '2025-10-26 09:11:21', '2025-10-26 09:11:21'),
(133, 207, 48, 5, '2025-10-26 09:11:21', '2025-10-26 09:11:21'),
(134, 207, 49, 5, '2025-10-26 09:11:21', '2025-10-26 09:11:21'),
(135, 207, 50, 4, '2025-10-26 09:11:21', '2025-10-26 09:11:21'),
(136, 207, 51, 3, '2025-10-26 09:11:21', '2025-10-26 09:11:21'),
(137, 207, 52, 4, '2025-10-26 09:11:21', '2025-10-26 09:11:21'),
(138, 207, 53, 3, '2025-10-26 09:11:21', '2025-10-26 09:11:21'),
(139, 216, 30, 4, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(140, 216, 33, 4, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(141, 216, 34, 3, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(142, 216, 35, 2, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(143, 216, 36, 3, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(144, 216, 37, 3, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(145, 216, 38, 2, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(146, 216, 39, 3, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(147, 216, 40, 2, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(148, 216, 41, 3, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(149, 216, 42, 2, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(150, 216, 32, 3, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(151, 216, 43, 4, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(152, 216, 44, 3, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(153, 216, 45, 3, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(154, 216, 46, 3, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(155, 216, 47, 4, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(156, 216, 48, 3, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(157, 216, 49, 4, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(158, 216, 50, 3, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(159, 216, 51, 4, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(160, 216, 52, 3, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(161, 216, 53, 4, '2025-10-26 09:20:06', '2025-10-26 09:20:06'),
(162, 214, 30, 3, '2025-10-26 09:20:40', '2025-10-26 09:20:40'),
(163, 214, 33, 4, '2025-10-26 09:20:40', '2025-10-26 09:20:40'),
(164, 214, 34, 3, '2025-10-26 09:20:40', '2025-10-26 09:20:40'),
(165, 214, 35, 4, '2025-10-26 09:20:40', '2025-10-26 09:20:40'),
(166, 214, 36, 3, '2025-10-26 09:20:40', '2025-10-26 09:20:40'),
(167, 214, 37, 4, '2025-10-26 09:20:40', '2025-10-26 09:20:40'),
(168, 214, 38, 3, '2025-10-26 09:20:40', '2025-10-26 09:20:40'),
(169, 214, 39, 4, '2025-10-26 09:20:40', '2025-10-26 09:20:40'),
(170, 214, 40, 3, '2025-10-26 09:20:40', '2025-10-26 09:20:40'),
(171, 214, 41, 4, '2025-10-26 09:20:40', '2025-10-26 09:20:40'),
(172, 214, 42, 4, '2025-10-26 09:20:40', '2025-10-26 09:20:40'),
(173, 214, 32, 4, '2025-10-26 09:20:40', '2025-10-26 09:20:40'),
(174, 214, 43, 3, '2025-10-26 09:20:40', '2025-10-26 09:20:40'),
(175, 214, 44, 4, '2025-10-26 09:20:40', '2025-10-26 09:20:40'),
(176, 214, 45, 3, '2025-10-26 09:20:40', '2025-10-26 09:20:40'),
(177, 214, 46, 4, '2025-10-26 09:20:40', '2025-10-26 09:20:40'),
(178, 214, 47, 3, '2025-10-26 09:20:40', '2025-10-26 09:20:40'),
(179, 214, 48, 4, '2025-10-26 09:20:40', '2025-10-26 09:20:40'),
(180, 214, 49, 3, '2025-10-26 09:20:40', '2025-10-26 09:20:40'),
(181, 214, 50, 4, '2025-10-26 09:20:40', '2025-10-26 09:20:40'),
(182, 214, 51, 3, '2025-10-26 09:20:40', '2025-10-26 09:20:40'),
(183, 214, 52, 4, '2025-10-26 09:20:40', '2025-10-26 09:20:40'),
(184, 214, 53, 3, '2025-10-26 09:20:40', '2025-10-26 09:20:40'),
(185, 200, 30, 3, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(186, 200, 33, 4, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(187, 200, 34, 3, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(188, 200, 35, 3, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(189, 200, 36, 4, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(190, 200, 37, 3, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(191, 200, 38, 5, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(192, 200, 39, 3, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(193, 200, 40, 5, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(194, 200, 41, 3, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(195, 200, 42, 4, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(196, 200, 32, 4, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(197, 200, 43, 3, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(198, 200, 44, 5, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(199, 200, 45, 3, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(200, 200, 46, 5, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(201, 200, 47, 3, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(202, 200, 48, 4, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(203, 200, 49, 4, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(204, 200, 50, 5, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(205, 200, 51, 3, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(206, 200, 52, 4, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(207, 200, 53, 3, '2025-10-26 09:21:07', '2025-10-26 09:21:07'),
(208, 213, 30, 4, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(209, 213, 33, 4, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(210, 213, 34, 3, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(211, 213, 35, 4, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(212, 213, 36, 5, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(213, 213, 37, 3, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(214, 213, 38, 4, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(215, 213, 39, 3, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(216, 213, 40, 4, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(217, 213, 41, 3, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(218, 213, 42, 4, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(219, 213, 32, 3, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(220, 213, 43, 4, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(221, 213, 44, 3, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(222, 213, 45, 4, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(223, 213, 46, 3, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(224, 213, 47, 4, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(225, 213, 48, 3, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(226, 213, 49, 4, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(227, 213, 50, 3, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(228, 213, 51, 4, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(229, 213, 52, 3, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(230, 213, 53, 4, '2025-10-26 09:21:08', '2025-10-26 09:21:08'),
(231, 215, 30, 1, '2025-10-26 09:21:32', '2025-10-26 09:21:32'),
(232, 215, 33, 2, '2025-10-26 09:21:32', '2025-10-26 09:21:32'),
(233, 215, 34, 2, '2025-10-26 09:21:32', '2025-10-26 09:21:32'),
(234, 215, 35, 3, '2025-10-26 09:21:32', '2025-10-26 09:21:32'),
(235, 215, 36, 2, '2025-10-26 09:21:32', '2025-10-26 09:21:32'),
(236, 215, 37, 2, '2025-10-26 09:21:32', '2025-10-26 09:21:32'),
(237, 215, 38, 2, '2025-10-26 09:21:32', '2025-10-26 09:21:32'),
(238, 215, 39, 2, '2025-10-26 09:21:32', '2025-10-26 09:21:32'),
(239, 215, 40, 3, '2025-10-26 09:21:32', '2025-10-26 09:21:32'),
(240, 215, 41, 3, '2025-10-26 09:21:32', '2025-10-26 09:21:32'),
(241, 215, 42, 2, '2025-10-26 09:21:32', '2025-10-26 09:21:32'),
(242, 215, 32, 2, '2025-10-26 09:21:32', '2025-10-26 09:21:32'),
(243, 215, 43, 3, '2025-10-26 09:21:32', '2025-10-26 09:21:32'),
(244, 215, 44, 2, '2025-10-26 09:21:32', '2025-10-26 09:21:32'),
(245, 215, 45, 3, '2025-10-26 09:21:32', '2025-10-26 09:21:32'),
(246, 215, 46, 2, '2025-10-26 09:21:32', '2025-10-26 09:21:32'),
(247, 215, 47, 3, '2025-10-26 09:21:32', '2025-10-26 09:21:32'),
(248, 215, 48, 1, '2025-10-26 09:21:32', '2025-10-26 09:21:32'),
(249, 215, 49, 1, '2025-10-26 09:21:32', '2025-10-26 09:21:32'),
(250, 215, 50, 1, '2025-10-26 09:21:32', '2025-10-26 09:21:32'),
(251, 215, 51, 2, '2025-10-26 09:21:32', '2025-10-26 09:21:32'),
(252, 215, 52, 1, '2025-10-26 09:21:32', '2025-10-26 09:21:32'),
(253, 215, 53, 1, '2025-10-26 09:21:32', '2025-10-26 09:21:32'),
(254, 198, 30, 5, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(255, 198, 33, 5, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(256, 198, 34, 5, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(257, 198, 35, 5, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(258, 198, 36, 5, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(259, 198, 37, 5, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(260, 198, 38, 5, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(261, 198, 39, 5, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(262, 198, 40, 5, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(263, 198, 41, 5, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(264, 198, 42, 5, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(265, 198, 32, 5, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(266, 198, 43, 5, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(267, 198, 44, 5, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(268, 198, 45, 5, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(269, 198, 46, 5, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(270, 198, 47, 5, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(271, 198, 48, 5, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(272, 198, 49, 5, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(273, 198, 50, 5, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(274, 198, 51, 5, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(275, 198, 52, 5, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(276, 198, 53, 5, '2025-10-26 09:22:08', '2025-10-26 09:22:08'),
(277, 197, 30, 3, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(278, 197, 33, 4, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(279, 197, 34, 3, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(280, 197, 35, 3, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(281, 197, 36, 3, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(282, 197, 37, 3, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(283, 197, 38, 3, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(284, 197, 39, 3, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(285, 197, 40, 3, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(286, 197, 41, 3, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(287, 197, 42, 3, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(288, 197, 32, 4, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(289, 197, 43, 3, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(290, 197, 44, 3, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(291, 197, 45, 4, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(292, 197, 46, 3, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(293, 197, 47, 3, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(294, 197, 48, 4, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(295, 197, 49, 3, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(296, 197, 50, 3, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(297, 197, 51, 3, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(298, 197, 52, 4, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(299, 197, 53, 3, '2025-10-26 09:22:48', '2025-10-26 09:22:48'),
(300, 199, 30, 3, '2025-10-26 09:23:28', '2025-10-26 09:23:28'),
(301, 199, 33, 3, '2025-10-26 09:23:28', '2025-10-26 09:23:28'),
(302, 199, 34, 3, '2025-10-26 09:23:28', '2025-10-26 09:23:28'),
(303, 199, 35, 3, '2025-10-26 09:23:28', '2025-10-26 09:23:28'),
(304, 199, 36, 3, '2025-10-26 09:23:28', '2025-10-26 09:23:28'),
(305, 199, 37, 3, '2025-10-26 09:23:28', '2025-10-26 09:23:28'),
(306, 199, 38, 3, '2025-10-26 09:23:28', '2025-10-26 09:23:28'),
(307, 199, 39, 3, '2025-10-26 09:23:28', '2025-10-26 09:23:28'),
(308, 199, 40, 3, '2025-10-26 09:23:28', '2025-10-26 09:23:28'),
(309, 199, 41, 3, '2025-10-26 09:23:28', '2025-10-26 09:23:28'),
(310, 199, 42, 3, '2025-10-26 09:23:28', '2025-10-26 09:23:28'),
(311, 199, 32, 3, '2025-10-26 09:23:28', '2025-10-26 09:23:28'),
(312, 199, 43, 3, '2025-10-26 09:23:28', '2025-10-26 09:23:28'),
(313, 199, 44, 3, '2025-10-26 09:23:28', '2025-10-26 09:23:28'),
(314, 199, 45, 3, '2025-10-26 09:23:28', '2025-10-26 09:23:28'),
(315, 199, 46, 3, '2025-10-26 09:23:28', '2025-10-26 09:23:28'),
(316, 199, 47, 3, '2025-10-26 09:23:28', '2025-10-26 09:23:28'),
(317, 199, 48, 3, '2025-10-26 09:23:28', '2025-10-26 09:23:28'),
(318, 199, 49, 3, '2025-10-26 09:23:28', '2025-10-26 09:23:28'),
(319, 199, 50, 3, '2025-10-26 09:23:28', '2025-10-26 09:23:28'),
(320, 199, 51, 3, '2025-10-26 09:23:28', '2025-10-26 09:23:28'),
(321, 199, 52, 3, '2025-10-26 09:23:28', '2025-10-26 09:23:28'),
(322, 199, 53, 3, '2025-10-26 09:23:28', '2025-10-26 09:23:28');

-- --------------------------------------------------------

--
-- Table structure for table `evaluation_timer_sessions`
--

DROP TABLE IF EXISTS `evaluation_timer_sessions`;
CREATE TABLE `evaluation_timer_sessions` (
  `session_id` int(11) NOT NULL,
  `evaluation_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `start_time` datetime NOT NULL DEFAULT current_timestamp(),
  `time_limit_minutes` int(11) NOT NULL DEFAULT 30,
  `end_time` datetime DEFAULT NULL,
  `status` enum('active','completed','expired') DEFAULT 'active',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `evaluation_timer_sessions`
--

INSERT INTO `evaluation_timer_sessions` (`session_id`, `evaluation_id`, `user_id`, `start_time`, `time_limit_minutes`, `end_time`, `status`, `created_at`) VALUES
(6, 165, 4, '2025-10-26 00:18:05', 6, NULL, 'active', '2025-10-25 16:18:05'),
(7, 181, 3, '2025-10-26 16:33:56', 6, NULL, 'active', '2025-10-26 08:33:56'),
(8, 212, 3, '2025-10-26 16:46:17', 6, NULL, 'active', '2025-10-26 08:46:17'),
(9, 208, 5, '2025-10-26 17:07:02', 6, NULL, 'active', '2025-10-26 09:07:02'),
(10, 206, 5, '2025-10-26 17:08:01', 6, NULL, 'active', '2025-10-26 09:08:01'),
(11, 205, 5, '2025-10-26 17:09:12', 6, NULL, 'active', '2025-10-26 09:09:12'),
(12, 207, 5, '2025-10-26 17:10:12', 6, NULL, 'active', '2025-10-26 09:10:12'),
(13, 200, 6, '2025-10-26 17:19:21', 6, NULL, 'active', '2025-10-26 09:19:21'),
(14, 216, 59, '2025-10-26 17:19:42', 6, NULL, 'active', '2025-10-26 09:19:42'),
(15, 214, 58, '2025-10-26 17:20:21', 6, NULL, 'active', '2025-10-26 09:20:21'),
(16, 213, 58, '2025-10-26 17:20:45', 6, NULL, 'active', '2025-10-26 09:20:45'),
(17, 215, 58, '2025-10-26 17:21:14', 6, NULL, 'active', '2025-10-26 09:21:14'),
(18, 198, 6, '2025-10-26 17:21:32', 6, NULL, 'active', '2025-10-26 09:21:32'),
(19, 197, 6, '2025-10-26 17:22:15', 6, NULL, 'active', '2025-10-26 09:22:15'),
(20, 199, 6, '2025-10-26 17:23:00', 6, NULL, 'active', '2025-10-26 09:23:00');

-- --------------------------------------------------------

--
-- Table structure for table `faculty`
--

DROP TABLE IF EXISTS `faculty`;
CREATE TABLE `faculty` (
  `faculty_id` int(11) NOT NULL,
  `program_id` int(11) NOT NULL,
  `faculty_number` varchar(20) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `rank` enum('Professor','Associate Professor','Assistant Professor','Instructor','Lecturer','Adjunct') NOT NULL,
  `status` enum('Active','On Leave','Sabbatical','Retired') NOT NULL DEFAULT 'Active',
  `hire_date` date DEFAULT NULL,
  `specialization` varchar(255) DEFAULT NULL,
  `is_archived` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `faculty`
--

INSERT INTO `faculty` (`faculty_id`, `program_id`, `faculty_number`, `first_name`, `last_name`, `email`, `rank`, `status`, `hire_date`, `specialization`, `is_archived`, `created_at`, `updated_at`) VALUES
(21, 1, 'NC-FAC-01', 'ARMAN', 'BITANCUR', 'NCARMAN@gmail.com', 'Professor', 'Active', NULL, 'N/A', 0, '2025-10-25 05:17:24', '2025-10-25 05:17:24'),
(22, 1, 'NC-FAC-02', 'RICHTER', 'LAPIG', 'NCRICHTER@gmail.com', 'Professor', 'Active', NULL, 'N/A', 0, '2025-10-25 05:17:49', '2025-10-25 05:17:49'),
(23, 1, 'NC-FAC-03', 'ALFEO', 'MENDOZA', 'NCALFEO@gmail.com', 'Professor', 'Active', NULL, 'N/A', 0, '2025-10-25 05:18:29', '2025-10-25 05:18:29'),
(24, 1, 'NC-FAC-04', 'MARK', 'DE GUZMAN', 'NCMARK@gmail.com', 'Professor', 'Active', NULL, 'N/A', 0, '2025-10-25 05:19:12', '2025-10-25 05:19:12'),
(25, 2, 'NC-FAC-05', 'RAMREL', 'ANONUEVO', 'NCRAMREL@gmail.com', 'Professor', 'Active', NULL, 'N/A', 0, '2025-10-25 06:57:00', '2025-10-25 06:57:00'),
(26, 2, 'NC-FAC-06', 'JUAN MIGUEL', 'DELA MERCED', 'NCJUANMIGUEL@gmail.com', 'Professor', 'Active', NULL, 'N/A', 0, '2025-10-25 06:57:25', '2025-10-25 06:57:25'),
(27, 2, 'NC-FAC-07', 'JANE MARIE', 'RODRIGO', 'NCJANEMARIE@gmail.com', 'Professor', 'Active', NULL, 'N/A', 0, '2025-10-25 06:58:03', '2025-10-25 06:58:03'),
(28, 3, 'NC-FAC-08', 'ARCHIELYN', 'SEMANERO', 'NCARCHIELYN@gmail.com', 'Professor', 'Active', NULL, 'N/A', 0, '2025-10-25 07:09:22', '2025-10-25 07:09:22'),
(29, 1, 'NC-FAC-09', 'JERIMY', 'LUMIBAO', 'ncjerimy@gmail.com', 'Professor', 'Active', NULL, 'N/A', 1, '2025-10-26 09:12:28', '2025-10-26 09:17:02');

-- --------------------------------------------------------

--
-- Table structure for table `faculty_performance_analytics`
--

DROP TABLE IF EXISTS `faculty_performance_analytics`;
CREATE TABLE `faculty_performance_analytics` (
  `analytics_id` int(11) NOT NULL,
  `faculty_id` int(11) NOT NULL,
  `period_id` int(11) NOT NULL,
  `total_evaluations` int(11) DEFAULT 0,
  `completed_evaluations` int(11) DEFAULT 0,
  `response_rate` decimal(5,2) DEFAULT 0.00,
  `average_rating` decimal(3,2) DEFAULT 0.00,
  `overall_score` decimal(5,2) DEFAULT 0.00,
  `performance_grade` varchar(50) DEFAULT NULL,
  `trend_direction` enum('improving','stable','declining') DEFAULT 'stable',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `faculty_recommendations`
--

DROP TABLE IF EXISTS `faculty_recommendations`;
CREATE TABLE `faculty_recommendations` (
  `recommendation_id` int(11) NOT NULL,
  `faculty_id` int(11) NOT NULL,
  `counselor_id` int(11) DEFAULT NULL,
  `recommendation_text` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `generated_reports`
--

DROP TABLE IF EXISTS `generated_reports`;
CREATE TABLE `generated_reports` (
  `report_id` int(11) NOT NULL,
  `report_name` varchar(255) NOT NULL,
  `report_type` enum('summary','faculty','department','comparative') NOT NULL DEFAULT 'summary',
  `period_id` int(11) DEFAULT NULL,
  `program_id` int(11) DEFAULT NULL,
  `faculty_id` int(11) DEFAULT NULL COMMENT 'Specific faculty for faculty reports',
  `file_format` enum('pdf','excel','csv','powerpoint') NOT NULL DEFAULT 'pdf',
  `file_path` varchar(500) DEFAULT NULL,
  `file_size` bigint(20) DEFAULT NULL COMMENT 'File size in bytes',
  `download_count` int(11) NOT NULL DEFAULT 0,
  `generated_by` int(11) NOT NULL COMMENT 'User ID who generated the report',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `performance_trends`
--

DROP TABLE IF EXISTS `performance_trends`;
CREATE TABLE `performance_trends` (
  `trend_id` int(11) NOT NULL,
  `faculty_id` int(11) NOT NULL,
  `period_id` int(11) NOT NULL,
  `metric_name` varchar(100) NOT NULL COMMENT 'e.g., overall_score, response_rate, teaching_effectiveness',
  `metric_value` decimal(10,4) NOT NULL,
  `previous_value` decimal(10,4) DEFAULT NULL,
  `change_percentage` decimal(5,2) DEFAULT NULL,
  `trend_direction` enum('Up','Down','Stable') DEFAULT NULL,
  `benchmark_comparison` enum('Above Average','Average','Below Average') DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `programs`
--

DROP TABLE IF EXISTS `programs`;
CREATE TABLE `programs` (
  `program_id` int(11) NOT NULL,
  `program_code` varchar(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `programs`
--

INSERT INTO `programs` (`program_id`, `program_code`, `name`, `description`, `created_at`, `updated_at`) VALUES
(1, 'BSCS', 'Department of Computing Studies', 'Bachelor of Science in Computer Science', '2025-09-12 02:36:01', '2025-10-25 06:24:48'),
(2, 'BSHM', 'Department of Hospitality Management', 'Bachelor of Science in Hospitality Management', '2025-09-12 02:36:01', '2025-10-25 06:24:59'),
(3, 'BEED & BSED', 'Department of Education', 'Bachelor of Elementary Education & Bachelor of Secondary Education', '2025-10-10 02:00:00', '2025-10-25 06:48:06');

-- --------------------------------------------------------

--
-- Table structure for table `response_analytics`
--

DROP TABLE IF EXISTS `response_analytics`;
CREATE TABLE `response_analytics` (
  `response_analytics_id` int(11) NOT NULL,
  `period_id` int(11) NOT NULL,
  `faculty_id` int(11) DEFAULT NULL,
  `subject_id` int(11) DEFAULT NULL,
  `section_id` int(11) DEFAULT NULL,
  `total_students` int(11) NOT NULL DEFAULT 0,
  `total_responses` int(11) NOT NULL DEFAULT 0,
  `response_rate` decimal(5,2) NOT NULL DEFAULT 0.00,
  `completion_rate` decimal(5,2) NOT NULL DEFAULT 0.00,
  `average_completion_time` int(11) DEFAULT NULL COMMENT 'In minutes',
  `on_time_submissions` int(11) NOT NULL DEFAULT 0,
  `late_submissions` int(11) NOT NULL DEFAULT 0,
  `peak_response_hour` int(11) DEFAULT NULL COMMENT 'Hour of day with most responses',
  `response_trend` enum('Increasing','Decreasing','Stable') DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sections`
--

DROP TABLE IF EXISTS `sections`;
CREATE TABLE `sections` (
  `section_id` int(11) NOT NULL,
  `section_code` varchar(50) NOT NULL COMMENT 'e.g., BSCS-4A, BSIT-3B',
  `section_name` varchar(100) NOT NULL COMMENT 'Full section name',
  `program_id` int(11) DEFAULT NULL COMMENT 'Link to programs table',
  `year_level` int(11) DEFAULT NULL COMMENT '1, 2, 3, 4',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `is_disable` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'Flag to disable section (1=disabled, 0=active)'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Section master data (BSCS-4A, BSIT-3B, etc.)';

--
-- Dumping data for table `sections`
--

INSERT INTO `sections` (`section_id`, `section_code`, `section_name`, `program_id`, `year_level`, `created_at`, `updated_at`, `is_disable`) VALUES
(1, 'BSCS-1A', 'Bachelor of Science in Computer Science - 1st Year Section A', 1, 1, '2025-10-10 08:34:42', '2025-10-24 08:58:20', 0),
(2, 'BSCS-1B', 'Bachelor of Science in Computer Science - 1st Year Section B', 1, 1, '2025-10-10 08:34:42', '2025-10-10 08:34:42', 0),
(3, 'BSCS-2A', 'Bachelor of Science in Computer Science - 2nd Year Section A', 1, 2, '2025-10-10 08:34:42', '2025-10-10 08:34:42', 0),
(4, 'BSCS-2B', 'Bachelor of Science in Computer Science - 2nd Year Section B', 1, 2, '2025-10-10 08:34:42', '2025-10-10 08:34:42', 0),
(5, 'BSCS-3A', 'Bachelor of Science in Computer Science - 3rd Year Section A', 1, 3, '2025-10-10 08:34:42', '2025-10-10 08:34:42', 0),
(6, 'BSCS-3B', 'Bachelor of Science in Computer Science - 3rd Year Section B', 1, 3, '2025-10-10 08:34:42', '2025-10-10 08:34:42', 0),
(7, 'BSCS-4A', 'Bachelor of Science in Computer Science - 4th Year Section A', 1, 4, '2025-10-10 08:34:42', '2025-10-10 08:34:42', 0),
(8, 'BSCS-4B', 'Bachelor of Science in Computer Science - 4th Year Section B', 1, 4, '2025-10-10 08:34:42', '2025-10-10 08:34:42', 0),
(9, 'BSHM-1A', 'Bachelor of Science in Hospitality Management - 1st Year Section A', 2, 1, '2025-10-10 08:34:42', '2025-10-10 08:34:42', 0),
(10, 'BSHM-1B', 'Bachelor of Science in Hospitality Management - 1st Year Section B', 2, 1, '2025-10-10 08:34:42', '2025-10-10 08:34:42', 0),
(11, 'BSHM-2A', 'Bachelor of Science in Hospitality Management - 2nd Year Section A', 2, 2, '2025-10-10 08:34:42', '2025-10-10 08:34:42', 0),
(12, 'BSHM-2B', 'Bachelor of Science in Hospitality Management - 2nd Year Section B', 2, 2, '2025-10-10 08:34:42', '2025-10-10 08:34:42', 0),
(13, 'BSHM-3A', 'Bachelor of Science in Hospitality Management - 3rd Year Section A', 2, 3, '2025-10-10 08:34:42', '2025-10-10 08:34:42', 0),
(14, 'BSHM-3B', 'Bachelor of Science in Hospitality Management - 3rd Year Section B', 2, 3, '2025-10-10 08:34:42', '2025-10-10 08:34:42', 0),
(15, 'BSHM-4A', 'Bachelor of Science in Hospitality Management - 4th Year Section A', 2, 4, '2025-10-10 08:34:42', '2025-10-10 08:34:42', 0),
(16, 'BSHM-4B', 'Bachelor of Science in Hospitality Management - 4th Year Section B', 2, 4, '2025-10-10 08:34:42', '2025-10-10 08:34:42', 0),
(17, 'BSCS-1C', 'Bachelor of Science in Computer Science - 1st Year Section C', 1, 1, '2025-10-10 08:51:21', '2025-10-19 03:10:58', 0),
(18, 'BSED-1A', 'Bachelor of Secondary Education Major in Science - 1st Year Section A', 3, 1, '2025-10-19 03:04:49', '2025-10-25 06:48:35', 0),
(19, 'BSED-1B', 'Bachelor of Secondary Education Major in Science - 1st Year Section B', 3, 1, '2025-10-19 03:04:49', '2025-10-25 06:48:40', 0),
(20, 'BSED-2A', 'Bachelor of Secondary Education Major in Science - 2nd Year Section A', 3, 2, '2025-10-19 03:04:49', '2025-10-25 06:48:44', 0),
(21, 'BSED-2B', 'Bachelor of Secondary Education Major in Science - 2nd Year Section B', 3, 2, '2025-10-19 03:04:49', '2025-10-25 06:48:47', 0),
(22, 'BSED-3A', 'Bachelor of Secondary Education Major in Science - 3rd Year Section A', 3, 3, '2025-10-19 03:04:49', '2025-10-25 06:48:49', 0),
(23, 'BSED-3B', 'Bachelor of Secondary Education Major in Science - 3rd Year Section B', 3, 3, '2025-10-19 03:04:49', '2025-10-25 06:48:54', 0),
(24, 'BSED-4A', 'Bachelor of Secondary Education Major in Science - 4th Year Section A', 3, 4, '2025-10-19 03:04:49', '2025-10-25 06:48:56', 0),
(25, 'BSED-4B', 'Bachelor of Secondary Education Major in Science - 4th Year Section B', 3, 4, '2025-10-19 03:04:49', '2025-10-25 06:49:00', 0),
(26, 'BEED-1A', 'Bachelor of Elementary Education - 1st Year Section A', 3, 1, '2025-10-19 03:04:49', '2025-10-19 03:10:28', 0),
(27, 'BEED-1B', 'Bachelor of Elementary Education - 1st Year Section B', 3, 1, '2025-10-19 03:04:49', '2025-10-19 03:10:28', 0),
(28, 'BEED-2A', 'Bachelor of Elementary Education - 2nd Year Section A', 3, 2, '2025-10-19 03:04:49', '2025-10-19 03:10:28', 0),
(29, 'BEED-2B', 'Bachelor of Elementary Education - 2nd Year Section B', 3, 2, '2025-10-19 03:04:49', '2025-10-19 03:10:28', 0),
(30, 'BEED-3A', 'Bachelor of Elementary Education - 3rd Year Section A', 3, 3, '2025-10-19 03:04:49', '2025-10-19 03:10:28', 0),
(31, 'BEED-3B', 'Bachelor of Elementary Education - 3rd Year Section B', 3, 3, '2025-10-19 03:04:49', '2025-10-19 03:10:28', 0),
(32, 'BEED-4A', 'Bachelor of Elementary Education - 4th Year Section A', 3, 4, '2025-10-19 03:04:49', '2025-10-19 03:10:28', 0),
(33, 'BEED-4B', 'Bachelor of Elementary Education - 4th Year Section B', 3, 4, '2025-10-19 03:04:49', '2025-10-19 03:10:28', 0),
(34, 'BSHM-1C', 'Bachelor of Science in Hospitality Management - 1st Year Section C', 2, 1, '2025-10-25 07:02:15', '2025-10-25 07:02:15', 0),
(35, 'BSHM-1D', 'Bachelor of Science in Hospitality Management - 1st Year Section D', 2, 1, '2025-10-25 07:02:27', '2025-10-25 07:02:27', 0);

-- --------------------------------------------------------

--
-- Table structure for table `section_students`
--

DROP TABLE IF EXISTS `section_students`;
CREATE TABLE `section_students` (
  `id` int(11) NOT NULL,
  `section_id` int(11) NOT NULL COMMENT 'Reference to sections.section_id',
  `student_id` int(11) NOT NULL COMMENT 'Reference to std_info.id',
  `assigned_date` datetime NOT NULL DEFAULT current_timestamp(),
  `status` enum('Active','Inactive') NOT NULL DEFAULT 'Active',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Direct section-student assignments (without class enrollment)';

--
-- Dumping data for table `section_students`
--

INSERT INTO `section_students` (`id`, `section_id`, `student_id`, `assigned_date`, `status`, `created_at`, `updated_at`) VALUES
(5, 7, 2, '2025-10-25 14:33:38', 'Active', '2025-10-14 09:17:36', '2025-10-25 06:33:38'),
(6, 8, 1, '2025-10-24 20:58:31', 'Inactive', '2025-10-14 10:20:34', '2025-10-25 04:49:53'),
(7, 15, 3, '2025-10-24 18:38:50', 'Inactive', '2025-10-19 01:39:07', '2025-10-24 10:39:50'),
(8, 7, 4, '2025-10-25 14:34:01', 'Active', '2025-10-21 15:23:43', '2025-10-25 06:34:01'),
(9, 7, 5, '2025-10-25 14:33:50', 'Active', '2025-10-21 23:18:09', '2025-10-25 06:33:50'),
(11, 7, 3, '2025-10-25 14:33:45', 'Active', '2025-10-24 10:39:50', '2025-10-25 06:33:45'),
(13, 15, 2, '2025-10-25 12:52:45', 'Inactive', '2025-10-25 04:52:45', '2025-10-25 04:53:01'),
(14, 7, 1, '2025-10-25 14:33:56', 'Active', '2025-10-25 04:55:51', '2025-10-25 06:33:56'),
(15, 35, 6, '2025-10-25 15:03:32', 'Active', '2025-10-25 07:03:32', '2025-10-25 07:03:32'),
(16, 33, 7, '2025-10-25 15:07:26', 'Active', '2025-10-25 07:07:26', '2025-10-25 07:07:26');

-- --------------------------------------------------------

--
-- Table structure for table `std_info`
--

DROP TABLE IF EXISTS `std_info`;
CREATE TABLE `std_info` (
  `id` int(11) NOT NULL,
  `std_Number` varchar(20) NOT NULL,
  `std_Surname` varchar(100) NOT NULL,
  `std_Firstname` varchar(100) NOT NULL,
  `std_Middlename` varchar(100) DEFAULT NULL,
  `std_Suffix` varchar(10) DEFAULT NULL,
  `std_Gender` enum('Male','Female','Other') NOT NULL,
  `std_Birthdate` date NOT NULL,
  `std_Age` int(11) NOT NULL,
  `std_CivilStatus` enum('Single','Married','Divorced','Widowed') DEFAULT 'Single',
  `std_Citizenship` varchar(50) DEFAULT 'Filipino',
  `std_Religion` varchar(50) DEFAULT NULL,
  `std_Address` text NOT NULL,
  `std_ContactNum` varchar(15) DEFAULT NULL,
  `std_EmailAdd` varchar(100) DEFAULT NULL,
  `std_FatherName` varchar(150) DEFAULT NULL,
  `std_FAge` int(11) DEFAULT NULL,
  `std_FOccupation` varchar(100) DEFAULT NULL,
  `std_FContactNum` varchar(15) DEFAULT NULL,
  `std_FEmail` varchar(100) DEFAULT NULL,
  `std_FEducation` varchar(100) DEFAULT NULL,
  `std_MotherName` varchar(150) DEFAULT NULL,
  `std_MAge` int(11) DEFAULT NULL,
  `std_MOccupation` varchar(100) DEFAULT NULL,
  `std_MContactNum` varchar(15) DEFAULT NULL,
  `std_MEmail` varchar(100) DEFAULT NULL,
  `std_MEducation` varchar(100) DEFAULT NULL,
  `std_LastSchool` varchar(200) DEFAULT NULL,
  `std_LSType` enum('Public','Private') DEFAULT 'Public',
  `std_LSAddress` text DEFAULT NULL,
  `std_AcadStrand` varchar(50) DEFAULT NULL,
  `std_PWD` enum('Yes','No') DEFAULT 'No',
  `std_CourseChoice1` varchar(100) DEFAULT NULL,
  `std_CourseChoice2` varchar(100) DEFAULT NULL,
  `std_CourseChoice3` varchar(100) DEFAULT NULL,
  `std_2x2` varchar(200) DEFAULT NULL,
  `std_Paying` enum('Unifast','Paying') DEFAULT 'Unifast',
  `std_Status` enum('Enrolled','UnEnrolled') DEFAULT 'Enrolled',
  `std_Level` enum('1st Year','2nd Year','3rd Year','4th Year','5th Year') DEFAULT '1st Year',
  `std_Course` varchar(100) DEFAULT NULL,
  `std_Curriculum` varchar(50) DEFAULT NULL,
  `section_id` int(11) DEFAULT NULL COMMENT 'Master section (BSCS-4A, BSIT-3B, etc.)',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `user_id` int(11) DEFAULT NULL,
  `is_archived` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'Whether the student is archived (0=active, 1=archived)'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `std_info`
--

INSERT INTO `std_info` (`id`, `std_Number`, `std_Surname`, `std_Firstname`, `std_Middlename`, `std_Suffix`, `std_Gender`, `std_Birthdate`, `std_Age`, `std_CivilStatus`, `std_Citizenship`, `std_Religion`, `std_Address`, `std_ContactNum`, `std_EmailAdd`, `std_FatherName`, `std_FAge`, `std_FOccupation`, `std_FContactNum`, `std_FEmail`, `std_FEducation`, `std_MotherName`, `std_MAge`, `std_MOccupation`, `std_MContactNum`, `std_MEmail`, `std_MEducation`, `std_LastSchool`, `std_LSType`, `std_LSAddress`, `std_AcadStrand`, `std_PWD`, `std_CourseChoice1`, `std_CourseChoice2`, `std_CourseChoice3`, `std_2x2`, `std_Paying`, `std_Status`, `std_Level`, `std_Course`, `std_Curriculum`, `section_id`, `created_at`, `updated_at`, `user_id`, `is_archived`) VALUES
(1, '2022-0215', 'Jimenez', 'Aaron Joseph', 'Mandita', '', 'Male', '2004-07-12', 21, 'Single', 'Filipino', 'Born Again', 'Diliman, Partida, Norzagaray, Bulacan', '09932326567', 'aaronjosephjimenezz@gmail.com', 'Aniceto C. Jimenez', 43, 'Trycycle Driver', '09353035009', 'japhapon@gmail.com', 'High School', 'Cherrie May F. Mandita', 43, 'School Utility', '09932326551', 'cherriemayjimenez24@gmail.com', 'Senior High School Graduate', 'Norzagaray College', 'Public', 'Municipal Compound, Poblacion, Norzagaray, Bulacan', 'Gas', 'No', 'BSCS', 'BSCS', 'BSCS', NULL, 'Unifast', 'Enrolled', '4th Year', 'Department of Computing Studies', '2018', NULL, '2025-09-12 02:36:01', '2025-10-25 06:33:56', 3, 0),
(2, '2022-0186', 'Cadorna', 'Rotcher', 'Asinas', 'Jr.', 'Male', '2004-06-16', 21, 'Married', 'Filipino', 'Catholic', 'blk2 lot 34 norhieghts brgy bitungol norzagaray bulacan', '09557850712', 'rotchercadorna16@gmail.com', 'Rotcher B. Cadorna', 47, 'Driver', '09060227405', 'rotchercadorna30@gmail.com', 'Elementary', 'Nonie Asinas', 48, 'House Wife', '0978392834', 'nonieasinas@gmail.com', 'highschool', 'Norzagaray National HighSchool', 'Public', 'Municipal Compound, Poblacion, Norzagaray, Bulacan', 'ICT', 'No', 'Information Technology', 'Computer Science', 'Marine', 'uploads/photos/2022-0186_4ce98920-2716-4afc-80de-301a95b624da.jpg', 'Unifast', 'Enrolled', '4th Year', 'Department of Computing Studies', '2018', NULL, '2025-09-12 02:36:01', '2025-10-25 06:33:38', 4, 0),
(3, '2022-01499', 'Fausto', 'Mark Allen', 'Dela Cruz', NULL, 'Male', '2004-10-20', 21, 'Single', 'Filipino', NULL, '248 Sitio Diliman Partida Norzagaray Bulacan', '09813300401', 'allenfausto92@gmail.com', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Public', NULL, NULL, 'No', NULL, NULL, NULL, NULL, 'Unifast', 'Enrolled', '4th Year', 'Department of Computing Studies', '2018', NULL, '2025-10-19 00:26:39', '2025-10-25 06:33:45', 5, 0),
(4, '2022-0206', 'Mangahas', 'Daniel', 'Pascual', NULL, 'Male', '2003-11-30', 21, 'Single', 'Filipino', NULL, 'Gulod Matictic Norzagaray Bulacan', '09675987722', 'danielmangahas11@gmail.com', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Public', NULL, NULL, 'No', NULL, NULL, NULL, NULL, 'Unifast', 'Enrolled', '4th Year', 'Department of Computing Studies', NULL, NULL, '2025-10-21 15:23:43', '2025-10-25 06:34:01', 6, 0),
(5, '2022- 0472', 'Ipo', 'Marian', 'Pagador', NULL, 'Male', '2002-07-17', 23, 'Single', 'Filipino', NULL, '200 St. Brgy Bangkal Norzagaray Bulacan', '09487866353', 'yannyipo21@gmail.com', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Public', NULL, NULL, 'No', NULL, NULL, NULL, NULL, 'Unifast', 'Enrolled', '4th Year', 'Department of Computing Studies', NULL, NULL, '2025-10-21 23:18:09', '2025-10-25 06:33:50', 7, 0),
(6, '2025-0564', ' DELOS SANTOS', 'ED ALLISON', 'B', NULL, 'Male', '2006-10-12', 19, 'Single', 'Filipino', NULL, 'Diliman, Partida, Norzagaray', '09932326567', 'edallisondelossantos509@gmail.com', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Public', NULL, NULL, 'No', NULL, NULL, NULL, NULL, 'Unifast', 'Enrolled', '1st Year', 'Department of Hospitality Management', NULL, NULL, '2025-10-25 07:03:32', '2025-10-25 07:03:32', 58, 0),
(7, '2022-322', 'Cruz', 'Gabrielle', 'Gaboa', NULL, 'Female', '2004-04-24', 21, 'Single', 'Filipino', NULL, '06 Sulucan, St. Poblacion, Norzagaray', '09611287799', 'gabriellegaboacruz@gmail.com', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Public', NULL, NULL, 'No', NULL, NULL, NULL, NULL, 'Unifast', 'Enrolled', '4th Year', 'Department of Education', NULL, NULL, '2025-10-25 07:07:26', '2025-10-25 07:07:26', 59, 0);

-- --------------------------------------------------------

--
-- Table structure for table `std_info_backup_20251019`
--

DROP TABLE IF EXISTS `std_info_backup_20251019`;
CREATE TABLE `std_info_backup_20251019` (
  `id` int(11) NOT NULL DEFAULT 0,
  `std_Number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `std_Surname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `std_Firstname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `std_Middlename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `std_Suffix` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `std_Gender` enum('Male','Female','Other') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `std_Birthdate` date NOT NULL,
  `std_Age` int(11) NOT NULL,
  `std_CivilStatus` enum('Single','Married','Divorced','Widowed') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'Single',
  `std_Citizenship` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'Filipino',
  `std_Religion` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `std_Address` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `std_ContactNum` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `std_EmailAdd` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `std_FatherName` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `std_FAge` int(11) DEFAULT NULL,
  `std_FOccupation` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `std_FContactNum` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `std_FEmail` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `std_FEducation` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `std_MotherName` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `std_MAge` int(11) DEFAULT NULL,
  `std_MOccupation` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `std_MContactNum` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `std_MEmail` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `std_MEducation` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `std_LastSchool` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `std_LSType` enum('Public','Private') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'Public',
  `std_LSAddress` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `std_AcadStrand` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `std_PWD` enum('Yes','No') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'No',
  `std_CourseChoice1` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `std_CourseChoice2` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `std_CourseChoice3` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `std_2x2` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `std_Paying` enum('Unifast','Paying') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'Unifast',
  `std_Status` enum('Enrolled','UnEnrolled') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'Enrolled',
  `std_Level` enum('1st Year','2nd Year','3rd Year','4th Year','5th Year') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '1st Year',
  `std_Course` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `std_Curriculum` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `section_id` int(11) DEFAULT NULL COMMENT 'Master section (BSCS-4A, BSIT-3B, etc.)',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `user_id` int(11) DEFAULT NULL,
  `is_archived` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'Whether the student is archived (0=active, 1=archived)'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `std_info_backup_20251019`
--

INSERT INTO `std_info_backup_20251019` (`id`, `std_Number`, `std_Surname`, `std_Firstname`, `std_Middlename`, `std_Suffix`, `std_Gender`, `std_Birthdate`, `std_Age`, `std_CivilStatus`, `std_Citizenship`, `std_Religion`, `std_Address`, `std_ContactNum`, `std_EmailAdd`, `std_FatherName`, `std_FAge`, `std_FOccupation`, `std_FContactNum`, `std_FEmail`, `std_FEducation`, `std_MotherName`, `std_MAge`, `std_MOccupation`, `std_MContactNum`, `std_MEmail`, `std_MEducation`, `std_LastSchool`, `std_LSType`, `std_LSAddress`, `std_AcadStrand`, `std_PWD`, `std_CourseChoice1`, `std_CourseChoice2`, `std_CourseChoice3`, `std_2x2`, `std_Paying`, `std_Status`, `std_Level`, `std_Course`, `std_Curriculum`, `section_id`, `created_at`, `updated_at`, `user_id`, `is_archived`) VALUES
(1, '2022-0215', 'Jimenez', 'Aaron Joseph', 'Mandita', '', 'Male', '2004-07-12', 21, 'Single', 'Filipino', 'Born Again', 'Diliman, Partida, Norzagaray, Bulacan', '09932326567', 'aaronjosephjimenezz@gmail.com', 'Aniceto C. Jimenez', 43, 'Trycycle Driver', '09353035009', 'japhapon@gmail.com', 'High School', 'Cherrie May F. Mandita', 43, 'School Utility', '09932326551', 'cherriemayjimenez24@gmail.com', 'Senior High School Graduate', 'Norzagaray College', 'Public', 'Municipal Compound, Poblacion, Norzagaray, Bulacan', 'Gas', 'No', 'BSCS', 'BSCS', 'BSCS', NULL, 'Unifast', 'Enrolled', '4th Year', 'Bachelor of Science in Computer Science', '2018', NULL, '2025-09-12 02:36:01', '2025-09-12 03:53:49', 3, 0),
(2, '2022-0186', 'Cadorna', 'Rotcher', 'Asinas', 'Jr.', 'Male', '2004-06-16', 21, 'Married', 'Filipino', 'Catholic', 'blk2 lot 34 norhieghts brgy bitungol norzagaray bulacan', '09557850712', 'rotchercadorna16@gmail.com', 'Rotcher B. Cadorna', 47, 'Driver', '09060227405', 'rotchercadorna30@gmail.com', 'Elementary', 'Nonie Asinas', 48, 'House Wife', '0978392834', 'nonieasinas@gmail.com', 'highschool', 'Norzagaray National HighSchool', 'Public', 'Municipal Compound, Poblacion, Norzagaray, Bulacan', 'ICT', 'No', 'Information Technology', 'Computer Science', 'Marine', 'uploads/photos/2022-0186_4ce98920-2716-4afc-80de-301a95b624da.jpg', 'Unifast', 'Enrolled', '4th Year', 'Bachelor of Science in Computer Science', '2018', 7, '2025-09-12 02:36:01', '2025-10-19 02:43:44', 4, 0),
(3, '2022-0123', 'doe', 'john', '', NULL, 'Male', '2004-06-19', 21, 'Single', 'Filipino', NULL, 'partida norzagaray', '091212345677', 'eyronbotmalakas@gmail.com', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Public', NULL, NULL, 'No', NULL, NULL, NULL, NULL, 'Unifast', 'Enrolled', '4th Year', 'Bachelor of Science in Hospitality Management', '2018', NULL, '2025-10-19 00:26:39', '2025-10-19 02:44:40', 5, 0);

-- --------------------------------------------------------

--
-- Table structure for table `subjects`
--

DROP TABLE IF EXISTS `subjects`;
CREATE TABLE `subjects` (
  `subject_id` int(11) NOT NULL,
  `program_id` int(11) NOT NULL,
  `subject_code` varchar(20) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `units` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `subjects`
--

INSERT INTO `subjects` (`subject_id`, `program_id`, `subject_code`, `title`, `description`, `units`, `created_at`, `updated_at`) VALUES
(25, 1, 'NC102', 'Network and Communication', 'Network and Communication', 3, '2025-10-25 05:20:19', '2025-10-25 05:20:19'),
(26, 1, 'FREELEC103', 'Robotics', 'Robotics', 3, '2025-10-25 05:21:57', '2025-10-25 05:21:57'),
(27, 1, 'FL101', 'Foreign Language', 'Foreign Language', 3, '2025-10-25 05:27:53', '2025-10-25 05:27:53'),
(28, 1, 'AL101', 'Automatic Theory and Formal Languages', 'Automatic Theory and Formal Languages', 3, '2025-10-25 05:28:08', '2025-10-25 05:28:08'),
(29, 2, 'GE2', 'Readings in Philippine History with Indigenous People Studies', 'Readings in Philippine History with Indigenous People Studies', 3, '2025-10-25 06:58:27', '2025-10-25 06:58:27'),
(30, 2, 'HPC1', 'Fundamentals in Food Service Operations', 'Fundamentals in Food Service Operations', 3, '2025-10-25 06:58:53', '2025-10-25 06:58:53'),
(31, 2, 'ABM1', 'Fundamentals of Accounting/Business and Management', 'Fundamentals of Accounting/Business and Management', 3, '2025-10-25 06:59:10', '2025-10-25 06:59:10'),
(32, 3, 'BEED221', 'Research in Education(Thesis Writing)', 'Research in Education(Thesis Writing)', 3, '2025-10-25 07:08:38', '2025-10-25 07:08:38'),
(33, 1, 'PL101', 'Programming Languages', 'Programming Languages', 3, '2025-10-26 09:13:06', '2025-10-26 09:13:06');

-- --------------------------------------------------------

--
-- Table structure for table `timer_settings`
--

DROP TABLE IF EXISTS `timer_settings`;
CREATE TABLE `timer_settings` (
  `setting_id` int(11) NOT NULL DEFAULT 1,
  `enabled` tinyint(1) NOT NULL DEFAULT 1 COMMENT 'Whether timer is enabled globally',
  `time_limit` int(11) NOT NULL DEFAULT 30 COMMENT 'Time limit for evaluations in minutes',
  `warning_1` int(11) NOT NULL DEFAULT 5 COMMENT 'First warning time in minutes before timeout',
  `warning_2` int(11) NOT NULL DEFAULT 2 COMMENT 'Second warning time in minutes before timeout',
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `updated_by` int(11) DEFAULT NULL COMMENT 'User ID of who last updated settings'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Global timer settings for evaluation forms';

--
-- Dumping data for table `timer_settings`
--

INSERT INTO `timer_settings` (`setting_id`, `enabled`, `time_limit`, `warning_1`, `warning_2`, `updated_at`, `updated_by`) VALUES
(1, 1, 6, 2, 1, '2025-10-25 14:55:48', 2);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `role` enum('admin','student','guidance') NOT NULL,
  `profile_image` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `is_verified` tinyint(1) NOT NULL DEFAULT 0,
  `verification_token` varchar(255) DEFAULT NULL,
  `reset_token` varchar(255) DEFAULT NULL,
  `reset_token_expiry` datetime DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password`, `email`, `first_name`, `last_name`, `role`, `profile_image`, `is_active`, `is_verified`, `verification_token`, `reset_token`, `reset_token_expiry`, `last_login`, `created_at`, `updated_at`) VALUES
(1, 'admin', 'b1234ef905a57887663c10e064bfb1510ff8881f22d679bf881ee09d8e9072406cc6f8527054c7038d0d9fed21c37c95df5981a1eb406a01e993e6698581cc19af2fa180e4fafdc55ba8266a52a6540d5d572e5b03a2b970e3e4b42f299f2731', 'aurumpascual@gmail.com', 'Aurum', 'Pascual', 'admin', NULL, 1, 1, NULL, NULL, NULL, '2025-10-26 17:11:51', '2025-09-12 02:36:01', '2025-10-26 09:11:51'),
(2, 'guidance', '03fcf7d850b0ec95a58425979e6937ddac1a82922758b85be2eead5e8d89bc0b61b9b791530c6f53ea01799af25033b7c5bf6d14a85990c51776858c3ac5b78b1dc7c00be2e2c3bb4aed2f5a089a5a5b2cd9b9bab242fd25ddc0ad14df876fc5', 'guidance@intellevalpro.com', 'Dr. Sarah', 'Brooks', 'guidance', NULL, 1, 1, NULL, NULL, NULL, '2025-10-26 17:49:09', '2025-09-15 00:53:55', '2025-10-26 09:49:09'),
(3, '2022-0215', 'BN2/FyyEI9aOfnUmIG2YjAgAYfM/WYHmXLCm+JR0Y/Yf2W42cpVzf6lOkJUTrSGb2tR0H8PUishDRgbWVVK24B+bq8l48My5T+/Hv3QwJeWCCXk7i69mW59DhQQN393V', 'aaronjosephjimenezz@gmail.com', 'Aaron Joseph', 'Jimenez', 'student', NULL, 1, 1, NULL, '335GFNUa9zz5aKGxqXkI8-Q_9TLcb1VbfF21zaFrKCkZ56HdrmUvkPZsDawnyIYP', '2025-10-21 21:59:12', '2025-10-26 16:46:10', '2025-09-12 03:53:49', '2025-10-26 08:46:10'),
(4, '2022-0186', '9z1F0sB3qNHO+296bKsI0DdEr9gwWtrHe6Qe2tfZT2Af5Kv28zKsYhaB+2uNpF4rmo91UBx7Xw6qJVqOlfsnpnfEBiXfP6RRCrAsi3FSnNk2Qktjci0BmatSurjsFV1i', 'rotchercadorna16@gmail.com', 'Rotcher', 'Cadorna', 'student', NULL, 1, 1, NULL, NULL, NULL, '2025-10-26 00:18:02', '2025-09-12 03:53:49', '2025-10-25 16:18:02'),
(5, '2022-0149', '7a6c7bcb116de423935f052c73a690d1c4f34cbb7a333a82c713c1bea45e0b39e62b5093c5aec08f1d6396478093b0d77de3d74364c4cd0de3e86f8ba555b2d4a865109b276374732fb21bca70b92345ba8e491f6cd25639cadd798f154dcc67', 'allenfausto92@gmail.com', 'Mark Allen', 'Fausto', 'student', NULL, 1, 1, NULL, NULL, NULL, NULL, '2025-10-19 00:26:39', '2025-10-26 09:18:13'),
(6, '2022-0206', '5bd925515501dc91dc4458b51d6c659462df4133acf30dd6fe7d4625c1e4a0f78b4516dfa2bc6cbd30dba96f6244d5c63944540db50a2f500ac0c63411f2d645b1778f78ff10f7c9a86e96e7f5a7c2918eee4544e8a2ce85cc63c159dfa20016', 'danielmangahas11@gmail.com', 'Daniel', 'Mangahas', 'student', NULL, 1, 1, NULL, NULL, NULL, '2025-10-26 17:18:35', '2025-10-21 15:23:43', '2025-10-26 09:18:35'),
(7, '2022- 0472', '34a67924f01d88842aa83238a296917594cecbbc0936b0bd5d9f21788c24353d61cbb9ea007d3c64277006e86449cf80665efa72f45bf3b3f606e65798aeeaa8de61c7dcef44264ebc5237f46d769beb3c331aceaa87ef9318add7e1b4b6ee92', 'yannyipo21@gmail.com', 'Marian', 'Ipo', 'student', NULL, 1, 1, NULL, NULL, NULL, NULL, '2025-10-21 23:18:09', '2025-10-25 06:33:50'),
(58, '2025-0564', 'BN2/FyyEI9aOfnUmIG2YjAgAYfM/WYHmXLCm+JR0Y/Yf2W42cpVzf6lOkJUTrSGb2tR0H8PUishDRgbWVVK24B+bq8l48My5T+/Hv3QwJeWCCXk7i69mW59DhQQN393V', 'edallisondelossantos509@gmail.com', 'ED ALLISON', ' DELOS SANTOS', 'student', NULL, 1, 1, NULL, NULL, NULL, '2025-10-26 17:20:17', '2025-10-25 07:03:32', '2025-10-26 09:20:17'),
(59, '2022-0322', 'BN2/FyyEI9aOfnUmIG2YjAgAYfM/WYHmXLCm+JR0Y/Yf2W42cpVzf6lOkJUTrSGb2tR0H8PUishDRgbWVVK24B+bq8l48My5T+/Hv3QwJeWCCXk7i69mW59DhQQN393V', 'gabriellegaboacruz@gmail.com', 'Gabrielle', 'Cruz', 'student', NULL, 1, 1, NULL, NULL, NULL, '2025-10-26 17:19:38', '2025-10-25 07:07:26', '2025-10-26 09:19:38');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `academic_terms`
--
ALTER TABLE `academic_terms`
  ADD PRIMARY KEY (`acad_term_id`),
  ADD UNIQUE KEY `unique_year_term` (`acad_year_id`,`term_code`),
  ADD KEY `fk_term_year` (`acad_year_id`),
  ADD KEY `idx_is_current` (`is_current`);

--
-- Indexes for table `academic_years`
--
ALTER TABLE `academic_years`
  ADD PRIMARY KEY (`acad_year_id`),
  ADD UNIQUE KEY `unique_year_code` (`year_code`),
  ADD KEY `idx_is_current` (`is_current`);

--
-- Indexes for table `activity_logs`
--
ALTER TABLE `activity_logs`
  ADD PRIMARY KEY (`log_id`),
  ADD KEY `idx_user_id` (`user_id`),
  ADD KEY `idx_activity_type` (`activity_type`),
  ADD KEY `idx_timestamp` (`timestamp`),
  ADD KEY `idx_user_role` (`user_role`);

--
-- Indexes for table `analytics_config`
--
ALTER TABLE `analytics_config`
  ADD PRIMARY KEY (`config_id`),
  ADD UNIQUE KEY `unique_config_key` (`config_key`);

--
-- Indexes for table `category_performance_analytics`
--
ALTER TABLE `category_performance_analytics`
  ADD PRIMARY KEY (`category_analytics_id`),
  ADD KEY `idx_analytics_category` (`analytics_id`,`category_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `class_sections`
--
ALTER TABLE `class_sections`
  ADD PRIMARY KEY (`section_id`),
  ADD KEY `fk_sections_subjects` (`subject_id`),
  ADD KEY `fk_sections_faculty` (`faculty_id`),
  ADD KEY `idx_section_ref` (`section_ref_id`),
  ADD KEY `fk_class_sections_term` (`acad_term_id`);

--
-- Indexes for table `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`comment_id`),
  ADD KEY `fk_comments_evaluations` (`evaluation_id`);

--
-- Indexes for table `enrollments`
--
ALTER TABLE `enrollments`
  ADD PRIMARY KEY (`enrollment_id`),
  ADD UNIQUE KEY `student_section_UNIQUE` (`student_id`,`section_id`),
  ADD KEY `fk_enrollments_sections` (`section_id`);

--
-- Indexes for table `evaluations`
--
ALTER TABLE `evaluations`
  ADD PRIMARY KEY (`evaluation_id`),
  ADD UNIQUE KEY `period_section_student_UNIQUE` (`period_id`,`section_id`,`student_id`),
  ADD KEY `fk_evaluations_sections` (`section_id`),
  ADD KEY `fk_evaluations_students` (`student_id`);

--
-- Indexes for table `evaluation_categories`
--
ALTER TABLE `evaluation_categories`
  ADD PRIMARY KEY (`category_id`),
  ADD KEY `idx_is_archived` (`is_archived`),
  ADD KEY `idx_display_order` (`display_order`);

--
-- Indexes for table `evaluation_criteria`
--
ALTER TABLE `evaluation_criteria`
  ADD PRIMARY KEY (`criteria_id`),
  ADD KEY `fk_criteria_categories` (`category_id`);

--
-- Indexes for table `evaluation_drafts`
--
ALTER TABLE `evaluation_drafts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_evaluation_drafts_evaluation_id` (`evaluation_id`);

--
-- Indexes for table `evaluation_periods`
--
ALTER TABLE `evaluation_periods`
  ADD PRIMARY KEY (`period_id`),
  ADD KEY `fk_evaluation_periods_term` (`acad_term_id`);

--
-- Indexes for table `evaluation_responses`
--
ALTER TABLE `evaluation_responses`
  ADD PRIMARY KEY (`response_id`),
  ADD UNIQUE KEY `evaluation_criteria_UNIQUE` (`evaluation_id`,`criteria_id`),
  ADD KEY `fk_responses_criteria` (`criteria_id`);

--
-- Indexes for table `evaluation_timer_sessions`
--
ALTER TABLE `evaluation_timer_sessions`
  ADD PRIMARY KEY (`session_id`),
  ADD KEY `idx_evaluation` (`evaluation_id`),
  ADD KEY `idx_user` (`user_id`),
  ADD KEY `idx_status` (`status`);

--
-- Indexes for table `faculty`
--
ALTER TABLE `faculty`
  ADD PRIMARY KEY (`faculty_id`),
  ADD UNIQUE KEY `faculty_number_UNIQUE` (`faculty_number`),
  ADD KEY `fk_faculty_programs` (`program_id`),
  ADD KEY `idx_faculty_archived` (`is_archived`);

--
-- Indexes for table `faculty_performance_analytics`
--
ALTER TABLE `faculty_performance_analytics`
  ADD PRIMARY KEY (`analytics_id`),
  ADD UNIQUE KEY `unique_faculty_period` (`faculty_id`,`period_id`),
  ADD KEY `idx_faculty_performance` (`faculty_id`,`period_id`),
  ADD KEY `idx_period_performance` (`period_id`,`average_rating`),
  ADD KEY `idx_performance_grade` (`performance_grade`);

--
-- Indexes for table `faculty_recommendations`
--
ALTER TABLE `faculty_recommendations`
  ADD PRIMARY KEY (`recommendation_id`),
  ADD KEY `idx_faculty_id` (`faculty_id`),
  ADD KEY `idx_counselor_id` (`counselor_id`),
  ADD KEY `idx_updated_at` (`updated_at`);

--
-- Indexes for table `generated_reports`
--
ALTER TABLE `generated_reports`
  ADD PRIMARY KEY (`report_id`),
  ADD KEY `idx_report_type` (`report_type`),
  ADD KEY `idx_period_id` (`period_id`),
  ADD KEY `idx_program_id` (`program_id`),
  ADD KEY `idx_created_at` (`created_at`),
  ADD KEY `fk_report_generated_by` (`generated_by`),
  ADD KEY `idx_faculty_id` (`faculty_id`);

--
-- Indexes for table `performance_trends`
--
ALTER TABLE `performance_trends`
  ADD PRIMARY KEY (`trend_id`),
  ADD KEY `idx_faculty_period_metric` (`faculty_id`,`period_id`,`metric_name`),
  ADD KEY `period_id` (`period_id`),
  ADD KEY `idx_performance_trends_faculty` (`faculty_id`,`created_at`);

--
-- Indexes for table `programs`
--
ALTER TABLE `programs`
  ADD PRIMARY KEY (`program_id`),
  ADD UNIQUE KEY `program_code` (`program_code`);

--
-- Indexes for table `response_analytics`
--
ALTER TABLE `response_analytics`
  ADD PRIMARY KEY (`response_analytics_id`),
  ADD KEY `idx_period` (`period_id`),
  ADD KEY `idx_faculty` (`faculty_id`),
  ADD KEY `idx_subject` (`subject_id`),
  ADD KEY `idx_section` (`section_id`),
  ADD KEY `idx_response_analytics_rate` (`response_rate`);

--
-- Indexes for table `sections`
--
ALTER TABLE `sections`
  ADD PRIMARY KEY (`section_id`),
  ADD UNIQUE KEY `unique_section_code` (`section_code`),
  ADD KEY `idx_program` (`program_id`),
  ADD KEY `idx_is_disable` (`is_disable`);

--
-- Indexes for table `section_students`
--
ALTER TABLE `section_students`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_section_student` (`section_id`,`student_id`),
  ADD KEY `idx_section` (`section_id`),
  ADD KEY `idx_student` (`student_id`),
  ADD KEY `idx_status` (`status`);

--
-- Indexes for table `std_info`
--
ALTER TABLE `std_info`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `std_Number` (`std_Number`),
  ADD UNIQUE KEY `std_EmailAdd` (`std_EmailAdd`),
  ADD KEY `idx_std_number` (`std_Number`),
  ADD KEY `idx_std_lastname` (`std_Surname`),
  ADD KEY `idx_std_email` (`std_EmailAdd`),
  ADD KEY `idx_std_status` (`std_Status`),
  ADD KEY `idx_std_level` (`std_Level`),
  ADD KEY `fk_std_info_user` (`user_id`),
  ADD KEY `idx_is_archived` (`is_archived`),
  ADD KEY `fk_std_info_sections` (`section_id`);

--
-- Indexes for table `subjects`
--
ALTER TABLE `subjects`
  ADD PRIMARY KEY (`subject_id`),
  ADD UNIQUE KEY `subject_code_UNIQUE` (`subject_code`),
  ADD KEY `fk_subjects_programs` (`program_id`);

--
-- Indexes for table `timer_settings`
--
ALTER TABLE `timer_settings`
  ADD PRIMARY KEY (`setting_id`),
  ADD KEY `fk_timer_settings_user` (`updated_by`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username_UNIQUE` (`username`),
  ADD UNIQUE KEY `email_UNIQUE` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `academic_terms`
--
ALTER TABLE `academic_terms`
  MODIFY `acad_term_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `academic_years`
--
ALTER TABLE `academic_years`
  MODIFY `acad_year_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `activity_logs`
--
ALTER TABLE `activity_logs`
  MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=89;

--
-- AUTO_INCREMENT for table `analytics_config`
--
ALTER TABLE `analytics_config`
  MODIFY `config_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `category_performance_analytics`
--
ALTER TABLE `category_performance_analytics`
  MODIFY `category_analytics_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `class_sections`
--
ALTER TABLE `class_sections`
  MODIFY `section_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=130;

--
-- AUTO_INCREMENT for table `comments`
--
ALTER TABLE `comments`
  MODIFY `comment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `enrollments`
--
ALTER TABLE `enrollments`
  MODIFY `enrollment_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `evaluations`
--
ALTER TABLE `evaluations`
  MODIFY `evaluation_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=255;

--
-- AUTO_INCREMENT for table `evaluation_categories`
--
ALTER TABLE `evaluation_categories`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `evaluation_criteria`
--
ALTER TABLE `evaluation_criteria`
  MODIFY `criteria_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=54;

--
-- AUTO_INCREMENT for table `evaluation_drafts`
--
ALTER TABLE `evaluation_drafts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `evaluation_periods`
--
ALTER TABLE `evaluation_periods`
  MODIFY `period_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `evaluation_responses`
--
ALTER TABLE `evaluation_responses`
  MODIFY `response_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=323;

--
-- AUTO_INCREMENT for table `evaluation_timer_sessions`
--
ALTER TABLE `evaluation_timer_sessions`
  MODIFY `session_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `faculty`
--
ALTER TABLE `faculty`
  MODIFY `faculty_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `faculty_performance_analytics`
--
ALTER TABLE `faculty_performance_analytics`
  MODIFY `analytics_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=101;

--
-- AUTO_INCREMENT for table `faculty_recommendations`
--
ALTER TABLE `faculty_recommendations`
  MODIFY `recommendation_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `generated_reports`
--
ALTER TABLE `generated_reports`
  MODIFY `report_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `performance_trends`
--
ALTER TABLE `performance_trends`
  MODIFY `trend_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `programs`
--
ALTER TABLE `programs`
  MODIFY `program_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `response_analytics`
--
ALTER TABLE `response_analytics`
  MODIFY `response_analytics_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sections`
--
ALTER TABLE `sections`
  MODIFY `section_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `section_students`
--
ALTER TABLE `section_students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `std_info`
--
ALTER TABLE `std_info`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `subjects`
--
ALTER TABLE `subjects`
  MODIFY `subject_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=60;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `academic_terms`
--
ALTER TABLE `academic_terms`
  ADD CONSTRAINT `fk_term_year` FOREIGN KEY (`acad_year_id`) REFERENCES `academic_years` (`acad_year_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `activity_logs`
--
ALTER TABLE `activity_logs`
  ADD CONSTRAINT `activity_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL;

--
-- Constraints for table `class_sections`
--
ALTER TABLE `class_sections`
  ADD CONSTRAINT `fk_class_sections_section` FOREIGN KEY (`section_ref_id`) REFERENCES `sections` (`section_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_class_sections_term` FOREIGN KEY (`acad_term_id`) REFERENCES `academic_terms` (`acad_term_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_sections_faculty` FOREIGN KEY (`faculty_id`) REFERENCES `faculty` (`faculty_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_sections_subjects` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`subject_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
