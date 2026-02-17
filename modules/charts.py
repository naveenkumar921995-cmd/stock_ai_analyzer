import plotly.graph_objects as go
import streamlit as st

def show_price_chart(data):

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        mode='lines',
        name='Close Price'
    ))

    fig.update_layout(template="plotly_dark", height=500)

    st.plotly_chart(fig, use_container_width=True)

