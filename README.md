# Covid19NER
My research on Named Entity Recognition on CORD-19 dataset

Spacy NER model for CoVID-19 entities: [download](https://drive.google.com/file/d/1xokPqcHkFbzAAgJlog_wYch4bMVevsQZ/view?usp=sharing)

Scispacy NER model for CoVID-19 entities: [download](https://drive.google.com/file/d/1I1ok6Xvx0gmmrRaZWHPYBnOBk59vlJ7G/view?usp=sharing)
## Installation
```
pip install en_model0-0.0.0.tar.gz
```
Model will be installed into pip and can be loaded as 'en_model0'

## Load model:
```
import en_model0
nlp = en_model0.load()
text = 'The Tokyo Metropolitan Government confirmed 218 new cases of coronavirus infection as of 3 p.m. on Saturday.'
doc = nlp(text)
```

## Use model to extract CORONAVIRUS entities:
```
#print entities
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)
```

Output:

The Tokyo Metropolitan 0 22 CHEMICAL

218 44 47 CARDINAL

coronavirus 61 72 CORONAVIRUS

3 p.m. 89 95 QUANTITY

Saturday 99 107 DATE

# References

