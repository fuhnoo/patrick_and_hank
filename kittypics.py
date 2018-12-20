from cachetools import cached, TTLCache
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

cache = TTLCache(maxsize=1000, ttl=86400) # caches 500 items. updates every 24 hours (86400 seconds)

class KittyPics(object):
    def __init__(self):
        self.pics = get_pics()

@cached(cache)
def get_pics():
    gauth = GoogleAuth()
    
    # Try to load saved client credentials
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")
    
    drive = GoogleDrive(gauth)
    
    kittypic_links = []
    
    # Auto-iterate through all files that matches this query
    file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
    for file_data in file_list:
        if file_data['mimeType'] =='application/vnd.google-apps.folder': # if folder
            if file_data['title'] == 'kittypics':
                folder_id = file_data['id']
    
    kittypics = drive.ListFile({'q': "'%s' in parents and trashed=false" % folder_id}).GetList()
    for kittypic_data in kittypics:
        kittypic_links.append(kittypic_data['webContentLink'])

    return kittypic_links

def main():
    pics = KittyPics().pics
    print pics

if __name__ == '__main__':
    main()

