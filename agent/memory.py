import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import numpy as np


class MemorySystem:
    """نظام ذاكرة هجين (محلي + سحابي)"""

    PINECONE_INDEX = "vanguard-memory"

    def __init__(self):
        self.memory_path = Path(os.getenv("VANGUARD_MEMORY_DB_PATH", "./data/memory.db"))
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)

        self.cache: List[Dict[str, Any]] = []
        self._load_cache()

        self.pinecone_index = None
        self._init_pinecone()

    def _load_cache(self):
        """تحميل الذاكرة من الملف المحلي"""
        if not self.memory_path.exists():
            return
        try:
            with open(self.memory_path, "r") as f:
                self.cache = json.load(f).get("entries", [])
        except (OSError, ValueError):
            self.cache = []

    def _save_cache(self):
        """حفظ الذاكرة في الملف المحلي"""
        with open(self.memory_path, "w") as f:
            json.dump(
                {"entries": self.cache, "updated": datetime.now().isoformat()},
                f,
                indent=2,
            )

    def _init_pinecone(self):
        """تهيئة Pinecone للبحث المتجهي"""
        api_key = os.getenv("VANGUARD_PINECONE_API_KEY")
        if not api_key:
            return

        try:
            from pinecone import Pinecone

            client = Pinecone(api_key=api_key)
            self.pinecone_index = client.Index(self.PINECONE_INDEX)
        except Exception:
            self.pinecone_index = None

    def store(
        self,
        error: str,
        solution: str,
        context: Dict[str, Any],
        vector: List[float],
    ):
        """تخزين حل جديد في الذاكرة"""
        entry = {
            "id": hashlib.md5(f"{error}{solution}".encode()).hexdigest()[:16],
            "error": error,
            "solution": solution,
            "context": context,
            "vector": vector,
            "timestamp": datetime.now().isoformat(),
            "success_count": 0,
            "failure_count": 0,
        }

        self.cache.append(entry)
        self._save_cache()

        if self.pinecone_index is not None:
            try:
                self.pinecone_index.upsert(
                    vectors=[
                        {
                            "id": entry["id"],
                            "values": vector,
                            "metadata": {"error": error, "solution": solution},
                        }
                    ]
                )
            except Exception:
                pass

    def search_similar(self, query_vector: List[float], top_k: int = 5) -> List[Dict]:
        """البحث عن حلول مشابهة باستخدام التشابه المتجهي"""
        results: List[Dict[str, Any]] = []

        query = np.array(query_vector, dtype=float)
        for entry in self.cache:
            vector = entry.get("vector") or []
            if len(vector) != len(query):
                continue

            vec = np.array(vector, dtype=float)
            if np.linalg.norm(query) == 0 or np.linalg.norm(vec) == 0:
                continue

            similarity = float(
                np.dot(query, vec) / (np.linalg.norm(query) * np.linalg.norm(vec))
            )
            results.append({**entry, "similarity": similarity})

        results.sort(key=lambda x: x["similarity"], reverse=True)

        if self.pinecone_index is not None:
            try:
                matches = self.pinecone_index.query(
                    vector=list(query_vector),
                    top_k=top_k,
                    include_metadata=True,
                ).get("matches", [])

                for match in matches:
                    if any(x["id"] == match["id"] for x in results):
                        continue
                    metadata = match.get("metadata") or {}
                    results.append(
                        {
                            "id": match["id"],
                            "error": metadata.get("error", ""),
                            "solution": metadata.get("solution", ""),
                            "similarity": match.get("score", 0.0),
                            "from_pinecone": True,
                        }
                    )
            except Exception:
                pass

        return results[:top_k]

    def record_outcome(self, entry_id: str, success: bool):
        """تسجيل نجاح/فشل الحل لتحسين التقييم"""
        for entry in self.cache:
            if entry["id"] != entry_id:
                continue
            key = "success_count" if success else "failure_count"
            entry[key] += 1
            self._save_cache()
            break

    def search_by_error(self, error: str, top_k: int = 3) -> List[Dict]:
        """البحث عن حلول لخطأ محدد (بحث نصي)"""
        error_lower = error.lower()
        results = [
            entry
            for entry in self.cache
            if error_lower in entry.get("error", "").lower()
        ]

        results.sort(key=self._success_ratio, reverse=True)

        return results[:top_k]

    @staticmethod
    def _success_ratio(entry: Dict[str, Any]) -> float:
        successes = entry.get("success_count", 0)
        failures = entry.get("failure_count", 0)
        return successes / (successes + failures + 1)
