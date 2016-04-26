# py-simple-youtube-parser

Simple Youtube video information extractor.

Requirement:
 
    Scrapy

Usage:

.. code-block:: python
    
    >>> import youtubeParser
    
    >>> yParser = YoutubeParser()
    
    >>> yParser.youtube_url = 'https://www.youtube.com/watch?v=videoID'
    >>> print(yParser.extract_info())
    
    OR simply give the VideoID to extract_info function.
    
    >>> print(yParser.extract_info(VideoID))
    




