# -*- coding: utf-8 -*-
from le2mUtile.le2mUtileTools import get_monnaie

# [VARIABLES] Please do not change the values
# traitements
BASELINE = 0
PRELEVEMENT = 1
DESAPPROBATION = 2
DESAPPROBATION_PRELEVEMENT = 3
# ordres
B_P_DP = 0
B_D_DP = 1
B_DP_D = 2
B_D_D_1 = 3
B_D_D_2 = 3

# [PARAMETERS] Some parameters can be changed
ORDRE = B_P_DP  # possible de le changer dans le menu de l'expérience
TAUX_CONVERSION = 0.067
NOMBRE_PERIODES = 10
TAILLE_GROUPES = 4  # ne pas changer sinon erreur
DOTATION = 20
MIN = 0
MAX = DOTATION
STEP = 1
MPCR = 0.4
MONNAIE = "ecu"
RENDEMENT_COMPTE_INDIVIDUEL_NORMAL = 1
RENDEMENT_COMPTE_INDIVIDUEL_PRELEVEMENT = 0.7
RENDEMENT_COMPTE_INDIVIDUEL = RENDEMENT_COMPTE_INDIVIDUEL_NORMAL  # Changé selon traitement
TRAITEMENT = BASELINE  # NE PAS TOUCHER - changé dans menu de l'expérience
DESAPPROBATION_MAX = 10
DESAPPROBATION_MIN = -1
DESAPPROBATION_STEP = 1

TEXTE_EXPLICATION = u"Vous disposez d'une dotation de {} jetons. Vous devez \
décider combien de jetons vous placez sur le compte collectif.".format(
    DOTATION)

LABEL_DECISION = u"Veuillez saisir le nombre de jetons que vous placez sur le \
compte collectif"

TEXTE_MESSAGE = u"Une action est morale si elle maximise les gains de tous les \
membres du groupe. Agir ainsi revient à placer la totalité de vos jetons \
sur le compte collectif."


def get_texte_recapitulatif(individuel, collectif, collectif_groupe,
                            gain_individuel, gain_collectif, gain_periode,
                            desapprobation_recus=None):
    """
    :param individuel: jetons sur le cpte individuel
    :param collectif: jetons sur le cpte collectif
    :param collectif_groupe: jetons total par le groupe sur cpte collectif
    :param gain_individuel: le gain du compte individuel
    :param gain_collectif: le gain du compte collectif
    :param gain_periode: le gain de la période du joueur
    :return: le texte du récapitulatif
    """
    txt = u"<p>Vous disposiez d'une dotation de {} jetons. Vous avez placé {} {} \
sur votre compte individuel et {} {} sur le compte collectif. Au total \
votre groupe a placé {} {} sur le compte collectif.". \
        format(DOTATION, individuel, get_monnaie(individuel, u"jeton"),
               collectif, get_monnaie(collectif, u"jeton"),
               collectif_groupe, get_monnaie(collectif_groupe, u"jeton"))

    if desapprobation_recus is not None:
        txt += u"<br /><b>Vous avez reçu {} {} de désapprobation.</b>".format(
            desapprobation_recus, get_monnaie(desapprobation_recus, u"point"))

    txt += u"<br />Votre gain pour la période est égal à la somme de votre gain \
issu de votre compte individuel, {} {}, et de votre gain issu du compte \
collectif, {} {}, soit {} {}.</p>".format(
        gain_individuel, get_monnaie(gain_individuel),
        gain_collectif, get_monnaie(gain_collectif),
        gain_periode, get_monnaie(gain_periode))

    return txt


def get_explication_desapprobation(collectif, collectif_groupe):
        individuel = DOTATION - collectif
        txt = u"Vous avez placé {} {} sur votre compte individuel et {} {} sur " \
              u"le compte collectif. Au total votre groupe a placé {} {} sur " \
              u"le compte collectif.\n" \
              u"Vous avez ci-dessous le nombre de jetons placés sur le compte " \
              u"collectif par chacun des autres membres de votre groupe.\n" \
              u"Pour chacun d'eux vous pouvez attribuer entre 0 et {} points " \
              u"de désapprobation".format(
            individuel, get_monnaie(individuel, u"jeton"), collectif,
            get_monnaie(collectif, u"jeton"), collectif_groupe,
            get_monnaie(collectif_groupe, u"jeton"), DESAPPROBATION_MAX)
        return txt

def get_label_desapprobation():
    return u"Veuillez saisir le nombre de points de désapprobation que vous " \
           u"attribuez à chacun des autres membres de votre groupe."
