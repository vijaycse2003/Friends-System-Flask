# from flask_mysqldb import MySQL
import sqlite3
from flask import Flask, \
    render_template as render,\
        redirect,url_for as url,request,flash



app=Flask(__name__)
app.secret_key="123b"

# app.config["MYSQL_HOST"]="localhost"
# app.config["MYSQL_USER"]="root"
# app.config["MYSQL_PASSWORD"]=""
# app.config["MYSQL_DB"]="henry_vijay_db"
# app.config["MYSQL_CURSORCLASS"]="DictCursor"




conn=sqlite3.connect("D://Python//SQLite//flask_student.db",check_same_thread=False)






@app.route('/')
def Home():
    con=conn.cursor()
    con.row_factory=sqlite3.Row
    sql="select * from students order by id"
    con.execute(sql)
    res=con.fetchall()
    for r in res:
        print(r)
    return render("home.html",dataset=res)
    


@app.route('/adduser',methods=['GET','POST'])
def Insert():
    if request.method == 'POST':
        uid=request.form['id']
        name=request.form['name']
        age=request.form['age']
        city=request.form['city']
        con=conn.cursor()
        sql="insert into students(id,name,age,city) values(?,?,?,?)"
        con.execute(sql,[uid,name,age,city])
        conn.commit()
        con.close()
        flash('Student Details Added!','success')
       
        return redirect(url('Home'))

    return render("addstudent.html")


@app.route('/editstudent/<string:id>',methods=['GET','POST'])
def Update(id):
    con=conn.cursor()
    con.row_factory=sqlite3.Row
    if request.method == 'POST':
        uid=request.form['id']
        name=request.form['name']
        age=request.form['age']
        city=request.form['city']
        sql="update students set id=?, name=?,city=?,age=? where id=?"
        con.execute(sql,[uid,name,city,age,id])
        conn.commit()
        con.close()
        flash(f'{name} Details Updated','info')
        return redirect(url("Home"))

    sql="select * from students where id=?"
    con.execute(sql,[id])
    res=con.fetchone()
    return render("editstudent.html", data=res)

@app.route("/deletestudent/<string:id>/<string:sname>",methods=['POST','GET'])
def Delete(id,sname):
    con=conn.cursor()
    sql="delete from students where id=?"
    conn.execute(sql,[id])
    conn.commit()
    con.close()
    flash(f'{sname} student Details Deleted!','danger')
    return redirect(url("Home"))

if __name__ == "__main__":
    app.run(debug=True)