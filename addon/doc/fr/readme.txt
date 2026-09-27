# ChatGPT Companion

Par Fernando de Paula Zamboni. Version 0.1.3 (bêta).

Extension NVDA pour lire les nouveaux messages sur le site et dans l’application Windows de ChatGPT. Elle peut lire les réponses automatiquement, lire ou confirmer les messages envoyés et annoncer la progression accessible sans déplacer le focus.

## Objectif

Suivre la conversation sans revenir constamment du champ de saisie vers la dernière réponse. Vous gardez votre compte et votre interface habituels, sans autre client, clé API ou paiement API supplémentaire. La voix et le braille utilisent les réglages de NVDA.

D’autres extensions peuvent proposer des fonctions similaires. Celle-ci se concentre sur les annonces automatiques dans l’interface existante, avec des options indépendantes pour les messages envoyés, les réponses et la progression. Cette aide facultative ne remplace pas les améliorations d’accessibilité de ChatGPT lui-même.

## Installation et utilisation

Téléchargez ChatGPTCompanion-0.1.3.nvda-addon, ouvrez-le avec NVDA actif, confirmez l’installation puis redémarrez NVDA. NVDA 2026.2 ou ultérieur est requis ; la version API déclarée comme testée est 2026.2. Les versions futures peuvent nécessiter une vérification de compatibilité.

Téléchargements : https://github.com/zambonif/ChatGPTCompanion/releases

Code source et signalements : https://github.com/zambonif/ChatGPTCompanion

Ouvrez une conversation dans Chrome ou l’application Windows, attendez un instant et envoyez une question. L’auteur a confirmé la lecture dans les deux environnements avec des versions précédentes. Les corrections de 0.1.3 nécessitent encore des essais réels. Edge, Firefox et Brave restent des cibles expérimentales supplémentaires.

L’historique n’est pas annoncé à l’ouverture. Seule la conversation active est surveillée. Jusqu’à huit contextes sont conservés pendant la session NVDA : en revenant dans une conversation reconnue, une réponse arrivée en votre absence peut être annoncée. Aucune lecture en arrière-plan. Redémarrer NVDA ou basculer la surveillance avec son raccourci efface cette mémoire.

## Paramètres

Menu NVDA, Préférences, Paramètres, ChatGPT Companion. Les mises à jour conservent les réglages. Enregistrez la configuration si l’enregistrement automatique est désactivé.

- Activer la lecture automatique : active ou désactive la surveillance.
- Lire les messages envoyés : lit le contenu après son apparition.
- Confirmer l’envoi : annonce seulement « Message envoyé » lorsque la lecture des messages envoyés est désactivée. Désactivez les deux options pour un envoi silencieux.
- Lire les réponses et Lire les informations de progression : options indépendantes.
- Ignorer les avis et les textes de l’interface : activé par défaut ; filtre les blocs finaux reconnus. Désactivez si un exemple littéral de pied de page en fin de réponse est supprimé.
- Réponse complète : attend un contrôle de fin reconnu et un texte stable. Nouveaux paragraphes est une alternative expérimentale pendant la génération.
- Attente après la fin : 1 à 10 secondes ; défaut 2.
- Solution de repli après silence : 0 à 60 secondes ; défaut 3 pour les nouvelles installations. Utilisée si le contrôle de génération n’est pas reconnu. Une longue pause peut sembler être la fin ; augmentez la valeur si la lecture commence trop tôt. 0 désactive le repli.

## Commandes

NVDA signifie Insert ou Verr Maj selon vos réglages. Réaffectez les commandes dans Gestes de commandes, ChatGPT Companion.

- NVDA+Control+Shift+G : activer ou désactiver la lecture automatique.
- NVDA+Control+Shift+R : lire la dernière réponse disponible, éventuellement partielle. Si une nouvelle question attend sa réponse, l’ancienne n’est pas utilisée à sa place.
- NVDA+Control+Shift+P : lire la dernière information accessible de progression.
- NVDA+Control+Shift+D : actualiser le diagnostic des messages récents et du contrôle de génération.
- Control : arrêter la parole actuelle. Utilisez G pour empêcher les annonces automatiques suivantes.

## Dépannage et limites

Si rien n’est lu, vérifiez Lire les réponses, essayez R et D et vérifiez le repli après silence. Le diagnostic compte la partie récente, pas tout l’historique. Essayez le mode navigation avec NVDA+Espace si la conversation n’est pas reconnue.

L’extension dépend du texte et des titres d’auteur exposés à NVDA. Si elle ne peut obtenir la réponse actuelle, elle indique qu’aucune réponse n’est disponible au lieu d’utiliser volontairement une ancienne réponse mémorisée. Les changements d’interface peuvent affecter la détection. Images, pièces jointes et formules ne sont pas interprétées spécialement. La progression désigne les avis accessibles, pas le raisonnement interne.

La version 0.1.3 cherche depuis la fin et ne rejette plus les historiques de plus de 250 000 caractères. Une réponse individuelle très longue ou un fournisseur sans navigation par titres peut encore ralentir la lecture ou la rendre incomplète. La recherche de repli couvre jusqu’à 2 560 lignes depuis la fin.

Les annonces natives peuvent doubler la parole ; désactivez la progression si nécessaire. Signalez les versions de NVDA et du navigateur/application, la langue, le diagnostic et les étapes de reproduction. Inutile de partager une conversation privée.

## Nouveautés et confidentialité

0.1.3 améliore les longues conversations et les historiques avec champs éditables, actualise le texte à répéter et conserve l’état lors de changements temporaires de focus. La documentation utilisateur a été réorganisée et le manifeste pointe vers le projet avec NVDA 2026.2 comme minimum.

Aucune connexion réseau ni accès aux mots de passe, cookies ou presse-papiers. Le texte accessible reste temporairement en mémoire, sans enregistrement ni envoi. NVDA conserve les réglages. Les écrans sécurisés sont exclus.

GNU GPL version 2 ou ultérieure, sans garantie. Projet indépendant, sans affiliation avec OpenAI ou NV Access. Interface et aide en anglais, portugais brésilien, espagnol, français et italien.
