# -*- coding: utf-8 -*-

from util.utiltools import get_pluriel
import bienPublicKateParametres as pms


def get_expl_ordres():
    return u"Cette boîte de dialogue permet de changer le paramètre 'Ordre'." \
           u"\nB=baseline, P=prélèvement et D=Désapprobation et " \
           u"DP=désapprobation avec prélèvement.\n " \
           u"Donc B_P_D signifie baseline puis prélèvement puis désapprobation."

def get_txt_treatment():
    if pms.TRAITEMENT == pms.BASELINE:
        return u"Baseline"
    elif pms.TRAITEMENT == pms.DESAPPROBATION:
        return u"désapprobation"
    elif pms.TRAITEMENT == pms.PRELEVEMENT:
        return u"prélèvement"
    else:
        return u"désapprobation avec prélèvement"


def get_histo_headers():
    return [
        u"Période", u"Compte\nindividuel", u"Compte\ncollectif",
        u"Total\ncompte\ncollectif", u"Gain\ncompte\nindividuel",
        u"Gain\ncompte\ncollectif", u"Gain\npériode", u"Gain\ncumulé"
    ]


def get_expl_decision():
    return u"Vous disposez d'une dotation de {} jetons. Vous devez " \
           u"décider combien de jetons vous placez sur le compte " \
           u"collectif.".format(pms.DOTATION)


def get_lab_decision():
    return u"Veuillez saisir le nombre de jetons que vous placez sur le \
compte collectif"


def message_moral():
    return u"Une action est morale si elle maximise les gains de tous les \
membres du groupe. Agir ainsi revient à placer la totalité de vos jetons \
sur le compte collectif."


def get_txt_summary(period_content):
    txt = u"<p>Vous disposiez d'une dotation de {}. Vous avez placé {} sur " \
          u"votre compte individuel et {} sur le compte collectif. Au total \
votre groupe a placé {} sur le compte collectif.". \
        format(pms.DOTATION, get_pluriel(period_content.BPK_individuel, u"jeton"),
               get_pluriel(period_content.BPK_collectif, u"jeton"),
               get_pluriel(period_content.BPK_collectif_groupe, u"jeton"))

    if period_content.BPK_desapprobation_recu is not None:
        txt += u"<br /><b>Vous avez reçu {} de désapprobation.</b>".format(
            get_pluriel(period_content.BPK_desapprobation_recu, u"point"))

    txt += u"<br />Votre gain pour la période est égal à la somme de votre " \
           u"gain issu de votre compte individuel, {}, et de votre gain issu " \
           u"du compte collectif, {}, soit {}.</p>".format(
                get_pluriel(period_content.BPK_gain_individuel, pms.MONNAIE),
                get_pluriel(period_content.BPK_gain_collectif, pms.MONNAIE),
                get_pluriel(period_content.BPK_gain_period))

    return txt


def get_expl_desapprobation(collectif, collectif_groupe):
        individuel = pms.DOTATION - collectif
        txt = u"Vous avez placé {} sur votre compte individuel et {} sur " \
              u"le compte collectif. Au total votre groupe a placé {} sur " \
              u"le compte collectif.\n" \
              u"Vous avez ci-dessous le nombre de jetons placés sur le compte " \
              u"collectif par chacun des autres membres de votre groupe.\n" \
              u"Pour chacun d'eux vous pouvez attribuer entre 0 et {} points " \
              u"de désapprobation".format(
            get_pluriel(individuel, u"jeton"), get_pluriel(collectif, u"jeton"),
            get_pluriel(collectif_groupe, u"jeton"), pms.DESAPPROBATION_MAX)
        return txt


def get_labs_desapprobation():
    return [
        u"Veuillez saisir le nombre de points de désapprobation que vous "
        u"attribuez à chacun des autres membres de votre groupe.",
        u"Compte collectif", u"Points de désapprobation"
    ]


def get_txt_final(in_euros, in_ecus):
    if in_ecus is not None:
        txt = u"Vous avez gagné {}, soit {}.".format(
            get_pluriel(in_ecus, u"ecu"), get_pluriel(in_euros, u"euro"))
    else:
        txt = u"Vous avez gagné {}.".format(get_pluriel(in_euros, u"euro"))
    return txt