#--------------------------------------------------------------------------------
# Copyright (c) 2013, MediaSift Ltd
# All rights reserved.
# Distribution of this software is strictly forbidden under the terms of this
# license.
#
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
from collections import defaultdict
from ...core.date import Day, dateFromTimeStamp, Day

class MaskExplorer(object):

    feeds           = None
    augmentations   = None
    feedSet         = None
    augmentationSet = None
    source          = None # either a feed or an augmentation
    myspace_end     = Day(20120415)

    bundle_translation = {
        'facebook': 'facebook_public',
        'dailymotion': 'boardreader',
        'youtube': 'boardreader',
        'video': 'boardreader',
        'amazon': 'boardreader',
        'flickr': 'boardreader',
        'imdb': 'boardreader',
        'reddit': 'boardreader',
        'topix': 'boardreader',
        '2ch': 'boardreader',
        'board': 'boardreader',
        'blog': 'boardreader',
    }

    deprecated = set(['digg','2ch','amazon','flickr'])

    def __init__(self,database,translateSource=True):
        self._db = database
        all = self._db.select('mask_bundle',['id','origin','type'])
        exclude = set(['','ollie','demographics_trial','bitly_trial'])
        MaskExplorer.feeds = { x['id']:x['origin'] for x in all if x['type'] == 'feed' and not x['origin'] in exclude }
        MaskExplorer.augmentations = { x['id']:x['origin'] for x in all if x['type'] == 'augmentation' }
        MaskExplorer.sources = dict(MaskExplorer.feeds)
        MaskExplorer.sources.update(MaskExplorer.augmentations)
        MaskExplorer.feedSet = set(self.feeds.values())
        MaskExplorer.augmentationSet = set(self.augmentations.values())
        self._translate_source = translateSource

    def userMask(self,userid,start,keep=None):
        extra = set()
        if start > self.myspace_end:
            extra.add('myspace')
        deprecated = self.deprecated.union(extra)
        if keep is None:
            keep = self.feedSet
        feeds = defaultdict(list)
        for v in self._db.select('mask_user_bundle_history',extra_sql="where user_id='%s' order by start_date" % (userid)):
            if v['bundle_id'] in self.sources:
                name = self.sources[v['bundle_id']]
                if name in keep:
                    feeds[name].append(v)
        start_stamp = start.unixTimeStamp()
        mask = {}
        for feed in feeds:
            new = [ x for x in feeds[feed] if start_stamp >= x['start_date'] ]
            if len(new) > 0:
                if new[-1]['end_date'] >= start_stamp or new[-1]['end_date'] is None:
                    if not feed in deprecated:
                        mask[self.bundleName(feed)] = '%s' % Day(dateFromTimeStamp(new[-1]['start_date']))
        return mask

    def sourceTimeline(self,userid,keep=None):
        if keep is None:
            keep = self.feedSet
        feeds = defaultdict(list)
        for v in self._db.select('mask_user_bundle_history',extra_sql="where user_id='%s' order by start_date" % (userid)):
            if v['bundle_id'] in self.sources:
                name = self.sources[v['bundle_id']]
                if name in keep and not name in self.deprecated:
                    v['start_date'] = dateFromTimeStamp(v['start_date']).stringvalue()
                    if v['end_date'] is not None:
                        v['end_date'] = dateFromTimeStamp(v['end_date']).stringvalue()
                    # sometimes a source is deactivated and reactivated straight away, the times
                    # of deactivation and re-activation being identical for some reason, we
                    # compress those.
                    saved = False
                    if name in feeds and len(feeds[name]) > 0:
                        previous = feeds[self.sources[v['bundle_id']]][-1]
                        if previous['end_date'] == v['start_date']:
                            previous['end_date'] = v['end_date']
                            saved = True
                    if not saved:
                        feeds[self.sources[v['bundle_id']]].append(v)
        return feeds

    def bundleName(self,source,force = False):
        if source in self.bundle_translation and (self._translate_source or force):
            bundle = self.bundle_translation[source]
            return bundle
            return self.bundle_translation[source]
        return source
