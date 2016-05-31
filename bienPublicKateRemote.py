# -*- coding: utf-8 -*-

from twisted.internet import defer
from twisted.spread import pb
from PyQt4 import QtGui
import logging
import random

from le2mClient.le2mClientGui.le2mClientGuiDialogs import GuiRecapitulatif
from le2mClient.le2mClientGui.le2mClientGuiDialogs import GuiHistorique


import bienPublicKateParametres as parametres
from bienPublicKateGui import GuiDecision, GuiDesapprobation

logger = logging.getLogger("le2m.{}".format(__name__))


class Remote(pb.Referenceable):
    def __init__(self, main_client):
        self._main_client = main_client
        self._nom = 'bienPublicKate'
        self._main_client.ajouter_remote(self._nom, self)
        self._historique = []

    def remote_set_traitement(self, traitement):
        """
        :param traitement:
        :return:
        """
        parametres.TRAITEMENT = traitement
        logger.info(u"Traitement: {}".format(parametres.TRAITEMENT))

    def remote_afficher_ecran_contribution(self, periode):
        """
        Affichage de l'ecran de décision.
        """
        logger.info(u"Affichage de l'écran de décision")
        if periode == 1:
            del self._historique[:]
        if self._main_client.simulation:
            renvoi = random.randint(parametres.MIN, parametres.MAX)
            logger.info(u"Renvoi {}".format(renvoi))
            return renvoi
        else:
            defered = defer.Deferred()
            ecran_decision = GuiDecision(
                defered, self._main_client.automatique,
                self._main_client.gestionnaire_graphique.ecran_attente,
                self._historique, periode)
            ecran_decision.show()
            return defered

    def remote_afficher_ecran_desapprobation(self, periode, explication,
                                             decisions_membres):
        """
        Affiche l'écran de désapprobations
        :param decisions_membres:
        :return:
        """
        logger.info("Ecran désapprobation")
        logger.debug("decisions_membres: {}".format(decisions_membres))
        if self._main_client.is_simulation():
            renvoi = dict()
            for k in decisions_membres.iterkeys():
                renvoi[k] = random.randint(
                    0, parametres.DESAPPROBATION_MAX
                )
            logger.info(u"Renvoi: {}".format(renvoi))
            return renvoi
        else:
            defered = defer.Deferred()
            ecran_desapprobation = GuiDesapprobation(
                defered, self._main_client.automatique,
                self._main_client.gestionnaire_graphique.ecran_attente,
                self._historique, periode, explication, decisions_membres
            )
            ecran_desapprobation.show()
            return defered

    def remote_afficher_ecran_recapitulatif(self, texte_recap, historique,
                                            periode):
        """

        :param texte_recap:
        :param historique:
        :param periode:
        :return:
        """
        logger.info(u'Récapitulatif')
        self._historique = historique
        if self._main_client.simulation:
            return 1
        else:
            defered = defer.Deferred()
            ecran_recap = GuiRecapitulatif(
                defered,
                self._main_client.automatique,
                self._main_client.gestionnaire_graphique.ecran_attente,
                periode, historique, texte_recap)
            ecran_recap.show()
            return defered

    def remote_afficher_historique(self, historique):
        """
        Fait afficher l'historique
        :param historique:
        :return:1
        """
        assert isinstance(historique, list)
        logger.debug(u"Appel de remote_afficher_historique")
        if self._main_client.simulation or \
                self._main_client.automatique:
            return 1
        ecran_historique = GuiHistorique(
            self._main_client.gestionnaire_graphique.ecran_attente,
            historique)
        ecran_historique.show()
        return 1