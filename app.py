import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///pathfinder.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'local-demo-secret-change-me')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
CORS(app, resources={r'/api/*': {'origins': '*'}})
db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    degree = db.Column(db.String(120), default='')
    branch = db.Column(db.String(120), default='')
    college = db.Column(db.String(120), default='')
    graduation_year = db.Column(db.Integer)
    skills = db.Column(db.JSON, default=list)
    career_goal = db.Column(db.String(120), default='')
    experience = db.Column(db.String(50), default='Beginner')
    learning_style = db.Column(db.String(50), default='Mixed')
    hours_per_day = db.Column(db.Float, default=2)
    days_per_week = db.Column(db.Integer, default=5)
    duration = db.Column(db.String(50), default='3 months')

class Career(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text, default='')
    skills = db.Column(db.JSON, default=list)
    difficulty = db.Column(db.String(30), default='Intermediate')
    duration = db.Column(db.String(50), default='12 weeks')

class Roadmap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    career_goal = db.Column(db.String(120), nullable=False)
    introduction = db.Column(db.Text, default='')
    source = db.Column(db.String(30), default='demo')
    estimated_duration = db.Column(db.String(50), default='12 weeks')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Phase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roadmap_id = db.Column(db.Integer, db.ForeignKey('roadmap.id'), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')
    duration = db.Column(db.String(50), default='2 weeks')
    difficulty = db.Column(db.String(30), default='Beginner')

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phase_id = db.Column(db.Integer, db.ForeignKey('phase.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    explanation = db.Column(db.Text, default='')
    objectives = db.Column(db.JSON, default=list)
    duration = db.Column(db.Integer, default=120)
    resources = db.Column(db.JSON, default=list)

class TopicProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    platform = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default='')
    difficulty = db.Column(db.String(30), default='Beginner')
    free = db.Column(db.Boolean, default=True)
    url = db.Column(db.String(500), nullable=False)

class SavedResource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'), nullable=False)

class Milestone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    target_date = db.Column(db.String(20), default='')
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)

class StudySession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    planned_minutes = db.Column(db.Integer, default=60)
    actual_minutes = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)

class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

CAREERS = [
 ('Data Analyst','Turn raw data into useful business insights.','Python, SQL, Excel, Statistics, Data visualization, Power BI','Intermediate','12 weeks'),
 ('Data Scientist','Build analytical models and extract predictions from data.','Python, Statistics, SQL, Machine Learning, Pandas','Advanced','16 weeks'),
 ('AI Engineer','Create AI applications using modern models and tools.','Python, Machine Learning, Deep Learning, Generative AI','Advanced','20 weeks'),
 ('Machine Learning Engineer','Train, deploy, and monitor machine learning systems.','Python, Machine Learning, SQL, AWS','Advanced','18 weeks'),
 ('Full Stack Developer','Build complete web applications end to end.','HTML, CSS, JavaScript, React, Flask, Databases','Intermediate','16 weeks'),
 ('Python Developer','Develop reliable applications and backend services with Python.','Python, Flask, SQL, APIs','Intermediate','12 weeks'),
 ('Java Developer','Build enterprise applications using Java ecosystems.','Java, SQL, Spring, APIs','Intermediate','14 weeks'),
 ('Cloud Engineer','Design and operate cloud infrastructure.','AWS, Azure, Google Cloud, Networking','Advanced','16 weeks'),
 ('Cybersecurity Analyst','Protect systems and monitor security threats.','Networking, Linux, Security, Python','Advanced','18 weeks'),
 ('Software Engineer','Design and build maintainable software systems.','Data Structures, Algorithms, Git, Testing','Intermediate','14 weeks'),
 ('Business Analyst','Connect business needs with practical technical solutions.','Excel, SQL, Statistics, Communication','Intermediate','10 weeks'),
 ('Product Manager','Plan products and lead cross-functional delivery.','Product Strategy, Analytics, Communication','Intermediate','10 weeks')]

RESOURCES = [
 ('Python Official Documentation','Python','Python','The canonical guide and reference for Python.','Beginner',True,'https://docs.python.org/3/'),
 ('SQLBolt','SQLBolt','SQL','Interactive SQL lessons and exercises.','Beginner',True,'https://sqlbolt.com/'),
 ('Microsoft Excel Training','Microsoft Support','Excel','Official Excel help and learning resources.','Beginner',True,'https://support.microsoft.com/excel'),
 ('Khan Academy Statistics','Khan Academy','Statistics','Free lessons covering statistics and probability.','Beginner',True,'https://www.khanacademy.org/math/statistics-probability'),
 ('Microsoft Power BI Learning','Microsoft Learn','Power BI','Free guided learning for Power BI.','Intermediate',True,'https://learn.microsoft.com/power-bi/'),
 ('React Documentation','React','React','Official React concepts and API reference.','Intermediate',True,'https://react.dev/'),
 ('Flask Documentation','Pallets','Flask','Official Flask framework documentation.','Intermediate',True,'https://flask.palletsprojects.com/'),
 ('AWS Skill Builder','Amazon Web Services','AWS','Free and paid AWS learning paths.','Intermediate',True,'https://skillbuilder.aws/'),
 ('Google Generative AI Courses','Google','Generative AI','Google training for generative AI concepts.','Intermediate',True,'https://www.cloudskillsboost.google/'),
 ('Machine Learning Crash Course','Google','Machine Learning','Practical introduction to machine learning.','Intermediate',True,'https://developers.google.com/machine-learning/crash-course')]

def seed():
    if Career.query.count() == 0:
        for title, desc, skills, diff, dur in CAREERS:
            db.session.add(Career(title=title, description=desc, skills=[x.strip() for x in skills.split(',')], difficulty=diff, duration=dur))
    if Resource.query.count() == 0:
        for title, platform, category, desc, diff, free, url in RESOURCES:
            db.session.add(Resource(title=title, platform=platform, category=category, description=desc, difficulty=diff, free=free, url=url))
    if not User.query.filter_by(email='demo@pathfinder.ai').first():
        u = User(name='Demo Student', email='demo@pathfinder.ai', password_hash=generate_password_hash('demo123'))
        db.session.add(u); db.session.flush()
        db.session.add(Profile(user_id=u.id, degree='B.Tech', branch='Computer Science', college='Demo University', graduation_year=2027, skills=['Python','Excel','SQL'], career_goal='Data Analyst', experience='Beginner', hours_per_day=2, days_per_week=5, duration='12 weeks'))
    db.session.commit()

with app.app_context():
    db.create_all(); seed()

@app.errorhandler(404)
def not_found(e): return jsonify(error='Resource not found'), 404
@app.errorhandler(500)
def server_error(e): return jsonify(error='Internal server error'), 500

@app.post('/api/auth/register')
def register():
    data = request.get_json(silent=True) or {}
    name, email, password = (data.get(k,'').strip() for k in ('name','email','password'))
    if not name or not email or len(password) < 6: return jsonify(error='Name, valid email and password (6+ characters) are required'), 400
    if User.query.filter_by(email=email.lower()).first(): return jsonify(error='Email already registered'), 409
    u = User(name=name, email=email.lower(), password_hash=generate_password_hash(password))
    db.session.add(u); db.session.flush()
    db.session.add(Profile(user_id=u.id, college=data.get('college',''), degree=data.get('education','')))
    db.session.commit()
    token = create_access_token(identity=str(u.id))
    return jsonify(token=token, user={'id':u.id,'name':u.name,'email':u.email}), 201

@app.post('/api/auth/login')
def login():
    data = request.get_json(silent=True) or {}
    u = User.query.filter_by(email=data.get('email','').lower().strip()).first()
    if not u or not check_password_hash(u.password_hash, data.get('password','')):
        return jsonify(error='Invalid email or password'), 401
    token = create_access_token(identity=str(u.id))
    return jsonify(token=token, user={'id':u.id,'name':u.name,'email':u.email})

@app.get('/api/auth/me')
@jwt_required()
def me():
    u = User.query.get(int(get_jwt_identity()))
    return jsonify(user={'id':u.id,'name':u.name,'email':u.email})

@app.get('/api/profile')
@jwt_required()
def get_profile():
    uid = int(get_jwt_identity()); p = Profile.query.filter_by(user_id=uid).first()
    return jsonify(profile={'degree':p.degree,'branch':p.branch,'college':p.college,'graduation_year':p.graduation_year,'skills':p.skills or [],'career_goal':p.career_goal,'experience':p.experience,'learning_style':p.learning_style,'hours_per_day':p.hours_per_day,'days_per_week':p.days_per_week,'duration':p.duration})

@app.put('/api/profile')
@jwt_required()
def update_profile():
    uid = int(get_jwt_identity()); p = Profile.query.filter_by(user_id=uid).first(); data = request.get_json(silent=True) or {}
    for key in ('degree','branch','college','graduation_year','skills','career_goal','experience','learning_style','hours_per_day','days_per_week','duration'):
        if key in data: setattr(p,key,data[key])
    db.session.commit(); db.session.add(UserActivity(user_id=uid,text='Updated learning profile'))
    db.session.commit(); return jsonify(profile={'career_goal':p.career_goal,'skills':p.skills or []})

@app.get('/api/careers')
def careers():
    return jsonify([{'id':c.id,'title':c.title,'description':c.description,'skills':c.skills,'difficulty':c.difficulty,'duration':c.duration} for c in Career.query.order_by(Career.title).all()])

ASSESSMENTS = {
 'Data Analyst':[('Python','What does len([1,2,3]) return?',['2','3','4'],'3','It returns the number of items.'),('SQL','Which clause filters rows?',['WHERE','GROUP','ORDER'],'WHERE','WHERE filters rows.'),('Excel','Which function adds a range?',['SUM','AVERAGE','COUNT'],'SUM','SUM adds numeric values.')],
 'Full Stack Developer':[('JavaScript','Which keyword declares a block-scoped variable?',['var','let','const'],'let','let creates block-scoped bindings.'),('React','Which hook manages state?',['useEffect','useState','useMemo'],'useState','useState stores component state.'),('Databases','What is a primary key?',['A unique row identifier','A table','A query'],'A unique row identifier','A primary key uniquely identifies each row.')]
}

CAREER_PHASES = {
    'Data Analyst': [
        ('Python for Analysis', 'Prepare and analyze data with Python.', ['Python basics', 'Pandas dataframes', 'Data cleaning']),
        ('SQL and Databases', 'Query and organize business data.', ['SQL fundamentals', 'Joins and aggregations', 'Database design']),
        ('Statistics and Visualization', 'Interpret trends and communicate findings.', ['Descriptive statistics', 'Excel dashboards', 'Power BI reports']),
        ('Analytics Portfolio', 'Apply the workflow to realistic business questions.', ['Exploratory data analysis', 'Business case study', 'Portfolio presentation']),
    ],
    'Data Scientist': [
        ('Data Science with Python', 'Build a reliable analysis workflow.', ['Python for data science', 'Pandas and NumPy', 'Feature preparation']),
        ('Statistics and Inference', 'Reason about uncertainty in data.', ['Probability distributions', 'Hypothesis testing', 'Experiment design']),
        ('Machine Learning', 'Train and evaluate predictive models.', ['Supervised learning', 'Model validation', 'Feature engineering']),
        ('Applied Data Science', 'Complete an end-to-end modeling project.', ['Unsupervised learning', 'Model interpretation', 'Capstone project']),
    ],
    'AI Engineer': [
        ('AI and Python Foundations', 'Prepare to build AI-powered products.', ['Python for AI', 'Neural network concepts', 'Model APIs']),
        ('Generative AI Applications', 'Use language models in application workflows.', ['Prompt design', 'Structured model outputs', 'Tool use']),
        ('Retrieval and Evaluation', 'Ground and measure AI responses.', ['Embedding concepts', 'Retrieval-augmented generation', 'Evaluation and safety']),
        ('AI Product Engineering', 'Deliver a usable AI application.', ['AI application architecture', 'Deployment basics', 'Capstone AI assistant']),
    ],
    'Machine Learning Engineer': [
        ('Machine Learning Foundations', 'Develop core modeling skills.', ['Python and NumPy', 'Supervised learning', 'Model evaluation']),
        ('Production Data Pipelines', 'Prepare repeatable training data.', ['Data validation', 'Feature pipelines', 'SQL for ML']),
        ('Model Deployment', 'Serve and monitor trained models.', ['Model APIs', 'Container concepts', 'Monitoring and drift']),
        ('MLOps Capstone', 'Build a reproducible ML service.', ['Experiment tracking', 'Deployment workflow', 'End-to-end ML project']),
    ],
    'Full Stack Developer': [
        ('Web Foundations', 'Build accessible, responsive web pages.', ['HTML and CSS', 'JavaScript essentials', 'Responsive layouts']),
        ('Frontend with React', 'Create interactive user interfaces.', ['React components', 'State and effects', 'API integration']),
        ('Backend and Databases', 'Build application services and persistence.', ['Flask REST APIs', 'SQL and data modeling', 'Authentication']),
        ('Full Stack Portfolio', 'Ship a complete web application.', ['Frontend-backend integration', 'Testing', 'Deployment and portfolio']),
    ],
    'Python Developer': [
        ('Python Core', 'Write clear, maintainable Python programs.', ['Python syntax and data structures', 'Functions and modules', 'Exceptions and testing']),
        ('Backend Development', 'Build services with Python frameworks.', ['Flask application structure', 'REST API design', 'Authentication']),
        ('Data and Integration', 'Connect applications to external systems.', ['SQL and SQLAlchemy', 'HTTP APIs', 'Background processing']),
        ('Developer Portfolio', 'Package and demonstrate a Python application.', ['Automated testing', 'Logging and configuration', 'Deploy a Python service']),
    ],
    'Java Developer': [
        ('Java Programming', 'Build a strong foundation in Java.', ['Java syntax and collections', 'Object-oriented design', 'Exceptions and testing']),
        ('Persistence and APIs', 'Connect Java services to data and clients.', ['SQL and relational modeling', 'JDBC and persistence', 'REST API fundamentals']),
        ('Spring Development', 'Structure maintainable backend applications.', ['Spring Boot fundamentals', 'Dependency injection', 'Application security']),
        ('Java Capstone', 'Build and present a production-style service.', ['Testing a Spring service', 'Build and deployment', 'Portfolio project']),
    ],
    'Cloud Engineer': [
        ('Cloud Foundations', 'Learn cloud architecture and networking.', ['Cloud service models', 'Networking fundamentals', 'Identity and access']),
        ('AWS Core Services', 'Work with common cloud building blocks.', ['Compute services', 'Object storage', 'Managed databases']),
        ('Infrastructure and Operations', 'Automate and observe cloud systems.', ['Command-line tooling', 'Infrastructure as Code', 'Monitoring and alerts']),
        ('Cloud Engineering Project', 'Design and deploy a secure cloud workload.', ['Cloud security practices', 'Resilient architecture', 'Deployment project']),
    ],
    'Cybersecurity Analyst': [
        ('Systems and Networking', 'Understand the systems defenders protect.', ['Networking fundamentals', 'Linux essentials', 'Security principles']),
        ('Threat Detection', 'Recognize and investigate suspicious activity.', ['Logs and indicators', 'Vulnerability concepts', 'Incident response']),
        ('Security Tooling', 'Practice safe defensive analysis.', ['SIEM workflows', 'Network traffic analysis', 'Security scripting']),
        ('Blue Team Portfolio', 'Document a defensive investigation.', ['Threat report writing', 'Hardening checklist', 'Incident-response exercise']),
    ],
    'Software Engineer': [
        ('Programming and Problem Solving', 'Build core engineering fluency.', ['Programming fundamentals', 'Data structures', 'Algorithms']),
        ('Software Design', 'Structure code for change and reliability.', ['Object-oriented design', 'Git workflows', 'Testing fundamentals']),
        ('Application Engineering', 'Build and integrate software components.', ['API design', 'Database fundamentals', 'Error handling']),
        ('Engineering Capstone', 'Deliver a tested, documented application.', ['System design basics', 'Code review practice', 'Portfolio project']),
    ],
    'Business Analyst': [
        ('Business Analysis Foundations', 'Translate business needs into clear questions.', ['Requirements gathering', 'Process mapping', 'Stakeholder communication']),
        ('Data and Metrics', 'Use data to understand performance.', ['Excel analysis', 'SQL queries', 'Descriptive statistics']),
        ('Insights and Recommendations', 'Communicate actionable findings.', ['Dashboard design', 'KPI definition', 'Insight storytelling']),
        ('Business Case Portfolio', 'Present a practical analysis from end to end.', ['Problem framing', 'Recommendation report', 'Case study presentation']),
    ],
    'Product Manager': [
        ('Product Foundations', 'Understand users, problems and product value.', ['User research', 'Problem statements', 'Product lifecycle']),
        ('Strategy and Prioritization', 'Make transparent product decisions.', ['Product vision', 'Roadmap prioritization', 'Experiment design']),
        ('Delivery and Analytics', 'Work with teams and measure outcomes.', ['Agile collaboration', 'Product analytics', 'Metrics and funnels']),
        ('Product Case Portfolio', 'Demonstrate product thinking with a case.', ['PRD writing', 'Launch planning', 'Product case study']),
    ],
}

@app.get('/api/assessment/questions')
@jwt_required()
def assessment_questions():
    uid=int(get_jwt_identity()); p=Profile.query.filter_by(user_id=uid).first(); career=p.career_goal or 'Data Analyst'
    setq=ASSESSMENTS.get(career,ASSESSMENTS['Data Analyst'])
    qs=[{'id':i+1,'skill':skill,'question':q,'options':opts,'answer':ans,'explanation':exp} for i,(skill,q,opts,ans,exp) in enumerate(setq)]
    return jsonify(questions=qs,career=career)

@app.post('/api/assessment/submit')
@jwt_required()
def assessment_submit():
    data=request.get_json(silent=True) or {}; answers=data.get('answers',{})
    uid=int(get_jwt_identity()); p=Profile.query.filter_by(user_id=uid).first(); career=p.career_goal or 'Data Analyst'; setq=ASSESSMENTS.get(career,ASSESSMENTS['Data Analyst'])
    results=[]; correct=0
    for i,(skill,q,opts,ans,exp) in enumerate(setq):
        user_ans=str(answers.get(str(i+1),'')); ok=user_ans==ans
        if ok: correct+=1
        results.append({'skill':skill,'correct':ok,'answer':ans,'explanation':exp})
    score=round(correct/len(setq)*100)
    db.session.add(UserActivity(user_id=uid,text=f'Completed {career} assessment with a score of {score}%')); db.session.commit()
    return jsonify(score=score,correct=correct,total=len(setq),results=results)

@app.get('/api/assessment/history')
@jwt_required()
def assessment_history():
    uid=int(get_jwt_identity())
    acts=UserActivity.query.filter_by(user_id=uid).filter(UserActivity.text.like('%assessment%')).order_by(UserActivity.created_at.desc()).all()
    return jsonify([{'text':a.text,'date':a.created_at.isoformat()} for a in acts])

def remove_roadmaps(uid, career):
    for r in Roadmap.query.filter_by(user_id=uid, career_goal=career).all():
        for ph in Phase.query.filter_by(roadmap_id=r.id).all():
            topic_ids = [topic.id for topic in Topic.query.filter_by(phase_id=ph.id).all()]
            if topic_ids:
                TopicProgress.query.filter(
                    TopicProgress.user_id == uid,
                    TopicProgress.topic_id.in_(topic_ids),
                ).delete(synchronize_session=False)
            Topic.query.filter_by(phase_id=ph.id).delete(synchronize_session=False)
            db.session.delete(ph)
        db.session.delete(r)

def career_roadmap_phases(career, profile):
    skills=set((profile.skills or []) if profile else [])
    phases = list(CAREER_PHASES.get(career, []))
    if not phases:
        career_record = Career.query.filter_by(title=career).first()
        required_skills = career_record.skills if career_record else [career]
        phases = [
            ('Core Skills', f'Build the essential skills for {career}.', [f'{skill} fundamentals' for skill in required_skills[:3]]),
            ('Applied Practice', f'Apply {career} skills to practical problems.', [f'{skill} applied practice' for skill in required_skills[3:]] or [f'{career} practice exercises']),
            ('Portfolio Project', f'Demonstrate your readiness for {career}.', [f'{career} capstone project', 'Testing and documentation']),
        ]
    if career == 'Data Analyst' and 'Python' in skills:
        phases[0] = ('Advanced Python and Pandas', 'Skip Python basics and focus on efficient analysis.', ['Pandas dataframes', 'Vectorized analysis', 'Data cleaning pipelines'])
    return phases

def roadmap_matches_plan(roadmap, expected_phases):
    actual_phases = Phase.query.filter_by(roadmap_id=roadmap.id).order_by(Phase.number).all()
    if len(actual_phases) != len(expected_phases):
        return False
    for actual, expected in zip(actual_phases, expected_phases):
        expected_title, _, expected_topics = expected
        actual_topics = [topic.name for topic in Topic.query.filter_by(phase_id=actual.id).all()]
        if actual.title != expected_title or actual_topics != expected_topics:
            return False
    return True

def build_demo_roadmap(uid, career):
    p=Profile.query.filter_by(user_id=uid).first()
    phases=career_roadmap_phases(career,p)
    r=Roadmap(user_id=uid,title=f'Personalized {career} Roadmap',career_goal=career,introduction=f'This roadmap adapts to your {p.experience if p else "Beginner"} level, {p.hours_per_day if p else 2} daily study hours and selected goal: {career}.',source='demo',estimated_duration=p.duration if p and p.duration else '12 weeks')
    db.session.add(r); db.session.flush()
    for i,(title,desc,topics) in enumerate(phases,1):
        difficulty='Beginner' if i < 3 and (not p or p.experience == 'Beginner') else 'Intermediate'
        ph=Phase(roadmap_id=r.id,number=i,title=title,description=desc,duration='1-3 weeks',difficulty=difficulty)
        db.session.add(ph); db.session.flush()
        for name in topics:
            db.session.add(Topic(phase_id=ph.id,name=name,explanation=f'Learn and practice {name} through guided exercises and a practical application.',objectives=[f'Understand {name}','Apply it in an exercise','Document what you learned'],duration=120,resources=['Python Official Documentation','SQLBolt','Microsoft Learn']))
    db.session.commit(); db.session.add(UserActivity(user_id=uid,text=f'Generated a demo roadmap for {career}')) ; db.session.commit()
    return r

@app.post('/api/roadmap/generate')
@jwt_required()
def generate():
    uid=int(get_jwt_identity()); p=Profile.query.filter_by(user_id=uid).first()
    data=request.get_json(silent=True) or {}
    career=data.get('career_goal') or p.career_goal or 'Data Analyst'
    if career not in CAREER_PHASES and career!=p.career_goal and not Career.query.filter_by(title=career).first():
        return jsonify(error='Unknown career goal'),400
    existing=Roadmap.query.filter_by(user_id=uid,career_goal=career).order_by(Roadmap.created_at.desc()).first()
    expected_phases=career_roadmap_phases(career,p)
    if existing and roadmap_matches_plan(existing,expected_phases):
        return jsonify({'roadmap':roadmap_json(existing,uid),'source':existing.source,'message':'Existing roadmap returned'}),200
    if existing:
        remove_roadmaps(uid,career)
    r=build_demo_roadmap(uid,career); return jsonify({'roadmap':roadmap_json(r,uid),'source':r.source,'message':'Demo roadmap generated'}),201

@app.post('/api/roadmap/regenerate')
@jwt_required()
def regenerate():
    uid=int(get_jwt_identity()); p=Profile.query.filter_by(user_id=uid).first(); career=p.career_goal or 'Data Analyst'; remove_roadmaps(uid,career); r=build_demo_roadmap(uid,career)
    return jsonify({'roadmap':roadmap_json(r,uid),'source':r.source,'message':'Roadmap regenerated in demo mode'})

def roadmap_json(r, uid):
    out={'id':r.id,'title':r.title,'career_goal':r.career_goal,'introduction':r.introduction,'source':r.source,'estimated_duration':r.estimated_duration,'phases':[]}
    for ph in Phase.query.filter_by(roadmap_id=r.id).order_by(Phase.number).all():
        topics=[]
        for t in Topic.query.filter_by(phase_id=ph.id).all():
            prog=TopicProgress.query.filter_by(user_id=uid,topic_id=t.id).first(); topics.append({'id':t.id,'name':t.name,'explanation':t.explanation,'objectives':t.objectives,'duration':t.duration,'resources':t.resources,'completed':bool(prog and prog.completed),'completed_at':prog.completed_at.isoformat() if prog and prog.completed_at else None})
        completed=sum(1 for t in topics if t['completed']); pct=round(completed/len(topics)*100) if topics else 0
        out['phases'].append({'id':ph.id,'number':ph.number,'title':ph.title,'description':ph.description,'duration':ph.duration,'difficulty':ph.difficulty,'completion':pct,'status':'Completed' if pct==100 else ('In Progress' if pct>0 else 'Not Started'),'topics':topics})
    return out

@app.get('/api/roadmap')
@jwt_required()
def get_roadmap():
    uid=int(get_jwt_identity())
    p=Profile.query.filter_by(user_id=uid).first()
    career=request.args.get('career_goal') or (p.career_goal if p and p.career_goal else 'Data Analyst')
    if career not in CAREER_PHASES and (not p or career!=p.career_goal) and not Career.query.filter_by(title=career).first():
        return jsonify(error='Unknown career goal'),400
    r=Roadmap.query.filter_by(user_id=uid,career_goal=career).order_by(Roadmap.created_at.desc()).first()
    return jsonify(roadmap=roadmap_json(r,uid) if r else None)

@app.get('/api/roadmap/<int:roadmap_id>')
@jwt_required()
def get_roadmap_id(roadmap_id):
    r=Roadmap.query.get_or_404(roadmap_id)
    if r.user_id!=int(get_jwt_identity()): return jsonify(error='Forbidden'),403
    return jsonify(roadmap=roadmap_json(r,int(get_jwt_identity())))

@app.get('/api/resources')
def resource_list():
    q=request.args.get('q','').lower(); cat=request.args.get('category','')
    items=Resource.query.all(); out=[]
    for r in items:
        if q and q not in (r.title+' '+r.description+' '+r.category).lower(): continue
        if cat and r.category!=cat: continue
        out.append({'id':r.id,'title':r.title,'platform':r.platform,'category':r.category,'description':r.description,'difficulty':r.difficulty,'free':r.free,'url':r.url})
    return jsonify(out)

@app.get('/api/resources/recommended')
@jwt_required()
def recommended_resources():
    uid=int(get_jwt_identity()); p=Profile.query.filter_by(user_id=uid).first(); career=p.career_goal if p else 'Data Analyst'
    if 'Data' in career or 'Analyst' in career: cats=['Python','SQL','Statistics','Excel','Power BI']
    elif 'Stack' in career: cats=['React','Flask','SQL','JavaScript']
    else: cats=['Python','AWS','Machine Learning','Generative AI']
    items=Resource.query.filter(Resource.category.in_(cats)).all()
    return jsonify([{'id':r.id,'title':r.title,'platform':r.platform,'category':r.category,'description':r.description,'difficulty':r.difficulty,'free':r.free,'url':r.url} for r in items])

@app.post('/api/resources/save')
@jwt_required()
def save_resource():
    uid=int(get_jwt_identity()); data=request.get_json(silent=True) or {}; rid=data.get('resource_id')
    existing=SavedResource.query.filter_by(user_id=uid,resource_id=rid).first()
    if existing:
        db.session.delete(existing); db.session.commit(); return jsonify(saved=False)
    db.session.add(SavedResource(user_id=uid,resource_id=rid)); db.session.commit(); return jsonify(saved=True)

@app.post('/api/progress/topic')
@jwt_required()
def progress_topic():
    uid=int(get_jwt_identity()); data=request.get_json(silent=True) or {}; tid=data.get('topic_id'); tid=int(tid)
    topic=db.session.get(Topic,tid)
    if not topic: return jsonify(error='Topic not found'),404
    phase=db.session.get(Phase,topic.phase_id)
    roadmap=db.session.get(Roadmap,phase.roadmap_id) if phase else None
    if not roadmap or roadmap.user_id!=uid: return jsonify(error='Forbidden'),403
    prog=TopicProgress.query.filter_by(user_id=uid,topic_id=tid).first()
    if not prog: prog=TopicProgress(user_id=uid,topic_id=tid); db.session.add(prog)
    prog.completed=not bool(prog.completed); prog.completed_at=datetime.utcnow() if prog.completed else None
    db.session.commit(); db.session.add(UserActivity(user_id=uid,text=f'{"Completed" if prog.completed else "Reopened"} topic: {topic.name}')); db.session.commit()
    return jsonify(completed=prog.completed)

@app.get('/api/progress/dashboard')
@jwt_required()
def dashboard():
    uid=int(get_jwt_identity()); p=Profile.query.filter_by(user_id=uid).first()
    career=p.career_goal if p and p.career_goal else 'Data Analyst'
    r=Roadmap.query.filter_by(user_id=uid,career_goal=career).order_by(Roadmap.created_at.desc()).first()
    total=completed=0; phases=[]
    if r:
        for ph in Phase.query.filter_by(roadmap_id=r.id).all():
            topics=Topic.query.filter_by(phase_id=ph.id).all()
            topic_progress=[]
            for topic in topics:
                is_completed=TopicProgress.query.filter_by(user_id=uid,topic_id=topic.id,completed=True).first() is not None
                topic_progress.append({'id':topic.id,'name':topic.name,'completed':is_completed})
            phase_completed=sum(1 for topic in topic_progress if topic['completed'])
            total+=len(topics); completed+=phase_completed
            phases.append({
                'name':ph.title,
                'completed':phase_completed,
                'total':len(topics),
                'completion':round(phase_completed/len(topics)*100) if topics else 0,
                'topics':topic_progress,
            })
    hours=sum(s.actual_minutes for s in StudySession.query.filter_by(user_id=uid).all())/60
    streak=0
    today=datetime.utcnow().date()
    for i in range(30):
        date=(today-timedelta(days=i)).isoformat()
        if StudySession.query.filter_by(user_id=uid,date=date,completed=True).first(): streak+=1
        else: break
    activities=UserActivity.query.filter_by(user_id=uid).order_by(UserActivity.created_at.desc()).limit(5).all()
    milestones=Milestone.query.filter_by(user_id=uid,completed=False).count()
    return jsonify({'welcome':(User.query.get(uid)).name,'career_goal':p.career_goal if p else '','overall_progress':round(completed/total*100) if total else 0,'completed_topics':completed,'total_topics':total,'learning_hours':round(hours,1),'streak':streak,'completed_milestones':Milestone.query.filter_by(user_id=uid,completed=True).count(),'upcoming_milestones':milestones,'phases':phases,'activities':[{'text':a.text,'date':a.created_at.strftime('%Y-%m-%d')} for a in activities]})

@app.get('/api/milestones')
@jwt_required()
def get_milestones():
    uid=int(get_jwt_identity()); items=Milestone.query.filter_by(user_id=uid).all(); return jsonify([{'id':m.id,'title':m.title,'target_date':m.target_date,'completed':m.completed,'completed_at':m.completed_at.isoformat() if m.completed_at else None} for m in items])

@app.post('/api/milestones')
@jwt_required()
def create_milestone():
    uid=int(get_jwt_identity()); d=request.get_json(silent=True) or {}; m=Milestone(user_id=uid,title=d.get('title','Custom milestone'),target_date=d.get('target_date','')); db.session.add(m); db.session.commit(); return jsonify({'id':m.id,'title':m.title,'target_date':m.target_date,'completed':False}),201

@app.put('/api/milestones/<int:mid>')
@jwt_required()
def update_milestone(mid):
    uid=int(get_jwt_identity()); m=Milestone.query.get_or_404(mid)
    if m.user_id!=uid:return jsonify(error='Forbidden'),403
    d=request.get_json(silent=True) or {}; m.completed=bool(d.get('completed',m.completed)); m.completed_at=datetime.utcnow() if m.completed else None; db.session.commit(); return jsonify({'id':m.id,'completed':m.completed})

@app.get('/api/study-sessions')
@jwt_required()
def get_sessions():
    uid=int(get_jwt_identity()); items=StudySession.query.filter_by(user_id=uid).order_by(StudySession.date).all(); return jsonify([{'id':s.id,'date':s.date,'topic':s.topic,'planned_minutes':s.planned_minutes,'actual_minutes':s.actual_minutes,'completed':s.completed} for s in items])

@app.post('/api/study-sessions')
@jwt_required()
def create_session():
    uid=int(get_jwt_identity()); d=request.get_json(silent=True) or {}; s=StudySession(user_id=uid,date=d.get('date',''),topic=d.get('topic','Study session'),planned_minutes=int(d.get('planned_minutes',60)),actual_minutes=int(d.get('actual_minutes',0)),completed=bool(d.get('completed',False))); db.session.add(s); db.session.commit(); return jsonify({'id':s.id,'date':s.date,'topic':s.topic,'planned_minutes':s.planned_minutes,'actual_minutes':s.actual_minutes,'completed':s.completed}),201

@app.put('/api/study-sessions/<int:sid>')
@jwt_required()
def update_session(sid):
    uid=int(get_jwt_identity()); s=StudySession.query.get_or_404(sid)
    if s.user_id!=uid:return jsonify(error='Forbidden'),403
    d=request.get_json(silent=True) or {}
    for k in ('date','topic','planned_minutes','actual_minutes','completed'):
        if k in d:setattr(s,k,d[k])
    db.session.commit(); return jsonify({'id':s.id,'completed':s.completed})

@app.delete('/api/study-sessions/<int:sid>')
@jwt_required()
def delete_session(sid):
    uid=int(get_jwt_identity()); s=StudySession.query.get_or_404(sid)
    if s.user_id!=uid:return jsonify(error='Forbidden'),403
    db.session.delete(s); db.session.commit(); return '',204

if __name__=='__main__': app.run(host='0.0.0.0',port=5000,debug=True)
