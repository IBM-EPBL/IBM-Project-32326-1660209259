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
            userType = "".join(tempUserType)
            userID = account['ID']
            if userType == "customer":
                print(account)
                return redirect(url_for('viewcusttickets'))
            elif userType == "agent":
                return redirect(url_for('agenttickets'))
            elif userType == "admin":
                return redirect(url_for('assignticket'))
       # return redirect(url_for('login'))
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
    tickets = []
    ticketQuery = "SELECT * FROM TICKET"
    stmt = prepare(conn, ticketQuery)
    execute(stmt)
    account = fetch_assoc(stmt)
    while account!= False:
            tickets.append(account)
            account = fetch_assoc(stmt)
    if request.method == 'POST':
        print(request.form.items)
        return redirect(url_for('assignagent',id = request.form['id']))
    return render_template("homeScreen.html",tickets = tickets)

@app.route('/assignagent',methods=['GET','POST'])
def assignagent():
    ticketid = request.args.get('id')
    agents = []
    ticketQuery = "SELECT * FROM TICKET where TICKET_ID = ?"
    stmt = prepare(conn, ticketQuery)
    bind_param(stmt, 1, request.args.get('id'))
    execute(stmt)
    account = fetch_assoc(stmt)
    agentQuery = "SELECT * FROM AGENT"
    stmt = prepare(conn, agentQuery)
    execute(stmt)
    agent = fetch_assoc(stmt)
    while agent!= False:
            agents.append(agent)
            agent = fetch_assoc(stmt)
    if request.method == 'POST':
        print(request.form['id'])
        create_ticket_query = "update TICKET set STATUS=?,AGENT_ID=? where TICKET_ID = ?"
        stmt = prepare(conn, create_ticket_query)
        bind_param(stmt, 1, "Assigned")
        bind_param(stmt, 2, request.form['id'])
        bind_param(stmt, 3, ticketid)
        execute(stmt)
        return redirect(url_for('assignticket'))
    return render_template("agentassignpage.html",agents = agents)


#agent

@app.route('/agenttickets',methods=['GET','POST'])
def agenttickets():
    global userID
    if request.method == 'POST':
        tickets = []
        create_ticket_query = "update TICKET set STATUS=? where TICKET_ID = ?"
        stmt = prepare(conn, create_ticket_query)
        bind_param(stmt, 1, "Approved")
        bind_param(stmt, 2, request.form['id'])
        execute(stmt)
        print(request.form.items)
        return render_template("agenttickets.html",tickets = tickets)
    tickets = []
    ticketQuery = "SELECT * FROM TICKET where STATUS = ?and AGENT_ID = ?"
    stmt = prepare(conn, ticketQuery)
    bind_param(stmt, 1, "Assigned")
    bind_param(stmt, 2, userID)
    execute(stmt)
    account = fetch_assoc(stmt)
    while account!= False:
            tickets.append(account)
            account = fetch_assoc(stmt)
    return render_template("agenttickets.html",tickets = tickets)

@app.route('/register',methods=['GET','POST'])
def register():
    if(request.method == 'POST'):
        l =  request.form.to_dict()
        tempUserType = [x for x in l if x in ["customer","agent","admin"]]
        mail_check_query = "insert into "+"".join(tempUserType)+" (EMAIL,NAME,PASSWORD) values (?,?,?)"
        stmt = prepare(conn, mail_check_query)
        bind_param(stmt, 1, request.form['email'])
        bind_param(stmt, 2, request.form['password'])
        bind_param(stmt, 3, request.form['name'])
        execute(stmt)
        return redirect(url_for('login'))
    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)