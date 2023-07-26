from flask import Flask, render_template, request, redirect, session, url_for
from flask import session as login_session
import pyrebase



config= {
  "apiKey": "AIzaSyB_P4lGUZ0VPG9ykrbjBYGt-nMbYIw_Er8",
  "authDomain": "indv-proj.firebaseapp.com",
  "projectId": "indv-proj",
  "storageBucket": "indv-proj.appspot.com",
  "messagingSenderId": "1003233979952",
  "appId": "1:1003233979952:web:39da2ae2a9ab2e7c7407f5",
  "measurementId": "G-0CL8PGYT5S",
  "databaseURL":"https://indv-proj-default-rtdb.firebaseio.com/"
};

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db= firebase.database()

app=Flask(__name__)

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'



@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            print("trying")
            login_session['user'] = {'email': email,"password":password}
            user = auth.sign_in_with_email_and_password(email,password)
            print("logged in")
            return redirect(url_for('index'))
        except:
            print("Error")
            return render_template('signin.html')
    return render_template('signin.html')

@app.route('/home')
def index():
    reviews = db.child("reviews").get().val()
    return render_template('index.html', reviews=reviews)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user']=auth.create_user_with_email_and_password(email,password)
            UID=login_session['user']['localId']
            user = {"email":email,"password":password}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('index'))
        except:
            return render_template('signup.html')
    return render_template('signup.html')


@app.route('/reviews', methods=['GET', 'POST'])
def reviwes():
    if request.method== 'POST':
        name = request.form['name']
        movie = request.form['movie']
        number = request.form['number']
        review = request.form['review']
        review_dict = {"name":name, "movie":movie,"number":number,"review":review}
        db.child("reviews").push(review_dict)
    return render_template("reviwes.html")





@app.route('/signout')
def signout():
    session.pop('user', None)
    return redirect('/')




if __name__ == '__main__':
    app.run(debug=True)





