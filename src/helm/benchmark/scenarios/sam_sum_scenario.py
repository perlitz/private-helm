import os
import csv
from typing import List

from helm.common.general import ensure_directory_exists, ensure_file_downloaded
from .scenario import Scenario, Instance, Reference, ALL_SPLITS, CORRECT_TAG, VALID_SPLIT, Input, Output


class SamSumScenario(Scenario):
    """
    Add some doc strings at some point
    """

    SOURCE_URL: str = "https://gist.githubusercontent.com/msaroufim/3f1845a5d93b50d849c42b7baeb2f716/raw/11c2d1814a69bb2cfa54549eaa50c0dcc104b9e5/samsum.tsv"

    name = "sam_sum"
    description = "SAMSum Corpus: A Human-annotated Dialogue Dataset for Abstractive Summarization"
    tags = ["summarization"]

    def get_instances(self, output_path: str) -> List[Instance]:
        """
        Build `Instance`s using the consumer health questions and their summarized versions.
        """

        def download_and_read_tsv(filename: str = "samsum.tsv") -> List[dict]:
            file_path: str = os.path.join(data_path, filename)
            ensure_file_downloaded(
                source_url=SamSumScenario.SOURCE_URL,
                target_path=file_path,
                unpack=False,
            )

            with open(file_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter="\t")
                return [row for row in reader]

        data_path: str = os.path.join(output_path, "data")
        ensure_directory_exists(data_path)

        rows = download_and_read_tsv()
        instances: List[Instance] = []

        for row in rows:
            dialogue = row["dialogue"]
            summary = row["summary"]

            # Assuming the split (train/test/val) is not provided in the TSV, using VALID_SPLIT for all instances.
            # You can modify this part if the split is provided in the TSV.
            instances.append(
                Instance(
                    input=Input(text=dialogue),
                    references=[Reference(output=Output(text=summary), tags=[CORRECT_TAG])],
                    split=VALID_SPLIT,
                )
            )

        return instances
