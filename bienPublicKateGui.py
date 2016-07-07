# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from client.cltgui.cltguidialogs import GuiHistorique
from client.cltgui.cltguiwidgets import WLabel, WPeriod, WExplication, \
    WSpinbox, WCombo
from util.utili18n import le2mtrans
import logging
import random

import bienPublicKateParams as pms
import bienPublicKateTexts as txt
from bienPublicKateGuiSrc import BPK_wid_desapprobation


logger = logging.getLogger("le2m.{}".format(__name__))


class DDecision(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, historique, period):
        QtGui.QDialog.__init__(self, parent)

        self._defered = defered
        self._automatique = automatique
        self._historique = GuiHistorique(self, historique, size=(700, 500))

        layout = QtGui.QVBoxLayout(self)

        wperiod = WPeriod(period=period, ecran_historique=self._historique,
                          parent=self)
        layout.addWidget(wperiod)

        wexplanation = WExplication(
            text=txt.get_expl_decision(), parent=self, size=(500, 60))
        layout.addWidget(wexplanation)

        self._wdecision = WSpinbox(label=txt.get_lab_decision(), minimum=pms.MIN,
                             maximum=pms.MAX, interval=pms.STEP, parent=self,
                             automatique=self._automatique)
        layout.addWidget(self._wdecision)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        self.setWindowTitle(le2mtrans(u"Decision"))
        self.adjustSize()
        self.setFixedSize(self.size())

        if self._automatique:
            self._timer_automatique = QtCore.QTimer()
            self._timer_automatique.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer_automatique.start(7000)

    def reject(self):
        pass

    def _accept(self):
        try:
            self._timer_automatique.stop()
        except AttributeError:
            pass

        try:
            decision = self._wdecision.get_value()
        except ValueError as e:
            return QtGui.QMessageBox.warning(
                self, le2mtrans(u"Warning"), e.message)

        if not self._automatique:
            if not QtGui.QMessageBox.question(
                self, le2mtrans(u"Confirmation"),
                le2mtrans(u"Do you confirm your choice?"),
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes) == \
                    QtGui.QMessageBox.Yes:
                return

        logger.info(u"Send back {}".format(decision))
        self.accept()
        self._defered.callback(decision)


class WDesapprobation(QtGui.QWidget):
    def __init__(self, parent, dec_to_display, automatique=False):
        QtGui.QWidget.__init__(self, parent)

        self.ui = BPK_wid_desapprobation.Ui_Form()
        self.ui.setupUi(self)

        labels = txt.get_labs_desapprobation()
        self.ui.label_compte.setText(labels[1])
        self.ui.label_desapprobation.setText(labels[2])

        for i in range(3):
            spb_cpte = getattr(self.ui, "spinBox_{}".format(i))
            spb_cpte.setValue(dec_to_display[i])
            spb_cpte.setReadOnly(True)
            spb_desapp = getattr(self.ui, "spinBox_des_{}".format(i))
            spb_desapp.setMinimum(pms.DESAPPROBATION_MIN)
            spb_desapp.setMaximum(pms.DESAPPROBATION_MAX)
            spb_desapp.setSingleStep(pms.DESAPPROBATION_STEP)

        if automatique:
            for i in range(3):
                spb_desapp = getattr(self.ui, "spinBox_des_{}".format(i))
                spb_desapp.setValue(random.randint(
                    pms.DESAPPROBATION_MIN, pms.DESAPPROBATION_MAX))

    def get_desapprobations(self):
        return [getattr(self.ui, "spinBox_des_{}".format(i)).value()
                for i in range(3)]


class GuiDesapprobation(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, historique,
                 period, explication, decisions_membres):
        QtGui.QDialog.__init__(self, parent)

        self._defered = defered
        self._automatique = automatique
        self._historique = GuiHistorique(self, historique, size=(700, 500))

        layout = QtGui.QVBoxLayout(self)

        wperiod = WPeriod(period=period, ecran_historique=self._historique,
                          parent=self)
        layout.addWidget(wperiod)

        wexplanation = WExplication(
            text=explication, parent=self, size=(500, 60))
        layout.addWidget(wexplanation)

        lab_desapprobation = WLabel(parent=self,
                                    text=txt.get_labs_desapprobation()[0])
        layout.addWidget(lab_desapprobation)

        self._ordre = range(3)
        random.shuffle(self._ordre)
        dec_to_display = [decisions_membres.get(i) for i in self._ordre]
        self._wid_desapprobation = WDesapprobation(
            parent=self, dec_to_display=dec_to_display,
            automatique=self._automatique)
        layout.addWidget(self._wid_desapprobation)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        self.setWindowTitle(le2mtrans(u"Désapprobation"))
        self.adjustSize()
        self.setFixedSize(self.size())

        if self._automatique:
            self._timer_automatique = QtCore.QTimer()
            self._timer_automatique.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer_automatique.start(7000)

    def reject(self):
        pass

    def _accept(self):
        try:
            self._timer_automatique.stop()
        except AttributeError:
            pass
        desapprob = self._wid_desapprobation.get_desapprobations()
        desapprob_affectees = {}
        for i, val in enumerate(self._ordre):
            desapprob_affectees[val] = desapprob[i]
        if not self._automatique:
            confirmation = QtGui.QMessageBox.question(
                self, u"Confirmation", u"Vous confirmez vos décisions?",
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirmation != QtGui.QMessageBox.Yes:
                return
        self._defered.callback(desapprob_affectees)
        logger.info("Renvoi: {}".format(desapprob_affectees))
        self.accept()


class DOrdre(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)

        layout = QtGui.QVBoxLayout(self)

        wexpl = WExplication(parent=self, text=txt.get_expl_ordres())
        layout.addWidget(wexpl)

        self._combo_ordres = WCombo(parent=self, label=u"Choisir l'ordre",
                              items=["B_P_DP", "B_D_DP", "B_DP_D", "B_D_D_1",
                                     "B_D_D_2"])
        self._combo_ordres.ui.comboBox.setCurrentIndex(pms.ORDRE)
        layout.addWidget(self._combo_ordres)

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

        self.setWindowTitle(le2mtrans(u"Choix ordre"))
        self.adjustSize()
        self.setFixedSize(self.size())

    def get_ordre(self):
        return self._combo_ordres.get_currentindex()
