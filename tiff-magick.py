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

# Process individual PDF
def process_pdf(file_name):
    print(file_name)
    result = subprocess.run(
        # This is a string locator test
        # ["magick", "identify", "\"" + file_name + "\""],
        ["magick", "identify", file_name],
        capture_output=True,
        text=True
    )
    pages = int(len(result.stdout.splitlines()))
    for x in range(pages):
        process_page((x + 1), file_name)


# Process for an individual page within pdf
def process_page(number, file_name):
    print(str(number) + " " + file_name)
    if number == 2:
        # Remember 2 is actually the THIRD item in the index. TODO: Fix this logic.
        subprocess.run([
            "magick",
            "-density", "300",
            f"{file_name}[{number}]",
            # TODO: Figure out how to algorithmically fix this line
            "test.tiff"
        ])


# Start Main Script and loop through all PDF files
folder = "input-files"
for file in os.listdir(folder):
    if file.lower().endswith(".pdf"):
        pdf_path = os.path.join(folder, file)
        process_pdf(pdf_path)
