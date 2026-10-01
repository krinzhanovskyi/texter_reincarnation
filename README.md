<a href="https://stand-with-ukraine.pp.ua"><img src="https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraineFlat.svg" alt="#StandWithUkraine" /></a>

# Texter Reincarnation

A lightweight desktop Python (PyQt6) application for automatic character-by-character text input. It simulates real human typing, allowing you to bypass paste (Ctrl+V) restrictions on websites and in various applications.

## Features

- **Preview and editing:** Text captured from the clipboard can be reviewed and edited directly in the application window before typing begins.
- **Human simulation:** Typing occurs with random micro-delays between keystrokes to mimic a live user.
- **Always on top:** The program window stays above all other windows, making it convenient when working with a browser.
- **Panic button:** The global `F12` shortcut instantly aborts the typing process at any moment.

## Installation

Python 3.x is required to run the program.

1. Open a terminal in the project folder.
2. Create and activate a virtual environment:
   PowerShell

```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install the required dependencies:
   PowerShell
   `bash
pip install -r requirements.txt
`
   _(Dependencies: `pyperclip`, `keyboard`, `PyQt6`)_

## Usage

1. Run the script:
   PowerShell

```bash
python main.py
```

2. Copy the desired text (Ctrl+C). The program will load it automatically upon startup. If the app is already running, click **Update** _(Update from clipboard)_.
3. Click **"Start** _(Start typing)_.
4. You will have exactly **5 seconds** to switch to your browser or target application and click inside the desired text field.
5. To immediately cancel the typing process, press the **F12** key (this works globally, even if the application window is not active).

## Important Notes (Windows)

- **Keyboard layout:** Before starting the text input, ensure your active Windows language layout matches the language of your text (e.g., ENG for English, RUS for Cyrillic). Otherwise, incorrect characters or symbols may be typed.
- **Administrator privileges:** The `keyboard` library operates at the system OS level. If your target application (where the text is being entered) is running as an administrator, the terminal running this Python script must also be launched with administrator privileges.
