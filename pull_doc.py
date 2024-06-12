from __future__ import print_function
import pickle
import os.path, io, sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_creds():
    creds = None
    pik_path = os.path.join("credentials", 'token.pickle')
    if os.path.exists(pik_path):
        with open(pik_path, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join("credentials",'cred.json'), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(pik_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def main():
    # Usage: python pull_doc.py [name] [doc_id]
    # name is the name of the project (i.e., the name of the pdf)
    # doc_id is visible in the google docs link
    name = sys.argv[1]
    doc_id = sys.argv[2]
    # Get credentials
    creds = get_creds()
    # Build a service object and request the file
    service = build('drive', 'v3', credentials=creds)
    fh = io.FileIO('{}.mdt'.format(name),'wb')
    x = service.files().export(fileId = doc_id, mimeType="text/plain")
    downloader = MediaIoBaseDownload(fh, x)
    done = False
    while not done:
        status, done = downloader.next_chunk()

if __name__ == '__main__':
    main()
