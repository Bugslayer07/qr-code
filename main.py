import os
import requests
from pdf2image import convert_from_path

# Set up the output directory for images
output_dir = 'qr_codes'
os.makedirs(output_dir, exist_ok=True)

# Initialize the starting filename index
start_index = 1  # Start numbering from 1


# Convert the downloaded PDF to an image, then delete the PDF
def convert_pdf_to_image(pdf_path, output_dir, file_index):
    pages = convert_from_path(pdf_path, dpi=300)  # Set high DPI for quality
    for page_num, page in enumerate(pages):
        image_path = os.path.join(output_dir, f"{file_index + page_num}.png")
        page.save(image_path, "PNG")
        print(f"Converted and saved image: {image_path}")
    os.remove(pdf_path)  # Delete the PDF after conversion


# Read URLs from the file
with open('linktrain.txt', 'r') as file:
    urls = [ line.strip() for line in file if line.strip() ]

# Download each QR code as a PDF, then convert to PNG and delete the PDF
for index, url in enumerate(urls):
    file_index = start_index + index
    pdf_path = os.path.join(output_dir, f"{file_index}.pdf")

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check if the request was successful

        # Save the content as a PDF temporarily
        with open(pdf_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded PDF: {pdf_path}")

        # Convert the downloaded PDF to high-resolution PNG(s) and delete the PDF
        convert_pdf_to_image(pdf_path, output_dir, file_index)

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")
