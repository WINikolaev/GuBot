from	__future__ import print_function
import	telebot
import	datetime
import	pickle
import	os.path
import	json

from	googleapiclient.discovery		import build
from	google_auth_oauthlib.flow		import InstalledAppFlow
from	google.auth.transport.requests	import Request

'''
Discription:
google api:
https://developers.google.com/calendar/v3/reference
'''
#TODO: get coordinates


'''
TOKEN = '931079067:AAFedzMljRnB8TlMC8MJSSJ_K3JAfXYw2Fg'
print(TOKEN)
bot = telebot.TeleBot(TOKEN)
'''

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
			print('flow: {0}'.format(flow))
			creds = flow.run_local_server(port=0)
			print('creds: {0}'.format(creds))
			with open('token.pickle', 'wb') as token:
				pickle.dump(creds, token)
	
	service = build('calendar', 'v3', credentials=creds)
	now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
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
		print(start, event['summary'])

if __name__ == "__main__":
	main()