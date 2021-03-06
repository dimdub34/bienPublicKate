# -*- coding: utf-8 -*-

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
ORDRE = B_DP_D  # possible de le changer dans le menu de l'expérience
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
DESAPPROBATION_MIN = 0
DESAPPROBATION_STEP = 1

