import dotenv
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import lancedb
from lancedb.pydantic import Vector, LanceModel
from demo import otel


class ArticleMetadata(LanceModel):
    source: str


class Article(LanceModel):
    content: str
    metadata: ArticleMetadata
    embedding: Vector(3072)


if __name__ == "__main__":
    dotenv.load_dotenv()

    otel.init_otel_tracing()
    otel.init_instrumentation()

    urls = ["https://www.gutenberg.org/ebooks/67256.txt.utf-8"]
    loader = UnstructuredURLLoader(urls=urls, show_progress_bar=True)
    data = loader.load()
    documents = CharacterTextSplitter().split_documents(data)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    document_texts = [doc.page_content for doc in documents]
    document_embeddings = embeddings.embed_documents(document_texts)
    articles = [
        Article(
            content=pair[0],
            embedding=pair[1],
            metadata=ArticleMetadata(source="Gutenberg"),
        )
        for pair in zip(document_texts, document_embeddings)
    ]

    uri = "data/sample-lancedb"
    db = lancedb.connect(uri)
    table = db.create_table("demo_gutenberg", schema=Article, mode="overwrite")
    table.add(articles)
