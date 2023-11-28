FROM python:3.8

WORKDIR /front

RUN pip install streamlit


COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]