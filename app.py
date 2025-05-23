import os
import logging
import sqlite3
import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_from_directory
from flask_mail import Mail, Message
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

# Configure mail settings
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'kandianishreddy@yahoo.co.in')

mail = Mail(app)

# Database setup
def get_db_connection():
    conn = sqlite3.connect('portfolio.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create messages table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        subject TEXT NOT NULL,
        message TEXT NOT NULL,
        date_sent TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create projects table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        technologies TEXT NOT NULL,
        image_url TEXT,
        github_url TEXT,
        live_url TEXT,
        featured BOOLEAN DEFAULT 0
    )
    ''')
    
    # Insert sample projects if none exist
    cursor.execute('SELECT COUNT(*) FROM projects')
    if cursor.fetchone()[0] == 0:
        projects = [
            (
                'Snowflake to Salesforce Integration', 
                'Automated data synchronization between Snowflake and Salesforce CRM using Python-based integration scripts with REST/SOAP APIs.',
                'Python, REST API, SOAP API, Snowflake, Salesforce, JSON',
                None,
                'https://github.com/anish-kandi/snowflake-salesforce-integration',
                None,
                1
            ),
            (
                'ETL Pipeline with Informatica', 
                'Developed ETL pipelines using Informatica PowerCenter for data flow, transformation with API integrations.',
                'Informatica PowerCenter, SQL, API Integration, Python',
                None,
                'https://github.com/anish-kandi/etl-informatica-pipeline',
                None,
                1
            ),
            (
                'ML-Based Lead Data Extraction', 
                'System for extracting lead data using ML, transforming data from GCP to Snowflake, and pushing to Salesforce CRM.',
                'Python, Machine Learning, GCP, Snowflake, Salesforce API',
                None,
                'https://github.com/anish-kandi/ml-lead-extraction',
                None,
                1
            ),
            (
                'AI Chatbot with CI/CD', 
                'Developed an AI chatbot (LLM) with CI/CD pipelines using GitHub Actions and Azure DevOps, containerized with Docker and deployed on AKS.',
                'Python, LLM, GitHub Actions, Azure DevOps, Docker, Kubernetes, Terraform',
                None,
                'https://github.com/anish-kandi/ai-chatbot-cicd',
                None,
                1
            ),
            (
                'Real-time Monitoring System', 
                'Python-based SCADA solution using OPC UA and pymodbus, integrated with various DCS platforms.',
                'Python, OPC UA, pymodbus, SCADA, ABB Advant/Melody, Siemens PCS7, Emerson DeltaV',
                None,
                'https://github.com/anish-kandi/realtime-monitoring-system',
                None,
                0
            ),
            (
                'Wastewater Treatment Monitoring', 
                'Flask-based REST API and Django web app for wastewater treatment monitoring with SQL CRUD operations and MongoDB for unstructured data.',
                'Python, Flask, Django, REST API, SQL, MongoDB',
                None,
                'https://github.com/anish-kandi/wastewater-monitoring',
                None,
                0
            )
        ]
        cursor.executemany('INSERT INTO projects (title, description, technologies, image_url, github_url, live_url, featured) VALUES (?, ?, ?, ?, ?, ?, ?)', projects)
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Routes
@app.route('/')
def index():
    return render_template('index.html', page_title="Home")

@app.route('/projects')
def projects():
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects ORDER BY featured DESC, id DESC').fetchall()
    conn.close()
    return render_template('projects.html', projects=projects, page_title="Projects")

@app.route('/experience')
def experience():
    return render_template('experience.html', page_title="Experience")

@app.route('/skills')
def skills():
    return render_template('skills.html', page_title="Skills")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        if not all([name, email, subject, message]):
            flash('All fields are required!', 'danger')
            return redirect(url_for('contact'))
        
        try:
            # Store in database
            conn = get_db_connection()
            conn.execute('INSERT INTO messages (name, email, subject, message) VALUES (?, ?, ?, ?)',
                        (name, email, subject, message))
            conn.commit()
            conn.close()
            
            # Send email if configured
            if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
                msg = Message(
                    subject=f"Portfolio Contact: {subject}",
                    recipients=[app.config['MAIL_DEFAULT_SENDER']],
                    body=f"From: {name} <{email}>\n\n{message}",
                    sender=app.config['MAIL_DEFAULT_SENDER']
                )
                mail.send(msg)
            
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            logging.error(f"Error sending message: {str(e)}")
            flash('An error occurred while sending your message. Please try again later.', 'danger')
            return redirect(url_for('contact'))
    
    return render_template('contact.html', page_title="Contact")

@app.route('/github')
def github():
    return render_template('github.html', page_title="GitHub")

@app.route('/api/github/repos')
def github_repos():
    try:
        username = "anish-kandi"  # This would ideally be configurable
        url = f"https://api.github.com/users/{username}/repos"
        
        # Add token if available
        headers = {}
        github_token = os.environ.get('GITHUB_TOKEN')
        if github_token:
            headers['Authorization'] = f'token {github_token}'
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Sort by updated_at date (most recent first)
        repos = sorted(response.json(), key=lambda x: x.get('updated_at', ''), reverse=True)
        
        # Limit to top 10 repositories
        return jsonify(repos[:10])
    except Exception as e:
        logging.error(f"Error fetching GitHub repos: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api_demo')
def api_demo():
    return render_template('api_demo.html', page_title="API Demo")

@app.route('/api/data/skills')
def api_skills():
    skills = {
        "programming_languages": [
            {"name": "Python", "proficiency": 90},
            {"name": "Java", "proficiency": 80},
            {"name": "C/C++", "proficiency": 75},
            {"name": "TypeScript", "proficiency": 70},
            {"name": "Bash", "proficiency": 85}
        ],
        "databases": [
            {"name": "MSSQL", "proficiency": 85},
            {"name": "SQLite", "proficiency": 80},
            {"name": "PostgreSQL", "proficiency": 75},
            {"name": "Azure SQL", "proficiency": 80},
            {"name": "MongoDB", "proficiency": 70}
        ],
        "web_frameworks": [
            {"name": "Django", "proficiency": 85},
            {"name": "Flask", "proficiency": 90}
        ],
        "cloud_platforms": [
            {"name": "AWS", "proficiency": 80},
            {"name": "Azure", "proficiency": 85},
            {"name": "GCP", "proficiency": 75},
            {"name": "Snowflake", "proficiency": 80}
        ],
        "devops_tools": [
            {"name": "Kubernetes", "proficiency": 85},
            {"name": "Docker", "proficiency": 90},
            {"name": "Jenkins", "proficiency": 80},
            {"name": "GitHub Actions", "proficiency": 85},
            {"name": "Azure DevOps", "proficiency": 80},
            {"name": "Terraform", "proficiency": 75},
            {"name": "Ansible", "proficiency": 70}
        ]
    }
    return jsonify(skills)

@app.route('/api/data/experience')
def api_experience():
    experience = [
        {
            "company": "SKF Lubrication systems GmbH",
            "position": "Werk student: Integration Engineer",
            "location": "Berlin, Germany",
            "start_date": "Mar 2025",
            "end_date": "Present",
            "description": [
                "Working on development and deployment of Python based integration scripts to automate data sync between snowflake and Salesforce (CRM) and other cloud systems using REST/SOAP APIs and JSON.",
                "Working on ETL pipelines using Informatica PowerCenter for data flow, transformation and with API integrations.",
                "Extracting the lead data by ML and transforming the data from GCP to Snowflake and pushing them to Salesforce (CRM) for sales team usage. Testing the aspects in Salesforce sandbox",
                "Preparing the technical documentation of the tech-stack being developed and published in the Group share points"
            ]
        },
        {
            "company": "GetYourGuide GmbH",
            "position": "Werk student: Software- Data Engineer",
            "location": "Berlin, Germany",
            "start_date": "Jan 2025",
            "end_date": "Mar 2025",
            "description": [
                "Worked on development of reporting solution in Looker that replaced dozens of individual reports while unifying the visual language used in the company Looker Studio reports.",
                "Worked on replacement of manual data collection process that cost the company 60K per annum by a scalable, automated solution leveraging AI.",
                "Data collection process is executed by integrating the data to Morgan Stanley."
            ]
        },
        {
            "company": "Fed Ex Express GmbH",
            "position": "Werk student: Data/DevOps Enginner",
            "location": "Berlin, Germany",
            "start_date": "Feb 2024",
            "end_date": "Jan 2025",
            "description": [
                "Involved in tasks associated with integration/automation with APIs and CRUD operations (SQL): feeding data into FedEx's tracking system to ensure accurate and upto-date information.",
                "Worked on development of AI chatbot project (LLM), implementing CI/CD pipelines using GitHub Actions and Azure DevOps, containerized applications with Docker, and deployed them on Azure Kubernetes Service (AKS) using Terraform for infrastructure as code.",
                "Deployment with Prometheus, Grafana and Azure log Analytics with seamless authentication."
            ]
        },
        {
            "company": "Alghanim International",
            "position": "Software Engineer/Automation",
            "location": "Kuwait",
            "start_date": "Jan 2016",
            "end_date": "Feb 2023",
            "description": [
                "Successfully delivered 8 large-scale software projects across power, water, and wind sectors, leading cross-functional teams (3–6 members) and ensuring stakeholder requirements were fulfilled.",
                "Developed and deployed real-time monitoring systems and a Python-based SCADA solution (using OPC UA, pymodbus) integrated with DCS platforms like ABB Advant/Melody, Siemens PCS7, and Emerson DeltaV, resulting in 15% reduced downtime and $100K annual cost savings.",
                "Built a Flask-based REST API and Django based web app for wastewater treatment monitoring, executed SQL CRUD operations, and applied MongoDB for unstructured data management.",
                "Integrated tools like PowerFactory and FGH Integral for power system analysis and fault automation, feeding insights into SCADA for optimized decision-making.",
                "Engineered device communication protocols (Modbus TCP/IP), developed energy management algorithms on Siemens S7 and Allen-Bradley PLC 5, and created a dynamic Java-based corporate website for portfolio and investor communications."
            ]
        },
        {
            "company": "Sai Wardha Power Pvt, Ltd",
            "position": "Internship: Software Engineer",
            "location": "Pune, India",
            "start_date": "Feb 2014",
            "end_date": "Jul 2015",
            "description": [
                "Assistance in the development of the company website.",
                "Involved in overhaul maintenance of controls, PLCs, and network communication.",
                "Involved in the integration of operator workstation with local plant network communication.",
                "Involved in activities such as Database creation, and all CRUD operations. Additionally involved in cleaning of data and scripting in SQL with JOIN/Sub queries etc based on the output necessary."
            ]
        },
        {
            "company": "320sms.com",
            "position": "Co-founder - Startup",
            "location": "Hyderabad, India",
            "start_date": "Apr 2011",
            "end_date": "Nov 2013",
            "description": [
                "Launched and scaled India's first 300-character SMS platform, serving B2B clients, managing backend development in PHP and SQL, and handling server backups.",
                "Generating funds through the selling of SMS to commercial shops and schools."
            ]
        }
    ]
    return jsonify(experience)

@app.route('/resume')
def resume():
    return render_template('resume.html', page_title="Resume")

@app.route('/download-resume')
def download_resume():
    return send_from_directory('static/assets', 'resume.pdf')

@app.route('/api/demo/weather')
def weather_demo():
    # Demo API that returns mock weather data
    city = request.args.get('city', 'Berlin')
    weather_types = ['Sunny', 'Cloudy', 'Rainy', 'Snowy', 'Windy']
    import random
    
    # Generate deterministic result based on city name
    random.seed(sum(ord(c) for c in city) + datetime.now().day)
    
    weather = {
        'city': city,
        'temperature': round(random.uniform(10, 30), 1),
        'weather': weather_types[random.randint(0, len(weather_types)-1)],
        'humidity': random.randint(30, 90),
        'wind_speed': round(random.uniform(0, 20), 1),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return jsonify(weather)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
