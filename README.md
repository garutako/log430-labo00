# Labo 00 – Infrastructure (Git, Docker, CI/CD)

<img src="https://upload.wikimedia.org/wikipedia/commons/2/2a/Ets_quebec_logo.png" width="250">    
ÉTS - LOG430 - Architecture logicielle - Chargé de laboratoire: Gabriel C. Ullmann.

## 🎯 Objectifs d'apprentissage

- Apprendre à créer un projet **Python** conteneurisé avec **Docker** à partir de zéro.
- Apprendre à écrire et exécuter des tests automatisés avec **pytest**.
- Mettre en place un pipeline **CI/CD** avec les ressources à notre disposition.
- Apprendre à publier une **image de conteneur** dans un registre (GitHub Container Registry), première étape de tout déploiement.

---

## ⚙️ Setup  

Dans ce laboratoire, vous travaillerez sur une application calculatrice. Cette calculatrice est volontairement très simple afin que nous puissions nous concentrer sur la configuration et la structure du projet, ainsi que sur la création d'un pipeline CI/CD.

Vous allez créer la structure du projet vous-même à partir de zéro, en créant le `requirements.txt`, `Dockerfile`, `docker-compose.yml` et `.env`. Chaque activité vous guidera dans une étape de setup, puis l'implémentation. Il est très important de réaliser ce laboratoire car :

- Les concepts que vous apprendrez ici (ex. le setup Python et Docker, les approches de test et déploiement, etc.) vous aideront à mieux comprendre **TOUS** les laboratoires suivants.
- Les concepts architecturaux et les pratiques de développement que vous apprenez ici peuvent être appliqués au projet, **dans n'importe quel langage de programmation ou framework**.

Dans les prochains laboratoires, nous verrons des architectures plus complexes et nous travaillerons avec une variété d'outils logiciels et de concepts architecturaux.

> ⚠️ **ATTENTION** : Si vous ne l'avez pas déjà fait, nous vous recommandons d'installer **VS Code**, **Python 3+**, **Docker Desktop** et **MySQL Workbench** avant de commencer.

> ⚠️ **IMPORTANT** : Avant de commencer le setup et les activités, veuillez lire la documentation architecturale dans le répertoire `/docs/arc42/docs.pdf` pour comprendre quel type d'application nous serons en train de développer.

### 1. Clonez le dépôt

```bash
git clone < lien à votre dépôt GitHub >
cd log430-labo0
```

### 2. Créez votre fichier requirements.txt

Le fichier `requirements.txt` contient la liste des dépendances Python que vous avez besoin pour exécuter votre projet et qui seront installées via [pip](https://www.w3schools.com/python/python_pip.asp) dans votre environnement. Vous aurez besoin d'une seule dépendance pour ce projet : `pytest` (pour exécuter les tests unitaires). Créez un fichier `requirements.txt` dans le répertoire racine de votre projet :

```sh
pytest>=7.0
```

### 3. Créez votre Dockerfile

Un fichier `Dockerfile` est une recette permettant de créer une image de conteneur Docker. Un conteneur est une machine virtuelle simplifiée qui s'exécutera dans votre environnement de développement local, mais qui peut également s'exécuter dans un environnement de production si vous le souhaitez. Créez un fichier `Dockerfile` dans le répertoire racine de votre projet :

```sh
FROM python:3.11-slim
WORKDIR /app
COPY src/ ./src/
COPY requirements.txt ./
ENV PYTHONPATH=/app/src
RUN pip install --no-cache-dir -r requirements.txt
```

### 4. Créez votre docker-compose.yml

Un fichier `docker-compose.yml` décrit quels conteneurs (également appelés services) seront créés en utilisant votre image de conteneur Docker comme base. Dans notre cas, nous voulons uniquement exécuter notre calculatrice. Créez un fichier `docker-compose.yml` dans le répertoire racine de votre projet :

```yml
services:
  calculator:
    build: .
    volumes:
      - .:/app
    stdin_open: true
    tty: true
```

### 5. Créez votre .env

Un fichier `.env` est utilisé pour garder les variables d'une application qui sont distinctes pour chaque instance et que nous ne voulons pas écrire dans le code pour des raisons de sécurité et de flexibilité. Par exemple, une application de gestion de magasin aura une base de données différente pour chaque magasin, avec un nom d'utilisateur et un mot de passe également distincts et qui ne doivent pas être partagés dans le code. Ici, dans ce très simple cas, nous garderons simplement le nom de l'utilisateur de la calculatrice. Créez un fichier `.env` dans le répertoire racine de votre projet avec une seule ligne :

```sh
CALCULATOR_USERNAME=YourName
```

Une fois le fichier `.env` créé et la variable définie, l'application dans `/src/calculator.py` est déjà préparée pour lire le `.env`, extraire la variable `CALCULATOR_USERNAME` et l'utiliser. Si vous faites votre propre application à partir de zéro, vous devriez écrire vous-même le code pour lire le `.env`, ou utiliser une librairie telle que [dotenv](https://www.geeksforgeeks.org/python/using-python-environment-variables-with-python-dotenv/) pour vous aider.

### 6. Démarrez le conteneur

Dans le terminal, exécutez :

```sh
docker compose build
docker compose up -d
```

Ensuite, cliquez sur votre conteneur dans la liste dans Docker Desktop, sélectionnez l'onglet `Exec` et exécutez :

```sh
python src/calculator.py
```

> 📝 **NOTE** : l'autocomplétion en appuyant sur Tab et les flèches du clavier ne marchent pas dans Docker Desktop, parce qu'il utilise une interface Bash simplifiée. Si vous n'aimez pas cela, vous pouvez également exécuter les commandes via [docker exec](https://docs.docker.com/reference/cli/docker/container/exec/) à partir de votre machine hôte (hors Docker).

---

## 🧪 Activités

### 1. Écrivez les tests

Dans le fichier `test_calculator.py`, écrivez des tests pour les fonctions définies dans `calculator.py`.

```python
def test_addition():
    assert addition(2, 3) == 5
```

Pour lancer les tests :

```bash
pytest
```

> 💡 **Question 1** : Si l'un des tests échoue à cause d'un bug, comment pytest signale-t-il l'erreur et aide-t-il à la localiser ? Rédigez un test qui provoque volontairement une erreur, puis montrez la sortie du terminal obtenue.

### 2. Vérifier les étapes à la pipeline CI (Intégration Continue)

Le fichier `.github/workflows/.github-ci.yml` est déjà préparé pour que GitHub exécute les tests automatiquement à chaque push. Veuillez lire le fichier pour vous familiarizer avec les étapes (steps).

> ⚠️ **IMPORTANT** : Il n'est pas recommandé d'écrire les noms d'utilisateur et les mots de passe en « plain text » dans un fichier tel que `.github/workflows/.github-ci.yml`. Veuillez utiliser les [secrets](https://docs.github.com/fr/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets) dans un [environnement GitHub](https://docs.github.com/fr/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments#creating-an-environment) **si vous avez besoin** de gérer des informations d'authentification.

### 3. Versionnez votre code

Si tous les tests passent :

```bash
git add .
git commit -m "Tests pour calculator.py"
git push
```

GitHub exécutera les tests sur son serveur, et ils devront passer également s'ils sont corrects.

> 💡 **Question 2** : Que fait GitHub pendant les étapes de « setup » et « checkout » ? Veuillez inclure la sortie du terminal GitHub CI dans votre réponse.

### 4. Réfléchissez à comment livrer votre code en production

Livrer en production signifie rendre votre application exécutable en dehors de votre environnement de développement. Cette cible pourrait être, par exemple :

- Un serveur physique dans une entreprise/école
- Un serveur en nuage (ex. Azure, AWS, etc.)
- Une grappe Kubernetes

Peu importe la cible, la première étape est toujours la même : **publier une image de conteneur** dans un registre accessible depuis l'extérieur de votre poste. C'est cette image, et non votre code source, qui sera déployée.

Dans ce laboratoire, nous publierons notre image dans le [GitHub Container Registry (GHCR)](https://docs.github.com/fr/packages/working-with-a-github-packages-registry/working-with-the-container-registry), qui est intégré à votre dépôt et gratuit pour les dépôts publics. Plus tard dans le cours (Labo 05), c'est précisément une image publiée de cette façon que vous déploierez sur une grappe Kubernetes.

### 5. Publiez votre image manuellement

Avant d'automatiser quoi que ce soit, faites-le une fois à la main pour comprendre chaque étape.

D'abord, créez un [Personal Access Token **classic**](https://github.com/settings/tokens) avec la portée `write:packages`. Un jeton *fine-grained* ne fonctionne pas correctement avec GHCR. Puis, connectez-vous au registre :

```bash
echo <VOTRE_TOKEN> | docker login ghcr.io -u <VOTRE_USERNAME_GITHUB> --password-stdin
```

Construisez votre image en la nommant selon la convention du registre (le nom doit être **en minuscules**) :

```bash
docker build -t ghcr.io/<votre-username>/<nom-de-votre-depot>:latest .
```

Publiez-la :

```bash
docker push ghcr.io/<votre-username>/<nom-de-votre-depot>:latest
```

Votre image devrait maintenant apparaître dans l'onglet « Packages » de votre profil GitHub.

Pour valider que l'image est réellement utilisable, supprimez votre copie locale et récupérez celle du registre :

```bash
docker rmi ghcr.io/<votre-username>/<nom-de-votre-depot>:latest
docker run -it --rm ghcr.io/<votre-username>/<nom-de-votre-depot>:latest python src/calculator.py
```

> ⚠️ **IMPORTANT** : Utilisez exactement le **nom de votre dépôt** dans le nom de l'image. L'activité 6 publiera au même endroit (`ghcr.io/OWNER/DEPOT`), et les deux étapes alimenteront ainsi le même paquet plutôt que deux paquets distincts.

> 📝 **Si l'activité 6 échoue avec `denied: permission_denied`** : votre paquet a été créé manuellement et n'est pas encore rattaché au dépôt. Allez dans « Packages » → votre image → « Package settings » → « Manage Actions access » → ajoutez votre dépôt avec le rôle **Write**.

> 📝 **NOTE** : Par défaut, une image publiée est privée. Pour la rendre publique, allez dans « Packages » → votre image → « Package settings » → « Change visibility ».

Pendant que votre conteneur s'exécute, observez les ressources qu'il consomme. Depuis votre ordinateur :

```bash
docker stats
```

Et depuis l'intérieur du conteneur :

```bash
docker compose exec calculator top
```

> 💡 **Question 3** : Quel type d'informations pouvez-vous obtenir via les commandes `docker stats` et `top` ? Veuillez donner quelques exemples et expliquer la différence entre ce que chacune vous montre. Veuillez inclure la sortie du terminal dans votre réponse.

### 6. Automatisez la publication (CD)

Maintenant que vous savez publier manuellement, automatisez-le. Créez un fichier `.github/workflows/cd.yml` qui construit et publie l'image à chaque `push` sur la branche principale.

Notez que vous n'avez **pas** besoin de créer un secret pour vous authentifier : GitHub fournit automatiquement un `GITHUB_TOKEN` à chaque exécution de workflow. Il suffit de lui accorder la permission d'écrire dans les packages.

```yml
name: CD

on:
  push:
    branches: [ main ]

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout dépôt
        uses: actions/checkout@v4

      - name: Authentification à GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Construire et publier l'image
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:latest
```

> ⚠️ **IMPORTANT** : Le bloc `permissions` est obligatoire. Sans `packages: write`, la publication échouera avec une erreur `denied: permission_denied`.

**Résultat attendu** : à chaque fois que vous faites `push` sur `main`, GitHub construit votre image et publie automatiquement une nouvelle version dans le registre, prête à être déployée sur n'importe quelle cible.
---

## 📦 Livrables

> ⚠️ **La remise se fait au niveau de la PHASE, pas du labo.** Les Labos 00, 01, 02 et 03 forment la **Phase 1**, remise en une seule fois dans un espace Moodle unique, à la fin de la phase.

Vous déposerez **exactement deux fichiers** dans Moodle, pour toute la Phase 1 :

| # | Fichier | Contenu |
|---|---|---|
| 1 | `LOG430-A26-Phase1-EquipeNN.zip` | Le code source des **4 labos**, un dossier par labo (`labo00/`, `labo01/`, `labo02/`, `labo03/`), incluant le fichier `.mwb` du Labo 03 |
| 2 | `LOG430-A26-Phase1-EquipeNN.pdf` | Un **rapport unique** en 4 sections, une par labo |

> ⚠️ Le rapport PDF doit être déposé **comme fichier séparé**, et non à l'intérieur du zip.

Ce que **ce labo** doit contenir dans la remise :

- Son code source complet, dans le dossier `labo00/` du zip.
- La section correspondante du rapport, répondant aux **3 questions** de ce fichier. Il est **obligatoire** d'illustrer chaque réponse avec du code ou une sortie de terminal.

Vous avez des questions sur le format de soumission ? [Voici un exemple](https://drive.google.com/file/d/12ss6zSayGCjHCydf9fRJ3wvqsOQNMBa9/view?usp=sharing). Veuillez respecter cette même structure de dossiers pour **toutes** vos soumissions de laboratoire. Cela nous permet de corriger vos laboratoires plus rapidement et plus correctement.
