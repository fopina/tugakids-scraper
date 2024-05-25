## tugakids-scraper

tugakids.com has a Kodi addon but looks poorly maintained (and its code looks like a ragdoll).

http://bit.ly/2FCdP2F is used by the [addon](https://www.tugakids.com/kodi-spmc/) to fetch the list of movies.

Why not just fetch them all and store the stream URLs in disk, to be indexed by Kodi? No addons required.

```
$ ./main.py

Scraping: 100%|███████████████████████████████| 236/236 [00:11<00:00, 20.08it/s, errors=233, name=Hotel Transylvania: Transformania (2022)]
```

Next to each `.strm` there is a [Parsing NFO](https://kodi.wiki/view/NFO_files/Parsing) to allow Kodi scraper to match the movie exactly.

