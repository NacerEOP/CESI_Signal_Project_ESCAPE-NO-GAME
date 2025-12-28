def ajouter_trame(suite_binaire):
    """Ajoute une trame (délimiteur de début et de fin) à une suite binaire."""
    trame_debut_fin = [0, 1, 1, 1, 1, 1, 1, 0]  # Exemple de délimiteur HDLC
    return trame_debut_fin + suite_binaire + trame_debut_fin

def retirer_trame(suite_tramee):
    """Retire la trame d'une suite binaire tramée."""
    trame_debut_fin = [0, 1, 1, 1, 1, 1, 1, 0]
    taille_trame = len(trame_debut_fin)

    # Vérification que la trame est bien présente
    if suite_tramee[:taille_trame] == trame_debut_fin and suite_tramee[-taille_trame:] == trame_debut_fin:
        return suite_tramee[taille_trame:-taille_trame]  # Enlever la trame
    else:
        raise ValueError("La trame est absente ou incorrecte.")

