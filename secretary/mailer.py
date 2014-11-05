#!/usr/bin/env python3

import smtplib
from email.mime.text import MIMEText

class Mailer:
	def __init__(self, username, password, host='smtp.gmail.com:587'):
		self.username = username
		self.password = password
		self.host = host
		self.sender = ''
		self.recipients = []
		self.cc = []
		self.bcc = []
		self.subject = ''
		self.content = ''

	def From(self, sender):
		if type(sender)==str: self.sender = sender
	def To(self, recipients, clear=False):
		if(clear): self.recipients = []
		self.recipients += parse_recipients(recipients)
	def Cc(self, recipients, clear=False):
		if(clear): self.cc = []
		self.cc += parse_recipients(recipients)
	def Bcc(self, recipients, clear=False):
		if(clear): self.bcc = []
		self.bcc += parse_recipients(recipients)
	def Subject(self, subject):
		self.subject = subject
	def Content(self, content):
		self.content = content

	def send(self):
		mail = MIMEText(self.content, 'html');
		mail['From'] = self.sender;
		set_csv(mail, 'To', self.recipients)
		set_csv(mail, 'Cc', self.cc)
		mail['Subject'] = self.subject

		recipients = self.recipients + self.cc + self.bcc

		smtp = smtplib.SMTP(self.host)
		smtp.starttls()
		smtp.login(self.username, self.password)
		smtp.sendmail(self.sender, recipients, mail.as_string())
		smtp.quit()

def set_csv(mail, title, values):
	if type(values) == str:
		mail[title] = values
	elif type(values) == list:
		mail[title] = ", ".join(values)

def parse_recipients(recipients):
	if type(recipients)==list:
		return recipients
	if type(recipients)==str:
		return [s.strip() for s in recipients.split(',')]

