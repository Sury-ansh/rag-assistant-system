import numpy as np

TOP_K=5

def cosineSimilarity(a,b):
    a=np.array(a)
    b=np.array(b)
    return np.dot(a,b) / np.linalg.norm(a) * np.linalg.norm(b)

def searchVector(document,queryEmbedding):
    result=[]
    for doc in document:
        score=cosineSimilarity(queryEmbedding,doc['embedding'])
        result.append(
            {
                'score':score,
                'text':doc['text']
            }
        )
    result=sorted(result,key=lambda x:x['score'],reverse=True)[:TOP_K]
    return result

def docFinder(collection):
    return collection.find()

def encodeQuery(userQuery,model):
    print("RAG pipeline started")
    if not userQuery.strip():
        return None
    return model.encode([userQuery])[0]

def generateResponse(userQuery,result,llm):
    context=['\n'.join(chunk['text'] for chunk in result)]
    prompt=f"Question: {userQuery}\nContext: {context}\nAnswer: "
    response =llm(prompt)
    return response
