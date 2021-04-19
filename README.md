# Unification-based Reconstruction of Multi-hop Explanations for Science Questions (EACL 2021)

## Abstract
This paper presents a novel framework for reconstructing multi-hop explanations in science Question Answering (QA). While existing approaches for multi-hop reasoning build explanations considering each question in isolation, we propose a method to leverage explanatory patterns emerging in a corpus of scientific explanations. Specifically, the framework ranks a set of atomic facts by integrating lexical relevance with the notion of unification power, estimated analysing explanations for similar questions in the corpus. 

An extensive evaluation is performed on the Worldtree corpus, integrating k-NN clustering and Information Retrieval (IR) techniques. We present the following conclusions: (1) The proposed method achieves results competitive with Transformers, yet being orders of magnitude faster, a feature that makes it scalable to large explanatory corpora (2) The unification-based mechanism has a key role in reducing semantic drift, contributing to the reconstruction of many hops explanations (6 or more facts) and the ranking of complex inference facts (+12.0 Mean Average Precision) (3) Crucially, the constructed explanations can support downstream QA models, improving the accuracy of BERT by up to 10% overall.

## Reproducibility
This repository contains the code used for the paper [Unification-based Reconstruction of Multi-hop Explanations for Science Questions](https://arxiv.org/abs/2004.00061) accepted at [EACL 2021](https://2021.eacl.org/).

Here, you can find the code (`experiment.py`) to reproduce the results obtained on the 2019 [Worldtree explanation regeneration task](https://github.com/umanlp/tg2019task) by our best joint model (Relevance Score BM25 + Unification Score BM25).

**Run the experiment:**

`python ./experiment.py`

**Compute the Mean Average Precision (MAP) score:** 

`./evaluate.py --gold=./data/questions/dev.tsv prediction.txt`

This command evaluates the explanation ranking stored in `prediction.txt` and should output a MAP score of 54.55.

### Bibtex
If you use the unification-based reconstruction in your work, please consider citing our paper:

```
@inproceedings{valentino-etal-2021-unification,
    title = "Unification-based Reconstruction of Multi-hop Explanations for Science Questions",
    author = "Valentino, Marco  and
      Thayaparan, Mokanarangan  and
      Freitas, Andr{\'e}",
    booktitle = "Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics: Main Volume",
    month = apr,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2021.eacl-main.15",
    pages = "200--211",
    abstract = "This paper presents a novel framework for reconstructing multi-hop explanations in science Question Answering (QA). While existing approaches for multi-hop reasoning build explanations considering each question in isolation, we propose a method to leverage explanatory patterns emerging in a corpus of scientific explanations. Specifically, the framework ranks a set of atomic facts by integrating lexical relevance with the notion of unification power, estimated analysing explanations for similar questions in the corpus. An extensive evaluation is performed on the Worldtree corpus, integrating k-NN clustering and Information Retrieval (IR) techniques. We present the following conclusions: (1) The proposed method achieves results competitive with Transformers, yet being orders of magnitude faster, a feature that makes it scalable to large explanatory corpora (2) The unification-based mechanism has a key role in reducing semantic drift, contributing to the reconstruction of many hops explanations (6 or more facts) and the ranking of complex inference facts (+12.0 Mean Average Precision) (3) Crucially, the constructed explanations can support downstream QA models, improving the accuracy of BERT by up to 10{\%} overall.",
}
```

For any issues or questions, feel free to contact us at marco.valentino@manchester.ac.uk
