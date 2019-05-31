from __future__ import print_function

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

page_token = None
folder_id = "xxxxxxxxxxxxxxxxxxxxxxxxx"
while True:
    response = DRIVE.files().list(
        q="fullText contains 'Effort Estimate' and name contains 'estimate' and fullText contains 'Person Days'",
        fields='nextPageToken, files(id, name, parents)',
        pageToken=page_token
        ).execute()
    for f in response.get('files', []):
        # print all the files
        print(f['name'], f['parents'])
        parents = ",".join(f['parents'])
        # copy the files to another folder
        DRIVE.files().update(fileId=f['id'],
                                    addParents=parents + "," + folder_id,
                                    fields='id, parents').execute()
    page_token = response.get('nextPageToken', None)
    if page_token is None:
        break
