
# Gioco dell'Impiccato — NiceGUI Edition

Un semplice ma completo **Gioco dell’Impiccato** realizzato in Python utilizzando **NiceGUI** per l’interfaccia grafica.
Supporta sia la modalità **grafica con immagini** che la modalità **ASCII art**, ed è compatibile con esecuzione tramite **PyInstaller** grazie al sistema di gestione delle risorse integrato.

<p align="center">
  <img src="media/logo.png" alt="Logo" width="200">
</p>

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/geo-petrini/impiccato)](https://github.com/geo-petrini/impiccato/graphs/commit-activity)
[![GitHub issues](https://img.shields.io/github/issues/geo-petrini/nicegui?color=blue)](https://github.com/geo-petrini/impiccato/issues)
[![GitHub forks](https://img.shields.io/github/forks/geo-petrini/impiccato)](https://github.com/geo-petrini/impiccato/network)
[![GitHub stars](https://img.shields.io/github/stars/geo-petrini/impiccato)](https://github.com/geo-petrini/impiccato/stargazers)

---

## ✨ Funzionalità

* ✔ **Interfaccia moderna** costruita con NiceGUI
* ✔ Sistema completo di **logica di gioco (MVC-like)**
* ✔ Supporto a **due modalità di disegno dell’omino**:

  * 🖼 immagini (`media/00.png … media/10.png`)
  * 🔤 ASCII art integrata
* ✔ Gestione automatica della cartella temporanea di PyInstaller (`_MEIPASS`)
* ✔ Notifiche grafiche di vittoria/sconfitta
* ✔ Tastiera virtuale con lettere cliccabili
* ✔ File esterno con lista di parole (`data/parole.txt`)

---

## 🧩 Struttura del Progetto

```
.
├── main.py
├── media/
│   ├── 00.png
│   ├── 01.png
│   └── ... 10.png
├── data/
│   └── parole.txt
└── README.md
```

---

## 🚀 Avvio del Programma

### 🔧 Requisiti

* Python 3.9+
* NiceGUI
  Installazione:

```bash
pip install nicegui
```

### ▶ Esecuzione

Avvia il programma con:

```bash
python main.py
```

L’applicazione si aprirà in una finestra nativa grazie alle API `ui.run(native=True)`.

---

## 🛠 Compilazione con PyInstaller

Il programma include `resource_path()`, una funzione che permette a PyInstaller di trovare correttamente immagini e file di testo anche all’interno della cartella temporanea.

Per la creazione del compilato consultare la guida seguente https://nicegui.io/documentation/section_configuration_deployment#package_for_installation

È richiesto pyinstaller, opzionalmente pillow per convertire l'icona da png al formato ideale per la piattaforma in uso
```bash
pip install pyinstaller pillow
```

Esempio di compilazione:

```bash
nicegui-pack 
 --onefile 
 --name "impiccato" 
 --icon "media/logo.png" 
 --windowed 
 --add-data "media/00.png:media" 
 --add-data "media/01.png:media" 
 --add-data "media/02.png:media" 
 --add-data "media/03.png:media" 
 --add-data "media/04.png:media" 
 --add-data "media/05.png:media" 
 --add-data "media/06.png:media" 
 --add-data "media/07.png:media" 
 --add-data "media/08.png:media" 
 --add-data "media/09.png:media" 
 --add-data "media/10.png:media"
 --add-data "media/logo.png:media" 
 --add-data "data/parole.txt:data" 
 impiccato.py
```

Il file verrà generato nella cartella `dist` del progetto.
Importante: cancellare la cartella `build` prima di ricompilarlo, altrimenti nicegui-pack restiuirà un errore.

---

## 🕹 Modalità di Gioco

* Clicca le lettere disponibili per indovinare la parola
* Le lettere corrette e sbagliate vengono visualizzate in due sezioni dedicate
* L’omino dell’impiccato avanza ad ogni errore (fino a 10 tentativi)
* A fine partita, un messaggio indica vittoria o sconfitta
* Il pulsante **“Nuova Partita”** permette di ricominciare immediatamente

---

## 📦 Personalizzazione

### Modifica della lista di parole

Basta editare:

```
data/parole.txt
```

Ogni parola deve essere su una riga.

### Modalità di disegno

Nel costruttore:

```python
ImpiccatoGame(mode=ImpiccatoGame.DRAW_MODE_PICS)
```

oppure

```python
ImpiccatoGame(mode=ImpiccatoGame.DRAW_MODE_TEXT)
```

---

## 📜 Licenza

MIT

---



