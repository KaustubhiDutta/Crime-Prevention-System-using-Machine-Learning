import streamlit as st
import requests
import urllib.parse
import plotly.graph_objects as go

st.set_page_config(page_title="Crime Prediction", layout="centered")

# --------- DARK STYLE ----------
st.markdown("""
    <style>
    .stApp {
        background-color: #0b1220;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Crime Risk Prediction Dashboard")

# --------- FETCH STATES ----------
try:
    response = requests.get("http://127.0.0.1:5000/states")
    states = response.json()
except:
    st.error("Flask server is not running")
    st.stop()

# --------- DROPDOWN ----------
selected_state = st.selectbox("Select State", states)

# --------- BUTTON ----------
if st.button("Predict"):
    try:
        # ✅ FIX: encode state (important)
        encoded_state = urllib.parse.quote(selected_state)

        url = f"http://127.0.0.1:5000/predict/{encoded_state}"
        response = requests.get(url)
        data = response.json()

        if "error" in data:
            st.error(data["error"])
        else:
            # --------- BASIC OUTPUT ----------
            st.success(f"Risk Level: {data['risk_level']}")

            st.subheader("Average Crime")
            st.write(data["average_crime"])

            st.subheader("Reason")
            st.write(data["reason"])

            # --------- CRIME BREAKDOWN (UPDATED) ----------
            st.subheader("Crime Breakdown")

            breakdown = data["crime_breakdown"]

            labels = list(breakdown.keys())
            values = list(breakdown.values())

            fig = go.Figure(
                data=[
                    go.Bar(
                        x=labels,
                        y=values,
                        marker=dict(color="#79A9D1"),
                        text=values,
                        textposition="outside"
                    )
                ]
            )

            fig.update_layout(
                height=500,
                plot_bgcolor="#0b1220",
                paper_bgcolor="#0b1220",
                font=dict(color="white"),
                xaxis=dict(
                    tickangle=-90,
                    showgrid=False
                ),
                yaxis=dict(
                    gridcolor="rgba(255,255,255,0.1)"
                )
            )

            st.plotly_chart(fig, use_container_width=True)

            # --------- VALUES LIST ----------
            for crime, value in breakdown.items():
                st.write(f"• {crime}: {value}")

            # --------- RECOMMENDATIONS ----------
            st.subheader("Recommendations")
            for rec in data["recommendations"]:
                st.write(f"• {rec}")

    except:
        st.error("Error connecting to Flask server")