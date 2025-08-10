from pdf_reader import read_pdf
import tkinter as tk
from tkinter import filedialog
import re 
from sentence_transformers import SentenceTransformer
from mongo_connect import getCollection

def chunks_text(text,chunk_size=500,overlap=50):
    chunks=[]
    start=0
    text_length=len(text)
    while start<text_length:
        end=min(start+chunk_size,text_length)
        while end<text_length and text[end]not in [' ','\n','!','.','?']:
            end+=1
        chunk=text[start:end].strip()
        if(chunk):
            chunks.append(chunk)
        start=end-overlap if end <text_length else text_length
    return chunks

def main():
    root=tk.Tk()
    root.withdraw()

    pdf_path=filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("PDF files","*.pdf")]
    )

    if not pdf_path:
        print("suryansh")
        return
    content=read_pdf(pdf_path)
    content = re.sub(r'\s+', ' ', content).strip()
    chunks=chunks_text(content)
    model=SentenceTransformer('all-MiniLM-L6-v2')
    embeddings=model.encode(chunks,show_progress_bar=True)
    collection=getCollection('Rag-1')
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        document = {
            'source': pdf_path,
            'chunk_index': i,
            'text': chunk,
            'embedding': embedding.tolist()  
        }
        collection.insert_one(document)
    print("All chunks and embeddings stored in MongoDB")


if __name__=="__main__":
    main()