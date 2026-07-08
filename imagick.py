import subprocess
import os
import sys

print("Welcome to Jonathan Candelaria's PDF to TIFF Magick!")

input_folder = "input-files"
output_folder = "output-files"

os.makedirs(output_folder, exist_ok=True)


# Validate Ghostscript
def check_ghostscript():
    result = subprocess.run(
        ["where", "gswin64c"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("Ghostscript found:")
        print(result.stdout.strip())
        return True
    else:
        return False


# Create Ghostscript output filename pattern
def generate_output_pattern(file_name):
    name = os.path.basename(file_name)

    date_part = name.replace("BlueRidgeSun_", "").replace(".pdf", "")

    output_pattern = os.path.join(
        output_folder,
        f"SpaBRS1_{date_part}_1_%02d.tiff"
    )

    return output_pattern


# Process entire PDF using Ghostscript directly
def process_pdf(file_name):
    print("")
    print("Processing File: " + file_name)

    output_pattern = generate_output_pattern(file_name)

    command = [
        "gswin64c",
        "-dSAFER",
        "-dBATCH",
        "-dNOPAUSE",
        "-r300",
        "-sDEVICE=tiff24nc",
        "-sCompression=lzw",
        "-dTextAlphaBits=4",
        "-dGraphicsAlphaBits=4",
        f"-sOutputFile={output_pattern}",
        file_name
    ]

    print("Output pattern:")
    print(output_pattern)
    print("")
    print("Ghostscript is running. It should print page progress below:")
    print("")

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in process.stdout:
        print(line, end="")

    process.wait()

    if process.returncode != 0:
        print("")
        print("Ghostscript failed.")
        raise SystemExit

    print("")
    print("Finished: " + file_name)


# Main script
if not os.path.exists(input_folder):
    print(f"Input folder does not exist: {input_folder}")
    raise SystemExit

if not check_ghostscript():
    print("Ghostscript Test Failed")
    raise SystemExit

pdf_files = []

for file in os.listdir(input_folder):
    if file.lower().endswith(".pdf"):
        pdf_files.append(file)

if len(pdf_files) == 0:
    print("No PDF files found in input-files.")
    raise SystemExit

for file in pdf_files:
    pdf_path = os.path.join(input_folder, file)
    process_pdf(pdf_path)

print("")
print("All PDF files processed.")
