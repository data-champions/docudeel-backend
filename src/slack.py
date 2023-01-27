"""  
For config check this:
https://data-championsgroup.slack.com/apps/A0F7XDUAZ-incoming-webhooks?tab=settings&next_id=0
"""
import json
import logging


def send_slack_message(message: str) -> bool:
    from urllib import request
    url = "https://hooks.slack.com/services/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"
    req = request.Request(url, method="POST")
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
    send_slack_message('test-docudeel')