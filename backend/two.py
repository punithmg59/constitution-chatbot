import re
import pickle
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss

# =========================
# STEP 1: LOAD PDF
# =========================
print("📥 Reading PDF...")

reader = PdfReader("constitution1.pdf")
raw_text = ""

for page in reader.pages:
    text = page.extract_text()
    if text:
        raw_text += text + "\n"

with open("constitution_raw.txt", "w", encoding="utf-8") as f:
    f.write(raw_text)

print("✅ Raw text extracted")


# =========================
# STEP 2: CLEAN TEXT
# =========================
print("🧹 Cleaning text...")

clean_text = raw_text

# remove extra spaces
clean_text = re.sub(r"\s+", " ", clean_text)

# remove page numbers like (i), (ii), etc.
clean_text = re.sub(r"\(\w+\)", "", clean_text)

# remove unwanted words
clean_text = clean_text.replace("Contents", "")
clean_text = clean_text.replace("THE CONSTITUTION OF INDIA", "")

with open("constitution_clean.txt", "w", encoding="utf-8") as f:
    f.write(clean_text)

print("✅ Clean text saved")


# =========================
# STEP 3: CHUNKING (ARTICLE BASED)
# =========================
print("✂️ Splitting into articles...")

articles = re.split(r"Article\s+\d+", clean_text)

# remove small/empty chunks
articles = [a.strip() for a in articles if len(a) > 100]

print(f"✅ Total useful chunks: {len(articles)}")


# =========================
# STEP 4: EMBEDDINGS
# =========================
print("🔢 Creating embeddings...")

model = SentenceTransformer('all-MiniLM-L6-v2')

embeddings = model.encode(articles)

print("✅ Embeddings created")


# =========================
# STEP 5: FAISS INDEX
# =========================
print("🗄️ Creating FAISS index...")

dimension = len(embeddings[0])
index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings))

print(f"✅ Stored {index.ntotal} vectors")


# =========================
# STEP 6: SAVE FILES
# =========================
print("💾 Saving files...")

faiss.write_index(index, "constitution_index.bin")

with open("articles.pkl", "wb") as f:
    pickle.dump(articles, f)

print("✅ Saved:")
print(" - constitution_clean.txt")
print(" - articles.pkl")
print(" - constitution_index.bin")


# =========================
# STEP 7: TEST SEARCH
# =========================
print("\n🔍 Testing search...\n")

query = "What is Article 21?"

query_embedding = model.encode([query])

D, I = index.search(query_embedding, k=3)

results = [articles[i] for i in I[0]]

for i, r in enumerate(results):
    print(f"\nResult {i+1}:")
    print(r[:500])  # print first 500 chars


print("\n🚀 Phase 1 COMPLETE!")