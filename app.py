import streamlit as st
import pandas as pd
import os
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

st.title("Analyse de feedbacks clients")

# Upload du fichier
fichier = st.file_uploader("Chargez votre fichier CSV", type="csv")

def analyser_sentiment(commentaires):
  client = OpenAI()
  sent_com = []
  for i in commentaires :
    cc = client.chat.completions.create (
      model = "gpt-5.4",
      messages = [
      {"role" : "system", "content":
      """tu classifies les commentaires en les résumant en un ligne et en leur attribuant un mot donnant le sentiment général : positif, mitigé ou négatif
      Résultat de ton analyse : résumé ; sentiment
      Exemples:
      c'était vraiment bien on valide ; positif
      on a aimé mais il manquait quelque chose ; mitigé
      ça ne me convient pas ; négatif
      """
      },
      {"role" : "user", "content" : i}
                 ],
      temperature = 0
                                        )
    sent_com.append(cc.choices[0].message.content)
  return sent_com

def exporter_resultats(df,sentiment):
  sent = []
  resum = []
  for s in sentiment :
    part = s.split(';')
    if len(part)==2:
      sent.append(part[1])
      resum.append(part[0])
    else :
      sent.append(None)
      resum.append(None)
  df["résumé"] = resum
  df["sentiment"] = sent
  ds = df["sentiment"].value_counts()
  html_avis = ds.to_frame().to_html()
  st.dataframe(ds)
  return html_avis

if fichier:
    df = pd.read_csv(fichier)
    colonne = st.selectbox("Choisissez la colonne à analyser", df.columns)
    if st.button("Lancer l'analyse"):
      resultats = analyser_sentiment(df[colonne])
      exporter_resultats(df, resultats)
