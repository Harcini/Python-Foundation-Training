import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from entity.artist import Artist
from entity.artwork import Artwork, insert_artwork
from entity.user import User
from dao.virtual_gallery_impl import VirtualGalleryImpl
from util.db_connect import get_connection
from exception.ArtworkNotFoundException import ArtworkNotFoundException
from exception.UserNotFoundException import UserNotFoundException

def insert_artist(artist):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Artist (Name, Biography, BirthDate, Nationality, Website, ContactInformation)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (artist.name, artist.biography, artist.birth_date,
              artist.nationality, artist.website, artist.contact_info))
        conn.commit()
        print("Artist inserted successfully!")
    except Exception as e:
        conn.rollback()
        print(f"Error inserting artist: {e}")
    finally:
        cursor.close()
        conn.close()

def view_all_artists():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Artist")
        rows = cursor.fetchall()
        print("\n--- All Artists ---")
        if not rows:
            print("No artists found.")
        else:
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, DOB: {row[3]}, Nationality: {row[4]}")
    except Exception as e:
        print(f"Error retrieving artists: {e}")
    finally:
        cursor.close()
        conn.close()

def view_all_artworks():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Artwork")
        rows = cursor.fetchall()
        print("\n--- All Artworks ---")
        if not rows:
            print("No artworks found.")
        else:
            for row in rows:
                print(f"ID: {row[0]}, Title: {row[1]}, Date: {row[3]}, Medium: {row[4]}")
    except Exception as e:
        print(f"Error retrieving artworks: {e}")
    finally:
        cursor.close()
        conn.close()

def view_artworks_by_artist():
    service = VirtualGalleryImpl()
    try:
        artist_id = int(input("Enter Artist ID to view their artworks: "))
        artworks = service.get_artworks_by_artist(artist_id)
        print(f"--- Artworks by Artist {artist_id} ---")
        for row in artworks:
            print(f"ID: {row[0]}, Title: {row[1]}, Date: {row[3]}, Medium: {row[4]}")
    except ArtworkNotFoundException as e:
        print(e)

def view_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM User")
        rows = cursor.fetchall()
        print("\n--- All Users ---")
        if not rows:
            print("No users found.")
        else:
            for row in rows:
                print(f"ID: {row[0]}, Username: {row[1]}, Email: {row[3]}")
    except Exception as e:
        print(f"Error retrieving users: {e}")
    finally:
        cursor.close()
        conn.close()

def view_favorites_by_user():
    service = VirtualGalleryImpl()
    try:
        user_id = int(input("Enter User ID to view favorites: "))
        favorites = service.get_favorites_by_user(user_id)
        if not favorites:
            print("No favorites found for this user.")
        else:
            print("\n--- User's Favorites ---")
            for row in favorites:
                print(f"Artwork ID: {row[0]}, Title: {row[1]}, Medium: {row[2]}")
    except UserNotFoundException as e:
        print(e)

def search_artworks():
    service = VirtualGalleryImpl()
    keyword = input("Enter a keyword to search in artworks (title or description): ")
    results = service.search_artworks(keyword)
    if not results:
        print("No artworks found.")
    else:
        print("\n--- Search results ---")
        for row in results:
            print(f"ID: {row[0]}, Title: {row[1]}, Medium: {row[4]}")

def add_favorite():
    service = VirtualGalleryImpl()
    try:
        user_id = int(input("Enter User ID: "))
        artwork_id = int(input("Enter Artwork ID to favorite: "))
        service.add_favorite(user_id, artwork_id)
        print("Favorite added successfully!")
    except Exception as e:
        print(f"Error adding favorite: {e}")

def remove_favorite():
    service = VirtualGalleryImpl()
    try:
        user_id = int(input("Enter User ID: "))
        artwork_id = int(input("Enter Artwork ID to remove from favorites: "))
        service.remove_favorite(user_id, artwork_id)
        print("Favorite removed successfully!")
    except Exception as e:
        print(f"Error removing favorite: {e}")

def update_artwork():
    service = VirtualGalleryImpl()
    artwork_id = int(input("Enter Artwork ID to update: "))
    new_title = input("Enter new Title: ") or None
    new_description = input("Enter new Description: ") or None
    new_creation_date = input("Enter new Creation Date (YYYY-MM-DD): ") or None
    new_medium = input("Enter new Medium: ") or None
    new_image_url = input("Enter new Image URL or path: ") or None

    new_values = {}
    if new_title:
        new_values['Title'] = new_title
    if new_description:
        new_values['Description'] = new_description
    if new_creation_date:
        new_values['CreationDate'] = new_creation_date
    if new_medium:
        new_values['Medium'] = new_medium
    if new_image_url:
        new_values['ImageURL'] = new_image_url

    service.update_artwork(artwork_id, new_values)
    print("Artwork updated successfully!")

def remove_artwork():
    service = VirtualGalleryImpl()
    artwork_id = int(input("Enter Artwork ID to delete: "))
    service.remove_artwork(artwork_id)
    print("Artwork removed successfully!")

# --- CLI MENU ---
def main():
    service = VirtualGalleryImpl()
    while True:
        print("\n--- Virtual Art Gallery Menu ---")
        print("1. Add Artist")
        print("2. Add Artwork")
        print("3. View All Artists")
        print("4. View All Artworks")
        print("5. View Artworks by Artist")
        print("6. View All Users")
        print("7. View Favorites by User")
        print("8. Search Artworks")
        print("9. Add Favorite")
        print("10. Remove Favorite")
        print("11. Update Artwork")
        print("12. Remove Artwork")
        print("13. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Name: ")
            biography = input("Biography: ")
            birth_date = input("Birth Date (YYYY-MM-DD): ")
            nationality = input("Nationality: ")
            website = input("Website: ")
            contact_info = input("Contact Info: ")
            artist = Artist(None, name, biography, birth_date, nationality, website, contact_info)
            insert_artist(artist)

        elif choice == "2":
            conn = get_connection()
            title = input("Title: ")
            description = input("Description: ")
            creation_date = input("Creation Date (YYYY-MM-DD): ")
            medium = input("Medium: ")
            image_url = input("Image URL or path: ")
            artist_id = int(input("Artist ID (must exist): "))
            artwork = Artwork(None, title, description, creation_date, medium, image_url, artist_id)
            try:
                insert_artwork(artwork, conn)
                print("Artwork inserted successfully!")
            except Exception as e:
                print(f"Error inserting artwork: {e}")
            conn.close()

        elif choice == "3":
            view_all_artists()
        elif choice == "4":
            view_all_artworks()
        elif choice == "5":
            view_artworks_by_artist()
        elif choice == "6":
            view_all_users()
        elif choice == "7":
            view_favorites_by_user()
        elif choice == "8":
            search_artworks()
        elif choice == "9":
            add_favorite()
        elif choice == "10":
            remove_favorite()
        elif choice == "11":
            update_artwork()
        elif choice == "12":
            remove_artwork()
        elif choice == "13":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
