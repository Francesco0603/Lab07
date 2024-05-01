from database.meteo_dao import MeteoDao as md
class Model:
    def __init__(self):
        self.situazioni = md.get_all_situazioni()