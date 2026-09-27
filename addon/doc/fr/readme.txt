# ChatGPT Companion 0.1.2 — version expérimentale

Par Fernando de Paula Zamboni. https://www.blog.fernandozamboni.com

Lit les messages envoyés, les réponses et les informations de progression accessibles dans la conversation ChatGPT active, sans déplacer le focus. Utilise la voix et le braille de NVDA. Interface et documentation en portugais brésilien, anglais, espagnol, français et italien.

## Modifications de la version 0.1.2

Ignorer les avis et les textes de l’interface est activé par défaut. Supprime le bloc final connu signalant les erreurs possibles, suivi de « Réponse la plus récente », en lecture automatique et avec la commande de répétition. Ce n’est pas un remplacement global : les phrases isolées, les exemples entre guillemets et les références au milieu de la réponse sont conservés. La reconnaissance est textuelle ; si une réponse se termine littéralement par ce bloc complet, désactivez l’option pour l’entendre. Les autres pieds de page non reconnus peuvent rester.

Une ancienne réponse n’est plus remise en file lors d’un nouvel envoi ou lorsqu’une réponse déjà annoncée disparaît puis revient dans l’arbre d’accessibilité. Les nouvelles installations utilisent un repli après silence de 3 secondes ; les réglages existants sont conservés. L’utilisateur a confirmé la lecture automatique avec ce repli dans Chrome et l’application Windows avec la version 0.1.1. Cette mise à jour doit encore être testée dans les deux environnements avant publication.

## Modification de la version 0.1.1

Correction des annonces répétées du message envoyé lors des mises à jour de la page. Chaque nouvel envoi est annoncé une fois ; les modifications du même texte ou sa disparition temporaire ne déclenchent pas une autre annonce. Un nouvel envoi avec un texte identique reste reconnu. Pour un envoi silencieux, désactivez Lire les messages envoyés et Confirmer l’envoi. Modifier un message existant sans en ajouter un autre ne déclenche pas une nouvelle lecture automatique de l’envoi.

## Installation et premier essai
Ouvrez fzChatGPTCompanion-0.1.2.nvda-addon, confirmez l’installation et redémarrez NVDA lorsque cela est demandé. Compatibilité déclarée : NVDA 2025.1 à 2026.2 ; des essais réels sous Windows restent nécessaires. lastTestedNVDAVersion représente la cible de compatibilité du paquet expérimental, pas un test d’exécution effectué.

Commencez par une conversation courte dans Chrome sur https://chatgpt.com. Attendez environ deux secondes puis envoyez une question simple. Votre message, les informations reconnues et la réponse terminée devraient être lus. L’historique n’est pas annoncé. Changer d’onglet, de conversation ou d’application établit une nouvelle référence ; les changements reçus en votre absence ne sont pas annoncés au retour. Gardez la conversation active pendant l’essai.

Edge, Firefox, Brave et l’application ChatGPT pour Windows sont des cibles expérimentales. L’application doit exposer un document avec du texte accessible structuré. Chaque environnement doit être validé. Aucune clé ni facturation supplémentaire de l’API ChatGPT n’est nécessaire.

## Paramètres
Ouvrez le menu NVDA, Préférences, Paramètres, ChatGPT Companion. Utilisez Tab, Espace et les flèches, puis OK. Enregistrez la configuration de NVDA si l’enregistrement à la fermeture est désactivé.

- Activer la lecture automatique : active ou désactive la surveillance.
- Lire les messages envoyés : lit le contenu après son apparition dans la conversation, pas simplement après Entrée.
- Confirmer l’envoi : si la lecture des messages envoyés est désactivée, annonce seulement « Message envoyé ». Désactivez les deux options pour un envoi silencieux.
- Lire les réponses et Lire les informations de progression : réglages indépendants.
- Réponse complète : par défaut ; attend un contrôle d’envoi reconnu et deux secondes sans modification du texte.
- Nouveaux paragraphes : expérimental ; lit les paragraphes terminés pendant la génération. Les révisions du site peuvent provoquer des répétitions. Sans séparation de paragraphes, la lecture peut attendre la fin.
- Attente après la fin : de 1 à 10 secondes ; valeur par défaut 2.
- Solution de repli après silence : de 0 à 60 secondes ; 0 désactive cette option et la valeur par défaut des nouvelles installations est 3. Sans contrôle de génération reconnu, une valeur telle que 8 déduit la fin après un silence. Une pause peut déclencher une lecture prématurée ; ce n’est pas une garantie de fin.

## Raccourcis
NVDA correspond à Insert ou Verr Maj selon votre configuration. Modifiez les raccourcis dans Préférences, Gestes de commandes, ChatGPT Companion.

- NVDA+Control+Shift+G : activer ou désactiver la lecture automatique.
- NVDA+Control+Shift+R : lire la dernière réponse disponible, éventuellement partielle. Fonctionne lorsque la lecture automatique est désactivée.
- NVDA+Control+Shift+P : lire la dernière information de progression disponible.
- NVDA+Control+Shift+D : annoncer le nombre de messages reconnus et l’état du contrôle de génération.
- Control : arrêter la parole actuelle avec le comportement normal de NVDA. Utilisez le raccourci G pour empêcher les annonces suivantes.

## Limites et dépannage
« Réflexion » désigne uniquement un état ou un résumé exposé par l’interface. L’extension ne récupère pas le raisonnement interne, le texte caché ou les contenus inaccessibles à NVDA. Elle reconnaît les titres d’auteur et les contrôles dans cinq langues ; les changements d’interface peuvent nécessiter une mise à jour. Pas d’interprétation particulière des images, pièces jointes et formules.

Si le diagnostic indique zéro message, vérifiez qu’un message a été envoyé et essayez le mode navigation avec NVDA+Espace, puis Chrome ou Edge si nécessaire. Si les messages sont reconnus mais pas le contrôle de génération, utilisez la lecture manuelle ou le repli après silence. Les conversations de plus de 250 000 caractères sont ignorées pour limiter le traitement ; d’autres longues conversations peuvent aussi ralentir le lecteur.

Les annonces natives des régions dynamiques de NVDA ou du site peuvent doubler la parole. Désactivez si nécessaire la lecture de progression de l’extension. Elle ne supprime pas globalement les annonces natives. Pour signaler un problème, indiquez les versions du navigateur ou de l’application et de NVDA, la langue de l’interface et le diagnostic ; inutile de partager la conversation. Avant publication, testez le changement d’onglet, l’installation, la suppression, l’enregistrement des paramètres et les quatre commandes.

## Confidentialité, licence et distribution
Aucun accès au réseau, aux cookies, aux mots de passe, au presse-papiers ou aux fichiers de conversation. Le texte accessible est traité en mémoire pendant que la conversation est active, sans enregistrement ni envoi. Les écrans sécurisés de Windows sont exclus. NVDA conserve les paramètres.

GNU GPL version 2 ou ultérieure, sans garantie ; voir COPYING.txt. Projet indépendant, sans affiliation avec OpenAI ou NV Access. Le manifest.ini racine est en anglais ; les traductions sont dans locale. Avant soumission à la boutique, testez sous Windows, vérifiez la compatibilité déclarée et publiez le code source et un lien HTTPS direct vers le paquet. La structure du paquet ne garantit pas son approbation.
