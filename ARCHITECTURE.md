# Architecture

React/Vite provides the responsive interface and calls a Flask REST API. Flask-SQLAlchemy stores users, profiles, careers, roadmaps, progress, resources, milestones and study sessions in SQLite. Flask-JWT-Extended protects student data.

Roadmap generation uses a local rule-based engine by default. A separate Bedrock module is prepared for optional AWS credentials and model invocation. All AWS deployment remains opt-in.
