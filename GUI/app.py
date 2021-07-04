from flask import Flask,request, url_for, redirect, render_template
import pickle
import pandas as pd
import numpy as np
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def email(mail,mail_list,z):
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
		<h4 style="text-align:left;padding-left:10%;">Email: {mail}</h4>
                <h4 style="text-align:left;padding-left:10%;">Gender: {mail_list[0]}</h4>
		<h4 style="text-align:left;padding-left:10%;">Age 60 and Above: {mail_list[1]}</h4>
		<h4 style="text-align:left;padding-left:10%;">Cough: {mail_list[2]}</h4>
		<h4 style="text-align:left;padding-left:10%;">Fever: {mail_list[3]}</h4>
		<h4 style="text-align:left;padding-left:10%;">Sore Throat: {mail_list[4]}</h4>
		<h4 style="text-align:left;padding-left:10%;">Shortness of Breath: {mail_list[5]}</h4>
		<h4 style="text-align:left;padding-left:10%;">Headache: {mail_list[6]}</h4>
		<h4 style="text-align:left;padding-left:10%;">Abroad: {mail_list[7]}</h4>
		<h4 style="text-align:left;padding-left:10%;">Contact With Covid Object: {mail_list[8]}</h4>
		<h4 style="text-align:left;padding-left:10%;">Contact with Covid Patient: {mail_list[9]}</h4>
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
    
app = Flask(
  __name__,
  template_folder='templates',
  static_folder='static'
)

model = pickle.load(open('model.pkl','rb'))

@app.route('/')
def hello_world():
    return render_template("index.html")
	
@app.route('/',methods=['POST','GET'])
def predict():
    int_features=[x for x in request.form.values()]
    mail=int_features[0]
    int_features=int_features[1:]
    a = [np.array(int_features)]
    mail_list = list(a[0])
    li = list(a[0])
    print(mail_list)
    
    temp_list=[]
    if(mail_list[0]=='1'):
        mail_list[0]="Male"
    else:
        mail_list[0]="Female"
    for i in mail_list:
        if(i=='1'):
            temp_list.append("Yes")
        elif(i=='0'):
            temp_list.append("No")
        else:
            temp_list.append(i)
    mail_list=temp_list
    print(mail_list)

    #Data Modeling on the dataset data
    a = []
    for i in li[1:]:
        a.append(int(i))
    data = {"cough":[a[1]],"fever":[a[2]],"sore_throat":[a[3]],"shortness_of_breath":[a[4]],"head_ache":[a[5]],"age_60_and_above":[a[0]],"abroad":[a[6]],"contact_with_covid_object":[a[7]],"contact_with_covid_patient":[a[8]]}
    df = pd.DataFrame(data)
    print(df)
    prediction=model.predict(df.values)
    pred_prob = model.predict_proba(df.values)
    z = float(pred_prob[0][1])
    print(prediction)
    
	
    # return render_template("index.html",data=fetchdata)

    if (z >= float(0.50)):
        email(mail,mail_list,int(z*100))
        return render_template('risky.html',pred="You Have {}% Risk".format(int(z*100)))
    else:
        email(mail,mail_list,int(z*100))
        return render_template('free.html',pred="You Have {}% Risk".format(int(z*100)))

		
if __name__ == '__main__':
  # Run the Flask app
  app.run(
	host='0.0.0.0',
	debug=True,
	port=8080
  )