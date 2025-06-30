# dao/virtual_gallery_interface.py

from abc import ABC, abstractmethod
from entity.Gallery import Gallery
from entity.artist import Artist
from entity.artwork import Artwork
from entity.user import User

class IVirtualArtGallery(ABC):
    # Artist methods
    @abstractmethod
    def add_artist(self, artist: Artist):
        pass

    @abstractmethod
    def get_all_artists(self):
        pass

    # Artwork methods
    @abstractmethod
    def add_artwork(self, artwork: Artwork):
        pass

    @abstractmethod
    def get_all_artworks(self):
        pass

    @abstractmethod
    def get_artworks_by_artist(self, artist_id):
        pass

    @abstractmethod
    def update_artwork(self, artwork_id, new_values):
        pass

    @abstractmethod
    def remove_artwork(self, artwork_id):
        pass

    @abstractmethod
    def get_artwork_by_id(self, artwork_id):
        pass

    @abstractmethod
    def search_artworks(self, keyword):
        pass

    # User methods
    @abstractmethod
    def add_user(self, user: User):
        pass

    @abstractmethod
    def get_all_users(self):
        pass

    # Favorites methods
    @abstractmethod
    def add_favorite(self, user_id, artwork_id):
        pass

    @abstractmethod
    def get_favorites_by_user(self, user_id):
        pass

    @abstractmethod
    def remove_favorite(self, user_id, artwork_id):
        pass

    # Gallery methods
    @abstractmethod
    def add_gallery(self, gallery: Gallery):
        pass

    @abstractmethod
    def get_all_galleries(self):
        pass

    @abstractmethod
    def get_gallery_by_id(self, gallery_id):
        pass
