import streamlit as st

# Liste des groupes d'utilisateurs avec leurs mots de passe et leurs jeux de données respectifs
user_credentials = {
    "Admin": {"password": "admin123", "datasets": ["Prénoms des enfants nés à Nantes", "Lieux Pratiques Numériques", "Stations Marguerite de Nantes Métropole - Tarifs", "Parcs relais de Nantes Métropole - Statistiques d'occupation", "Déchèteries-écopoints de Nantes Métropole - Tonnages", "Déchèteries-écopoints de Nantes Métropole - Fréquentations"]},
    "Collectivité": {"password": "collect123", "datasets": ["Prénoms des enfants nés à Nantes", "Lieux Pratiques Numériques"]},
    "Déplacement": {"password": "deplacement123", "datasets": ["Stations Marguerite de Nantes Métropole - Tarifs", "Parcs relais de Nantes Métropole - Statistiques d'occupation"]},
    "Direction Déchêts": {"password": "dechets123", "datasets": ["Déchèteries-écopoints de Nantes Métropole - Tonnages", "Déchèteries-écopoints de Nantes Métropole - Fréquentations"]}
}

# Fonction pour l'authentification
def authenticate_user():
    st.title("Application de Mise à Jour des Jeux de Données")
    
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if username in user_credentials and password == user_credentials[username]["password"]:
            st.success("Connexion réussie en tant que {}".format(username))
            return username
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect")
    
    return None

# Fonction pour la sélection du jeu de données
def select_dataset(username):
    st.subheader("Sélectionnez le jeu de données à mettre à jour :")
    datasets = user_credentials[username]["datasets"]
    selected_dataset = st.selectbox("Jeu de données", datasets)
    return selected_dataset

# Fonction pour charger le fichier de mise à jour
def upload_file():
    uploaded_file = st.file_uploader("Charger le fichier de mise à jour", type=["csv", "xlsx"])
    return uploaded_file

# Fonction pour exécuter le traitement
def execute_processing():
    if st.button("Exécuter le traitement"):
        # Ici, vous ajouteriez la logique de traitement des données
        st.success("Traitement exécuté avec succès")

# Fonction pour afficher l'historique
def show_history(username):
    st.subheader("Historique des traitements pour {}".format(username))
    # Ajoutez ici la logique pour afficher l'historique, par exemple :
    st.write("Aucun traitement effectué jusqu'à présent.")

# Fonction principale de l'application
# Fonction principale de l'application
def main():
    username = authenticate_user()

    if username:
        st.sidebar.title("Menu")
        menu_selection = st.sidebar.radio("Choisissez une option", ["Accueil", "Traitement"])

        if menu_selection == "Accueil":
            show_history(username)
        elif menu_selection == "Traitement":
            if username == "Admin":
                selected_dataset = select_dataset(username)
                if selected_dataset:
                    uploaded_file = upload_file()
                    if uploaded_file:
                        execute_processing()
            else:
                st.warning("Vous n'avez pas la permission d'accéder à cette fonctionnalité.")


# Exécution de l'application
if __name__ == "__main__":
    main()
