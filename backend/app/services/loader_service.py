import faiss
import pickle
import os
from sentence_transformers import SentenceTransformer
from app.utils.logger import logger


class Loader:
    def __init__(self):
        self.model = None
        self.index = None
        self.articles = None

        # 🔥 Absolute base path (very important)
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.data_path = os.path.join(self.base_dir, "data")

    def load(self):
        try:
            logger.info("🔄 Loading embedding model...")
            self.model = SentenceTransformer("all-MiniLM-L6-v2")

            # ✅ Build correct file paths
            index_path = os.path.join(self.data_path, "constitution_index.bin")
            articles_path = os.path.join(self.data_path, "articles.pkl")

            # 🔍 Debug (optional)
            logger.info(f"Index path: {index_path}")
            logger.info(f"Articles path: {articles_path}")

            # ✅ Check files exist
            if not os.path.exists(index_path):
                raise FileNotFoundError(f"FAISS index not found: {index_path}")

            if not os.path.exists(articles_path):
                raise FileNotFoundError(f"Articles file not found: {articles_path}")

            logger.info("📦 Loading FAISS index...")
            self.index = faiss.read_index(index_path)

            logger.info("📚 Loading articles...")
            with open(articles_path, "rb") as f:
                self.articles = pickle.load(f)

            logger.info("✅ All resources loaded successfully")

        except Exception as e:
            logger.error(f"❌ Loader error: {e}")
            raise RuntimeError("Failed to load system")


# global instance
loader = Loader()