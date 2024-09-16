from spleeter.separator import Separator
import os
import time
import threading
import sys
import subprocess

def get_file_size(file_path):
    return os.path.getsize(file_path)

def estimate_progress(start_time, file_size, processed_size):
    elapsed_time = time.time() - start_time
    if processed_size == 0:
        return 0, "Unknown"
    progress = (processed_size / file_size) * 100
    estimated_total_time = (elapsed_time / progress) * 100
    remaining_time = estimated_total_time - elapsed_time
    return progress, time.strftime("%M:%S", time.gmtime(remaining_time))

def animate_progress(stop, file_path):
    file_size = get_file_size(file_path)
    start_time = time.time()
    while not stop():
        try:
            processed_size = sum(get_file_size(os.path.join(root, name))
                                 for root, _, files in os.walk(os.path.dirname(file_path))
                                 for name in files if name.endswith('.wav'))
        except:
            processed_size = 0

        progress, remaining = estimate_progress(start_time, file_size, processed_size)
        sys.stdout.write(f"\rProgress: {progress:.1f}% | Est. remaining time: {remaining}     ")
        sys.stdout.flush()
        time.sleep(1)

def convert_audio(input_file, output_file, format='mp3', quality='128k'):
    command = [
        'ffmpeg', '-i', input_file,
        '-ab', quality,
        output_file
    ]
    subprocess.run(command, check=True)

def separate_instruments(input_dir, output_dir, output_format='mp3', quality='128k'):
    separator = Separator('spleeter:5stems')
    os.makedirs(output_dir, exist_ok=True)
    audio_files = [f for f in os.listdir(input_dir) if f.endswith(('.mp3', '.wav', '.flac', '.ogg'))]
    audio_files.sort(key=lambda x: int(x.split('.')[0]))  # Sort numerically

    total_files = len(audio_files)

    for index, audio_file in enumerate(audio_files, 1):
        input_path = os.path.join(input_dir, audio_file)
        base_name = os.path.splitext(audio_file)[0]
        file_output_dir = os.path.join(output_dir, base_name)

        print(f"\nProcessing file {index} of {total_files}: {audio_file}")
        print("Separating: ")

        stop_animation = False
        animation_thread = threading.Thread(target=animate_progress, args=(lambda: stop_animation, input_path))
        animation_thread.start()

        start_time = time.time()
        separator.separate_to_file(input_path, file_output_dir)
        end_time = time.time()

        stop_animation = True
        animation_thread.join()

        for root, _, files in os.walk(file_output_dir):
            for file in files:
                if file.endswith(('.mp3', '.wav')):
                    stem_name = file.split('.')[0]  # Changed from '_' to '.'
                    new_name = f"{base_name}_{stem_name}.{output_format}"
                    input_file_path = os.path.join(root, file)
                    output_file_path = os.path.join(root, new_name)

                    convert_audio(input_file_path, output_file_path, format=output_format, quality=quality)
                    os.remove(input_file_path)

        duration = end_time - start_time
        print(f"\nSeparation complete for {audio_file}.")
        print(f"Time taken: {duration:.2f} seconds")
        print(f"Output saved in {file_output_dir}")
        print(f"Progress: {index}/{total_files} files processed")

    print(f"\nAll separations complete. Total files processed: {total_files}")
    print(f"Output files saved in {output_dir}")

def separate_instruments_single_file(input_file, output_dir, output_format='mp3', quality='128k'):
  separator = Separator('spleeter:5stems')
  base_name = os.path.splitext(os.path.basename(input_file))[0]
  file_output_dir = os.path.join(output_dir, base_name)
  
  os.makedirs(file_output_dir, exist_ok=True)
  
  # Separate the input file
  separator.separate_to_file(input_file, file_output_dir)

  for root, _, files in os.walk(file_output_dir):
    for file in files:
      if file.endswith(('.mp3', '.wav')):
        stem_name = file.split('.')[0]
        new_name = f"{base_name}_{stem_name}.{output_format}"
        input_file_path = os.path.join(root, file)
        output_file_path = os.path.join(root, new_name)

        convert_audio(input_file_path, output_file_path, format=output_format, quality=quality)
        os.remove(input_file_path)

  return file_output_dir


if __name__ == '__main__':

    input_dir = os .path.join(os.getcwd + "inputsamples")
    output_dir = os .path.join(os.getcwd + "outputdir")
    separate_instruments(input_dir, output_dir)