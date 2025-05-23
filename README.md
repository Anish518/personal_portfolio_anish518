# personal_portfolio_anish518

Anish Kandi - Personal Portfolio Website
A professional portfolio website showcasing integration and data engineering skills through interactive projects and API demonstrations. Built with Python Flask backend.

Features
Responsive Design: Mobile-first approach using Bootstrap for a consistent experience across devices
Interactive Skills Visualization: Dynamic charts using Chart.js to showcase technical proficiency
Project Showcase: Database-driven project portfolio with filtering options
GitHub Integration: Live display of GitHub repositories with metadata
API Demonstrations: Interactive API endpoints showcasing backend development skills
Contact Form: Functional contact form with database storage and email notifications
Resume Display & Download: Professional resume with downloadable PDF version
Technologies Used
Backend: Python, Flask, SQLite (can be configured for PostgreSQL)
Frontend: HTML5, CSS3, JavaScript, Bootstrap, Chart.js
API Integration: GitHub API, custom REST API endpoints
Deployment: Compatible with most cloud platforms (AWS, Azure, etc.)
Installation
Clone the repository:

git clone https://github.com/anish-kandi/portfolio-website.git
cd portfolio-website
Create and activate a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

pip install -r requirements.txt
Set up environment variables (optional):

Create a .env file in the root directory with the following variables:
FLASK_APP=main.py
FLASK_ENV=development
SESSION_SECRET=your_secret_key
GITHUB_TOKEN=your_github_token  # Optional for higher rate limits
MAIL_USERNAME=your_email        # For contact form emails
MAIL_PASSWORD=your_email_password
DATABASE_URL=your_database_url  # For PostgreSQL (optional)
Initialize the database:

# The database will be automatically initialized on first run
Run the application:

python main.py
# or
gunicorn --bind 0.0.0.0:5000 main:app
Access the website at http://localhost:5000

portfolio-website/
├── app.py                  # Flask application setup and routes
├── main.py                 # Application entry point
├── models.py               # Database models
├── portfolio.db            # SQLite database (created on first run)
├── requirements.txt        # Python dependencies
├── static/                 # Static assets
│   ├── assets/             # Images, resume PDF, etc.
│   ├── css/                # CSS stylesheets
│   └── js/                 # JavaScript files
└── templates/              # HTML templates
    ├── layout.html         # Base template
    ├── index.html          # Homepage
    ├── projects.html       # Projects page
    ├── experience.html     # Experience page
    └── ...                 # Other page templates
API Endpoints
The application provides several API endpoints:

GET /api/data/skills: Returns skills data with proficiency levels
GET /api/data/experience: Returns professional experience data
GET /api/github/repos: Returns GitHub repositories

Customization
You can customize this portfolio by:

Updating personal information in the templates
Modifying the database initialization in app.py to include your projects
Updating API endpoints to return your personal data
Customizing the CSS in static/css/style.css
Deployment
This application can be deployed to various cloud platforms:

Heroku: Add a Procfile with web: gunicorn main:app
AWS Elastic Beanstalk: Use the provided requirements.txt
Docker: A Dockerfile is included for containerized deployment


Contact
Anish Kandi - kandianishreddy@yahoo.co.in

Project Link: https://github.com/anish-kandi/portfolio-website
