# Feel the Buzz - a JobTweetsClassifier

Goal: text classifier for tweets containing job offers

## Roadmap

1. Load dump of tweets (Settings -> Content -> Your Twitter archive -> Request your archive)
2. Manually mark tweets with a job posting as positive samples (True)
3. Sample and format the dataset as a CSV: one tweet per line with balanced classes and shuffled samples

4. Train a classifier to detect job tweets, e.g. fastText, or support vector machine with RBF kernel trained on uni-grams or random forest.

5. Explain the classifier predictions with LIME


## Requirements

* pandas
* [fasttext](https://github.com/salestock/fastText.py)
* [LIME](https://github.com/marcotcr/lime)


## References

1. [Crepe](https://github.com/zhangxiangxiao/Crepe)
2. [fastText](https://github.com/facebookresearch/fastText)
3. [fastText tutorial](https://github.com/facebookresearch/fastText/blob/master/tutorials/supervised-learning.md)
4. [Lime](https://marcotcr.github.io/lime/tutorials/Lime%20-%20basic%20usage%2C%20two%20class%20case.html)(https://arxiv.org/pdf/1602.04938.pdf)
