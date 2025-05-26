from flask import Flask, request, render_template
from PyPDF2 import PdfReader
import re
from anthropic import Anthropic
from dotenv import load_dotenv
import os
import google.generativeai as genai
from openai import OpenAI
from werkzeug.utils import secure_filename
import json
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Check for required API keys
if not os.getenv('OPENAI_API_KEY'):
    raise ValueError("OPENAI_API_KEY environment variable is not set")
if not os.getenv('GOOGLE_API_KEY'):
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

# Configure Google Generative AI
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

app = Flask(__name__)

# Clean resume==========================================================================================================
def cleanResume(txt):
    cleanText = re.sub('http\S+\s', ' ', txt)
    cleanText = re.sub('RT|cc', ' ', cleanText)
    cleanText = re.sub('#\S+\s', ' ', cleanText)
    cleanText = re.sub('@\S+', '  ', cleanText)
    cleanText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
    cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText)
    cleanText = re.sub('\s+', ' ', cleanText)
    return cleanText

def pdf_to_text(file):
    reader = PdfReader(file)
    text = ''
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text




# resume parsing
import re

def extract_contact_number_from_resume(text):
    contact_number = None

    # Use regex pattern to find a potential contact number
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    if match:
        contact_number = match.group()

    return contact_number
def extract_email_from_resume(text):
    email = None

    # Use regex pattern to find a potential email address
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    if match:
        email = match.group()

    return email

def extract_skills_from_resume(text):
    # List of predefined skills
    skills_list = [
        'Python', 'Data Analysis', 'Machine Learning', 'Communication', 'Project Management', 'Deep Learning', 'SQL',
        'Tableau',
        'Java', 'C++', 'JavaScript', 'HTML', 'CSS', 'React', 'Angular', 'Node.js', 'MongoDB', 'Express.js', 'Git',
        'Research', 'Statistics', 'Quantitative Analysis', 'Qualitative Analysis', 'SPSS', 'R', 'Data Visualization',
        'Matplotlib',
        'Seaborn', 'Plotly', 'Pandas', 'Numpy', 'Scikit-learn', 'TensorFlow', 'Keras', 'PyTorch', 'NLTK', 'Text Mining',
        'Natural Language Processing', 'Computer Vision', 'Image Processing', 'OCR', 'Speech Recognition',
        'Recommendation Systems',
        'Collaborative Filtering', 'Content-Based Filtering', 'Reinforcement Learning', 'Neural Networks',
        'Convolutional Neural Networks',
        'Recurrent Neural Networks', 'Generative Adversarial Networks', 'XGBoost', 'Random Forest', 'Decision Trees',
        'Support Vector Machines',
        'Linear Regression', 'Logistic Regression', 'K-Means Clustering', 'Hierarchical Clustering', 'DBSCAN',
        'Association Rule Learning',
        'Apache Hadoop', 'Apache Spark', 'MapReduce', 'Hive', 'HBase', 'Apache Kafka', 'Data Warehousing', 'ETL',
        'Big Data Analytics',
        'Cloud Computing', 'Amazon Web Services (AWS)', 'Microsoft Azure', 'Google Cloud Platform (GCP)', 'Docker',
        'Kubernetes', 'Linux',
        'Shell Scripting', 'Cybersecurity', 'Network Security', 'Penetration Testing', 'Firewalls', 'Encryption',
        'Malware Analysis',
        'Digital Forensics', 'CI/CD', 'DevOps', 'Agile Methodology', 'Scrum', 'Kanban', 'Continuous Integration',
        'Continuous Deployment',
        'Software Development', 'Web Development', 'Mobile Development', 'Backend Development', 'Frontend Development',
        'Full-Stack Development',
        'UI/UX Design', 'Responsive Design', 'Wireframing', 'Prototyping', 'User Testing', 'Adobe Creative Suite',
        'Photoshop', 'Illustrator',
        'InDesign', 'Figma', 'Sketch', 'Zeplin', 'InVision', 'Product Management', 'Market Research',
        'Customer Development', 'Lean Startup',
        'Business Development', 'Sales', 'Marketing', 'Content Marketing', 'Social Media Marketing', 'Email Marketing',
        'SEO', 'SEM', 'PPC',
        'Google Analytics', 'Facebook Ads', 'LinkedIn Ads', 'Lead Generation', 'Customer Relationship Management (CRM)',
        'Salesforce',
        'HubSpot', 'Zendesk', 'Intercom', 'Customer Support', 'Technical Support', 'Troubleshooting',
        'Ticketing Systems', 'ServiceNow',
        'ITIL', 'Quality Assurance', 'Manual Testing', 'Automated Testing', 'Selenium', 'JUnit', 'Load Testing',
        'Performance Testing',
        'Regression Testing', 'Black Box Testing', 'White Box Testing', 'API Testing', 'Mobile Testing',
        'Usability Testing', 'Accessibility Testing',
        'Cross-Browser Testing', 'Agile Testing', 'User Acceptance Testing', 'Software Documentation',
        'Technical Writing', 'Copywriting',
        'Editing', 'Proofreading', 'Content Management Systems (CMS)', 'WordPress', 'Joomla', 'Drupal', 'Magento',
        'Shopify', 'E-commerce',
        'Payment Gateways', 'Inventory Management', 'Supply Chain Management', 'Logistics', 'Procurement',
        'ERP Systems', 'SAP', 'Oracle',
        'Microsoft Dynamics', 'Tableau', 'Power BI', 'QlikView', 'Looker', 'Data Warehousing', 'ETL',
        'Data Engineering', 'Data Governance',
        'Data Quality', 'Master Data Management', 'Predictive Analytics', 'Prescriptive Analytics',
        'Descriptive Analytics', 'Business Intelligence',
        'Dashboarding', 'Reporting', 'Data Mining', 'Web Scraping', 'API Integration', 'RESTful APIs', 'GraphQL',
        'SOAP', 'Microservices',
        'Serverless Architecture', 'Lambda Functions', 'Event-Driven Architecture', 'Message Queues', 'GraphQL',
        'Socket.io', 'WebSockets'
                     'Ruby', 'Ruby on Rails', 'PHP', 'Symfony', 'Laravel', 'CakePHP', 'Zend Framework', 'ASP.NET', 'C#',
        'VB.NET', 'ASP.NET MVC', 'Entity Framework',
        'Spring', 'Hibernate', 'Struts', 'Kotlin', 'Swift', 'Objective-C', 'iOS Development', 'Android Development',
        'Flutter', 'React Native', 'Ionic',
        'Mobile UI/UX Design', 'Material Design', 'SwiftUI', 'RxJava', 'RxSwift', 'Django', 'Flask', 'FastAPI',
        'Falcon', 'Tornado', 'WebSockets',
        'GraphQL', 'RESTful Web Services', 'SOAP', 'Microservices Architecture', 'Serverless Computing', 'AWS Lambda',
        'Google Cloud Functions',
        'Azure Functions', 'Server Administration', 'System Administration', 'Network Administration',
        'Database Administration', 'MySQL', 'PostgreSQL',
        'SQLite', 'Microsoft SQL Server', 'Oracle Database', 'NoSQL', 'MongoDB', 'Cassandra', 'Redis', 'Elasticsearch',
        'Firebase', 'Google Analytics',
        'Google Tag Manager', 'Adobe Analytics', 'Marketing Automation', 'Customer Data Platforms', 'Segment',
        'Salesforce Marketing Cloud', 'HubSpot CRM',
        'Zapier', 'IFTTT', 'Workflow Automation', 'Robotic Process Automation (RPA)', 'UI Automation',
        'Natural Language Generation (NLG)',
        'Virtual Reality (VR)', 'Augmented Reality (AR)', 'Mixed Reality (MR)', 'Unity', 'Unreal Engine', '3D Modeling',
        'Animation', 'Motion Graphics',
        'Game Design', 'Game Development', 'Level Design', 'Unity3D', 'Unreal Engine 4', 'Blender', 'Maya',
        'Adobe After Effects', 'Adobe Premiere Pro',
        'Final Cut Pro', 'Video Editing', 'Audio Editing', 'Sound Design', 'Music Production', 'Digital Marketing',
        'Content Strategy', 'Conversion Rate Optimization (CRO)',
        'A/B Testing', 'Customer Experience (CX)', 'User Experience (UX)', 'User Interface (UI)', 'Persona Development',
        'User Journey Mapping', 'Information Architecture (IA)',
        'Wireframing', 'Prototyping', 'Usability Testing', 'Accessibility Compliance', 'Internationalization (I18n)',
        'Localization (L10n)', 'Voice User Interface (VUI)',
        'Chatbots', 'Natural Language Understanding (NLU)', 'Speech Synthesis', 'Emotion Detection',
        'Sentiment Analysis', 'Image Recognition', 'Object Detection',
        'Facial Recognition', 'Gesture Recognition', 'Document Recognition', 'Fraud Detection',
        'Cyber Threat Intelligence', 'Security Information and Event Management (SIEM)',
        'Vulnerability Assessment', 'Incident Response', 'Forensic Analysis', 'Security Operations Center (SOC)',
        'Identity and Access Management (IAM)', 'Single Sign-On (SSO)',
        'Multi-Factor Authentication (MFA)', 'Blockchain', 'Cryptocurrency', 'Decentralized Finance (DeFi)',
        'Smart Contracts', 'Web3', 'Non-Fungible Tokens (NFTs)']


    skills = []

    for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            skills.append(skill)

    return skills


def extract_education_from_resume(text):
    education = []

    # List of education keywords to match against
    education_keywords = [
        'Computer Science', 'Information Technology', 'Software Engineering', 'Electrical Engineering', 'Mechanical Engineering', 'Civil Engineering',
        'Chemical Engineering', 'Biomedical Engineering', 'Aerospace Engineering', 'Nuclear Engineering', 'Industrial Engineering', 'Systems Engineering',
        'Environmental Engineering', 'Petroleum Engineering', 'Geological Engineering', 'Marine Engineering', 'Robotics Engineering', 'Biotechnology',
        'Biochemistry', 'Microbiology', 'Genetics', 'Molecular Biology', 'Bioinformatics', 'Neuroscience', 'Biophysics', 'Biostatistics', 'Pharmacology',
        'Physiology', 'Anatomy', 'Pathology', 'Immunology', 'Epidemiology', 'Public Health', 'Health Administration', 'Nursing', 'Medicine', 'Dentistry',
        'Pharmacy', 'Veterinary Medicine', 'Medical Technology', 'Radiography', 'Physical Therapy', 'Occupational Therapy', 'Speech Therapy', 'Nutrition',
        'Sports Science', 'Kinesiology', 'Exercise Physiology', 'Sports Medicine', 'Rehabilitation Science', 'Psychology', 'Counseling', 'Social Work',
        'Sociology', 'Anthropology', 'Criminal Justice', 'Political Science', 'International Relations', 'Economics', 'Finance', 'Accounting', 'Business Administration',
        'Management', 'Marketing', 'Entrepreneurship', 'Hospitality Management', 'Tourism Management', 'Supply Chain Management', 'Logistics Management',
        'Operations Management', 'Human Resource Management', 'Organizational Behavior', 'Project Management', 'Quality Management', 'Risk Management',
        'Strategic Management', 'Public Administration', 'Urban Planning', 'Architecture', 'Interior Design', 'Landscape Architecture', 'Fine Arts',
        'Visual Arts', 'Graphic Design', 'Fashion Design', 'Industrial Design', 'Product Design', 'Animation', 'Film Studies', 'Media Studies',
        'Communication Studies', 'Journalism', 'Broadcasting', 'Creative Writing', 'English Literature', 'Linguistics', 'Translation Studies',
        'Foreign Languages', 'Modern Languages', 'Classical Studies', 'History', 'Archaeology', 'Philosophy', 'Theology', 'Religious Studies',
        'Ethics', 'Education', 'Early Childhood Education', 'Elementary Education', 'Secondary Education', 'Special Education', 'Higher Education',
        'Adult Education', 'Distance Education', 'Online Education', 'Instructional Design', 'Curriculum Development'
        'Library Science', 'Information Science', 'Computer Engineering', 'Software Development', 'Cybersecurity', 'Information Security',
        'Network Engineering', 'Data Science', 'Data Analytics', 'Business Analytics', 'Operations Research', 'Decision Sciences',
        'Human-Computer Interaction', 'User Experience Design', 'User Interface Design', 'Digital Marketing', 'Content Strategy',
        'Brand Management', 'Public Relations', 'Corporate Communications', 'Media Production', 'Digital Media', 'Web Development',
        'Mobile App Development', 'Game Development', 'Virtual Reality', 'Augmented Reality', 'Blockchain Technology', 'Cryptocurrency',
        'Digital Forensics', 'Forensic Science', 'Criminalistics', 'Crime Scene Investigation', 'Emergency Management', 'Fire Science',
        'Environmental Science', 'Climate Science', 'Meteorology', 'Geography', 'Geomatics', 'Remote Sensing', 'Geoinformatics',
        'Cartography', 'GIS (Geographic Information Systems)', 'Environmental Management', 'Sustainability Studies', 'Renewable Energy',
        'Green Technology', 'Ecology', 'Conservation Biology', 'Wildlife Biology', 'Zoology']

    for keyword in education_keywords:
        pattern = r"(?i)\b{}\b".format(re.escape(keyword))
        match = re.search(pattern, text)
        if match:
            education.append(match.group())

    return education

def extract_name_from_resume(text):
    name = None

    # Use regex pattern to find a potential name
    pattern = r"(\b[A-Z][a-z]+\b)\s(\b[A-Z][a-z]+\b)"
    match = re.search(pattern, text)
    if match:
        name = match.group()

    return name




# routes===============================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resume')
def resume():
    return render_template("resume.html")

@app.route('/pred', methods=['POST'])
def pred():
    if 'resume' not in request.files:
        return render_template('resume.html', message="No resume file uploaded.")
    
    file = request.files['resume']
    if file.filename == '':
        return render_template('resume.html', message="No selected file.")
        
    interests = request.form.get('interests', '').strip()
    if not interests:
        return render_template('resume.html', message="Please provide your interests.")
    
    try:
        filename = secure_filename(file.filename)
        if filename.endswith('.pdf'):
            resume_text = pdf_to_text(file)
        elif filename.endswith('.txt'):
            resume_text = file.read().decode('utf-8')
        else:
            return render_template('resume.html', message="Invalid file format. Please upload a PDF or TXT file.")

        if not resume_text.strip():
            return render_template('resume.html', message="The resume appears to be empty. Please check the file content.")

        # Extract info
        phone = extract_contact_number_from_resume(resume_text)
        email = extract_email_from_resume(resume_text)
        extracted_skills = extract_skills_from_resume(resume_text)
        extracted_education = extract_education_from_resume(resume_text)
        name = extract_name_from_resume(resume_text)

        # Get structured career recommendations
        try:
            match_score, career_recs, feedback = analyze_resume_match(resume_text, interests)
            
            # Log successful analysis
            app.logger.info(f"Successfully analyzed resume for {name if name else 'unnamed user'}")
            
            return render_template(
                'results.html', 
                match_score=match_score,
                career_recommendations=career_recs,
                feedback=feedback,
                phone=phone,
                name=name,
                email=email,
                extracted_skills=extracted_skills,
                extracted_education=extracted_education,
                message=None  # Clear any error messages
            )
        except Exception as e:
            app.logger.error(f"Error in analyze_resume_match: {str(e)}")
            return render_template('resume.html', message=f"Error analyzing resume: {str(e)}")

    except Exception as e:
        app.logger.error(f"Error processing resume: {str(e)}")
        return render_template('resume.html', message=f"Error processing resume: {str(e)}")

def analyze_resume_match(resume_text, interests):
    # Ask OpenAI to return only JSON with these keys: match_score, career_recommendations, and overall_feedback
    prompt = f"""
You are an expert career counselor and talent advisor. Based on the resume and interests below, provide career recommendations in the following JSON format:
{{
    "match_score": "85%",
    "career_recommendations": [
        {{
            "career_name": "Example Career 1",
            "description": "Brief description of the career path",
            "entry_level": "Entry level position and salary range",
            "mid_level": "Mid level position and salary range",
            "senior_level": "Senior level position and salary range",
            "required_skills": ["Skill 1", "Skill 2", "Skill 3"]
        }},
        // 2 more similar career recommendation objects
    ],
    "overall_feedback": "Detailed feedback about the candidate's profile"
}}

Resume:
{resume_text}

Candidate's Interests:
{interests}

Provide exactly 3 career recommendations. Return ONLY the JSON object, no other text.
"""

    try:
        # Call OpenAI with your existing configuration
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert career counselor. Always return valid JSON with exactly 3 career recommendations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000  # Increased token limit for more detailed responses
        )

        content = response.choices[0].message.content.strip()
        
        # Log the raw response for debugging
        app.logger.info(f"OpenAI API Response: {content}")

        try:
            # Parse the JSON response
            data = json.loads(content)
            
            # Ensure we have all required fields with default values if missing
            match_score = data.get("match_score", "70%")  # Default score if missing
            career_recommendations = data.get("career_recommendations", [])
            overall_feedback = data.get("overall_feedback", "Based on your resume and interests, here are some career recommendations.")

            # Ensure we have exactly 3 career recommendations
            if not career_recommendations or len(career_recommendations) == 0:
                # Create default recommendation if none provided
                career_recommendations = [{
                    "career_name": "Data Analyst",
                    "description": "Entry-level data analysis role focusing on business insights",
                    "entry_level": "Junior Data Analyst ($50,000 - $65,000)",
                    "mid_level": "Senior Data Analyst ($65,000 - $85,000)",
                    "senior_level": "Lead Data Analyst ($85,000 - $120,000)",
                    "required_skills": ["Python", "SQL", "Data Visualization", "Statistics"]
                }]

            # Log successful parsing
            app.logger.info(f"Successfully parsed career recommendations. Found {len(career_recommendations)} recommendations.")

            return match_score, career_recommendations, overall_feedback

        except json.JSONDecodeError as e:
            app.logger.error(f"JSON parsing error: {str(e)}")
            app.logger.error(f"Problematic content: {content}")
            raise Exception("Error parsing career recommendations. Please try again.")

    except Exception as e:
        app.logger.error(f"Error in analyze_resume_match: {str(e)}")
        raise Exception(f"Error analyzing resume: {str(e)}")

@app.route('/bulk-resume')
def bulk_resume():
    return render_template('bulk_resume.html')

@app.route('/bulk-analyze', methods=['POST'])
def bulk_analyze():
    if 'resumes' not in request.files:
        return render_template('bulk_resume.html', message="No files uploaded")
    
    files = request.files.getlist('resumes')
    if not files or all(file.filename == '' for file in files):
        return render_template('bulk_resume.html', message="No files selected")
    
    interests = request.form.get('interests', '').strip()
    if not interests:
        return render_template('bulk_resume.html', message="Please provide interests")
    
    results = []
    
    for file in files:
        if file.filename == '':
            continue
            
        try:
            filename = secure_filename(file.filename)
            
            if not (filename.endswith('.pdf') or filename.endswith('.txt')):
                results.append({
                    'filename': filename,
                    'status': 'error',
                    'message': 'Invalid file format. Please upload PDF or TXT files only.'
                })
                continue
                
            # Read resume content
            try:
                if filename.endswith('.pdf'):
                    resume_text = pdf_to_text(file)
                else:  # .txt file
                    resume_text = file.read().decode('utf-8')
                
                if not resume_text.strip():
                    results.append({
                        'filename': filename,
                        'status': 'error',
                        'message': 'Resume appears to be empty'
                    })
                    continue
                    
                # Analyze resume
                match_score, career_recommendations, feedback = analyze_resume_match(resume_text, interests)
                
                results.append({
                    'filename': filename,
                    'status': 'success',
                    'match_score': match_score,
                    'career_recommendations': career_recommendations,
                    'feedback': feedback
                })
                
            except Exception as e:
                app.logger.error(f"Error processing {filename}: {str(e)}")
                results.append({
                    'filename': filename,
                    'status': 'error',
                    'message': f'Error processing resume: {str(e)}'
                })
                
        except Exception as e:
            app.logger.error(f"Error with file {file.filename}: {str(e)}")
            results.append({
                'filename': file.filename,
                'status': 'error',
                'message': f'Error handling file: {str(e)}'
            })
    
    if not results:
        return render_template('bulk_resume.html', message="No valid files were processed")
        
    return render_template('bulk_resume.html', results=results)

if __name__ == '__main__':
    print("Please use production.py for running the server in production mode")
    print("Example: python production.py")
