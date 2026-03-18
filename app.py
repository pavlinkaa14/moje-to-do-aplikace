import streamlit as st

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

# uloží data mezi refreshi
if "ukoly" not in st.session_state:
    st.session_state.ukoly = nacti_ukoly()

st.title("📝 Můj TO-DO list")

# přidání úkolu
novy = st.text_input("Zadej nový úkol")

if st.button("Přidat"):
    if novy.strip():
        st.session_state.ukoly.append([novy, False])
        uloz_ukoly(st.session_state.ukoly)

# seznam
st.subheader("Seznam úkolů")

for i, ukol in enumerate(st.session_state.ukoly):
    col1, col2 = st.columns([4,1])

    with col1:
        checked = st.checkbox(ukol[0], value=ukol[1], key=i)
        st.session_state.ukoly[i][1] = checked

    with col2:
        if st.button("❌", key=f"del{i}"):
            st.session_state.ukoly.pop(i)
            uloz_ukoly(st.session_state.ukoly)
            st.rerun()

uloz_ukoly(st.session_state.ukoly)