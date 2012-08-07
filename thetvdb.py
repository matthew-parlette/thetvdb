import urllib
from xml.dom import minidom

class Episode:
    def __init__(self,episode_id,season_number,episode_number,episode_name):
        self.episode_id = episode_id
        self.season_number = season_number
        self.episode_number = episode_number
        self.episode_name = episode_name
    
    def get_name(self):
        return self.episode_name

class TVShow:
    
    def __init__(self,series_id = None,language = 'en'):
        self.api_key = '2CDD930540D49661'
        self.series_id = series_id
        self.language = language
        self.error_message = None
        self.episode_list = None
        if self.series_id is not None:
            self.refresh()

    def refresh(self,series_id = None):
        """Build the episode list for the provided series id. If no series id is provided, 
        then the current class instance's series_id is used. If an episode list already exists,
        then it will be overwritten. True is returned on success, False on failure.
        
        """
        if series_id is None:
            if self.series_id is None:
                self.set_error("series_id is invalid")
                return False
            else:
                series_id = self.series_id
        
        #Clear some variables
        self.episode_list = None
        
        series_url = "http://www.thetvdb.com/api/%s/series/%s/all/%s.xml" % (self.api_key,series_id,self.language)
        print "url: %s" % series_url
        dom = minidom.parse(urllib.urlopen(series_url))
        
        #Build the episode list
        #for node in dom.getElementsByTagNameNS(WEATHER_NS, 'Episode'):
    
    def set_error(self,error_message = None):
        """Set the current error message when the user needs more information when a 
        False value is returned from a function.
        
        """
        if error_message is not None:
            self.error_message = error_message
    
    def get_episode_list(self):
        """Returns the episode list. This function may return None.
        
        """
        return self.episode_list
