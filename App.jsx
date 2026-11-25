import { useEffect, useMemo, useRef, useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate, Link, useNavigate } from 'react-router-dom'
import axios from 'axios'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { LayoutDashboard, UserRound, Compass, ClipboardCheck, Route as RouteIcon, Library, CalendarDays, Trophy, LogOut, Menu, X, ArrowRight, CheckCircle2, Clock3, Flame, TrendingUp, Bookmark, ExternalLink } from 'lucide-react'
import './index.css'

const api = axios.create({ baseURL: 'http://localhost:5000/api' })
api.interceptors.request.use(config => { const token=localStorage.getItem('pf_token'); if(token) config.headers.Authorization=`Bearer ${token}`; return config })

function Button({children,variant='primary',...props}){ return <button className={`btn btn-${variant}`} {...props}>{children}</button> }
function Logo(){ return <Link className="logo" to="/"><div className="logo-mark">P</div><span>PathFinder <b>AI</b></span></Link> }

function Landing(){
 const navigate=useNavigate();
 return <div className="landing">
  <nav><Logo/><div className="nav-links"><a href="#features">Features</a><a href="#careers">Careers</a><a href="#how">How it works</a></div><div className="nav-actions"><Link to="/login" className="link-btn">Log in</Link><Link to="/register" className="btn btn-primary small">Get Started</Link></div></nav>
  <main>
   <section className="hero-section"><div className="hero-copy"><div className="eyebrow">AI-powered learning journeys</div><h1>Build Your Future,<br/><span>One Skill at a Time.</span></h1><p>Your Skills. Your Goals. Your Personalized Journey.</p><div className="hero-actions"><Button onClick={()=>navigate('/register')}>Get Started <ArrowRight size={18}/></Button><Button variant="secondary" onClick={()=>navigate('/careers')}>Explore Careers</Button></div></div><div className="hero-visual"><div className="glow"></div><div className="progress-card"><div className="mini-head"><b>Data Analyst Path</b><span>68%</span></div><div className="progress-track"><div style={{width:'68%'}}></div></div><div className="mini-steps"><div><CheckCircle2/>Python & Pandas</div><div><CheckCircle2/>SQL Foundations</div><div className="active-step"><Clock3/>Statistics</div></div></div></div></section>
   <section id="features" className="features"><div className="section-title"><span>Everything you need</span><h2>Turn ambition into a clear plan</h2></div><div className="feature-grid"><Feature icon={<Compass/>} title="Personalized Roadmaps" text="Receive a learning path tailored to your skills, pace and career goal."/><Feature icon={<ClipboardCheck/>} title="Skill Assessments" text="Identify strengths and knowledge gaps with focused assessments."/><Feature icon={<TrendingUp/>} title="Progress Tracking" text="Visualize milestones and stay consistent with practical weekly planning."/></div></section>
   <section id="careers" className="career-strip"><div><span>Popular career paths</span><h2>Find the direction that fits you</h2></div><div className="career-pills"><span>Data Analyst</span><span>AI Engineer</span><span>Full Stack Developer</span><span>Cloud Engineer</span></div></section>
   <section id="how" className="how"><div className="section-title"><span>How it works</span><h2>Four steps from goal to growth</h2></div><div className="steps"><Step n="1" title="Build your profile"/><Step n="2" title="Take an assessment"/><Step n="3" title="Get your roadmap"/><Step n="4" title="Learn and progress"/></div></section>
   <section className="testimonials"><div className="quote">“PathFinder helped me turn a broad career goal into a realistic weekly plan.”<b>— Sample Student Review</b></div><div className="quote">“The visual skill-gap analysis made it clear what I needed to learn next.”<b>— Sample Learner Review</b></div></section>
  </main><footer><Logo/><span>© 2026 PathFinder AI · Learning demo</span></footer>
 </div>
}
function Feature({icon,title,text}){return <div className="feature"><div className="feature-icon">{icon}</div><h3>{title}</h3><p>{text}</p></div>}
function Step({n,title}){return <div className="step"><div>{n}</div><h3>{title}</h3></div>}

function AuthPage({mode}){
 const register=mode==='register'; const [form,setForm]=useState({name:'',email:'',password:'',confirm:'',education:'',college:''}); const [error,setError]=useState(''); const [loading,setLoading]=useState(false); const navigate=useNavigate();
 const submit=async(e)=>{e.preventDefault();setError('');if(register&&form.password!==form.confirm)return setError('Passwords do not match');setLoading(true);try{const res=await api.post(register?'/auth/register':'/auth/login',register?form:{email:form.email,password:form.password});localStorage.setItem('pf_token',res.data.token);navigate('/dashboard')}catch(e){setError(e.response?.data?.error||'Unable to continue')}finally{setLoading(false)}}
 const demo=async()=>{setLoading(true);try{const res=await api.post('/auth/login',{email:'demo@pathfinder.ai',password:'demo123'});localStorage.setItem('pf_token',res.data.token);navigate('/dashboard')}catch(e){setError('Start the backend to use demo login')}finally{setLoading(false)}}
 return <div className="auth-page"><div className="auth-side"><Logo/><div><h1>{register?'Start your journey':'Welcome back'}</h1><p>A focused roadmap is waiting for you.</p></div><div className="auth-card-mini"><b>Demo account</b><span>demo@pathfinder.ai</span><span>Password: demo123</span></div></div><form className="auth-form" onSubmit={submit}><h2>{register?'Create account':'Log in to PathFinder'}</h2>{error&&<div className="alert">{error}</div>}{register&&<><label>Full name<input required value={form.name} onChange={e=>setForm({...form,name:e.target.value})}/></label><div className="form-grid"><label>Education level<select value={form.education} onChange={e=>setForm({...form,education:e.target.value})}><option>Undergraduate</option><option>Postgraduate</option><option>Graduate</option></select></label><label>College<input value={form.college} onChange={e=>setForm({...form,college:e.target.value})}/></label></div></>}<label>Email address<input type="email" required value={form.email} onChange={e=>setForm({...form,email:e.target.value})}/></label><label>Password<input type="password" required minLength={6} value={form.password} onChange={e=>setForm({...form,password:e.target.value})}/></label>{register&&<label>Confirm password<input type="password" required value={form.confirm} onChange={e=>setForm({...form,confirm:e.target.value})}/></label>}<Button disabled={loading}>{loading?'Please wait':register?'Create Account':'Log in'}</Button><Button type="button" variant="secondary" onClick={demo}>Use demo account</Button><p className="switch-auth">{register?'Already have an account?':'New to PathFinder?'} <Link to={register?'login':'register'}>{register?'Log in':'Create account'}</Link></p></form></div>
}

function Protected({children}){ return localStorage.getItem('pf_token')?children:<Navigate to="/login" replace/> }

function Layout({children}){
 const [open,setOpen]=useState(false); const navigate=useNavigate(); const logout=()=>{localStorage.removeItem('pf_token');navigate('/')};
 const items=[['Dashboard','/dashboard',<LayoutDashboard/>],['My Profile','/profile',<UserRound/>],['Career Goals','/careers',<Compass/>],['Assessment','/assessment',<ClipboardCheck/>],['My Roadmap','/roadmap',<RouteIcon/>],['Resources','/resources',<Library/>],['Study Planner','/planner',<CalendarDays/>],['Milestones','/milestones',<Trophy/>]];
 return <div className="app-shell"><aside className={open?'open':''}><Logo/><button className="mobile-close" onClick={()=>setOpen(false)}><X/></button><nav>{items.map(([label,to,icon])=><Link key={to} to={to} onClick={()=>setOpen(false)}>{icon}<span>{label}</span></Link>)}</nav><button className="logout" onClick={logout}><LogOut/><span>Log out</span></button></aside><div className="main-shell"><header><button className="menu-btn" onClick={()=>setOpen(true)}><Menu/></button><div className="header-search">PathFinder AI</div><div className="avatar">DS</div></header><main className="content">{children}</main></div></div>
}

function PageHeader({title,subtitle,action}){return <div className="page-head"><div><h1>{title}</h1>{subtitle&&<p>{subtitle}</p>}</div>{action}</div>}

function Dashboard(){
 const [d,setD]=useState(null);
 useEffect(()=>{api.get('/progress/dashboard').then(r=>setD(r.data)).catch(()=>{})},[]);
 if(!d)return <Skeleton/>;
 const chart=d.phases.map(p=>({name:p.name.replace(/^(Phase|Advanced|Python|SQL)/,'').slice(0,12),progress:p.completion}));
 return <>
  <PageHeader title={`Welcome back, ${d.welcome}`} subtitle="Here is your learning progress"/>
  <div className="stat-grid"><Stat icon={<TrendingUp/>} label="Overall progress" value={`${d.overall_progress}%`}/><Stat icon={<CheckCircle2/>} label="Completed topics" value={`${d.completed_topics}/${d.total_topics}`}/><Stat icon={<Clock3/>} label="Learning hours" value={d.learning_hours}/><Stat icon={<Flame/>} label="Current streak" value={`${d.streak} days`}/></div>
  <div className="dashboard-grid"><div className="card chart-card"><h3>Phase progress</h3>{chart.length?<ResponsiveContainer width="100%" height={220}><BarChart data={chart}><XAxis dataKey="name"/><YAxis/><Tooltip/><Bar dataKey="progress" fill="#4f46e5" radius={[6,6,0,0]}/></BarChart></ResponsiveContainer>:<Empty text="Generate your career roadmap to see progress"/>}</div><div className="card"><h3>Career goal</h3><div className="career-focus"><Compass/><div><span>Current path</span><b>{d.career_goal||'Choose a career'}</b></div></div><Link className="text-link" to="/roadmap">View roadmap →</Link></div></div>
  <section className="card activity">
   <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',gap:12,flexWrap:'wrap'}}><div><h3 style={{marginBottom:4}}>Course progress</h3><p style={{margin:0,color:'#667085'}}>Completed learning content for {d.career_goal||'your selected career'}</p></div><Link className="text-link" to="/careers">Change career →</Link></div>
   {d.phases.length?d.phases.map((phase,index)=><article key={`${phase.name}-${index}`} style={{borderTop:'1px solid #edf0f5',marginTop:16,paddingTop:16}}>
    <div style={{display:'flex',justifyContent:'space-between',gap:12,alignItems:'center',flexWrap:'wrap'}}><b>{phase.name}</b><span style={{color:'#667085'}}>{phase.completed}/{phase.total} topics · {phase.completion}%</span></div>
    <div style={{height:6,background:'#eef0f5',borderRadius:8,marginTop:10,overflow:'hidden'}}><div style={{width:`${phase.completion}%`,height:'100%',background:'#4f46e5',borderRadius:8}}/></div>
    {phase.topics.some(topic=>topic.completed)?<ul style={{margin:'12px 0 0',paddingLeft:20,color:'#344054'}}>{phase.topics.filter(topic=>topic.completed).map(topic=><li key={topic.id} style={{padding:'3px 0'}}><CheckCircle2 size={15} style={{verticalAlign:'middle',color:'#16a34a',marginRight:7}}/>{topic.name}</li>)}</ul>:<p style={{margin:'10px 0 0',color:'#98a2b3',fontSize:13}}>No completed topics in this course yet.</p>}
   </article>):<Empty text="Generate a roadmap for this career to see course progress"/>}
  </section>
  <div className="card activity"><h3>Recent activities</h3>{d.activities.length?d.activities.map((a,i)=><div className="activity-row" key={i}><div className="activity-dot"></div><span>{a.text}</span><small>{a.date}</small></div>):<Empty text="Complete an activity to see it here"/>}</div>
 </>
}
function Stat({icon,label,value}){return <div className="stat"><div>{icon}</div><span>{label}</span><b>{value}</b></div>}
function Skeleton(){return <div className="skeleton-grid"><div/><div/><div/><div/></div>}
function Empty({text}){return <div className="empty">{text}</div>}

function Profile(){const [p,setP]=useState({degree:'',branch:'',college:'',graduation_year:'',skills:[],career_goal:'',experience:'Beginner',learning_style:'Mixed',hours_per_day:2,days_per_week:5,duration:'12 weeks'});const [saved,setSaved]=useState(false);useEffect(()=>{api.get('/profile').then(r=>setP(r.data.profile)).catch(()=>{})},[]);const skillOptions=['Python','Java','C','C++','JavaScript','SQL','MySQL','PostgreSQL','Excel','Statistics','Power BI','Tableau','HTML','CSS','React','Flask','Machine Learning','Deep Learning','Generative AI','AWS','Azure','Google Cloud'];const toggle=s=>setP({...p,skills:p.skills.includes(s)?p.skills.filter(x=>x!==s):[...p.skills,s]});const submit=async(e)=>{e.preventDefault();await api.put('/profile',p);setSaved(true);setTimeout(()=>setSaved(false),2500)};return <><PageHeader title="My Profile" subtitle="Tell us about your background and goals"/><form className="card profile-form" onSubmit={submit}><div className="form-grid"><label>Degree<input value={p.degree||''} onChange={e=>setP({...p,degree:e.target.value})}/></label><label>Branch<input value={p.branch||''} onChange={e=>setP({...p,branch:e.target.value})}/></label><label>College<input value={p.college||''} onChange={e=>setP({...p,college:e.target.value})}/></label><label>Graduation year<input type="number" value={p.graduation_year||''} onChange={e=>setP({...p,graduation_year:e.target.value})}/></label></div><label>Existing skills</label><div className="skill-picker">{skillOptions.map(s=><button type="button" className={p.skills?.includes(s)?'selected':''} key={s} onClick={()=>toggle(s)}>{s}</button>)}</div><label><input className="custom-skill" placeholder="Add a custom skill (comma separated)" onBlur={e=>{const vals=e.target.value.split(',').map(x=>x.trim()).filter(Boolean);if(vals.length)setP({...p,skills:[...new Set([...(p.skills||[]),...vals])]});e.target.value=''}}/></label><div className="form-grid"><label>Experience<select value={p.experience||'Beginner'} onChange={e=>setP({...p,experience:e.target.value})}><option>Beginner</option><option>Intermediate</option><option>Advanced</option></select></label><label>Learning style<select value={p.learning_style||'Mixed'} onChange={e=>setP({...p,learning_style:e.target.value})}><option>Visual</option><option>Reading</option><option>Hands-on</option><option>Mixed</option></select></label><label>Hours per day<input type="number" min="1" max="12" value={p.hours_per_day||2} onChange={e=>setP({...p,hours_per_day:Number(e.target.value)})}/></label><label>Days per week<input type="number" min="1" max="7" value={p.days_per_week||5} onChange={e=>setP({...p,days_per_week:Number(e.target.value)})}/></label></div><Button>{saved?'Saved successfully':'Save profile'}</Button></form></>
}

function Careers(){
 const [careers,setCareers]=useState([]);
 const [selected,setSelected]=useState('');
 const [roadmap,setRoadmap]=useState(null);
 const [loading,setLoading]=useState(false);
 const [error,setError]=useState('');
 const selectionRequest=useRef(0);
 useEffect(()=>{
  const initialRequest=++selectionRequest.current;
  api.get('/careers').then(r=>setCareers(r.data)).catch(()=>setError('Could not load career paths.'));
  api.get('/profile').then(async r=>{
   if(initialRequest!==selectionRequest.current)return;
   const career=r.data.profile.career_goal||'';
   setSelected(career);
   if(career){
    try{const response=await api.get('/roadmap',{params:{career_goal:career}});if(initialRequest===selectionRequest.current)setRoadmap(response.data.roadmap)}catch{if(initialRequest===selectionRequest.current)setError('Could not load your saved course progress.')}
   }
  }).catch(()=>{if(initialRequest===selectionRequest.current)setError('Could not load your selected career.')});
 },[]);
 const select=async career=>{
  const request=++selectionRequest.current;
  setSelected(career);setRoadmap(null);setLoading(true);setError('');
  try{
   await api.put('/profile',{career_goal:career});
   let response=await api.get('/roadmap',{params:{career_goal:career}});
   if(!response.data.roadmap)response=await api.post('/roadmap/generate',{career_goal:career});
   if(request===selectionRequest.current)setRoadmap(response.data.roadmap);
  }catch{if(request===selectionRequest.current)setError('Could not load this career path. Please try again.')}
  finally{if(request===selectionRequest.current)setLoading(false)}
 };
 const toggleTopic=async topicId=>{
  const request=selectionRequest.current;
  const career=selected;
  try{
   await api.post('/progress/topic',{topic_id:topicId});
   const response=await api.get('/roadmap',{params:{career_goal:career}});
   if(request===selectionRequest.current)setRoadmap(response.data.roadmap);
  }catch{if(request===selectionRequest.current)setError('Could not update topic progress. Please try again.')}
 };
 const topics=roadmap?.phases.flatMap(phase=>phase.topics)||[];
 const completed=topics.filter(topic=>topic.completed).length;
 const overall=topics.length?Math.round(completed/topics.length*100):0;
 return <>
  <PageHeader title="Choose a Career Goal" subtitle="Select a path to see its courses and your progress"/>
  <div className="career-grid">{careers.map(c=><button key={c.id} className={`career-card ${selected===c.title?'selected':''}`} disabled={loading} onClick={()=>select(c.title)}><div className="career-card-top"><Compass/><span>{c.difficulty}</span></div><h3>{c.title}</h3><p>{c.description}</p><div className="skill-tags">{c.skills.slice(0,4).map(s=><span key={s}>{s}</span>)}</div><b>{c.duration}</b></button>)}</div>
  {error&&<div className="alert" role="alert">{error}</div>}
  {selected&&<section className="card" style={{marginTop:20}} aria-live="polite">
   <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',gap:16,flexWrap:'wrap'}}>
    <div><h2 style={{margin:'0 0 6px'}}>{selected} courses</h2><p style={{margin:0,color:'#667085'}}>{loading?'Loading your course progress…':roadmap?`${completed} of ${topics.length} topics complete`:'Preparing this learning path'}</p></div>
    {roadmap&&<strong style={{color:'#4f46e5',fontSize:20}}>{overall}% complete</strong>}
   </div>
   {roadmap&&<div style={{height:8,background:'#eef0f5',borderRadius:8,marginTop:14,overflow:'hidden'}}><div style={{width:`${overall}%`,height:'100%',background:'#4f46e5',borderRadius:8,transition:'width .2s'}}/></div>}
   {loading&&!roadmap&&<Skeleton/>}
   {roadmap?.phases.map(phase=><article className="phase card" key={phase.id} style={{marginTop:14}}>
    <div style={{display:'flex',justifyContent:'space-between',alignItems:'flex-start',gap:12,flexWrap:'wrap'}}>
     <div><h3 style={{margin:'0 0 6px'}}>{phase.number}. {phase.title}</h3><p style={{margin:0,color:'#667085'}}>{phase.description}</p></div>
     <strong style={{color:'#4f46e5',whiteSpace:'nowrap'}}>{phase.completion}% · {phase.topics.filter(topic=>topic.completed).length}/{phase.topics.length} topics</strong>
    </div>
    <div style={{height:6,background:'#eef0f5',borderRadius:8,marginTop:12,overflow:'hidden'}}><div style={{width:`${phase.completion}%`,height:'100%',background:'#4f46e5',borderRadius:8}}/></div>
    <div className="topics">{phase.topics.map(topic=><div className="topic" key={topic.id}>
     <button type="button" className={topic.completed?'topic-check done':'topic-check'} aria-label={`${topic.completed?'Reopen':'Complete'} ${topic.name}`} onClick={()=>toggleTopic(topic.id)}><CheckCircle2/></button>
     <div><b>{topic.name}</b><p>{topic.explanation}</p><div className="topic-footer"><span><Clock3/> {topic.duration} min</span><button type="button" onClick={()=>toggleTopic(topic.id)}>{topic.completed?'Reopen topic':'Mark complete'}</button></div></div>
    </div>)}</div>
   </article>)}
   {roadmap&&!roadmap.phases.length&&<Empty text="No courses found for this career path"/>}
  </section>}
 </>
}

function Assessment(){const [qs,setQs]=useState([]);const [career,setCareer]=useState('');const [index,setIndex]=useState(0);const [answers,setAnswers]=useState({});const [result,setResult]=useState(null);useEffect(()=>{api.get('/assessment/questions').then(r=>{setQs(r.data.questions);setCareer(r.data.career)}).catch(()=>{})},[]);const submit=async()=>{const r=await api.post('/assessment/submit',{answers});setResult(r.data)};if(result)return <><PageHeader title="Assessment Results" subtitle={`${career} · ${result.score}% score`}/><div className="card result-card"><div className="score-ring">{result.score}%</div><h2>{result.correct} of {result.total} correct</h2><div className="result-list">{result.results.map((x,i)=><div key={i}><CheckCircle2 className={x.correct?'ok':'bad'}/><div><b>{x.skill}</b><p>{x.correct?'Correct':`Correct answer: ${x.answer}`}</p><small>{x.explanation}</small></div></div>)}</div><Button onClick={()=>{setResult(null);setIndex(0);setAnswers({})}}>Retake assessment</Button></div></>;if(!qs.length)return <Skeleton/>;const q=qs[index];return <><PageHeader title={`${career} Assessment`} subtitle="Answer each question honestly"/><div className="assessment-card card"><div className="assessment-progress"><span>Question {index+1} of {qs.length}</span><div><i style={{width:`${((index+1)/qs.length)*100}%`}}/></div></div><h2>{q.question}</h2><div className="options">{q.options.map(o=><button key={o} className={answers[q.id]==o?'selected':''} onClick={()=>setAnswers({...answers,[q.id]:o})}>{o}</button>)}</div><div className="assessment-actions"><Button variant="secondary" disabled={index===0} onClick={()=>setIndex(index-1)}>Previous</Button>{index<qs.length-1?<Button disabled={!answers[q.id]} onClick={()=>setIndex(index+1)}>Next</Button>:<Button disabled={!answers[q.id]} onClick={submit}>Submit assessment</Button>}</div></div></>}

function Roadmap(){const [roadmap,setRoadmap]=useState(null);const [open,setOpen]=useState({});useEffect(()=>{void load()},[]);const load=()=>api.get('/roadmap').then(r=>setRoadmap(r.data.roadmap)).catch(()=>{});const generate=async()=>{const r=await api.post('/roadmap/generate');setRoadmap(r.data.roadmap)};const regenerate=async()=>{if(confirm('Regenerate this roadmap?')){const r=await api.post('/roadmap/regenerate');setRoadmap(r.data.roadmap)}};const toggleTopic=async(tid)=>{await api.post('/progress/topic',{topic_id:tid});load()};if(!roadmap)return <><PageHeader title="My Learning Roadmap" subtitle="A personalized path for your career goal"/><div className="card empty-roadmap"><RouteIcon/><h2>No roadmap yet</h2><p>Generate a roadmap based on your profile and career goal.</p><Button onClick={generate}>Generate roadmap</Button></div></>;const topics=roadmap.phases.flatMap(p=>p.topics);const done=topics.filter(t=>t.completed).length;const pct=topics.length?Math.round(done/topics.length*100):0;return <><PageHeader title={roadmap.title} subtitle={`${roadmap.source==='demo'?'Rule-based demo roadmap':roadmap.source} · ${roadmap.estimated_duration}`} action={<Button variant="secondary" onClick={regenerate}>Regenerate</Button>}/><div className="roadmap-summary card"><div className="score-ring small-ring">{pct}%</div><div><b>{done} of {topics.length} topics completed</b><p>{roadmap.introduction}</p></div></div><div className="timeline">{roadmap.phases.map(ph=><div className="phase card" key={ph.id}><button className="phase-head" onClick={()=>setOpen({...open,[ph.id]:open[ph.id]===false?true:!(open[ph.id]??true)})}><div className="phase-number">{ph.number}</div><div><h3>{ph.title}</h3><p>{ph.description}</p></div><div className="phase-meta"><span>{ph.completion}%</span><i style={{width:`${ph.completion}%`}}/></div></button>{(open[ph.id]??true)&&<div className="topics">{ph.topics.map(t=><div className="topic" key={t.id}><button className={t.completed?'topic-check done':'topic-check'} onClick={()=>toggleTopic(t.id)}><CheckCircle2/></button><div><b>{t.name}</b><p>{t.explanation}</p><div className="topic-footer"><span><Clock3/> {t.duration} min</span><button onClick={()=>toggleTopic(t.id)}>{t.completed?'Reopen topic':'Mark complete'}</button></div></div></div>)}</div>}</div>)}</div></>
}

function Resources(){const [items,setItems]=useState([]);const [q,setQ]=useState('');const [category,setCategory]=useState('');useEffect(()=>{load()},[q,category]);const load=()=>api.get('/resources',{params:{q,category}}).then(r=>setItems(r.data)).catch(()=>{});const save=async(id)=>{await api.post('/resources/save',{resource_id:id})};return <><PageHeader title="Learning Resources" subtitle="Curated, legitimate learning materials"/><div className="resource-tools"><input placeholder="Search resources" value={q} onChange={e=>setQ(e.target.value)}/><select value={category} onChange={e=>setCategory(e.target.value)}><option value="">All categories</option>{['Python','SQL','Excel','Statistics','Power BI','React','Flask','AWS','Machine Learning','Generative AI'].map(c=><option key={c}>{c}</option>)}</select></div><div className="resource-grid">{items.map(r=><article className="resource-card card" key={r.id}><div className="resource-top"><span>{r.category}</span><button onClick={()=>save(r.id)} title="Save resource"><Bookmark/></button></div><h3>{r.title}</h3><p>{r.description}</p><div className="resource-meta"><span>{r.platform}</span><span>{r.difficulty}</span><span>{r.free?'Free':'Paid'}</span></div><a href={r.url} target="_blank" rel="noreferrer">Open resource <ExternalLink/></a></article>)}</div></>}

function Planner(){const [sessions,setSessions]=useState([]);const [form,setForm]=useState({date:new Date().toISOString().slice(0,10),topic:'',planned_minutes:60,actual_minutes:0,completed:false});useEffect(()=>{void load()},[]);const load=()=>api.get('/study-sessions').then(r=>setSessions(r.data)).catch(()=>{});const submit=async(e)=>{e.preventDefault();await api.post('/study-sessions',form);setForm({...form,topic:''});load()};const toggle=async(s)=>{await api.put(`/study-sessions/${s.id}`,{completed:!s.completed});load()};const remove=async(id)=>{await api.delete(`/study-sessions/${id}`);load()};const summary=sessions.reduce((a,s)=>({planned:a.planned+Number(s.planned_minutes),actual:a.actual+Number(s.actual_minutes),done:a.done+(s.completed?1:0)}),{planned:0,actual:0,done:0});return <><PageHeader title="Weekly Study Planner" subtitle="Plan realistic sessions around your availability"/><div className="planner-layout"><div className="card"><h3>Add study session</h3><form className="planner-form" onSubmit={submit}><label>Date<input type="date" required value={form.date} onChange={e=>setForm({...form,date:e.target.value})}/></label><label>Topic<input required placeholder="e.g. SQL joins" value={form.topic} onChange={e=>setForm({...form,topic:e.target.value})}/></label><div className="form-grid"><label>Planned minutes<input type="number" min="15" value={form.planned_minutes} onChange={e=>setForm({...form,planned_minutes:Number(e.target.value)})}/></label><label>Actual minutes<input type="number" min="0" value={form.actual_minutes} onChange={e=>setForm({...form,actual_minutes:Number(e.target.value)})}/></label></div><Button>Add session</Button></form></div><div className="card"><h3>Weekly summary</h3><div className="summary-row"><span>Planned</span><b>{summary.planned} min</b></div><div className="summary-row"><span>Actual</span><b>{summary.actual} min</b></div><div className="summary-row"><span>Completed</span><b>{summary.done} sessions</b></div></div></div><div className="card sessions"><h3>Scheduled sessions</h3>{sessions.length?sessions.map(s=><div className="session-row" key={s.id}><button className={s.completed?'topic-check done':'topic-check'} onClick={()=>toggle(s)}><CheckCircle2/></button><div><b>{s.topic}</b><span>{s.date}</span></div><span>{s.actual_minutes||s.planned_minutes} min</span><button className="delete-btn" onClick={()=>remove(s.id)}>Delete</button></div>):<Empty text="No study sessions scheduled"/>}</div></>}

function Milestones(){const [items,setItems]=useState([]);const [title,setTitle]=useState('');const [date,setDate]=useState('');useEffect(()=>{void load()},[]);const load=()=>api.get('/milestones').then(r=>setItems(r.data)).catch(()=>{});const add=async(e)=>{e.preventDefault();await api.post('/milestones',{title,target_date:date});setTitle('');setDate('');load()};const toggle=async(m)=>{await api.put(`/milestones/${m.id}`,{completed:!m.completed});load()};return <><PageHeader title="Milestones" subtitle="Celebrate the checkpoints on your journey"/><form className="card milestone-form" onSubmit={add}><input required placeholder="Milestone title" value={title} onChange={e=>setTitle(e.target.value)}/><input type="date" value={date} onChange={e=>setDate(e.target.value)}/><Button>Add milestone</Button></form><div className="milestone-grid">{items.length?items.map(m=><div className={`milestone card ${m.completed?'completed':''}`} key={m.id}><Trophy/><div><h3>{m.title}</h3><p>{m.target_date?`Target: ${m.target_date}`:'No target date'}</p></div><button onClick={()=>toggle(m)}>{m.completed?'Completed':'Mark complete'}</button></div>):<Empty text="No milestones yet"/>}</div></>}

function App(){return <BrowserRouter><Routes><Route path="/" element={<Landing/>}/><Route path="/login" element={<AuthPage mode="login"/>}/><Route path="/register" element={<AuthPage mode="register"/>}/><Route path="/dashboard" element={<Protected><Layout><Dashboard/></Layout></Protected>}/><Route path="/profile" element={<Protected><Layout><Profile/></Layout></Protected>}/><Route path="/careers" element={<Protected><Layout><Careers/></Layout></Protected>}/><Route path="/assessment" element={<Protected><Layout><Assessment/></Layout></Protected>}/><Route path="/roadmap" element={<Protected><Layout><Roadmap/></Layout></Protected>}/><Route path="/resources" element={<Protected><Layout><Resources/></Layout></Protected>}/><Route path="/planner" element={<Protected><Layout><Planner/></Layout></Protected>}/><Route path="/milestones" element={<Protected><Layout><Milestones/></Layout></Protected>}/></Routes></BrowserRouter>}
export default App
