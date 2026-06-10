<?php
/**
 * Skript zur Generierung einer Übersichtsseite für alle Ordner in /httpdocs/
 * Sucht nach Index-Dateien und erstellt ein responsives Raster mit 4 Spalten.
 * Ausgabe: /httpdocs/all.html
 */

// Root-Verzeichnis des Webspaces
$rootDir = __DIR__;

// Dateinamen, die als Startseiten gelten
$indexFiles = [
    'index.html',
    'index.php',
    'default.html',
    'default.php',
    'start.html',
    'home.html',
    'home.php'
];

// Funktion zum Suchen der Index-Datei in einem Ordner
function findIndexFile($dir, $indexFiles) {
    foreach ($indexFiles as $file) {
        $path = $dir . '/' . $file;
        if (file_exists($path) && is_file($path)) {
            return $file;
        }
    }
    return null;
}

// Alle Unterordner in /httpdocs/ sammeln
$dirs = [];
$items = scandir($rootDir);
foreach ($items as $item) {
    if ($item === '.' || $item === '..' || $item === basename(__FILE__) || $item === 'all.html') {
        continue;
    }
    $path = $rootDir . '/' . $item;
    if (is_dir($path)) {
        $dirs[] = $item;
    }
}

// Alphabetisch sortieren
sort($dirs);

// HTML-Inhalt generieren
$html = <<<HTML
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Übersicht aller Projekte</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
        }
        h1 {
            text-align: center;
            margin-bottom: 20px;
            color: #333;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }
        .card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .card a {
            text-decoration: none;
            color: #333;
            font-weight: bold;
            font-size: 1.2em;
            display: block;
        }
        .card .no-index {
            color: #888;
            font-style: italic;
            font-size: 0.9em;
        }
        .card .error {
            color: #d32f2f;
            font-size: 0.9em;
        }
        @media (max-width: 1200px) {
            .grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }
        @media (max-width: 900px) {
            .grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        @media (max-width: 600px) {
            .grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <h1>Übersicht aller Projekte</h1>
    <div class="grid">
HTML;

// Für jeden Ordner eine Karte erstellen
foreach ($dirs as $dir) {
    $dirPath = $rootDir . '/' . $dir;
    $indexFile = findIndexFile($dirPath, $indexFiles);
    
    if ($indexFile !== null) {
        $url = '/' . $dir . '/' . $indexFile;
        $html .= <<<HTML
        <div class="card">
            <a href="$url">$dir</a>
        </div>
HTML;
    } else {
        // Keine Index-Datei gefunden
        $html .= <<<HTML
        <div class="card">
            <span class="no-index">$dir</span>
            <div class="error">Keine Startseite gefunden</div>
        </div>
HTML;
    }
}

$html .= <<<HTML
    </div>
</body>
</html>
HTML;

// HTML in /httpdocs/all.html speichern
$outputPath = $rootDir . '/all.html';
file_put_contents($outputPath, $html);

echo "Übersichtsseite erfolgreich generiert: <a href='/all.html'>/all.html</a>";
?