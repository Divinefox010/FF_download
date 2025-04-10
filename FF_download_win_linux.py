from selenium import webdriver # type: ignore
from selenium.webdriver.edge.service import Service as EdgeService# type: ignore
from selenium.webdriver.chrome.service import Service  # Ubuntu
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.edge.options import Options as EdgeOptions# type: ignore
from selenium.webdriver.chrome.options import Options # Ubuntu
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import os
import time
import platform

#Globale variables
file_path = "lien.txt"
wait_time = 3600            # 1 heure

#Efface la console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def wait_download(dossier, timeout=wait_time):
    debut = time.time()
    while time.time() - debut < timeout:
        fichiers = os.listdir(dossier)
        if any(f.endswith(".crdownload") for f in fichiers):
            time.sleep(1)
        else:
            print(f"✅ Téléchargement terminé en {time.time() - debut:.1f} secondes.")
            return True
    print("⛔ Timeout : téléchargement non terminé.")
    exit()


#Initialisation
def Init():
    global driver_path, download_dir, options, file_path    
    
    # Détéction du système
    system = platform.system()
    print(f"Système {system} détécté!")
    print("😎 Initialisation de l'environnement...")
    
    # Lien vers le fichier texte contenant les URLs
    if os.path.exists(file_path):
        print("✅ Le fichier d'URL a été trouvé.")
    else:
        print("❌ Le fichier texte n'a pas été trouvé / Placez-le dans le même dossier que ce script en le renommant lien.txt")
        exit()

    if system == "Windows":
        # Chemin vers le Edge WebDriver
        if os.path.exists("msedgedriver.exe"):
            driver_path = "msedgedriver.exe"  # <-- adapte ici
            print("✅ Le WebDriver a été trouvé.")
        else:
            print("❌ Le WebDriver n'a pas été trouvé / Placez-le dans le même dossier que ce script.")
            exit()

        # Dossier de téléchargement
        if os.path.exists("telechargements"):
            download_dir = os.path.abspath("telechargements")
            print("✅ Le dossier de téléchargement a été trouvé.")
        else:
            print("❌ Le dossier de téléchargement n'a pas été trouvé.")
            os.mkdir("telechargements")
            print("✅ Le dossier de téléchargement a été créé.")

        print("Configuration de l'environnement...")
        # Options de configuration
        options = EdgeOptions()

    elif system == "Linux":    
        # Chemin vers le Edge WebDriver
        if os.path.exists("/usr/lib/chromium-browser/chromedriver"):
            driver_path = "/usr/lib/chromium-browser/chromedriver"  # <-- adapte ici
            print("✅ Le WebDriver a été trouvé.")
        else:
            print("❌ Le WebDriver chromium n'a pas été trouvé / Assurez vous d'avoir bien installé chromium driver.")
            exit()

        # Dossier de téléchargement
        if os.path.exists("telechargements"):
            download_dir = os.path.abspath("telechargements")
            print("✅ Le dossier de téléchargement a été trouvé.")
        else:
            print("❌ Le dossier de téléchargement n'a pas été trouvé.")
            os.mkdir("telechargements")
            print("✅ Le dossier de téléchargement a été créé.")

        print("Configuration de l'environnement...")
        # Options de configuration
        options = Options()
    else:
        print(f"Système non supporté : {system}")
        exit()
    
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "directory_upgrade": True
    }
    options.add_experimental_option("prefs", prefs)
    
    # Activer le mode headless
    #options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Option nécessaire parfois en mode headless
    options.add_argument('--no-sandbox')


    while True:
        try:
            choix = input("Lancer le navigateur maintenant? (O/N) : ")
            if choix == "O" or choix == "o":    
                start_browser()
                break
            elif choix == "N" or choix == "n":
                print("🙋 Application fermée!")
                exit()
            else:
                print("❌ Choix invalide. Veuillez entrer O ou N.")
        except ValueError:
            print("❌ Veuillez entrer un nombre valide.")

def start_browser():
    global driver
    # Démarrage de Edge avec Selenium
    try:
        if platform.system() == "Windows":
            driver = webdriver.Edge(service=Service(driver_path), options=options)
        elif platform.system() =="Linux":
            driver = webdriver.Chrome(service=Service(driver_path), options=options)
        else:
            print(f"❌ Système non supporté : {platform.system()}")
            exit()

        print("😎 Le navigateur a été lancé.")
        start_download()
    except Exception as e:
        print(f"❌ Erreur lors du lancement du navigateur : {e}")
        exit()

def start_download():
    print("Lancement du téléchargement...")
    # Lire les URLs depuis le fichier
    with open(file_path, "r") as file:
        urls = [line.strip() for line in file if line.strip()]
    
    print(f"Ouverture du lien...")
    for url in urls:
        choix = input(f"Lancer le téléchargement de {url} ? (O/N) S: sortir : ")
        if choix == "O" or choix == "o":
            driver.get(url)
            sleep(1)
            try:
                bouton = driver.find_element(By.CSS_SELECTOR, ".link-button")
                bouton.click()
                sleep(3)
                bouton.click()
                print(f"Téléchargement de {url}")
                time.sleep(20)
                wait_download(download_dir) # type: ignore
            except Exception as e:
                print(f"Erreur : {e}")
        elif choix == "N" or choix == "n":
            print("Fichier ignoré !")
        elif choix == "S" or choix == "s":
            print("🙋 Application fermée !")
            exit()
        else:
            print("❌ Choix invalide. Veuillez entrer O ou N.")

Init()
input("Le téléchargement complet est terminé...")
driver.quit()
