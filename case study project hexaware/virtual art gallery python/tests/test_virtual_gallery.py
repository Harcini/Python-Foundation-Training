import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dao.virtual_gallery_impl import VirtualGalleryImpl
from entity.artwork import Artwork
from entity.Gallery import Gallery


class TestVirtualGallery(unittest.TestCase):

    def setUp(self):
        self.service = VirtualGalleryImpl()

    # 1. Add Artwork
    def test_add_artwork(self):
        artwork = Artwork(None, "Test Art", "Test Desc", "2024-01-01", "Oil", "test.jpg", 1)
        result = self.service.add_artwork(artwork)
        self.assertTrue(result)

    # 2. Update Artwork
    def test_update_artwork(self):
        # Insert artwork before updating
        artwork = Artwork(None, "UpdateTest", "To be updated", "2023-10-10", "Oil", "update.jpg", 1)
        result = self.service.add_artwork(artwork)
        self.assertTrue(result)

        # Get the latest artwork ID
        all_artworks = self.service.get_all_artworks()
        artwork_id = all_artworks[-1][0]

        # Update the artwork
        self.service.update_artwork(artwork_id, {"Title": "Updated Title"})

        # Fetch updated artwork and check
        updated = self.service.get_artwork_by_id(artwork_id)
        self.assertIsNotNone(updated)
        self.assertEqual(updated[1], "Updated Title")  # index 1 = Title

    # 3. Remove Artwork
    def test_remove_artwork(self):
        artwork = Artwork(None, "Delete Me", "To Delete", "2022-02-02", "Watercolor", "delete.jpg", 1)
        self.service.add_artwork(artwork)
        all_artworks = self.service.get_all_artworks()
        artwork_id = all_artworks[-1][0]

        self.service.remove_artwork(artwork_id)
        self.assertIsNone(self.service.get_artwork_by_id(artwork_id))

    # 4. Search Artworks
    def test_search_artworks(self):
        artwork = Artwork(None, "SearchKeywordTest", "Desc", "2023-01-01", "Ink", "search.jpg", 1)
        self.service.add_artwork(artwork)
        results = self.service.search_artworks("SearchKeywordTest")
        self.assertTrue(any("SearchKeywordTest" in a[1] for a in results))

    # 5. Add Gallery
    def test_add_gallery(self):
        gallery = Gallery(None, "Test Gallery", "Testing Gallery", "Pune", 1, "9AM-6PM")
        self.service.add_gallery(gallery)
        galleries = self.service.get_all_galleries()
        self.assertTrue(any(g[1] == "Test Gallery" for g in galleries))

    # 6. Update Gallery
    def test_update_gallery(self):
        galleries = self.service.get_all_galleries()
        if not galleries:
            gallery = Gallery(None, "Update Gallery", "To update", "OldPlace", 1, "9AM-6PM")
            self.service.add_gallery(gallery)
            galleries = self.service.get_all_galleries()

        gallery_id = galleries[-1][0]
        self.service.update_gallery(gallery_id, {"Location": "Mumbai"})
        gallery = self.service.get_gallery_by_id(gallery_id)
        self.assertEqual(gallery[3], "Mumbai")

    # 7. Remove Gallery
    def test_remove_gallery(self):
        gallery = Gallery(None, "Delete Gallery", "To delete", "Delhi", 1, "10AM-4PM")
        self.service.add_gallery(gallery)
        galleries = self.service.get_all_galleries()
        gallery_id = galleries[-1][0]

        self.service.remove_gallery(gallery_id)
        self.assertIsNone(self.service.get_gallery_by_id(gallery_id))

    # 8. Search Galleries
    def test_search_galleries(self):
        unique_name = "Searchable_Gallery_12345"
        gallery = Gallery(None, unique_name, "Searchable Desc", "Delhi", 1, "10AM-4PM")
        self.service.add_gallery(gallery)
        results = self.service.search_galleries("Searchable_Gallery_12345")
        self.assertTrue(any(unique_name in g[1] for g in results))


if __name__ == "__main__":
    unittest.main()


