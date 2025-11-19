import streamlit as st
import requests

# Inject Cyberpunk CSS styles for neon/glow effect
st.markdown("""
    <style>
    body {
        background-color: #000000;
        color: #00ffff;
        font-family: 'Fira Code', monospace;
    }
    .neon-box {
        border: 2px solid #ff0080;
        box-shadow: 0 0 10px #ff0080;
        padding: 20px;
        margin-top: 20px;
        border-radius: 5px;
    }
    .chromatic-text {
        text-shadow: 2px 2px #ff0080, -2px -2px #00ff00;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌧️ Ultra-Precision Nowcasting Engine")

lat = st.number_input("Enter Latitude", value=12.34)
lon = st.number_input("Enter Longitude", value=56.78)

if st.button("Get Prediction"):
    try:
        resp = requests.post("http://127.0.0.1:5000/predict", json={"lat": lat, "lon": lon})
        if resp.status_code == 200:
            data = resp.json()
            st.markdown(f"""
                <div class="neon-box chromatic-text">
                    {data['prediction']}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Error from prediction API")
    except Exception as e:
        st.error(f"Could not reach prediction API: {e}")