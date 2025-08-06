import json
from glob import glob

# Adjust this list to your actual filenames and offsets
split_files = [
    ("WHO_1.json", 0),
    ("WHO_2.json", 100),
    ("WHO_3.json", 200),
    ("WHO_4.json", 300),
]

all_pages = []

for filename, offset in split_files:
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
        pages = data.get("pages", [])

        for page in pages:
            local_page = page.get("page", 1)
            global_page = local_page + offset

            # Replace local page with global page
            page["page"] = global_page
            page["source_part"] = filename

            # Update image names to global version
            if "images" in page:
                for img in page["images"]:
                    img["name"] = f"page_{global_page}.jpg"

            all_pages.append(page)

# Save the merged output
with open("clean_merged_pages.json", "w", encoding="utf-8") as out:
    json.dump({"pages": all_pages}, out, indent=2, ensure_ascii=False)

print(f"✅ Merged and cleaned {len(all_pages)} pages into 'clean_merged_pages.json'")
