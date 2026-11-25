import sys
from pathlib import Path
import os

os.environ['DATABASE_URL'] = 'sqlite://'
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import app, db, User, Profile, Roadmap, Phase, Topic, CAREERS, CAREER_PHASES
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash


def client():
    app.config.update(TESTING=True)
    with app.app_context():
        db.drop_all(); db.create_all()
    return app.test_client()


def test_demo_login():
    c=client()
    r=c.post('/api/auth/login', json={'email':'demo@pathfinder.ai','password':'demo123'})
    assert r.status_code == 401


def test_careers():
    c=client(); r=c.get('/api/careers')
    assert r.status_code == 200


def test_career_roadmap_plans_are_distinct():
    assert {career[0] for career in CAREERS} == set(CAREER_PHASES)
    assert CAREER_PHASES['Data Analyst'] != CAREER_PHASES['Data Scientist']
    assert CAREER_PHASES['Data Scientist'] != CAREER_PHASES['AI Engineer']
    assert CAREER_PHASES['Full Stack Developer'] != CAREER_PHASES['Cloud Engineer']
    assert len({
        tuple((title, tuple(topics)) for title, _, topics in phases)
        for phases in CAREER_PHASES.values()
    }) == len(CAREER_PHASES)


def test_each_career_goal_generates_its_own_roadmap():
    c=client()
    with app.app_context():
        user=User(name='Test Student',email='all-careers@example.com',password_hash=generate_password_hash('secret1'))
        db.session.add(user); db.session.flush()
        db.session.add(Profile(user_id=user.id,career_goal='Data Analyst',skills=[]))
        db.session.commit()
        token=create_access_token(identity=str(user.id))

    headers={'Authorization':f'Bearer {token}'}
    generated={}
    for career in CAREER_PHASES:
        c.put('/api/profile',headers=headers,json={'career_goal':career})
        response=c.post('/api/roadmap/generate',headers=headers)
        assert response.status_code==201
        roadmap=response.get_json()['roadmap']
        assert roadmap['career_goal']==career
        generated[career]=tuple(
            (phase['title'],tuple(topic['name'] for topic in phase['topics']))
            for phase in roadmap['phases']
        )

    assert len(set(generated.values()))==len(CAREER_PHASES)


def test_generate_replaces_stale_saved_roadmap_for_same_career():
    c=client()
    with app.app_context():
        user=User(name='Test Student',email='stale-plan@example.com',password_hash=generate_password_hash('secret1'))
        db.session.add(user); db.session.flush()
        db.session.add(Profile(user_id=user.id,career_goal='AI Engineer',skills=[]))
        db.session.flush()
        stale=Roadmap(user_id=user.id,title='Personalized AI Engineer Roadmap',career_goal='AI Engineer')
        db.session.add(stale); db.session.flush()
        phase=Phase(roadmap_id=stale.id,number=1,title='Advanced Python',description='Old generic plan')
        db.session.add(phase); db.session.flush()
        db.session.add(Topic(phase_id=phase.id,name='Python advanced concepts'))
        db.session.commit()
        token=create_access_token(identity=str(user.id))

    headers={'Authorization':f'Bearer {token}'}
    response=c.post('/api/roadmap/generate',headers=headers)
    roadmap=response.get_json()['roadmap']
    assert response.status_code==201
    assert roadmap['phases'][0]['title']=='AI and Python Foundations'
    assert roadmap['phases'][0]['topics'][0]['name']=='Python for AI'


def test_roadmap_changes_when_career_goal_changes():
    c=client()
    with app.app_context():
        user=User(name='Test Student',email='test@example.com',password_hash=generate_password_hash('secret1'))
        db.session.add(user); db.session.flush()
        db.session.add(Profile(user_id=user.id,career_goal='Data Analyst',skills=['Python']))
        db.session.commit()
        token=create_access_token(identity=str(user.id))

    headers={'Authorization':f'Bearer {token}'}
    first=c.post('/api/roadmap/generate',headers=headers).get_json()['roadmap']
    assert first['career_goal']=='Data Analyst'
    assert first['phases'][0]['title']=='Advanced Python and Pandas'
    first_topic=first['phases'][0]['topics'][0]['id']
    assert c.post('/api/progress/topic',headers=headers,json={'topic_id':first_topic}).get_json()['completed'] is True

    c.put('/api/profile',headers=headers,json={'career_goal':'Data Scientist'})
    assert c.get('/api/roadmap',headers=headers).get_json()['roadmap'] is None
    second_response=c.post('/api/roadmap/generate',headers=headers)
    second=second_response.get_json()['roadmap']
    assert second_response.status_code==201
    assert second['career_goal']=='Data Scientist'
    assert second['phases'][0]['title']=='Data Science with Python'
    saved_data_analyst=c.get('/api/roadmap?career_goal=Data%20Analyst',headers=headers).get_json()['roadmap']
    assert saved_data_analyst['id']==first['id']
    assert saved_data_analyst['phases'][0]['topics'][0]['completed'] is True
    dashboard=c.get('/api/progress/dashboard',headers=headers).get_json()
    assert dashboard['career_goal']=='Data Scientist'
    assert dashboard['phases'][0]['name']=='Data Science with Python'
    assert dashboard['phases'][0]['topics'][0]=={
        'id':second['phases'][0]['topics'][0]['id'],
        'name':'Python for data science',
        'completed':False,
    }

    reused=c.post('/api/roadmap/generate',headers=headers)
    assert reused.status_code==200
    assert reused.get_json()['roadmap']['id']==second['id']
    second_topic=second['phases'][0]['topics'][0]['id']
    assert c.get('/api/roadmap',headers=headers).get_json()['roadmap']['phases'][0]['topics'][0]['completed'] is False
    c.post('/api/progress/topic',headers=headers,json={'topic_id':second_topic})
    c.post('/api/roadmap/regenerate',headers=headers)

    c.put('/api/profile',headers=headers,json={'career_goal':'Data Analyst'})
    restored=c.get('/api/roadmap',headers=headers).get_json()['roadmap']
    assert restored['id']==first['id']
    assert restored['phases'][0]['topics'][0]['completed'] is True
    dashboard=c.get('/api/progress/dashboard',headers=headers).get_json()
    assert dashboard['career_goal']=='Data Analyst'
    assert dashboard['phases'][0]['name']=='Advanced Python and Pandas'
    assert dashboard['phases'][0]['completion']==33
    assert dashboard['phases'][0]['topics'][0]['name']=='Pandas dataframes'
    assert dashboard['phases'][0]['topics'][0]['completed'] is True
    assert dashboard['phases'][0]['topics'][1]['completed'] is False


def test_users_cannot_update_another_users_topic_progress():
    c=client()
    with app.app_context():
        users=[]
        for email in ('one@example.com','two@example.com'):
            user=User(name='Student',email=email,password_hash=generate_password_hash('secret1'))
            db.session.add(user); db.session.flush()
            db.session.add(Profile(user_id=user.id,career_goal='Data Analyst'))
            users.append(user.id)
        db.session.commit()
        token=create_access_token(identity=str(users[0]))
        other_token=create_access_token(identity=str(users[1]))
    owner_headers={'Authorization':f'Bearer {token}'}
    other_headers={'Authorization':f'Bearer {other_token}'}
    topic_id=c.post('/api/roadmap/generate',headers=owner_headers).get_json()['roadmap']['phases'][0]['topics'][0]['id']
    assert c.post('/api/progress/topic',headers=other_headers,json={'topic_id':topic_id}).status_code==403
