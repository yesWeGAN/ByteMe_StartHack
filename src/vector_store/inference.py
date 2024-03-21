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
from sentence_transformers import SentenceTransformer
import scipy

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
        self.clear_snippets = self.find_jsonfile(regex="snippets")
        self.contact_persons = self.find_jsonfile(regex="contacts")

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

    def find_jsonfile(self, regex: str):
        """This is the method that loads the json-files that correspond to the built index.
        They contain the clear text snippets, and whatever else is listed (contact person)

        Args:
            regex (str): identify which file you're looking for. 

        Returns:
            _type_: JSON-filecontent (list)
        """
        try:
            filep = next(Path(self.dataset).rglob(f"*{regex}s*.json"))
            return json.load(open(filep, "r"))
        except StopIteration:
            raise FileNotFoundError(f"No json file found for regex {regex}. Exiting.")

    def embed_query(self, query: str, max_tokens: int):
        embedded_query = self.embedder.encode(query, convert_to_tensor=True)
        return embedded_query.cpu().numpy()
    
    def search_full_index(self, vectors, k):
        self.index.nprobe = 80
        distances, neighbors = self.index.search(vectors, k)
        return distances, neighbors
    
    def run_inference(self, query: str, max_tokens: int = 50, k=5):
        """under construction still"""
        query_tensor = self.embed_query(query=query, max_tokens=max_tokens)
        dist, neighbors = self.search_full_index(query_tensor, k)
        jsonf = self.find_jsonfile()    # this is the matching from an index in the search-index to a file / question / topic / department
        knn_imagepaths = [Path(jsonf[str(neighbor)]) for neighbor in neighbors[0]]


class KNNSimpleInference:
    def __init__(self, inputpath:str, outputpath=None, index_of_what: str = "q"):
        """Class is essentially the same as the one above, yet it does iteration over stacked embedding KB, not index building for inference.
        Index of what: irrelevant, in this inference scenario only questions get embedded and matched.
        """
        self.inputpath = Path(inputpath)
        if outputpath:
            self.outputpath = Path(outputpath)
            os.makedirs(self.outputpath, exist_ok=True)
        else:
            self.outputpath = self.inputpath
        self.writepath = os.path.join(self.inputpath.parent, "index")
        self.vectors = self.load_stacked_tensors(regex=index_of_what)
        self.clear_input_questions = self.load_json(regex="questions")
        self.clear_input_answers = self.load_json(regex="answers")
        self.embedder = self._setup_embedder(model_identifier="multilingual-e5-large-instruct", max_tokens=500)

    def load_stacked_tensors(self, regex: str):
        """This is here to load a stack of tensors (embedded strings from LLM)"""
        try:
            tensor_stack_file = next(
                iter(Path(self.inputpath).rglob(f"{regex}_embed_stack.pt"))
            )
            return torch.load(tensor_stack_file)
        except:
            print(f"No tensor stack file found for: {regex}_embed_stack.pt")

    def load_json(self, regex: str):
        """Load a json-file that contains the clear-text questions/answers (not the embeds)

        Args:
            regex (str): indication if to load the questions or answers

        Returns:
            _type_: JSON file content.
        """
        try:
            json_file = next(iter(Path(self.inputpath).rglob(f"*{regex}*.json")))
            return json.load(open(json_file, "r"))
        except:
            print(f"No json file found for: {regex}*.json")

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

    def inference(self, query: str, k=5, printprop=True):
        """Inference iterating over a stack of embeddings. No index search.

        Args:
            query (_type_): Query string (the question.)
            k (int, optional): Number of samples to return. Defaults to 5.

        Returns:
            _type_: Thruple of lists: List of Answers (str), List Of Questions (str), List of distances (float)
        """
        queries = [query]
        query_embeddings = self.embedder.encode(queries)
        for query, query_embedding in zip(queries, query_embeddings):
            distances = scipy.spatial.distance.cdist([query_embedding], self.vectors, "cosine")[0]

            results = zip(range(len(distances)), distances)
            results = sorted(results, key=lambda x: x[1])
            if printprop:
                print("\n\n======================\n\n")
                print("Query:", query)
                print("\nTop 5 most similar sentences in corpus:")
            result_distances = []
            result_questions = []
            # result_answers = []
            for idx, distance in results[0:k]:
                if printprop:
                    print(f"The cosine similarity score for the following Q-A-pair is: {(1-distance)})")
                    print(self.clear_input_questions[idx].strip())
                    print(self.clear_input_answers[idx].strip())
                result_distances.append(1-distance)
                result_questions.append(self.clear_input_questions[idx].strip())
                #result_answers.append(self.clear_input_answers[idx].strip())
            
        return None, result_questions, result_distances
            
# TODO: 
raw_data_path = "src/raw_stacks"
simpleInf = KNNSimpleInference(    inputpath=raw_data_path,
    outputpath="src/index_files",
    index_of_what='q'
)
simpleInf.inference(query="Ich werde beschuldigt, kann ich einen Anwalt einschalten?", k=5)