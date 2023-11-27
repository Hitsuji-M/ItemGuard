import streamlit as st
import requests

api_url = "http://api:5000"

def main():
    st.title("Application Streamlit avec Authentification")
    st.session_state.setdefault('is_authenticated', False)

    # Page de connexion
    if not st.session_state.is_authenticated:
        st.header("Connexion")

        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")

        if st.button("Se connecter"):
            # Faire la requête d'authentification à votre API FastAPI
            response = requests.post(
                f"{api_url}/auth",
                data={"grant_type":"password","username": username, "password": password}
            )

            if response.status_code == 200:
                st.session_state.is_authenticated = True
                st.success("Connexion réussie! Vous pouvez accéder au reste de l'application.")
            else:
                print(response.reason)
                st.error("Échec de la connexion. Veuillez vérifier vos informations d'identification.")

    
    
            st.header("Bienvenue dans l'application")

            if st.button("Récupérer les données depuis FastAPI"):
                # Faire la requête pour récupérer les données
                response = requests.get(f"{api_url}/log/last")
                
                if response.status_code == 200:
                    data = response.json()
                    st.write("Name: ")
                    st.write(data)
                else:
                    st.error("Échec de la récupération des données depuis FastAPI.")

if __name__ == '__main__':
    main()
