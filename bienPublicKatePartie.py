# -*- coding: utf-8 -*-

from __future__ import division
from twisted.internet import defer
import logging
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey

from le2mServ.le2mServBase import Base
from le2mServ.le2mServParties import Partie
from le2mUtile.le2mUtileTools import get_monnaie
import bienPublicKateParametres as parametres

logger = logging.getLogger("le2m.{}".format(__name__))


class PartieBPK(Partie):
    __tablename__ = "partie_bienPublicKate"
    __mapper_args__ = {'polymorphic_identity': 'bienPublicKate'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    repetitions = relationship('RepetitionsBPK')

    def __init__(self, main_serveur, joueur):
        super(PartieBPK, self).__init__("bienPublicKate", "BPK")
        self._main_serveur = main_serveur
        self.joueur = joueur
        self.BPK_gain_ecus, self.BPK_gain_euros = 0, 0
        self._texte_final = ""
        self._histo_vars = ["BPK_periode", "BPK_individuel", "BPK_collectif",
                            "BPK_collectif_groupe", "BPK_gain_individuel",
                            "BPK_gain_collectif", "BPK_gain_periode",
                            "BPK_gain_cumule"
                            ]
        self._histo = [[u"Période", u"Compte\nindividuel", u"Compte\ncollectif",
                        u"Total\ncompte\ncollectif", u"Gain\ncompte\nindividuel",
                        u"Gain\ncompte\ncollectif", u"Gain\npériode",
                        u"Gain\ncumulé"]
                       ]
        self._periodes = {}
        self._liste_periodes = []

    @defer.inlineCallbacks
    def set_traitement(self):
        """
        Cette fonction est appelée au lancement d'un nouvelle partie
        :return:
        """
        yield (self.remote.callRemote(
            "set_traitement", parametres.TRAITEMENT))
        self._periodes.clear()
        del self._histo[1:]

    def nouvelle_periode(self, periode):
        logger.debug("nouvelle_periode")
        periode_new = RepetitionsBPK(periode)
        self._main_serveur.gestionnaire_base.ajouter(periode_new)
        self.repetitions.append(periode_new)
        self.periode_courante = periode_new
        logger.info("Période {} -> Ok".format(periode))

    @defer.inlineCallbacks
    def afficher_ecran_contribution(self):
        """
        Fait afficher l'écran de contribution sur les postes clients.
        """
        decision_start = datetime.now()
        self.periode_courante.BPK_collectif = yield (
            self.remote.callRemote(
                "afficher_ecran_contribution",
                self.periode_courante.BPK_periode
            )
        )
        decision_end = datetime.now()
        self.periode_courante.BPK_decision_time = (
            decision_end - decision_start
        ).seconds
        self.periode_courante.BPK_individuel = \
            self.periode_courante.BPK_dotation - \
            self.periode_courante.BPK_collectif
        self.joueur.afficher_info("{}".format(
            self.periode_courante.BPK_collectif)
        )
        self.joueur.remove_wait_mode()

    @defer.inlineCallbacks
    def afficher_ecran_desapprobation(self):
        """
        :param: les décisions de tous les membres du groupe. C'est un dictionnaire
        avec l'uid et la décision
        :return:
        """
        decisions_membres_groupe = dict()
        for i in range(3):
            decisions_membres_groupe[i] = \
                getattr(self.periode_courante, "BPK_collectif_{}".format(i))
        logger.debug("decisions_membres_groupe: {}".format(
            decisions_membres_groupe)
        )
        explic_desapprobation = parametres.get_explication_desapprobation(
            self.periode_courante.BPK_collectif,
            self.periode_courante.BPK_collectif_groupe
        )
        desapprobation_start = datetime.now()
        desapprobations = yield (self.remote.callRemote(
            "afficher_ecran_desapprobation", self.periode_courante.BPK_periode,
            explic_desapprobation, decisions_membres_groupe)
        )
        desapprobation_end = datetime.now()
        self.periode_courante.BPK_desapprobation_time = (
            desapprobation_end - desapprobation_start
        ).seconds
        for k, v in desapprobations.iteritems():
            setattr(self.periode_courante, "BPK_desapprobation_{}".format(k), v)
        self.joueur.afficher_info(u"{}".format(
            ["j{}: {}".format(getattr(self.periode_courante,
                                      "BPK_membre_{}".format(k)
                                      ).split("_")[2], v) for k, v in
             desapprobations.items()])
        )
        self.joueur.remove_wait_mode()

    def calculer_gain_periode(self):
        logger.debug(u"call of calculer_gain_periode")
        self.periode_courante.BPK_gain_individuel = self.periode_courante. \
            BPK_individuel * parametres.RENDEMENT_COMPTE_INDIVIDUEL
        self.periode_courante.BPK_gain_collectif = \
            self.periode_courante.BPK_collectif_groupe * parametres.MPCR
        self.periode_courante.BPK_gain_periode = \
            self.periode_courante.BPK_gain_individuel + \
            self.periode_courante.BPK_gain_collectif

        if self.periode_courante.BPK_periode == 1:
            self.periode_courante.BPK_gain_cumule = self.periode_courante. \
                BPK_gain_periode
        else:
            self.periode_courante.BPK_gain_cumule = \
                self._periodes[
                    self.periode_courante.BPK_periode - 1].BPK_gain_cumule + \
                self.periode_courante.BPK_gain_periode
        self._periodes[self.periode_courante.BPK_periode] = self.periode_courante
        logger.info("Joueur {} - gains: {},{}".format(
            self.joueur, self.periode_courante.BPK_gain_periode,
            self.periode_courante.BPK_gain_cumule))

    @defer.inlineCallbacks
    def afficher_ecran_recapitulatif(self):
        # recap ================================================================
        params = [self.periode_courante.BPK_individuel,
                  self.periode_courante.BPK_collectif,
                  self.periode_courante.BPK_collectif_groupe,
                  self.periode_courante.BPK_gain_individuel,
                  self.periode_courante.BPK_gain_collectif,
                  self.periode_courante.BPK_gain_periode]
        if self.periode_courante.BPK_traitement == parametres.DESAPPROBATION or \
                self.periode_courante.BPK_traitement == \
                parametres.DESAPPROBATION_PRELEVEMENT:
            params.append(self.periode_courante.BPK_desapprobation_recu)
        texte_recap = parametres.get_texte_recapitulatif(*params)

        # historique ===========================================================
        self._histo.append([getattr(self.periode_courante, e) for e in
                            self._histo_vars])

        yield (self.remote.callRemote(
            "afficher_ecran_recapitulatif", texte_recap, self._histo,
            self.periode_courante.BPK_periode))
        self.joueur.afficher_info("Ok")
        self.joueur.remove_wait_mode()

    def calculer_gain_partie(self, partie_tiree):
        """
        :param partie_tiree: la sequence tirée au sort
        :return:
        """
        self._liste_periodes.append(self._periodes.copy())
        assert (partie_tiree <= len(self._liste_periodes))
        logger.debug(u"Partie tirée: {}".format(partie_tiree))
        self.BPK_gain_ecus = self._liste_periodes[partie_tiree][parametres.
            NOMBRE_PERIODES].BPK_gain_cumule
        self.BPK_gain_euros = self.BPK_gain_ecus * parametres.TAUX_CONVERSION
        self._texte_final = u"C'est la partie {} qui a été tirée au sort pour \
la rémunération. A cette partie vous avez gagné {:.2f} {}, soit {:.2f} {}.".\
            format(partie_tiree + 1, self.BPK_gain_ecus,
                   get_monnaie(self.BPK_gain_ecus), self.BPK_gain_euros,
                   get_monnaie(self.BPK_gain_euros, u"euro"))
        logger.debug('gain ecus:{}, gain euros: {:.2f}'.format(
            self.BPK_gain_ecus, self.BPK_gain_euros))

    @defer.inlineCallbacks
    def faire_afficher_historique(self):
        del self._histo[1:]
        for partie in self._liste_periodes:
            cles = partie.keys()
            cles.sort()
            for p in cles:
                self._histo.append([getattr(partie[p], e) for e in
                                    self._histo_vars])
        yield (self.remote.callRemote("afficher_historique", self._histo))
        self.joueur.afficher_info(u"Ok")
        self.joueur.remove_wait_mode()


class RepetitionsBPK(Base):
    __tablename__ = 'partie_bienPublicKate_repetitions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_partie_id = Column(Integer,
                              ForeignKey("partie_bienPublicKate.partie_id"))

    BPK_periode = Column(Integer)
    BPK_traitement = Column(Integer)
    BPK_ordre = Column(Integer)
    BPK_groupe = Column(String(50))
    BPK_membre_0 = Column(String(50))
    BPK_membre_1 = Column(String(50))
    BPK_membre_2 = Column(String(50))
    BPK_dotation = Column(Integer)
    BPK_individuel = Column(Integer)
    BPK_collectif = Column(Integer)
    BPK_collectif_groupe = Column(Integer)
    BPK_decision_time = Column(Integer)
    BPK_collectif_0 = Column(Integer)
    BPK_collectif_1 = Column(Integer)
    BPK_collectif_2 = Column(Integer)
    BPK_desapprobation_0 = Column(Integer)
    BPK_desapprobation_1 = Column(Integer)
    BPK_desapprobation_2 = Column(Integer)
    BPK_desapprobation_recu = Column(Integer)
    BPK_desapprobation_time = Column(Integer)
    BPK_gain_individuel = Column(Float)
    BPK_gain_collectif = Column(Float)
    BPK_gain_periode = Column(Float)
    BPK_gain_cumule = Column(Float)

    def __init__(self, periode):
        self.BPK_traitement = parametres.TRAITEMENT
        self.BPK_ordre = parametres.ORDRE
        self.BPK_periode = periode
        self.BPK_dotation = parametres.DOTATION
        self.BPK_decision_time = 0
        self.BPK_gain_periode = 0
        self.BPK_gain_cumule = 0
