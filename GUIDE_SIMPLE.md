# PyBar - Guide Simple d'Utilisation

Ce guide explique comment utiliser PyBar en **3 étapes simples**.

## Configuration Initiale

1. **Cloner le dépôt**
```bash
git clone https://github.com/Aguelord/PyBar.git
cd PyBar
```

2. **Installer les dépendances Python**
```bash
pip install -r requirements.txt
```

## Les 3 Étapes Simples

### Étape 1 : Entraîner le Modèle

Lancez simplement le script Python pour entraîner le modèle de reconnaissance de code-barres :

```bash
python train_model.py
```

**Ce que fait ce script :**
- Génère 5000 images synthétiques de codes-barres pour l'entraînement
- Entraîne le réseau de neurones pendant 20 époques
- Sauvegarde le meilleur modèle dans `barcode_model.pth`
- Durée : environ 10-30 minutes (selon votre machine)

**Sortie attendue :**
```
Training on device: cpu
Epoch [1/20], Batch [0/156], Loss: 2.5432
...
Model saved to barcode_model.pth
Training completed!
```

### Étape 2 : Construire l'APK

Lancez le script Python pour construire l'application Android :

```bash
python build_apk.py
```

**Ce que fait ce script :**
- Vérifie que buildozer est installé (l'installe si nécessaire)
- Vérifie les dépendances système
- Construit l'APK Android
- Affiche l'emplacement de l'APK généré

**Note pour Windows :** Le script détectera automatiquement WSL et l'utilisera pour la compilation.

**Durée :** 
- Première fois : 30-60 minutes (télécharge Android SDK et NDK)
- Fois suivantes : 5-10 minutes

**Sortie attendue :**
```
==================================================
PyBar Android APK Builder
==================================================

Detected platform: Linux

✓ Buildozer is installed
✓ All required dependencies found

==================================================
Building APK
==================================================

...

==================================================
BUILD SUCCESSFUL!
==================================================

APK location: /path/to/PyBar/bin/pybar-1.0-arm64-v8a-debug.apk
```

### Étape 3 : Télécharger l'APK sur Android

Vous avez **3 options** pour installer l'APK sur votre appareil Android :

#### Option A : Via USB (ADB)

1. Activez le débogage USB sur votre Android :
   - Allez dans Paramètres → À propos du téléphone
   - Tapez 7 fois sur "Numéro de build"
   - Retournez et allez dans Options de développement
   - Activez "Débogage USB"

2. Connectez votre téléphone à votre ordinateur via USB

3. Installez l'APK :
```bash
adb install bin/*.apk
```

#### Option B : Transfert Manuel

1. Copiez le fichier APK (situé dans le dossier `bin/`) sur votre téléphone :
   - Via USB (copier le fichier dans le dossier Téléchargements)
   - Via email (envoyez-vous l'APK par email)
   - Via cloud (Google Drive, Dropbox, etc.)

2. Sur votre téléphone :
   - Ouvrez le gestionnaire de fichiers
   - Naviguez vers le dossier où se trouve l'APK
   - Tapez sur le fichier APK
   - Autorisez l'installation depuis des sources inconnues si demandé
   - Suivez les instructions d'installation

#### Option C : Via Serveur Web Local

1. Démarrez un serveur web dans le dossier PyBar :
```bash
python -m http.server 8000
```

2. Trouvez l'adresse IP de votre ordinateur :
```bash
# Linux/Mac
ifconfig | grep "inet "

# Windows
ipconfig
```

3. Sur votre Android :
   - Assurez-vous d'être sur le même réseau WiFi que votre ordinateur
   - Ouvrez le navigateur web
   - Allez à : `http://<IP-de-votre-ordinateur>:8000/bin/`
   - Téléchargez le fichier APK
   - Installez-le

**Exemple :**
Si votre IP est `192.168.1.100`, allez à : `http://192.168.1.100:8000/bin/`

## Utilisation de l'Application

Une fois l'APK installé sur votre Android :

1. **Ouvrez** l'application PyBar
2. **Autorisez** l'accès à la caméra quand demandé
3. **Pointez** la caméra vers un code-barres
4. **Appuyez** sur le bouton "Scan Barcode"
5. **Lisez** le numéro du code-barres affiché à l'écran

## Résumé des 3 Commandes

```bash
# 1. Entraîner le modèle
python train_model.py

# 2. Construire l'APK
python build_apk.py

# 3. Installer sur Android (option USB)
adb install bin/*.apk
```

C'est aussi simple que ça ! 🎉

## Dépendances Système (Linux uniquement)

Si vous êtes sur Linux et que `build_apk.py` signale des dépendances manquantes, installez-les :

```bash
sudo apt-get install -y \
    python3-pip \
    build-essential \
    git \
    zip \
    unzip \
    default-jdk \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev
```

## Support Windows

Sur Windows, `build_apk.py` utilisera automatiquement **WSL** (Windows Subsystem for Linux) pour construire l'APK.

**Si WSL n'est pas installé :**

1. Ouvrez PowerShell en tant qu'administrateur
2. Exécutez :
```powershell
wsl --install
```
3. Redémarrez votre ordinateur
4. Relancez `python build_apk.py`

## Problèmes Courants

### Le modèle ne détecte pas les codes-barres

**Solution :** Le modèle entraîné sur des données synthétiques n'est pas parfait. Pour améliorer :
- Entraînez avec plus de données réelles
- Assurez-vous que l'éclairage est bon
- Tenez le code-barres stable et net

### L'APK ne se construit pas

**Solution :**
1. Vérifiez les logs d'erreur
2. Assurez-vous d'avoir assez d'espace disque (environ 5 GB)
3. Vérifiez votre connexion internet
4. Sur Windows, assurez-vous que WSL est installé

### L'installation APK échoue sur Android

**Solution :**
1. Allez dans Paramètres → Sécurité
2. Activez "Sources inconnues" ou "Installer des applications inconnues"
3. Réessayez l'installation

## Pour Aller Plus Loin

- Consultez [README.md](README.md) pour plus de détails techniques
- Consultez [QUICKSTART.md](QUICKSTART.md) pour plus d'informations
- Consultez [WINDOWS_BUILD_GUIDE.md](WINDOWS_BUILD_GUIDE.md) pour les utilisateurs Windows

## Support

Pour toute question ou problème, ouvrez une issue sur GitHub :
https://github.com/Aguelord/PyBar/issues
