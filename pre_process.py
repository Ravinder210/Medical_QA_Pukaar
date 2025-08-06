import json

def extract_page_level_chunks(pages):
    chunks = []

    for page in pages:
       
        page_num = page.get("page", -1)
        md = page.get("md").strip()
        items = page.get("items", [])

        # Find first value 
        first_value = None
        for item in items:
            if item.get("value"):
                first_value = item["value"].strip()
                break


        
        chunk = {
            "content": f"{first_value}\n\n{md}" if first_value else md,
            "metadata": {
                "source": "POCKET BOOK OF Hospital care",
                "page": page_num,
                "section": first_value 
            }
        }
        chunks.append(chunk)

    return chunks

# Load your JSON file
with open("parsed_pdf/fully_cleaned_pages.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract the simplified page chunks
page_chunks = extract_page_level_chunks(data["pages"])

# Save to .jsonl
with open("page_chunks_Pocket_book_of_hospital_care.jsonl", "w", encoding="utf-8") as f:
    for chunk in page_chunks:
        f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

print(f"✅ Extracted {len(page_chunks)} page-level chunks to 'page_chunks_Pocket_book_of_hospital_care.jsonl'")
