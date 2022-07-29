# Rapport

## Description du projet
Le projet vise à automatiser l'anonymisation de données sensibles de documents PDF en remplaçant chaque valeur par un identifiant unique à elle-même.

Le projet se déroule en 3 étapes-clefs :
- Lecture d'un fichier PDF et récupération de son contenu textuel, puis envoi des données extraites à une API (hypothétique) qui répondra avec les données sensibles ;
- Attribution d'un alias d'anonymisation pour chaque donnée en fonction de sa valeur (les données sensibles identiques auront le même d'anonymisation) ;
- Réécriture sur le fichier PDF avec les alias anonymisants à la place des données sensibles pour anonymiser le document.

## Entrée attendue
Documents PDF avec des données sensibles (noms, adresses, codes bancaires, numéros de téléphone, etc.)

## Sortie attendue
Document PDF anonymisé, c'est-à-dire en tous points identique à l'exception des données sensibles qui auront été remplacées par un alias anonyme et unique.

## Méthode
Il existe deux manière d'effectuer cette tâche dans le cadre du projet :

**1 :** Utilisation d'une bibliothèque type `PyPDF2` ou `pdfrw` qui permettra de lire le fichier PDF et d'écrire un nouveau fichier identique en remplaçant le texte sensible par des alias.

​    <u>**Avantages :**</u>

- **Accomplit la tâche exactement comme demandé.**

​    <u>**Inconvénients :**</u>

- **Ne fonctionne pas sur certains fichiers PDF pour des raisons obscures** ;
- Certains PDF sont mal "lus" par les bibliothèques et leur texte est corrompu (t r o p  d ' e s p a c e s  ou pasassez ou a léatoi remn t).

**2 :** de `tesseract` pour l'identification de chaque mot du document et sa position, puis anonymisation des données sensibles avec `opencv` en réécrivant au-dessus.

​    <u>**Avantages :**</u>

- Détection des zones de texte au pixel près ;
- Plus grande liberté quant au choix de l'alias (texte, code couleur, etc) ;
- **Détection du texte même quand il n'est pas vectoriel** (ex : document numérisé).

​    <u>**Inconvénients :**</u>

- Le fichier de sortie après anonymisation est une image. Il sera possible de convertir l'image en PDF mais elle restera alors une image sur un PDF (cependant, avec une résolution suffisante, la seule fonctionnalité perdue serait la sélection de texte) ;
- Il peut y avoir des erreurs dans l'interprétation du texte par `tesseract`. **Néanmoins, après quelques expérimentations, la retranscription semble être plus fidèle avec `tesseract` comparée à `PyPDF2`**.

