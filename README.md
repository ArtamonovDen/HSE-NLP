# HSE-NLP

NLP Classes, 2021

## Prepare env

Prepare python vertual env with

```bash
python -m venv venv
```

 and install package with:

```bash
pip install -r requirements.txt
```

In case of something goes wrong, try requirements generated with `pip freeze`:

```bash
freeze_requirements.txt
```

**Download** files from [Goodle drive](https://drive.google.com/drive/folders/12iT4ppXizT4V5bVhgHyAe3NFT1jFCfNR?usp=sharing):

* nplus1_news.json - dataset with news
* preprocessed.pickle - pickled preprocessed texts
* w2v.zip - word2vec  tayga_upos_skipgram_300_2_2019 model, downloaded from [rusvectores](https://rusvectores.org/ru/models)
* Optional: model NewsDenseNet.pt

**Clone** repo [webvectores](https://github.com/akutuzov/webvectors) with

```bash
https://github.com/akutuzov/webvectors.git
```

as [preprocessing script](https://github.com/akutuzov/webvectors/blob/master/preprocessing/rus_preprocessing_udpipe.py) is needed
## Crawler

Run crawler to parse news from [nplus1.ru](https://nplus1.ru) with:

Collected dataset you can find on [Google Drive](https://drive.google.com/drive/u/0/folders/12iT4ppXizT4V5bVhgHyAe3NFT1jFCfNR)

```python
python crawlers/npus1_crawler.py --start 2020-01-01 --end 2021-01-01 --output news.json
```

## NER

Download biLSTM model from [Google Drive](https://drive.google.com/drive/u/0/folders/12iT4ppXizT4V5bVhgHyAe3NFT1jFCfNR).
Split dataset is also available there. Check Preprocessing and training process in NER.ipynb

