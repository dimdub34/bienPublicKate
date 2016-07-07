# -*- coding: utf-8 -*-

from __future__ import division
from twisted.internet import defer
import logging
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from server.servbase import Base
from server.servparties import Partie
import bienPublicKateParams as pms
import bienPublicKateTexts as txt
from util.utiltools import get_module_attributes


logger = logging.getLogger("le2m.{}".format(__name__))


class PartieBPK(Partie):
    __tablename__ = "partie_bienPublicKate"
    __mapper_args__ = {'polymorphic_identity': 'bienPublicKate'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    repetitions = relationship('RepetitionsBPK')

    def __init__(self, main_serveur, joueur):
        super(PartieBPK, self).__init__(
            nom="bienPublicKate", nom_court="BPK", joueur=joueur,
            le2mserv=main_serveur)
        self.BPK_gain_ecus = 0
        self.BPK_gain_euros = 0
        self._sequences = {}

    @defer.inlineCallbacks
    def configure(self, currentsequence):
        logger.debug(u"{} Configure".format(self.joueur))
        self._currentsequence = currentsequence
        self.periods.clear()
        yield (self.remote.callRemote("configure", get_module_attributes(pms),
                                      self._currentsequence))
        self.joueur.info(u"Ok")

    @defer.inlineCallbacks
    def new_period(self, period):
        logger.debug("nouvelle_periode")
        periode_new = RepetitionsBPK(period)
        self.le2mserv.gestionnaire_base.ajouter(periode_new)
        self.repetitions.append(periode_new)
        self.currentperiod = periode_new
        yield (self.remote.callRemote("new_period", period))
        logger.info("Periode {} -> Ok".format(period))

    @defer.inlineCallbacks
    def display_contribution(self):
        decision_start = datetime.now()
        self.currentperiod.BPK_collectif = yield (
            self.remote.callRemote("display_contribution"))
        self.currentperiod.BPK_decision_time = (
            datetime.now() - decision_start).seconds
        self.currentperiod.BPK_individuel = \
            self.currentperiod.BPK_dotation - \
            self.currentperiod.BPK_collectif
        self.joueur.info("{}".format(self.currentperiod.BPK_collectif))
        self.joueur.remove_waitmode()

    @defer.inlineCallbacks
    def display_desapprobation(self):
        """
        :param: les décisions de tous les membres du groupe.
        C'est un dictionnaire avec l'uid et la décision
        :return:
        """
        decisions_membres_groupe = dict()
        for i in range(3):
            decisions_membres_groupe[i] = \
                getattr(self.currentperiod, "BPK_collectif_{}".format(i))
        logger.debug("decisions_membres_groupe: {}".format(
            decisions_membres_groupe))

        explic_desapprobation = txt.get_expl_desapprobation(
            self.currentperiod.BPK_collectif,
            self.currentperiod.BPK_collectif_groupe)

        desapprobation_start = datetime.now()
        desapprobations = yield (self.remote.callRemote(
            "display_desapprobation", explic_desapprobation,
            decisions_membres_groupe))
        desapprobation_end = datetime.now()

        self.currentperiod.BPK_desapprobation_time = (
            desapprobation_end - desapprobation_start).seconds
        for k, v in desapprobations.viewitems():
            setattr(self.currentperiod, "BPK_desapprobation_{}".format(k), v)

        self.joueur.info(u"{}".format(
            ["j{}: {}".format(
                getattr(self.currentperiod, "BPK_membre_{}".format(k)).\
                    split("_")[2], v) for k, v in desapprobations.items()]))
        self.joueur.remove_waitmode()

    def compute_periodpayoff(self):
        logger.debug(u"call of compute_periodpayoff")

        self.currentperiod.BPK_gain_individuel = self.currentperiod. \
            BPK_individuel * pms.RENDEMENT_COMPTE_INDIVIDUEL
        self.currentperiod.BPK_gain_collectif = \
            self.currentperiod.BPK_collectif_groupe * pms.MPCR
        self.currentperiod.BPK_periodpayoff = \
            self.currentperiod.BPK_gain_individuel + \
            self.currentperiod.BPK_gain_collectif

        # cumulative payoff
        if self.currentperiod.BPK_periode == 1:
            self.currentperiod.BPK_cumulativepayoff = self.currentperiod. \
                BPK_periodpayoff
        else:
            self.currentperiod.BPK_cumulativepayoff = \
                self.periods[
                    self.currentperiod.BPK_periode - 1].BPK_cumulativepayoff + \
                self.currentperiod.BPK_periodpayoff

        # save the period
        self.periods[self.currentperiod.BPK_periode] = self.currentperiod

        logger.info("Joueur {} - gains: {},{}".format(
            self.joueur, self.currentperiod.BPK_periodpayoff,
            self.currentperiod.BPK_cumulativepayoff))

    @defer.inlineCallbacks
    def display_summary(self):
        period_dict = self.currentperiod.todict()
        yield (self.remote.callRemote(
            "display_summary", period_dict))
        self.joueur.info("Ok")
        self.joueur.remove_waitmode()

    @defer.inlineCallbacks
    def compute_partpayoff(self, which_sequence):
        self._sequences[self._currentsequence] = self.periods.copy()
        logger.debug(u"Partie tirée: {}".format(which_sequence))
        self.BPK_gain_ecus = self._sequences[which_sequence][pms.
            NOMBRE_PERIODES].BPK_cumulativepayoff
        self.BPK_gain_euros = float("{:.2f}".format(
            self.BPK_gain_ecus * pms.TAUX_CONVERSION))
        yield (self.remote.callRemote(
            "set_payoffs", self.BPK_gain_ecus, self.BPK_gain_euros))
        logger.debug('gain ecus:{}, gain euros: {:.2f}'.format(
            self.BPK_gain_ecus, self.BPK_gain_euros))


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
    BPK_periodpayoff = Column(Float)
    BPK_cumulativepayoff = Column(Float)

    def __init__(self, periode):
        self.BPK_traitement = pms.TRAITEMENT
        self.BPK_ordre = pms.ORDRE
        self.BPK_periode = periode
        self.BPK_dotation = pms.DOTATION
        self.BPK_decision_time = 0
        self.BPK_periodpayoff = 0
        self.BPK_cumulativepayoff = 0

    def todict(self, joueur=None):
        temp = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if joueur:
            temp["joueur"] = joueur
        return temp
