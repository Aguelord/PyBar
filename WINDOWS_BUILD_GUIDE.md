# Guide de construction APK pour Windows / Windows APK Build Guide

Ce guide détaille comment construire l'APK Android de PyBar sur Windows.

*This guide explains how to build the PyBar Android APK on Windows.*

---

## 🇫🇷 Version Française

### Vue d'ensemble

Buildozer, l'outil de compilation pour Android, nécessite un environnement Linux. Sur Windows, vous avez trois options:

1. **WSL2 (Recommandé)** - Windows Subsystem for Linux
2. **Docker Desktop** - Conteneur Linux
3. **Machine Virtuelle** - VirtualBox, VMware, Hyper-V

### Option 1: WSL2 (Recommandé) ⭐

C'est la méthode la plus simple et la plus performante pour Windows 10/11.

#### Étape 1: Installer WSL2

**Prérequis:**
- Windows 10 version 2004+ (Build 19041+) ou Windows 11
- Droits administrateur

**Installation:**

1. Ouvrir PowerShell en tant qu'administrateur
2. Exécuter:
   ```powershell
   wsl --install
   ```
3. Redémarrer l'ordinateur
4. Au premier lancement, créer un nom d'utilisateur et mot de passe Linux

**Vérification:**
```cmd
wsl --version
wsl --list --verbose
```

Vous devriez voir une distribution Ubuntu listée.

#### Étape 2: Configurer l'environnement WSL

Ouvrir WSL (taper `wsl` dans CMD ou chercher "Ubuntu" dans le menu Démarrer):

```bash
# Mettre à jour les packages
sudo apt-get update
sudo apt-get upgrade -y

# Installer les dépendances Python
sudo apt-get install -y python3 python3-pip python3-venv

# Installer les dépendances pour Buildozer
sudo apt-get install -y \
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
    zlib1g-dev \
    openjdk-11-jdk \
    zip \
    unzip

# Installer Buildozer
pip3 install buildozer cython
```

#### Étape 3: Accéder au projet depuis WSL

Vos fichiers Windows sont accessibles depuis WSL dans `/mnt/`:

```bash
# Exemple: Si votre projet est dans C:\Users\VotreNom\PyBar
cd /mnt/c/Users/VotreNom/PyBar

# Vérifier que les fichiers sont présents
ls -la
```

**⚠️ Important:** Travaillez toujours depuis `/mnt/c/...` pour accéder à vos fichiers Windows.

#### Étape 4: Construire l'APK

**Depuis Windows CMD/PowerShell:**
```cmd
cd C:\Users\VotreNom\PyBar
build_apk.bat
```

Le script détectera WSL et lancera automatiquement la compilation.

**OU directement depuis WSL:**
```bash
cd /mnt/c/Users/VotreNom/PyBar
./build_apk.sh
```

#### Étape 5: Récupérer l'APK

L'APK sera créé dans `bin/pybar-1.0-arm64-v8a-debug.apk`.

Vous pouvez y accéder depuis:
- **Windows:** `C:\Users\VotreNom\PyBar\bin\`
- **WSL:** `/mnt/c/Users/VotreNom/PyBar/bin/`

### Option 2: Docker Desktop

#### Prérequis

1. Installer [Docker Desktop pour Windows](https://www.docker.com/products/docker-desktop)
2. Activer l'intégration WSL2 dans Docker Desktop (Paramètres > General > Use WSL 2)

#### Construction avec Docker

Ouvrir PowerShell ou CMD:

```cmd
cd C:\Users\VotreNom\PyBar

# Lancer un conteneur Ubuntu
docker run -v %CD%:/app -w /app -it ubuntu:22.04 bash
```

Dans le conteneur:

```bash
# Installer les dépendances
apt-get update
apt-get install -y \
    python3-pip \
    git \
    build-essential \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    openjdk-11-jdk \
    zip \
    unzip

# Installer Buildozer
pip3 install buildozer cython

# Construire l'APK
./build_apk.sh
```

L'APK sera dans `bin/` et accessible depuis Windows.

### Option 3: Machine Virtuelle

#### Logiciels recommandés:
- [VirtualBox](https://www.virtualbox.org/) (gratuit)
- [VMware Workstation Player](https://www.vmware.com/) (gratuit pour usage personnel)
- Hyper-V (intégré à Windows 10/11 Pro)

#### Configuration:

1. Télécharger [Ubuntu 22.04 LTS](https://ubuntu.com/download/desktop)
2. Créer une machine virtuelle:
   - RAM: 4 GB minimum (8 GB recommandé)
   - Disque: 40 GB minimum
   - CPU: 2 cœurs minimum
3. Installer Ubuntu dans la VM
4. Suivre les instructions Linux standard (voir README.md)

#### Transfert de fichiers:

- **Dossier partagé:** Configurer un dossier partagé entre Windows et la VM
- **SSH/SCP:** Transférer via le réseau
- **Disque virtuel:** Monter le disque de la VM depuis Windows

### Résolution de problèmes Windows

#### WSL n'est pas reconnu

```cmd
# Vérifier l'installation
wsl --version

# Si erreur, installer/réinstaller WSL
wsl --install

# Ou mettre à jour
wsl --update
```

#### Erreur "Le système ne peut pas trouver le chemin d'accès spécifié"

Vérifiez que vous êtes dans le bon dossier:
```cmd
cd C:\Users\VotreNom\PyBar
dir
```

Vous devriez voir `build_apk.bat` dans la liste.

#### Permission refusée dans WSL

```bash
# Donner les permissions d'exécution
chmod +x build_apk.sh setup.sh

# Puis relancer
./build_apk.sh
```

#### Buildozer échoue avec erreur SDK/NDK

```bash
# Dans WSL, nettoyer les builds précédents
cd /mnt/c/Users/VotreNom/PyBar
buildozer android clean

# Relancer
buildozer android debug
```

#### Espace disque insuffisant

Buildozer télécharge ~5 GB de données (SDK, NDK). Assurez-vous d'avoir au moins 10 GB d'espace libre.

Pour WSL:
```cmd
# Vérifier l'espace dans WSL
wsl df -h
```

#### Compilation très lente

- **WSL:** Placez votre projet dans le système de fichiers Linux (`~/PyBar`) plutôt que sur `/mnt/c/`
- **Docker:** Augmentez la RAM allouée (Settings > Resources)
- **VM:** Allouez plus de CPU et RAM à la machine virtuelle

### Conseils de performance

#### Pour WSL (Plus rapide):

Au lieu de travailler depuis `/mnt/c/`, clonez le projet directement dans WSL:

```bash
# Dans WSL
cd ~
git clone https://github.com/Aguelord/PyBar.git
cd PyBar

# Installer les dépendances
pip3 install -r requirements.txt

# Construire
./build_apk.sh
```

**Récupérer l'APK dans Windows:**
```bash
# Depuis WSL, copier vers Windows
cp bin/*.apk /mnt/c/Users/VotreNom/Desktop/
```

Ou ouvrir l'explorateur Windows depuis WSL:
```bash
explorer.exe .
```

### Installation de l'APK sur Android

#### Via ADB (Android Debug Bridge)

1. **Activer le mode développeur** sur votre appareil Android:
   - Aller dans Paramètres > À propos du téléphone
   - Taper 7 fois sur "Numéro de build"
   - Retour > Options de développement > Activer "Débogage USB"

2. **Installer ADB sur Windows:**
   - Télécharger [SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools)
   - Extraire et ajouter au PATH

3. **Connecter l'appareil et installer:**
   ```cmd
   # Vérifier la connexion
   adb devices
   
   # Installer l'APK
   adb install bin\pybar-1.0-arm64-v8a-debug.apk
   ```

#### Installation manuelle

1. Transférer l'APK sur votre appareil (USB, email, cloud, etc.)
2. Ouvrir le fichier APK sur l'appareil
3. Autoriser l'installation depuis des sources inconnues si demandé
4. Installer

---

## 🇬🇧 English Version

### Overview

Buildozer, the Android compilation tool, requires a Linux environment. On Windows, you have three options:

1. **WSL2 (Recommended)** - Windows Subsystem for Linux
2. **Docker Desktop** - Linux container
3. **Virtual Machine** - VirtualBox, VMware, Hyper-V

### Option 1: WSL2 (Recommended) ⭐

This is the simplest and most performant method for Windows 10/11.

#### Step 1: Install WSL2

**Prerequisites:**
- Windows 10 version 2004+ (Build 19041+) or Windows 11
- Administrator rights

**Installation:**

1. Open PowerShell as Administrator
2. Run:
   ```powershell
   wsl --install
   ```
3. Restart your computer
4. On first launch, create a Linux username and password

**Verification:**
```cmd
wsl --version
wsl --list --verbose
```

You should see an Ubuntu distribution listed.

#### Step 2: Configure WSL Environment

Open WSL (type `wsl` in CMD or search "Ubuntu" in Start menu):

```bash
# Update packages
sudo apt-get update
sudo apt-get upgrade -y

# Install Python dependencies
sudo apt-get install -y python3 python3-pip python3-venv

# Install Buildozer dependencies
sudo apt-get install -y \
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
    zlib1g-dev \
    openjdk-11-jdk \
    zip \
    unzip

# Install Buildozer
pip3 install buildozer cython
```

#### Step 3: Access Project from WSL

Your Windows files are accessible from WSL in `/mnt/`:

```bash
# Example: If your project is in C:\Users\YourName\PyBar
cd /mnt/c/Users/YourName/PyBar

# Verify files are present
ls -la
```

**⚠️ Important:** Always work from `/mnt/c/...` to access your Windows files.

#### Step 4: Build the APK

**From Windows CMD/PowerShell:**
```cmd
cd C:\Users\YourName\PyBar
build_apk.bat
```

The script will detect WSL and automatically launch the build.

**OR directly from WSL:**
```bash
cd /mnt/c/Users/YourName/PyBar
./build_apk.sh
```

#### Step 5: Retrieve the APK

The APK will be created in `bin/pybar-1.0-arm64-v8a-debug.apk`.

You can access it from:
- **Windows:** `C:\Users\YourName\PyBar\bin\`
- **WSL:** `/mnt/c/Users/YourName/PyBar/bin/`

### Option 2: Docker Desktop

#### Prerequisites

1. Install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. Enable WSL2 integration in Docker Desktop (Settings > General > Use WSL 2)

#### Building with Docker

Open PowerShell or CMD:

```cmd
cd C:\Users\YourName\PyBar

# Launch Ubuntu container
docker run -v %CD%:/app -w /app -it ubuntu:22.04 bash
```

Inside the container:

```bash
# Install dependencies
apt-get update
apt-get install -y \
    python3-pip \
    git \
    build-essential \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    openjdk-11-jdk \
    zip \
    unzip

# Install Buildozer
pip3 install buildozer cython

# Build APK
./build_apk.sh
```

The APK will be in `bin/` and accessible from Windows.

### Option 3: Virtual Machine

#### Recommended Software:
- [VirtualBox](https://www.virtualbox.org/) (free)
- [VMware Workstation Player](https://www.vmware.com/) (free for personal use)
- Hyper-V (built into Windows 10/11 Pro)

#### Configuration:

1. Download [Ubuntu 22.04 LTS](https://ubuntu.com/download/desktop)
2. Create a virtual machine:
   - RAM: 4 GB minimum (8 GB recommended)
   - Disk: 40 GB minimum
   - CPU: 2 cores minimum
3. Install Ubuntu in the VM
4. Follow standard Linux instructions (see README.md)

#### File Transfer:

- **Shared Folder:** Configure a shared folder between Windows and VM
- **SSH/SCP:** Transfer over network
- **Virtual Disk:** Mount the VM disk from Windows

### Windows Troubleshooting

#### WSL not recognized

```cmd
# Check installation
wsl --version

# If error, install/reinstall WSL
wsl --install

# Or update
wsl --update
```

#### Error "The system cannot find the path specified"

Verify you're in the correct folder:
```cmd
cd C:\Users\YourName\PyBar
dir
```

You should see `build_apk.bat` in the list.

#### Permission denied in WSL

```bash
# Give execution permissions
chmod +x build_apk.sh setup.sh

# Then retry
./build_apk.sh
```

#### Buildozer fails with SDK/NDK error

```bash
# In WSL, clean previous builds
cd /mnt/c/Users/YourName/PyBar
buildozer android clean

# Retry
buildozer android debug
```

#### Insufficient disk space

Buildozer downloads ~5 GB of data (SDK, NDK). Ensure you have at least 10 GB free.

For WSL:
```cmd
# Check space in WSL
wsl df -h
```

#### Very slow compilation

- **WSL:** Place your project in Linux filesystem (`~/PyBar`) rather than `/mnt/c/`
- **Docker:** Increase allocated RAM (Settings > Resources)
- **VM:** Allocate more CPU and RAM to the virtual machine

### Performance Tips

#### For WSL (Faster):

Instead of working from `/mnt/c/`, clone the project directly in WSL:

```bash
# In WSL
cd ~
git clone https://github.com/Aguelord/PyBar.git
cd PyBar

# Install dependencies
pip3 install -r requirements.txt

# Build
./build_apk.sh
```

**Retrieve APK in Windows:**
```bash
# From WSL, copy to Windows
cp bin/*.apk /mnt/c/Users/YourName/Desktop/
```

Or open Windows Explorer from WSL:
```bash
explorer.exe .
```

### Installing APK on Android

#### Via ADB (Android Debug Bridge)

1. **Enable developer mode** on your Android device:
   - Go to Settings > About phone
   - Tap 7 times on "Build number"
   - Back > Developer options > Enable "USB debugging"

2. **Install ADB on Windows:**
   - Download [SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools)
   - Extract and add to PATH

3. **Connect device and install:**
   ```cmd
   # Check connection
   adb devices
   
   # Install APK
   adb install bin\pybar-1.0-arm64-v8a-debug.apk
   ```

#### Manual Installation

1. Transfer APK to your device (USB, email, cloud, etc.)
2. Open the APK file on the device
3. Allow installation from unknown sources if prompted
4. Install

---

## 📋 Quick Reference

### Commands Cheat Sheet

```cmd
# Windows - Install WSL
wsl --install

# Windows - Run build
build_apk.bat

# WSL - Access project
cd /mnt/c/Users/YourName/PyBar

# WSL - Build APK
./build_apk.sh

# Docker - Build APK
docker run -v %CD%:/app -w /app -it ubuntu:22.04 bash
./build_apk.sh

# Install on Android device
adb install bin\pybar-1.0-arm64-v8a-debug.apk
```

### Disk Space Requirements

- SDK/NDK download: ~5 GB
- Build artifacts: ~2 GB
- Total recommended: 10 GB free

### Build Time

- First build: 30-60 minutes (downloads SDK/NDK)
- Subsequent builds: 5-10 minutes

### Support

For issues or questions:
- GitHub Issues: https://github.com/Aguelord/PyBar/issues
- Check logs in `.buildozer/` directory
- Enable debug mode: `buildozer -v android debug`
