from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import urllib.parse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from cryptography.fernet import Fernet

def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password)
    return decrypted_password.decode()

def count_unread_notifications(username, password):
    
    # Start the WebDriver and open LinkedIn
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/login")
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "username")))

    # Log in to LinkedIn
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    button = driver.find_element(By.XPATH,"//button[contains(text(), 'Sign in')]")
    button.click()
    
    meta_tag = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'meta[name="notifications/config/environment"][content="%7B%22sparkPlaceholders%22%3A%7B%22includeHashes%22%3A%5B%22assets/media-player.amd.js%22%5D%7D%7D"]')))

# Access the content attribute of the meta tag
    content = meta_tag.get_attribute("content")

# Parse the JSON content
    decoded_content = urllib.parse.unquote(content)
    
# Parse the JSON content
    data = json.loads(decoded_content)

# Get the count of unread notifications
    unread_count = data["sparkPlaceholders"].get("unreadCount",0)

# Print the count of unread notifications
    print("Unread Notifications:", unread_count)
    
# Get the unread messages count
    unread_count_element = driver.find_element(By.CLASS_NAME, "msg-overlay-bubble-header")
    unread_msg = unread_count_element.text.strip() if unread_count_element else "0"
    print("Unread Messages:",unread_msg)
    
    # Close the browser
    driver.quit()
    
    return unread_count, unread_msg
    
def send1_email(send_email, send_password, recipient_email, subject, message):
    
    # Create a multipart message
    msg = MIMEMultipart()
    msg["From"] = send_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    # Add the message body
    msg.attach(MIMEText(message, "plain"))

    # Create an SMTP session
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        
        # Start the TLS encryption
        smtp.starttls()

        # Login to the sender's email account
        smtp.login(send_email, send_password)

        # Send the email
        smtp.send_message(msg)
    
# Provide your LinkedIn credentials
username = "<Enter_LinkedIn_Username/Email>"
encryption_key = b'<Enter_the_encryption_key>'
encrypted_password = b'<Enter_the_Encrypted_password>'

password = decrypt_password(encrypted_password, encryption_key)

# Count the unread notifications
unread_count, unread_msg = count_unread_notifications(username, password)

# Provide your email details 
send_email = "<Enter_senders_email_address>"
send_password = "<Enter_app_password/less_secure_password_for_senders_email>"
recipient_email = "<Enter_recipient_mail_id>"
subject = "LinkedIn count"
message =  f"""Number of Unread Notifications: {unread_count}

             Number of Unread Messages: {unread_msg}"""
             
send1_email(send_email, send_password, recipient_email, subject, message)