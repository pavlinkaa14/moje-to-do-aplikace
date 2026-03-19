import streamlit as st

# --- NASTAVENÍ STRÁNKY ---
st.set_page_config(page_title="Pájův Růžový Seznam", page_icon="🌸")

# --- CUSTOM CSS (Vzhled zůstává stejný) ---
st.markdown("""
<style>
    .stApp {
        background-color: #ffcccc;
    }
    /* Všechno písmo černé */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, label, input {
        color: #db2777 !important;
    }

    /* TLAČÍTKO PŘIDAT - BÍLÝ TEXT */
    .stButton>button {
        background-color: #ff69b4 !important;
        color: #ffffff !important;
        border-radius: 20px !important;
        border: none !important;
    }
    
    .stButton>button p {
        color: #ffffff !important;
    }

    /* KULATÝ KŘÍŽEK */
    button[key^="del"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border-radius: 50% !important;
        width: 28px !important;
        height: 28px !important;
        padding: 0 !important;
        border: 2px solid #ff1493 !important;
        color: #ff1493 !important;
        background-color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# --- PAMĚŤ PROHLÍŽEČE ---
# Tady se vytvoří prázdný seznam pro každého uživatele zvlášť
if "ukoly" not in st.session_state:
    st.session_state.ukoly = []

st.title("💖 Můj TO-DO list")

# --- FORMULÁŘ PRO PŘIDÁVÁNÍ ---
with st.form("muj_formular", clear_on_submit=True):
    novy = st.text_input("Zadej nový úkol", placeholder="Napiš sem něco... ✍️")
    submit = st.form_submit_button("Přidat úkol ✨")
    
    if submit and novy.strip():
        # Přidá úkol jen do paměti aktuálního uživatele
        st.session_state.ukoly.append([novy.strip(), False])
        st.rerun()

st.subheader("Seznam úkolů", anchor=False) # Schovali jsme tu kotvu/řetěz

if not st.session_state.ukoly:
    st.write("Tvůj seznam je prázdný. Naplánuj si něco! ✨")
else:
    for i, ukol in enumerate(st.session_state.ukoly):
        c1, c2, c3 = st.columns([0.6, 8, 1])

        with c1:
            # Checkbox změní stav jen v tomto prohlížeči
            checked = st.checkbox("", value=ukol[1], key=f"check_{i}")
            st.session_state.ukoly[i][1] = checked
            
        with c2:
            if ukol[1]:
                st.markdown(f"<p style='text-decoration: line-through; color: #555555; padding-top: 5px; margin:0;'>{ukol[0]}</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p style='color: #000000; padding-top: 5px; margin:0; font-weight: 500;'>{ukol[0]}</p>", unsafe_allow_html=True)

        with c3:
            if st.button("×", key=f"del_{i}"):
                st.session_state.ukoly.pop(i)
                st.rerun()
