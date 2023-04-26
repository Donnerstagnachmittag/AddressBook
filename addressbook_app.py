import streamlit as st
import pandas as pd
from geocode import get_coordinates
from jsonbin import load_key, save_key
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# -------- load secrets for jsonbin.io --------
jsonbin_secrets = st.secrets["jsonbin"]
api_key = jsonbin_secrets["api_key"]
bin_id = jsonbin_secrets["bin_id"]

# -------- user login --------
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

fullname, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == True:   # login successful
    authenticator.logout('Logout', 'main')   # show logout button
elif authentication_status == False:
    st.error('Username/password is incorrect')
    st.stop()
elif authentication_status == None:
    st.warning('Please enter your username and password')
    st.stop()

# --------- sidebar ---------
# Sidebar zum Hinzufügen neuer Adressen
st.sidebar.header("Neue Adresse hinzufügen")
name = st.sidebar.text_input("Name")
street = st.sidebar.text_input("Straße")
city = st.sidebar.text_input("Stadt")
submit = st.sidebar.button("Adresse hinzufügen")
delete = st.sidebar.button("Lezter Eintrag löschen")

# -------- main app --------

# Titel der App
st.title(f"Adressbuch von {fullname}")

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
    address_list = load_key(api_key, bin_id, username)
    address_list.append(new_address)
    res = save_key(api_key, bin_id, username, address_list)
    if 'message' in res:
        st.error(res['message'])

# Löschen der letzten Adresse
if delete:
    # delete last entry
    address_list = load_key(api_key, bin_id, username)
    address_list.pop()
    res = save_key(api_key, bin_id, username, address_list)
    if 'message' in res:
        st.error(res['message'])

# Darstellung der Adressliste als Tabelle mit Karte
address_list = load_key(api_key, bin_id, username)
df = pd.DataFrame(address_list)
st.table(df)
st.map(df.dropna())
