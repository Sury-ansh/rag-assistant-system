from pdf_reader import read_pdf
import tkinter as tk
from tkinter import filedialog
import re 
from sentence_transformers import SentenceTransformer
import mongo_connect as mg
import RAG as rag
from transformers import pipeline

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
    model=SentenceTransformer('all-MiniLM-L6-v2')
    llm=pipeline('text-generation',model='distilgpt2', max_new_tokens=100)
    print('Select 1 option out of two:\n1. Upload a new document\n2. Select from given documents: ')
    print(f"List of documents avaialble:\n{mg.getCollectionList()}")
    inp=int(input('\nEnter a number:'))
    while inp > 0:

        if inp == 1:
            root=tk.Tk()
            root.withdraw()
            pdf_path=filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("PDF files","*.pdf")]
            )
            if not pdf_path:
                print("Not a valid path")
                return
            content=read_pdf(pdf_path)
            content = re.sub(r'\s+', ' ', content).strip()
            chunks=chunks_text(content)
            
            embeddings=model.encode(chunks,show_progress_bar=True)
            col_name=input('\nEnter the name of storage')
            collection=mg.getCollection(col_name)
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                document = {
                    'source': pdf_path,
                    'chunk_index': i,
                    'text': chunk,
                    'embedding': embedding.tolist()  
                    }
                collection.insert_one(document)
            print("All chunks and embeddings stored in MongoDB")
            inp=int(input('\nEnter a number: '))
        elif inp == 2:
            existing_name=input('\nEnter the collection name: \n')
            if existing_name.lower() in [name.lower() for name in mg.getCollectionList()]:
                while True:
                    userQuery=input('\nEnter your query or exit() for exit: \n')
                    if(userQuery.strip() == 'exit()'):
                        break

                    embedded= rag.encodeQuery(userQuery,model)
                    documentList=rag.docFinder(mg.getCollection(existing_name))
                    result=rag.searchVector(documentList,embedded)
                    print(rag.generateResponse(userQuery,result,llm))
            inp=int(input('\nEnter a number: '))
        else :
            inp=int(input('\nWrong choice entered\nAgain select a choice from 1 or 2 else select 0 to end'))


                

    

    
    


if __name__=="__main__":
    main()