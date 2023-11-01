import csv
import os
import random
from typing import List, Dict, Any
from helm.common.general import ensure_file_downloaded, ensure_directory_exists
from .scenario import Scenario, Instance, Reference, ALL_SPLITS, CORRECT_TAG, VALID_SPLIT, Input, Output

# TODO: Should I just get rid of the train/test split?

class Corr2CauseScenario(Scenario):
    """Information on this class"""
    name = "corr2cause"
    description = "Can Large Language Models Infer Causation from Correlation?"
    tags = ["classification"]
    DATASET_FILE_NAME = "corr2cause.csv"
    TRAIN_RATIO = 0.8  # 80% for training, 20% for validation
    TRAIN_SPLIT = "train"
    VALID_SPLIT = "valid"

    def download_dataset(self, output_path: str):
        """Downloads the Corr2Cause dataset if not already present."""
        # Define the target path for the dataset
        data_dir = os.path.join(output_path, "data")
        dataset_path = os.path.join(data_dir, self.DATASET_FILE_NAME)
        
        # Check if the dataset already exists
        if os.path.exists(dataset_path):
            print(f"The dataset '{self.DATASET_FILE_NAME}' already exists at '{dataset_path}'. Skipping download.")
            return
        
        # Download the raw data
        url = "https://gist.githubusercontent.com/msaroufim/2835e9a27490bb183de86c54c0614169/raw/4160842cd2574716355a5fe9134387a20baed9f8/corr2cause.csv"
        ensure_directory_exists(data_dir)
        ensure_file_downloaded(source_url=url, target_path=dataset_path)


    def load_dataset(self, output_path: str) -> List[Dict[str, Any]]:
        file_path = os.path.join(output_path, "data", self.DATASET_FILE_NAME)
        
        data = []
        with open(file_path, encoding="utf-8") as f:
            csv_reader = csv.reader(f)
            next(csv_reader)
            for label, question in csv_reader:
                formatted_input = f"{question}\nFirst Option: 0\nSecond Option: 1"
                data_point = {
                    "label": int(label),
                    "input": formatted_input.strip()
                }
                data.append(data_point)
        random.shuffle(data)
        return data

    def data_to_instance(self, data_point: Dict[str, Any], split: str, instance_id: str) -> Instance:
        input_text = Input(text=data_point["input"])
        label = "First Option" if data_point["label"] == 0 else "Second Option"
        reference = Reference(output=Output(text=label), tags=[CORRECT_TAG])

        return Instance(
            id=instance_id,
            input=input_text,
            references=[reference],
            split=split
        )


    def get_instances(self, output_path: str) -> List[Instance]:
        """Returns the instances for this scenario."""
        data = self.load_dataset(output_path)
        # Split the data
        split_k = int(len(data) * self.TRAIN_RATIO)
        train_data = data[:split_k]
        valid_data = data[split_k:]
        
        train_instances = [self.data_to_instance(dt, self.TRAIN_SPLIT, f"id{i}") for i, dt in enumerate(train_data)]
        valid_instances = [self.data_to_instance(dt, self.VALID_SPLIT, f"id{i+len(train_data)}") for i, dt in enumerate(valid_data)]
        
        return train_instances + valid_instances