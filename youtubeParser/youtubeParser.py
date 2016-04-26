#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urlparse import parse_qs
from scrapy import Selector

import requests
import json
import re

DEV = True

if DEV:
    import pprint


class YoutubeParser(object):

    regX = re.compile(ur'ytplayer.config = ({.*});yt')
    storyBoardRegX = re.compile(ur'#M\$M#(?P<sigh>[\w-]+)\|')
    durationRegX = re.compile(ur'^PT(?:(?P<H>\d+)H)?(?:(?P<M>\d+)M)?(?:(?P<S>\d+)S)?$')
    youtube_id = None

    @property
    def youtube_url(self):
        return self.youtube_id

    @youtube_url.setter
    def youtube_url(self, link):
        find = re.search(ur'v=(\w+)', link)
        if find:
            self.youtube_id = find.groups()[0]
        else:
            raise ValueError('It seems not a valid youtube url.')

    def __init__(self):
        pass

    def extract_info(self, video_id=None):

        video_id = video_id and video_id or self.youtube_id

        if video_id is None:
            raise ValueError('No specify youtube url or id.')

        bash_url = 'https://www.youtube.com/watch?v=%s' % video_id

        r = requests.get(bash_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                                                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 '
                                                          'Safari/537.36'})

        if r.status_code == 200:
            extract = re.search(self.regX, r.content)

            if extract:
                try:
                    raw = extract.groups()[0]
                    data = json.loads(raw)
                    selector = Selector(text=r.content)

                except SyntaxError:
                    raise ValueError('No correct data to extract information.')
                except TypeError:
                    raise ValueError('No correct data to extract information.')

                info = {}.copy()

                info['title'] = data['args']['title']
                info['author'] = data['args']['author']
                info['keywords'] = data['args']['keywords']
                info['video_id'] = data['args']['video_id']
                info['thumbnail'] = data['args']['iurlhq_webp']
                info['view_count'] = data['args']['view_count']
                info['avg_rating'] = data['args']['avg_rating']

                story_board_base_url = 'https://i.ytimg.com/sb/%s/storyboard3_L1/M0.jpg?sigh=%s'

                sb_search = re.search(self.storyBoardRegX, data['args']['storyboard_spec'])

                if sb_search:
                    info['story_board'] = story_board_base_url % (video_id, sb_search.groupdict()['sigh'])

                info['duration'] = selector.css('meta[itemprop="duration"]::attr("content")').extract_first()

                duration_search = re.search(self.durationRegX, info['duration'])

                if duration_search:
                    duration_search = duration_search.groupdict()
                    info['duration_ts'] = 0
                    info['duration_ts'] += duration_search['H'] and int(duration_search['H']) * 3600 or 0
                    info['duration_ts'] += duration_search['M'] and int(duration_search['M']) * 60 or 0
                    info['duration_ts'] += duration_search['S'] and int(duration_search['S'])

                info['datePublished'] = selector.css('meta[itemprop="datePublished"]::attr("content")').extract_first()

                info['description'] = ''.join(selector.css('p#eow-description').extract_first())

                info['description'] = info['description'].replace('<p id="eow-description">', '')
                info['description'] = info['description'].replace('</p>', '')

                info['description'] = re.sub(
                    ur'data-\w+=[^ >]*',
                    '', info['description']
                )

                info['description'] = re.sub(
                    ur'class=[^ >]*(?: +")?',
                    '', info['description']
                )

                info['description'] = re.sub(
                    ur'( {2,})',
                    ' ', info['description']
                )

                stream_maps = data['args']['url_encoded_fmt_stream_map'].split(',')

                info['streams'] = []
                for stream_map in stream_maps:
                    stream = parse_qs(stream_map)
                    del(stream['fallback_host'])
                    del(stream['itag'])

                    stream['type'] = stream['type'][0]
                    stream['url'] = stream['url'][0]
                    stream['quality'] = stream['quality'][0]

                    info['streams'].append(stream)

                return info
