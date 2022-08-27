import streamlit as st
import pandas as pd
import numpy as np
from ast import literal_eval


# read_data
@st.cache
def preprocess(rules):
  rc  = rules[['antecedents', 'consequents']].copy()
  rc.antecedents = rc.antecedents.apply(lambda x: literal_eval(x.split('{')[1].split('}')[0]))
  rc.consequents = rc.consequents.apply(lambda x: literal_eval(x.split('{')[1].split('}')[0]))
  rc.antecedents =  rc.antecedents.apply(lambda x: x if not(isinstance(x, tuple))else None)
  rc.dropna(inplace = True)
  rc.consequents = rc.consequents.apply(lambda x: list(x) if isinstance(x, tuple) else [x])
  rec_map = rc.groupby('antecedents')['consequents'].sum().to_dict()
  return rec_map

def recommend(basket, map):
  recommended = []
  for item in basket:
    recommended.extend(map[item])
  return recommended
def main():
    page_bg_img = """
    <style>
    [data-testid="stAppViewContainer"] > {
        background-image: url("https://images.unsplash.com/photo-1501426026826-31c667bdf23d");
        background-size: 180%;
        background-position: top left;
        background-repeat: no-repeat;
        background-attachment: local;
        }
        </style>
    """

    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.title("Groceries Market Basket Analysis")
    rules = pd.read_csv('Data/rules.csv')
    rec_map = preprocess(rules)

    items = st.text_input("Items selected", key="items")
    if st.button('Make Recommendation') and items :
        basket = [item.strip() for item in items.split(',')]
        result = recommend(basket, rec_map)
        st.write(result)

if __name__ == '__main__':
    main()
