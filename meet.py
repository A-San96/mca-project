from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/admin.reports.audit.readonly', 'https://www.googleapis.com/auth/cloud-platform']

def meet_data(id_reunion):
	"""Shows basic usage of the Admin SDK Reports API.
	Prints the time, email, and name of the last 10 login events in the domain.
	"""
	creds = None
	# The file token.json stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists('token.json'):
		creds = Credentials.from_authorized_user_file('token.json', SCOPES)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials_web.json', SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open('token.json', 'w') as token:
			token.write(creds.to_json())

	service = build('admin', 'reports_v1', credentials=creds)

	# Call the Admin SDK Reports API
	print('Appel de l\'API')
	results = service.activities().list(userKey='all', applicationName='meet',
		filters='meeting_code=='+id_reunion).execute()
	activities = results.get('items', [])

	if not activities:
		print('Erreur d\'authentification')
	else:
		print("Connexion avec succès")
		'''
        for activity in activities:
			if activity['events'][0]['name'] == 'call_ended':
				#return activity['events'][0]['parameters'][17]
				return activity

				#break
				#print(activity)
				#break

			 #print(u'{0}: {1} ({2})'.format(activity['id']['time'],
			#activity['events'][0]['name'], activity['events'][0]['parameters']))
        '''
		return activities
