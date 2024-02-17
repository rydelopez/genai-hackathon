# Initializes a Redis connection

import os
import json
import requests
import weaviate

import time


class WeaviateVDB:
    def __init__(self):
        """Initialize settings for Weaviate server"""
        self.WEAVIATE_URL = os.environ["WEAVIATE_URL"]
        self.client = weaviate.Client(
            url=self.WEAVIATE_URL,
        )

        # Create a "class" (basically a table)
        try:
            class_obj = {
                "class": "Documents",
                "vectorizer": "text2vec-transformers",  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
                "moduleConfig": {
                    "text2vec-transformers": {},
                },
            }
            self.client.schema.create_class(class_obj)
        except:
            # We reach here if the class has already been created
            pass

    def query_documents(self, user_query: str, lesson_id: str) -> str:
        """Given a user query, returns the most relevant document

        This is the method that should be finished for the task "Vector database: search"
        """
        try:
            response = (
                self.client.query.get("Document", ["content"])
                .with_where(
                    {
                        "path": ["lesson_id"],
                        "operator": "Equal",
                        "valueText": lesson_id,
                    }
                )
                .with_near_text({"concepts": ["test hello"]})
                .with_limit(1)
                .do()
            )
            return response["data"]["Get"]["Document"][0]["content"]
        except:
            return "..."
