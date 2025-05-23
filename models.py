# This file contains database models for the application
# Currently using SQLite with direct connections, 
# but can be extended to use an ORM like SQLAlchemy for more complex applications

class Message:
    """Model for contact form messages"""
    def __init__(self, id, name, email, subject, message, date_sent):
        self.id = id
        self.name = name
        self.email = email
        self.subject = subject
        self.message = message
        self.date_sent = date_sent

class Project:
    """Model for portfolio projects"""
    def __init__(self, id, title, description, technologies, image_url=None, github_url=None, live_url=None, featured=False):
        self.id = id
        self.title = title
        self.description = description
        self.technologies = technologies
        self.image_url = image_url
        self.github_url = github_url
        self.live_url = live_url
        self.featured = featured
