

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

    ok_resp = dict(en=f'Your files was successfully uploaded! ✔️',
                   nl=f'Uw bestanden is succesvol geüpload! ✔️',
                   es=f'¡Su archivos se cargó con éxito! ✔️')
    resp = dict(debitnummer_notfound=debitnummer_notfound,
                fallback=fallback_resp,
                ok=ok_resp,
                # nofile=nofile
                )
    message = resp[response_type][lang]
    return dict(message=message)
