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


# ################### COMPONENT TO EDIT #################################
# Returns file name for generation of TIFF file
def generate_file_name(file_name, page_num):
    name = os.path.basename(file_name)
    date_part = name.replace("BlueRidgeSun_", "").replace(".pdf", "")
    page = str(page_num + 1).zfill(2)
    return os.path.join("output-files", f"SpaBRS6_{date_part}_1_{page}.tiff")


# Process for an individual page within PDF
def process_page(number, file_name):
    print(str(number + 1) + " " + file_name)

    new_file = generate_file_name(file_name, number)

    result = subprocess.run([
        "magick",
        "-density", "300",
        f"{file_name}[{number}]",
        "-depth", "8",
        new_file
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"  WARNING: page {number + 1} failed — {result.stderr.strip()}")
    else:
        print("  output: " + new_file)


# Fallback: get page count using magick identify
def get_page_count_magick(file_name):
    result = subprocess.run(
        ["magick", "identify", "-format", "%n\n", file_name],
        capture_output=True,
        text=True
    )
    # identify returns one line per page — take the last non-empty value
    lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
    if not lines:
        return None
    try:
        # Some versions repeat the count per page; the actual count is the value itself
        # Use the first token which should be total page count
        return int(lines[-1])
    except ValueError:
        return None


# Get page count using Ghostscript directly — more reliable than magick identify
def get_page_count_gs(file_name):
    result = subprocess.run(
        [
            "gswin64c",
            "-q",
            "-dNODISPLAY",
            "-dNOSAFER",
            "--permit-file-read=" + file_name,
            "-c",
            f"({file_name}) (r) file runpdfbegin pdfpagecount = quit"
        ],
        capture_output=True,
        text=True
    )
    try:
        return int(result.stdout.strip())
    except ValueError:
        return None


# Process individual PDF
def process_pdf(file_name):
    print("Processing File: " + file_name)

    # Try Ghostscript first, fall back to magick identify
    pages = get_page_count_gs(file_name)
    if pages is None:
        print("  GS page count failed, trying magick identify...")
        pages = get_page_count_magick(file_name)
    if pages is None:
        print(f"  ERROR: could not determine page count for {file_name}, skipping.")
        return

    print(f"  Pages: {pages}")

    for x in range(pages):
        process_page(x, file_name)


# ################### COMPONENT TO EDIT #################################
# Start Main Script and loop through all PDF files
input_folder = "SpaBRS6"
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
