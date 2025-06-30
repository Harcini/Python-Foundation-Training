# entity/Gallery.py
class Gallery:
    def __init__(self, gallery_id=None, name=None, description=None, location=None, curator=None, opening_hours=None):
        self.gallery_id = gallery_id
        self.name = name
        self.description = description
        self.location = location
        self.curator = curator
        self.opening_hours = opening_hours
