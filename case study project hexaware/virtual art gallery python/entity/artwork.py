class Artwork:
    def __init__(self, artwork_id, title, description, creation_date, medium, image_url, artist_id):
        self.artwork_id = artwork_id
        self.title = title
        self.description = description
        self.creation_date = creation_date
        self.medium = medium
        self.image_url = image_url
        self.artist_id = artist_id


def insert_artwork(artwork, conn):
    cursor = conn.cursor()
    sql = """
    INSERT INTO Artwork (Title, Description, CreationDate, Medium, ImageURL, ArtistID)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (
        artwork.title, artwork.description, artwork.creation_date,
        artwork.medium, artwork.image_url, artwork.artist_id
    )
    cursor.execute(sql, values)
    conn.commit()
    print("Artwork inserted successfully!")
    cursor.close()
