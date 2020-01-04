from	__future__ import print_function
import	telebot
from	telebot.types import Message

import	datetime
import	pickle
import	os.path
import	json
import	requests

from	googleapiclient.discovery		import build
from	google_auth_oauthlib.flow		import InstalledAppFlow
from	google.auth.transport.requests	import Request

'''
Discription:
google api:
https://developers.google.com/calendar/v3/reference
https://github.com/gsuitedevs/python-samples/tree/master/calendar/quickstart
http://wescpy.blogspot.com/2015/09/creating-events-in-google-calendar.html
https://readthedocs.org/
https://rtportal.ru/index.php/stati/164-calendar-python-bot

bot:
https://core.telegram.org/bots/api
https://github.com/eternnoir/pyTelegramBotAPI

'''
#TODO: get coordinates

TOKEN = '931079067:AAFedzMljRnB8TlMC8MJSSJ_K3JAfXYw2Fg'
chat_id = '931079067'
print(TOKEN)
bot = telebot.TeleBot(TOKEN)
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
	creds = None
	if os.path.exists('token.pickle'):
		print('point_00')
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token) 
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
			with open('token.pickle', 'wb') as token:
				pickle.dump(creds, token)
	
	service = build('calendar', 'v3', credentials=creds)
	print('service', service)
	now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	print('time now', now)
	print('Getting the upcoming 10 events')
	events_result = service.events().list(calendarId='primary', timeMin=now,
					maxResults=10, singleEvents=True,
					orderBy='startTime').execute()
	events = events_result.get('items', [])
	
	with open('report.json', 'w') as w:
		json.dump(events, w)

	if not events:
		print('No upcoming events found.')
	for event in events:
		start = event['start'].get('dateTime', event['start'].get('date'))
		print(start, event['start']['dateTime'])
		for t in event:
			print('t: ', event[t])
	#bot.send_message('849914042', event)
	#bot.polling()

@bot.message_handler(func=lambda message: True)
def upper(message: Message):
	print(message)
	bot.reply_to(message, 'test-test')

if __name__ == "__main__":
	main()