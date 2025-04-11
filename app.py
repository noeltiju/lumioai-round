import streamlit as st
import requests
import json
import smtplib
from email.message import EmailMessage
import os
import re

# Set page config - MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="SmartReach AI Email Generator", layout="centered")

@st.cache_data(show_spinner=False)
def get_openrouter_api_key():
    return st.secrets["OPENROUTER_API_KEY"]

# Function to generate email content using OpenRouter API
def generate_email_with_openrouter(prompt):
    api_key = get_openrouter_api_key()
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    # Improved prompt with more explicit formatting instructions
    body = {
        "model": "google/gemma-3-27b-it:free",
        "messages": [
            {
                "role": "user",
                "content": f"""Write a professional email based on the following prompt: {prompt}. 
                Format your response EXACTLY as follows:
                
                SUBJECT: Your subject line here
                
                Your email body starts here and continues with the rest of the content.
                
                Do not include any additional text, explanations, or notes."""
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(body), timeout=30)
        response.raise_for_status()
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # Improved parsing logic for subject and body
        # Use regex to find the subject line
        subject_match = re.search(r"SUBJECT:\s*(.*?)(?:\n\s*\n|\n$)", content, re.IGNORECASE | re.DOTALL)
        
        if subject_match:
            subject = subject_match.group(1).strip()
            
            # Find where the body starts (after subject and blank line)
            subject_end_pos = subject_match.end()
            # Skip any blank lines after the subject
            body_start = re.search(r"\n\s*\n", content[subject_end_pos:])
            
            if body_start:
                body = content[subject_end_pos + body_start.end():].strip()
            else:
                # If no clear body separator is found, take everything after the subject line
                body = re.sub(r"^SUBJECT:.*?\n", "", content, flags=re.IGNORECASE).strip()
                
            return subject, body
        else:
            # If no subject is found, use the first line as subject and the rest as body
            lines = content.strip().split('\n', 1)
            if len(lines) > 1:
                return lines[0].strip(), lines[1].strip()
            else:
                return "Email Regarding Your Request", content.strip()
            
    except Exception as e:
        st.error(f"❌ Error generating email: {str(e)}")
        return "Follow-up Email", f"Hi [recipient_name],\n\nThis is a fallback email as the AI generation failed.\n\nBest regards,\n[Your Name]"

# Title and description
st.title("📧 SmartReach AI Email Generator")

# Initialize state variables as empty strings if they don't exist
if 'email_subject' not in st.session_state:
    st.session_state['email_subject'] = ""
if 'email_body' not in st.session_state:
    st.session_state['email_body'] = ""

# Step 1: Input Details
st.subheader("Step 1: Email Details")

# Email configuration 
with st.expander("Email Configuration (Optional)"):
    sender_email = st.text_input("Sender Email", 
                              value=os.getenv("SENDER_EMAIL", ""),
                              placeholder="your.email@gmail.com")
    sender_password = st.text_input("Email Password", 
                                 type="password",
                                 placeholder="App Password or Email Password")
    st.caption("Note: For Gmail, use an App Password. Keep your credentials secure.")

recipients = st.text_input("Recipient Email(s)", placeholder="e.g. person1@example.com, person2@example.com")
prompt = st.text_area("Prompt for Email", placeholder="e.g. Follow up on a sales pitch to ABC Corp regarding our marketing services...", height=150)

# Step 2: Generate Email
if st.button("Generate Email ✨"):
    if not prompt:
        st.warning("Please provide a prompt for email generation.")
    else:
        with st.spinner("Generating email... This may take a moment..."):
            subject, email_body = generate_email_with_openrouter(prompt)
            st.session_state['email_subject'] = subject
            st.session_state['email_body'] = email_body
            st.success("Email generated! Review and edit below.")

# Show the generated email
if st.session_state['email_subject'] or st.session_state['email_body']:
    st.subheader("Step 2: Edit & Send")
    subject = st.text_input("Email Subject", value=st.session_state['email_subject'])
    body = st.text_area("Email Body", value=st.session_state['email_body'], height=250)

    # Step 3: Send Email
    if st.button("Send Email 🚀"):
        if not recipients:
            st.warning("Please enter at least one recipient email address.")
        elif not subject or not body:
            st.warning("Subject and body cannot be empty.")
        else:
            try:
                # Use either environment variables or inputs from user
                email_sender = sender_email or os.getenv("SENDER_EMAIL")
                email_password = sender_password or os.getenv("SENDER_PASSWORD")
                
                if not email_sender or not email_password:
                    st.error("Missing sender credentials. Please provide them in the Email Configuration section.")
                else:
                    msg = EmailMessage()
                    msg['Subject'] = subject
                    msg['From'] = email_sender
                    msg['To'] = [r.strip() for r in recipients.split(',')]
                    msg.set_content(body)

                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(email_sender, email_password)
                        smtp.send_message(msg)

                    st.success("✅ Email sent successfully!")

            except Exception as e:
                st.error(f"❌ Failed to send email: {str(e)}")
                st.info("If using Gmail, make sure to use an App Password. Go to your Google Account > Security > App Passwords.")