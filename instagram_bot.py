import json
import os
import requests

class GetRecentPics(object):
    def __init__(self):
        self.pics = self.get_recent()

    def get_recent(self):
        if 'INSTAGRAM_ACCESS_TOKEN' not in os.environ.keys():
            raise AccessTokenError('INSTAGRAM_ACCESS_TOKEN environment variable must be set!')

        access_token = os.environ['INSTAGRAM_ACCESS_TOKEN']
        
        response = requests.get("https://api.instagram.com/v1/users/self/media/recent/?access_token=%s" % access_token)
        posts = json.loads(response.text)['data']
        recent_pics = []
        
        for post in posts:
            recent_pics.append(post['images']['standard_resolution']['url'])

        return recent_pics

def main():
    pics = GetRecentPics().pics
    return pics

if __name__ == '__main__':
    main()
