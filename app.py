import streamlit as st

# --- NASTAVENÍ STRÁNKY ---
st.set_page_config(page_title="Páji to-do list", page_icon="🌸")

# --- FUNKCE PRO NAČÍTÁNÍ A UKLÁDÁNÍ ---
def nacti_ukoly():
    ukoly = []
    try:
        with open("todo.txt", "r", encoding="utf-8") as soubor:
            for radek in soubor:
                radek = radek.strip()
                if radek:
                    casti = radek.split(";")
                    if len(casti) == 2:
                        ukoly.append([casti[0], casti[1] == "1"])
    except FileNotFoundError:
        pass
    return ukoly

def uloz_ukoly(ukoly):
    with open("todo.txt", "w", encoding="utf-8") as soubor:
        for ukol in ukoly:
            hotovo = "1" if ukol[1] else "0"
            soubor.write(f"{ukol[0]};{hotovo}\n")

# --- CUSTOM CSS (Vylepšené zarovnání a křížek) ---
st.markdown("""
<style>
    .stApp {
        background-color: #ffcccc;
    }
    /* Všechno písmo bude černé */
    html, body, [class*="css"], p, h1, h2, h3, label, input {
        color: #000000 !important;
    }
    /* Zarovnání textu úkolu na střed řádku */
    .stWrite {
        line-height: 2.5rem;
    }

    /* Styl pro kulaté tlačítko s křížkem */
    button[key^="del"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border-radius: 50% !important;
        width: 30px !important;
        height: 30px !important;
        padding: 0 !important;
        line-height: 0 !important;
        border: 2px solid #ff69b4 !important;
        color: #ff69b4 !important;
        background-color: white !important;
    }
    
    button[key^="del"]:hover {
        background-color: #ff69b4 !important;
        color: white !important;
    }

    /* Schování nápisu u checkboxu pro lepší zarovnání */
    .stCheckbox {
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

if "ukoly" not in st.session_state:
    st.session_state.ukoly = nacti_ukoly()

st.title("💖 TO-DO list")

# --- FORMULÁŘ PRO ENTER ---
with st.form("muj_formular", clear_on_submit=True):
    novy = st.text_input("Zadej nový úkol", placeholder="...")
    tlacitko = st.form_submit_button("Přidat ✨")
    
    if tlacitko and novy.strip():
        st.session_state.ukoly.append([novy.strip(), False])
        uloz_ukoly(st.session_state.ukoly)
        st.rerun()
    }
    
st.subheader("Seznam úkolů")

if not st.session_state.ukoly:
    st.info("Zatím žádné úkoly.")
else:
    for i, ukol in enumerate(st.session_state.ukoly):
        # Poměr sloupců upravený pro lepší vzhled
        c1, c2, c3 = st.columns([0.5, 8, 1])

        with c1:
            # Checkbox
            checked = st.checkbox("", value=ukol[1], key=f"check_{i}")
            if checked != ukol[1]:
                st.session_state.ukoly[i][1] = checked
                uloz_ukoly(st.session_state.ukoly)
                st.rerun()
            
        with c2:
            # Text úkolu - pokud je hotovo, přeškrtneme ho
            if ukol[1]:
                st.markdown(f"<p style='text-decoration: line-through; color: gray; padding-top: 5px;'>{ukol[0]}</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p style='padding-top: 5px; font-weight: 500;'>{ukol[0]}</p>", unsafe_allow_html=True)

        with c3:
            # Smazací tlačítko
            if st.button("❌", key=f"del_{i}"):
                st.session_state.ukoly.pop(i)
                uloz_ukoly(st.session_state.ukoly)
                st.rerun()
