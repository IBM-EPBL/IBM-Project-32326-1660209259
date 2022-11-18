from flask import Flask,render_template,request,url_for,redirect
from dao import conn
from ibm_db import prepare,execute,bind_param,fetch_assoc

app =Flask(__name__)
userType = None
userID = None

print(conn)

@app.route('/login' ,methods=['POST','GET'])
def login():
    global userID
    global userType
    if request.method=='POST':
        l =  request.form.to_dict()
        tempUserType = [x for x in l if x in ["customer","agent","admin"]]
        mail_check_query = "SELECT * FROM "+"".join(tempUserType)+" WHERE EMAIL = ? and PASSWORD=?"
        stmt = prepare(conn, mail_check_query)
        bind_param(stmt, 1, request.form['email'])
        bind_param(stmt, 2, request.form['password'])
        execute(stmt)
        account = fetch_assoc(stmt)
        if account != False:
            userType = tempUserType
            userID = account['ID']
            return redirect(url_for('viewcusttickets'))
        return redirect(url_for('login'))
    return render_template("login.html")

@app.route("/createticket",methods=['POST','GET'])
def createTicket():
    global userID
    if request.method == 'POST':
        create_ticket_query = "insert into TICKET (ISSUE,STATUS,CUSTOMER_ID) values(?,?,?)"
        stmt = prepare(conn, create_ticket_query)
        bind_param(stmt, 1, request.form['issue'])
        bind_param(stmt, 2, "UnAssigned")
        bind_param(stmt, 3, userID)
        execute(stmt)
        return redirect(url_for('viewcusttickets'))
    return render_template("ticketForm.html")

@app.route("/viewcusttickets")
def viewcusttickets():
    global userID
    print(userID)
    tickets = []
    ticketQuery = "SELECT * FROM TICKET WHERE CUSTOMER_ID = ?"
    stmt = prepare(conn, ticketQuery)
    bind_param(stmt, 1, userID)
    execute(stmt)
    account = fetch_assoc(stmt)
    while account!= False:
            tickets.append(account)
            account = fetch_assoc(stmt)
    return render_template("customerPage.html",tickets = tickets)

@app.route('/assignticket',methods=['GET','POST'])
def assignticket():
    return 


if __name__ == "__main__":
    app.run(debug=True)