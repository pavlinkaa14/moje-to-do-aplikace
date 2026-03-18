import streamlit as st

# --- NASTAVENÍ STRÁNKY (Ikona a název v tabu prohlížeče) ---
st.set_page_config(page_title="Pájův Růžový Seznam", page_icon="📝")

# --- FUNKCE PRO NAČÍTÁNÍ A UKLÁDÁNÍ (Tohle je tvůj původní kód) ---
def nacti_ukoly():
    ukoly = []
    try:
        with open("todo.txt", "r", encoding="utf-8") as soubor:
            for radek in soubor:
                radek = radek.strip()
                if radek:
                    casti = radek.split(";")
                    if len(casti) != 2:
                        continue
                    nazev = casti[0]
                    hotovo = casti[1] == "1"
                    ukoly.append([nazev, hotovo])
    except FileNotFoundError:
        pass
    return ukoly

def uloz_ukoly(ukoly):
    with open("todo.txt", "w", encoding="utf-8") as soubor:
        for ukol in ukoly:
            nazev = ukol[0]
            hotovo = "1" if ukol[1] else "0"
            soubor.write(f"{nazev};{hotovo}\n")

# --- CUSTOM CSS (Magie pro růžové pozadí a fonty) ---
# Tady si můžeš změnit barvy: lightpink, ffcccc, darkmagenta...
# Font: 'Poppins' nebo 'Montserrat' (pokud bys chtěl kulatější)
st.markdown("""
<style>
    /* 1. Růžové pozadí celé stránky */
    .stApp {
        background-color: #ffcccc; /* Světle růžová (zkus #ffb6c1 nebo #ff69b4 pro sytější) */
        color: #333; /* Barva textu */
    }

    /* 2. Stylové písmo (Kulatější a čistší) */
    html, body, [class*="css"]  {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
    }

    /* 3. Styly pro hlavní nadpis */
    .stTitle {
        color: #db2777; /* Tmavě růžová pro nadpis */
        text-shadow: 2px 2px 4px #ffb6c1; /* Jemný stín */
    }

    /* 4. Styly pro tlačítko "Přidat" */
    .stButton>button {
        background-color: transparent;
        color: #db2777; /* Růžový text tlačítka */
        border: 2px solid #db2777; /* Růžové orámování */
        border-radius: 20px; /* Kulaté rohy */
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #db2777; /* Po najetí myší se vyplní růžově */
        color: white; /* Text zbělá */
        border-color: #db2777;
    }

    /* 5. Styly pro smazací tlačítko (Křížek) */
    .stButton>button[key^="del"] {
        border-radius: 50%; /* Úplně kulatý křížek */
        border: none;
        background-color: #ff69b4; /* Sytá růžová pro smazání */
        color: white;
    }
    .stButton>button[key^="del"]:hover {
        background-color: #db2777; /* Po najetí myší ztmavne */
    }

    /* 6. Vzhled pro checkbox */
    .stCheckbox label {
        color: #333; /* Barva textu u checkboxu */
        font-size: 18px; /* Trochu větší písmo */
    }
    /* Přeškrtnutý text pro hotový úkol */
    .stCheckbox label[class*="css"] {
        text-decoration: line-through; 
    }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZACE SESSION STATE ---
if "ukoly" not in st.session_state:
    st.session_state.ukoly = nacti_ukoly()

# --- HLAVNÍ ČÁST APLIKACE ---
st.title("💖 Můj TO-DO list")

# Přidání úkolu
novy = st.text_input("Zadej nový úkol", placeholder="Např. Koupit donut 🍩")

if st.button("Přidat ✨"):
    if novy.strip():
        # Přidáme nový úkol, false = není hotový
        st.session_state.ukoly.append([novy.strip(), False])
        uloz_ukoly(st.session_state.ukoly)
        # Smažeme input (tohle je malý hack)
        st.rerun()

# Seznam úkolů
st.subheader("Seznam úkolů")

if not st.session_state.ukoly:
    st.info("Zatím nemáš žádné úkoly! Přidej si nějaký. 🎉")
else:
    for i, ukol in enumerate(st.session_state.ukoly):
        # Uděláme si hezčí rozložení: checkbox (vlevo), text úkolu, smazání (vpravo)
        col1, col2 = st.columns([1, 12, 1]) # Větší mezera pro smazání, ať to nelítá

        with col1:
            # Checkbox bez textu
            checked = st.checkbox("", value=ukol[1], key=f"check_{i}")
            # Aktualizujeme state, pokud se změní
            st.session_state.ukoly[i][1] = checked
            
        with col2:
            # Zobrazíme text (a přeškrtneme ho, pokud je hotovo)
            text_styl = f"~~{ukol[0]}~~" if ukol[1] else ukol[0]
            st.write(text_styl, unsafe_allow_html=True)

        with col3:
            # Smazací tlačítko (Křížek)
            if st.button("❌", key=f"del_{i}"):
                st.session_state.ukoly.pop(i)
                uloz_ukoly(st.session_state.ukoly)
                st.rerun()

    # Automaticky uložíme po každém renderu (pro jistotu při změně checkboxů)
    uloz_ukoly(st.session_state.ukoly)
