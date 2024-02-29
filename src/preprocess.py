import spacy
from collections import Counter
import re


def data_preprocessor(reader):
    nlp = spacy.load('en_core_web_sm')
    pages_data = []
    for i in range(100):
        text = reader.pages[i].extract_text()
        if text is None:
            continue
        text = re.sub(r'(?:\[\d+\]\nNOTES\n| \n|-  \n)', '', text)
        text = text.lower()
        doc = nlp(text)
        entities = [ent.text for ent in doc.ents if not ent.text.isspace()]
        keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'VERB', 'ADJ'] and not token.is_stop]
        word_tokens = [token.text for token in doc if not token.is_punct and not token.text.isspace()]
        sentence_tokens = [sentence.text for sentence in doc.sents]
        page_data = {
            'original_page_number': i + 1,
            'text': text,
            'word_tokens': word_tokens,
            'sentence_tokens': sentence_tokens,
            'entities': Counter(entities),
            'keywords': Counter(keywords),
            'length': len(word_tokens)
        }
        pages_data.append(page_data)
        
    return pages_data