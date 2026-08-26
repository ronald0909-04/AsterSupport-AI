from pathlib import Path
import re

from .models import DocumentChunk


class KnowledgeBaseLoader:
    def __init__(self, directory: str):
        self.directory = Path(directory)

    def load_documents(self) -> list[dict]:
        documents = []

        for path in sorted(self.directory.glob("*.md")):
            text = path.read_text(encoding="utf-8")

            metadata = {
                "title": path.stem,
                "status": "active",
                "authority": "official",
            }

            if text.startswith("---"):
                parts = text.split("---", 2)

                if len(parts) == 3:
                    front_matter = parts[1]
                    text = parts[2].strip()

                    for line in front_matter.splitlines():
                        if ":" in line:
                            key, value = line.split(":", 1)
                            metadata[key.strip()] = value.strip()

            documents.append(
                {
                    "source": path.name,
                    "title": metadata.get("title", path.stem),
                    "status": metadata.get("status", "active"),
                    "authority": metadata.get("authority", "official"),
                    "text": text,
                }
            )

        return documents

    def chunk_documents(
        self,
        documents: list[dict],
        max_words: int = 120,
    ) -> list[DocumentChunk]:

        chunks = []

        for document in documents:
            sections = re.split(
                r"\n(?=#{1,3}\s)",
                document["text"],
            )

            for section in sections:
                section = section.strip()

                if not section:
                    continue

                words = section.split()

                for start in range(0, len(words), max_words):
                    chunk_text = " ".join(
                        words[start:start + max_words]
                    )

                    chunks.append(
                        DocumentChunk(
                            source=document["source"],
                            title=document["title"],
                            text=chunk_text,
                            status=document["status"],
                            authority=document["authority"],
                        )
                    )

        return chunks