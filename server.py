from flask import *
from flask_mysqldb import MySQL, MySQLdb


app = Flask(__name__)
app.secret_key = "flask"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'campus-plexus'
mysql = MySQL(app)

#home
@app.route('/')
def home():
    return redirect(url_for('login'))

#login
@app.route('/login/', methods = ['GET','POST'])
def login():
    if request.method == "POST":
        check = request.form
        email1 = check['email']
        passw1 = check['pass']
        con = mysql.connection.cursor()
        a = con.execute('SELECT email,pass FROM register WHERE email = %s AND pass = %s', (email1, passw1))
        if int(a) == 1 :
            session['email'] = email1 
            return redirect(url_for('profile'))
        else:
            flash("Details wrong")
            return redirect(url_for('login'))
        con.close()
    return render_template('main.html')

#signup
@app.route('/signup/', methods = ['GET','POST'])
def signup():
    
    if request.method == "POST":
        try:
            data = request.form
            fname = data['fname']
            lname = data['lname']
            email = data['email']
            passw = data['pass']
            clgname = data['clgname']
            branch = data['branch']
            year = data['year']

            cur = mysql.connection.cursor()
            cur1 = mysql.connection.cursor()
            cur.execute("INSERT INTO register(fname,lname,email,pass,college,branch,clgyear) VALUES (%s,%s,%s,%s,%s,%s,%s)", (fname,lname,email,passw,clgname,branch,year))
            a1 = cur1.execute('SELECT * FROM register WHERE email = %s AND fname = %s AND lname = %s', (email, fname,lname))
            if int(a1) <= 1 :
                mysql.connection.commit()
                flash("Signed in successfully")
                return redirect(url_for('login'))        
            else:
                flash("User already exists ")
                return redirect(url_for('signup'))        
            cur.close()
            cur1.close()
        except:
            print("Exception")
            return redirect(url_for('signup'))
            
    return render_template('acc.html')

#forgot
@app.route('/forgot/', methods = ['GET','POST'])
def forgot():
    if request.method == "POST":
        details = request.form
        email2 = details['email']
        newpass = details['newpass']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE register SET pass = %s where email = %s",(newpass,email2))
        mysql.connection.commit()
        cur.close() 
        return redirect(url_for('login'))
    return render_template('forgot.html')

#feed
@app.route('/feed/')
def feed():
    return render_template('feed.html')

#profile
@app.route('/profile/')
def profile():
    if 'email' in session:  
        return render_template('profile.html')  
    else:  
        return '<p>Please login first</p>'  

#placements
@app.route('/placements/')
def placements():
    return render_template('placements.html')

#help and about
@app.route('/help/')
def help():
    return render_template('help.html')

#logout
@app.route('/logout/')
def logout():
    if 'email' in session:  
        session.pop('email',None)  
        return render_template('logout.html');  
    else:  
        return '<p>user already logged out</p>'  

if __name__ == '__main__':
    app.run(debug = True)

