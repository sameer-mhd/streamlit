import streamlit as st
from vega_datasets import data

source = data.barley()
print(data)

st.bar_chart(source, x="year", y="yield", color="site", stack=False)