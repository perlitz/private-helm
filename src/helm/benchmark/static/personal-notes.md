# Summarization metrics

Rouge-N: Measure overlap of n-grams
Extractiveness: Extend of generated summary being extracted directly from source text (Also looks at ngrams)
Compression: Length of original doc vs summary
Faithfullness: Ask an LLM how good the summary is

Schema.yaml 
* lists out summarization metrics
* `run_groups` lists out subgroups like question_answering, information, summarization etc so what's considred a core scenario (most likely for helm-summarize)
* Question: do we need to vary the number of in context examples next to ablations
* Summarization scenarios are listed allong with the relevant metrics like accuracy, summarization metrics, but also a taxonomy like what, who, when


`summarization_metrics.py` includes how to download the dataset, evaluate the metrics and then write the metrics on a disk

There's also some custom scenarios like `me_q_sum_scenario` that seem much simpler to implement, I might just consider this instead (`legal_summarization_scenario`) is also another option

Then need to figure out the actual name the summarization scenario would have in a `run_specs.conf`

In `summarize.py` it runs `helm-summarize` which among other things will run summarization tasks

