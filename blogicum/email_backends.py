from django.core.mail.backends.filebased import EmailBackend


class SaveEmailsBackend(EmailBackend):
    def send_messages(self, email_messages):
        for message in email_messages:
            with open(f'sent_emails/{message.subject}.eml', 'w') as file:
                file.write(message.message().as_string())

        return len(email_messages)
