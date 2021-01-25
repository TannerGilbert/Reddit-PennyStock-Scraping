import os
import argparse
import datetime
import csv

import pandas as pd
import praw
from psaw import PushshiftAPI


def validate_file(f):
    if not os.path.exists(f):
        raise argparse.ArgumentTypeError("{0} does not exist".format(f))
    return f


def scrap_data(date: datetime.datetime, acronyms_path: str, output_dir: str):
    reddit = praw.Reddit(client_id="", client_secret="",
                         user_agent="")
    api = PushshiftAPI(reddit)

    acronyms = open(acronyms_path).read().splitlines()

    date_plus_one_day = date + datetime.timedelta(days=1)

    submissions = list(api.search_submissions(after=int(date.timestamp()),
                                              before=int(date_plus_one_day.timestamp()),
                                              subreddit="pennystocks",
                                              q="|".join(acronyms)))

    comments = list(api.search_comments(after=int(date.timestamp()),
                                        before=int(date_plus_one_day.timestamp()),
                                        subreddit="pennystocks",
                                        q="|".join(acronyms)))

    submissions_df = pd.DataFrame(
        ([post.title, post.id, post.url, post.num_comments, post.selftext, post.created] for post in submissions),
        columns=['title', 'id', 'url', 'num_comments', 'text', 'created'])

    comments_df = pd.DataFrame(
        ([post.body, post.id, post.submission, post.permalink, post.created] for post in comments),
        columns=['body', 'id', 'submission', 'permalink', 'created'])

    acronym_occurrences = []
    # Loop through acronyms and count occurrences
    for acronym in acronyms:
        acronym_in_submissions = submissions_df["title"].str.contains(acronym) | submissions_df["text"].str.contains(acronym)
        acronym_in_comments = comments_df["body"].str.contains(acronym)
        acronym_occurrences.append({"name": acronym, "count": acronym_in_submissions.sum() + acronym_in_comments.sum()})

    # Create output directory if it doesn't exist yet
    os.makedirs(output_dir, exist_ok=True)

    # Save list of dictionaries to csv
    with open(os.path.join(output_dir, "acronym_counts.csv"), "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "count"])
        writer.writeheader()
        writer.writerows(acronym_occurrences)

    submissions_df.to_csv(os.path.join(output_dir, "submissions.csv"))
    comments_df.to_csv(os.path.join(output_dir, "comments.csv"))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Reddit Pennystock Scraper")
    parser.add_argument("-d", "--date", required=True, type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
                        help="Date")
    parser.add_argument("-a", "--acronyms", required=True, type=validate_file, help="Path to acronyms file")
    parser.add_argument("-o", "--output_dir", default="result", type=str, help="Path to output directory")
    args = parser.parse_args()
    scrap_data(args.date, args.acronyms, args.output_dir)
