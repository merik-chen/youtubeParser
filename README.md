youtubeParser
=============

##### Simple extract Youtube video information extractor.

### Req. Packages:
 
    Scrapy
    Requests

### Demo:

    python youtubeParser/youtubeParser.py

### Usage:

```python
    >>> import youtubeParser
    
    >>> yParser = youtubeParser.YoutubeParser()
    
    >>> yParser.youtube_url = 'https://www.youtube.com/watch?v=videoID'
    >>> print(yParser.extract_info())
```
OR simply give the VideoID to extract_info function.
```python
    >>> print(yParser.extract_info(VideoID))
```

### Response:

```
{
    'author': String,
    'avg_rating': String,
    'datePublished': String,
    'description': String,
    'duration': String,
    'duration_ts': Intger,
    'keywords': String,
    'story_board': String,
    'streams': Dict,
    'thumbnail': String,
    'title': String,
    'video_id': String,
    'view_count': String
}
```




