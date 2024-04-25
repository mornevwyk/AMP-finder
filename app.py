import streamlit as st
import io
from Bio import SeqIO
import myUtils as ut
from PyBioMed.Pyprotein import CalculateAAComposition, CalculateDipeptideComposition, CalculateCTD, GetAPseudoAAC
from joblib import dump, load
import pandas as pd

st.set_page_config(
    page_title="Antimicrobial Peptide Finder",
    page_icon="🧬",
    layout="wide"
)

if 'download_disabled' not in st.session_state:
    st.session_state.download_disabled = False

@st.cache_data
def rf_model_prediction(data):
    return rf.predict_proba(data)[:,1]

@st.cache_data
def gb_model_prediction(data):
    return gb.predict_proba(data)[:,1]

@st.cache_data
def get_data(seq):
    data = ut.prep_data(seq, [], [CalculateAAComposition, CalculateCTD])
    return data.drop('activity', axis=1)

st.title('Antimcirobial Peptide Finder')
st.markdown("**How to use:** Upload a .fasta file with the protein sequences you would like to screen for antimicrobial activity. The sequences can only contain combinations of the 20 common amino acids.")

rf = load('./Models/RF_classifier.joblib')
gb = load('./Models/GB_classifier.joblib')
sequences = []

file_uploader=st.file_uploader(' Please upload a .fasta file ')

expander = st.expander("See Sequence Data")

main_container = st.container()

#df_predictions = pd.DataFrame()
#download_button = st.download_button("Download Predictions", df_predictions.to_csv(index=False).encode('utf-8'), disabled=st.session_state.download_disabled)

if file_uploader is not None: 
    byte_str=file_uploader.read()
    text_obj=byte_str.decode("UTF-8")
    
    #st.write(io.StringIO(text_obj))
    seq_object=SeqIO.parse(io.StringIO(text_obj), "fasta")
    #st.markdown('***')
    count = 0
    for seq in seq_object:
        count += 1
        sequences.append(str(seq.seq))

    main_container.write(f"Found {count} sequences")

    selected_features = pd.read_csv("./Models/DNN_input_features_mask.csv")
    selected_features = selected_features['mask'].values

    seq = sequences
    #data = ut.prep_data(seq, [], [CalculateAAComposition, CalculateCTD])
    
    data = get_data(seq)
    
    #data = data.drop('activity', axis=1)

    expander.dataframe(data)
    expander.download_button("Download Features", file_name="extracted_features_data.txt", data=data.to_csv(index=True).encode('utf-8'), disabled=st.session_state.download_disabled)
    

    data_features = ut.filter_features(data, selected_features)

    #rf_pred = rf.predict_proba(data_features)[:,1]
    rf_pred = rf_model_prediction(data_features)
    #gb_pred = gb.predict_proba(data_features)[:,1]
    gb_pred = gb_model_prediction(data_features)

    df_predictions = pd.DataFrame({'Random Forrest Model Predictions': rf_pred, 'Gradient Boost Model Predictions': gb_pred, 'Sequences': sequences})
    main_container.dataframe(df_predictions, 
                 column_config={
                     'Random Forrest Model Predictions':st.column_config.ProgressColumn(min_value=0, max_value=1),
                     'Gradient Boost Model Predictions':st.column_config.ProgressColumn(min_value=0, max_value=1)
                     })
    
    st.download_button("Download Predictions", data=df_predictions.to_csv(index=True).encode('utf-8'), file_name="predicted_amp_activity_probability.txt", disabled=st.session_state.download_disabled)
    





    
    
