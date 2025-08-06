import json

# Load original merged JSON
with open("Integrated_management_child_illness.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Unwanted top-level keys
UNNECESSARY_KEYS = [
    "status", "originalOrientationAngle", "links", "width", "height",
    "triggeredAutoMode", "parsingMode", "structuredData",
    "noStructuredContent", "noTextContent",
    "pageHeaderMarkdown", "pageFooterMarkdown"
]

def clean_page(page):
    # Remove top-level junk keys
    for key in UNNECESSARY_KEYS:
        page.pop(key, None)

    # Clean bbox from items
    if "items" in page:
        for item in page["items"]:
            item.pop("bBox", None)

    # Clean images
    if "images" in page:
        for img in page["images"]:
            for key in ["x", "y", "width", "height", "original_width", "original_height"]:
                img.pop(key, None)

    return page

# Apply to all pages
cleaned_pages = [clean_page(p) for p in data["pages"]]

# Save cleaned file
with open("Cleaned_Integrated_management.json", "w", encoding="utf-8") as out:
    json.dump({"pages": cleaned_pages}, out, indent=2, ensure_ascii=False)

print(f"✅ All unwanted fields removed. Output → Cleaned_Integrated_management.json")
