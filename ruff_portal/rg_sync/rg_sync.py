import requests
import json
import ConfigParser
from .models import Animal


class RGSync:
    def __init__(self):
        # Set the rescue groups URL and API key
        self.config = ConfigParser.ConfigParser()
        self.config.read('rg_sync/rg_config.ini')

        self.url = self.config.get('account', 'url')
        self.api_key = self.config.get('account', 'apiKey')
        pass

    def get_available_animals(self):
        # Form the JSON msg body
        api_args = {'apikey': self.api_key,
                    'objectType': 'animals',
                    'objectAction': 'publicSearch',
                    'search': {
                        'resultStart': 0,
                        'resultLimit': 100,
                        'fields': ['animalId'],
                        'filters': [{
                            'fieldName': 'animalStatus',
                            'operation': 'equals',
                            'criteria': 'Available',
                        }],
                    }}
        api_args = json.dumps(api_args)

        # Send the request
        request = requests.post(self.url, data=api_args)
        request_txt = json.loads(request.text)

        # Get the data
        if 'data' in request_txt:
            animals_in_db = Animal.objects.all()
            print "current size: " + str(len(animals_in_db))
            animals_in_db_ids = []
            for db_animal in animals_in_db:
                animals_in_db_ids.append(db_animal.rg_id)
            print animals_in_db_ids

            for item in request_txt['data']:
                item = int(item)
                # Add animals that aren't already in DB
                if item not in animals_in_db_ids:
                    print "adding " + str(item)
                    animal = Animal(rg_id=item)
                    animal.save()
            return_txt = "okay"
        else:
            return_txt = "error"

        return return_txt

