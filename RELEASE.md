# Processus de release

Ce dépôt contient uniquement des dépendances de la bibliothèque standard. Pour générer une release Windows incluant un exécutable :

1. Créer et activer un environnement virtuel (recommandé).
2. Installer PyInstaller :
   ```bash
   python -m pip install pyinstaller
   ```
3. Générer le binaire :
   ```bash
   pyinstaller --onefile --noconsole --name PortScanner main.py
   ```
4. Récupérer l'exécutable dans `dist/PortScanner.exe` et le placer dans l'archive de release.
5. Vérifier le lancement de l'EXE sur une machine Windows (double-clic ou `PortScanner.exe` dans le terminal).

Pensez à mettre à jour `CHANGELOG.md` et à incrémenter `APP_VERSION` dans `main.py` lors d'une nouvelle release.
