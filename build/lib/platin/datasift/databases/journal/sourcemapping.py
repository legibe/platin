"""
Maps monitoring aggregator's interaction_type to the journal's sources. If it is not
known, the same one is returned
"""
class SourceMapping(object):

    sources = {
        '2ch': None,
        'amazon': None,
        'bitly': None,
        'bitly_allocation': 'bitly',
        'bitly_trial': 'bitly',
        'blog': 'blogs',
        'board': 'boards',
        'dailymotion': None,
        'demographics': None,
        'demographics_perinteraction': 'demographics',
        'demographics_trial': 'demographics',
        'disqus': None,
        'disqus_allocation': 'disqus',
        'edgar': None,
        'facebook': None,
        'facebook_public': 'facebook',
        'facebook_page': None,
        'flickr': None,
        'focus_allocation': 'focus',
        'focus_perinteraction': 'focus',
        'focus_trial': 'focus',
        'gender': None,
        'gnip_demographics': None,
        'googleplus': None,
        'imdb': None,
        'instagram': None,
        'intensedebate_perinteraction': 'intensedebate',
        'intensedebate': None,
        'intensedebate_promo': 'intensedebate',
        'intensedebate_trial': 'intensedebate',
        'klout_profile': 'klout.profile',
        'klout_score': 'klout.score',
        'klout_topics': 'klout.topics',
        'language': None,
        'lexisnexis': None,
        'lexisnexis_trial': 'lexisnexis',
        'lexisnexis.per_interaction': 'lexisnexis',
        'lexisnexis_perinteraction': 'lexisnexis',
        'links': None,
        'links_allocation': 'links',
        'newscred': None,
        'newscred.per_interaction': 'newscred',
        'reddit': None,
        'salience.entities': None,
        'salience.topics': None,
        'salience.sentiment': None,
        'sinaweibo': None,
        'sinaweibo_perinteraction': 'sinaweibo',
        'sinaweibo_trial': 'sinaweibo',
        'tencentweibo': None,
        'tencentweibo_perinteraction': 'tencentweibo',
        'tencentweibo_trial': 'tencentweibo',
        'topix': None,
        'trends': None,
        'tumblr': None,
        'tumblr_trial': 'tumblr',
        'twitter': None,
        'twitter_gnip': None,
        'video': None,
        'wikipedia': None,
        'wordpress_perinteraction': 'wordpress',
        'wordpress': None,
        'wordpress_promo': 'wordpress',
        'wordpress_trial': 'wordpress',
        'yammer': None,
        'youtube': None
    }

    names = {
        '2ch': '2ch',
        'amazon': 'Amazon',
        'bitly': 'Bitly',
        'blogs': 'Blogs',
        'boards': 'Boards',
        'dailymotion': 'DailyMotion',
        'demographics': 'Demographics',
        'disqus': 'Disqus',
        'edgar': 'Edgar',
        'facebook': 'Favebook',
        'facebook_page': 'Favebook Pages',
        'flickr': 'Flickr',
        'focus': 'Focus',
        'gender': 'Gender',
        'gnip_demographics': 'Demographics',
        'googleplus': 'Google+',
        'imdb': 'Imdb',
        'instagram': 'Instagram',
        'intensedebate': 'IntenseDebate',
        'klout.profile': 'Kout Profile',
        'klout.score': 'Klout Score',
        'klout.topics': 'Klout Topics',
        'language': 'Language',
        'lexisnexis': 'Lexisnexis',
        'links': 'Links',
        'newscred': 'NewsCred',
        'reddit': 'Reddit',
        'salience.entities': 'Salience Entities',
        'salience.sentiment': 'Salience Sentiment',
        'salience.topics': 'Salience Topics',
        'sinaweibo': 'Sina Weibo',
        'tencentweibo': 'Tencent Weibo',
        'topix': 'Topix',
        'trends': 'Trends',
        'tumblr': 'Tumblr',
        'twitter': 'Twitter',
        'twitter_gnip': 'Twitter Gnip',
        'video': 'Video',
        'wikipedia': 'Wikipedia',
        'wordpress': 'WordPress',
        'yammer': 'Yammer',
        'youtube': 'YouTube',
    }

    @classmethod
    def mapSource(self,source):
        result = source
        if source in self.sources:
             if self.sources[source] is not None:
                result = self.sources[source]
        return result

    @classmethod
    def prettyName(self,source):
        if not source in self.names:
            return 'unregistered'
        return self.names[source]
