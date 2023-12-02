import streamlit as st
import requests
from datetime import datetime as dt
import re
import hashlib


api_url = "http://api:5000"


#Gestion des différentes pages
if "page" not in st.session_state:
    st.session_state.page = 0

def nextpage(): 
    st.session_state.page += 1

def restart(): 
    st.session_state.page = 0


#Page de connexion
def login_page() -> str:
    st.header("Connexion")
    username: str = st.text_input("Nom d'utilisateur")
    username = username.lower()
    password = st.text_input("Mot de passe", type="password")

    token = ""
    if st.button("Se connecter"):
        pattern = re.compile("([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
        if not pattern.match(username):
            st.error("Incorrect email format")
            return ""

        response = requests.post(
            f"{api_url}/login",
            data={"grant_type": "password", "username": username, "password": password}
        )

        if response.status_code == 200:
            st.session_state.is_authenticated = True
            token = response.json().get("access_token")
            st.success("Connexion réussie! Vous pouvez accéder au reste de l'application.")
            st.write(token)
            st.session_state.token = token
            nextpage()
            st.rerun()
    return token


#Page principale
def main_page(token: str):
    st.title("ItemGuard")   
    st.sidebar.header("Navigation")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{api_url}/user/me", headers=headers)
    admin = False
    if response.status_code == 200:
        user_data = response.json()
        admin = user_data["administrator"]
        st.write(admin)
    else:
        st.error(f"Échec de la récupération du profil utilisateur. Code d'erreur : {response.status_code}, {response.reason}")

    # Différents onglets possible
    if admin:    
        selected_tab = st.sidebar.radio("Choisissez une action", ["Tous les produits", "Créer", "Supprimer", "Mettre à jour", "Logs", "Profil","Modifier Profil", "Déconnexion"])
        if selected_tab == "Créer":
            create(token)
        elif selected_tab == "Supprimer":
            delete_product(token)
        elif selected_tab == "Mettre à jour":
            update_product(token)
        elif selected_tab == "Logs":
            show_logs(token)
    else:
        selected_tab = st.sidebar.radio("Choisissez une action", ["Tous les produits", "Profil","Modifier Profil", "Déconnexion"])
    if selected_tab == "Tous les produits":
        all_product(token)
    elif selected_tab == "Profil":
        profil(token)
    elif selected_tab == "Modifier Profil":
        update_profile_page(token)
    elif selected_tab == "Déconnexion":
        disconnect()

# Permet de récupérer le type des données
def get_product_types(token: str):
    types: dict[str, int] = {}
    response = requests.get(
        url=f"{api_url}/types/product",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    if response.status_code == 200:
        data = response.json()
        for row in data:
            types.update({row['nametype']: row['idtype']})
    return types


# Affiche l'intégralité des produits  présents dans la base
def all_product(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{api_url}/products", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data)
        st.write("Produits: ")
        st.write(data)
    else:
        st.error("Échec de la récupération des données depuis FastAPI.")

# Création d'un nouveau produit
def create(token):
    st.header("Create")
    types: dict[str, int] = get_product_types(token)

    with st.form("create_product_form"):
        product_name = st.text_input("Nom du produit", key="product_name")
        if types: product_type = st.radio("Type de produit", options=types.keys())
        quantity_product = st.number_input("Quantité", key="quantity_product", min_value=0, max_value=999, step=1)
        product_price = st.number_input("Prix du produit", key="product_price", min_value=0.0, max_value=999.0, step=0.5)
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        
        product_data = {
            "idType": types[product_type] if types else 0,
            "productName": product_name,
            "quantity": quantity_product,
            "price": product_price
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{api_url}/product", headers=headers, json=product_data)

        if response.status_code == 200:
            st.success("Produit créé avec succès!")
            st.write(product_name, product_type, quantity_product, product_price)
        else:
            st.error("Échec de la création du produit.")


#Supprimer un produit
def delete_product(token):
    st.header("Delete Product")

    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{api_url}/products", headers=headers)
    
    if response.status_code == 200:
        product_data = response.json()

        
        selected_product_name = st.selectbox("Choisir un produit à supprimer", [product["productname"] for product in product_data])

        if st.button("Supprimer"):
            selected_product_id = next((product["idproduct"] for product in product_data if product["productname"] == selected_product_name), None)
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


# Mettre à jour un produit
def update_product(token):
    st.header("Update Product")

    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{api_url}/products", headers=headers)
    
    if response.status_code == 200:
        product_data = response.json()

        types: dict[str, int] = get_product_types(token)

       
        selected_product_name = st.selectbox("Choisir un produit à mettre à jour", [product["productname"] for product in product_data])

        
        selected_product_id = next((product["idproduct"] for product in product_data if product["productname"] == selected_product_name), None)

        if selected_product_id is not None:
            
            response = requests.get(f"{api_url}/product/{selected_product_id}", headers=headers)

            if response.status_code == 200:
                product_data = response.json()

                
                with st.form("update_product_form"):
                    listed_types = []
                    idx = 0
                    if types:
                        for i, p_type in enumerate(types.keys()):
                            listed_types.append(p_type)
                            if types[p_type] == product_data["idtype"]: idx = i 

                    product_name = st.text_input("Nom du produit", key="product_name", value=product_data["productname"])
                    if types: product_type = st.radio("Type de produit", options=types.keys(), index=idx)
                    quantity_product = st.number_input("Quantité", key="quantity_product", min_value=0, max_value=999, step=1, value=product_data["quantity"])
                    product_price = st.number_input("Prix du produit", key="product_price", value=product_data["price"])

                    submit_button = st.form_submit_button("Mettre à jour le produit")

                if submit_button:
                    updated_product_data = {
                        "idProduct": selected_product_id,
                        "idType": types[product_type] if types else 0,
                        "productName": product_name,
                        "quantity": quantity_product,
                        "price": product_price
                    }
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


#Permet de gèrer les logs en appellant la fonction qui correspond à l'action souahitée
def show_logs(token: str):
    st.header("Logs")

    
    selected_action = st.selectbox("Choisir une action", ["Tous les logs", "Rechercher", "Logs limités", "Supprimer"])

    if selected_action == "Tous les logs":
        logs = get_all_logs(token)
        st.write(logs)
    elif selected_action == "Rechercher":
        limit = st.number_input("Limite", value=0)
        desc = st.checkbox("Tri décroissant", value=True)
        before = st.date_input("Avant", value=None)
        before = dt.combine(before, dt.max.time()) if before else dt.now()
        logs = search_logs(limit, desc, before, token)
        st.write(logs)
    elif selected_action == "Logs limités":
        limit = st.number_input("Limite", value=10)
        logs = get_logs_limit(limit, token)
        st.write(logs)
    elif selected_action == "Supprimer":
        log_id = st.number_input("ID du log à supprimer", value=0, min_value=0)
        if st.button("Supprimer"):
            result = delete_log(log_id, token)
            st.write(result)

#Tous les logs
def get_all_logs(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{api_url}/logs", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Échec de la récupération de tous les logs depuis FastAPI. Code d'erreur : {response.status_code}"

#Logs spécifiques en fonction d'une date et d'une limite
def search_logs(limit: int, desc: bool, before: dt, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"limit": limit, "desc": desc, "before": before}
    response = requests.get(f"{api_url}/logs/search", headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Échec de la recherche de logs depuis FastAPI. Code d'erreur : {response.status_code}"

#Juste en fonction de la limite
def get_logs_limit(limit: int, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{api_url}/logs/{limit}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Échec de la récupération de logs limités depuis FastAPI. Code d'erreur : {response.status_code}"

#Supprimer un log
def delete_log(log_id: int, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{api_url}/log/{log_id}", headers=headers)
    if response.status_code == 200:
        return "Log supprimé avec succès!"
    else:
        return f"Échec de la suppression du log. Code d'erreur : {response.status_code}"

# Afficher le profil
def profil(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{api_url}/user/me", headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        st.write("User Profile: ")
        st.write(user_data)
    else:
        st.error(f"Échec de la récupération du profil utilisateur. Code d'erreur : {response.status_code}, {response.reason}")



#On récupère les infos d'un utilisateur
def get_user_profile(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{api_url}/user/me", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None

#Changement du profil
def update_profile_page(token: str):
    st.header("Mise à jour du Profil")
    user_data = get_user_profile(token)

    if user_data:
        administrator = False
        with st.form("update_profile_form"):
            new_email = st.text_input("Nouvel email", value=user_data.get("email"))
            new_password = st.text_input("Nouveau mot de passe", type="password")
            if user_data["administrator"]: administrator = st.checkbox("Administrateur", value=True)
            hashed_password = hashlib.sha256(bytes(new_password, encoding="utf-8")).hexdigest()
            submit_button = st.form_submit_button("Mettre à jour le profil")

        if submit_button:
            updated_profile_data = {
                "email": new_email,
                "passwd": hashed_password if hashed_password else user_data["passwd"],
                "administrator": administrator,
            }

            response = requests.put(f"{api_url}/user/update", headers={"Authorization": f"Bearer {token}"}, json=updated_profile_data)
            if response.status_code == 200:
                st.success("Profil mis à jour avec succès!")
                st.session_state.is_authenticated = False
                st.session_state.page = 0
                st.rerun()
            else:
                st.error(f"Échec de la mise à jour du profil. Code d'erreur : {response.status_code}")
    else:
        st.error("Échec de la récupération du profil utilisateur.")


def disconnect():
    st.session_state.is_authenticated = False
    st.session_state.page = 0
    st.rerun()



if __name__ == '__main__':
    if st.session_state.page == 0:
        login_page()
    else:
        if st.session_state.is_authenticated:
            main_page(st.session_state.token)
