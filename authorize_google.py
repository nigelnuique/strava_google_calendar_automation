from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import json

SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials/credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    # Save the token
    with open('credentials/token.json', 'w') as token:
        token.write(creds.to_json())
    print("✅ token.json saved!")
    
    # Provide instructions for setting up GitHub secret
    print("\n" + "="*60)
    print("🔑 GITHUB ACTIONS SETUP")
    print("="*60)
    print("To use this with GitHub Actions, add the following secret:")
    print("Secret name: GOOGLE_CREDENTIALS")
    print("Secret value (copy the entire content below):")
    print("-" * 60)
    
    # Read and display the token content for easy copying
    with open('credentials/token.json', 'r') as token:
        token_content = token.read()
        print(token_content)
    
    print("-" * 60)
    print("📝 How to add this secret to GitHub:")
    print("1. Go to your GitHub repository")
    print("2. Click Settings > Secrets and variables > Actions")
    print("3. Click 'New repository secret'")
    print("4. Name: GOOGLE_CREDENTIALS")
    print("5. Value: Copy the entire content above")
    print("6. Click 'Add secret'")
    print("\n⚠️  Keep this token secure and never commit it to version control!")

if __name__ == '__main__':
    main()
