import os
import logging
import tempfile

from langchain_community.document_loaders import TextLoader, PyPDFLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from vector_store.pinecone_vectordb import PineconeStore

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class FileService:
    def __init__(self):
        self.pinecone_db = PineconeStore()

    def store_to_vectorstore(self,  file, conversation_id, user_id, namespace="memory"):

        suffix = os.path.splitext(file.filename)[1].lower()
        logger.info(f"Processing file: {file.filename} with suffix: {suffix}")

        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            file_content = file.file.read()
            logger.info(f"File size: {len(file_content)} bytes")
            tmp.write(file_content)
            tmp_path = tmp.name

        try:
            if not os.path.exists(tmp_path):
                raise RuntimeError(f"File {tmp_path} does not exist")

            file_size = os.path.getsize(tmp_path)
            logger.info(f"Temporary file created at {tmp_path}, File size: {file_size} bytes")

            if file_size == 0:
                raise ValueError(f"File {tmp_path} is empty")

            if suffix == ".txt":
                loader = TextLoader(tmp_path, encoding='utf-8')
            elif suffix == ".pdf":
                loader = PyPDFLoader(tmp_path)
            elif suffix == ".csv":
                loader = CSVLoader(file_path=tmp_path)
            else:
                raise ValueError(f"Unsupported file format: {suffix}")

            logger.info(f"Using loader: {type(loader).__name__}")

            try:
                raw_docs = loader.load()
                logger.info(f"Loaded {len(raw_docs)} documents")

                if not raw_docs:
                    raise ValueError(f"No documents loaded")

            except Exception as load_err:
                logger.error(f"Loader failed: {str(load_err)}")
                logger.error(f"Loader type: {type(loader).__name__}")
                logger.error(f"File path: {tmp_path}")
                logger.error(f"File exists: {os.path.exists(tmp_path)}")
                raise RuntimeError(
                    f"Failed to load document with {type(loader).__name__}: {str(load_err)}") from load_err

            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            docs = splitter.split_documents(raw_docs)
            logger.info(f"Split document size: {len(docs)} into chunks")

            for doc in docs:
                doc.metadata.update({"user_id": user_id, "conversation_id": conversation_id})

            self.pinecone_db.upsert(docs, namespace=namespace)
            logger.info(f"Upserted {len(docs)} documents successfully")

        except Exception as e:
            logger.error(f"Error in store_to_vectorstore: {str(e)}")
            raise

        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
                logger.info(f"Cleaned up temporary file at {tmp_path}")
