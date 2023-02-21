from flask import Flask, make_response,render_template,request,redirect,Response,send_file
from flask_sqlalchemy import SQLAlchemy
import pyrebase
from werkzeug.utils import secure_filename
import uuid
from io import BytesIO
from main import bone_fracture,lung_disease,diabetes_predict,insurance_pre,heart_prediction,mental_health
from keys import config
from flask_mail import Mail, Message
import datetime
import pdfkit

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///record.db'
app.config['SQLALCHEMY_BINDS']={'data':'sqlite:///data.db','prediction':'sqlite:///prediction.db'}
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'nihilkd@gmail.com'
app.config['MAIL_PASSWORD'] = 'Shubhee@123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
db=SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = ''

# db.init_app(app)

firebase = pyrebase.initialize_app(config)
auth=firebase.auth()

class Record(db.Model):
    user_name=db.Column(db.String(200),primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    address=db.Column(db.String(200),nullable=False)
    city=db.Column(db.String(50),nullable=False)
    state=db.Column(db.String(50),nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    gender=db.Column(db.String(20),nullable=False)
    date=db.Column(db.String(30),nullable=False)
    blood_group=db.Column(db.String(10),nullable=False)
    aadhar=db.Column(db.String(10),nullable=False)
    job=db.Column(db.String(100),nullable=False)
    
    def __repr__(self) -> str:
        return f"{self.user_name} - {self.name}"

class Data(db.Model):
    __bind_key__ = 'data'
    user_name=db.Column(db.String(100),nullable=False)
    img = db.Column(db.Text, unique=True, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    uid = db.Column(db.Text, unique=True, nullable=False)


class Prediction(db.Model):
    __bind_key__ = 'prediction'
    user_name=db.Column(db.String(100),nullable=False,primary_key=True)
    diabetes=db.Column(db.String(100),nullable=True)
    depression=db.Column(db.String(100),nullable=True)
    bone_fracture=db.Column(db.String(100),nullable=True)
    heart_prediction=db.Column(db.String(100),nullable=True)
    lung_disease=db.Column(db.String(100),nullable=True)


with app.app_context():
    db.create_all()

user="Nikhil"
predictions={}
dates={}

# Home Page
@app.route("/")
def home():
    return render_template('/home/index.html')

@app.route('/insurance_predict',methods=['POST'])
def insurance_predict():
    if request.method == 'POST' :
        age=request.form.get("age"),
        gender=request.form.get("gender"),
        bmi=request.form.get("bmi"),
        child=request.form.get("child"),
        smoke=request.form.get("smoke"),
        region=request.form.get("region"),
        x=insurance_pre(int(age[0]),int(gender[0]),float(bmi[0]),int(child[0]),int(smoke[0]),int(region[0]))
    return x

# Dashbord with records of images
@app.route("/dashboard")
def dashboard():
    global user
    x = Record.query.filter_by(user_name=user).first()
    img=Data.query.filter_by(user_name=user).all()
    return render_template('/dashboard/index.html',user=x,img=img)

@app.route('/download/<string:uid>')
def download(uid):
    x = Data.query.filter_by(uid=uid).first()
    return send_file(BytesIO(x.img), download_name=x.name,as_attachment=True)

# Login Page
@app.route("/signUp",methods =["GET","POST"])
def signUp():
    if request.method == "POST":
        global user
        user=request.form.get("femail")
        auth.create_user_with_email_and_password(
        email=user,
        password=request.form.get("fpassword"),
        )
        return redirect('/register')
    return render_template('/login/index.html')

@app.route("/signIn",methods =["GET","POST"])
def signIn():
    if request.method == "POST":
        global user
        user=request.form.get("femail")
        auth.sign_in_with_email_and_password(
        email=user,
        password=request.form.get("fpassword")
        )
        return redirect('/dashboard')
    return render_template('/login/index.html')


# register page
@app.route("/register",methods =["GET", "POST"])
def register():
    if request.method =='POST':
        global user
        record=Record(
            user_name=user,
            name=request.form.get("fname"),
            address=request.form.get("faddress"),
            city=request.form.get("fcity"),
            state=request.form.get("fstate"),
            pincode=request.form.get("fpincode"),
            gender=request.form.get("fgender"),
            date=request.form.get("fdate"),
            blood_group=request.form.get("fblood"),
            aadhar=request.form.get("faadhar"),
            job=request.form.get("fjob")
        )
        predict=Prediction(
            user_name=user,
            diabetes="null/null",
            depression="null/null",
            bone_fracture="null/null",
            heart_prediction="null/null",
            lung_disease="null/null",
        )
        db.session.add(predict)
        db.session.commit()
        db.session.add(record)
        db.session.commit()
        return redirect('/dashboard')
    return render_template('/register/index.html')


# upload images
@app.route('/upload',methods=['POST'])
def upload():
    global user
    if request.method == 'POST':
        pic=request.files['file']
        if not pic:
            return "<h2> No Pic Uploaded</h2>\n"
        print (uuid.uuid1())
        fileName=secure_filename(pic.filename)
        uid=uuid.uuid1()
        uid=str(uid)
        img=Data(user_name=user,img=pic.read(),name=fileName,uid=uid)
        db.session.add(img)
        db.session.commit()
    return "<h2>Got it!</h2>"

# Prediction
@app.route('/prediction')
def prediction():
    x = Record.query.filter_by(user_name=user).first()
    return render_template('/prediction/index.html',user=x)

@app.route('/bone_fracture',methods=['POST'])
def result1():
    if request.method == 'POST' :
        pic=request.files['file']
        pic.save('image123.jpg')
        if not pic:
            return "<h2> No Pic Uploaded</h2>"
    x=bone_fracture()
    y = Prediction.query.filter_by(user_name=user).first()
    current_date = datetime.date.today()
    y.bone_fracture=x+"/"+str(current_date)
    db.session.add(y)
    db.session.commit()
    return redirect('/summary')

#mental health
@app.route('/mental_health')
def depression():
    x = Record.query.filter_by(user_name=user).first()
    return render_template('/mental/index.html',user=x)

@app.route('/mental_predict',methods=['POST'])
def result5():
    list1=[]
    if request.method == 'POST':
        q1=request.form.get("question1")
        q2=request.form.get("question2")
        q3=request.form.get("question3")
        list1.append([str(q1)])
        list1.append([str(q2)])
        list1.append([str(q3)])
    print(list1)
    x=mental_health(list1)
    y = Prediction.query.filter_by(user_name=user).first()
    current_date = datetime.date.today()
    y.depression=x+"/"+str(current_date)
    db.session.add(y)
    db.session.commit()
    return redirect('/summary')

@app.route('/heart_disease',methods=['POST'])
def result2():
    if request.method == 'POST' :
        age=request.form.get("age"),
        sex=request.form.get("sex"),
        cp=request.form.get("cp"),
        trestbps=request.form.get("trestbps"),
        chol=request.form.get("chol"),
        fbs=request.form.get("fbs"),
        restecg=request.form.get("restecg"),
        thalach=request.form.get("thalach"),
        exang=request.form.get("exang"),
        old=request.form.get("old"),
        slope=request.form.get("slope"),
        ca=request.form.get("ca"),
        thal=request.form.get("thal"),
        print(age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,old,slope,ca,thal)
    x=heart_prediction(int(age[0]),int(sex[0]),int(cp[0]),int(trestbps[0]),int(chol[0]),int(fbs[0]),int(restecg[0]),int(thalach[0]),int(exang[0]),float(old[0]),int(slope[0]),int(ca[0]),int(thal[0]))
    y = Prediction.query.filter_by(user_name=user).first()
    current_date = datetime.date.today()
    y.heart_prediction=x+"/"+str(current_date)
    db.session.add(y)
    db.session.commit()
    return redirect('/summary')

@app.route('/diabetes',methods=['POST'])
def result3():
    if request.method == 'POST' :
        p=request.form.get("p"),
        g=request.form.get("g"),
        bp=request.form.get("bp"),
        st=request.form.get("st"),
        insulin=request.form.get("insulin"),
        bmi=request.form.get("bmi"),
        dpf=request.form.get("dpf"),
        age=request.form.get("age"),
    x=diabetes_predict(int(p[0]),int(g[0]),int(bp[0]),int(st[0]),int(insulin[0]),float(bmi[0]),float(dpf[0]),int(age[0]))
    y = Prediction.query.filter_by(user_name=user).first()
    current_date = datetime.date.today()
    y.diabetes=x+"/"+str(current_date)
    db.session.add(y)
    db.session.commit()
    return redirect('/summary')

@app.route('/lung_disease',methods=['POST'])
def result4():
    if request.method == 'POST' :
        pic=request.files['file']
        pic.save('lung_disease.jpg')
        if not pic:
            return "<h2> No Pic Uploaded</h2>"
    x=lung_disease()
    y = Prediction.query.filter_by(user_name=user).first()
    current_date = datetime.date.today()
    y.lung_disease=x+"/"+str(current_date)
    db.session.add(y)
    db.session.commit()
    return redirect('/summary')

@app.route('/insurance')
def insurance():
    x = Record.query.filter_by(user_name=user).first()
    return render_template('/insurance/index.html',user=x)

@app.route('/summary')
def summary():
    global predictions
    global dates
    x = Record.query.filter_by(user_name=user).first()
    y = Prediction.query.filter_by(user_name=user).first()
    bone_fracture=y.bone_fracture.split('/')
    diabetes=y.diabetes.split('/')
    lung_disease=y.lung_disease.split('/')
    heart_prediction=y.heart_prediction.split('/')
    depression=y.depression.split('/')
    predict={
        'bone_fracture':bone_fracture[0],
        'diabetes':diabetes[0],
        'lung_disease':lung_disease[0],
        'heart_prediction':heart_prediction[0],
        'depression':depression[0],
    }
    date={
        'bone_fracture':bone_fracture[1],
        'diabetes':diabetes[1],
        'lung_disease':lung_disease[1],
        'heart_prediction':heart_prediction[1],
        'depression':depression[1],
    }
    predictions=predict
    dates=date
    return render_template('/summary/index.html',user=x,predict=predict,date=date)

@app.route('/get_pdf')
def get_pdf():
    global predictions
    global dates
    global user
    x = Record.query.filter_by(user_name=user).first()
    res=render_template('/pdf/index.html',predict=predictions,date=dates,profile=x)
    responsestring=pdfkit.from_string(res,False)
    response=make_response(responsestring)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition']='inline; filename=report.pdf'
    message = Message("Your Report", sender='nihilkd@gmail.com', recipients=[user])
    message.attach('file.pdf', 'application/pdf', responsestring)

    mail.send(message)
    return response
    # print(res)
    # return render_template('/pdf/index.html',predict=predictions,date=dates,profile=x)


@app.route('/doctors')
def doctors():
    x = Record.query.filter_by(user_name=user).first()
    return render_template('/doctors/index.html',user=x)

# add report
@app.route('/add_report')
def add_report():
    x = Record.query.filter_by(user_name=user).first()
    return render_template('/upload/index.html',user=x)

#profile page
@app.route('/profile')
def profile():
    x = Record.query.filter_by(user_name=user).first()
    return render_template('/profile/index.html',user=x)

if __name__ == "__main__":
    app.run(host="localhost", port=4000, debug=True)