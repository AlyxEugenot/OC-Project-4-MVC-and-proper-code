# OC-Project-4-MVC-and-proper-code - Bienvenue.

Ce code est un exercice de MVC dans mon cursus de Python d'OpenClassroom
dédié à faire une application de tournoi d'échecs avec un code propre qui respecte la PEP8 dont
[ce lien flake8](https://rawcdn.githack.com/AlyxEugenot/OC-Project-4-MVC-and-proper-code/main/flake-report/index.html) en atteste la qualité.

### Pour lancer ce projet :

Vous pouvez dans un premier temps télécharger le projet et extraire son zip à l'emplacement de
votre choix.<br>
Copiez son chemin une fois extrait.

Puis, si vous avez Python3 déjà installé :  
Dans un terminal de commandes tel que Bash ou l'invite de commandes cmd.  
Pour vous rendre dans le dossier du projet, vous pouvez y écrire :

```
Sous Bash : cd chemin/du/dossier (ou cd ctrl+shift+inser)
Sous cmd : cd chemin\du\dossier (ou cd ctrl+v)
```

---

Pour y initialiser un environnement virtuel appelé ici `.venv`, écrivez :

```
python -m venv .venv
```

Puis, vous l'activez grâce à  
**sous cmd** :

```
.venv\scripts\activate
```

**sous Bash** :

```
source .venv/scripts/activate
```

---

Maintenant que vous avez activé l'environnement virtuel :  
Pour installer les dépendances, écrire dans la console

```
pip install -r requirements.txt
```

---

Enfin, pour lancer le programme, vous pouvez lancer :

**sous cmd** :

```
python src\chess_tournament_app.py
```

**sous Bash** :

```
python src/chess_tournament_app.py
```

---

---

## Si vous désirez générer un nouveau rapport flake8 :

Toujours dans l'environnement virtuel, installez flake-html en écrivant

```
pip install flake8-html
```

puis générez le nouveau rapport avec

```
flake8 --exclude=.venv --format=html --htmldir=flake-report
```
