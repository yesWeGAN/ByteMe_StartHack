
import argparse
import json
import os
import shutil
from pathlib import Path
import faiss
import numpy as np
import torch
from faiss.contrib.ondisk import merge_ondisk



class KNNIndexTrainer:
    def __init__(self, inputpath, batchsize, outputpath=None, index_of_what: str = "q"):
        self.inputpath = Path(inputpath)
        if outputpath:
            self.outputpath = Path(outputpath)
            os.makedirs(self.outputpath, exist_ok=True)
        else:
            self.outputpath = self.inputpath
        self.writepath = os.path.join(self.inputpath.parent, "index")
        self.vectors = self.load_stacked_tensors(regex=index_of_what)
        self.clear_input_questions = self.load_json(regex="questions")
        self.clear_paths = self.load_json(regex="paths")
        self.index = faiss.index_factory(self.vectors.shape[1], "IVF50,Flat")
        self.batchsize = batchsize

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

    def train_index(self):
        self.index.train(self.vectors[0 : self.batchsize])

    def write_index(self, filename="trained.index"):
        os.makedirs(self.writepath, exist_ok=True)
        faiss.write_index(self.index, os.path.join(self.writepath, filename))

    def read_index(self, filename="trained.index"):
        self.index = faiss.read_index(os.path.join(self.writepath, filename))

    def build_index(self):
        self.train_index()
        self.write_index()
        n_batches = self.vectors.shape[0] // self.batchsize
        for i in range(n_batches):
            self.read_index()
            self.index.add_with_ids(
                self.vectors[i * self.batchsize : (i + 1) * self.batchsize],
                np.arange(i * self.batchsize, (i + 1) * self.batchsize),
            )
            self.write_index(f"block_{i}.index")
        self.read_index()
        block_fnames = [
            os.path.join(self.writepath, f"block_{b}.index") for b in range(n_batches)
        ]
        merge_ondisk(
            self.index,
            block_fnames,
            os.path.join(self.writepath, "merged_index.ivfdata"),
        )
        self.write_index("populated.index")
        for block in block_fnames:
            os.remove(block)


raw_data_path = "raw_stacks"

trainer = KNNIndexTrainer(
    inputpath=raw_data_path,
    batchsize=100,
    outputpath="src/index_files",
    index_of_what='q'
)
len(trainer.clear_input_answers)    # 125
# trainer.build_index()   # will fail for few samples (at least 350 samples for IVF10)



