# PyBar - Utilisation Simple / Simple Usage

[Version Française](#version-française) | [English Version](#english-version)

---

## Version Française

### Les 3 Étapes Simples pour Utiliser PyBar

PyBar est maintenant ultra-simple à utiliser ! Il suffit de suivre ces 3 étapes :

#### 🎓 Étape 1 : Entraîner le Modèle

```bash
python train_model.py
```

Ce script entraîne le réseau de neurones qui reconnaît les codes-barres.
- Durée : ~10-30 minutes
- Génère automatiquement des données d'entraînement
- Sauvegarde le modèle dans `barcode_model.pth`

#### 📦 Étape 2 : Construire l'APK

```bash
python build_apk.py
```

Ce script construit l'application Android (fichier .apk).
- Durée : ~30-60 minutes (première fois)
- Le script détecte automatiquement votre système d'exploitation
- Sur Windows, utilise automatiquement WSL si disponible
- L'APK est créé dans le dossier `bin/`

#### 📱 Étape 3 : Installer sur Android

**Option Simple - Via USB :**
```bash
adb install bin/*.apk
```

**Option Alternative - Transfert Manuel :**
1. Copiez le fichier APK (dans `bin/`) sur votre téléphone (USB, email, ou cloud)
2. Ouvrez le fichier APK sur votre téléphone
3. Autorisez l'installation et suivez les instructions

**Option Alternative - Via WiFi :**
```bash
python -m http.server 8000
```
Puis sur votre téléphone, allez à : `http://<IP-de-votre-PC>:8000/bin/`

### C'est Tout ! 🎉

Votre application PyBar est maintenant installée sur votre Android et prête à scanner des codes-barres !

### Documentation Détaillée

Pour plus d'informations, consultez :
- [GUIDE_SIMPLE.md](GUIDE_SIMPLE.md) - Guide détaillé en français
- [README.md](README.md) - Documentation technique complète
- [WINDOWS_BUILD_GUIDE.md](WINDOWS_BUILD_GUIDE.md) - Guide spécifique Windows (en anglais)

---

## English Version

### 3 Simple Steps to Use PyBar

PyBar is now super easy to use! Just follow these 3 steps:

#### 🎓 Step 1: Train the Model

```bash
python train_model.py
```

This script trains the neural network that recognizes barcodes.
- Duration: ~10-30 minutes
- Automatically generates training data
- Saves the model to `barcode_model.pth`

#### 📦 Step 2: Build the APK

```bash
python build_apk.py
```

This script builds the Android application (.apk file).
- Duration: ~30-60 minutes (first time)
- Automatically detects your operating system
- On Windows, automatically uses WSL if available
- The APK is created in the `bin/` folder

#### 📱 Step 3: Install on Android

**Simple Option - Via USB:**
```bash
adb install bin/*.apk
```

**Alternative Option - Manual Transfer:**
1. Copy the APK file (in `bin/`) to your phone (USB, email, or cloud)
2. Open the APK file on your phone
3. Allow installation and follow the prompts

**Alternative Option - Via WiFi:**
```bash
python -m http.server 8000
```
Then on your phone, go to: `http://<your-PC-IP>:8000/bin/`

### That's It! 🎉

Your PyBar app is now installed on your Android device and ready to scan barcodes!

### Detailed Documentation

For more information, see:
- [GUIDE_SIMPLE.md](GUIDE_SIMPLE.md) - Detailed guide in French
- [README.md](README.md) - Complete technical documentation
- [WINDOWS_BUILD_GUIDE.md](WINDOWS_BUILD_GUIDE.md) - Windows-specific guide

---

## Requirements / Prérequis

### All Platforms / Toutes Plateformes
- Python 3.8+
- Git

### Windows Only / Windows Seulement
- WSL2 (Windows Subsystem for Linux)
  ```powershell
  wsl --install
  ```

### Linux Only / Linux Seulement
```bash
sudo apt-get install -y build-essential git zip unzip default-jdk \
    libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
```

---

## Quick Start / Démarrage Rapide

```bash
# Clone the repository / Cloner le dépôt
git clone https://github.com/Aguelord/PyBar.git
cd PyBar

# Install Python dependencies / Installer les dépendances Python
pip install -r requirements.txt

# 1. Train model / Entraîner le modèle
python train_model.py

# 2. Build APK / Construire l'APK
python build_apk.py

# 3. Install on Android / Installer sur Android
adb install bin/*.apk
```

---

## Support

For questions or issues / Pour questions ou problèmes :
- GitHub Issues: https://github.com/Aguelord/PyBar/issues
- Documentation: [README.md](README.md)
