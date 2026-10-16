from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

texts = ["I deposited money at the bank.", "We sat on the bank of the river.", "I put cash into my account"]
vectors = model.encode(texts)

print(vectors.shape)
print(util.cos_sim(vectors[0], vectors[1]).item())
print(util.cos_sim(vectors[0], vectors[2]).item())
print(util.cos_sim(vectors[1], vectors[2]).item())
