import telegram, threading
from facebook_scraper import get_posts
from datetime import datetime
import csv
from tempfile import NamedTemporaryFile
import shutil

# insert your bot token here
TOKEN = ''
bot = telegram.Bot(TOKEN)

# insert the tag of the channel where you want to send posts after the @
chat_id = '@'


date_format = '%Y-%m-%d %H:%M:%S'

fields = ['page_name', 'page_tag', 'last_post_used']


WAIT_SECONDS = 120

def check():
    with NamedTemporaryFile(mode='w', delete=False) as tempfile:
        with open('pages.csv', mode='r+') as csv_file, tempfile:
            csv_reader = csv.DictReader(csv_file)
            csv_writer = csv.DictWriter(tempfile, fields)
            line_count = 0
            csv_writer.writeheader()
            for page in csv_reader:
                temp = None
                for post in get_posts(page['page_tag'], pages=1):
                    if post['time'] <= datetime.strptime(page['last_post_used'], date_format): # post already sent to channel
                        break
                    if post['image'] is not None:
                        bot.send_photo(chat_id, post['image'], (post['text'] if post['text'] else '')+ '\n[' + page['page_name'] + ']')
                        if (post['time'] > datetime.strptime(page['last_post_used'], date_format) and temp is None):
                            temp = post['time']
                        temp = post['time']
                            temp = post['time']
                        temp = post['time']
                            temp = post['time']
                    elif post['text'] is not None:
                        bot.send_message(chat_id, (post['text'] if post['text'] else '')+ '\n[' + page['page_name'] + ']')
                        if (post['time'] > datetime.strptime(page['last_post_used'], date_format) and temp is None):
                            temp = post['time']
                if temp is not None:
                    page['last_post_used'] = temp
                row = {'page_name': page['page_name'], 'page_tag': page['page_tag'], 'last_post_used': page['last_post_used']}
                csv_writer.writerow(row)
        shutil.move(tempfile.name, 'pages.csv')
        threading.Timer(WAIT_SECONDS, check).start()

check()
