import pandas as pd
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient, models
from tqdm import tqdm


# Refactored class from the https://github.com/stanford-oval/storm/tree/main for the purposes of this project.
class QdrantVectorStoreManager:
    """
    Helper class for managing the Qdrant vector store, can be used with `VectorRM` in rm.py.

    Before you initialize `VectorRM`, call `create_or_update_vector_store` to create or update the vector store.
    Once you have the vector store, you can initialize `VectorRM` with the vector store path or the Qdrant server URL.
    """

    @staticmethod
    def _check_create_collection(
        client: QdrantClient, collection_name: str, model: HuggingFaceEmbeddings
    ) -> Qdrant:
        """Check if the Qdrant collection exists and create it if it does not."""
        if client is None:
            raise ValueError("Qdrant client is not initialized.")
        if client.collection_exists(collection_name=f"{collection_name}"):
            print(f"Collection {collection_name} exists. Loading the collection...")
            return Qdrant(
                client=client,
                collection_name=collection_name,
                embeddings=model,
            )
        else:
            print(
                f"Collection {collection_name} does not exist. Creating the collection..."
            )
            # create the collection
            client.create_collection(
                collection_name=f"{collection_name}",
                vectors_config=models.VectorParams(
                    size=1024, distance=models.Distance.COSINE
                ),
            )
            return Qdrant(
                client=client,
                collection_name=collection_name,
                embeddings=model,
            )

    @staticmethod
    def _init_online_vector_db(
        location: str, port: int, collection_name: str, model: HuggingFaceEmbeddings
    ) -> Qdrant:
        """Initialize the Qdrant client that is connected to an online vector store with the given URL and API key.

        Args:
            location (str): The location of the Qdrant store
        """
        try:
            client = QdrantClient(location, port=port)
            return QdrantVectorStoreManager._check_create_collection(
                client=client, collection_name=collection_name, model=model
            )
        except Exception as e:
            raise ValueError(f"Error occurs when connecting to the server: {e}")

    @staticmethod
    def _init_offline_vector_db(
        vector_store_path: str, collection_name: str, model: HuggingFaceEmbeddings
    ) -> Qdrant:
        """Initialize the Qdrant client that is connected to an offline vector store with the given vector store folder path.

        Args:
            vector_store_path (str): Path to the vector store.
        """
        if vector_store_path is None:
            raise ValueError("Please provide a folder path.")

        try:
            client = QdrantClient(path=vector_store_path)
            return QdrantVectorStoreManager._check_create_collection(
                client=client, collection_name=collection_name, model=model
            )
        except Exception as e:
            raise ValueError(f"Error occurs when loading the vector store: {e}")

    @staticmethod
    def create_or_update_vector_store(
        collection_name: str,
        location: str,
        port: int,
        file_path: str,
        content_column: str,
        title_column: str = "title",
        url_column: str = "url",
        desc_column: str = "description",
        batch_size: int = 64,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
        embedding_model: str = "BAAI/bge-m3",
        device: str = "mps",
    ) -> None:
        """
        Takes a CSV file and adds each row in the CSV file to the Qdrant collection.

        This function expects each row of the CSV file as a document.
        The CSV file should have columns for "content", "title", "URL", and "description".

        Args:
            collection_name: Name of the Qdrant collection.
            location (str): Location of the Qdrant server.
            port (int): Port of the Qdrant server.
            file_path (str): Path to the CSV file.
            content_column (str): Name of the column containing the content.
            title_column (str): Name of the column containing the title. Default is "title".
            url_column (str): Name of the column containing the URL. Default is "url".
            desc_column (str): Name of the column containing the description. Default is "description".
            batch_size (int): Batch size for adding documents to the collection.
            chunk_size: Size of each chunk if you need to build the vector store from documents.
            chunk_overlap: Overlap between chunks if you need to build the vector store from documents.
            embedding_model: Name of the Hugging Face embedding model.
            device: Device to run the embeddings model on, can be "mps", "cuda", "cpu".
        """
        # check if the collection name is provided
        if collection_name is None:
            raise ValueError("Please provide a collection name.")

        model_kwargs = {"device": device}
        encode_kwargs = {"normalize_embeddings": True}
        model = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs,
        )

        if file_path is None:
            raise ValueError("Please provide a file path.")
        # check if the file is a csv file
        if not file_path.endswith(".csv"):
            raise ValueError("Not valid file format. Please provide a csv file.")
        if content_column is None:
            raise ValueError("Please provide the name of the content column.")
        if url_column is None:
            raise ValueError("Please provide the name of the url column.")

        # try to initialize the Qdrant client
        qdrant = QdrantVectorStoreManager._init_online_vector_db(
            location=location,
            port=port,
            collection_name=collection_name,
            model=model,
        )
        if qdrant is None:
            raise ValueError("Qdrant client is not initialized.")

        # read the csv file
        df = pd.read_csv(file_path)
        # check that content column exists and url column exists
        if content_column not in df.columns:
            raise ValueError(
                f"Content column {content_column} not found in the csv file."
            )
        if url_column not in df.columns:
            raise ValueError(f"URL column {url_column} not found in the csv file.")

        documents = [
            Document(
                page_content=row[content_column],
                metadata={
                    "title": row.get(title_column, ""),
                    "url": row[url_column],
                    "description": row.get(desc_column, ""),
                },
            )
            for row in df.to_dict(orient="records")
        ]

        # split the documents
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            add_start_index=True,
            separators=[
                "\n\n",
                "\n",
                ".",
                "\uff0e",  # Fullwidth full stop
                "\u3002",  # Ideographic full stop
                ",",
                "\uff0c",  # Fullwidth comma
                "\u3001",  # Ideographic comma
                " ",
                "\u200B",  # Zero-width space
                "",
            ],
        )
        split_documents = text_splitter.split_documents(documents)

        # update and save the vector store
        num_batches = (len(split_documents) + batch_size - 1) // batch_size
        for i in tqdm(range(num_batches)):
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, len(split_documents))
            qdrant.add_documents(
                documents=split_documents[start_idx:end_idx],
                batch_size=batch_size,
            )

        # close the qdrant client
        qdrant.client.close()
