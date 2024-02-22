import streamlit as st

import spacy

from spacy.lang.en.stop_words import STOP_WORDS

from string import punctuation

import re

def original_text(text):

    stopwords= list(STOP_WORDS)
    #print(stopwords)

    nlp = spacy.load("en_core_web_sm")
    document = nlp(text)
    #print(document)

    # Tokenization process !!!!!!!!!
    tokens = [token.text for token in document]
    #print(tokens)

    # Calculating frequency of each word !!!!!!!!
    word_frequency = {}
    for word in document:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation and word.text.lower() != "\n" and word.text.lower() != "\n\n":
            if word.text not in word_frequency.keys():
                word_frequency[word.text]=1
            else:
                word_frequency[word.text]+=1

    #print(word_frequency)

    # Finding maximum frequency !!!!!!!
    max_frequency = max(word_frequency.values())
    #print(max_frequency)

    # Finding normalized frequency !!!!!!!
    for word in word_frequency.keys():
        word_frequency[word] = word_frequency[word]/max_frequency
    #print(word_frequency)

    sentence_tokens = [sent for sent in document.sents]
    #print(sentence_tokens)

    # Calculating sentence scores
    sentence_score = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text in word_frequency.keys():
                if sent not in sentence_score.keys():
                    sentence_score[sent] = word_frequency[word.text]
                else:
                    sentence_score[sent] += word_frequency[word.text]

    #print(sentence_score)

    # Generating Summary according to length and score
    new_dict = sentence_score.copy()
    summary = ""
    for key,value in new_dict.items():
        if value >= 1.5:
            summary = summary + str(key)

    #print(summary)

    # Converting Summary into one paragraph
    Text_processed = re.compile(r"\n+")
    Final_summary = Text_processed.sub(" ", summary).strip()

    return Final_summary
    

st.title("Summarize Your Document !!!")
text = st.text_area("Enter the Text")
if st.button("Summarize"):
    if len(text)<100:
        st.write("Enter Valid Text (Atleast 100 words)")
    else:  
        st.write("Generated Summary:")
        result=original_text(text)
        st.write(result)

