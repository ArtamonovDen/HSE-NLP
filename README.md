# HSE-NLP

NLP Classes, 2021

## Prepare env

Prepare python vertual env and install package with:

```bash
pip install -r requirements.txt
```

## Crawler

Run crawler to parse news from [nplus1.ru](https://nplus1.ru) with:

```python
python crawlers/npus1_crawler.py --start 2020-01-01 --end 2021-01-01 --output news.json
```
