

def get_response(response_type: str, lang: str,
                 ) -> dict:
    """
    response_type = debitnummer_notfound, fallback, ok
    """
    # this should be in frontend
    # nofile = dict(en='Your debtor number or your file is incorrect.',
    #                      nl='Uw debiteurennummer is niet gevonden. ',
    #                      es='No se encontró su número de deudor.')
    debitnummer_notfound = dict(en='Your debtor number was not found.',
                                nl='Uw debiteurennummer is niet gevonden.',
                                es='No se encontró su número de deudor.')

    fallback_resp = dict(en="Something went wrong, please try again ❌",
                         nl="Er ging iets fout, aub nog een keer proberen ❌",
                         es="Algo salió mal, intenta de nuevo ❌")
    file_too_large = dict(en="Your file is too large, please upload a file smaller than 5.5MB ❌",
                          nl="Uw bestand is te groot, aub een bestand kleiner dan 5.5MB uploaden ❌",
                          es="Su archivo es demasiado grande, por favor suba un archivo más pequeño que 5.5MB ❌")
    ok_resp = dict(en=f'Your files was successfully uploaded! ✔️',
                   nl=f'Uw bestanden is succesvol geüpload! ✔️',
                   es=f'¡Su archivos se cargó con éxito! ✔️')
    resp = dict(debitnummer_notfound=debitnummer_notfound,
                fallback=fallback_resp,
                ok=ok_resp,
                file_too_large=file_too_large
                # nofile=nofile
                )
    message = resp[response_type][lang]
    return dict(message=message)
