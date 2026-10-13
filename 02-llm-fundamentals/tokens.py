import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

text = "Olá meu nome é Alessandro"
ids = enc.encode(text)
print(ids)

for id in ids:
  print(enc.decode([id]))