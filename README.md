# Unification-based Reconstruction of Explanations for Science Questions

This repository contains the code used for the paper [Unification-based Reconstruction of Explanations for Science Questions](https://arxiv.org/abs/2004.00061).

## Code to reproduce results
We have released the code (`experiment.py`) to reproduce the results obtained on the [Worldtree explanation reconstruction task](https://github.com/umanlp/tg2019task) by our best model (RS BM25 + US BM25).
**Example Usage:** `python ./experiment.py`
**Compute the Mean Average Precision (MAP) score:** `./evaluate.py --gold=./data/questions/dev.tsv prediction.txt`

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