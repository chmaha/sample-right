#!/usr/bin/env python3
import os
import glob
import wave
import tkinter as tk
from tkinter import filedialog, messagebox


# Supported file extensions
SUPPORTED_EXTENSIONS = {"wav"}

def is_supported_file(file):
    """Check if the file has a supported extension."""
    _, ext = os.path.splitext(file)
    return ext[1:].lower() in SUPPORTED_EXTENSIONS


def change_samplerate(file, new_samplerate):
    """Update the samplerate metadata in the WAV file header."""
    # Get the directory and filename of the input file
    dir_name, file_name = os.path.split(file)

    # Create the temporary file path in the same directory
    temp_file = os.path.join(dir_name, f"fixed_{file_name}")

    try:
        with wave.open(file, 'rb') as wav:
            # Read the current parameters
            params = wav.getparams()
            num_channels, sample_width, old_samplerate, num_frames, comptype, compname = params[:6]

            # Reopen the file for writing with updated samplerate
            with wave.open(temp_file, 'wb') as out_wav:
                # Set new parameters, keeping other values unchanged
                new_params = (num_channels, sample_width, new_samplerate, num_frames, comptype, compname)
                out_wav.setparams(new_params)

                # Copy audio frames to the new file
                frames = wav.readframes(num_frames)
                out_wav.writeframes(frames)

        # Replace the original file with the updated file
        os.replace(temp_file, file)
        output_text.insert(tk.END, f"Updated metadata for {file} to samplerate {new_samplerate}\n")
        output_text.yview(tk.END)  # Scroll to the bottom of the Text widget
    except Exception as e:
        output_text.insert(tk.END, f"Error processing {file}: {e}\n")
        output_text.yview(tk.END)

def select_files():
    """Open a file dialog to select multiple WAV files."""
    files = filedialog.askopenfilenames(
        title="Select WAV Files",
        filetypes=[("WAV Files", "*.wav")],
        multiple=True
    )

    if files:
        folder_label.config(text=", ".join(files))  # Display selected files

def start_processing():
    """Start the process of changing samplerates based on the GUI selections."""
    try:
        samplerate = int(samplerate_var.get())  # Get selected samplerate
    except ValueError:
        messagebox.showerror("Input Error", "Please select a valid samplerate.")
        return

    files_to_process = folder_label.cget("text")  # Get the selected files

    if not files_to_process:
        messagebox.showerror("Selection Error", "Please select some files.")
        return

    # Split the files into a list
    files_to_process = files_to_process.split(", ")

    if not files_to_process:
        messagebox.showwarning("No Files", "No WAV files found.")
        return

    # Clear the output text box
    output_text.delete(1.0, tk.END)

    for file in files_to_process:
        if is_supported_file(file):
            change_samplerate(file, samplerate)
        else:
            output_text.insert(tk.END, f"Skipping unsupported file: {file}\n")
            output_text.yview(tk.END)

    messagebox.showinfo("Processing Complete", "All selected files have been processed.")

# Setup the GUI window
root = tk.Tk()
root.title("Sample-Right - Batch Fix Incorrect Samplerate Stamps")
# root.geometry("800x600")  # Set a wider initial window size (800x600)

# Configure grid to make rows and columns flexible
root.grid_rowconfigure(4, weight=1, uniform="equal")  # Make the output row flexible
root.grid_columnconfigure(0, weight=1, uniform="equal")  # Make the first column flexible
root.grid_columnconfigure(1, weight=1, uniform="equal")  # Make the second column flexible

# Create a dropdown for selecting samplerate
samplerate_var = tk.StringVar()
samplerate_label = tk.Label(root, text="Select Samplerate:")
samplerate_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
samplerate_dropdown = tk.OptionMenu(
    root, samplerate_var, "22050", "44100", "48000", "88200", "96000", "176400", "192000")
samplerate_dropdown.config(width=8)
samplerate_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Label for displaying the selected files
folder_label = tk.Label(root, text="No files selected", width=40, relief="sunken")
folder_label.grid(row=1, column=0, columnspan=2, padx=0, pady=10)

# Browse button to select files
browse_button = tk.Button(root, text="Browse Files", command=select_files)
browse_button.grid(row=2, column=0, columnspan=2, pady=10)

# Start button to begin processing
start_button = tk.Button(root, text="Start Processing", command=start_processing)
start_button.grid(row=3, column=0, columnspan=2, pady=10)

# Create a text widget to show output
output_text = tk.Text(root, height=10, width=60)
output_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")  # Expand in all directions

# Add a scrollbar to the Text widget
scrollbar = tk.Scrollbar(root, command=output_text.yview)
scrollbar.grid(row=4, column=2, sticky='ns')
output_text.config(yscrollcommand=scrollbar.set)

# Start the Tkinter event loop
root.mainloop()
