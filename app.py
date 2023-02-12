from flask import Flask,render_template,request,redirect,Response,send_file
from flask_sqlalchemy import SQLAlchemy
import pyrebase
from werkzeug.utils import secure_filename
import uuid
from io import BytesIO
from main import ans

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///record.db'
app.config['SQLALCHEMY_BINDS']={'data':'sqlite:///data.db'}

db=SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = ''

config={
        'apiKey': "AIzaSyA0NrL3k15_rk4hQV2Mj1Ejf49GkECuaoQ",
        'authDomain': "hideout-de60d.firebaseapp.com",
        'databaseURL': "https://hideout-de60d-default-rtdb.firebaseio.com",
        'projectId': "hideout-de60d",
        'storageBucket': "hideout-de60d.appspot.com",
        'messagingSenderId': "822673797712",
        'appId': "1:822673797712:web:16624f9015f991d74e1755",
        'measurementId': "G-NER9QNPQK4"
}
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


with app.app_context():
    db.create_all()

user="Nikhil"


@app.route("/")
def home():
    return render_template('/home/index.html')

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
        db.session.add(record)
        db.session.commit()
        return redirect('/dashboard')
    return render_template('/register/index.html')

@app.route("/dashboard")
def dashboard():
    global user
    x = Record.query.filter_by(user_name=user).first()
    img=Data.query.filter_by(user_name=user).all()
    return render_template('/dashboard/index.html',user=x,img=img)


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
        password=request.form.get("fpassword"),
        )
        return redirect('/dashboard')
    return render_template('/login/index.html')

@app.route('/add_report')
def add_report():
    x = Record.query.filter_by(user_name=user).first()
    return render_template('/upload/index.html',user=x)

@app.route('/result',methods=['POST'])
def result():
    if request.method == 'POST':
        pic=request.files['file']
        pic.save('image123.jpg')
        if not pic:
            return "<h2> No Pic Uploaded</h2>"
    x=ans()
    return x

@app.route('/prediction')
def prediction():
    x = Record.query.filter_by(user_name=user).first()
    return render_template('/prediction/index.html',user=x)

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

@app.route('/download/<string:uid>')
def download(uid):
    x = Data.query.filter_by(uid=uid).first()
    return send_file(BytesIO(x.img), download_name=x.name,as_attachment=True)

@app.route('/profile')
def profile():
    x = Record.query.filter_by(user_name=user).first()
    return render_template('/profile/index.html',user=x)

if __name__ == "__main__":
    app.run(host="localhost", port=4000, debug=True)