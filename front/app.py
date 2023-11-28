import streamlit as st
import requests

api_url = "http://api:5000"




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





def navigation(token):
    if st.session_state.is_authenticated:
        all_product(token)
        create(token)


        


def main():
    st.title("ItemGuard")
    st.session_state.setdefault('is_authenticated', False)
    token = None

    # Page de connexion
    if not st.session_state.is_authenticated:
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
                
    if st.session_state.is_authenticated:
        navigation(token)
    
        
if __name__ == '__main__':
    main()
