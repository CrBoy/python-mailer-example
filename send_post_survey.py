#!/usr/bin/env python3

from secretary.mailer import Mailer
from jinja2 import Environment, FileSystemLoader
from sys import stdin
import urllib.parse
import config

def send_notification(nickname, email):
	sender = 'COSCUP<noreply@coscup.org>'
	subject = '寄信小測試'

	env = Environment(loader=FileSystemLoader('./templates'))
	template = env.get_template('content.html')

	content = template.render(nickname=nickname)

	mailer = Mailer(config.mandrill['username'], config.mandrill['password'], host='smtp.mandrillapp.com:587')
	mailer.From(sender)
	mailer.Subject(subject)
	mailer.Content(content)

	print('Sending `{email}`...'.format(email=email), end='', flush=True)
	mailer.To(email, clear=True)
	mailer.send()
	print('OK!')

if __name__ == '__main__':
	file = open('storage/all-list')

	for line in file:
		cols = [col.strip() for col in line.split('\t')]
		send_notification(cols[0], cols[1])
