import streamlit as st
import requests


api_url = "http://api:5000"


def main():
    if st.button("Récupérer les données depuis FastAPI"):

        response = requests.get(f"{api_url}/log/last")
        data = response.json()
        st.write("Name: ")
        st.write(data)


if __name__ == '__main__':
    main()
