### [GeoDB](https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_GeoDBCities.md)

Used to obtain Topher Mykolyk's location on the map and other geographical features including proximity, coordinates, population, etc to develop the prediction algorithm.
INSERT & USE api key in key_geodb.txt
Example usage:
- GET Request to cities near a city: `https://wft-geo-db.p.rapidapi.com/v1/geo/cities/{cityId}/nearbyCities`, replace `cityID` with the ID found in `https://wft-geo-db.p.rapidapi.com/v1/geo/cities`.

### [Abstract](https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_Abstract's_Holidays_API.md)

Used to obtain holiday information for specific countries. Used to format calendar.
INSERT & use api key in key_abstract.txt
Example usage:
- GET request to get all holidays in a country and year: ```https://holidays.abstractapi.com/v1/```. View Documentation for parameters format.

### [Unsplash](https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_unsplash.md)

Used to obtain weather information for a specific time & coordinates in the world.
INSERT & use api key in key_unsplash.txt
Example usage:
- GET request to get some images for a specific query ```https://api.unsplash.com/search/photos?client_id=(api_id)&page=1&query=(query)```