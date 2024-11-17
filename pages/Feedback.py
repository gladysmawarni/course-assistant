import streamlit as st  # Import Streamlit library and alias as 'st'
import smtplib  # Import smtplib to send emails
from email.mime.text import MIMEText  # Import MIMEText to format the email content

# Set up the Streamlit page with a title and an icon
st.set_page_config(page_title="Feedback", page_icon="💭")

## Email credentials
email = st.secrets['EMAIL']
password = st.secrets['APP_PASSWORD']

# Create a form for user feedback
with st.form("feedback_form"):
    st.write("Write feedback about the Q&A bot")

    # Add a dropdown menu to select the feedback subject
    option = st.selectbox(
        "Select a subject",
        (
            "Bot Did Not Understand My Question", 
            "Bot Provided an Incorrect or Irrelevant Answer", 
            "Bot Response Was Too Slow or Unhelpful", 
            "Bot Response Was Confusing or Incomplete",
            "Bot Answered My Question Accurately and Clearly",
            "Bot Was Helpful and Responsive",
            "Bot Helped Me Learn Something New",
        ),
    )

    # Text area for detailed feedback
    feedb = st.text_area("Tell us what you think!")

    # Add a submit button for the form
    submitted = st.form_submit_button("Submit")
    
    # Send email if form is submitted
    if submitted:
        try:
            # Create an email message with the feedback content
            msg = MIMEText(feedb)  # The body of the email
            msg['From'] = email  # Set sender's email
            msg['To'] = email  # Set receiver's email (in this case, sending feedback to the sender)
            msg['Subject'] = f"Feedback: {option}"  # Subject line includes the selected feedback option

            # Configure and connect to the SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)  # Gmail's SMTP server and port
            server.starttls()  # Secure the connection with TLS
            server.login(email, password)  # Login with email and password
            server.sendmail(email, email, msg.as_string())  # Send the email with feedback
            server.quit()  # Close the connection to the server

            st.success('Thank you for your feedback!')  # Show success message in the app
        except Exception as e:
            st.error(f"Error sending email: {e}")  # Show error message in the app if email fails to send
            raise Exception


        

