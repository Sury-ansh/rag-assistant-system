import streamlit as st
from pdf_reader import read_pdf
import regex as re
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import mongo_connect as mg
import RAG as rg

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

def upload_pdf(model):
    st.subheader('Upload a file or document (only supporting text document currently)')
    uploaded_file = st.file_uploader('Choose a PDF file',type=['pdf'])
    col_name = st.text_input('Enter collection name')
    if st.button('Upload and Process'):
        if uploaded_file and col_name:
            with st.spinner('Processing file...'):
                content = read_pdf(uploaded_file)
                if content.startswith("Error reading pdf"):
                    st.error(content)
                    return
                content = re.sub(r'\s+', ' ', content).strip()
                chunks=chunks_text(content)
                embeddings = model.encode(chunks, show_progress_bar=True)
                collection = mg.getCollection(col_name)
                for i, (chunk,embedding) in enumerate(zip(chunks,embeddings)):
                    document = {
                        'source': uploaded_file.name,
                        'chunk_size': i,
                        'text': chunk,
                        'embedding': embedding
                    }
                    collection.insert_one(document)
                st.success(f'All the chunks {len(chunks)} and embedding stored in collection {collection.name}')



        else:
            st.error('Either collection name is empty or no file being uploaded')

def query_document(llm,model):
    st.subheader('Query Existing Query')
    collection_list = mg.getCollectionList()
    if not collection_list:
        st.warning('No Collection Found !!!')
        return
    existing_name = st.selectbox('Select one collection',collection_list)
    user_query = st.text_input('Enter your query:')
    if st.button('Submit Query'):
        if user_query and existing_name:
            embedded_query = rg.encodeQuery(user_query,model)
            document_list = rg.docFinder(mg.getCollection(existing_name))
            result = rg.searchVector(document_list,embedded_query)
            response = rg.generateResponse(user_query,result,llm)
            st.write('**Response**')
            st.write(response)

        else:
            st.error('Select both query and collection name')


def main():
    st.title('AI-Powered Knowledge Assitant')
    with st.spinner('Loading models... Please wait ⏳'):
        model = SentenceTransformer('all-MiniLM-L6-v2')
        llm = pipeline('text-generation', model='distilgpt2', max_new_tokens=100)
    st.success('Models loaded successfully! 🚀')
    option = st.radio('Select your choice',['Upload a new document','Choose from existing document'])
    if option == 'Upload a new document':
        upload_pdf(model)
    else:
        query_document(llm,model)

if __name__ == "__main__":
    main()