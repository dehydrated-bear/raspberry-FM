from flask import Flask,render_template,request,session,redirect



local_server=True 
app=Flask(__name__)

@app.route("/dashboard")
def dashhboard():
    return render_template("home.html")





