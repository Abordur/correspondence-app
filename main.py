# ✅ Code mis à jour le 5 juin 15h21 pour corriger erreur Streamlit Cloud
import streamlit as st
import pandas as pd    #Biblio pour manip les fichiers excel
from supabase import create_client, Client 
 

@st.cache_data #Permet à Streamlit de ne pas recharger les fichiers Excel à chaque fois
def load_data(): #fonction qui va charger et retourner tous les fichiers Excel en un seul DataFrame.
    url = "https://pkfzbsfjcrjtkbrtqiis.supabase.co" # URL Supabase et la clé publique (anon) ->
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBrZnpic2ZqY3JqdGticnRxaWlzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg0MTg0NzcsImV4cCI6MjA2Mzk5NDQ3N30.YGR7YBD0LrljuXVtBf427ug92jtHuqBFUAxhK_fZv7Q"  
    supabase: Client = create_client(url, key)  # Crée le client Supabase
    response = supabase.table("Correspondence").select("*").execute()  # Change "Correspondence" si le tableau a un autre nom
    data = response.data  # Données brutes (liste de dictionnaires)
    df = pd.DataFrame(data)  # Transforme en DataFrame
    return df


df = load_data()

# Interface Streamlit
st.title("Correspondence table")
st.markdown("Choisissez une méthode pour retrouver le nouveau lien Microsoft " \
"SharePoint à partir d’un lien Google Drive, " \
"d’un nom de fichier ou d’un ID.", unsafe_allow_html=True)

# Initialiser les états
if "mode_selection" not in st.session_state:
    st.session_state.mode_selection = None
if "user_input" not in st.session_state:
    st.session_state.user_input = ""


# Fonction pour gérer le clic sur un bouton
def select_mode(mode):
    st.session_state.mode_selection = mode
    st.session_state.user_input = ""  # Reset à chaque changement

# Les 3 boutons de choix
col1, col2, col3 = st.columns(3)
with col1:
    st.button("Name File", on_click=select_mode, args=("name",))
with col2:
    st.button("Link File", on_click=select_mode, args=("link",))
with col3:
    st.button("ID File", on_click=select_mode, args=("id",))

# Saisie utilisateur
user_input = None
if st.session_state.mode_selection == "name":
    user_input = st.text_input("Entrez le **nom** du fichier :", key="user_input")
    column_to_search = "FileName"
elif st.session_state.mode_selection == "link":
    user_input = st.text_input("Entrez le **lien Google Drive** du fichier :", key="user_input")
    column_to_search = "PathGoogle"
elif st.session_state.mode_selection == "id":
    user_input = st.text_input("Entrez l’**ID du lien** Google Drive :", key="user_input")
    column_to_search = "FileID"

# Traitement après saisie
if user_input and user_input.strip() != "": # Si il y a une valeur dans le champ alors:

    if st.button("Convertir"): # Bouton Convertir apparaît

        matches = df[df[column_to_search] == user_input.strip()] # Elle cherche dans le fichier 
            # Excel (df) toutes les lignes où la colonne column_to_search contient exactement ce 
            # que l'utilisateur a tapé (user_input.strip()).

        if not matches.empty: # Si matches à une valeur alors:
            row = matches.iloc[0] # Récupère la première ligne de la colonne 
            link = row["LinkSharepoint"]
            path = row["PathSharepoint"]
            st.markdown(f"**Lien Microsoft :** <a href='{link}'>{link}</a>", unsafe_allow_html=True)
            st.markdown(f"**Chemin SharePoint :** `{path}`")
        else:
            st.error("Aucun fichier correspondant trouvé dans la base.")




#La commande pour lancer l'app c'est streamlit run main.py