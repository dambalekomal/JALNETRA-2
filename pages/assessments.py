import streamlit as st
import pandas as pd

st.title("Assessment Units")

data = {
    "Name":["Aurangabad","Paithan","Vaijapur"],
    "Status":["Safe","Critical","Semi-Critical"],
    "Extraction %":[70,95,88],
    "Year":[2024,2024,2024]
}

df = pd.DataFrame(data)

st.dataframe(df,use_container_width=True)