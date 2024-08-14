

import torch
import torchaudio
from spleeter.separator import Separator
import os

def separate_instruments(input_file, output_dir):
    # Create a Separator object
    separator = Separator('spleeter:4stems')

    # Separate the audio file
    separator.separate_to_file(input_file, output_dir)

    print(f"Separation complete. Output files saved in {output_dir}")


input_file = 'path'
output_dir = "path"


print(f"Input file: {input_file}")
print(f"Output directory: {output_dir}")

# Run separation
separate_instruments(input_file, output_dir)


