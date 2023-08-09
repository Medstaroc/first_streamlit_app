import os
import requests
import streamlit as st
import pandas as pd
from streamlit_extras.dataframe_explorer import dataframe_explorer

# Page d'authentification
def login():
    st.title("Authentification")
    utilisateur = st.text_input("Nom d'utilisateur")
    mot_de_passe = st.text_input("Mot de passe", type="password")
    submit_button = st.button("Se connecter")
    
    if submit_button:
        # Vérifier les informations d'identification
        if utilisateur == st.secrets.NM_credentials.username and mot_de_passe == st.secrets.NM_credentials.password:
            st.session_state.authenticated = True
            st.success("Authentification réussie. Vous pouvez maintenant mettre à jour les jeux de données.")
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

# Fonction pour récupérer l'UID du jeu de données
def get_dataset_uid(dataset_id):
    response = requests.get(f'https://data.nantesmetropole.fr/api/v2/catalog/datasets?where=dataset_id%20%3D%20%22{dataset_id}%22', auth=(utilisateur, mot_de_passe))
    data = response.json()
    dataset_uid = data['datasets'][0]['dataset']['dataset_uid']
    return dataset_uid

# Fonction pour mettre à jour les jeux de données
def update_dataset(selected_dataset, df):
    # Code pour mettre à jour les jeux de données sur le portail de Nantes Métropole
    dataset_id = selected_dataset
    dataset_uid = get_dataset_uid(dataset_id)
    
    # Chargement du DataFrame dans un fichier CSV temporaire
    temp_file_path = "temp_update_file.csv"
    df.to_csv(temp_file_path, index=False)
    
    upload_url = "https://data.nantesmetropole.fr/api/management/v2/files"

    with open(temp_file_path, 'rb') as file:
        files = {'file': (temp_file_path, file.read())}
        response = requests.post(upload_url, files=files, auth=(utilisateur, mot_de_passe))
    data = response.json()
    url_res = data['url']
    
    url = f'https://data.nantesmetropole.fr/api/management/v2/datasets/{dataset_uid}/resources/'
    response = requests.get(url, auth=(utilisateur, mot_de_passe))
    data = response.json()
    resource_uid = data[0]["resource_uid"]
    
    url = f'https://data.nantesmetropole.fr/api/management/v2/datasets/{dataset_uid}/resources/{resource_uid}'
    payload = {
        "url": url_res,
        "title": "07082023_lieux_pratiques_numeriques",
        "type": "csvfile",
        "params": {
            "headers_first_row": True,
            "separator": ',',
            "encoding": "UTF8",
            "extract_filename": False,
            "first_row_no": 1,
            "escapechar": '\\',
            "doublequote": True
        }
    }
    response = requests.put(url, json=payload, auth=(utilisateur, mot_de_passe))
    
    url = f'https://data.nantesmetropole.fr/api/management/v2/datasets/{dataset_uid}/publish/'
    response = requests.put(url, auth=(utilisateur, mot_de_passe))
    
    # Suppression du fichier temporaire
    os.remove(temp_file_path)
    
    return response

# Page principale
def main():
    st.title("Mise à jour des Jeux de Données")

    # Vérifier si l'utilisateur est authentifié
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        login()
    else:
        st.write("Merci de sélectionner le JDD à mettre à jour :")
        dataset_options = [
            "244400404_lieux-pratiques-numeriques-nantes",
            "244400404_piscines-nantes-metropole-horaires",
            "244400404_nombre-annuel-naissances-nantes",
            "244400404_nombre-annuel-mariages-nantes",
            "244400404_nombre-annuel-deces-nantes"
        ]
        selected_dataset = st.selectbox("Sélectionner un jeu de données", dataset_options)

        if selected_dataset:
            st.write(f"Jeu de données sélectionné : {selected_dataset}")
            uploaded_file = st.file_uploader("Charger le fichier à jour", type=["csv"])

            if uploaded_file:
                st.write("Aperçu du fichier chargé :")
                df = pd.read_csv(uploaded_file)
                filtred_df = dataframe_explorer(df)
                st.dataframe(filtred_df, use_container_width =True)

                update_button = st.button("Mettre à jour le jeu de données")

                if update_button:
                    update_response = update_dataset(selected_dataset, df)

                    if update_response.status_code == 200:
                        st.success("Mise à jour réussie !")
                    else:
                        st.error("Une erreur est survenue lors de la mise à jour.")

if __name__ == "__main__":
    main()
