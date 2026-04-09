import subprocess
import os

print("Welcome to Jonathan Candelaria's PDF to TIFF Magick!")

# Run test to see if command line works for ImageMagick and that magick is working
subprocess.run([
    "magick",
    "-size", "300x100",
    "xc:black",
    "-fill", "white",
    "-gravity", "center",
    "-pointsize", "24",
    "-annotate", "0", "Hello",
    "test.png"
])

# If we haven't crashed, delete the test file.
if os.path.exists("test.png"):
    os.remove("test.png")
    print("Functionality Test Complete")
else:
    print("Failed to test Magick. Please check your magick installation and try again.")
    raise SystemExit


# Validate Ghostscript
def check_ghostscript():
    result = subprocess.run(
        ["where", "gswin64c"],
        capture_output=True,
        text=True
    )
    return result.returncode == 0


# Returns file name for generation of TIFF file
def generate_file_name(file_name, page_num):
    name = os.path.basename(file_name)
    date_part = name.replace("BlueRidgeSun_", "").replace(".pdf", "")
    page = str(page_num + 1).zfill(2)
    return os.path.join("output-files", f"SpaBRS1_{date_part}_1_{page}.tiff")


# Process for an individual page within PDF
def process_page(number, file_name):
    print(str(number + 1) + " " + file_name)

    new_file = generate_file_name(file_name, number)

    subprocess.run([
        "magick",
        "-density", "300",
        f"{file_name}[{number}]",
        new_file
    ])

    print("output is: " + new_file)


# Process individual PDF
def process_pdf(file_name):
    print("Processing File: " + file_name)

    result = subprocess.run(
        ["magick", "identify", "-format", "%n", file_name],
        capture_output=True,
        text=True
    )

    pages = int(result.stdout.strip())

    for x in range(pages):
        process_page(x, file_name)


# Start Main Script and loop through all PDF files
input_folder = "input-files"
output_folder = "output-files"

os.makedirs(output_folder, exist_ok=True)

if check_ghostscript():
    print("Ghostscript Test Complete")
else:
    print("Ghostscript Test Failed")
    raise SystemExit

for file in os.listdir(input_folder):
    if file.lower().endswith(".pdf"):
        pdf_path = os.path.join(input_folder, file)
        process_pdf(pdf_path)
