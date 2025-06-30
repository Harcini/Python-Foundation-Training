def add_favorite(user_id, artwork_id):
    from db_connect import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO FavoriteArtworks (UserID, ArtworkID)
            VALUES (%s, %s)
        """, (user_id, artwork_id))
        conn.commit()
        print("Favorite added successfully!")
    except Exception as e:
        print("Error adding favorite:", e)
    finally:
        cursor.close()
        conn.close()

def view_favorites_by_user(user_id):
    from db_connect import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Artwork.ArtworkID, Artwork.Title, Artwork.Medium
        FROM FavoriteArtworks
        JOIN Artwork ON FavoriteArtworks.ArtworkID = Artwork.ArtworkID
        WHERE FavoriteArtworks.UserID = %s
    """, (user_id,))
    rows = cursor.fetchall()
    print(f"\n--- Favorites for User ID {user_id} ---")
    if not rows:
        print("No favorite artworks found.")
    else:
        for row in rows:
            print(f"Artwork ID: {row[0]}, Title: {row[1]}, Medium: {row[2]}")
    cursor.close()
    conn.close()
