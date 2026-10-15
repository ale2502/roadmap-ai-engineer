from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

texts = ["invoice", "fatura", "fatura de energia", "cobrança", "boleto"]
vectors = model.encode(texts)

print(vectors.shape)

for i in range(1, len(texts)):
    print("invoice -", texts[i], util.cos_sim(vectors[0], vectors[i]).item())
