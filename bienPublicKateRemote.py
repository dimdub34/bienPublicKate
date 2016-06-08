# -*- coding: utf-8 -*-

from client.cltremote import IRemote
from twisted.internet import defer
from client.cltgui.cltguidialogs import GuiRecapitulatif
import logging
import random


import bienPublicKateParametres as pms
import bienPublicKateTexts as txt
from bienPublicKateGui import GuiDecision, GuiDesapprobation

logger = logging.getLogger("le2m.{}".format(__name__))


class RemoteBPK(IRemote):
    def __init__(self, le2mclt):
        IRemote.__init__(self, le2mclt)

    def remote_configure(self, params, currentsequence):
        logger.info(u"{} configure".format(self.le2mclt.uid))
        self._currentsequence = currentsequence
        for k, v in params.viewitems():
            setattr(pms, k, v)

    def remote_newperiod(self, periode):
        logger.info(u"{} Period {}".format(self.le2mclt.uid, periode))
        self.currentperiod = periode
        if self.currentperiod == 1:
            del self.histo[:]
            self.histo.append(txt.get_histo_headers())

    def remote_display_contribution(self):
        """
        Affichage de l'ecran de décision.
        """
        logger.info(u"Affichage de l'écran de décision")
        if self._le2mclt.simulation:
            renvoi = random.randint(pms.MIN, pms.MAX)
            logger.info(u"Renvoi {}".format(renvoi))
            return renvoi
        else:
            defered = defer.Deferred()
            ecran_decision = GuiDecision(
                defered, self.le2mclt.automatique,
                self.le2mclt.gestionnaire_graphique.ecran_attente,
                self.histo, self.currentperiod)
            ecran_decision.show()
            return defered

    def remote_display_desapprobation(self, explication,
                                             decisions_membres):
        """
        Affiche l'écran de désapprobations
        :param decisions_membres:
        :return:
        """
        logger.info("Ecran désapprobation")
        logger.debug("decisions_membres: {}".format(decisions_membres))
        if self.le2mclt.is_simulation():
            renvoi = dict()
            for k in decisions_membres.viewkeys():
                renvoi[k] = random.randint(
                    0, pms.DESAPPROBATION_MAX)
            logger.info(u"Renvoi: {}".format(renvoi))
            return renvoi
        else:
            defered = defer.Deferred()
            ecran_desapprobation = GuiDesapprobation(
                defered, self.le2mclt.automatique,
                self.le2mclt.gestionnaire_graphique.ecran_attente,
                self.histo, self.currentperiod, explication, decisions_membres)
            ecran_desapprobation.show()
            return defered

    def remote_display_summary(self, period_content):
        """

        :param texte_recap:
        :param historique:
        :param periode:
        :return:
        """
        logger.info(u'Récapitulatif')
        self.histo.append([period_content.get(k) for k in self._histo_vars])
        if self.le2mclt.simulation:
            return 1
        else:
            defered = defer.Deferred()
            txt_summary = txt.get_txt_summary(period_content)
            ecran_recap = GuiRecapitulatif(
                defered,
                self.le2mclt.automatique,
                self.le2mclt.gestionnaire_graphique.ecran_attente,
                self.currentperiod, self.histo, txt_summary)
            ecran_recap.show()
            return defered

    # def remote_display_history(self, historique):
    #     """
    #     Fait afficher l'historique
    #     :param historique:
    #     :return:1
    #     """
    #     assert isinstance(historique, list)
    #     logger.debug(u"Appel de remote_afficher_historique")
    #     if self._main_client.simulation or \
    #             self._main_client.automatique:
    #         return 1
    #     ecran_historique = GuiHistorique(
    #         self._main_client.gestionnaire_graphique.ecran_attente,
    #         historique)
    #     ecran_historique.show()
    #     return 1

    def remote_set_payoffs(self, in_euros, in_ecus=None):
        logger.info(u"{} set_payoffs".format(self.le2mclt.uid))
        self._payoffs[self._currentsequence] = {
            "euros": in_euros, "ecus": in_ecus,
            "txt": txt.get_txt_final(in_euros, in_ecus)}

    def remote_display_payoffs_BPK(self, sequence):
        logger.info(u"{} display_payoffs".format(self.le2mclt.uid))
        return self.le2mclt.get_remote("base").remote_display_information(
            self._payoffs[sequence]["txt"])
