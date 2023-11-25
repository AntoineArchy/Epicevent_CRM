# Présentation
L'objectif de cet exercice est de mettre en place un CRM permettant à des utilisateurs de créer des clients, de définir les contrats et événements associés à ces clients, ainsi qu'aux administrateurs d'ajouter des comptes utilisateurs.  
Toutes les entités de l'application (collaborateurs, clients, contrats et événements) doivent être sauvegardées en base de données, les autorisations de création et de mise à jour de ces entités suivent des règles dictées dans le cahier des charges.   
Pour une visualisation côte à côte du cahier des charges et des extraits de code correspondant, voir "Design/analyse_cahier_des_charges.pdf".  
Cette application est développée en utilisant Python et MySQL.

# Prérequis
Pour mettre en place cette application, l'hôte doit impérativement avoir un serveur [MySQL](https://www.mysql.com/) déjà configuré.   
Pour permettre la mise en place de l'application, l'administrateur doit disposer d'un compte ayant les droits administrateurs sur le serveur MySQL.  
Pour permettre l'utilisation de l'application, l'utilisateur final devra avoir un compte configuré par l'un des administrateurs (membre "Gestion") depuis l'application.

Avant la première utilisation, un administrateur système doit impérativement exécuter le script 'setup.py' (voir 'Mise en place').

# Fonctionnalités
Depuis l'application, il est possible pour un utilisateur de :
- Se connecter à un compte collaborateur de manière sécurisée.
- Visualiser en lecture seule les principales entités de l'application.
- Créer et mettre à jour des entités (en fonction des autorisations accordées à l'utilisateur).
- Utiliser des filtres d'affichage particuliers en fonction du rôle du collaborateur.
- Chaque opération d'ajout ou de mise à jour à la base de données requiert une nouvelle authentification de l'utilisateur.
- L'intégration d'un lien Sentry au module de logging afin d'avoir un accès direct au suivi de l'application (optionnel).
- Un logging détaillé des opérations des utilisateurs.

# Fonctionnement général

La boucle principale de l'application repose sur trois classes :

Le contexte (Context): Le contexte est garant de l'état actuel de l'application, la connexion, l'utilisateur, l'identification de la vue actuellement affichée.  
Le contrôleur principal (EpicEventController): Le contrôleur principal, un pool de contrôleurs, dispatche les différentes fonctions aux contrôleurs secondaires de l'application et maintient à jour le menu de l'application.  
Le display (RichQuestionaryCliDisplay): Le display affiche les informations de la vue actuelle, le menu des options transmises par le contrôleur principal et récupère le choix de l'utilisateur avant de le retourner au contrôleur principal.

# Fonctionnement interne

Chaque table de la base de données est associée à un modèle (model.py) dont les champs coïncident avec cette table (entité).  
En fonction des autorisations (authorization.py) associées au rôle (roles.py) du collaborateur connecté, différentes vues (views.py) sont disponibles pour l'utilisateur (correspondant aux différentes opérations CRUD).  
En cas de création ou de mise à jour d'entité, l'utilisateur interagit avec un formulaire (form.py).  
Les informations de ce formulaire sont alors sérialisées (serializer.py) et sanitiser avant interaction avec la base de données.  
Les interactions entre ces différents modules passent par le contrôleur correspondant à l'entité, qui met à disposition les vues et le menu utilisateur adapté au contexte de l'application.  

# Mise en place

### Récupération du dépot 
- Téléchargez le contenu de ce dépot via le bouton dédié ou, dans un terminal : $ git clone https://github.com/AntoineArchy/Epicevent_CRM.git

### Création de l'environnement virtuel
Ouvrez un terminal; 

- Pour ouvrir un terminal sur Windows, pressez les touches windows + r et entrez cmd.
- Sur Mac, pressez les touches command + espace et entrez "terminal".
- Sur Linux, vous pouvez ouvrir un terminal en pressant les touches Ctrl + Alt + T.

Placez-vous dans le dossier où vous souhaitez créer l'environnement (Pour plus de facilité aux étapes suivantes, il est recommandé de faire cette opération dans le dossier contenant le script à exécuter). Puis exécutez à présent la commande : 

`python -m venv env
`

Une fois fait, un nouveau dossier "env" devrait être créé dans le répertoire, il s'agit de votre environnement virtuel.


### Activation de l'environnement virtuel
Une fois la première étape réalisée, vous pouvez à présent activer votre environnement.

Pour ce faire, dans le dossier où l'environnement a été créé :


Ouvrez un terminal, rendez-vous au chemin d'installation de votre environnement puis exécutez la commande : 

- Windows (Cmd) : `env\Scripts\activate.bat`
- bash/zsh : `source venv/bin/activate`
- fish : `source venv/bin/activate.fish`
- csh/tcsh : `source venv/bin/activate.csh`
- PowerShell : `venv/bin/Activate.ps1`

Une fois fait, vous constatez que les lignes de votre cmd commencent à présent par "(env)", cela signifie que votre environnement est actif.

### Installation des dépendances
Dans le même terminal qu'à l'étape précédente :

`pip install -r requirements.txt`


### Execution 
Lors du premier lancement, il est important de suivre les étapes l'une après l'autre. Lors des exécutions suivantes, il est possible de réutiliser l'environnement créé précédemment. Pour ce faire, ne suivez que l'étape 2 (Activer l'environnement virtuel), vous pouvez alors simplement contrôler que les dépendances sont bien installées via la commande : `pip freeze`. Si toutes les dépendances sont bien présentes, il est possible de passer directement à l'exécution du script.


# Mise en place par les Administrateurs
Lors de la mise en place et avant la distribution aux utilisateurs, il est essentiel qu'un utilisateur ayant les droits d'administration sur le serveur MySQL mette en place l'application.

Pour ce faire :

Exécutez le script 'setup.py' présent à la racine du projet.  
Choisissez l'installation : 'setup'.

Le système va alors vous accompagner dans la mise en place du fichier de configuration, où vous pourrez :

Mettre en place l'hôte par défaut pour l'application.  
Ajouter votre Salt existant pour la gestion des mots de passe ou en générer un nouveau.  
Ajouter le lien Sentry pour le suivi des erreurs et la récupération des logs utilisateurs.  

Une fois fait, les différentes requêtes permettant la création des éléments nécessaires au bon fonctionnement de l'application seront exécutées.   
Ces requêtes sont consultables dans le dossier SQL de l'application.

Les requêtes exécutées avec succès, vous serez alors invité à créer le premier utilisateur au rôle "Gestion" du système et commencer l'utilisation normale de l'application.  
Il est possible de transmettre une version de l'installation ne comportant pas le dossier SQL et le fichier setup.py aux utilisateurs finaux de l'application.
### Note
Il est également possible d'executer le fichier 'setup.py' et de sélectionner 'uninstall' pour proceder à la désinstallation de l'application sur le système.  
Il vous sera demandé une connection administrateur, le choix de faire un dump de la base avant désinstallation vous sera également proposé.  

# Utilisation par les collaborateurs 
Pour accéder au menu principal de l'application, exécutez : 'python3 main_menu.py'.  
Il vous faudra alors vous connecter avec les identifiants transmis par un administrateur pour commencer à utiliser l'application.
### Navigation
La navigation dans les menus se fait via les flèches directionnelles du clavier, la sélection de l'option actuellement active dans le menu se fait avec la touche 'entrée'.  
Lors de la sélection multiple (sélectionner les champs à éditer sur un formulaire par exemple), naviguez avec les flèches, effectuez la sélection ou la désélection avec la touche 'espace' puis validez vos choix avec la touche 'entrée'.  
Il est normal que lorsque vous renseignez votre mot de passe, aucun caractère ne soit visible à l'écran.

# Rapports
Il est possible de généré un rapport pytest en utilisant la commande 'pytest'  
Une fois fait, un rapport coverage sera disponible dans le repertoire 'reports/'  
Un rapport pytest s'affichera également dans le terminal après execution. 
