"""
Faculty Performance and Response Analytics Model
Handles all analytics calculations and data aggregation
"""
from models.database import get_db_connection
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

class FacultyAnalytics:
    """Faculty Performance Analytics Handler"""
    
    @staticmethod
    def calculate_faculty_performance(faculty_id: int, period_id: int, subject_id: Optional[int] = None) -> Dict:
        """Calculate comprehensive performance metrics for a faculty member"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Base query conditions
            subject_condition = "AND cs.subject_id = %s" if subject_id else ""
            params = [faculty_id, period_id]
            if subject_id:
                params.append(subject_id)
            
            # Get evaluation statistics
            cursor.execute(f"""
                SELECT 
                    COUNT(DISTINCT e.evaluation_id) as total_evaluations,
                    COUNT(DISTINCT CASE WHEN e.status = 'Completed' THEN e.evaluation_id END) as completed_evaluations,
                    COUNT(DISTINCT er.response_id) as total_responses,
                    AVG(CASE WHEN er.rating IS NOT NULL THEN er.rating END) as average_rating,
                    COUNT(DISTINCT c.comment_id) as total_comments,
                    COUNT(DISTINCT CASE WHEN c.sentiment = 'Positive' THEN c.comment_id END) as positive_comments,
                    COUNT(DISTINCT CASE WHEN c.sentiment = 'Negative' THEN c.comment_id END) as negative_comments,
                    COUNT(DISTINCT CASE WHEN c.sentiment = 'Neutral' THEN c.comment_id END) as neutral_comments
                FROM evaluations e
                JOIN class_sections cs ON e.section_id = cs.section_id
                LEFT JOIN evaluation_responses er ON e.evaluation_id = er.evaluation_id
                LEFT JOIN comments c ON e.evaluation_id = c.evaluation_id
                WHERE cs.faculty_id = %s 
                AND e.period_id = %s
                {subject_condition}
            """, params)
            
            stats = cursor.fetchone()
            
            # Calculate response rate
            total_evaluations = stats['total_evaluations'] or 0
            completed_evaluations = stats['completed_evaluations'] or 0
            response_rate = (completed_evaluations / total_evaluations * 100) if total_evaluations > 0 else 0
            
            # Get category-wise performance
            cursor.execute(f"""
                SELECT 
                    ec.category_id,
                    ec.name as category_name,
                    AVG(er.rating) as average_score,
                    COUNT(er.response_id) as total_responses,
                    JSON_OBJECT(
                        '1', COUNT(CASE WHEN er.rating = 1 THEN 1 END),
                        '2', COUNT(CASE WHEN er.rating = 2 THEN 1 END),
                        '3', COUNT(CASE WHEN er.rating = 3 THEN 1 END),
                        '4', COUNT(CASE WHEN er.rating = 4 THEN 1 END),
                        '5', COUNT(CASE WHEN er.rating = 5 THEN 1 END)
                    ) as score_distribution
                FROM evaluations e
                JOIN class_sections cs ON e.section_id = cs.section_id
                JOIN evaluation_responses er ON e.evaluation_id = er.evaluation_id
                JOIN evaluation_criteria ecr ON er.criteria_id = ecr.criteria_id
                JOIN evaluation_categories ec ON ecr.category_id = ec.category_id
                WHERE cs.faculty_id = %s 
                AND e.period_id = %s
                AND e.status = 'Completed'
                {subject_condition}
                GROUP BY ec.category_id, ec.name
            """, params)
            
            category_performance = cursor.fetchall()
            
            # Calculate overall score and performance grade
            average_rating = float(stats['average_rating'] or 0)
            overall_score = average_rating * 20  # Convert to 100-point scale
            performance_grade = FacultyAnalytics._calculate_performance_grade(average_rating)
            
            # Get top strengths and improvement areas from comments
            strengths, improvements = FacultyAnalytics._analyze_comments(faculty_id, period_id, subject_id)
            
            result = {
                'faculty_id': faculty_id,
                'period_id': period_id,
                'subject_id': subject_id,
                'total_evaluations': total_evaluations,
                'completed_evaluations': completed_evaluations,
                'response_rate': round(response_rate, 2),
                'average_rating': round(average_rating, 2),
                'overall_score': round(overall_score, 2),
                'performance_grade': performance_grade,
                'strengths_summary': '; '.join(strengths[:3]),  # Top 3 strengths
                'improvement_areas': '; '.join(improvements[:3]),  # Top 3 areas
                'total_comments': stats['total_comments'] or 0,
                'positive_comments': stats['positive_comments'] or 0,
                'negative_comments': stats['negative_comments'] or 0,
                'neutral_comments': stats['neutral_comments'] or 0,
                'category_performance': category_performance
            }
            
            cursor.close()
            conn.close()
            return result
            
        except Exception as e:
            logger.error(f"Error calculating faculty performance: {str(e)}")
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
            return {}
    
    @staticmethod
    def _calculate_performance_grade(average_rating: float) -> str:
        """Calculate performance grade based on average rating"""
        if average_rating >= 4.5:
            return 'Excellent'
        elif average_rating >= 4.0:
            return 'Very Good'
        elif average_rating >= 3.5:
            return 'Good'
        elif average_rating >= 3.0:
            return 'Satisfactory'
        else:
            return 'Needs Improvement'
    
    @staticmethod
    def _analyze_comments(faculty_id: int, period_id: int, subject_id: Optional[int] = None) -> Tuple[List[str], List[str]]:
        """Analyze comments to extract strengths and improvement areas"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            subject_condition = "AND cs.subject_id = %s" if subject_id else ""
            params = [faculty_id, period_id]
            if subject_id:
                params.append(subject_id)
            
            # Get positive comments for strengths
            cursor.execute(f"""
                SELECT c.comment_text
                FROM comments c
                JOIN evaluations e ON c.evaluation_id = e.evaluation_id
                JOIN class_sections cs ON e.section_id = cs.section_id
                WHERE cs.faculty_id = %s 
                AND e.period_id = %s
                AND c.sentiment = 'Positive'
                {subject_condition}
                ORDER BY CHAR_LENGTH(c.comment_text) DESC
                LIMIT 10
            """, params)
            
            positive_comments = cursor.fetchall()
            
            # Get negative comments for improvements
            cursor.execute(f"""
                SELECT c.comment_text
                FROM comments c
                JOIN evaluations e ON c.evaluation_id = e.evaluation_id
                JOIN class_sections cs ON e.section_id = cs.section_id
                WHERE cs.faculty_id = %s 
                AND e.period_id = %s
                AND c.sentiment = 'Negative'
                {subject_condition}
                ORDER BY CHAR_LENGTH(c.comment_text) DESC
                LIMIT 10
            """, params)
            
            negative_comments = cursor.fetchall()
            
            # Extract key themes (simplified version - in production, use NLP)
            strengths = FacultyAnalytics._extract_themes([c['comment_text'] for c in positive_comments])
            improvements = FacultyAnalytics._extract_themes([c['comment_text'] for c in negative_comments])
            
            cursor.close()
            conn.close()
            
            return strengths, improvements
            
        except Exception as e:
            logger.error(f"Error analyzing comments: {str(e)}")
            return [], []
    
    @staticmethod
    def _extract_themes(comments: List[str]) -> List[str]:
        """Extract common themes from comments (simplified keyword-based approach)"""
        if not comments:
            return []
        
        # Keywords for different aspects
        theme_keywords = {
            'Clear Explanation': ['clear', 'explain', 'understand', 'clarity'],
            'Engaging Teaching': ['engaging', 'interesting', 'interactive', 'participation'],
            'Well Prepared': ['prepared', 'organized', 'structure', 'plan'],
            'Helpful': ['helpful', 'support', 'assistance', 'available'],
            'Knowledgeable': ['knowledge', 'expert', 'experienced', 'skilled'],
            'Patient': ['patient', 'understanding', 'calm', 'kind'],
            'Communication': ['communication', 'speak', 'voice', 'presentation'],
            'Time Management': ['time', 'punctual', 'schedule', 'manage'],
            'Assessment': ['exam', 'test', 'grade', 'feedback', 'evaluation'],
            'Technology Use': ['technology', 'online', 'digital', 'computer']
        }
        
        theme_scores = {}
        text = ' '.join(comments).lower()
        
        for theme, keywords in theme_keywords.items():
            score = sum(text.count(keyword) for keyword in keywords)
            if score > 0:
                theme_scores[theme] = score
        
        # Return top themes sorted by frequency
        return sorted(theme_scores.keys(), key=lambda x: theme_scores[x], reverse=True)
    
    @staticmethod
    def save_analytics_to_db(analytics_data: Dict) -> bool:
        """Save calculated analytics to database"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Insert or update faculty performance analytics
            cursor.execute("""
                INSERT INTO faculty_performance_analytics 
                (faculty_id, period_id, subject_id, total_evaluations, completed_evaluations, 
                 response_rate, average_rating, overall_score, performance_grade, 
                 strengths_summary, improvement_areas, total_comments, positive_comments, 
                 negative_comments, neutral_comments, last_calculated)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                ON DUPLICATE KEY UPDATE
                total_evaluations = VALUES(total_evaluations),
                completed_evaluations = VALUES(completed_evaluations),
                response_rate = VALUES(response_rate),
                average_rating = VALUES(average_rating),
                overall_score = VALUES(overall_score),
                performance_grade = VALUES(performance_grade),
                strengths_summary = VALUES(strengths_summary),
                improvement_areas = VALUES(improvement_areas),
                total_comments = VALUES(total_comments),
                positive_comments = VALUES(positive_comments),
                negative_comments = VALUES(negative_comments),
                neutral_comments = VALUES(neutral_comments),
                last_calculated = NOW()
            """, (
                analytics_data['faculty_id'],
                analytics_data['period_id'],
                analytics_data['subject_id'],
                analytics_data['total_evaluations'],
                analytics_data['completed_evaluations'],
                analytics_data['response_rate'],
                analytics_data['average_rating'],
                analytics_data['overall_score'],
                analytics_data['performance_grade'],
                analytics_data['strengths_summary'],
                analytics_data['improvement_areas'],
                analytics_data['total_comments'],
                analytics_data['positive_comments'],
                analytics_data['negative_comments'],
                analytics_data['neutral_comments']
            ))
            
            analytics_id = cursor.lastrowid
            
            # Save category performance data
            if analytics_data.get('category_performance'):
                for category in analytics_data['category_performance']:
                    performance_level = FacultyAnalytics._calculate_performance_grade(category['average_score'])
                    
                    cursor.execute("""
                        INSERT INTO category_performance_analytics 
                        (analytics_id, category_id, average_score, total_responses, 
                         score_distribution, performance_level)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        average_score = VALUES(average_score),
                        total_responses = VALUES(total_responses),
                        score_distribution = VALUES(score_distribution),
                        performance_level = VALUES(performance_level)
                    """, (
                        analytics_id,
                        category['category_id'],
                        category['average_score'],
                        category['total_responses'],
                        category['score_distribution'],
                        performance_level
                    ))
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"Error saving analytics to database: {str(e)}")
            if 'conn' in locals():
                conn.rollback()
                cursor.close()
                conn.close()
            return False
    
    @staticmethod
    def calculate_response_analytics(period_id: int) -> Dict:
        """Calculate response rate analytics for a period"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Overall response statistics
            cursor.execute("""
                SELECT 
                    COUNT(DISTINCT e.evaluation_id) as total_evaluations,
                    COUNT(DISTINCT CASE WHEN e.status = 'Completed' THEN e.evaluation_id END) as completed_evaluations,
                    COUNT(DISTINCT CASE WHEN e.status = 'In Progress' THEN e.evaluation_id END) as in_progress,
                    COUNT(DISTINCT CASE WHEN e.status = 'Pending' THEN e.evaluation_id END) as pending,
                    AVG(CASE WHEN e.completion_time IS NOT NULL AND e.start_time IS NOT NULL 
                        THEN TIMESTAMPDIFF(MINUTE, e.start_time, e.completion_time) END) as avg_completion_time
                FROM evaluations e
                WHERE e.period_id = %s
            """, (period_id,))
            
            overall_stats = cursor.fetchone()
            
            # Faculty-wise response rates
            cursor.execute("""
                SELECT 
                    f.faculty_id,
                    CONCAT(f.first_name, ' ', f.last_name) as faculty_name,
                    COUNT(DISTINCT e.evaluation_id) as total_evaluations,
                    COUNT(DISTINCT CASE WHEN e.status = 'Completed' THEN e.evaluation_id END) as completed,
                    ROUND(COUNT(DISTINCT CASE WHEN e.status = 'Completed' THEN e.evaluation_id END) / 
                          COUNT(DISTINCT e.evaluation_id) * 100, 2) as response_rate
                FROM faculty f
                JOIN class_sections cs ON f.faculty_id = cs.faculty_id
                JOIN evaluations e ON cs.section_id = e.section_id
                WHERE e.period_id = %s
                GROUP BY f.faculty_id, f.first_name, f.last_name
                ORDER BY response_rate DESC
            """, (period_id,))
            
            faculty_stats = cursor.fetchall()
            
            # Subject-wise response rates
            cursor.execute("""
                SELECT 
                    s.subject_id,
                    s.subject_code,
                    s.title as subject_title,
                    COUNT(DISTINCT e.evaluation_id) as total_evaluations,
                    COUNT(DISTINCT CASE WHEN e.status = 'Completed' THEN e.evaluation_id END) as completed,
                    ROUND(COUNT(DISTINCT CASE WHEN e.status = 'Completed' THEN e.evaluation_id END) / 
                          COUNT(DISTINCT e.evaluation_id) * 100, 2) as response_rate
                FROM subjects s
                JOIN class_sections cs ON s.subject_id = cs.subject_id
                JOIN evaluations e ON cs.section_id = e.section_id
                WHERE e.period_id = %s
                GROUP BY s.subject_id, s.subject_code, s.title
                ORDER BY response_rate DESC
            """, (period_id,))
            
            subject_stats = cursor.fetchall()
            
            # Calculate overall response rate
            total_evals = overall_stats['total_evaluations'] or 0
            completed_evals = overall_stats['completed_evaluations'] or 0
            overall_response_rate = (completed_evals / total_evals * 100) if total_evals > 0 else 0
            
            result = {
                'period_id': period_id,
                'overall_response_rate': round(overall_response_rate, 2),
                'total_evaluations': total_evals,
                'completed_evaluations': completed_evals,
                'in_progress': overall_stats['in_progress'] or 0,
                'pending': overall_stats['pending'] or 0,
                'average_completion_time': round(overall_stats['avg_completion_time'] or 0, 1),
                'faculty_stats': faculty_stats,
                'subject_stats': subject_stats
            }
            
            cursor.close()
            conn.close()
            return result
            
        except Exception as e:
            logger.error(f"Error calculating response analytics: {str(e)}")
            return {}
    
    @staticmethod
    def get_performance_trends(faculty_id: int, periods: int = 5) -> Dict:
        """Get performance trends for a faculty member over multiple periods"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT 
                    fpa.period_id,
                    ep.title as period_title,
                    fpa.overall_score,
                    fpa.response_rate,
                    fpa.average_rating,
                    fpa.performance_grade,
                    fpa.last_calculated
                FROM faculty_performance_analytics fpa
                JOIN evaluation_periods ep ON fpa.period_id = ep.period_id
                WHERE fpa.faculty_id = %s
                ORDER BY ep.start_date DESC
                LIMIT %s
            """, (faculty_id, periods))
            
            trends = cursor.fetchall()
            
            # Calculate trend directions
            if len(trends) >= 2:
                for i in range(len(trends) - 1):
                    current = trends[i]
                    previous = trends[i + 1]
                    
                    # Calculate changes
                    score_change = current['overall_score'] - previous['overall_score']
                    response_change = current['response_rate'] - previous['response_rate']
                    
                    trends[i]['score_change'] = round(score_change, 2)
                    trends[i]['response_change'] = round(response_change, 2)
                    trends[i]['score_trend'] = 'Up' if score_change > 0 else 'Down' if score_change < 0 else 'Stable'
                    trends[i]['response_trend'] = 'Up' if response_change > 0 else 'Down' if response_change < 0 else 'Stable'
            
            cursor.close()
            conn.close()
            return {'trends': trends}
            
        except Exception as e:
            logger.error(f"Error getting performance trends: {str(e)}")
            return {'trends': []}


class AnalyticsScheduler:
    """Handle scheduled analytics calculations"""
    
    @staticmethod
    def calculate_all_faculty_analytics(period_id: int) -> bool:
        """Calculate analytics for all faculty in a given period"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Get all faculty who have evaluations in this period
            cursor.execute("""
                SELECT DISTINCT cs.faculty_id
                FROM class_sections cs
                JOIN evaluations e ON cs.section_id = e.section_id
                WHERE e.period_id = %s
            """, (period_id,))
            
            faculty_list = cursor.fetchall()
            
            success_count = 0
            for faculty in faculty_list:
                faculty_id = faculty['faculty_id']
                
                # Calculate overall analytics
                analytics = FacultyAnalytics.calculate_faculty_performance(faculty_id, period_id)
                if analytics and FacultyAnalytics.save_analytics_to_db(analytics):
                    success_count += 1
                
                # Calculate subject-specific analytics
                cursor.execute("""
                    SELECT DISTINCT cs.subject_id
                    FROM class_sections cs
                    JOIN evaluations e ON cs.section_id = e.section_id
                    WHERE cs.faculty_id = %s AND e.period_id = %s
                """, (faculty_id, period_id))
                
                subjects = cursor.fetchall()
                for subject in subjects:
                    subject_analytics = FacultyAnalytics.calculate_faculty_performance(
                        faculty_id, period_id, subject['subject_id']
                    )
                    if subject_analytics:
                        FacultyAnalytics.save_analytics_to_db(subject_analytics)
            
            cursor.close()
            conn.close()
            
            logger.info(f"Successfully calculated analytics for {success_count}/{len(faculty_list)} faculty members")
            return True
            
        except Exception as e:
            logger.error(f"Error in scheduled analytics calculation: {str(e)}")
            return False