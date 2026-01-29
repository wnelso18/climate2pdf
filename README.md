# 🌤️Weather Report Generator⛈️

A desktop GUI app that lets you click a map (or enter coordinates), choose a date, and generate a PDF precipitation report for the prior 7 days. Data is pulled from the Visual Crossing Weather API and exported as a clean table with 48-hour and 7-day totals.

## Features
- Interactive map click-to-select location (or manual lat/lon entry)
- Generates a PDF report:
  - Daily precipitation (inches) for the 7-day window
  - 48-hour total ending on the selected date
  - 7-day total ending on the selected date
  - Coordinates + custom town/city name in the title
- Displays a random “weather fact” each launch

## Tech Stack
- Python + Tkinter GUI
- `tkintermapview` for the map widget
- `requests` for API calls
- `reportlab` for PDF generation
- `ttkthemes` for a modern theme

## Setup

### 1) Create and activate a virtual environment (recommended)
**Windows (PowerShell)**
```
python -m venv .venv
.\.venv\Scripts\activate
```

### 2) Build a Windows `.exe` (PyInstaller)
**These steps package the app into a standalone Windows executable.**

#### 1) Open a terminal in the project folder
Make sure you are in the same directory as your main Python file (e.g., `app.py`).

#### 2) (Recommended) Create + activate a virtual environment
```
python -m venv .venv
.\.venv\Scripts\activate
```

#### 3) Install dependencies
```
pip install -r requirements.txt
pip install pyinstaller
```

#### 4) Build the executable
```
Replace app.py with your actual entry-point filename if different:

pyinstaller --noconfirm --onefile --windowed --name Climate2PDF app.py
Output location

dist/Climate2PDF.exe
```

#### 5) If the .exe opens then immediately closes
##### Rebuild with hidden imports (helps PyInstaller bundle GUI dependencies):
```
pyinstaller --noconfirm --onefile --windowed --name Climate2PDF ^
  --hidden-import=tkintermapview ^
  --hidden-import=ttkthemes ^
  app.py
```

#### 6) Notes

PyInstaller will create build/ (temporary files) and dist/ (final output).

For sharing, you typically distribute the executable found in dist/.

Windows SmartScreen warnings are common for unsigned executables.





