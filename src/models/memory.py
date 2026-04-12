# memories / memory_types / memory_categories / memory_embeddings
from src.core.database import Base  # Base import

class Memory(Base):
    __tablename__ = "memories"

class MemoryType(Base):
    __tablename__ = "memory_types"

class MemoryCategory(Base):
    __tablename__ = "memory_categories"

class MemoryEmbedding(Base):
    __tablename__ = "memory_embeddings"
