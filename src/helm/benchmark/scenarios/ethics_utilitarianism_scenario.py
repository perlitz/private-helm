import csv
import os
import random
from typing import List, Dict, Any
from helm.common.general import ensure_file_downloaded, ensure_directory_exists
from .scenario import Scenario, Instance, Reference, ALL_SPLITS, CORRECT_TAG, VALID_SPLIT, Input, Output
import random

class EthicsUtilitarianismScenario(Scenario):
    """Information on this class"""
    name = "ethics_utilitarianism"
    description = "Ethics Utilitarianism dataset"
    tags = ["classification"]
    DATASET_FILE_NAME = "util.csv"
    TRAIN_RATIO = 0.7  # 70% for training, 30% for validation
    TRAIN_SPLIT = "train"
    VALID_SPLIT = "valid"

    def download_dataset(self, output_path: str):
        """Ethics utilitarianism dataset"""
        # Define the target path for the dataset
        data_dir = os.path.join(output_path, "data")
        dataset_path = os.path.join(data_dir, self.DATASET_FILE_NAME)

        # Check if the dataset already exists
        if os.path.exists(dataset_path):
            print(f"The dataset '{self.DATASET_FILE_NAME}' already exists at '{dataset_path}'. Skipping download.")
            return

        # Download the raw data
        url ="https://gist.githubusercontent.com/msaroufim/0fe76e3d59214bfe9cc760dda99df5b1/raw/c0983230762bdbc0a1f3c5873d3f6deb21d04cbe/util.csv"
        ensure_directory_exists(data_dir)
        ensure_file_downloaded(source_url=url, target_path=dataset_path)

    def load_dataset(self, output_path: str) -> List[Dict[str, Any]]:
        self.download_dataset(output_path)
        file_path = os.path.join(output_path, "data", self.DATASET_FILE_NAME)

        data = []
        with open(file_path, encoding="utf-8") as f:
            csv_reader = csv.reader(f)
            next(csv_reader)  # Skip the header row if it exists
            for row in csv_reader:
                scenario_1, scenario_2, label = row
                data_point = {
                "input": f"Scenario 1: {scenario_1.strip()}\nScenario 2: {scenario_2.strip()}",
                "label" : int(label),
                }
                data.append(data_point)
        random.seed(0)
        random.shuffle(data)
        return data
    
    def data_to_instance(self, data_point: Dict[str, Any], split: str, instance_id: str) -> Instance:
        input_text = Input(text=data_point["input"])

        references = []
        for i in range(2):
            references.append(Reference(output=Output(text=f"Scenario {i + 1}"), tags=[CORRECT_TAG] if data_point["label"] == i else []))

        return Instance(
            input=input_text, references=references, split=split
        )

    
    def get_instances(self, output_path: str) -> List[Instance]:
        self.download_dataset(output_path)
        data = self.load_dataset(output_path)
        split_index = int(len(data) * self.TRAIN_RATIO)
        train_data = data[:split_index]
        valid_data = data[split_index:]

        train_instances = [self.data_to_instance(dp, self.TRAIN_SPLIT, f"id{i}") for i, dp in enumerate(train_data)]
        valid_instances = [self.data_to_instance(dp, self.VALID_SPLIT, f"id{i+len(train_data)}") for i, dp in enumerate(valid_data)]

        return train_instances + valid_instances