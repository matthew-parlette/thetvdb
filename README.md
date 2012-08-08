thetvdb
=======

A python interface into thetvdb.com API. Its main purpose is to get a standard filename for moving media into your standardized library.

Usage
=====
After importing this library, you should create an instance of TVShow. The optional parameter is the series id, which is specific to thetvdb.org. If you don't know this, then you can leave this parameter blank, and use the search("term") function, where term is the name of the show you are looking for. This will return a dictionary of results, with a key of the series id, and a value of the TV show's friendly name.

Once you have the series id, you can call refresh(series_id), which will retrieve all of the show's information, including the episode list.

Now when you have a file that you need to rename for moving to your library, you can call get_filename(season,episode) (or get_samba_filename(season,episode) to remove colons) to use as your filename in a standardized format.

Filename Format
===============
This interface provides some functions to give you a standard filename that you can use in renaming a bunch of files to then go into your library. For example, you might have a file 'Community 2x05.avi' and you'd like it in the format 'Community.S02E05.Messianic Myths and Ancient Peoples.avi'.

The default filename convention is: 'Series Name.S00E00.Flag1.Flag2.Episode Name'

If you'd like a different file format than what is provided, then you should modify the get_filename() function in the TVShow class.