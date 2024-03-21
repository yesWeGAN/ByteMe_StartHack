# https://davidefiocco.github.io/nearest-neighbor-search-with-faiss/
import argparse
import json
import os
import shutil
from pathlib import Path
import faiss
import numpy as np
import torch
from faiss.contrib.ondisk import merge_ondisk


class KNNIndexInference:
    def __init__(self, dataset: str, embedding_model: str = "sentence-transformers/all-MiniLM-L12-v2", max_tokens = 50, outputpath: str =None, batchsize: int=100):
        """Base class to do inference with a text-query against existing index.

        Args:
            dataset (str): The path to the pretrained index.
            embedding_model (str): Str identifier from huggingface.
            outputpath (str, optional): Dir to put the output. Defaults to None.
            batchsize (int, optional): Batchsize. Defaults to 100.
        """
        if outputpath:
            self.outputpath = Path(outputpath)
        else:
            self.outputpath = os.path.join(self.query, "knn_result")    # default output 
        self.embedder = self._setup_embedder(model_identifier=embedding_model, max_tokens=max_tokens)
        self.batchsize = batchsize
        self.dataset = dataset
        self.index = self.find_indexfile()

    def find_indexfile(self):
        try:
            indexfile = next(Path(self.dataset).rglob("populated.index"))
            return faiss.read_index(indexfile.as_posix(), faiss.IO_FLAG_ONDISK_SAME_DIR)
        except StopIteration:
            raise FileNotFoundError("No index file found. Exiting.")

    def _setup_embedder(self,model_identifier: str, max_tokens: int):
        """Setup the embedder. 

        Args:
            model_identifier (str): Identifier for huggingface model. 
            max_tokens (int): Max tokens to embed. Has a runtime impact.

        Returns:
            _type_: The embedder.
        """
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        embedder = SentenceTransformer(model_identifier)
        embedder.max_seq_length = (
            max_tokens  # quadratic increase of transformer nodes with increasing input size!
        )
        return embedder

    def find_jsonfile(self):
        try:
            filep = next(Path(self.dataset).rglob("**/filepath_index.json"))
            return json.load(open(filep, "r"))
        except StopIteration:
            raise FileNotFoundError("No json file found. Exiting.")

    def embed_query(self, query: str, max_tokens: int):
        embedded_query = self.embedder.encode(query, convert_to_tensor=True)
        return embedded_query.cpu().numpy()
    
    def search_full_index(self, vectors, k):
        self.index.nprobe = 80
        distances, neighbors = self.index.search(vectors, k)
        return distances, neighbors
    
    def run_inference(self, query: str, max_tokens: int = 50, k=5):
        query_tensor = self.embed_query(query=query, max_tokens=max_tokens)
        dist, neighbors = self.search_full_index(query_tensor, k)
        jsonf = self.find_jsonfile()    # this is the matching from an index in the search-index to a file / question / topic / department
        knn_imagepaths = [Path(jsonf[str(neighbor)]) for neighbor in neighbors[0]]
