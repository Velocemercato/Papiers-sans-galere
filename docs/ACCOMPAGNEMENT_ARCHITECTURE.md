# Papiers Sans Galère – service d'accompagnement administratif

Document de travail préparé par Claude (18 octobre 2026). Il décrit la démonstration livrée et ce qu'il faut pour passer à une vraie version payante. Rien ici n'est encore en service.

## 1. Ce que contient la démonstration (`accompagnement.html`)

- **Mode test uniquement** : bandeau permanent, aucune donnée réelle, aucun paiement réel. Les dossiers fictifs sont stockés dans le navigateur de la personne qui teste (localStorage), jamais sur GitHub.
- **Vue client** : « Faire une demande », « Mes dossiers » avec, pour chaque dossier, l'avancement, les messages, « Mon devis » et « Mes documents ».
- **Vue administrateur** : liste filtrable par statut, lecture de la demande, réponse, devis ligne par ligne (prix, délai, exclusions), suivi du paiement, préparation, vérification humaine obligatoire, transmission.
- **Statuts** : demande reçue → en étude → devis envoyé → paiement confirmé → en préparation → à vérifier → terminé, plus « hors périmètre ».
- **Garde-fous** :
  - deux cases obligatoires avant l'envoi (pas de documents sensibles, aide administrative et non conseil juridique) ;
  - blocage des messages contenant un numéro de sécurité sociale, un IBAN ou un mot de passe ;
  - détection de mots-clés juridiques (divorce, succession, litige…) : message d'orientation côté client, alerte côté administrateur, bouton « Hors périmètre » ;
  - devis à accepter avec les CGV et la demande d'exécution avant la fin du délai de rétractation ;
  - assistance IA facultative, seulement si le client l'a autorisée, et toujours suivie d'une relecture humaine cochée ;
  - le brouillon de démonstration est un modèle fixe : aucune IA réelle n'est appelée.

## 2. Ce que la démonstration ne fait pas (et ne doit pas faire sur GitHub Pages)

GitHub Pages ne sert que des fichiers publics. Il est **impossible** d'y stocker des dossiers privés en sécurité : un fichier JSON ou un élément HTML masqué reste lisible par tout le monde. La vraie version demande un hébergement avec serveur.

## 3. Architecture proposée pour la vraie version

| Brique | Rôle | Points d'attention |
|---|---|---|
| Hébergement applicatif | Pages et API du service | Hébergeur situé dans l'Union européenne de préférence |
| Base de données | Dossiers, messages, devis, statuts | Accès limité par utilisateur (chaque client ne voit que ses dossiers), chiffrement au repos, sauvegardes quotidiennes |
| Authentification | Connexion client et administrateur | Lien de connexion par e-mail ou mot de passe solide, double authentification pour l'administrateur |
| Stockage de fichiers | Documents livrés au client | Accès par lien signé à durée limitée, chiffrement, suppression automatique |
| Paiement | Encaissement du devis | Prestataire reconnu (par exemple Stripe Checkout) ; le dossier ne passe « paiement confirmé » qu'à réception de l'événement de paiement vérifié côté serveur (webhook signé), jamais sur la seule redirection du navigateur |
| Notifications | Prévenir Romain d'une nouvelle demande | E-mail ou notification sans contenu sensible (« Nouvelle demande D-0042 ») |
| Assistance IA | Brouillons de documents de travail | API Anthropic appelée depuis le serveur seulement, clé secrète jamais dans le navigateur, plafond de dépense, données minimisées (pas de pièces d'identité ni de numéros), consentement explicite du client, relecture humaine obligatoire |
| Journal | Traçabilité des actions administrateur | Qui a consulté ou modifié quel dossier, et quand |

## 4. Obligations à préparer avant toute ouverture payante

- **Statut** : micro-entreprise créée, activité « assistance administrative » ; vérifier la compatibilité avec l'emploi salarié (clause d'exclusivité, loyauté).
- **Périmètre** : aide aux démarches et à la constitution de dossiers administratifs uniquement. Pas de consultation juridique ni de rédaction d'actes pour autrui (réservées aux professions réglementées). Orientation systématique vers avocat, notaire, expert-comptable, Point-justice, ADIL ou France Services quand c'est nécessaire.
- **Service à la personne (facultatif)** : la déclaration ouvre droit au crédit d'impôt de 50 % pour les clients, mais seulement pour l'assistance administrative réalisée **à domicile**.
- **Documents commerciaux** : mentions légales complètes (nom, adresse, numéro SIREN), conditions générales de vente, modèle de devis et de facture, information sur le droit de rétractation de 14 jours (et demande expresse d'exécution anticipée), coordonnées d'un **médiateur de la consommation** (obligatoire pour vendre aux particuliers).
- **Données personnelles (RGPD)** : politique de confidentialité, registre des traitements, durées de conservation (par exemple suppression du dossier 12 mois après la fin, sauf factures conservées 10 ans), contrats de sous-traitance avec l'hébergeur, le prestataire de paiement et le fournisseur d'IA, information sur les éventuels transferts hors Union européenne, procédure en cas de fuite de données.
- **Assurance** : responsabilité civile professionnelle recommandée.
- **Jamais** : demander des mots de passe (FranceConnect, CAF, impôts…), envoyer un dossier officiel sans l'accord explicite du client, promettre l'obtention d'une aide ou l'issue d'une démarche.

## 5. Prochaines étapes proposées

1. Romain et ChatGPT testent la démonstration et listent les améliorations.
2. Choix de l'hébergement et du prestataire de paiement, après création de la micro-entreprise.
3. Rédaction des CGV, de la politique de confidentialité et du modèle de devis.
4. Construction de la version serveur en environnement de test (paiements en mode test du prestataire).
5. Ouverture à quelques personnes de confiance avant tout lancement public.
