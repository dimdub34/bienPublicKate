# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import logging
import random
from le2mUtile import le2mUtileTools

from le2mClient.le2mClientGui.le2mClientGuiDialogs import GuiHistorique

import bienPublicKateParametres as parametres
from bienPublicKateGuiSrc import bienPublicKateGuiSrcDecision, \
    bienPublicKateGuiSrcDesapprobation

logger = logging.getLogger("le2m.{}".format(__name__))


class GuiDecision(QtGui.QDialog):
    def __init__(self, defered, automatique, ecran_attente, historique,
                 periode):
        QtGui.QDialog.__init__(self, parent=ecran_attente)
        self.ui = bienPublicKateGuiSrcDecision.Ui_Dialog()
        self.ui.setupUi(self)
        self._defered = defered
        self._automatique = automatique

        self.ui.label_periode.setText(u"Période {}".format(periode))
        self.ui.pushButton_historique.clicked.\
            connect(lambda _: self._afficher_historique(historique))
        self.ui.textEdit_explication.setText(parametres.TEXTE_EXPLICATION)
        self.ui.textEdit_explication.setReadOnly(True)
        self.ui.textEdit_explication.setFixedSize(400, 80)
        self.ui.textEdit_message.setVisible(False)  # vient de bienPublicRustam
        self.ui.label_decision.setText(parametres.LABEL_DECISION)
        self.ui.spinBox_decision.setMinimum(parametres.MIN)
        self.ui.spinBox_decision.setMaximum(parametres.MAX)
        self.ui.spinBox_decision.setSingleStep(parametres.STEP)
        self.ui.spinBox_decision.setValue(parametres.MIN)
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.buttonBox.button(QtGui.QDialogButtonBox.Cancel). \
            setVisible(False)
        self.setWindowTitle(u"Décision")
        self.setFixedSize(600, 320)

        if self._automatique:
            self.ui.spinBox_decision.setValue(random.randint(parametres.MIN,
                                                             parametres.MAX))
            try:
                self._timer_automatique.start(7000)
            except AttributeError:
                self._timer_automatique = QtCore.QTimer()
                self._timer_automatique.timeout.connect(self.accept)
                self._timer_automatique.start(7000)

    def reject(self):
        pass

    def accept(self):
        try:
            self._timer_automatique.stop()
        except AttributeError:
            pass
        decision = self.ui.spinBox_decision.value()
        if not self._automatique:
            confirmation = QtGui.QMessageBox.question(
                self, u"Confirmation", u"Vous confirmez votre décision?",
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirmation != QtGui.QMessageBox.Yes:
                return
        logger.info("Renvoi: {}".format(decision))
        self._defered.callback(decision)
        super(GuiDecision, self).accept()

    def _afficher_historique(self, historique):
        ecran_historique = GuiHistorique(self, historique)
        ecran_historique.show()        


class GuiDesapprobation(QtGui.QDialog):
    def __init__(self, defered, automatique, ecran_attente, historique,
                 periode, explication, decisions_membres):
        QtGui.QDialog.__init__(self, parent=ecran_attente)
        self.ui = bienPublicKateGuiSrcDesapprobation.Ui_Dialog()
        self.ui.setupUi(self)
        self._defered = defered
        self._automatique = automatique

        self.ui.label_periode.setText(u"Période {}".format(periode))
        self.ui.pushButton_historique.clicked.\
            connect(lambda _: self._afficher_historique(historique))
        self.ui.textEdit_explication.setText(explication)
        self.ui.textEdit_explication.setReadOnly(True)
        self.ui.textEdit_explication.setFixedSize(400, 80)

        for i in range(3):
            getattr(self.ui, "spinBox_des_{}".format(i)).setMinimum(
                parametres.DESAPPROBATION_MIN)
            getattr(self.ui, "spinBox_des_{}".format(i)).setMaximum(
                parametres.DESAPPROBATION_MAX)
            getattr(self.ui, "spinBox_des_{}".format(i)).setSingleStep(
                parametres.DESAPPROBATION_STEP)
            getattr(self.ui, "spinBox_des_{}".format(i)).setValue(
                parametres.DESAPPROBATION_MIN)

        self._ordre = range(3)
        random.shuffle(self._ordre)
        self._decisions_membres = decisions_membres
        for i, o in enumerate(self._ordre):
            getattr(self.ui, "spinBox_{}".format(i)).setValue(
                self._decisions_membres[o])

        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.buttonBox.button(QtGui.QDialogButtonBox.Cancel). \
            setVisible(False)
        self.setWindowTitle(u"Points de désapprobation")
        self.setFixedSize(600, 320)

        if self._automatique:
            for i in range(3):
                getattr(self.ui, "spinBox_des_{}".format(i)).setValue(
                    random.randint(0, parametres.DESAPPROBATION_MAX)
                )
            try:
                self._timer_automatique.start(7000)
            except AttributeError:
                self._timer_automatique = QtCore.QTimer()
                self._timer_automatique.timeout.connect(self.accept)
                self._timer_automatique.start(7000)

    def reject(self):
        pass

    def accept(self):
        try:
            self._timer_automatique.stop()
        except AttributeError:
            pass
        decisions = dict()
        for i, o in enumerate(self._ordre):
            decisions[o] = getattr(self.ui, "spinBox_des_{}".format(i)).value()
            if decisions[o] < 0:
                QtGui.QMessageBox.warning(
                    self, u"Attention", u"Vous devez saisir une valeur "
                                        u"comprise entre 0 et {}.".format(
                        parametres.DESAPPROBATION_MAX)
                )
                return
        if not self._automatique:
            confirmation = QtGui.QMessageBox.question(
                self, u"Confirmation", u"Vous confirmez vos décisions?",
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirmation != QtGui.QMessageBox.Yes:
                return
        self._defered.callback(decisions)
        logger.info("Renvoi: {}".format(decisions))
        super(GuiDesapprobation, self).accept()

    def _afficher_historique(self, historique):
        ecran_historique = GuiHistorique(self, historique)
        ecran_historique.show()
