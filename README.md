# Unification-based Reconstruction of Multi-hop Explanations for Science Questions

## Abstract
This paper presents a novel framework for reconstructing multi-hop explanations in science Question Answering (QA). While existing approaches for multi-hop reasoning build explanations considering each question in isolation, we propose a method to leverage explanatory patterns emerging in a corpus of scientific explanations. Specifically, the framework ranks a set of atomic facts by integrating lexical relevance with the notion of unification power, estimated analysing explanations for similar questions in the corpus. 

An extensive evaluation is performed on the Worldtree corpus, integrating k-NN clustering and Information Retrieval (IR) techniques. We present the following conclusions: (1) The proposed method achieves results competitive with Transformers, yet being orders of magnitude faster, a feature that makes it scalable to large explanatory corpora (2) The unification-based mechanism has a key role in reducing semantic drift, contributing to the reconstruction of many hops explanations (6 or more facts) and the ranking of complex inference facts (+12.0 Mean Average Precision) (3) Crucially, the constructed explanations can support downstream QA models, improving the accuracy of BERT by up to 10% overall.

## Code to reproduce the results
This repository contains the code used for the paper [Unification-based Reconstruction of Multi-hop Explanations for Science Questions](https://arxiv.org/abs/2004.00061) accepted at EACL 2021.

Here, you can find the code (`experiment.py`) to reproduce the results obtained on the 2019 [Worldtree explanation regeneration task](https://github.com/umanlp/tg2019task) by our best joint model (Relevance Score BM25 + Unification Score BM25).

**Run the experiment:**

`python ./experiment.py`

**Compute the Mean Average Precision (MAP) score:** 

`./evaluate.py --gold=./data/questions/dev.tsv prediction.txt`

For any issues or questions, please contact us for at: marco.valentino@manchester.ac.uk

### Bibtex
If you use this paper in your work, please cite [Unification-based Reconstruction of Multi-hop Explanations for Science Questions](https://arxiv.org/abs/2004.00061):

```
@article{valentino2020unification,
  title={Unification-based Reconstruction of Explanations for Science Questions},
  author={Valentino, Marco and Thayaparan, Mokanarangan and Freitas, Andr{\'e}},
  journal={arXiv preprint arXiv:2004.00061},
  year={2020}
}
```
