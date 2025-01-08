#!/usr/bin/env python3
#
# Sample-Right - Batch fix incorrect samplerate stamps
# Copyright (C) 2025 chmaha
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import glob
import wave

# Supported file extensions
SUPPORTED_EXTENSIONS = {"wav"}

def is_supported_file(file):
    """Check if the file has a supported extension."""
    _, ext = os.path.splitext(file)
    return ext[1:].lower() in SUPPORTED_EXTENSIONS

def change_samplerate(file, new_samplerate):
    """Update the samplerate metadata in the WAV file header."""
    temp_file = f"fixed_{file}"

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
    print(f"Updated metadata for {file} to samplerate {new_samplerate}")

def main():
    if len(sys.argv) != 3:
        print("Usage: ./sample-right.py correct_samplerate file_pattern")
        print('Example: ./sample-right.py 44100 "*.wav"')
        sys.exit(1)

    try:
        samplerate = int(sys.argv[1])
    except ValueError:
        print("Error: correct_samplerate must be a numeric value (e.g., 44100, 96000).")
        sys.exit(1)

    file_pattern = sys.argv[2]

    # Handle wildcard expansion using glob
    files_to_process = []
    expanded_files = glob.glob(file_pattern)  # Expand wildcard patterns
    if not expanded_files:
        print(f"Warning: No files matched for pattern '{file_pattern}'")
    files_to_process.extend(expanded_files)  # Add expanded files to the list

    if not files_to_process:
        print("No files to process. Exiting.")
        sys.exit(1)

    for file in files_to_process:
        if is_supported_file(file):
            change_samplerate(file, samplerate)
        else:
            print(f"Skipping unsupported file: {file}")

if __name__ == "__main__":
    main()
