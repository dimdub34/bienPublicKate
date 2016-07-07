# -*- coding: utf-8 -*-

import logging
from twisted.internet import defer
from collections import OrderedDict
import random
from util import utiltools
from util.utili18n import le2mtrans
import bienPublicKateParams as pms
import bienPublicKateTexts as txt
from bienPublicKateGui import DOrdre

logger = logging.getLogger("le2m.{}".format(__name__))


class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv
        
        # self._traitements_lances = []
        self._current_sequence = 0

        actions = OrderedDict()
        actions[u"Changer le paramètre 'ordre'"] = self._changer_ordre
        actions[le2mtrans(u"Display parameters")] = \
            lambda _: self._le2mserv.gestionnaire_graphique. \
            display_information2(
                utiltools.get_module_info(pms), le2mtrans(u"Parameters"))
        actions[u"Démarrer - baseline"] = lambda _: self._demarrer(
            pms.BASELINE)
        actions[u"Démarrer - prélèvement"] = lambda _: self._demarrer(
            pms.PRELEVEMENT)
        actions[u"Démarrer - désapprobation"] = lambda _: self._demarrer(
            pms.DESAPPROBATION)
        actions[u"Démarrer - désapprobation avec prélèvement"] = lambda _: \
            self._demarrer(pms.DESAPPROBATION_PRELEVEMENT)
        actions[u"Afficher les gains"] = lambda _: self._le2mserv. \
            gestionnaire_experience.display_payoffs_onserver(
            "bienPublicKate")
        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            u"Bien Public Kate", actions)

    @defer.inlineCallbacks
    def _demarrer(self, traitement):

        # check conditions =====================================================
        if self._le2mserv.gestionnaire_joueurs.nombre_joueurs == 0:
            self._le2mserv.gestionnaire_graphique.display_error(
                le2mtrans(u"No clients connected!"))
            return

        if self._le2mserv.gestionnaire_joueurs.nombre_joueurs % \
                pms.TAILLE_GROUPES != 0:
            self._le2mserv.gestionnaire_graphique.display_error(
                le2mtrans(u"The number of players is not compatible with "
                          u"the groups size"))
            return

        # set treatment ========================================================
        pms.TRAITEMENT = traitement

        # set rendement compte individuel
        if pms.TRAITEMENT == pms.BASELINE or pms.TRAITEMENT == pms.DESAPPROBATION:
            pms.RENDEMENT_COMPTE_INDIVIDUEL = pms.RENDEMENT_COMPTE_INDIVIDUEL_NORMAL

        elif pms.TRAITEMENT == pms.PRELEVEMENT or pms.TRAITEMENT == \
                pms.DESAPPROBATION_PRELEVEMENT:
            pms.RENDEMENT_COMPTE_INDIVIDUEL = pms.RENDEMENT_COMPTE_INDIVIDUEL_PRELEVEMENT

        # confirmation start part ==============================================
        confirmation = self._le2mserv.gestionnaire_graphique.question(
            u"Démarrer bien public - " + txt.get_txt_treatment())
        if not confirmation:
            return

        # init part ============================================================
        yield (self._le2mserv.gestionnaire_experience.init_part(
            "bienPublicKate", "PartieBPK", "RemoteBPK", pms))
        self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
            'bienPublicKate')
        self._le2mserv.gestionnaire_graphique.infoserv(
            [u"Traitement: " + txt.get_txt_treatment(),
             u"Rend. cpte indiv: {}".format(pms.RENDEMENT_COMPTE_INDIVIDUEL)])
        # self._traitements_lances.append(pms.TRAITEMENT)

        # configure part (player and remote)
        self._current_sequence += 1
        yield (self._le2mserv.gestionnaire_experience.run_step(
            u"Configure", self._tous, "configure", self._current_sequence))

        # form groups
        self._le2mserv.gestionnaire_groupes.former_groupes(
            self._le2mserv.gestionnaire_joueurs.get_players(),
            pms.TAILLE_GROUPES, forcer_nouveaux=False)

        # start répétitions ====================================================
        for p in range(1, pms.NOMBRE_PERIODES + 1):
            if self._le2mserv.gestionnaire_experience.stop_repetitions:
                break

            # new period -------------------------------------------------------
            self._le2mserv.gestionnaire_graphique.infoserv(
                [None, u"Période {}".format(p)])
            self._le2mserv.gestionnaire_graphique.infoclt(
                [None, u"Période {}".format(p)], fg="white", bg="gray")
            logger.info(u"Start periode {}".format(p))
            yield (self._le2mserv.gestionnaire_experience.run_func(
                self._tous, "new_period", p))

            # set the group in players' data -----------------------------------
            for k, v in self._le2mserv.gestionnaire_groupes. \
                    get_groupes("bienPublicKate").viewitems():
                for j in v:
                    j.currentperiod.BPK_groupe = k
                    for i, l in enumerate(
                            self._le2mserv.gestionnaire_groupes.
                                    get_autres_membres_groupe(j.joueur)):
                        setattr(j.currentperiod, "BPK_membre_{}".format(i), l.uid)

            self._le2mserv.gestionnaire_base.enregistrer()

            # contributions ----------------------------------------------------
            yield (self._le2mserv.gestionnaire_experience.run_step(
                u"Contributions", self._tous, "display_contribution"))

            # group contributions and other group members' contribution --------
            self._le2mserv.gestionnaire_graphique. \
                infoserv(u"Contributions groupes")
            for k, v in self._le2mserv.gestionnaire_groupes. \
                    get_groupes("bienPublicKate").viewitems():
                total_groupe = 0
                for j in v:
                    total_groupe += j.currentperiod.BPK_collectif
                    # other group members' contribution
                    for i, l in enumerate(
                            self._le2mserv.gestionnaire_groupes.
                                    get_autres_membres_groupe(j.joueur)):
                        setattr(j.currentperiod, "BPK_collectif_{}".format(i),
                                l.get_part("bienPublicKate").
                                currentperiod.BPK_collectif)
                for j in v:
                    j.currentperiod.BPK_collectif_groupe = total_groupe
                self._le2mserv.gestionnaire_graphique. \
                    infoserv("G{}: {}".format(k.split("_")[2], total_groupe))

            # disapproval ------------------------------------------------------
            if pms.TRAITEMENT == pms.DESAPPROBATION or pms.TRAITEMENT == \
                    pms.DESAPPROBATION_PRELEVEMENT:

                yield (self._le2mserv.gestionnaire_experience.run_step(
                    u"Désapprobation", self._tous, "display_desapprobation"))

                # each group
                for v in self._le2mserv.gestionnaire_groupes.get_groupes(
                        "bienPublicKate").viewvalues():
                    # each player of the group
                    for j in v:
                        total_contre_j = 0
                        # each of the others in the group
                        for l in self._le2mserv.gestionnaire_groupes.\
                                get_autres_membres_groupe(j.joueur):
                            for m in range(3):
                                if getattr(l.get_part("bienPublicKate").
                                                   currentperiod,
                                           "BPK_membre_{}".format(m)) == \
                                        j.joueur.uid:
                                    desapp = getattr(
                                        l.get_part("bienPublicKate").
                                        currentperiod,
                                        "BPK_desapprobation_{}".format(m))
                                    logger.debug("desapp {} pour {}: {}".format(
                                        l, j.joueur, desapp))
                                    break
                            total_contre_j += desapp
                        j.currentperiod.BPK_desapprobation_recu = total_contre_j
                self._le2mserv.gestionnaire_graphique.infoclt(
                    u"Désapprobations reçues")
                for j in self._tous:
                    j.joueur.info(u"{}".format(
                        j.currentperiod.BPK_desapprobation_recu))

            # period payoffs ---------------------------------------------------
            self._le2mserv.gestionnaire_experience.compute_periodpayoffs(
                "bienPublicKate")

            # summary ----------------------------------------------------------
            yield (self._le2mserv.gestionnaire_experience.run_step(
                u"Récapitulatif", self._tous, "display_summary"))

        # end of part ==========================================================
        # on tire au sort une partie jouée
        # partie_tiree = random.randint(0, len(self._traitements_lances) - 1)
        drawn_sequence = random.randint(1, self._current_sequence)
        self._le2mserv.gestionnaire_graphique.infoserv(
            u"Partie rénumérée: {}".format(drawn_sequence))
        yield (self._le2mserv.gestionnaire_experience.finalize_part(
            "bienPublicKate", drawn_sequence))

    def _changer_ordre(self):
        screen = DOrdre(self._le2mserv.gestionnaire_graphique.screen)
        if screen.exec_():
            pms.ORDRE = screen.get_ordre()
            self._le2mserv.gestionnaire_graphique.infoserv(
                u"Ordre: {}".format(pms.ORDRE))
