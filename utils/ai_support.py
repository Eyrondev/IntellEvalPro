"""
AI Support Assistant for IntellEvalPro
Uses Google Gemini AI to provide intelligent help and support
"""
import os
import logging
import google.generativeai as genai

# Suppress ALTS credentials warnings from gRPC
logging.getLogger('grpc').setLevel(logging.ERROR)
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GRPC_TRACE'] = ''

# System context for the AI
SYSTEM_CONTEXT = """
You are the IntellEvalPro AI Support Assistant. You help students with questions about the IntellEvalPro Faculty Evaluation System.

**IMPORTANT RULES:**
1. ONLY answer questions related to the IntellEvalPro system, its features, and usage
2. You can understand questions in BOTH English and Tagalog (Filipino)
3. Always respond in English, even if the question is in Tagalog
4. If a question is NOT about IntellEvalPro (in any language), politely respond: "I'm the IntellEvalPro AI Assistant and I can only help with questions about this evaluation system. Please ask me about system features, navigation, evaluations, or troubleshooting."
5. Be helpful, friendly, and concise
6. Use **bold** formatting for important terms
7. Keep responses under 200 words unless detail is absolutely necessary

**LANGUAGE SUPPORT:**
- Understand questions in: English, Tagalog/Filipino
- Always respond in: English
- Example: If asked "Paano mag-submit ng evaluation?", respond in English about how to submit evaluations

**SYSTEM INFORMATION:**

## IntellEvalPro Features:

### Student Dashboard:
- Shows evaluation progress (completed/total with percentage)
- Displays current evaluation period and deadline
- Shows days remaining with color-coded indicators (Red: ≤3 days, Yellow: 4-7 days, Green: >7 days)
- Quick access to pending evaluations

### Pending Evaluations:
- Lists all faculty assigned for evaluation
- Filter options: Department, Course, Section, Status, Search
- "Refresh List" button to update data
- Color-coded urgency indicators
- Shows faculty details: name, course, section, room

### Evaluation Form:
- 5-point rating scale: 5=Strongly Agree (Excellent), 4=Agree (Very Good), 3=Neutral (Satisfactory), 2=Disagree (Needs Improvement), 1=Strongly Disagree (Poor)
- "Save Progress" button to continue later
- All rating fields must be completed before submission
- Optional comments section
- Submit button to finalize (cannot be changed after submission)

### My Evaluations:
- View complete evaluation history
- Shows: Course, Faculty, Evaluation Period, Completion Date, Status
- Filter by: Status, Period, Course, Search
- Statistics: Total, Completed, Pending evaluations

### Evaluation System:
- Completely anonymous (faculty cannot identify who submitted evaluations)
- Two main periods: Mid-term and Final
- Cannot change evaluations after submission
- Deadline enforced (cannot submit after period closes)

### Navigation:
- Sidebar menu with: Dashboard, Pending Evaluations, My Evaluations, Help & Support
- Mobile responsive with hamburger menu
- Active page highlighted in navigation

### Technical:
- Works on desktop, tablet, and mobile devices
- Optimized for touch screens (larger tap targets)
- Supported browsers: Chrome, Firefox, Edge, Safari (latest versions)
- Landscape mode recommended for mobile evaluation forms

### Login/Account:
- Use institutional student credentials
- "Forgot Password" link on login page
- Email-based password reset

### Common Issues:
- Slow performance: Refresh page (F5/Ctrl+R), clear cache, try different browser
- Faculty not showing: Check evaluation period is active, click "Refresh List", verify enrollment
- Form won't submit: Ensure all rating fields complete, check internet connection, try "Save Progress" then refresh
- Missing data: Contact academic office to verify enrollment and assignments

Be concise, helpful, and always remind users that evaluations are anonymous and help improve education quality.
"""

def initialize_gemini():
    """Initialize Gemini AI with API key"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    genai.configure(api_key=api_key)
    # Use Gemini 2.0 Flash (fastest model for analytics)
    return genai.GenerativeModel('gemini-2.0-flash')

def get_ai_response(user_message):
    """
    Get AI response for user message
    
    Args:
        user_message: User's question/message
        
    Returns:
        tuple: (success: bool, response: str)
    """
    try:
        model = initialize_gemini()
        
        # Create the full prompt with system context
        full_prompt = f"{SYSTEM_CONTEXT}\n\nUser Question: {user_message}\n\nAssistant:"
        
        # Generate response
        response = model.generate_content(full_prompt)
        
        if response and response.text:
            return True, response.text.strip()
        else:
            return False, "I couldn't generate a response. Please try again."
            
    except ValueError as ve:
        # API key not configured
        return False, "AI Assistant is not configured. Please contact your administrator."
    except Exception as e:
        print(f"Error generating AI response: {e}")
        return False, "I'm having trouble processing your request. Please try again or check the FAQs above."

def is_system_related_question(user_message):
    """
    Quick check if question seems system-related
    This is a simple filter before calling AI
    
    Args:
        user_message: User's question
        
    Returns:
        bool: True if likely system-related
    """
    # Keywords that suggest system-related questions (English and Tagalog)
    system_keywords = [
        # English keywords
        'evaluation', 'evaluate', 'faculty', 'professor', 'teacher', 'instructor',
        'dashboard', 'login', 'password', 'submit', 'save', 'rating', 'rate',
        'deadline', 'period', 'progress', 'complete', 'pending', 'anonymous',
        'filter', 'search', 'course', 'section', 'how', 'what', 'where', 'when',
        'why', 'help', 'can i', 'unable', 'error', 'problem', 'issue', 'mobile',
        'browser', 'intellevalpro', 'system', 'account', 'navigation', 'menu',
        # Tagalog keywords
        'paano', 'ano', 'saan', 'kailan', 'bakit', 'pano', 'mag-evaluate', 
        'magturo', 'guro', 'propesor', 'mag-login', 'mag-log in', 'password',
        'i-submit', 'isumite', 'mag-submit', 'i-save', 'rating', 'marka',
        'deadline', 'takdang-araw', 'progress', 'pag-unlad', 'tapos', 'nakabitin',
        'naghihintay', 'anonim', 'anonymous', 'kurso', 'subject', 'klase',
        'hindi', 'ayaw', 'error', 'problema', 'mobile', 'browser', 'tulong',
        'help', 'tulungan', 'patulong'
    ]
    
    message_lower = user_message.lower()
    return any(keyword in message_lower for keyword in system_keywords)


# ================================
# AI ANALYTICS FUNCTIONS
# ================================

def generate_performance_trend_insight(trends_data, metrics, advanced_mode=False):
    """Generate AI insight for performance trends - Standard or Advanced mode"""
    try:
        if not trends_data or len(trends_data) < 2:
            return "Insufficient data for trend analysis. Need at least 2 evaluation periods."
        
        # Calculate key metrics
        latest_rating = float(trends_data[-1]['avg_rating']) if trends_data[-1]['avg_rating'] else 0
        previous_rating = float(trends_data[-2]['avg_rating']) if trends_data[-2]['avg_rating'] else 0
        first_rating = float(trends_data[0]['avg_rating']) if trends_data[0]['avg_rating'] else 0
        change = latest_rating - previous_rating
        overall_change = latest_rating - first_rating
        
        # Get all ratings for trend analysis
        all_ratings = [float(t['avg_rating']) for t in trends_data if t['avg_rating']]
        avg_rating = sum(all_ratings) / len(all_ratings) if all_ratings else 0
        
        if advanced_mode:
            # Advanced mode: Comprehensive deep analysis
            prompt = f"""
            Conduct a comprehensive performance trend analysis for this faculty member:
            
            **Performance Data:**
            - Total evaluation periods: {len(trends_data)}
            - Current rating: {latest_rating:.2f}
            - Previous rating: {previous_rating:.2f}
            - First rating: {first_rating:.2f}
            - Recent change: {change:+.2f}
            - Overall change: {overall_change:+.2f}
            - Average across all periods: {avg_rating:.2f}
            - Highest rating: {max(all_ratings):.2f}
            - Lowest rating: {min(all_ratings):.2f}
            
            **Required Analysis (4-6 paragraphs):**
            
            1. **Trend Assessment:** Analyze the overall trajectory (improving, declining, stable). Identify any significant patterns or inflection points.
            
            2. **Root Cause Analysis:** What factors might explain the observed trends? Consider teaching methods, student expectations, course difficulty, external factors.
            
            3. **Performance Benchmarking:** How does this trend compare to institutional standards? Rate performance as Outstanding (≥4.50), Highly Satisfactory (3.50-4.49), Satisfactory (2.50-3.49), or Needs Improvement (<2.50).
            
            4. **Predictive Insights:** Based on current trends, what is the likely trajectory for the next evaluation period? Identify early warning signs or positive momentum indicators.
            
            5. **Strategic Recommendations:** Provide 3-5 specific, actionable recommendations with expected outcomes. Include both immediate actions and long-term strategies.
            
            6. **Support Resources:** Suggest specific professional development opportunities, mentoring strategies, or institutional support programs that would be most beneficial.
            
            Use professional academic language suitable for institutional reporting. Be specific and data-driven.
            """
        else:
            # Standard mode: Quick, concise analysis
            prompt = f"""
            Quick analysis: Faculty performance {latest_rating:.2f} (current) vs {previous_rating:.2f} (previous). 
            Change: {change:+.2f}. Overall trend across {len(trends_data)} periods: {overall_change:+.2f} from start.
            Provide 2-3 concise sentences: trend assessment + actionable insight + recommendation.
            """
        
        model = initialize_gemini()
        response = model.generate_content(prompt)
        
        return response.text.strip() if response and response.text else f"Faculty performance {'improved' if change > 0 else 'declined'} by {abs(change):.2f} points. {'Continue current initiatives' if change > 0 else 'Implement targeted support programs'}."
        
    except Exception as e:
        print(f"Error generating performance trend insight: {e}")
        return "Overall faculty performance shows consistent patterns across evaluation periods with opportunities for targeted improvement."


def generate_comparison_insight(comparison_data, top_faculty, bottom_faculty, advanced_mode=False):
    """Generate AI insight for faculty comparison - Standard or Advanced mode"""
    try:
        if not comparison_data:
            return "No comparison data available for analysis."
        
        # Quick statistical analysis
        top_count = len(top_faculty)
        bottom_count = len(bottom_faculty)
        total_count = len(comparison_data)
        avg_rating = sum(float(f['avg_rating']) for f in comparison_data if f.get('avg_rating')) / total_count if total_count > 0 else 0
        
        if advanced_mode:
            # Advanced mode: Comprehensive comparative analysis
            top_avg = sum(float(f['avg_rating']) for f in top_faculty) / top_count if top_count > 0 else 0
            bottom_avg = sum(float(f['avg_rating']) for f in bottom_faculty) / bottom_count if bottom_count > 0 else 0
            performance_gap = top_avg - bottom_avg if top_count > 0 and bottom_count > 0 else 0
            
            prompt = f"""
            Conduct comprehensive faculty comparison analysis:
            
            **Performance Distribution:**
            - Total faculty analyzed: {total_count}
            - Top performers (≥4.50): {top_count} faculty (avg: {top_avg:.2f})
            - Need support (<3.50): {bottom_count} faculty (avg: {bottom_avg:.2f})
            - Overall department average: {avg_rating:.2f}
            - Performance gap: {performance_gap:.2f} points
            
            **Required Analysis (4-5 paragraphs):**
            
            1. **Distribution Analysis:** Assess the overall performance distribution. Is it balanced, skewed, or polarized? What does this reveal about department health?
            
            2. **Excellence Factors:** Analyze characteristics of top performers. What teaching strategies, engagement methods, or approaches distinguish high-performing faculty?
            
            3. **Support Needs:** Identify patterns among faculty needing support. Are there common challenges, specific criteria, or departmental factors affecting performance?
            
            4. **Equity & Fairness:** Consider if evaluation criteria are applied consistently. Are there structural factors affecting certain faculty groups?
            
            5. **Strategic Recommendations:** Provide specific actions for:
               - Recognizing and retaining top performers
               - Peer mentoring programs pairing strong with developing faculty
               - Targeted professional development initiatives
               - Resource allocation priorities
               - Timeline for improvement assessment
            
            Use data-driven insights with specific, actionable recommendations.
            """
        else:
            # Standard mode: Quick analysis
            prompt = f"""
            Faculty stats: {total_count} total, {top_count} top performers, {bottom_count} need support. Overall avg: {avg_rating:.2f}.
            Provide 2-3 sentences: performance distribution assessment + key recommendation.
            """
        
        model = initialize_gemini()
        response = model.generate_content(prompt)
        
        return response.text.strip() if response and response.text else f"Top {top_count} faculty maintain excellent performance above 4.5, while {bottom_count} faculty show potential for targeted development support."
        
    except Exception as e:
        print(f"Error generating comparison insight: {e}")
        return f"Faculty performance analysis shows {top_count} excellent performers eligible for recognition and {bottom_count} faculty who would benefit from additional support."


def generate_question_analysis_insight(question_data, advanced_mode=False):
    """Generate AI insight for question analysis - Standard or Advanced mode"""
    try:
        if not question_data:
            return "No question performance data available for analysis."
        
        # Updated score analysis based on new rating scale
        outstanding_questions = [q for q in question_data if float(q['avg_score']) >= 4.50]
        highly_satisfactory = [q for q in question_data if 3.50 <= float(q['avg_score']) < 4.50]
        satisfactory = [q for q in question_data if 2.50 <= float(q['avg_score']) < 3.50]
        needs_improvement = [q for q in question_data if 1.50 <= float(q['avg_score']) < 2.50]
        poor_questions = [q for q in question_data if float(q['avg_score']) < 1.50]
        
        if advanced_mode:
            # Advanced mode: Deep questionnaire analysis
            total_questions = len(question_data)
            avg_score = sum(float(q['avg_score']) for q in question_data) / total_questions if total_questions > 0 else 0
            
            # Identify highest and lowest performing questions
            sorted_questions = sorted(question_data, key=lambda x: float(x['avg_score']), reverse=True)
            top_question = sorted_questions[0] if sorted_questions else None
            bottom_question = sorted_questions[-1] if sorted_questions else None
            
            prompt = f"""
            Conduct comprehensive questionnaire performance analysis:
            
            **Performance Distribution:**
            - Total evaluation criteria: {total_questions}
            - Outstanding (≥4.50): {len(outstanding_questions)} criteria
            - Highly Satisfactory (3.50-4.49): {len(highly_satisfactory)} criteria
            - Satisfactory (2.50-3.49): {len(satisfactory)} criteria
            - Needs Improvement (1.50-2.49): {len(needs_improvement)} criteria
            - Poor (<1.50): {len(poor_questions)} criteria
            - Overall average score: {avg_score:.2f}
            
            **Top Criterion:** {top_question['question_text'][:100] if top_question else 'N/A'} (Score: {float(top_question['avg_score']):.2f})
            **Lowest Criterion:** {bottom_question['question_text'][:100] if bottom_question else 'N/A'} (Score: {float(bottom_question['avg_score']):.2f})
            
            **Required Analysis (4-5 paragraphs):**
            
            1. **Strengths Assessment:** Analyze the {len(outstanding_questions)} outstanding criteria. What teaching competencies are faculty excelling in?
            
            2. **Development Areas:** Deep dive into the {len(needs_improvement) + len(poor_questions)} criteria needing attention. Identify common themes and skill gaps.
            
            3. **Competency Mapping:** Map question performance to pedagogical competency areas (content mastery, student engagement, assessment methods, communication).
            
            4. **Root Cause Analysis:** Why might certain criteria consistently score lower? Consider training gaps or evaluation design issues.
            
            5. **Professional Development Strategy:** Design specific training modules targeting the identified weak areas with expected outcomes and timeline.
            
            Provide actionable, evidence-based recommendations for curriculum and faculty development.
            """
        else:
            # Standard mode: Quick analysis
            prompt = f"""
            Quick analysis: {len(outstanding_questions)} outstanding, {len(highly_satisfactory)} highly satisfactory, {len(needs_improvement + poor_questions)} need attention.
            Provide 2-3 sentences: key finding + development focus.
            """
        
        model = initialize_gemini()
        response = model.generate_content(prompt)
        
        return response.text.strip() if response and response.text else f"Question analysis reveals {len(outstanding_questions)} outstanding areas and {len(needs_improvement + poor_questions)} areas requiring focused faculty development efforts."
        
    except Exception as e:
        print(f"Error generating question analysis insight: {e}")
        return f"Questionnaire analysis shows {len(outstanding_questions)} high-performing criteria and {len(needs_improvement + poor_questions)} areas where faculty development programs could provide significant improvement."


def generate_engagement_insight(engagement_data, stats, advanced_mode=False):
    """Generate AI insight for student engagement - Standard or Advanced mode"""
    try:
        if not engagement_data:
            return "No engagement data available for analysis."
        
        # Quick engagement stats
        high_count = len([e for e in engagement_data if e['engagement_rate'] >= 85])
        medium_count = len([e for e in engagement_data if 70 <= e['engagement_rate'] < 85])
        low_count = len([e for e in engagement_data if e['engagement_rate'] < 70])
        total_count = len(engagement_data)
        
        if advanced_mode:
            # Advanced mode: Comprehensive engagement analysis
            avg_engagement = stats.get('overall_engagement', 'N/A')
            
            # Calculate engagement distribution
            very_high = len([e for e in engagement_data if e['engagement_rate'] >= 90])
            critical_low = len([e for e in engagement_data if e['engagement_rate'] < 60])
            
            prompt = f"""
            Conduct comprehensive student engagement analysis:
            
            **Engagement Distribution:**
            - Total classes analyzed: {total_count}
            - Very High engagement (≥90%): {very_high} classes
            - High engagement (85-89%): {high_count - very_high} classes
            - Medium engagement (70-84%): {medium_count} classes
            - Low engagement (60-69%): {low_count - critical_low} classes
            - Critical low (<60%): {critical_low} classes
            - Overall average: {avg_engagement}
            
            **Required Analysis (4-5 paragraphs):**
            
            1. **Engagement Pattern Assessment:** Analyze the distribution of student participation. Is engagement generally strong, declining, or inconsistent? What trends emerge?
            
            2. **High Engagement Analysis:** Examine the {very_high + high_count} high-performing classes. What factors contribute to strong student participation? Consider:
               - Communication strategies used
               - Evaluation timing and reminders
               - Faculty-student relationships
               - Course characteristics (difficulty, interest level)
            
            3. **Low Engagement Root Causes:** Deep dive into the {low_count} classes with below-target engagement. Identify barriers:
               - Student awareness and motivation
               - Technical access issues
               - Evaluation fatigue
               - Timing conflicts
               - Perceived value of evaluations
            
            4. **Predictive Insights:** What does current engagement predict for future evaluation cycles? Identify early warning signs for declining participation.
            
            5. **Strategic Improvement Plan:** Provide specific, actionable recommendations:
               - Multi-channel communication strategy (email, SMS, in-class announcements)
               - Optimal timing for evaluation windows
               - Incentive structures to boost participation
               - Faculty role in encouraging completion
               - Mobile accessibility improvements
               - Expected engagement targets and timeline for improvement
            
            Focus on practical, evidence-based strategies to increase student participation rates.
            """
        else:
            # Standard mode: Quick analysis
            prompt = f"""
            Engagement stats: {high_count} high (≥85%), {low_count} low (<70%), avg {stats.get('overall_engagement', 'N/A')}.
            Provide 2-3 sentences: assessment + improvement strategy.
            """
        
        model = initialize_gemini()
        response = model.generate_content(prompt)
        
        return response.text.strip() if response and response.text else f"Student engagement shows {high_count} classes with excellent participation while {low_count} classes may benefit from improved communication strategies."
        
    except Exception as e:
        print(f"Error generating engagement insight: {e}")
        return f"Engagement analysis indicates {stats.get('overall_engagement', 'N/A')} average participation with {low_count} classes requiring attention to improve response rates."


def generate_improvement_opportunities_insight(improvement_data, advanced_mode=False):
    """Generate AI insight for improvement opportunities - Standard or Advanced mode"""
    try:
        if not improvement_data:
            return "No improvement opportunities identified at this time."
        
        # Updated analysis based on new rating scale
        faculty_count = len(set(item['faculty_name'] for item in improvement_data))
        critical_count = len([item for item in improvement_data if item['avg_score'] < 2.50])  # Below Satisfactory
        needs_attention = len([item for item in improvement_data if item['avg_score'] < 3.50])  # Below Highly Satisfactory
        moderate_count = len([item for item in improvement_data if 2.50 <= item['avg_score'] < 3.50])  # Satisfactory
        
        if advanced_mode:
            # Advanced mode: Comprehensive improvement planning
            total_areas = len(improvement_data)
            avg_score = sum(item['avg_score'] for item in improvement_data) / total_areas if total_areas > 0 else 0
            
            # Group by faculty for deeper analysis
            faculty_data = {}
            for item in improvement_data:
                faculty_name = item['faculty_name']
                if faculty_name not in faculty_data:
                    faculty_data[faculty_name] = []
                faculty_data[faculty_name].append(item)
            
            # Find faculty with most improvement needs
            faculty_with_most_needs = max(faculty_data.keys(), key=lambda f: len(faculty_data[f])) if faculty_data else 'N/A'
            most_needs_count = len(faculty_data[faculty_with_most_needs]) if faculty_with_most_needs != 'N/A' else 0
            
            prompt = f"""
            Conduct comprehensive improvement opportunities analysis:
            
            **Performance Gap Analysis:**
            - Faculty members needing support: {faculty_count}
            - Total improvement areas identified: {total_areas}
            - Critical priority (score <2.50): {critical_count} areas
            - Moderate priority (2.50-3.49): {moderate_count} areas
            - Average score of improvement areas: {avg_score:.2f}
            - Faculty with most needs: {faculty_with_most_needs} ({most_needs_count} areas)
            
            **Improvement Areas Breakdown:**
            {chr(10).join([f"- {item['faculty_name']}: {item['criterion']} (Score: {item['avg_score']:.2f})" for item in improvement_data[:5]])}
            
            **Required Analysis (5-6 paragraphs):**
            
            1. **Priority Assessment:** Categorize the {total_areas} improvement needs by urgency and impact. Which require immediate intervention vs. long-term development?
            
            2. **Pattern Recognition:** Analyze common themes across the {faculty_count} faculty members. Are there:
               - Systemic issues affecting multiple faculty?
               - Specific competency gaps (e.g., assessment methods, student engagement)?
               - Department-specific challenges?
               - New faculty vs. veteran faculty patterns?
            
            3. **Root Cause Deep Dive:** For the {critical_count} critical areas, investigate underlying causes:
               - Lack of training or resources?
               - Unclear institutional expectations?
               - Misalignment between teaching style and student needs?
               - External factors (large class sizes, difficult subjects)?
            
            4. **Individualized Development Plans:** For each faculty member, recommend:
               - Top 3 priority areas for immediate focus
               - Specific training workshops or programs
               - Peer mentoring pairings (match with high performers in weak areas)
               - Timeline for improvement (30-day, 60-day, semester goals)
               - Success metrics and reassessment schedule
            
            5. **Institutional Support Framework:** Design comprehensive support system:
               - Professional development workshops (schedule, topics, facilitators)
               - One-on-one coaching sessions
               - Classroom observation and feedback programs
               - Resource allocation (teaching materials, technology, teaching assistants)
               - Recognition for improvement progress
            
            6. **Expected Outcomes & Monitoring:** Define measurable success criteria:
               - Target performance levels (move all below 2.50 to at least 3.00)
               - Timeline for achieving targets
               - Monitoring checkpoints (monthly reviews, mid-semester assessments)
               - Escalation procedures if improvement stalls
            
            Provide a detailed, actionable roadmap for systematic faculty development.
            """
        else:
            # Standard mode: Quick assessment
            prompt = f"""
            Quick assessment: {faculty_count} faculty need support, {critical_count} critical (below satisfactory), {needs_attention} total needing attention.
            Provide 2-3 sentences: priority focus + recommended action.
            """
        
        model = initialize_gemini()
        response = model.generate_content(prompt)
        
        return response.text.strip() if response and response.text else f"Analysis identifies {faculty_count} faculty members who would benefit from targeted professional development, with immediate focus on {critical_count} critical performance gaps below satisfactory level."
        
    except Exception as e:
        print(f"Error generating improvement insight: {e}")
        return f"Improvement opportunities indicate {faculty_count} faculty members would benefit from focused professional development support, particularly {critical_count} in critical need areas."


def generate_comprehensive_training_plan():
    """Generate comprehensive training plan using AI"""
    try:
        prompt = """
        Generate a comprehensive faculty training plan for Norzagaray College based on evaluation analytics.
        
        Create a structured training program including:
        1. Training Modules (4-6 modules)
        2. Timeline (semester-based)
        3. Target Audiences
        4. Learning Objectives
        5. Assessment Methods
        6. Resource Requirements
        
        Focus on common faculty development areas:
        - Student Engagement Techniques
        - Feedback and Assessment Strategies  
        - Classroom Management
        - Technology Integration
        - Communication Skills
        - Inclusive Teaching Practices
        
        Format as professional academic document suitable for college administration.
        Use bullet points and clear structure.
        """
        
        model = initialize_gemini()
        response = model.generate_content(prompt)
        
        return response.text.strip() if response and response.text else """
        <h4>Faculty Development Training Plan</h4>
        <p><strong>Module 1:</strong> Student Engagement Enhancement</p>
        <p><strong>Module 2:</strong> Effective Feedback Strategies</p>
        <p><strong>Module 3:</strong> Classroom Communication Skills</p>
        <p><strong>Module 4:</strong> Assessment and Evaluation Methods</p>
        <p><strong>Timeline:</strong> Implementation over 2 semesters with monthly sessions</p>
        """
        
    except Exception as e:
        print(f"Error generating training plan: {e}")
        return "Comprehensive faculty training plan focusing on student engagement, assessment strategies, and professional development will be generated and distributed to relevant departments."
