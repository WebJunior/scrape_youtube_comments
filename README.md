# Simple extract comments from youtube video

First, you need get api-goolge-key [in your profile](https://console.cloud.google.com/) ( for youtube service ).

Second, create file `config.py` and set variable `api_key`. Global variables - `video_id` and `max_comments`


That`s all..

In output will be csv file with headers:
* id
* text
* published
* modified
* author
* author_url
* likes ( count likes)
* parent_id ( id for upper comment)