# PyBar - Quick Start Guide

> **💻 Utilisateurs Windows / Windows Users:** Pour des instructions détaillées sur la compilation APK sous Windows, voir [WINDOWS_BUILD_GUIDE.md](WINDOWS_BUILD_GUIDE.md)

## Installation rapide

### 1. Cloner le dépôt
```bash
git clone https://github.com/Aguelord/PyBar.git
cd PyBar
```

### 2. Installation automatique

**Linux / macOS:**
```bash
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

**Ou installation manuelle:**
```bash
pip install -r requirements.txt
```

## Utilisation

### Test rapide
```bash
python demo.py
```

### Tests complets
```bash
python test_detector.py
```

### Entraîner le modèle
```bash
python train_model.py
```

### Construire l'APK Android

**Linux:**
```bash
./build_apk.sh
```

**Windows:**
```cmd
build_apk.bat
```

**Ou manuellement:**
```bash
buildozer android debug
```

## Architecture de l'application

### Structure du code
- `main.py` - Application Kivy principale avec interface caméra
- `barcode_detector.py` - Réseau de neurones PyTorch pour la détection
- `train_model.py` - Script d'entraînement du modèle
- `test_detector.py` - Tests unitaires
- `demo.py` - Démonstration rapide
- `buildozer.spec` - Configuration pour la compilation APK

### Comment ça marche

1. **Capture**: L'application capture une image via la caméra Android
2. **Prétraitement**: L'image est redimensionnée et normalisée
3. **Détection**: Le réseau de neurones PyTorch analyse l'image
   - Détecte la présence d'un code-barres
   - Prédit chaque chiffre (0-9)
4. **Décodage**: Les prédictions sont converties en numéro de code-barres
5. **Affichage**: Le numéro est affiché à l'utilisateur

### Réseau de neurones

Le modèle `BarcodeNet` utilise:
- **ResNet18** comme backbone (extraction de caractéristiques)
- **Tête de présence**: Classifieur binaire (code-barres présent/absent)
- **Têtes de chiffres**: 13 classifieurs (un par position de chiffre)
  - Chaque classifieur prédit 0-9 ou "pas de chiffre"

### Entraînement

Le script `train_model.py` génère des codes-barres synthétiques:
- Images avec barres verticales
- Texte avec le numéro
- Variations (rotation, bruit)

Pour utiliser de vraies images:
1. Collectez des photos de codes-barres
2. Modifiez la classe `SyntheticBarcodeDataset`
3. Relancez l'entraînement

## Compilation APK

### Prérequis
- Python 3.8+
- Git, Java, zip/unzip
- Espace disque: ~5GB pour SDK/NDK

**Important pour Windows:** Buildozer nécessite un environnement Linux pour compiler des APK Android.

### Sur Linux

#### Installation des dépendances système
```bash
sudo apt-get install -y \
    python3-pip \
    build-essential \
    git \
    ffmpeg \
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

#### Première compilation
```bash
pip install buildozer
./build_apk.sh
```

⚠️ La première compilation prend 30-60 minutes (téléchargement SDK/NDK)

### Sur Windows

**Méthode recommandée: WSL2 (Windows Subsystem for Linux)**

1. **Installer WSL2** (si pas déjà installé):
   ```powershell
   # Ouvrir PowerShell en tant qu'administrateur
   wsl --install
   # Redémarrer l'ordinateur après installation
   ```

2. **Vérifier l'installation WSL**:
   ```cmd
   wsl --version
   ```

3. **Installer les dépendances dans WSL**:
   ```cmd
   wsl
   # Dans WSL:
   sudo apt-get update
   sudo apt-get install -y python3-pip build-essential git \
       libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
       libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev
   ```

4. **Construire l'APK**:
   ```cmd
   # Dans Windows CMD ou PowerShell
   build_apk.bat
   ```

Le script détectera automatiquement WSL et l'utilisera pour la compilation.

**Alternative 1: Docker Desktop**

Si vous avez Docker Desktop installé sur Windows:

```cmd
# Télécharger l'image Ubuntu
docker pull ubuntu:22.04

# Lancer le conteneur avec le dossier du projet monté
docker run -v %CD%:/app -w /app -it ubuntu:22.04 bash

# Dans le conteneur:
apt-get update && apt-get install -y python3-pip git build-essential \
    libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev

pip3 install buildozer
./build_apk.sh
```

**Alternative 2: Machine virtuelle Linux**

Utiliser VirtualBox, VMware, ou Hyper-V avec Ubuntu 22.04 ou Debian 11.

**Alternative 3: Buildozer natif Windows (Support limité)**

⚠️ Le support natif de Buildozer sur Windows est limité et peut rencontrer des problèmes.

```cmd
pip install buildozer
buildozer android debug
```

**Note:** Cette méthode peut ne pas fonctionner correctement. WSL2 ou Docker sont fortement recommandés.

### Sur macOS

macOS nécessite également un environnement Linux pour compiler des APK Android:

- **Docker Desktop**: Utiliser la méthode Docker décrite ci-dessus
- **Machine virtuelle**: VirtualBox, Parallels, UTM avec Linux
- **Instance cloud**: AWS, GCP, Azure avec Ubuntu

### Installation sur appareil

Une fois l'APK construit:

```bash
adb install bin/pybar-1.0-arm64-v8a-debug.apk
```

Ou transférer l'APK sur votre appareil et l'installer manuellement.

## Utilisation de l'application

1. **Lancer** l'application sur Android
2. **Autoriser** l'accès à la caméra
3. **Pointer** la caméra vers un code-barres
4. **Appuyer** sur "Scan Barcode"
5. **Lire** le numéro affiché

## Formats de codes-barres supportés

Le modèle peut être entraîné pour:
- EAN-13 (13 chiffres)
- EAN-8 (8 chiffres)
- UPC-A (12 chiffres)
- Code-39
- Code-128

Par défaut, le modèle gère jusqu'à 13 chiffres.

## Amélioration de la précision

Pour améliorer la détection:

1. **Collectez plus de données**
   - Photos réelles de codes-barres
   - Différents angles et éclairages
   - Différents types de codes-barres

2. **Augmentation de données**
   - Rotation, flou, bruit
   - Variations d'éclairage
   - Déformations

3. **Ajustez l'architecture**
   - Plus de couches
   - Modèle plus grand (ResNet50)
   - Fine-tuning

4. **Entraînement plus long**
   - Plus d'époques
   - Plus d'exemples
   - Meilleur taux d'apprentissage

## Dépannage

### Problèmes courants

**La caméra ne fonctionne pas**
- Vérifier les permissions dans les paramètres Android
- Redémarrer l'application
- Vérifier qu'aucune autre app n'utilise la caméra

**Le modèle ne détecte rien**
- S'assurer que le modèle est entraîné
- Améliorer l'éclairage
- Tenir le code-barres stable et net
- Entraîner avec plus de données

**L'APK ne se construit pas**
- Vérifier les dépendances système
- Consulter les logs buildozer
- Augmenter l'espace disque
- Essayer avec buildozer clean
- **Windows:** Vérifier que WSL2 est correctement installé
- **Windows:** S'assurer que les dépendances Linux sont installées dans WSL

**Erreurs WSL sur Windows**
- Vérifier que WSL2 est installé: `wsl --version`
- Mettre à jour WSL: `wsl --update`
- Réinstaller la distribution: `wsl --install -d Ubuntu-22.04`
- Vérifier l'intégration Docker-WSL si vous utilisez Docker

**Erreur Docker sur Windows**
- Activer l'intégration WSL2 dans Docker Desktop
- Augmenter la RAM allouée à Docker (Paramètres > Resources)
- Vérifier que la virtualisation est activée dans le BIOS

**Erreur "module not found"**
- Réinstaller les dépendances
- Vérifier la version Python
- Activer l'environnement virtuel

## Performance

### Modèle
- Taille: ~50 MB
- Inférence: ~100-200 ms par image (CPU)
- RAM: ~500 MB

### Optimisations possibles
- Quantification du modèle
- Pruning (élagage)
- Conversion TorchScript/ONNX
- GPU mobile (si disponible)

## Prochaines étapes

- [ ] Support des QR codes
- [ ] Scan continu en temps réel
- [ ] Base de données des codes scannés
- [ ] Export CSV/JSON
- [ ] Mode hors ligne
- [ ] Support multilingue

## Ressources

- [Documentation PyTorch](https://pytorch.org/docs/)
- [Documentation Kivy](https://kivy.org/doc/stable/)
- [Documentation Buildozer](https://buildozer.readthedocs.io/)
- [Guide ResNet](https://pytorch.org/vision/stable/models.html)

## Contribution

Les contributions sont bienvenues! Pour contribuer:
1. Fork le projet
2. Créez une branche (`git checkout -b feature/amelioration`)
3. Committez vos changements
4. Push vers la branche
5. Ouvrez une Pull Request

## License

MIT License - voir le fichier LICENSE

## Contact

Pour questions ou problèmes, ouvrir une issue sur GitHub.
