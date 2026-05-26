# ...existing code...
try:
    import plotly.express as px  # type: ignore[import]
except ImportError:
    px = None

import streamlit as st
import pandas as pd

st.title("Visualizations")

data = pd.DataFrame({
    "Category":["Safe","Critical","Semi-Critical"],
    "Count":[5,2,3]
})

if px:
    fig = px.pie(data, names="Category", values="Count")
    st.plotly_chart(fig, use_container_width=True)

    bar = px.bar(
        x=["Aurangabad","Paithan","Vaijapur"],
        y=[70,95,88]
    )
    st.plotly_chart(bar, use_container_width=True)
else:
    st.error("plotly not installed. Install with `pip install plotly` to see interactive charts.")
    st.bar_chart(data.set_index("Category"))
# ...existing code...