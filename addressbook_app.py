import streamlit as st
import pandas as pd
from geocode import get_coordinates
from jsonbin import load_data, save_data

# Key und bin id laden
jsonbin_secrets = st.secrets["jsonbin"]

# Titel der App
st.title("Adressbuch App - Cloud Version")

# Sidebar zum Hinzufügen neuer Adressen
st.sidebar.header("Neue Adresse hinzufügen")
name = st.sidebar.text_input("Name")
street = st.sidebar.text_input("Straße")
city = st.sidebar.text_input("Stadt")
submit = st.sidebar.button("Adresse hinzufügen")
delete = st.sidebar.button("Lezter Eintrag löschen")

# Funktion zum Hinzufügen einer neuen Adresse zur Adressliste
if submit:
    address = f"{street}, {city}"
    latitude, longitude = get_coordinates(address)

    new_address = {
        "name": name,
        "street": street,
        "city": city,
        "latitude": latitude,
        "longitude": longitude
    }
    address_list = load_data(jsonbin_secrets["api_key"], jsonbin_secrets["bin_id"])
    address_list.append(new_address)
    res = save_data(jsonbin_secrets["api_key"], jsonbin_secrets["bin_id"], address_list)
    if 'message' in res:
        st.error(res['message'])

if delete:
    # delete last entry
    address_list = load_data(jsonbin_secrets["api_key"], jsonbin_secrets["bin_id"])
    address_list.pop()
    res = save_data(jsonbin_secrets["api_key"], jsonbin_secrets["bin_id"], address_list)
    if 'message' in res:
        st.error(res['message'])

# Darstellung der Adressliste als Tabelle
address_list = load_data(jsonbin_secrets["api_key"], jsonbin_secrets["bin_id"])
df = pd.DataFrame(address_list)
st.table(df)
st.map(df)
