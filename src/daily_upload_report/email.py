import boto3

from typing import List


def send_plain_email(
        message: str,
        subject: str,
        receivers: List[str] = ["infodatachampions@gmail.com"]
        ) -> None:
    ses_client = boto3.client("ses")
    CHARSET = "UTF-8"

    ses_client.send_email(
        Destination={
            "BccAddresses": receivers,
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": message,
                },
                "Html": {
                    "Charset": CHARSET,
                    "Data": message,
                },
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": subject,
            },
        },
        Source="o-nexus monitoring <no-reply@o-nexus.com>",
    )
    # send shadow email to double check what is going to the client
    email_went_to_client = [x for x in receivers
                            if not x.endswith('o-nexus.com')]
    if email_went_to_client:
        explain_receivers = '--'.join(receivers)
        print(f'sending shadow emails from new platform {receivers=}')
        ses_client.send_email(
            Destination={
                "BccAddresses": ["david.fortini@o-nexus.com"],
            },
            Message={
                "Body": {
                    "Text": {
                        "Charset": CHARSET,
                        "Data": message,
                    },
                    "Html": {
                        "Charset": CHARSET,
                        "Data": message,
                    },
                },
                "Subject": {
                    "Charset": CHARSET,
                    "Data": f'{subject} shadow: {explain_receivers}',
                },
            },
            Source="Docudeel rapportage <no-reply@docudeel.com>",
        )
