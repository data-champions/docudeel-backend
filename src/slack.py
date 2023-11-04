"""  
For config check this:
https://data-championsgroup.slack.com/apps/A0F7XDUAZ-incoming-webhooks?tab=settings&next_id=0
"""
import json
import logging
from config import SLACK_URL

def send_slack_message(message: str) -> bool:
    from urllib import request
    req = request.Request(SLACK_URL, method="POST")
    req.add_header('Content-Type', 'application/json')
    data = {
        "text": message
    }
    data = json.dumps(data)
    data = data.encode()
    try:
        r = request.urlopen(req, data=data)
        content = r.read()
        print(content)
        return True
    except Exception as e:
        print('slacked failed', e)
        logging.exception('Slack failed')
        return False



if __name__ == '__main__':
    send_slack_message('test-docu')