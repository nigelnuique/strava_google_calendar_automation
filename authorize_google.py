from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials/credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    # Save the token
    with open('credentials/token.json', 'w') as token:
        token.write(creds.to_json())
    print("✅ token.json saved!")

if __name__ == '__main__':
    main()
