# Reddit PennyStocks Scrapper

## Installation

Using pip:

```bash
pip install -r requirements.txt
```

Using conda:

```bash
conda env create -f environment.yml
conda activate reddit-pennystock-scraping
```

## Create a Reddit Application

To access the Reddit API navigate to the [Reddit Apps page](https://www.reddit.com/prefs/apps), and click **create app** or **create another application**.

![Reddit Create Application](https://cms.gilberttanner.com/content/images/size/w2000/2020/06/create_a_reddit_application.png) 

This opens a from where you can create your Application. For the redirect uri you can choose localhost:8080 as described in the [PRAW documentaion](https://praw.readthedocs.io/en/latest/getting_started/authentication.html#script-application)

![Reddit Create Application 2](https://cms.gilberttanner.com/content/images/size/w2000/2020/06/create_new_reddit_application.png)

After pressing **create app** a new application will appear. Here you can find the authentication information needed to create the praw.Reddit instance.

![Reddit Application](https://cms.gilberttanner.com/content/images/size/w2000/2020/06/authentication_information.png)

Copy the three marked attributes into line 18-19 of the **scrape.py** file.

## How to use

```bash
usage: scrape.py [-h] -d DATE -a ACRONYMS [-o OUTPUT_DIR]

Reddit Pennystock Scraper

optional arguments:
  -h, --help            show this help message and exit
  -d DATE, --date DATE  Date
  -a ACRONYMS, --acronyms ACRONYMS
                        Path to acronyms file
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Path to output directory
```

Example:

```bash
python scrape.py -d 2020-08-03 -a acronyms.txt -o result
```