import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import cloudscraper
from bs4 import BeautifulSoup
import threading
import time

# --- CONFIGURATION ---
METALS_CONFIG = [
    {"name": "Gold",      "url": "https://www.apmex.com/gold-price",      "search_term": "Gold Price Per Ounce"},
    {"name": "Silver",    "url": "https://www.apmex.com/silver-price",    "search_term": "Silver Price Per Ounce"},
    {"name": "Platinum",  "url": "https://www.apmex.com/platinum-price",  "search_term": "Platinum Price Per Ounce"},
    {"name": "Palladium", "url": "https://www.apmex.com/palladium-price", "search_term": "Palladium Price Per Ounce"},
]

# Global State
APP_STATE = {
    "show_in_oz": False,        # False = Grams, True = Troy Oz
    "auto_refresh": False,      # Is auto-refresh on?
    "last_data": None,          # Cache for the latest scraped data
    "is_fetching": False        # Prevent double-clicking refresh
}

CONST_GRAMS_PER_OZ = 31.1034768

# --- UTILS & SCRAPING ---

def clean_price_text(price_text):
    """Removes '$', 'USD', and commas to return a float."""
    try:
        clean = price_text.replace("$", "").replace("USD", "").replace(",", "").strip()
        return float(clean)
    except ValueError:
        return 0.0

def fetch_price(metal_info):
    """Fetches the price string for a single metal."""
    scraper = cloudscraper.create_scraper()
    try:
        response = scraper.get(metal_info["url"])
        if response.status_code == 403:
            return "Blocked"
        
        soup = BeautifulSoup(response.content, 'html.parser')
        label = soup.find(string=metal_info["search_term"])
        
        if label:
            price_element = label.find_next("td")
            if price_element:
                raw_text = price_element.get_text(strip=True)
                clean_display = raw_text.replace(" USD", "").strip()
                return clean_display
        return "Not Found"
    except Exception as e:
        print(f"Error fetching {metal_info['name']}: {e}")
        return "Error"

def calculate_coin_value(weight_grams, purity, spot_price):
    """Returns the raw value float for a coin."""
    return ((weight_grams * purity) / CONST_GRAMS_PER_OZ) * spot_price

def get_all_data():
    """Scrapes all data and calculates values."""
    spot_results = []
    silver_price_str = "0"
    
    # 1. Fetch Spot Prices
    for metal in METALS_CONFIG:
        price = fetch_price(metal)
        spot_results.append({
            "name": metal["name"], 
            "weight_g": 31.1034768, 
            "price_str": price,
            "is_spot": True
        })
        
        if metal["name"] == "Silver":
            silver_price_str = price
            
    silver_spot = clean_price_text(silver_price_str)
    
    # Initialize lists for all categories
    categories = {
        "us": [], "cad": [], "uk": [], "aus": [], "mex": [],
        "prt": [], "esp": [], "fra": [], "ita": [], "deu": [], "che": []
    }

    if silver_spot > 0:
        def add_coin(cat_key, name, weight_g, purity):
            val = calculate_coin_value(weight_g, purity, silver_spot)
            categories[cat_key].append({
                "name": name,
                "weight_g": weight_g,
                "price_str": f"${val:.2f}",
                "is_spot": False
            })

        # --- US JUNK ---
        add_coin("us", "5c Wartime Nickel (1942-1945 35%)", 5, 0.350)
        add_coin("us", "10c Dime (1892-1964)", 2.5, 0.9)
        add_coin("us", "25c Quarter (1892-1964)", 6.25, 0.9)
        add_coin("us", "50c Half Dollar (1892-1964)", 12.5, 0.9)
        add_coin("us", "50c Half Dollar (1965-1970 40%)", 11.5, 0.4)
        add_coin("us", "Morgan/Peace Dollar (1878-1935)", 26.73, 0.9)
        add_coin("us", "Eisenhower Dollar (1971-1977 40%)", 24.59, 0.4)

        # --- CAD JUNK ---
        add_coin("cad", "10c Dime (1858-1919)", 2.324, 0.925)
        add_coin("cad", "10c Dime (1920-1967)", 2.33, 0.8)
        add_coin("cad", "10c Dime (1968 50%)", 2.33, 0.5)
        add_coin("cad", "25c Quarter (1870-1919)", 5.83, 0.925)
        add_coin("cad", "25c Quarter (1920-1967)", 5.83, 0.8)
        add_coin("cad", "25c Quarter (1968 50%)", 5.83, 0.5)
        add_coin("cad", "50c Half Dollar (1870-1919)", 11.62, 0.925)
        add_coin("cad", "50c Half Dollar (1920-1967)", 11.66, 0.8)
        add_coin("cad", "$1 Dollar (1935-1967)", 23.33, 0.8)

        # --- UK JUNK ---
        add_coin("uk", "3 Pence (1887-1919)", 1.41, 0.925)
        add_coin("uk", "3 Pence (1920-1936)", 1.41, 0.500)
        add_coin("uk", "6 Pence (1887-1919)", 2.83, 0.925)
        add_coin("uk", "6 Pence (1920-1946)", 2.83, 0.500)
        add_coin("uk", "1 Shilling (1887-1919)", 5.66, 0.925)
        add_coin("uk", "1 Shilling (1920-1946)", 5.66, 0.500)
        add_coin("uk", "2 Shilling/Florin (1887-1919)", 11.31, 0.925)
        add_coin("uk", "2 Shilling/Florin (1920-1946)", 11.3, 0.500)
        add_coin("uk", "1/2 Crown (1887-1919)", 14.14, 0.925)
        add_coin("uk", "1/2 Crown (1920-1946)", 14.14, 0.500)

        # --- AUSTRALIAN JUNK ---
        add_coin("aus", "3 Pence (1910-1944)", 1.41, 0.925)
        add_coin("aus", "3 Pence (1947-1964)", 1.41, 0.500)
        add_coin("aus", "6 Pence (1910-1945)", 2.83, 0.925)
        add_coin("aus", "6 Pence (1946-1963)", 2.83, 0.500)
        add_coin("aus", "1 Shilling (1910-1945)", 5.66, 0.925)
        add_coin("aus", "1 Shilling (1946-1963)", 5.66, 0.500)
        add_coin("aus", "2 Shilling/Florin (1910-1945)", 11.31, 0.925)
        add_coin("aus", "2 Shilling/Florin (1946-1963)", 11.31, 0.500)
        add_coin("aus", "50 Cents (1966)", 13.28, 0.800)

        # --- MEXICO JUNK ---
        add_coin("mex", "20 Centavos (1920-1943)", 3.33, 0.720)
        add_coin("mex", "25 Centavos (1950-1953)", 3.33, 0.300)
        add_coin("mex", "50 Centavos (1919-1945)", 8.33, 0.720)
        add_coin("mex", "50 Centavos (1950-1951)", 6.66, 0.300)
        add_coin("mex", "1 Peso (1920-1945)", 16.6, 0.720)
        add_coin("mex", "1 Peso (1947-1949)", 14.0, 0.500)
        add_coin("mex", "1 Peso (1950)", 13.33, 0.300)
        add_coin("mex", "1 Peso (1957-1967)", 16.0, 0.100)
        add_coin("mex", "5 Peso (1951-1954)", 27.78, 0.720)
        add_coin("mex", "5 Peso (1955-1957)", 18.055, 0.720)
        add_coin("mex", "10 Peso (1955-1960)", 28.888, 0.900)
        add_coin("mex", "100 Peso (1977-1979)", 27.78, 0.720)

        # --- PORTUGAL JUNK ---
        add_coin("prt", "2.50 Escudos (1932-1951)", 3.5, 0.650)
        add_coin("prt", "5 Escudos (1932-1951)", 7.0, 0.650)
        add_coin("prt", "10 Escudos (1932-1948)", 12.5, 0.835)
        add_coin("prt", "10 Escudos (1954-1955)", 12.5, 0.680)

        # --- SPANISH JUNK ---
        add_coin("esp", "100 Pesetas (1966-1970)", 19.0, 0.800)

        # --- FRENCH JUNK ---
        add_coin("fra", "1/2 Franc (1897-1920)", 2.5, 0.835)
        add_coin("fra", "1 Franc (1898-1920)", 5.0, 0.835)
        add_coin("fra", "2 Franc (1898-1920)", 10.0, 0.835)
        add_coin("fra", "10 Franc (1929-1939)", 10.0, 0.680)
        add_coin("fra", "20 Franc (1929-1939)", 20.0, 0.680)
        add_coin("fra", "5 Franc (1960-1969)", 12.0, 0.835)
        add_coin("fra", "10 Franc (1965-1973)", 25.0, 0.900)
        add_coin("fra", "50 Franc (1974-1980)", 30.0, 0.900)
        add_coin("fra", "100 Franc (1982-2001)", 15.0, 0.900)

        # --- ITALIAN JUNK ---
        add_coin("ita", "5 Lire (1926-1941)", 5.0, 0.835)
        add_coin("ita", "10 Lire (1926-1941)", 10.0, 0.835)
        add_coin("ita", "20 Lire (1927-1934)", 15.0, 0.800)
        add_coin("ita", "20 Lire (1936-1941)", 20.0, 0.800)
        add_coin("ita", "500 Lire (1958-1967)", 11.0, 0.835)

        # --- GERMAN JUNK ---
        add_coin("deu", "1/2 Mark (1896-1919)", 2.777, 0.900)
        add_coin("deu", "1 Mark (1891-1916)", 5.556, 0.900)
        add_coin("deu", "1 Reichsmark (1924-1927)", 5.0, 0.500)
        add_coin("deu", "2 Reichsmark (1925-1931)", 10.0, 0.500)
        add_coin("deu", "2 Reichsmark (1933-1939)", 8.0, 0.625)
        add_coin("deu", "3 Reichsmark (1924-1933)", 15.0, 0.500)
        add_coin("deu", "5 Reichsmark (1935-1939)", 13.889, 0.900)
        add_coin("deu", "5 Deutschmark (1951-1974)", 11.2, 0.625)

        # --- SWITZERLAND JUNK ---
        add_coin("che", "1/2 Franc (1875-1967)", 2.5, 0.835)
        add_coin("che", "1 Franc (1875-1967)", 5.0, 0.835)
        add_coin("che", "2 Franc (1875-1967)", 10.0, 0.835)
        add_coin("che", "5 Franc (1931-1967)", 15.0, 0.835)

    else:
        # Error state for all lists if spot is 0
        err = {"name": "Calculation Failed", "weight_g": 0, "price_str": "Error", "is_spot": False}
        for k in categories:
            categories[k].append(err)

    return {"spot": spot_results, **categories}

# --- TRACKER LOGIC ---

def render_table():
    """Refreshes the Treeview from APP_STATE['last_data']."""
    data = APP_STATE['last_data']
    if not data:
        return

    # Clear current
    for item in tree.get_children():
        tree.delete(item)

    show_oz = APP_STATE['show_in_oz']

    def insert_rows(rows):
        for row in rows:
            if row["weight_g"] == 0:
                w_str = "-"
            elif show_oz:
                w_val = row["weight_g"] / CONST_GRAMS_PER_OZ
                w_str = f"{w_val:.3f} oz"
            else:
                w_str = f"{row['weight_g']} g"

            p_str = row['price_str']
            tags = []
            if "Error" in p_str or "Blocked" in p_str:
                tags.append("error")
            elif row.get("is_spot"):
                tags.append("spot_row")

            tree.insert("", "end", values=(row['name'], w_str, p_str), tags=tuple(tags))
    
    def insert_header(title):
        tree.insert("", "end", values=(f"--- {title} ---", "", ""), tags=('category',))

    # Render Order
    insert_rows(data['spot'])
    
    insert_header("US JUNK SILVER")
    insert_rows(data['us'])

    insert_header("CANADIAN JUNK SILVER")
    insert_rows(data['cad'])
    
    insert_header("UK JUNK SILVER")
    insert_rows(data['uk'])

    insert_header("AUSTRALIAN JUNK SILVER")
    insert_rows(data['aus'])
    
    insert_header("MEXICAN JUNK SILVER")
    insert_rows(data['mex'])
    
    insert_header("PORTUGUESE JUNK SILVER")
    insert_rows(data['prt'])
    
    insert_header("SPANISH JUNK SILVER")
    insert_rows(data['esp'])
    
    insert_header("FRENCH JUNK SILVER")
    insert_rows(data['fra'])
    
    insert_header("ITALIAN JUNK SILVER")
    insert_rows(data['ita'])
    
    insert_header("GERMAN JUNK SILVER")
    insert_rows(data['deu'])
    
    insert_header("SWISS JUNK SILVER")
    insert_rows(data['che'])

    weight_header = "Weight (Troy Oz) ▼" if show_oz else "Weight (Grams) ▼"
    tree.heading("weight", text=weight_header)
    
    update_calculator_spot_display()

def toggle_units():
    """Switches between grams and ounces and re-renders instantly."""
    if not APP_STATE['last_data']:
        return
    APP_STATE['show_in_oz'] = not APP_STATE['show_in_oz']
    render_table()

def start_refresh_thread():
    """Starts the background scraping."""
    if APP_STATE["is_fetching"]:
        return

    APP_STATE["is_fetching"] = True
    refresh_btn.config(text="Refreshing...", state="disabled")
    status_lbl.config(text="Status: Fetching latest prices...", bootstyle="warning")

    def task():
        new_data = get_all_data()
        
        def update_ui():
            APP_STATE['last_data'] = new_data
            render_table()
            APP_STATE["is_fetching"] = False
            refresh_btn.config(text="↻ Refresh Now", state="normal")
            
            t = time.strftime("%H:%M:%S")
            status_lbl.config(text=f"Status: Updated at {t}", bootstyle="success")

            if APP_STATE["auto_refresh"]:
                root.after(60000, start_refresh_thread)

        root.after(0, update_ui)

    threading.Thread(target=task, daemon=True).start()

def toggle_auto_refresh():
    is_on = auto_refresh_var.get()
    APP_STATE["auto_refresh"] = is_on
    if is_on:
        status_lbl.config(text="Status: Auto-Refresh Started...", bootstyle="info")
        if not APP_STATE["is_fetching"]:
            start_refresh_thread()
    else:
        status_lbl.config(text="Status: Auto-Refresh Stopped", bootstyle="secondary")

# --- CALCULATOR LOGIC ---

def update_calculator_spot_display():
    if APP_STATE['last_data']:
        for item in APP_STATE['last_data']['spot']:
            if item['name'] == "Silver":
                calc_spot_lbl.config(text=f"Live Silver Spot: {item['price_str']}")
                return
    calc_spot_lbl.config(text="Live Silver Spot: -- (Run Refresh)")

def perform_calculation():
    try:
        weight = float(calc_weight_entry.get())
        unit = calc_unit_var.get()
        purity_raw = float(calc_purity_entry.get())
        
        if purity_raw > 1.0:
            if purity_raw > 100:
                purity = purity_raw / 1000.0
            else:
                purity = purity_raw / 100.0
        else:
            purity = purity_raw

        spot_price = 0.0
        if APP_STATE['last_data']:
            for item in APP_STATE['last_data']['spot']:
                if item['name'] == "Silver":
                    spot_price = clean_price_text(item['price_str'])
                    break
        
        if spot_price == 0:
            calc_result_lbl.config(text="Error: No Spot Price", bootstyle="danger")
            return

        if unit == "Troy Oz":
            weight_in_grams = weight * CONST_GRAMS_PER_OZ
        else:
            weight_in_grams = weight

        pure_silver_grams = weight_in_grams * purity
        value = (pure_silver_grams / CONST_GRAMS_PER_OZ) * spot_price

        calc_result_lbl.config(text=f"${value:,.2f} USD", bootstyle="success")
        calc_details_lbl.config(text=f"Contains {pure_silver_grams:.2f}g ({pure_silver_grams/CONST_GRAMS_PER_OZ:.3f} oz) Pure Silver")

    except ValueError:
        calc_result_lbl.config(text="Invalid Input", bootstyle="danger")
        calc_details_lbl.config(text="Check numbers")


# --- GUI SETUP ---
root = ttk.Window(themename="darkly") 
root.title("Metal & Coin Tracker Pro")
root.geometry("900x850")

# Header
header_frame = ttk.Frame(root, padding=20)
header_frame.pack(fill=X)
title_lbl = ttk.Label(header_frame, text="Precious Metals Manager", font=("Segoe UI", 20, "bold"), bootstyle="inverse-primary")
title_lbl.pack(side=LEFT)

# Notebook
notebook = ttk.Notebook(root, bootstyle="primary")
notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

# ================= TAB 1: TRACKER =================
tab_tracker = ttk.Frame(notebook)
notebook.add(tab_tracker, text="  Market Tracker  ")

control_frame = ttk.Frame(tab_tracker, padding=(10, 10, 10, 10))
control_frame.pack(fill=X)

refresh_btn = ttk.Button(control_frame, text="↻ Refresh Now", command=start_refresh_thread, bootstyle="primary-outline", width=15)
refresh_btn.pack(side=LEFT, padx=(0, 15))

auto_refresh_var = ttk.BooleanVar(value=False)
auto_switch = ttk.Checkbutton(control_frame, text="Auto-Refresh (60s)", variable=auto_refresh_var, command=toggle_auto_refresh, bootstyle="success-round-toggle")
auto_switch.pack(side=LEFT)

status_lbl = ttk.Label(control_frame, text="Status: Ready", font=("Segoe UI", 9), bootstyle="secondary")
status_lbl.pack(side=RIGHT)

tree_frame = ttk.Frame(tab_tracker, padding=10)
tree_frame.pack(fill=BOTH, expand=True)

scroll = ttk.Scrollbar(tree_frame, bootstyle="primary-round")
scroll.pack(side=RIGHT, fill=Y)

columns = ("metal", "weight", "price")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=scroll.set, bootstyle="primary")
scroll.config(command=tree.yview)

tree.heading("metal", text="Item Description", anchor=W)
tree.heading("weight", text="Weight (Grams) ▼", anchor=CENTER, command=toggle_units) 
tree.heading("price", text="Current Value", anchor=CENTER)

tree.column("metal", width=350, anchor=W)
tree.column("weight", width=150, anchor=CENTER)
tree.column("price", width=150, anchor=CENTER)

tree.tag_configure('error', foreground='#ff4d4d')
tree.tag_configure('spot_row', background='#303030', font=("Segoe UI", 10, "bold"))
tree.tag_configure('category', background='#444444', foreground='#ffffff', font=("Segoe UI", 9, "italic", "bold"))

tree.pack(fill=BOTH, expand=True)

hint_lbl = ttk.Label(tab_tracker, text="💡 Tip: Click 'Weight' header to toggle Grams/Oz.", font=("Segoe UI", 8), bootstyle="secondary")
hint_lbl.pack(pady=5)

# ================= TAB 2: MELT CALCULATOR =================
tab_calc = ttk.Frame(notebook, padding=20)
notebook.add(tab_calc, text="  Melt Calculator  ")

calc_header = ttk.Label(tab_calc, text="Silver Melt Value Calculator", font=("Segoe UI", 16, "bold"))
calc_header.pack(pady=(0, 20))

calc_spot_lbl = ttk.Label(tab_calc, text="Live Silver Spot: -- (Run Refresh)", font=("Segoe UI", 12), bootstyle="warning")
calc_spot_lbl.pack(pady=(0, 20))

inputs_frame = ttk.Labelframe(tab_calc, text="Item Details", padding=20, bootstyle="info")
inputs_frame.pack(fill=X)
inputs_frame.columnconfigure(1, weight=1)

ttk.Label(inputs_frame, text="Weight:").grid(row=0, column=0, sticky=E, padx=5, pady=5)
calc_weight_entry = ttk.Entry(inputs_frame)
calc_weight_entry.grid(row=0, column=1, sticky=EW, padx=5, pady=5)
calc_weight_entry.insert(0, "1")

calc_unit_var = ttk.StringVar(value="Grams")
unit_combo = ttk.Combobox(inputs_frame, textvariable=calc_unit_var, values=["Grams", "Troy Oz"], state="readonly", width=10)
unit_combo.grid(row=0, column=2, padx=5, pady=5)

ttk.Label(inputs_frame, text="Purity:").grid(row=1, column=0, sticky=E, padx=5, pady=5)
calc_purity_entry = ttk.Entry(inputs_frame)
calc_purity_entry.grid(row=1, column=1, sticky=EW, padx=5, pady=5)
calc_purity_entry.insert(0, "925")
ttk.Label(inputs_frame, text="(e.g. 925, .999)").grid(row=1, column=2, sticky=W, padx=5)

calc_btn = ttk.Button(inputs_frame, text="Calculate Value", command=perform_calculation, bootstyle="success")
calc_btn.grid(row=2, column=0, columnspan=3, pady=(15, 0), sticky=EW)

results_frame = ttk.Frame(tab_calc, padding=20)
results_frame.pack(fill=X, pady=10)

calc_result_lbl = ttk.Label(results_frame, text="$0.00 USD", font=("Segoe UI", 24, "bold"), bootstyle="success", anchor=CENTER)
calc_result_lbl.pack()
calc_details_lbl = ttk.Label(results_frame, text="Waiting for input...", font=("Segoe UI", 10), bootstyle="secondary", anchor=CENTER)
calc_details_lbl.pack()

info_frame = ttk.Labelframe(tab_calc, text="Silverware Identification Guide", padding=15, bootstyle="primary")
info_frame.pack(fill=BOTH, expand=True, pady=10)

info_text = """
HOW TO SPOT REAL SILVER (STERLING) vs PLATE:

✅ REAL SILVER (STERLING)
• LOOK FOR MARKS: "925", "Sterling", "Ster", ".925".
• BRITISH MARKS: A "Lion Passant" (walking lion) symbol guarantees Sterling.
• COLOR: Has a warm, soft white luster. Tarnishes black/grey.
• MAGNET TEST: Silver is NON-magnetic. If it sticks, it's not silver.

❌ SILVER PLATE (LOW VALUE)
• LOOK FOR MARKS: 
  - "EPNS" (Electro Plated Nickel Silver)
  - "EP" (Electro Plated)
  - "A1", "AA", "Triple Plate", "Quadruple Plate"
  - "IS" (International Silver - usually plated unless marked Sterling)
• COLOR: If worn, you may see "brassy" or copper colors showing through.
"""
info_lbl = ttk.Label(info_frame, text=info_text, justify=LEFT, font=("Consolas", 10))
info_lbl.pack(anchor=W)

root.after(1000, start_refresh_thread)
root.mainloop()