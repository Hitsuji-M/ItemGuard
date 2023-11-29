import streamlit as st
import requests
from datetime import datetime as dt


api_url = "http://api:5000"
token = None


if "page" not in st.session_state:
    st.session_state.page = 0

def nextpage(): 
    st.session_state.page += 1

def restart(): 
    st.session_state.page = 0

def login_page():
    global token
    token = None
    st.header("Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        # Faire la requête d'authentification à votre API FastAPI
        response = requests.post(
            f"{api_url}/auth",
            data={"grant_type": "password", "username": username, "password": password}
        )

        if response.status_code == 200:
            st.session_state.is_authenticated = True
            token = response.json().get("access_token")
            st.success("Connexion réussie! Vous pouvez accéder au reste de l'application.")
            st.write(token)
            nextpage()
            st.rerun()
    


def main_page(token):
    st.title("ItemGuard")   
    st.sidebar.header("Navigation")
    
    # Onglets
    selected_tab = st.sidebar.radio("Choisissez une action", ["Toutes les produits", "Créer", "Supprimer", "Mettre à jour", "Logs","Profil"])

    if selected_tab == "Tous les produits":
        all_product(token)
    elif selected_tab == "Créer":
        create(token)
    elif selected_tab == "Supprimer":
        delete_product(token)
    elif selected_tab == "Mettre à jour":
        update_product(token)
    elif selected_tab == "Logs":
        show_logs()
    elif selected_tab == "Profil":
        profil()    


def all_product(token):
    if st.button("Récupérer les données depuis FastAPI"):
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{api_url}/products", headers=headers)
        if response.status_code == 200:
            data = response.json()
            st.write("Produits: ")
            st.write(data)
        else:
            st.error("Échec de la récupération des données depuis FastAPI.")


def create(token):
    st.header("Create")

    with st.form("create_product_form"):
        product_name = st.text_input("Nom du produit", key="product_name")
        product_price = st.number_input("Prix du produit", key="product_price")

        submit_button = st.form_submit_button("Submit")

    if submit_button:
        product_data = {"name": product_name, "price": product_price}
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{api_url}/product", headers=headers, json=product_data)

        if response.status_code == 200:
            st.success("Produit créé avec succès!")
            all_product(token)
        else:
            st.error("Échec de la création du produit.")


def delete_product(token):
    st.header("Delete Product")

    # Récupérer la liste des produits
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{api_url}/products", headers=headers)
    
    if response.status_code == 200:
        product_data = response.json()

        # Liste déroulante pour choisir quel élément supprimer
        selected_product_name = st.selectbox("Choisir un produit à supprimer", [product["name"] for product in product_data])

        # Bouton pour supprimer le produit sélectionné
        if st.button("Supprimer"):
            selected_product_id = next((product["id"] for product in product_data if product["name"] == selected_product_name), None)
            if selected_product_id:
                response = requests.delete(f"{api_url}/product/{selected_product_id}", headers=headers)
                if response.status_code == 200:
                    st.success("Produit supprimé avec succès!")
                else:
                    st.error("Échec de la suppression du produit.")
            else:
                st.warning("Aucun produit sélectionné.")
    else:
        st.error("Échec de la récupération des produits depuis FastAPI.")



def update_product(token):
    st.header("Update Product")

    # Récupérer la liste des produits
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{api_url}/products", headers=headers)
    
    if response.status_code == 200:
        product_data = response.json()

        # Liste déroulante pour choisir quel élément mettre à jour
        selected_product_name = st.selectbox("Choisir un produit à mettre à jour", [product["name"] for product in product_data])

        # Récupérer l'ID du produit sélectionné
        selected_product_id = next((product["id"] for product in product_data if product["name"] == selected_product_name), None)

        if selected_product_id is not None:
            # Récupérer les données du produit depuis l'API
            response = requests.get(f"{api_url}/product/{selected_product_id}", headers=headers)

            if response.status_code == 200:
                product_data = response.json()

                # Formulaire pré-rempli avec les données du produit
                with st.form("update_product_form"):
                    product_name = st.text_input("Nom du produit", key="product_name", value=product_data["name"])
                    product_price = st.number_input("Prix du produit", key="product_price", value=product_data["price"])

                    submit_button = st.form_submit_button("Mettre à jour le produit")

                if submit_button:
                    updated_product_data = {"id": selected_product_id, "name": product_name, "price": product_price}
                    response = requests.put(f"{api_url}/product", headers=headers, json=updated_product_data)

                    if response.status_code == 200:
                        st.success("Produit mis à jour avec succès!")
                    else:
                        st.error("Échec de la mise à jour du produit.")
            else:
                st.error("Échec de la récupération du produit depuis FastAPI.")
        else:
            st.warning("Aucun produit sélectionné.")
    else:
        st.error("Échec de la récupération des produits depuis FastAPI.")



def show_logs():
    st.header("Logs")

    # Liste déroulante pour choisir l'action
    selected_action = st.selectbox("Choisir une action", ["Tous les logs", "Rechercher", "Logs limités", "Supprimer"])

    if selected_action == "Tous les logs":
        logs = get_all_logs()
        st.write(logs)
    elif selected_action == "Rechercher":
        limit = st.number_input("Limite", value=0)
        desc = st.checkbox("Tri décroissant", value=True)
        before = st.date_input("Avant", value=None)
        logs = search_logs(limit, desc, before)
        st.write(logs)
    elif selected_action == "Logs limités":
        limit = st.number_input("Limite", value=10)
        logs = get_logs_limit(limit)
        st.write(logs)
    elif selected_action == "Supprimer":
        log_id = st.number_input("ID du log à supprimer", value=0, min_value=0)
        if st.button("Supprimer"):
            result = delete_log(log_id)
            st.write(result)

def get_all_logs():
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{api_url}/logs", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Échec de la récupération de tous les logs depuis FastAPI. Code d'erreur : {response.status_code}"

def search_logs(limit: int, desc: bool, before: dt):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"limit": limit, "desc": desc, "before": before}
    response = requests.get(f"{api_url}/logs/search", headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Échec de la recherche de logs depuis FastAPI. Code d'erreur : {response.status_code}"

def get_logs_limit(limit: int):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{api_url}/logs/{limit}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Échec de la récupération de logs limités depuis FastAPI. Code d'erreur : {response.status_code}"

def delete_log(log_id: int):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{api_url}/log/{log_id}", headers=headers)
    if response.status_code == 200:
        return "Log supprimé avec succès!"
    else:
        return f"Échec de la suppression du log depuis FastAPI. Code d'erreur : {response.status_code}"


def profil():
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{api_url}/user/me", headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        st.write("User Profile: ")
        st.write(user_data)
    else:
        st.error(f"Échec de la récupération du profil utilisateur. Code d'erreur : {response.status_code}")


if __name__ == '__main__':
    if st.session_state.page == 0:
        login_page()
    else:
        if st.session_state.is_authenticated:
            main_page(token)












