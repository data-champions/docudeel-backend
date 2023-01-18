import json
import logging
def send_slack_message(message: str) -> None:
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
    except Exception as e:
        print('slacked failed', e)
        logging.exception('Slack failed')

    return None


if __name__ == '__main__':
    send_slack_message('test')