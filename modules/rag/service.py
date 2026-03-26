from sentence_transformers import SentenceTransformer

async def retrieve_context(
    query: str,
    top_k: int,
    collection,
    embedding_model: SentenceTransformer
    ) -> tuple[str, list[str]]:
    embedded_query = embedding_model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=embedded_query,
        n_results=top_k
        )
    docs = results["documents"][0] if results["documents"] else []

    return "\n\n".join(docs), docs

async def query(
    query: str,
    top_k: int,
    collection,
    embedding_model: SentenceTransformer,
    generative_model
    ) ->tuple[str, list[str]]:

    context, chunks = await retrieve_context(query, top_k, collection, embedding_model)
    prompt = f"""Use the context below to answer the question. Be concise and specific.
              use line break if width exceeds 800px.
              If the answer isn't in the context, say so.

              Context:
              {context}

              Question: {query}

              Answer:"""

    response = await generative_model.generate_content_async(prompt)
    return response.text, chunks