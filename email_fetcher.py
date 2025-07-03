
import imaplib
import email
import os
import joblib
from attachment_processor import predict_attachment

model = joblib.load('text_model.pkl')
vectorizer = joblib.load('text_vectorizer.pkl')

def fetch_email_attachments():
    mail = imaplib.IMAP4_SSL('imap.example.com')
    mail.login('user@example.com', 'password')
    mail.select('inbox')
    status, messages = mail.search(None, 'ALL')
    email_ids = messages[0].split()

    for e_id in email_ids:
        status, msg_data = mail.fetch(e_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])

        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            file_name = part.get_filename()
            if bool(file_name):
                file_path = os.path.join('/tmp', file_name)
                with open(file_path, 'wb') as f:
                    f.write(part.get_payload(decode=True))
                prediction = predict_attachment(file_path, model, vectorizer)
                print(f'File: {file_name}, Prediction: {prediction}')
