from flask import Flask, render_template, request,session,flash,abort
import sqlite3 as sql
import os


app = Flask(__name__)
#app.config['SECRET_KEY'] = 'oh_so_secret'



@app.route('/')
def home():
    check=False
    try:
        check=session['logged_in']
    except:
        check=False
    finally:
        if check:
            return render_template('computer1.html',massage="Please Log in again")
        else:
            return render_template('database.html',msg="Please Log in again")


@app.route('/forget')
def new_student():
    return render_template('student.html')

@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    check=False
    if request.method == 'POST' :
        try:
            nm = request.form['username']
            ps = request.form['password']
            ps1 = request.form['rpassword']
            add = request.form['address']
            city = request.form['city']
            pin = request.form['pin']
            job = request.form['cem']
            msg = 'Sorry both passwords are not same'
            if ps != ps1:
                check=True
                return 0

            with sql.connect("storemanagement.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO register (emailId,password,addr,city,pin,job) VALUES(?, ?, ?, ?, ?, ?)",(nm,ps,add,city,pin,job) )
                con.commit()
                msg = "Record successfully added"
        except:
            #msg = "error in insert operation"
            con.rollback()
            msg = "error in insert operation"

        finally:
            if check:
                return render_template("database.html", msg=msg)
            else:
                return render_template("result.html", msg=msg)
            con.close()


emailid=''

@app.route('/login', methods=['POST'])
def login():
    check=False
    if request.method == 'POST':
        con=sql.connect("storemanagement.db")
        cur=con.cursor()
        cur.execute('select emailId ,password,job from register')
        data=cur.fetchall()

        for usr in data:
            if request.form['username'] == usr[0] and request.form['password'] == usr[1] and request.form['cem'] == usr[2]:
                session['user'] = usr[0]
                session['job'] = usr[2]
                session['logged_in']=True
                check=True
                msg = 'Logged in successfully'

        if not session.get('logged_in'):
            flash('wrong username or password')
            check=False
            msg='Sorry try again Fill correct details'
        if not check:
            return render_template("database.html", msg=msg)
        elif session['job'] == "Employee":
            return render_template("Information.html")
        elif session['job'] == "Manager":
            return refreshEmp("manageEmp.html")
        elif session['job'] == "Customer":
            return refreshObject("computer1.html","Your welcome you are "+msg)
        else:
            return render_template("result.html", msg=msg)

    #return home()
@app.route('/manageEmp')
def manage():
    return refreshEmp("manageEmp.html")

@app.route('/computer1')
def computer1():
    return refreshObject("computer1.html")


@app.route('/info')
def info():
    con = sql.connect('storemanagement.db')
    con.row_factory = sql.Row
    job = 'Customer'
    cur = con.cursor()
    conect=cur.execute("SELECT * FROM cart inner join register on register.emailId=cart.eid where register.job=?",(job,))
    rows = conect.fetchall();
    return render_template("information2.html", rows=rows)


@app.route('/computer11',methods=['POST'])
def computer11():
    if request.method == 'POST':
        objid = request.form['objid']
        con=sql.connect("storemanagement.db")
        con.row_factory = sql.Row
        cur=con.cursor()
        cur.execute("SELECT obid,objname,image,prevPrice,curPrice FROM object where obid=?",(objid,))
        rows = cur.fetchall()
        return render_template("computer11.html",rows=rows)


@app.route('/pass',methods=['post','get'])
def passw():
    return render_template('password.html')


@app.route('/addEmployee', methods=['POST'])
def addEmployee():
    if request.method == 'POST' :
        try:
            eid = request.form['eid']
            add = request.form['add']
            citty = request.form['citty']
            pincode = request.form['pincode']
            job = request.form['job']
            msg = "error in insert operation1"
            with sql.connect("storemanagement.db") as con:
                cur = con.cursor()
                msg = "change object id to insert new value"
                cur.execute("INSERT INTO register (emailId,addr,city,pin,job) VALUES(?, ?, ?, ?, ?)",(eid,add,citty,pincode,job) )
                con.commit()
                msg = "Record successfully added "
        except:
            #msg = "error in insert operation"
            con.rollback()
            msg = "error in insertion of employee "

        finally:
            file="manageEmp.html"
            return refreshEmp(file,msg)
            con.close()


@app.route('/deleteEmployee',methods=['POST'])
def deleteEmployee():
    if request.method == 'POST' :
        try:
            eid = request.form['eid']
            jobb = request.form['job']
            msg = "error in deletion operation1"
            with sql.connect("storemanagement.db") as con:
                cur = con.cursor()
                msg = "error in deletion operation"
                cur.execute("DELETE FROM register WHERE emailId=? and job=?", (eid,jobb))
                con.commit()
                msg = "Record successfully deleted "
        except:
            #msg = "error in i operation"
            con.rollback()
            msg = "error in deleteion of employee"

        finally:
            file="manageEmp.html"
            return refreshEmp(file,msg)
            con.close()


@app.route('/cart', methods=['POST'])
def cart():
    if request.method == 'POST':
        try:
            emailid = session['user']
            objid = request.form['objid']
            objname = request.form['objname']
            objval = request.form['value']
            price = request.form['price']
            totalval=(int(price))*(int(objval))
            msg = "error in insert operation1"
            with sql.connect("storemanagement.db") as con:
                cur = con.cursor()
                msg = "change object id to insert new value"
                cur.execute("INSERT INTO cart (objId,eid,objName,objVal,price,val) VALUES(?, ?, ?, ?, ?, ?)",
                            (objid, emailid, objname, objval,price,totalval))
                con.commit()
                msg = "Record successfully added into cart"
        except:
            # msg = "error in insert operation"
            con.rollback()
            msg = "error in insertion of object in cart operation"

        finally:
            file = "cart.html"
            return refreshCart(file, msg)
            con.close()


@app.route('/password',methods=['post','get'])
def password():
    msg = 'Passord not changed'
    if request.method == 'POST':
        con=sql.connect("storemanagement.db")
        cur=con.cursor()
        cur.execute('update register set password=? where emailId=?', (request.form['npassword'], request.form['email']))
        con.commit()
        msg='Passord chaged successfully'
    return render_template('database.html',msg=msg)


@app.route('/addObject', methods=['POST'])
def addObject():
    if request.method == 'POST' :
        try:
            objid = request.form['objid']
            objname = request.form['objname']
            imageUrl = request.form['image']
            pprice = request.form['prevprice']
            cprice = request.form['curprice']
            msg = "error in insert operation1"
            with sql.connect("storemanagement.db") as con:
                cur = con.cursor()
                msg = "change object id to insert new value"
                cur.execute("INSERT INTO object (obid,objname,image,prevPrice,curPrice) VALUES(?, ?, ?, ?, ?)",(objid,objname,imageUrl,pprice,cprice) )
                con.commit()
                msg = "Record successfully added "
        except:
            #msg = "error in insert operation"
            con.rollback()
            msg = "error in insertion of object "

        finally:
            file="manageobj.html"
            return refreshObject(file,msg)
            con.close()


@app.route('/deleteObject',methods=['POST'])
def deleteObject():
    if request.method == 'POST' :
        try:
            objid = request.form['objid']
            msg = "error in deletion operation1"
            with sql.connect("storemanagement.db") as con:
                cur = con.cursor()
                msg = "error in deletion operation"
                cur.execute("DELETE FROM object WHERE obid=?", (objid,))
                con.commit()
                msg = "Record successfully deleted "
        except:
            #msg = "error in i operation"
            con.rollback()
            msg = "error in deleteion of object"

        finally:
            file="manageobj.html"
            return refreshObject(file,msg)
            con.close()


def refreshEmp(file="manageEmp.html",massage="Updated"):
    con = sql.connect('storemanagement.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM register where job='Employee'")
    rows = cur.fetchall()
    return render_template(file, rows=rows,massage=massage)


@app.route('/object')
def refreshObject(file="manageobj.html",massage="Updated"):
    con = sql.connect('storemanagement.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM object")
    rows = cur.fetchall()
    return render_template(file, rows=rows,massage=massage)



def refreshCart(fname,massage="updated"):
    con = sql.connect('storemanagement.db')
    con.row_factory = sql.Row
    emailid = session['user']
    cur = con.cursor()
    conect=cur.execute("SELECT count (cart.objId) FROM cart inner join register on register.emailId=cart.eid where register.emailId=?",(emailid,))
    row = conect.fetchone();
    session['cart']=row[0]
    return render_template(fname, value=row[0],massage=massage)

@app.route('/cartlist')
def cartlist():
    con = sql.connect('storemanagement.db')
    emailid = session['user']
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM cart where eid=?",(emailid,))
    rows = cur.fetchall();
    return render_template("cartlist.html", rows=rows)


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return home()


@app.route('/list')
def list():
    con = sql.connect('storemanagement.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM register")
    rows = cur.fetchall();
    return render_template("list.html", rows=rows)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=4000)