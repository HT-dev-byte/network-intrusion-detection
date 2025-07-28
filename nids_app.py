import streamlit as st
import requests
import json

# Replace with your actual values
API_KEY = 'XXpm44q4qOcerjKYmNckPC_IE76O1A5i4zZBYL5XvqRV'
DEPLOYMENT_URL = 'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/15f51369-b7bf-43a1-a918-c2918dfaf340/predictions?version=2021-05-01'

# Step 1: Get IAM Token
def get_iam_token():
    response = requests.post(
        'https://iam.cloud.ibm.com/identity/token',
        data={'apikey': API_KEY, 'grant_type': 'urn:ibm:params:oauth:grant-type:apikey'},
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        st.error("❌ Failed to get IAM token.")
        st.text(response.text)
        return None

# Step 2: Send input and get prediction
import pandas as pd

def predict_intrusion(values):
    token = get_iam_token()
    if token is None:
        return None

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }

    # Full list of 41 feature names used in your model
    columns = [
        "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", "land",
        "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in", "num_compromised",
        "root_shell", "su_attempted", "num_root", "num_file_creations", "num_shells",
        "num_access_files", "num_outbound_cmds", "is_host_login", "is_guest_login", "count",
        "srv_count", "serror_rate", "srv_serror_rate", "rerror_rate", "srv_rerror_rate",
        "same_srv_rate", "diff_srv_rate", "srv_diff_host_rate", "dst_host_count",
        "dst_host_srv_count", "dst_host_same_srv_rate", "dst_host_diff_srv_rate",
        "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate", "dst_host_serror_rate",
        "dst_host_srv_serror_rate", "dst_host_rerror_rate", "dst_host_srv_rerror_rate"
    ]

    # Sample input row: Replace these with values from the UI or test values
    values = [0, 'tcp', 'http', 'SF', 491, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              2, 2, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 255, 254, 1.0, 0.0, 0.01, 0.0, 0.0,
              0.0, 0.0, 0.0]

    input_df = pd.DataFrame([values], columns=columns)

    # Convert to Watson ML payload
    payload = {
        "input_data": [{
            "fields": input_df.columns.tolist(),
            "values": input_df.values.tolist()
        }]
    }

    response = requests.post(DEPLOYMENT_URL, json=payload, headers=headers)

    if response.status_code == 200:
        prediction = response.json()['predictions'][0]['values'][0][0]
        return prediction
    else:
        st.error(f"Error: {response.status_code}\n{response.text}")
        return None


# Streamlit UI
st.title("🚨 Network Intrusion Detection System (NIDS)")

st.write("Enter network session features to classify traffic as normal or an intrusion.")

# Get user inputs
duration = st.number_input("Duration", min_value=0, step=1)
src_bytes = st.number_input("Source Bytes", min_value=0, step=1)
dst_bytes = st.number_input("Destination Bytes", min_value=0, step=1)
count = st.number_input("Connection Count", min_value=0, step=1)

# Validate inputs
if st.button("Predict"):
    if None in (duration, src_bytes, dst_bytes, count):
        st.warning("Please enter all required values.")
    else:
        # Build input vector with dummy/default values and user input
        input_values =  list(map(float, [
    duration, 0, 0, 0, src_bytes, dst_bytes, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    count, count, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
    255, 254, 1.0, 0.0, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0
]))

        result = predict_intrusion(input_values)

        if result == 0:
            st.success("✅ Normal traffic detected.")
        elif result == 1:
            st.error("🚨 Intrusion detected!")
        else:
            st.warning("Prediction failed.")