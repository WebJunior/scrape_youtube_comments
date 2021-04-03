import requests
from datetime import datetime, timedelta
from config import api_key


video_id = 'l9nh1l8ZIJQ'
max_comments = 5000


def get_comments(video_id, page_token=''):
    api_url = 'https://www.googleapis.com/youtube/v3/commentThreads'
    params = {
        'part': 'snippet,replies',
        'videoId': video_id,
        'maxResults': 100,
        'key': api_key,
        'pageToken': page_token
    }

    r = requests.get(api_url, params=params)
    r.raise_for_status()
    return r.json()


def format_date(date):
    date = datetime.fromisoformat(date[:-1])
    hours_added = timedelta(hours=3)
    date = date + hours_added

    return date


def parse_comments(comments, api_comments):
    for api_comment in api_comments['items']:
        id = api_comment['snippet']['topLevelComment']['id']
        author = api_comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
        author_img = api_comment['snippet']['topLevelComment']['snippet']['authorProfileImageUrl']
        author_url = api_comment['snippet']['topLevelComment']['snippet']['authorChannelUrl']
        text = api_comment['snippet']['topLevelComment']['snippet']['textDisplay']
        likes = api_comment['snippet']['topLevelComment']['snippet']['likeCount']
        published = api_comment['snippet']['topLevelComment']['snippet']['publishedAt']
        published = format_date(published)
        modified = api_comment['snippet']['topLevelComment']['snippet']['updatedAt']
        modified = format_date(modified)
        if published == modified:
            modified = 'not modified'

        comments = add_comments_to_array(comments, id, author, author_img, author_url,
                                         text, likes, published, modified)

        if 'replies' in api_comment:
            for replies in api_comment['replies']['comments']:
                id = replies['id']
                text = replies['snippet']['textDisplay']
                parent_id = replies['snippet']['parentId']
                author = replies['snippet']['authorDisplayName']
                author_img = replies['snippet']['authorProfileImageUrl']
                author_url = replies['snippet']['authorChannelUrl']
                likes = replies['snippet']['likeCount']
                published = replies['snippet']['publishedAt']
                published = format_date(published)
                modified = replies['snippet']['updatedAt']
                modified = format_date(modified)
                if published == modified:
                    modified = 'not modified'

                comments = add_comments_to_array(comments, id, author, author_img, author_url,
                                                 text, likes, published, modified, parent_id=parent_id)
    return comments


def main():
    comments_counter = 0
    comments = []
    page = 1
    page_token = ''
    while comments_counter < max_comments:
        print(f'parse page {page}')
        comments_counter += 100
        api_comments = get_comments(video_id, page_token=page_token)
        comments = parse_comments(comments, api_comments)

        if 'nextPageToken' in api_comments:
            page += 1
            page_token = api_comments['nextPageToken']
        else:
            break
    write_to_csv(comments)


def write_to_csv(comments):
    headers_csv = 'id|text|published|modified|author|author_url|likes|parent_id\n'
    with open('comments.csv', 'w', encoding='utf-8') as f:
        f.write(headers_csv)

    for comment in comments:
        with open('comments.csv', 'a', encoding='utf-8') as f:
            f.write(f'{comment["id"]}|{comment["text"]}|{comment["published"]}|{comment["modified"]}|{comment["author"]}|{comment["author_url"]}|{comment["likes"]}|{comment["parent_id"]}\n')


def add_comments_to_array(comments, id, author, author_img, author_url, text, likes, published, modified, parent_id=''):
    text = text.replace('|', ',')

    comments.append({
        'id': id,
        'text': text,
        'published': published,
        'modified': modified,
        'author': author,
        'author_img': author_img,
        'author_url': author_url,
        'likes': likes,
        'parent_id': parent_id
    })

    return comments


if __name__ == '__main__':
    main()
