import streamlit as st
import stripe
from google.cloud import firestore
from streamlit.components.v1 import html
import streamlit.components.v1 as components
from datetime import datetime
import json
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time


if 'key1' not in st.session_state:
	st.session_state.key1  = False
	
if "otp1" not in st.session_state:
	st.session_state.otp1 = str(random.randint(100000, 999999))
	
stripe.api_key = st.secrets["strpie_api_key"]
stripe_publishable_key = st.secrets["strpie_publishable_key"]

service_account_info = {"type":st.secrets["type"],
						"project_id":st.secrets["project_id"],
						"private_key_id":st.secrets["private_key_id"],
						 "private_key":st.secrets["private_key"],
						 "client_email":st.secrets["client_email"],
						 "client_id":st.secrets["client_id"],
						 "auth_uri":st.secrets["auth_uri"],
						 "token_uri":st.secrets["token_uri"],
						 "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
						 "client_x509_cert_url":st.secrets["client_x509_cert_url"],
						 "universe_domain":st.secrets["universe_domain"]
						}

db = firestore.Client.from_service_account_info(service_account_info)

try:
	# Query Stripe API for all payments
	all_payments = stripe.PaymentIntent.list(limit = 10)
except stripe.error.InvalidRequestError as e:
	# Handle API request error
	st.error(f"Error retrieving payments: {e}")
	
current_date = datetime.now().strftime('%d-%m-%Y')
count = 0
success = "succeeded"
if all_payments:
	for payment in all_payments.data:
		created_date = datetime.utcfromtimestamp(payment.created).strftime('%d-%m-%Y')
		if(created_date == current_date and success == payment.status):
			count = count + 1

remaining = 5 - count

circle = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');
    	.circle
    	{
    	   background: white;
    	   width: 220px;
    	   height: 220px;
    	   border: 5px solid black;
    	   border-radius: 50%;
    	   position: relative;
    	   left: 30px;
    	   top:-35px;
    	}
        #text{
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            font-size: 3em;
            color: black;
            position:relative;
            left: 6%;
            top:30%;
            font-family: 'Pacifico';
        }
        #connect
        {
        	color: red;
        	position: relative;
        	left: 12%;
        	top: -20px;
        	font-size: 2em;
        	font-family: 'Pacifico';
        }
    </style>
"""

with st.sidebar:
	st.markdown(circle, unsafe_allow_html=True)
	st.markdown(f'<div class="circle">\
			<span id="text">feelings</span>\
		</div><div id="connect">Stay Connected!</div>',unsafe_allow_html=True)
	st.sidebar.header(':red[Navigation]')
	radio_value = st.sidebar.radio('Select an option', ('About', 'Information', 'Take a Session','Feedback','Review'))


def About():
	st.session_state.key1  = False
	st.session_state.otp1 = str(random.randint(100000, 999999))
	st.header("Welcome to :red[Feeling].streamlit.app")
	st.write("It is a :green[platform] for those who are :blue[introvert and want to share feelings]")
	st.write("like some :blue[confessions],:blue[love] someone but afraid to tell or even some people can share :blue[guilty] they did in past.")
	st.write("We are :green[providing] :red[U] a support means having :green[face to face] communication with our staff member.")
	st.write("So, it may :green[help] u to things getting :blue[better] or even :blue[good] to share :blue[feeling] with our member.")
	st.write(":violet[IT IS TOTALLY CONFIDENTIAL] ok")
	
	st.write("")
	st.write("")
	st.write(":red[ U Just need to follow three steps]:")
	
	st.write(" ")
	st.write(" ")
	
	st.header(":blue[Step 1]: Read the Page properly, we mention some :violet[terms and conditions]")
	st.caption("if :red[u] want to :green[communicate] then have to follow this steps")
	st.write(":red[U] have to book one :violet[session] from :red[table] that present in the :red[end of the page].")
	st.write(":violet[session] price is around :green[5$ dollars] and may be more due to taxes.")
	st.write("we don't share :violet[Your secret and everything is confidential].")
	st.write("we :red[Don't give any refund].")
	
	
	st.write(" ")
	st.write(" ")
	
	st.header(":blue[Step 2]: U need to fill the form that are present in :red[Information] section")
	st.write("please provide :violet[accurate information], so we can verify u during session")
	st.write("U need to fill this form only :blue[one time].")
	st.write("If :red[U not fill this form] then :red[U can't allow to make a payment for Session.]")
	st.write("It is your responsibility to :green[provide accurate information] otherwise :green[we are not responsible for anything].")
	
	st.write(" ")
	st.write(" ")
	
	st.header(":blue[Step 3]: The Final Step:")
	st.write("IN this step, :red[U need to enter that email that is used to fill the form]")
	st.write(":violet[Other-wise], U will not be able to pay fees and book a :violet[session].")
	
	st.write(" ")
	st.write(" ")
	st.write(" ")
	st.write(" ")
	
	st.header(f":red[Number] of :violet[Session] Available is :green[{remaining}]")
	
	data = {"Number of Session": ['1','2','3','4','5'],"Timing": ['9 to 10','10:10 to 11:10','11:10 to 12:10','12:20 to 13:20','13:30 to 14:30']}
	st.table(data)
	
	st.write(" ")
	st.write(" ")
	st.write(" ")
	st.write(" ")
	
	st.header("After taking a session, I will send an email within an hour.")


def is_valid_email(email):
	if '@' in email and all(ord(c) < 128 for c in email):
		return True
	return False

def is_valid_mobile(mobile):
	if mobile.isdigit() and len(mobile) == 10:
		return True
	return False

def Information():
	
	st.header("Information: ")
	st.caption(":red[Provide your information. So, it is easy to verify U during Session.]")
	st.caption(":green[ONLY one time Form] and :violet[make sure U provide correct email]")
	
	#user_information
	full_name = st.text_input("Enter :blue[Full Name]: ")
	mobile = st.text_input(":green[Mobile] number: ")
	age =  st.text_input(":violet[Age] : ")
	gender = st.text_input("Enter :green[Gender]:")
	email = st.text_input("Enter :red[Email]: ")
	st.caption("we can :green[communicate] with email")
	
	#detail_verification
	if(st.button("Submit")):
		if(full_name == "" or gender == "" or mobile == "" or  age == "" or email == ""):
			st.error("Please Complete the form:")
		elif not is_valid_email(email):
			st.error("Please enter a valid email address")
		elif not is_valid_mobile(mobile):
			st.error("Please enter a valid 10-digit mobile number")
		else:
			try:
				search = db.collection("users")    #get a collection document			
				search_docs = search.stream()     # in stream form
				
				t = True                         # check variable
				for doc1 in search_docs:                  
					if(doc1.to_dict()['email'] == email):
						t = False
				
				if t:
					st.session_state.key1 = True
					message = "This is your OTP " +  st.session_state.otp1  + "  for registration"
					sender_email = st.secrets["sender_email"]
					password = st.secrets["password"]
					smtp_server = st.secrets["smtp_server"] # Change according to your email provider
					smtp_port = st.secrets["smtp_port"]  # Change according to your email provider

					# Create message
					email1 = MIMEMultipart()
					email1["From"] = sender_email
					email1["To"] = email
					email1["Subject"] = "Subject"  # You can customize the subject here
					email1.attach(MIMEText(message, "plain"))

					# Connect to SMTP server and send email
					try:
						server = smtplib.SMTP(smtp_server, smtp_port)
						server.starttls()
						server.login(sender_email, password)
						text = email1.as_string()
						server.sendmail(sender_email, email, text)
						st.write("Email sent successfully!")
					except Exception as e:
						st.write(f"Error: {e}")
					finally:
						server.quit()
				else:
					st.error("this email is already used!")
					st.error("used different email id!!")
			except:
				st.warning(f"Please Fill the Information form first")
	
	if(st.session_state.key1):
		OTP =  st.text_input(":violet[OTP] Please : ")
		if(st.button("verify")):
			if(OTP == ""):
				st.error("Please Enter the OTP:")
			elif(st.session_state.otp1 == OTP):
				st.success("OK, OTP matched")
				search = db.collection("users") 
				search.document(full_name).set({"gender": gender,"mobile": mobile,"age": age,"email": email})
				st.success("Details submitted")
				st.balloons()
				st.header("OK, now you can pay the fees for Session.")
				time.sleep(4)
				radio_value = "Take a Session"
			else:
				st.error("Entered :violet[OTP] does not match!")


def Take_a_Session():
	st.session_state.key1 = False
	st.session_state.otp1 = str(random.randint(100000, 999999))
	st.header("Take a Session:")
	st.caption(":green[verify your email], :red[we just ensure your submitted details]")
	
	#email verification, we just ensure that player share there details
	email_pay = st.text_input("Enter :red[Email]: ")
	if(st.button("Submit")):
		try:
			#user = auth.get_user_by_email(email_pay)
			user_email = db.collection("users")
			docs = user_email.stream()
			t1 = False
			for doc in docs:
				if(doc.to_dict()['email'] == email_pay):
					t1 = True
			if t1:
				if(count >=5):
					st.write("stop payment please")
					st.write(f"remaining session is : {remaining}")
				else:
					st.header("Proceding to payment gateway")
					stripe_js = """
					<script async	src="https://js.stripe.com/v3/buy-button.js"></script>
					<stripe-buy-button	buy-button-id="buy_btn_1P8MwWSJCEUI0WslyaUN3G5U"
  					publishable-key="{}">
					</stripe-buy-button>""".format(stripe_publishable_key)
					html(stripe_js)
			else:
				st.warning("Please Fill the Information form first")
		except:
			st.warning("Please Fill the Information form first")

def Feedback():
	st.header(":blue[Feedback: ]")
	st.caption(":red[Please submit Your Feedback, so we can improve our website]")
	feedback_name = st.text_input("Enter :orange[Name]: ")
	feedback_email = st.text_input("Enter :violet[Email]: ")
	feedback_write = st.text_area("Enter :green[Feedback]: ",max_chars=250)
	if(st.button("Submit")):
		if(feedback_name == "" or feedback_email == "" or feedback_write == ""):
			st.error("Please Complete the feedback form!")
		else:
			search_for_feed = db.collection("users")   						 #get a collection document			
			search_docs_feed = search_for_feed.stream()     				 #in stream form
			t_feed = False                        							 #check variable
			for doc1_feed in search_docs_feed:                  
				if(doc1_feed.to_dict()['email'] == feedback_email):
					t_feed = True
		
			if(t_feed):
				feed = db.collection("feedback") 
				feed.document(feedback_name).set({"date": datetime.now().strftime('%d-%m-%Y'),"feedbacks": feedback_write})
				st.success("Details submitted")
				st.balloons()
				st.write("u can read your feedback from review")
			else:
				st.error("U can't submit a feedback form")
		

custom_css = """
    <style>
        .custom-container {
            background-color: #f0f0f0;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            color: black;
        }
    </style>
"""

def Review():
	st.header(":green[Review: ]")
	st.markdown(custom_css, unsafe_allow_html=True)
	search_for_review = db.collection("feedback").stream() 
	for doc1_review in search_for_review:
		#with st.container(className="custom-container"): 
			#st.write(doc1_review.id)
			#st.write(doc1_review.to_dict()["date"])
			#st.write(doc1_review.to_dict()["feedbacks"])
		st.markdown(f'<div class="custom-container">\
		<p>Name: <b>{doc1_review.id}</b></p>\
		<p>Date: {doc1_review.to_dict()["date"]}</p>\
		<p>Feedback: {doc1_review.to_dict()["feedbacks"]}</p>\
		</div>',unsafe_allow_html=True)

if(radio_value == "About"):
	About()
elif(radio_value == "Information"):
	Information()
elif(radio_value == "Take a Session"):
	Take_a_Session()
elif(radio_value == "Feedback"):
	Feedback()
elif(radio_value == "Review"):
	Review()

#https://console.firebase.google.com/project/earn-by-game/firestore?hl=en_GB
