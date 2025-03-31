import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, receiver_email, subject, body, smtp_server, smtp_port, sender_password):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            st.success(f"✅ Email sent successfully to {receiver_email}")
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 AI-Enhanced Cold Mail Automation")

    url_input = st.text_input("Enter a URL:")
    sender_email = st.text_input("Your Email", value="richie2003.anto@gmail.com")
    receiver_email = st.text_input("Receiver's Email", value="josephine.rosy23@gmail.com")
    sender_password = st.text_input("Your Email Password", type="password")
    
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input], headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                })
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)

            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email_body = llm.write_mail(job, links)

                subject = "Expert Solutions for Your Job Requirement"
                send_email(sender_email, receiver_email, subject, email_body, smtp_server, smtp_port, sender_password)

        except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="AI-Enhanced Cold Mail Automation", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)