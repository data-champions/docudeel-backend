def send_confirmation_email(receiver: str, description: str, lang: str) -> str:
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
    return lang_to_template.get(lang, "en")


if __name__ == "__main__":
    for lang in ['en', 'es', 'nl']:
        styled_html = send_confirmation_email('test', 'test description', lang=lang)
        with open(f'conf_email_{lang}.html', 'w') as f:
            f.write(styled_html)