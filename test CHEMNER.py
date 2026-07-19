import spacy

nlp = spacy.load("en_chemner")

text = "what is aluminium powder?"

doc = nlp(text)

print("Number of entities:", len(doc.ents))

for ent in doc.ents:
    print("TEXT:", ent.text)
    print("LABEL:", ent.label_)


texts = [
    "acetone",
    "ethanol",
    "benzene",
    "sulfuric acid",
    "aluminium powder"
]

for text in texts:
    doc = nlp(text)

    print("\nInput:", text)

    for ent in doc.ents:
        print(ent.text, ent.label_)