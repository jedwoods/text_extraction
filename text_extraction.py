import fitz
import jsonlines

def separate_text_to_jsonl(pdf_path, output_path):
    """Use PyMuPDF to extract text from a PDF file and save it to a JSONL file with coordinates, direction, and page number"""
    doc = fitz.open(pdf_path)
    
    with jsonlines.open(output_path, mode='w') as writer:
        for page_num, page in enumerate(doc):
            blocks = page.get_text("dict", flags=0)["blocks"]
            
            for block_index, block in enumerate(blocks):
                lines = block["lines"]
                for line_index, line in enumerate(lines):
                    text = line["spans"][0]["text"]
                    direction = line["dir"]
                    x0, y0, x1, y1 = line["bbox"]  # Extract the coordinates
                    
                    data = {
                        "page": page_num + 1,
                        "line": line_index + 1,
                        "direction": "horizontal" if direction == (1.0, 0.0) else "vertical",
                        "text": text,
                        "x0": x0,  # Add the x-coordinate
                        "y0": y0,  # Add the y-coordinate
                        "x1": x1,  # Add the x-coordinate
                        "y1": y1   # Add the y-coordinate
                    }
                    writer.write(data)

    print(f"Text extracted and saved to {output_path}")
if __name__ == "__main__":
# Specify the input PDF file path and output JSONL file path
    pdf_path = "/app/product-name/opendir/pdfjson/test_files/2023-PERSONAL INSURANCE ADDITIONAL COMPENSATION AGREEMENT.pdf"
    output_path = "2023_bonus_output.jsonl"

    # Call the separate_text_to_jsonl function
    separate_text_to_jsonl(pdf_path, output_path)
