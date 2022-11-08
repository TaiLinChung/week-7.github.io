from flask import Flask #載入Flask
from flask import request  #載入request物件
from flask import render_template #載入render_template
from flask import redirect
from flask import session
from flask import url_for

app=Flask(
    __name__,
    static_folder="static",
    static_url_path="/"
)
app.secret_key="any string but secret"



##前置作業與資料庫連線創建資料庫跟表

import mysql.connector
mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Bb0970662139"
)
mycursor=mydb.cursor()
sql="CREATE DATABASE IF NOT EXISTS signin"
mycursor.execute(sql)
sql="USE signin"
mycursor.execute(sql)
sql="CREATE TABLE IF NOT EXISTS accounts(id_people INT PRIMARY KEY AUTO_INCREMENT,name VARCHAR(20),account VARCHAR(20),password VARCHAR(20))"
mycursor.execute(sql)
sql="CREATE TABLE IF NOT EXISTS messageTable(id_message INT PRIMARY KEY AUTO_INCREMENT,id_people INT,message VARCHAR(200))"
mycursor.execute(sql)



#1.導引至前端主頁面
#使用GET方法，處理路徑/的對應函式
@app.route("/")
def index():
    return render_template("indexW06.html")



#2.接收前端回傳的註冊資訊
#使用POST方法，處理路徑/signup 的對應函式
@app.route("/signup", methods=["POST"])
def signup():
    #接收 POST 方法的 Query String
    account=request.form["account"]
    password=request.form["password"]
    name=request.form["name"]
    print("註冊姓名",name)
    print("註冊帳號",account)
    print("註冊密碼",password)

    #3.連線資料庫判定是否註冊過
    mycursor=mydb.cursor()
    sql_all="SELECT *FROM accounts WHERE (account=%s and password=%s) or name=%s"
    adr_all=(account,password,name)
    mycursor.execute(sql_all,adr_all)
    myresult_all=mycursor.fetchone()

    sql_name="SELECT *FROM accounts WHERE name=%s"
    adr_name=(name,)
    mycursor.execute(sql_name,adr_name)
    myresult_name=mycursor.fetchone()

    #3.1帳號密碼在資料庫中找不到，註冊成功，導向登入頁面member
    if myresult_all == None and (name!="" and account!="" and password!=""):
        sql="INSERT INTO accounts(name,account,password) VALUES(%s,%s,%s)"
        val=(name,account,password)
        mycursor.execute(sql,val)
        mydb.commit()
        return redirect("http://127.0.0.1:3000/")

    elif myresult_all == None and (name=="" or account=="" or password==""):
        return redirect("http://127.0.0.1:3000/error?message=資料不全請重新填寫")
    
    elif myresult_all == None and myresult_name != None:
        print("註冊姓名重複，導向錯誤頁面")
        return redirect("http://127.0.0.1:3000/error?message=暱稱重複已經被註冊過")

    else:
        print("已註冊過，導向錯誤頁面")
        return redirect("http://127.0.0.1:3000/error?message=同組帳號"+'、'+"密碼已經被註冊")
        


#利用要求字串(Query String)提供彈性:/error?message=自訂文字  
@app.route("/error", methods=["GET"])
def error():
    customize=request.args.get("message","帳號、或密碼錯誤")
    # print(str(customize))
    # return "error"
    return render_template("errorW06.html",content=str(customize))



#4.接收前端回傳的註冊資訊處理登入功能
#使用POST方法，處理路徑/signin 的對應函式
@app.route("/signin", methods=["POST"])
def signin():
    #接收 POST 方法的 Query String
    account=request.form["account"]
    password=request.form["password"]

    #5.連線資料庫判定能否登入
    #傳統搜尋法--------------------
    mycursor=mydb.cursor()
    sql="SELECT *FROM accounts WHERE account='"+account+"' and password='"+password+"'"
    mycursor.execute(sql)
    # #佔位符號填入搜尋
    # mycursor=mydb.cursor()
    # sql="SELECT *FROM accounts WHERE account=%s and password=%s"
    # adr=(account,password)
    # mycursor.execute(sql,adr)
    myresult=mycursor.fetchone()

    if myresult == None or (account=="" and password==""):
        print("帳號密碼錯誤，導入錯誤頁面")
        return redirect("http://127.0.0.1:3000/error")

    else:
        print("帳號密碼正確")
        session["keyFlag"]="open"
        session["id_people"]=myresult[0] #記錄使用者id 供後面改名字時如果有姓名相同時用
        session["name"]=myresult[1]
        print("當前登入者是: ",session["name"])
        return redirect("/member")



###登入頁面後端
@app.route("/member")
def member():
    if session["keyFlag"]=="open":
        nameNow=session["name"]
        ##連結資料庫把歷史資料抓出來
        mycursor=mydb.cursor()
        sql_new="SELECT accounts.name,messagetable.message FROM messagetable INNER JOIN accounts ON messagetable.id_people = accounts.id_people"
        mycursor.execute(sql_new)
        myresult_new=mycursor.fetchall()
        # print("myresult_new: ",myresult_new)
        print(myresult_new[0][0])
        return render_template("memberw06.html",record_name=nameNow,record_message=myresult_new)
    
    #沒登錄過就回首頁
    else:
        return redirect("/")



@app.route("/signout")
def signout():
    session["keyFlag"]=""
    session["name"]=""
    return redirect("/")



from flask import jsonify
@app.route("/api/member/",methods=["GET","PATCH"])
def apimember():
    if request.method=="GET":
        account=request.args.get("username",None)
        mycursor=mydb.cursor()
        sql="SELECT id_people,name,account FROM accounts WHERE account=%s"
        adr=(account,)
        mycursor.execute(sql,adr)
        myresult=mycursor.fetchone()

        # print(myresult)
        if myresult !=None and session["keyFlag"]=="open":
            search={
                "data":{
                    "id":myresult[0],
                    "name":myresult[1],
                    "username":myresult[2]
                }
            }
            # return ({
            #     "data":{
            #         "id":myresult[0],
            #         "name":myresult[1],
            #         "username":myresult[2]
            #     }
            # })
            
            
        else:
            search={
                "data":None
            }
            # return ({
            #     "data":None
            # })

        return jsonify(search)
        # return search
#-------USE PATCH
    else:        
        new_name=request.get_json() #透過JS抓到在HTML輸入的新的名字
        new_name=new_name["name"]
        print("new_name",new_name)
        # print("NULL=",new_name)
        if new_name=="" or session["keyFlag"] != "open":
            print({"error":True})
            return {"error":True}

        #判定有登入
        else:
            print("待改的id_people: ",session["id_people"])

            mycursor=mydb.cursor()
            sql="UPDATE accounts SET name =%s  WHERE id_people=%s"
            adr=(str(new_name),str(session["id_people"]))
            mycursor.execute(sql,adr)
            mydb.commit()
            session["name"]=new_name
            print({"ok":True})
            return {"ok":True}



@app.route("/message", methods=["POST"])
def message():
    name=session["name"]
    messagecontent=request.form["message"]

    # 如果留言不為空才寫入
    mycursor=mydb.cursor()
    if messagecontent !="":
        ##將id_people連同這則留言填入資料庫
        sql2="INSERT INTO messageTable(id_people,message) VALUES(%s,%s)"
        val2=(session["id_people"],messagecontent)
        mycursor.execute(sql2,val2)
        mydb.commit()

    ##連結資料庫把歷史資料抓出來
    mycursor=mydb.cursor()
    sql_new="SELECT accounts.name,messagetable.message FROM messagetable INNER JOIN accounts ON messagetable.id_people = accounts.id_people"
    mycursor.execute(sql_new)
    myresult_new=mycursor.fetchall()
    # print("myresult_new: ",myresult_new)
    print(myresult_new[0][0])

    # return render_template("memberw06.html",record_name=session["record"]["peopleNow"],record_message=session["record"]["history"])
    return render_template("memberw06.html",record_name=session["name"],record_message=myresult_new)



# 啟動網站伺服器，可透過port參數指定埠號
# if __name__=="__main__":
#     app.run(port=3000,debug=True)
app.config["JSON_AS_ASCII"]=False
app.run(port=3000)



