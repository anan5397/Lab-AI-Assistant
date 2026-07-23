from rag import search_chroma

question = "Tell me about Enzymes"

results = search_chroma(question)

print(results)

