from pypdf import PdfReader
import fitz  # PyMuPDF
import os
import re 

# === Ρυθμίσεις ===
pdf_path = "Color_Atlas_of_Forensic_Medicine_and_Patholo.pdf"
output_dir = "extracted_images"
keyword_to_search = "gun"  # <-- Εδώ αλλάζεις τη λέξη αναζήτησης

# === Βήμα 1: Άνοιγμα PDF ===
reader = PdfReader(pdf_path)
doc = fitz.open(pdf_path)
os.makedirs(output_dir, exist_ok=True)

# === Βήμα 2: Extract εικόνων και περιγραφών ===
img_count = 0
for page_index in range(len(doc)):
    page = doc[page_index]
    text = page.get_text("text")
    image_list = page.get_images(full=True)
    
    print(f"[Page {page_index+1}] Found {len(image_list)} images.")
    
    for img_index, img in enumerate(image_list):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        
        image_filename = f"image_{page_index+1}_{img_index+1}.{image_ext}"
        image_path = os.path.join(output_dir, image_filename)
        
        with open(image_path, "wb") as f:
            f.write(image_bytes)
        
        print(f"✅ Saved: {image_filename}")
        
        # Απόπειρα εξαγωγής περιγραφής εικόνας (απλά δείγμα: παίρνουμε 300 χαρακτήρες από το κείμενο της σελίδας)
        snippet = text.strip().replace("\n", " ")
        snippet = snippet[:300] + "..." if len(snippet) > 300 else snippet
        print(f"📝 Possible caption (Page {page_index+1}): {snippet}\n")
        
        img_count += 1

print(f"\n✅ Total images extracted: {img_count}")

# === Βήμα 3: Αναζήτηση λέξης σε όλο το PDF ===
print(f"\n🔍 Searching for pages containing the word: '{keyword_to_search}'\n")
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text and keyword_to_search.lower() in text.lower():
        print(f"🔎 Found on Page {i+1}:\n{text[:500]}...\n")  # Εμφάνιση 500 πρώτων χαρακτήρων
