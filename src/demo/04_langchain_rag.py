import dotenv
import lancedb
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores.lancedb import LanceDB
from opentelemetry import trace
from demo import otel

if __name__ == "__main__":
    dotenv.load_dotenv()

    otel.init_otel_tracing()
    otel.init_instrumentation()

    uri = "data/sample-lancedb"
    db = lancedb.connect(uri)

    llm = OpenAI()
    prompt = PromptTemplate.from_template("""
    human
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:
    """)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    docsearch = LanceDB(
        connection=db,
        embedding=embeddings,
        table_name="demo_gutenberg",
        vector_key="embedding",
        text_key="content",
    )
    retriever = docsearch.as_retriever()

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    tracer = trace.get_tracer(__name__)

    user_query = "who is the author of BELGIAN FAIRY TALES?"
    with tracer.start_as_current_span(user_query):
        print(rag_chain.invoke(user_query))

    user_query = "what is the capital of Belgium?"
    with tracer.start_as_current_span(user_query):
        print(rag_chain.invoke(user_query))
