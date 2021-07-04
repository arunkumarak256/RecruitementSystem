from flask import Flask, render_template, url_for , request, redirect , session, g
from flask_sqlalchemy import SQLAlchemy
# from flask.ext.session import Session
from datetime import datetime
from sqlalchemy.orm import backref
from sqlalchemy import update
from sqlalchemy.orm import relationship
import sqlite3
from flask_mail import Mail,Message
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recruitment.db'
app.static_folder = 'static'
app.secret_key = 'aravind'
db = SQLAlchemy(app)
mail= Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'aravind18021@cse.ssn.edu.in'
app.config['MAIL_PASSWORD'] = 'Aravind@2814'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

class Resume(db.Model):
    __tablename__='resume'
    id = db.Column(db.Integer,primary_key=True)
    filename = db.Column(db.String(30))
    data = db.Column(db.LargeBinary)
    user = db.relationship("Applicant", backref=backref("user", uselist=False))

class Applicant(db.Model):
    __tablename__ = 'applicant'
    id = db.Column(db.Integer,primary_key=True)
    Name = db.Column(db.String(50),nullable=False)
    Password = db.Column(db.String(50),nullable=False)
    Email_id = db.Column(db.String(200),nullable=False)
    Contact = db.Column(db.String(15))
    Address = db.Column(db.String(30))
    Education = db.Column(db.String(30))
    Specialization = db.Column(db.String(30))
    College = db.Column(db.String(200))
    CGPA = db.Column(db.Float)
    skill_1=db.Column(db.String(50))
    
    skill_2=db.Column(db.String(50))
    
    skill_3=db.Column(db.String(50))
    
    skill_4=db.Column(db.String(50))
    
    skill_5=db.Column(db.String(50))
    resume_id = db.Column(db.Integer,db.ForeignKey( 'resume.id'))

class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer,primary_key=True)
    Name = db.Column(db.String(50),nullable=False)
    Password = db.Column(db.String(50),nullable=False)
    Email_id = db.Column(db.String(200),nullable=False)
    Contact = db.Column(db.String(15))
    Address = db.Column(db.String(30))
    Domain = db.Column(db.String(30))
    Jobs = db.relationship('Job', backref='company', lazy=True)
class MyDateTime(db.TypeDecorator):
    impl = db.DateTime
    
    def process_bind_param(self, value, dialect):
        if type(value) is str:
            return datetime.strptime(value, '%Y-%m-%d')
        return value
class Job(db.Model):
    __tablename__ = 'job'
    id = db.Column(db.Integer,primary_key=True)
    job_domain=db.Column(db.String(100),nullable=False)
    job_name = db.Column(db.String(100),nullable=False)
    date_created = db.Column(MyDateTime, default=datetime.utcnow)
    last_date =  db.Column(MyDateTime, default=datetime.utcnow)
    job_role = db.Column(db.String(200),nullable=False)
    skill_1=db.Column(db.String(30))
    
    skill_2=db.Column(db.String(30))
    
    skill_3=db.Column(db.String(30))
    
    skill_4=db.Column(db.String(30))
    
    skill_5=db.Column(db.String(30))
    location=db.Column(db.String(50))

    experience = db.Column(db.Integer)
    salary = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'),nullable=False)
    
    company_name = db.Column(db.String(30),nullable=False)

    
    

class Applied(db.Model):
    __tablename__ = 'applied'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer,primary_key=True)
    job_id=db.Column(db.Integer, db.ForeignKey('job.id'), primary_key=True)
    app_id=db.Column(db.Integer, db.ForeignKey('applicant.id'), primary_key=True)
    hire_reason=db.Column(db.String(200))
    company_id=db.Column(db.Integer, db.ForeignKey('company.id'), primary_key=True)
    
    

@app.before_request
def before_request():
    g.user = None


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    global Logged
    if request.method == 'POST':
        username = request.form['uname']
        passwd = request.form['passwd']
        selectapplicant = Applicant.query.filter_by(Email_id=username).first()
        selectcompany = Company.query.filter_by(Email_id=username).first()
        if selectapplicant and selectapplicant.Password == passwd:
            Logged =selectapplicant
            return redirect('/student')
        elif selectcompany and selectcompany.Password == passwd:
            Logged =selectcompany
            return redirect('/company_index')
        else:
            error = "User with Given Credentials not found"
            return render_template('login.html',error=error)
    else:
        return render_template('login.html',error=None)

@app.route('/student', methods=['POST', 'GET'])
def student():
    return render_template('student_index.html',error=None)
@app.route('/view_profile', methods=['POST', 'GET']) 
def view_profile():
    selectapplicant = Applicant.query.filter_by(Email_id=Logged.Email_id).first()
    return render_template('view_profile.html',items=selectapplicant)

@app.route('/update_profile', methods=['POST', 'GET']) 
def update_profile():
    name = request.form['uname']
    selectapplicant = Applicant.query.filter_by(Email_id=Logged.Email_id).first()
    setattr(selectapplicant, 'Name',name)
    try:
        db.session.commit()
    except:
        return "error adding values to database"
    error = "Updated Successfully"
    return render_template('view_profile.html',items=selectapplicant,error=error) 

@app.route('/company_index', methods=['POST', 'GET'])
def company_index():
    return render_template('company_index.html',error=None)


@app.route('/add_jobs', methods=['POST', 'GET'])
def add_jobs():
        if request.method == 'POST':
            company_id=Logged.id
            company_name=Logged.Name
            print(company_name)
            job_name = request.form['job_name']
            #print(job_name)
            job_domain = request.form['job_domain']
            print(job_domain)
            #print(job_name)
            date_created = request.form['date_created']
            #print(date_created)
            last_date = request.form['last_date']
            #print(last_date)
            experience = request.form['Experience']
            #print(experience)
            job_role=request.form['job_role']
            #print(job_role)
            salary = request.form['Salary']
            #print(salary)
            skill_1=request.form['skill_1']
            #print(skill_1)
            skill_2=request.form['skill_2']
            #print(skill_2)
            skill_3=request.form['skill_3']
            #print(skill_3)
            skill_4=request.form['skill_4']
            #print(skill_4)
            skill_5=request.form['skill_5']
            #print(skill_5)
            
            location=request.form['location']
            job = Job(company_id=company_id,location=location,company_name=company_name,job_domain=job_domain,skill_1=skill_1,skill_2=skill_2,skill_3=skill_3,skill_4=skill_4,skill_5=skill_5,job_name=job_name,date_created=date_created,last_date=last_date,experience=experience,salary=salary,job_role=job_role)
            db.session.add(job)
            db.session.commit()
            error = "Job added succesfully"
            return render_template('company_index.html',error=error)

        else:
            return render_template('add_jobs.html')



@app.route('/apply_jobs', methods=['POST', 'GET'])
def apply_jobs():
    items=Job.query.all()
    print(items)
    return render_template("apply_jobs.html",items=items)
    
@app.route('/apply_selected_job', methods=['POST', 'GET'])
def apply_selected_job():
    
    hire_reason=request.form['text']
    job_id=request.form['job_id']
    company_id=request.form['company_id']
    print(job_id)
    applied = Applied(job_id=job_id,app_id=Logged.id,hire_reason=hire_reason,company_id=company_id)
    db.session.add(applied)
    db.session.commit()
    error = "Job applied succesfully"
    items=Job.query.all()
    return render_template('apply_jobs.html',error=error,items=items)
class CursorByName():
    def __init__(self, cursor):
        self._cursor = cursor
    
    def __iter__(self):
        return self

    def __next__(self):
        row = self._cursor.__next__()

        return { description[0]: row[col] for col, description in enumerate(self._cursor.description) }
@app.route('/view_applicants', methods=['POST', 'GET'])
def view_applicants():
    temp=Job.query.filter_by(company_id=Logged.id)
    return render_template('view_applicants.html',items=temp)
@app.route('/view_applied_jobs', methods=['POST', 'GET'])
def view_applied_jobs():
    conn = sqlite3.connect('recruitment.db')
    items=conn.execute('select company_name,job_name,salary,experience,location from job j inner join applied a on a.job_id=j.id where a.app_id="'+str(Logged.id)+'"')
    data=items.fetchall()
    return render_template('view_applied_jobs.html',items=data)
    conn.close()
@app.route('/filter_jobs', methods=['POST', 'GET'])
def filter_jobs():
    if request.method == 'POST':
        print("hi")
        menu_value=request.form['menu']
        text_value=request.form['text']
        print(menu_value)
        print(text_value)
        if(menu_value=="company"):
            items=Job.query.filter_by(company_name=text_value).all()
            print("Hi",items)
            return render_template('filtered_jobs.html',items=items)
        if(menu_value=="domain"):
            items=Job.query.filter_by(job_domain=text_value).all()
            print("Hi",items)
            return render_template('filtered_jobs.html',items=items)
        if(menu_value=="role"):
            items=Job.query.filter_by(job_name=text_value).all()
            print("Hi",items)
            return render_template('filtered_jobs.html',items=items)
        if(menu_value=="experience"):
            items=Job.query.filter_by(experience=text_value).all()
            print("Hi",items)
            return render_template('filtered_jobs.html',items=items)
        if(menu_value=="salary"):
            items=Job.query.filter(Job.salary>=int(text_value)).all()
            print("Hi",items)
            return render_template('filtered_jobs.html',items=items)
    
    else:
        print("bye")
        return render_template('apply_jobs.html')  

@app.route('/view_job_applicants', methods=['POST', 'GET'])
def view_job_applicants():
    if request.method=='POST':
        conn = sqlite3.connect('recruitment.db')
        ip_jobid=request.form['job_id']
        items=conn.execute('select applicant.Name,applicant.Email_id,applicant.College,applicant.Education,applicant.Specialization,applicant.CGPA,applicant.skill_1,applicant.skill_2,applicant.skill_3,applicant.skill_4,applicant.skill_5,ap.hire_reason from applicant  inner join applied ap on applicant.id=ap.app_id where ap.job_id="'+str(ip_jobid)+'"')
        data=items.fetchall()
        return render_template('view_job_applicants.html',items=data)
        conn.close()
    else:
        return render_template('view_applicants.html')

@app.route('/send_mail', methods=['POST', 'GET'])
def send_mail():
    mail_id=request.form['email_id']
    msg = Message('Job application regd', sender = 'aravind18021@cse.ssn.edu.in', recipients = [mail_id])
    msg.body = "Greetings from Google.Thank for applying to us.We appreciate your time and effort and we found your profile interesting.So,please find the  interview link https://meet.google.com/uac-mfzr-bpg .Your inteview is scheduled tomorrow.We wil let you know about your selection after the interview."
    mail.send(msg)
    return render_template('company_index.html')

    

    






@app.route('/studentsignup', methods=['POST', 'GET'])
def studentsignup():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        name = fname + lname
        passwd = request.form['password']
        email = request.form['email']
        contact = request.form['contact']
        address = request.form['address']
        clg = request.form['clg']
        spec = request.form['spec']
        degree = request.form['degree']
        cgpa = request.form['cgpa']
        skill_1=request.form['skill_1']
        skill_2=request.form['skill_2']
        skill_3=request.form['skill_3']
        skill_4=request.form['skill_4']
        skill_5=request.form['skill_5']
            
        file = request.files['myfile']
        resume = Resume(filename=file.filename,data=file.read())
        aspirant = Applicant(Name=name,Password=passwd,Email_id=email,Contact=contact,Address=address,Education=degree,Specialization=spec,College=clg,CGPA=cgpa,user=resume,skill_1=skill_1,skill_2=skill_2,skill_3=skill_3,skill_4=skill_4,skill_5=skill_5)
        db.session.add(resume)
        db.session.add(aspirant)
        db.session.commit()
        error = "Signed Up Successfully"
        return render_template('login.html',error=error)

    else:
        return render_template('studentsignup.html')

@app.route('/companysignup', methods=['POST', 'GET'])
def companysignup():
    if request.method == 'POST':
        name = request.form['name']
        passwd = request.form['password']
        email = request.form['email']
        contact = request.form['contact']
        address = request.form['address']
        domain = request.form['domain']
        company = Company(Name=name,Password=passwd,Email_id=email,Contact=contact,Address=address,Domain = domain)
        try:
            db.session.add(company)
            db.session.commit()
        except:
            return "error adding values to database"
        error = "Signed Up Successfully"
        return render_template('login.html',error=error)

    else:
        return render_template('companysignup.html')
@app.route('/delete_vacancy', methods=['POST', 'GET'])
def delete_vacancy():
    if request.method == 'POST':
        jobid = request.form['jobid']
        del_vac = Job.query.filter_by(job_id=jobid,company_id=Logged.id).first()
        try:
            db.session.delete(del_vac)
            db.session.commit()
        except:
            return "error deleting values from database"
        error = "Vacancy Deleted Successfully"
        return render_template('delete_vacancy.html',error=error)

@app.route('/update_vacancy', methods=['POST', 'GET'])
def update_vacancy():
    if request.method == 'POST':
        jobid = request.form['jobid']
        lastdate = request.form['lastdate']
        exp = request.form['exp']
        sal = request.form['sal']
        del_vac = Job.query.filter_by(job_id=jobid,company_id=Logged.id).first()
        if(lastdate != ""):
            setattr(del_vac, 'last_date',lastdate)
        if(exp != ""):
            setattr(del_vac, 'experience',exp)
        if(sal != ""):
            setattr(del_vac, 'salary',sal)
    try:
        db.session.commit()
    except:
        return "error adding values to database"
    error = "Updated Successfully"
    return render_template('update_vacancy.html',items=del_vac,error=error)


if __name__ == "__main__":
    app.run(debug=True)

# def index():
    # if request.method == 'POST':
    #     task_content = request.form['content']
    #     new_task = Todo(content=task_content)

    #     try:
    #         db.session.add(new_task)
    #         db.session.commit()
    #         return redirect('/')
    #     except:
    #         return 'There was an issue adding your task'

    # else:
    #     tasks = Todo.query.order_by(Todo.date_created).all()


# @app.route('/delete/<int:id>')
# def delete(id):
#     task_to_delete = Todo.query.get_or_404(id)

#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return 'There was a problem deleting that task'

# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     task = Todo.query.get_or_404(id)

#     if request.method == 'POST':
#         task.content = request.form['content']

#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue updating your task'

#     else:
#         return render_template('update.html', task=task)