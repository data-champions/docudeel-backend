def clean_debiteur_nummer(user_id: str) -> str:
    """ 
    Clean debiteur_nummer. Should be AAAABB where A = capital letter and B = number.
    """
    debiteur_nummer = user_id.replace('-', '').replace(' ', '').upper().strip()
    return debiteur_nummer