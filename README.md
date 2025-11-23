# Port Scanner GUI

Application de scan de ports avec interface Tkinter moderne. Elle permet de tester rapidement une plage de ports sur une adresse IP ou un domaine, d'afficher les ports ouverts et de les ouvrir dans le navigateur.

## Fonctionnalités
- Interface sombre moderne avec formulaire clair et barre de progression.
- Scan multi-threads configurable sur une plage de ports donnée.
- Possibilité d'arrêter un scan en cours.
- Liste triée des ports ouverts et bouton pour les ouvrir dans le navigateur (HTTP ou HTTPS sur 443).
- Indication de version intégrée dans l'interface (v1.1.0).

## Prérequis
- Python 3.10 ou plus récent.
- Modules standards uniquement (socket, tkinter, concurrent.futures...). Aucune dépendance externe n'est nécessaire pour l'exécution.

## Installation et lancement
```bash
python main.py
```

Sous Windows, vous pouvez également utiliser le script `start.bat` :
```bat
start.bat
```

## Construire un exécutable (.exe)
1. Installez PyInstaller (dans un environnement virtuel de préférence) :
   ```bash
   python -m pip install pyinstaller
   ```
2. Générez l'exécutable :
   ```bash
   pyinstaller --onefile --noconsole --name PortScanner main.py
   ```
3. Le binaire sera disponible dans `dist/PortScanner.exe`. Copiez ce fichier où vous le souhaitez pour distribuer l'application.

## Utilisation
1. Indiquez l'adresse IP ou le domaine à scanner.
2. Définissez la plage de ports (1 à 65535).
3. Cliquez sur **Lancer le scan** puis surveillez la progression.
4. Cliquez sur **Ouvrir les ports** pour tester les services détectés dans le navigateur.

## Dépannage
- Si aucun port n'est trouvé, vérifiez que la cible est accessible et que les ports ne sont pas filtrés.
- Si l'interface ne s'affiche pas sous Windows, assurez-vous d'avoir installé Python avec l'option Tkinter.
- Pour réduire les faux positifs, évitez de lancer plusieurs scans simultanés sur la même cible.

## Licence
Ce projet est distribué sous licence MIT. Consultez le fichier [LICENSE](LICENSE).
