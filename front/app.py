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



def navigation(token):
    if st.session_state.is_authenticated:
        all_product(token)
        create(token)
        delete_product(token)
        update_product(token)


        
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

