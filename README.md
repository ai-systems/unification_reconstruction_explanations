# Unification-based Reconstruction of Explanations for Science Questions

## Abstract
The paper presents a framework to reconstruct explanations for multiple choice science questions through explanation-centred corpora. 
Building upon the notion of unification in science, the framework ranks explanatory facts with respect to question and candidate answer by leveraging a combination of two different scores: 
(a) A Relevance Score (RS) that represents the extent to which a given fact is specific to the question; (b) A Unification Score (US) that takes into account the explanatory power of a fact, 
determined according to its frequency in explanations for similar questions. An extensive evaluation of the framework is performed on the Worldtree corpus, adopting IR weighting schemes for its implementation.
The following findings are presented: (1) The proposed approach achieves competitive results when compared to state-of-the-art Transformers, yet possessing the property of being scalable to large explanatory knowledge bases;
(2) The combined model significantly outperforms IR baselines (+7.8/8.4 MAP), confirming the complementary aspects of relevance and unification score; 
(3) The constructed explanations can support downstream models for answer prediction, 
improving the accuracy of BERT for multiple choices QA on both ARC easy (+6.92%) and challenge (+15.69%) questions.

## Code to reproduce results
This repository contains the code used for the paper [Unification-based Reconstruction of Explanations for Science Questions](https://arxiv.org/abs/2004.00061).

We have released the code (`experiment.py`) to reproduce the results obtained on the [Worldtree explanation reconstruction task](https://github.com/umanlp/tg2019task) by our best joint model (Relevance Score BM25 + Unification Score BM25).

**Running the experiment:** `python ./experiment.py`

**Computing the Mean Average Precision (MAP) score:** `./evaluate.py --gold=./data/questions/dev.tsv prediction.txt`

### Bibtex
If you use this paper in your work, please cite [Unification-based Reconstruction of Explanations for Science Questions](https://arxiv.org/abs/2004.00061):

```
@misc{valentino2020unificationbased,
    title={Unification-based Reconstruction of Explanations for Science Questions},
    author={Marco Valentino and Mokanarangan Thayaparan and André Freitas},
    year={2020},
    eprint={2004.00061},
    archivePrefix={arXiv},
    primaryClass={cs.AI}
}
```