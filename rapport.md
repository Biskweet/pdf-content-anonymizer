# Rapport

Ce projet a pour but d'anonymiser les données sensibles d'un PDF en extrayant son contenu, en détectant les données sensibles et les écrasant avec un alias.

## Entrée
Un fichier PDF contenant du texte (pas de scan).

## Sortie
Le même fichier PDF duquel on aura caché les informations jugées sensibles

## Méthode
J'ai créé une interface web à l'aide de Flask pour pouvoir utiliser le script Python plus confortablement.

On peut entrer un seul fichier, ou plusieurs.

L'anonymiseur fonctionne en 4 étapes-clefs :
- Extraction du texte du PDF page par page ;
- Analyse du contenu textuel et reconnaissance des information sensibles (tâche sous-traitée par une API) ;
- Création et assignation d'alias pour marquer chaque élément de façon unique même s'il apparaît plusieurs fois dans le texte ;
- Écriture dans le document descriptif du PDF des alias après avoir supprimé les données sensibles ;
- Écriture du PDF sur le disque.

Le document est ainsi prêt à être renvoyés sur l'interface web pour répondre à la requête de l'utilisateur.
