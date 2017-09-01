from flask import Flask, request, render_template
import cx_Oracle
app = Flask(__name__)

conn = 'PRIYA/priya1411@localhost:1521/xe'
db=cx_Oracle.connect(conn)

@app.route("/login")
def start():
    return render_template('index.html')

@app.route("/map")
def map():
    return render_template('index.html',msg='Logged Out Successfully')
    
@app.route('/login',methods=['POST'])
def signup():
    with app.app_context():
        if request.method=='POST':
            name=request.form['name']
            mno=request.form['no']
            email=request.form['email']
            password=request.form['psw']
            teach=request.form['teach']
            learn=request.form['learn']
            cur = db.cursor()

            cur.prepare('select * from users where email = :email')
            cur.execute(None, {'email': email})
            res = 0
            for result in cur:
                res = res + 1
            if res > 0:
                return render_template('index.html',msg='Already Registered')
            cur.close()

            cur = db.cursor()
            query = """Insert into users(name,mno,email,
            password,teach,learn) VALUES ('"""+name+"""',
            """+mno+""",'"""+email+"""'
            ,'"""+password+"""','"""+teach+"""','"""+learn+"""')"""           
            cur.execute(query)
            db.commit()
            cur.close()
            return render_template('index.html',msg='Regestration Success')

@app.route('/user',methods=['POST'])
def login():
    with app.app_context():
        if request.method=='POST':
            email=request.form['email']
            password=request.form['psw']
            cur = db.cursor()
            cur.prepare("""select * from users
            where email = :email and password = :password""")
            cur.execute(None, {'email': email,'password':password})
            res = 0
            for result in cur:
                res = res + 1
            cur.close()
            if res > 0:                
                return render_template('map.html', user=email)            
            else:
                return render_template('index.html',msg='Invalid Credentials')

if __name__=='__main__':
    app.run()
