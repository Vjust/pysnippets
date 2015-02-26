"""
Extract gmail messages and do some analysis on them.
Borrowed from Doug Hellman's IMAP example
"""
import imaplib
import email
import os


def extract_body(payload):
    """
    Extract email body
    """
    if isinstance(payload, str):
        return payload
    else:
        return "\n".join([extract_body(part.get_payload())
                          for part in payload])

MAIL_UID = os.environ.get('mail_uid')
MAIL_PWD = os.environ.get('mail_pwd')
conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
conn.login(MAIL_UID, MAIL_PWD)
conn.select('[Gmail]/Spam')
typ, data = conn.search(None, r'ALL')
try:
    for num in data[0].split()[:100]:
        typ, msg_data = conn.fetch(num, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject = msg['subject']
                print(subject)
                payload = msg.get_payload()
                body = extract_body(payload)
                # print(body[1:100])

finally:
    try:
        conn.close()
    except:
        pass
    conn.logout()
