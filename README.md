# 🥈 Silver Tracker Pro

A desktop app for antique hunters to value silver coins and silverware in real time using live spot prices.

**Features:** Live spot prices (APMEX + fallbacks) · Multi-currency display (USD, GBP, EUR, CAD, AUD, MXN, CHF) · 70+ junk silver coins across 11 countries · Melt value calculator · Manual spot override for offline use · Auto-refresh

---

## 📦 Installation (for users)

### Option A — Run from source (simplest)

```bash
# 1. Make sure Python 3.8+ is installed: https://python.org/downloads
# 2. Download or clone this repo, then:

pip install -r requirements.txt
python silver_tracker.py
```

### Option B — Install as a command (pip install)

```bash
pip install .
silver-tracker-gui        # launches the app
```

### Option C — Download a standalone .exe / .app (no Python needed)

See the [Releases](../../releases) page — grab the latest `.exe` (Windows) or `.app` (Mac).

---

## 🚀 Publishing to GitHub (step by step)

### First time setup

```bash
# Install Git if you don't have it: https://git-scm.com/downloads
# Install GitHub CLI (optional but easier): https://cli.github.com

cd path/to/your/silver_tracker/folder

git init
git add .
git commit -m "Initial release: Silver Tracker Pro v1.1"
```

### Create the repo on GitHub

**With GitHub CLI (easiest):**
```bash
gh auth login          # one-time login, follow prompts
gh repo create silver-tracker --public --push --description "Precious metals tracker for antique hunters"
```

**Manually via website:**
1. Go to https://github.com/new
2. Name it `silver-tracker`, set to Public, click Create
3. Then run:
```bash
git remote add origin https://github.com/YOUR_USERNAME/silver-tracker.git
git branch -M main
git push -u origin main
```

### Pushing future updates

```bash
git add .
git commit -m "Describe what you changed"
git push
```

---

## 📱 Making a Standalone App (no Python needed for users)

This is how you turn the script into a proper `.exe` (Windows) or `.app` (Mac) that anyone can download and double-click.

### Windows — create a .exe

```bash
# Install PyInstaller
pip install pyinstaller

# Build the exe (--noconsole hides the terminal window, --onefile = single file)
pyinstaller --noconsole --onefile --name "SilverTracker" silver_tracker.py

# Your .exe will be in:  dist/SilverTracker.exe
```

**Add a custom icon (optional):**
1. Get a `.ico` file (convert any PNG at https://convertio.co/png-ico)
2. Place it in the folder, then:
```bash
pyinstaller --noconsole --onefile --icon=silver.ico --name "SilverTracker" silver_tracker.py
```

### Mac — create a .app

```bash
pip install pyinstaller

pyinstaller --noconsole --onefile --windowed --name "SilverTracker" silver_tracker.py

# Your .app bundle will be in:  dist/SilverTracker.app
# To share it: zip the .app and send/upload it
```

> **Mac note:** Users may see a security warning ("unidentified developer") when opening.
> They can right-click the app → Open → Open anyway to bypass it.
> To avoid this permanently, you'd need an Apple Developer account ($99/year) for code signing.

### Linux — create a binary

```bash
pip install pyinstaller
pyinstaller --onefile --name "silver-tracker" silver_tracker.py
# dist/silver-tracker  (no extension, just runs)
```

---

## 📤 Publishing the app as a GitHub Release

This is how to add your `.exe` / `.app` to GitHub so people can download it directly:

```bash
# Tag a version
git tag v1.1.0
git push origin v1.1.0
```

Then on GitHub:
1. Go to your repo → **Releases** → **Create a new release**
2. Select the `v1.1.0` tag
3. Drag and drop your `SilverTracker.exe` (or `.app` zip) into the assets section
4. Click **Publish release**

Users can then download your app from: `https://github.com/YOUR_USERNAME/silver-tracker/releases`

---

## 💡 Tips & Notes

- **Yellow highlighted rows** in the tracker mean the price came from a fallback source (not APMEX directly) — still accurate but worth knowing.
- **Manual spot override** on the Calculator tab lets you use the app completely offline — just look up today's silver spot on your phone and enter it.
- **Currency selector** in the top-right converts all values live using real exchange rates fetched alongside spot prices.
- All coin weights and purities are based on official mint specifications.

---

## 🛠 Dependencies

| Package | Purpose |
|---|---|
| `ttkbootstrap` | Dark-themed GUI |
| `cloudscraper` | Bypasses Cloudflare on APMEX |
| `beautifulsoup4` | Parses APMEX HTML |
| `urllib` (stdlib) | Fallback price & exchange rate fetching — no install needed |

---

## 📄 Licence

MIT — free to use, share, and modify.
