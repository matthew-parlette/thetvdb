import urllib
import xml.etree.ElementTree as ET

class Episode:
    def __init__(self,episode_id,season_number,episode_number,episode_name):
        self.episode_id = episode_id
        self.season_number = season_number
        self.episode_number = episode_number
        self.episode_name = episode_name
    
    def __repr__(self):
        return "["+self.episode_id+"] S"+self.season_number.zfill(2)+"E"+self.episode_number.zfill(2)+" "+self.episode_name
    
    def __hash__(self):
        return int(self.season_number.zfill(2)+self.episode_number.zfill(2))
    
    def get_name(self):
        return self.episode_name
    
    def get_season(self):
        return int(self.season_number)
    
    def get_episode(self):
        return int(self.episode_number)
    
    def get_episode_identifier(self):
        """For this episode, return the S01E01 formatted string.
        
        """
        return "S"+self.season_number.zfill(2)+"E"+self.episode_number.zfill(2)

class TVShow:
    
    def __init__(self,series_id = None,language = 'en'):
        self.api_key = '2CDD930540D49661'
        self.series_id = series_id
        self.language = language
        self.error_message = None
        self.episode_list = None
        self.series_name = None
        if self.series_id is not None:
            self.refresh()

    def __repr__(self):
      return "%s (%s, %s)" % (str(self.series_id),str(self.series_name),str(self.language))

    def refresh(self,series_id = None):
        """Build the episode list for the provided series id. If no series id is provided, 
        then the current class instance's series_id is used. If an episode list already exists,
        then it will be overwritten. True is returned on success, False on failure.
        
        """
        
        #If series_id is not passed, then use the class series_id variable
        #If series_id is passed, then set the class series_id variable to match it
        if series_id is None:
            if self.series_id is None:
                self.set_error("series_id is invalid")
                return False
            else:
                series_id = self.series_id
        else:
            self.series_id = series_id
        
        #Clear some variables
        self.episode_list = dict()
        self.series_name = None
        
        #Get the XML from thetvdb API
        series_url = "http://www.thetvdb.com/api/%s/series/%s/all/%s.xml" % (self.api_key,series_id,self.language)
        tree = ET.parse(urllib.urlopen(series_url))
        root = tree.getroot()
        
        #Set the series-level variables
        self.series_name = root.find('Series').find('SeriesName').text
        #Build the episode list
        for series in root.iter('Episode'):
            #There must be a better way to get the data, but this works
            episode = Episode(series.find('id').text,
                              series.find('SeasonNumber').text,
                              series.find('EpisodeNumber').text,
                              series.find('EpisodeName').text)
            if episode.get_season() not in self.episode_list:
                self.episode_list[episode.get_season()] = dict()
            self.episode_list[episode.get_season()][episode.get_episode()] = episode
        
        return True
    
    def search(self,search_term,language = None):
        """Searches thetvdb.org for search_term and returns a dictionary of results.
        The dicationry key is the series_id, the value is the friendly show name.
        
        """
        if language is None:
            language = self.language
        
        #Initialize
        results = dict()
        
        search_url = "http://www.thetvdb.com/api/GetSeries.php?seriesname=%s&language=%s" % (search_term,language)
        search_url = search_url.replace(" ","%20")
        tree = ET.parse(urllib.urlopen(search_url))
        root = tree.getroot()
        
        #Parse the results to build the dictionary
        for series in root.iter('Series'):
            key = series.find('seriesid').text
            value =  series.find('SeriesName').text
            if key not in results:
                results[key] = value
        
        return results
    
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
    
    def get_show_name(self):
        """Return the show name or a blank string if it is not set.
        
        """
        if self.series_name is not None:
            return self.series_name
        else:
            return ""
    
    def get_samba_show_name(self):
        """Return a samba-friendly name for the show.
        
        """
        series_name = self.get_show_name()
        series_name = series_name.replace(":"," -")
        return series_name

    def get_filename(self,season_number,episode_number, flags = []):
        """Returns a filename (without extension) for the given season and episode number.
        None is returned if there is some invalud input, or if the series is not loaded.
        Flags can be provided as a list.
        
        """
        episode = self.get_episode(int(season_number),int(episode_number))
        if episode is not None:
            #file_format is a list of the components, change this if you want a different file format
            file_format = [self.get_show_name(),episode.get_episode_identifier()]
            file_format.extend(flags)
            file_format.append(episode.get_name())
            return '.'.join(file_format)
        else:
            self.set_error("Series is not loaded (call refresh()) or invalid season or episode number")
            return None
    
    def get_samba_filename(self,season_number,episode_number,flags = []):
        """Return a filename (without extension) for this episode that is friendly to samba.
        Characters replaced: ':'
        Flags can be provided as a list.
        
        """
        filename = self.get_filename(season_number,episode_number,flags)
        if filename is not None:
            filename = filename.replace(":"," -")
            return filename
        else:
            self.set_error("get_filename returned None")
            return None
    
    def get_episode(self,season_number,episode_number):
        """Return the Episode object for the given season and episode number.
        Returns None if there is an error
        
        """
        if self.series_id is not None and int(season_number) in self.episode_list and int(episode_number) in self.episode_list[season_number]:
            return self.episode_list[int(season_number)][int(episode_number)]
        else:
            return None
