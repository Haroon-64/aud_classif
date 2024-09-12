import streamlit as st
from seperator import *
import os
import subprocess
from tempfile import NamedTemporaryFile


st.title('Audio Instrument Separator')

# File Upload
uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "flac", "ogg"])

# Output Options
output_format = st.selectbox("Select output format", ['mp3', 'wav'])
quality = st.selectbox("Select audio quality", ['128k', '192k', '256k', '320k'])

# Processing
if st.button('Start Separation') and uploaded_file:
  with NamedTemporaryFile(delete=False) as temp_input_file:
    temp_input_file.write(uploaded_file.read())
    temp_input_file.flush()

    output_dir = os.path.join(os.getcwd(), 'output')
    
    with st.spinner('Processing...'):
      output_path = separate_instruments_single_file(temp_input_file.name, output_dir, output_format, quality)
      
    st.success('Separation complete!')
    st.write(f"Output saved in {output_path}")
    
    # Display audio players and download links
    for root, _, files in os.walk(output_path):
      for file in files:
        file_path = os.path.join(root, file)
        
        # Display audio player
        audio_file = open(file_path, 'rb').read()
        st.audio(audio_file, format=f'audio/{output_format}')
        
        # Display download button
        st.download_button(f"Download {file}", audio_file, file_name=file)