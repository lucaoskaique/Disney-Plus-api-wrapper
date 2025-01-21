from collections import defaultdict
import logging
from pydisney import DisneyAPI
from pydisney.models.ProgramType import MovieType, SeriesType
import json

class MovieEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            return {
                'title': obj.title if hasattr(obj, 'title') else None,
                'startYear': obj.startYear if hasattr(obj, 'startYear') else None,
                'mediaMetadata': obj.mediaMetadata if hasattr(obj, 'mediaMetadata') else None,
                'type': obj.__class__.__name__
            }
        return json.JSONEncoder.default(self, obj)


api = DisneyAPI(email="lucas.kaique175@hotmail.com", password="")
api.set_log_level(logging.DEBUG)
series = []
movies = api.get_movies(MovieType.ALL)

all_items = series + movies

grouped_by_year = defaultdict(list)
for item in all_items:
    start_year = item.startYear
    if start_year:
        grouped_by_year[start_year].append(item)

sorted_grouped_by_year_desc = {k: grouped_by_year[k] for k in sorted(grouped_by_year, reverse=True)}

json_output = json.dumps(sorted_grouped_by_year_desc, indent=2, cls=MovieEncoder)
print(json_output)