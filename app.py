from flask import Flask,request, url_for, redirect, render_template
from flask_mysqldb import MySQL
import pickle
import pandas as pd
import numpy as np
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

def email(mail,mail_list,date_time,z):
    mail_content = '''
    <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
</head>
<body>
    <div style="background-color:#eee;padding:10px 20px;">
        <h2 style="font-family:Georgia, 'Times New Roman', Times, serif;color:#185ADB;">Test Report By INFY-SOARS</h2>
    </div>
    <div style="padding:20px 0px">
        <div style="height: 1000px;width:400px">
            <img style="height:40%;"src="https://raw.githubusercontent.com/mykeysid10/Sem-6-Risk-Prediction-of-Covid-19-Cases/main/Logo.png" style="height: 300px;">
            <div style="text-align:center;">
		<h4 style="text-align:left;padding-left:10%;">Email: {mail_list[1]}</h4>
		<h4 style="text-align:left;padding-left:10%;">Test Date: {date_time[0]}</h4>
		<h4 style="text-align:left;padding-left:10%;">Time: {date_time[1]}</h4>
                <h4 style="text-align:left;padding-left:10%;">Gender: {mail_list[2]}</h4>
		<h4 style="text-align:left;padding-left:10%;">Age 60 and Above: {mail_list[3]}</h4>
		<h4 style="text-align:left;padding-left:10%;">Cough: {mail_list[4]}</h4>
		<h4 style="text-align:left;padding-left:10%;">Fever: {mail_list[5]}</h4>
		<h4 style="text-align:left;padding-left:10%;">Sore Throat: {mail_list[6]}</h4>
		<h4 style="text-align:left;padding-left:10%;">Shortness of Breath: {mail_list[7]}</h4>
		<h4 style="text-align:left;padding-left:10%;">Headache: {mail_list[8]}</h4>
		<h4 style="text-align:left;padding-left:10%;">Abraod: {mail_list[9]}</h4>
		<h4 style="text-align:left;padding-left:10%;">Contact With Covid Object: {mail_list[10]}</h4>
		<h4 style="text-align:left;padding-left:10%;">Contact with Covid Patient: {mail_list[11]}</h4>
		<br>
		<h4 style="text-align:left;padding-left:10%;">Corona Risk: {z}%</h4>
		<br>
                <p></p>
            </div>
        </div>
    </div>
</body>
</html>'''.format(**locals())
    #The mail addresses and password
    sender_address = 'highriskcovid19@gmail.com'
    sender_pass = 'RiskyCovid@19'
    receiver_address = mail
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'A test mail sent by Infy-SOARS.'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'html'))
    #Create SMTP session for sending the mail
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_address, sender_pass)
        server.sendmail(
        sender_address, receiver_address, message.as_string()
    )
    
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'covid-user-input (1)'

mysql = MySQL(app)

model = pickle.load(open('model.pkl','rb'))

@app.route('/')
def hello_world():
    cur = mysql.connection.cursor()
    cur.execute("SELECT count(distinct mail_id) FROM details")
    id2=cur.fetchone()[0]
    return render_template("index.html",users=id2)
	
@app.route('/predict',methods=['POST','GET'])
def predict():
    int_features=[x for x in request.form.values()]
    mail=int_features[0]
    int_features=int_features[1:]
    a = [np.array(int_features)]
    li = list(a[0])
    print(li)

    #Database Connection with sending values
    cur = mysql.connection.cursor()
    cur.execute("SELECT max(test_id) FROM details")
    id_temp=cur.fetchone()[0]
    if(id_temp==None):
        id1=1
    else:
        id1 = int(id_temp)+1
    #cur.execute("INSERT INTO details VALUES (%s,'2020-05-08','0',%s,%s,%s,%s,%s,%s,%s,%s,%s,null,%s)",(mail,str(a[2]),str(a[3]),str(a[4]),str(a[5]),str(a[6]),str(a[7]),str(a[8]),str(a[9]),str(a[10]),id1))
    cur.execute("INSERT INTO details VALUES (%s,%s,null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,null,null)",(id1,mail,li[0],li[1],li[2],li[3],li[4],li[5],li[6],li[7],li[8],li[9]))
    mysql.connection.commit()
    
    #Retrival of information from dataset:
    cur.execute("SELECT * from details ORDER BY test_id DESC LIMIT 1")
    mail_list=list(cur.fetchone())
    fetchdata = list(mail_list[4:-2])
    mail_list=mail_list[:-2]
    date_time=mail_list[2]
    f = '%Y-%m-%d %H:%M:%S'
    date_time=date_time.strftime(f)
    date_time=list(date_time.split())
    mail_list=mail_list[:2]+mail_list[3:]
    temp_list=[]
    if(mail_list[2]=='1'):
        mail_list[2]="Male"
    else:
        mail_list[2]="Female"
    for i in mail_list:
        if(i=='1'):
            temp_list.append("Yes")
        elif(i=='0'):
            temp_list.append("No")
        else:
            temp_list.append(i)
    mail_list=temp_list

    #Data Modeling on the dataset data
    a = []
    for i in fetchdata:
        a.append(int(i))
    data = {"cough":[a[1]],"fever":[a[2]],"sore_throat":[a[3]],"shortness_of_breath":[a[4]],"head_ache":[a[5]],"age_60_and_above":[a[0]],"abroad":[a[6]],"contact_with_covid_object":[a[7]],"contact_with_covid_patient":[a[8]]}
    df = pd.DataFrame(data)
    print(df)
    prediction=model.predict(df.values)
    pred_prob = model.predict_proba(df.values)
    z = float(pred_prob[0][1])
    print(prediction)
    
    #Updating the Predictions to Database
    cur.execute("UPDATE details SET corona_result=%s,risk_prob=%s where test_id=%s",(prediction[0],z,id1))
    mysql.connection.commit()
    cur.execute("SELECT count(distinct mail_id) FROM details")
    id2=cur.fetchone()[0]
    cur.close()
    print(fetchdata)
	
    # return render_template("index.html",data=fetchdata)

    if (z >= float(0.50)):
        email(mail,mail_list,date_time,int(z*100))
        return render_template('risky.html',pred="You Have {}% Risk".format(int(z*100)),users=id2)
    else:
        email(mail,mail_list,date_time,int(z*100))
        return render_template('free.html',pred="You Have {}% Risk".format(int(z*100)),users=id2)

		
if __name__ == '__main__':
    app.run(debug=True)
