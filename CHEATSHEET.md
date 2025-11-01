# PyBar - Aide-Mémoire / Cheat Sheet

## Les 3 Commandes Essentielles / The 3 Essential Commands

### 1️⃣ Entraîner / Train
```bash
python train_model.py
```
⏱️ ~10-30 minutes | Crée/Creates `barcode_model.pth`

### 2️⃣ Construire / Build
```bash
python build_apk.py
```
⏱️ ~30-60 minutes (première fois/first time) | Crée/Creates `bin/*.apk`

### 3️⃣ Installer / Install
```bash
adb install bin/pybar-1.0-arm64-v8a-debug.apk
```
ou/or copier manuellement sur Android / manually copy to Android

---

## Installation Rapide / Quick Setup

```bash
# 1. Cloner / Clone
git clone https://github.com/Aguelord/PyBar.git
cd PyBar

# 2. Installer dépendances / Install dependencies
pip install -r requirements.txt

# 3. Suivre les 3 étapes ci-dessus / Follow 3 steps above
```

---

## Prérequis / Prerequisites

### Tous / All Platforms
- Python 3.8+
- Git

### Windows Seulement / Only
```powershell
# Installer WSL2 / Install WSL2
wsl --install
```

### Linux Seulement / Only
```bash
sudo apt-get install -y build-essential git zip unzip default-jdk \
    libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev
```

---

## Installation APK - Options / APK Install Options

### Option A: USB + ADB
```bash
adb install bin/pybar-*.apk
```

### Option B: Transfert Manuel / Manual Transfer
1. Copier APK sur téléphone / Copy APK to phone
2. Ouvrir fichier / Open file
3. Installer / Install

### Option C: Serveur Web Local / Local Web Server
```bash
python -m http.server 8000
# Puis aller à / Then go to: http://<your-ip>:8000/bin/
```

---

## Dépannage Rapide / Quick Troubleshooting

### Erreur "buildozer not found"
```bash
pip install buildozer
```

### Erreur "WSL not installed" (Windows)
```powershell
wsl --install
# Redémarrer / Reboot
```

### Erreur "Missing dependencies" (Linux)
```bash
sudo apt-get update
sudo apt-get install -y build-essential git zip unzip default-jdk
```

### APK ne s'installe pas / APK won't install
- Autoriser sources inconnues / Allow unknown sources
- Paramètres → Sécurité / Settings → Security

---

## Liens Utiles / Useful Links

- 📖 [SIMPLE_USAGE.md](SIMPLE_USAGE.md) - Guide complet / Complete guide
- 🇫🇷 [GUIDE_SIMPLE.md](GUIDE_SIMPLE.md) - Guide détaillé français
- 📚 [README.md](README.md) - Documentation technique
- 💻 [WINDOWS_BUILD_GUIDE.md](WINDOWS_BUILD_GUIDE.md) - Guide Windows

---

## Support

🐛 Issues: https://github.com/Aguelord/PyBar/issues

---

**Fait avec ❤️ / Made with ❤️**
