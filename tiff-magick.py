import subprocess
import os

# Check to see if Python is awake in terminal
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
    print(quit)


# DECLARATION OF HELPER FUNCTIONS/SUBROUTINES

# Validate Ghostscript.
# Ghostscript is a library made for ImageMagick designed to allow for the support of larger files
def check_ghostscript():
    result = subprocess.run(
        ["where", "gswin64c"],
        capture_output=True,
        text=True
    )
    return result.returncode == 0


# Process individual PDF
def process_pdf(file_name):
    print("Processing File: " + file_name)
    result = subprocess.run(
        # This is a string locator test
        # ["magick", "identify", "\"" + file_name + "\""],
        ["magick", "identify", file_name],
        capture_output=True,
        text=True
    )
    pages = int(len(result.stdout.splitlines()))
    for x in range(pages):
        process_page(x, file_name)


# Process for an individual page within PDF
def process_page(number, file_name):
    print(str(number) + " " + file_name)
    # Remember 2 is actually the THIRD item in the index. TODO: Fix this logic.

    new_file = generate_file_name(file_name, number)

    subprocess.run([
        "magick",
        "-density", "300",
        f"{file_name}[{number}]",
        new_file
    ])
    print("output is: " + new_file)


# Returns file name for generation of TIFF file
def generate_file_name(file_name, page_num):

    file_name = file_name.replace("input-files", "output-files")
    base = file_name.replace(".pdf", "")
    base = base.replace("BlueRidgeSun", "")
    page_num = page_num + 1 # this is to make sure page number 0 is called "Page Number 1"
    page = str(page_num).zfill(2)

    return f"{base}_{page}.tiff"


# Start Main Script and loop through all PDF files
folder = "input-files"
# validate Ghostscript
if check_ghostscript():
    print("Ghostscript Test Complete")
else:
    print("Ghostscript Test Failed")

for file in os.listdir(folder):
    if file.lower().endswith(".pdf"):
        pdf_path = os.path.join(folder, file)
        process_pdf(pdf_path)
