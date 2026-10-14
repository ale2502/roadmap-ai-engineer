from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = ["dog", "puppy", "invoice"]
vectors = model.encode(texts)

print(vectors.shape)
print(util.cos_sim(vectors[0], vectors[1]))
print(util.cos_sim(vectors[0], vectors[2]))
