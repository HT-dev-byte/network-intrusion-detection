# Network Intrusion Detection System (NIDS)

Built a robust Network Intrusion Detection System (NIDS) using machine learning that detects and classifies various types of cyber-attacks (DoS, Probe, R2L, U2R) and distinguishes them from normal network activity.

Dataset Source: [Kaggle - Network Intrusion Detection Dataset](https://www.kaggle.com/datasets/sampadab17/networkintrusion-detection)

##  ML Pipeline

1. Data cleaning and preprocessing
2. Feature encoding and scaling
3. Random Forest classifier training
4. Model saved as `nids_pipeline.pkl`
5. Deployment on **IBM Cloud (Watson Machine Learning)**

##  Deployment

The model is deployed on **IBM Cloud Lite** using:
- `Watsonx.ai Studio`
- Public endpoint for inference
- Streamlit interface for testing predictions

##  Files

- `nids_pipeline.pkl`: Trained model
- `streamlit_app.py`: Interactive Streamlit web app
- `nids_data_exploration.ipynb`: Data exploration and model training
- `requirements.txt`: Dependencies for local execution

## Example Endpoint

- **Deployment URL**: `https://us-south.ml.cloud.ibm.com/ml/v4/deployments/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/predictions?version=2021-05-01`
- Authentication handled via IAM API Key

## Usage(Streamlit)

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
