import os
import boto3

s3 = boto3.client("s3")

TWEET_IDS_KEY = os.environ["TWEET_IDS_KEY"]
BUCKET_NAME = os.environ["BUCKET_NAME"]


def close_and_upload_file(temp_file, temp_filename):
    if temp_file:
        temp_file.close()
        s3.upload_file('/tmp/' + temp_filename, BUCKET_NAME, temp_filename)


def split_tweet_list():
    lines_per_file = 30000
    temp_file = None
    filenames = []

    with open('/tmp/' + TWEET_IDS_KEY) as master_file:
        iteration = 0
        for line_num, line in enumerate(master_file):
            if line_num % lines_per_file == 0:
                iteration += 1

                close_and_upload_file(temp_file, temp_filename)

                temp_filename = f"tweet_ids/tweet_ids_{iteration}.txt"
                filenames.append({"filename": temp_filename})
                temp_file = open('/tmp/' + temp_filename, "w")

            temp_file.write(line)

        close_and_upload_file(temp_file, temp_filename)

    return filenames


def lambda_handler(event, context):

    s3.download_file(BUCKET_NAME, TWEET_IDS_KEY, '/tmp/' + TWEET_IDS_KEY)

    filenames = split_tweet_list()

    return {
        "filenames": filenames,
    }
