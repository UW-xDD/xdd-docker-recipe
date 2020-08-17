import glob
import spacy
from os import path

nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")

for doc in glob.glob("/input/*.txt"):
    with open(path.join("/output/", path.basename(doc).replace(".txt", "_gpe.txt")), "w") as fout:
        with open(doc) as fin:
            doc = nlp(fin.read())
            for ent in doc.ents:
                if ent.label_ == "GPE":
                    print(ent.text, ent.start_char, ent.end_char, ent.label_)
                    fout.write(f"{ent.text}\n")

