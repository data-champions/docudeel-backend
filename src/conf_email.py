import re
import requests


def _send_email(text: str, recipient: str, subject: str) -> None:
    URL_EMAIL_UPLOAD_CONFIRM = 'https://hook.eu1.make.com/cac1pr1r1cfu819f8jragt9i8t5uvl98'
    data = {'text': text, 'recipient': recipient, 'subject': subject}
    print(f'{data=}')
    r = requests.post(URL_EMAIL_UPLOAD_CONFIRM,
                      data=data)
    print(r.json())


def create_html(receiver: str, description: str, lang: str) -> str:
    en_description = f"""Dear customer {receiver},
            <p> Hereby the confirmation that you have correctly uploaded the document with the following description: "{description}" </p>
            <p> Regards from the Docudeel team. <p>
            """ 
    nl_description = f"""Geachte klant {receiver},
<p> Hierbij de bevestiging dat u het document correct heeft geüpload met de volgende omschrijving: "{description}" </p>
<p> Groeten van het Docudeel team. <p>
"""
    es_description = f"""Estimado/a cliente {receiver},

    <p> Por la presente la confirmación de que ha subido correctamente el documento con la siguiente descripción: "{description}" </p>
    <p> Saludos desde el equipo de Docudeel. </p>
"""
    lang_to_template = dict(en=en_description,
                            nl=nl_description,
                            es=es_description)
    email_html = lang_to_template.get(lang, "en")
    return email_html


def _get_subject_from_lang(lang: str) -> str:
    en_description = "Docudeel: Upload confirmation"
    nl_description = "Docudeel: Upload bevestiging"
    es_description = "Docudeel: Confirmación de carga"
    lang_to_template = dict(en=en_description,
                            nl=nl_description,
                            es=es_description)
    email_html = lang_to_template.get(lang, "en")
    return email_html

def _is_bad_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return not bool(re.match(pattern, email))


def send_confirmation_email(receiver: str, description: str, lang: str) -> None:
    """ main method to send email"""
    email_html = create_html(receiver=receiver, description=description, lang=lang)
    email_subject = _get_subject_from_lang(lang=lang)
    if _is_bad_email(email=receiver):
        print(f'invalid email: {receiver}..not sending confirmation email')
        return None
    try:
        _send_email(text=email_html, recipient=receiver, subject=email_subject)
    except Exception as e:
        print(e)
    return None


if __name__ == "__main__":

    for lang in ['en', 'es', 'nl']:
        send_confirmation_email(receiver='infodatachampions@gmail.com',
                                description='factuur q1 data champions',
                                lang=lang)