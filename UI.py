import streamlit as st
from seperator import *
import os
from tempfile import NamedTemporaryFile


ms = st.session_state
if "themes" not in ms: 
  ms.themes = {"current_theme": "light",
                    "refreshed": True,
                    
                    "light": {"theme.base": "dark",
                              "theme.backgroundColor": "black",
                              "theme.primaryColor": "#c98bdb",
                              "theme.secondaryBackgroundColor": "#5591f5",
                              "theme.textColor": "white",
                              "theme.textColor": "white",
                              "button_face": "🌜"},

                    "dark":  {"theme.base": "light",
                              "theme.backgroundColor": "white",
                              "theme.primaryColor": "#5591f5",
                              "theme.secondaryBackgroundColor": "#82E1D7",
                              "theme.textColor": "#0a1464",
                              "button_face": "🌞"},
                    }
  

def ChangeTheme():
  previous_theme = ms.themes["current_theme"]
  tdict = ms.themes["light"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]
  for vkey, vval in tdict.items(): 
    if vkey.startswith("theme"): st._config.set_option(vkey, vval)

  ms.themes["refreshed"] = False
  if previous_theme == "dark": ms.themes["current_theme"] = "light"
  elif previous_theme == "light": ms.themes["current_theme"] = "dark"


btn_face = ms.themes["light"]["button_face"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]["button_face"]
st.button(btn_face, on_click=ChangeTheme)

if ms.themes["refreshed"] == False:
  ms.themes["refreshed"] = True
  st.rerun()

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