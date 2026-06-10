# Übersichtsseite für code.nozilla.net

Dieses Skript generiert eine Übersichtsseite (`all.html`), die alle Ordner in `/httpdocs/` auflistet und mit ihren Index-Dateien verlinkt.

---

## 📁 Dateien
- **`generate_all.php`**: PHP-Skript zur Generierung der Übersichtsseite.
- **`all.html`**: Generierte Übersichtsseite (wird automatisch erstellt).

---

## 🚀 Einrichtung

### 1. Skript hochladen
Lade die Datei `generate_all.php` in dein `/httpdocs/` Verzeichnis auf dem Server hoch.

### 2. Manuell ausführen
Ruf das Skript einmal manuell auf, um `all.html` zu generieren:
```bash
php /pfad/zum/httpdocs/generate_all.php
```
Oder per Browser:
```
https://code.nozilla.net/generate_all.php
```

### 3. Cronjob einrichten (für tägliche Aktualisierung)
Füge folgenden Eintrag zu deiner **Crontab** hinzu:
```bash
0 3 * * * /usr/bin/php /pfad/zum/httpdocs/generate_all.php >/dev/null 2>&1
```
- **Bedeutung**: Das Skript wird täglich um **3:00 Uhr** ausgeführt.
- **Pfad anpassen**: Ersetze `/pfad/zum/httpdocs/` mit dem tatsächlichen Pfad zu deinem Webspace (z. B. `/home/nozilla/httpdocs/`).

#### So bearbeitest du die Crontab:
1. Verbinde dich per SSH mit deinem Server.
2. Führe aus:
   ```bash
   crontab -e
   ```
3. Füge die Zeile oben ein und speichere die Datei.

---

## ✅ Funktionen
- **Automatische Erkennung**: Sucht nach `index.html`, `index.php`, `default.html`, `default.php`, `start.html`, `home.html`, `home.php`.
- **Responsives Design**: 4-Spalten-Raster, das sich an die Bildschirmgröße anpasst.
- **Fehlerbehandlung**: Ordner ohne Index-Datei werden mit Hinweis angezeigt.
- **Sortierung**: Ordner werden alphabetisch sortiert.

---

## 🔧 Anpassungen

### Weitere Index-Dateien hinzufügen
Bearbeite die Liste `$indexFiles` in `generate_all.php`:
```php
$indexFiles = [
    'index.html',
    'index.php',
    'default.html',
    // Füge hier weitere Dateinamen hinzu
];
```

### Design anpassen
Ändere die CSS-Stile im `<style>`-Block in `generate_all.php`:
- Farben, Schatten, Abstände etc. können direkt angepasst werden.

---

## 📌 Hinweise
- Das Skript **überschreibt** die bestehende `all.html` bei jedem Aufruf.
- Ordner, die mit `.` beginnen (z. B. `.git`), werden ignoriert.
- Die Dateien `generate_all.php` und `all.html` werden nicht als Ordner angezeigt.

---

## 🔗 Zugriff auf die Übersichtsseite
Nach der Einrichtung ist die Übersichtsseite unter folgender URL erreichbar:
```
https://code.nozilla.net/all.html
```
