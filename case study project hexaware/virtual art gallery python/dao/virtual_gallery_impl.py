import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dao.virtual_gallery_interface import IVirtualArtGallery
from entity.artist import Artist
from entity.artwork import Artwork
from entity.user import User
from entity.Gallery import Gallery
from util.DBConnUtil import get_connection
from exception.ArtworkNotFoundException import ArtworkNotFoundException
from exception.UserNotFoundException import UserNotFoundException

class VirtualGalleryImpl(IVirtualArtGallery):

    # ---------- Artist ----------
    def add_artist(self, artist):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Artist (Name, Biography, BirthDate, Nationality, Website, ContactInformation)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (artist.name, artist.biography, artist.birth_date,
                  artist.nationality, artist.website, artist.contact_info))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error adding artist: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def get_all_artists(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Artist")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving artists: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    # ---------- Artwork ----------
    def add_artwork(self, artwork):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Artwork (Title, Description, CreationDate, Medium, ImageURL, ArtistID)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                artwork.title,
                artwork.description,
                artwork.creation_date,
                artwork.medium,
                artwork.image_url,
                artwork.artist_id
            ))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error adding artwork: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def get_all_artworks(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Artwork")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving artworks: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def get_artworks_by_artist(self, artist_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Artwork WHERE ArtistID = %s", (artist_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving artworks by artist: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def update_artwork(self, artwork_id, new_values):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            set_values = ", ".join([f"{k} = %s" for k in new_values.keys()])
            parameters = list(new_values.values()) + [artwork_id]
            cursor.execute(f"UPDATE Artwork SET {set_values} WHERE ArtworkID = %s", parameters)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error updating artwork: {e}")
        finally:
            cursor.close()
            conn.close()

    def remove_artwork(self, artwork_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Artwork WHERE ArtworkID = %s", (artwork_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error removing artwork: {e}")
        finally:
            cursor.close()
            conn.close()

    def get_artwork_by_id(self, artwork_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Artwork WHERE ArtworkID = %s", (artwork_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving artwork by id: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def search_artworks(self, keyword):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT * FROM Artwork
                WHERE Title LIKE %s OR Description LIKE %s
            """, (f"%{keyword}%", f"%{keyword}%"))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error searching artworks: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    # ---------- User ----------
    def add_user(self, user):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO User (Username, Password, Email, FirstName, LastName, DateOfBirth, ProfilePicture)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (user.username, user.password, user.email,
                  user.first_name, user.last_name, user.dob, user.profile_pic))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error adding user: {e}")
        finally:
            cursor.close()
            conn.close()

    def get_all_users(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM User")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving users: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    # ---------- Favorites ----------
    def add_favorite(self, user_id, artwork_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO FavoriteArtworks (UserID, ArtworkID) VALUES (%s, %s)", (user_id, artwork_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error adding favorite: {e}")
        finally:
            cursor.close()
            conn.close()

    def get_favorites_by_user(self, user_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT Artwork.ArtworkID, Artwork.Title, Artwork.Medium
                FROM FavoriteArtworks
                JOIN Artwork ON FavoriteArtworks.ArtworkID = Artwork.ArtworkID
                WHERE FavoriteArtworks.UserID = %s
            """, (user_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving favorites: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def remove_favorite(self, user_id, artwork_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM FavoriteArtworks WHERE UserID = %s AND ArtworkID = %s",
                           (user_id, artwork_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error removing favorite: {e}")
        finally:
            cursor.close()
            conn.close()

    # ---------- Gallery ----------
    def add_gallery(self, gallery):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Gallery (Name, Description, Location, Curator, OpeningHours)
                VALUES (%s, %s, %s, %s, %s)
            """, (gallery.name, gallery.description, gallery.location,
                  gallery.curator, gallery.opening_hours))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error adding gallery: {e}")
        finally:
            cursor.close()
            conn.close()

    def get_all_galleries(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Gallery")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving galleries: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def get_gallery_by_id(self, gallery_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Gallery WHERE GalleryID = %s", (gallery_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving gallery by id: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def update_gallery(self, gallery_id, new_values):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            set_values = ", ".join([f"{k} = %s" for k in new_values.keys()])
            parameters = list(new_values.values()) + [gallery_id]
            cursor.execute(f"UPDATE Gallery SET {set_values} WHERE GalleryID = %s", parameters)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error updating gallery: {e}")
        finally:
            cursor.close()
            conn.close()

    def remove_gallery(self, gallery_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Gallery WHERE GalleryID = %s", (gallery_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error removing gallery: {e}")
        finally:
            cursor.close()
            conn.close()

    def search_galleries(self, keyword):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT * FROM Gallery
                WHERE Name LIKE %s OR Description LIKE %s
            """, (f"%{keyword}%", f"%{keyword}%"))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error searching galleries: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
