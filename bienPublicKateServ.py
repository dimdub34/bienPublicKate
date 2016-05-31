# -*- coding: utf-8 -*-

import logging
from twisted.internet import defer
from collections import OrderedDict
import random

from le2mUtile import le2mUtileTools, le2mUtileTwisted
import bienPublicKateParametres as parametres
from bienPublicKatePartie import PartieBPK

logger = logging.getLogger("le2m.{}".format(__name__))


class Serveur(object):
    def __init__(self, main_serveur):
        self._main_serveur = main_serveur
        self._main_serveur.gestionnaire_experience. \
            ajouter_to_remote_parties("bienPublicKate")
        self._traitements_lances = []

        actions = OrderedDict()
        actions[u"Changer le paramètre 'ordre'"] = self._changer_ordre
        actions[u"Afficher les paramètres"] = lambda _: self._main_serveur. \
            gestionnaire_graphique.afficher_information2(
            titre=u"Paramètres",
            texte=le2mUtileTools.get_module_info(parametres))
        actions[u"Démarrer - baseline"] = lambda _: self._demarrer(
            parametres.BASELINE)
        actions[u"Démarrer - prélèvement"] = lambda _: self._demarrer(
            parametres.PRELEVEMENT)
        actions[u"Démarrer - désapprobation"] = lambda _: self._demarrer(
            parametres.DESAPPROBATION)
        actions[u"Démarrer - désapprobation avec prélèvement"] = lambda _: \
            self._demarrer(parametres.DESAPPROBATION_PRELEVEMENT)
        actions[u"Afficher les gains"] = lambda _: self._main_serveur. \
            gestionnaire_experience.afficher_ecran_gains_partie(
            "bienPublicKate")
        actions[u"Faire afficher l'historique complet"] = lambda _: \
            self._faire_afficher_historique()
        self._main_serveur.gestionnaire_graphique. \
            ajouter_to_menu_experience(u"Bien Public Kate", actions)


    @defer.inlineCallbacks
    def _demarrer(self, traitement):
        # set du traitement
        parametres.TRAITEMENT = traitement

        # fixation du rendement du compte individuel en fonction du traitement
        if parametres.TRAITEMENT == parametres.BASELINE or \
                        parametres.TRAITEMENT == parametres.DESAPPROBATION:
            parametres.RENDEMENT_COMPTE_INDIVIDUEL = parametres.\
                RENDEMENT_COMPTE_INDIVIDUEL_NORMAL
        elif parametres.TRAITEMENT == parametres.PRELEVEMENT or \
                        parametres.TRAITEMENT == \
                        parametres.DESAPPROBATION_PRELEVEMENT:
            parametres.RENDEMENT_COMPTE_INDIVIDUEL = parametres.\
                RENDEMENT_COMPTE_INDIVIDUEL_PRELEVEMENT

        traitement_str = u"baseline" if \
            parametres.TRAITEMENT == parametres.BASELINE else \
            u"désapprobation" if parametres.TRAITEMENT == \
                                 parametres.DESAPPROBATION else \
                u"prélèvement" if parametres.TRAITEMENT == \
                                  parametres.PRELEVEMENT else \
                    u"désapprobation avec prélèvement"

        confirmation = self._main_serveur.gestionnaire_graphique. \
            afficher_question(
            u"Démarrrer bien public - {}?".format(traitement_str))
        if not confirmation:
            return

        # initialisation de la partie ==========================================
        self._main_serveur.gestionnaire_experience. \
            initialiser_partie("bienPublicKate", parametres)
        self._main_serveur.gestionnaire_graphique.afficher_info_serveur(
            [u"Traitement: {}".format(traitement_str),
             u"Rend. cpte indiv: {}".format(parametres.
                                            RENDEMENT_COMPTE_INDIVIDUEL)])
        self._traitements_lances.append(parametres.TRAITEMENT)

        # formation des groupes ================================================
        try:
            self._main_serveur.gestionnaire_groupes.former_groupes(
                self._main_serveur.gestionnaire_joueurs.get_liste_joueurs(),
                parametres.TAILLE_GROUPES, forcer_nouveaux=False)
        except (AttributeError, ArithmeticError) as e:
            self._main_serveur.gestionnaire_graphique.afficher_erreur(e.message)
            return

        # creation de la partie chez chq joueur ================================
        for j in self._main_serveur.gestionnaire_joueurs.get_liste_joueurs():
            yield (j.ajouter_partie(PartieBPK(self._main_serveur, j)))
        self._tous = self._main_serveur.gestionnaire_joueurs. \
            get_liste_joueurs('bienPublicKate')

        # on informe les remote clients du traitement
        yield(le2mUtileTwisted.forAll(self._tous, "set_traitement"))

        # début des répétitions ================================================
        for p in xrange(1, parametres.NOMBRE_PERIODES + 1):
            if self._main_serveur.gestionnaire_experience.stop_repetitions:
                break

            # nouvelle periode ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self._main_serveur.gestionnaire_graphique. \
                afficher_info_serveur([None, u"Période {}".format(p)])
            self._main_serveur.gestionnaire_graphique. \
                afficher_info_client([None, u"Période {}".format(p)],
                                     fg="white", bg="gray")
            logger.info(u"Start periode {}".format(p))
            self._main_serveur.gestionnaire_experience.run_func(
                self._tous, "nouvelle_periode", p)

            # mise dans la base du groupe ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            for k, v in self._main_serveur.gestionnaire_groupes. \
                    get_groupes("bienPublicKate").iteritems():
                for j in v:
                    j.periode_courante.BPK_groupe = k
                    for i, l in enumerate(
                            self._main_serveur.gestionnaire_groupes.
                                get_autres_membres_groupe(j.joueur)):
                        setattr(j.periode_courante, "BPK_membre_{}".format(i),
                                l.uid)
            self._main_serveur.gestionnaire_base.enregistrer()

            # décisions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            yield (self._main_serveur.gestionnaire_experience.run_step(
                u"Contributions", self._tous, "afficher_ecran_contribution"))

            # traitement des décisions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self._main_serveur.gestionnaire_graphique. \
                afficher_info_serveur(u"Contributions groupes")
            for k, v in self._main_serveur.gestionnaire_groupes. \
                    get_groupes("bienPublicKate").iteritems():
                total_groupe = 0
                for j in v:
                    total_groupe += j.periode_courante.BPK_collectif
                    # décisions des autres du groupe
                    for i, l in enumerate(
                            self._main_serveur.gestionnaire_groupes.
                                    get_autres_membres_groupe(j.joueur)):
                        setattr(j.periode_courante,
                                "BPK_collectif_{}".format(i),
                                l.get_partie("bienPublicKate").
                                periode_courante.BPK_collectif)
                self._main_serveur.gestionnaire_graphique. \
                    afficher_info_serveur("G{}: {}".format(k.split("_")[2],
                                                           total_groupe))
                for j in v:
                    j.periode_courante.BPK_collectif_groupe = total_groupe

            # désapprobation ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if parametres.TRAITEMENT == parametres.DESAPPROBATION or \
                            parametres.TRAITEMENT == \
                            parametres.DESAPPROBATION_PRELEVEMENT:
                yield (self._main_serveur.gestionnaire_experience.run_step(
                    u"Désapprobation", self._tous,
                    "afficher_ecran_desapprobation"))
                # chq groupe
                for v in self._main_serveur.gestionnaire_groupes. \
                        get_groupes("bienPublicKate").itervalues():
                    logger.debug("v: {}".format(v))
                    # chq joueur du groupe
                    for j in v:
                        total_contre_j = 0
                        # chq autre membre du groupe
                        for l in self._main_serveur.gestionnaire_groupes.\
                                get_autres_membres_groupe(j.joueur):
                            for m in range(3):
                                if getattr(
                                        l.get_partie("bienPublicKate").
                                                periode_courante,
                                           "BPK_membre_{}".format(m)) == \
                                        j.joueur.uid:
                                    desapp = getattr(
                                        l.get_partie("bienPublicKate").
                                        periode_courante,
                                        "BPK_desapprobation_{}".format(m))
                                    logger.debug("desapp {} pour {}: {}".format(
                                        l, j.joueur, desapp))
                                    break
                            total_contre_j += desapp
                        j.periode_courante.BPK_desapprobation_recu = \
                            total_contre_j
                self._main_serveur.gestionnaire_graphique.afficher_info_client(
                    u"Désapprobations reçues")
                for j in self._tous:
                    j.joueur.afficher_info(u"{}".format(
                        j.periode_courante.BPK_desapprobation_recu))

            # calcul des gains de la période ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self._main_serveur.gestionnaire_experience. \
                calculer_gains_periode("bienPublicKate")

            # affichage du récapitulatif de la periode ~~~~~~~~~~~~~~~~~~~~~~~~~
            yield (self._main_serveur.gestionnaire_experience.run_step(
                u"Récapitulatif", self._tous, "afficher_ecran_recapitulatif"))

        # fin de la partie =====================================================
        # on tire au sort une partie jouée
        partie_tiree = random.randint(0, len(self._traitements_lances) - 1)
        self._main_serveur.gestionnaire_graphique.afficher_info_serveur(
            u"Partiée rénumérée: {}".format(partie_tiree + 1))
        self._main_serveur.gestionnaire_experience.finaliser_partie(
            "bienPublicKate", partie_tiree)

    def _changer_ordre(self):
        """
        :return: le numéro d'item sélectionné ou None si annulé
        """
        txt_explic = u"Cette boîte de dialogue permet de changer le paramètre " \
                     u"'Ordre'.\nB=baseline, P=prélèvement et D=Désapprobation " \
                     u"et DP=désapprobation avec prélèvement.\n Donc B_P_D" \
                     u"signifie baseline puis prélèvement puis désapprobation."
        txt_label = u"Choisir l'ordre"
        items = ["B_P_DP", "B_D_DP", "B_DP_D", "B_D_D_1", "B_D_D_2"]
        reponse = self._main_serveur.gestionnaire_graphique. \
            get_choix_combo(txt_explic, txt_label, items)
        if reponse is not None:
            parametres.ORDRE = reponse
            self._main_serveur.gestionnaire_graphique.afficher_statusbar(
                u"Ordre: {}".format(parametres.ORDRE))

    @defer.inlineCallbacks
    def _faire_afficher_historique(self):
        confirm = self._main_serveur.gestionnaire_graphique.afficher_question(
            u"Faire afficher l'historique complet sur les postes?")
        if confirm:
            try:
                yield (self._main_serveur.gestionnaire_experience.run_step(
                    u"Affichage de l'historique complet", self._tous,
                    "faire_afficher_historique"))
            except AttributeError as e:
                self._main_serveur.gestionnaire_graphique.\
                    afficher_avertissement(u"Aucun traitement n'a été lancé!")
