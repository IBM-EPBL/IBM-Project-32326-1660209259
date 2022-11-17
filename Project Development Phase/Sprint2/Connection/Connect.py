import ibm_db


def Connection():
    try:
        conn = ibm_db.connect(
            "DATABASE=bludb;HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32459;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=nwc93718;PWD=TqtAIa6NnzSat4qS", "", "")
        print("Database Connected Successfully !")
        return conn
    except:
        print("Unable to connect: ", ibm_db.conn_errormsg())


def Create(email, name, phone, password, conn):

    columns = '"UNAME","UEMAIL","UPHONE","UPASSWORD"'
    val = "'"+name+"','"+email+"','"+phone+"','"+password+"'"
    sql = 'Insert into NWC93718.USER(' + columns + ') values('+val+')'
    try:
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.execute(stmt)
        print("added :-)")
        return 1
    except:
        print("Error While Adding the User ! ")
        return 0


def Signin(email, password, conn):

    sql = "SELECT * FROM NWC93718.USER"
    try:
        result = ibm_db.exec_immediate(conn, sql)
        tuple = ibm_db.fetch_tuple(result)
        while tuple != False:
            if str(tuple[1]) == email and str(tuple[3]) == password:
                res = [str(tuple[0]), str(tuple[1]), str(tuple[2])]
                return res
            tuple = ibm_db.fetch_tuple(result)
        print("Fetch Success :-)")
        return 0
    except:
        print("fetch not found !")
        return 0
