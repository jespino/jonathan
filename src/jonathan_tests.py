import os
import jonathan
import unittest
import tempfile
import shutil

class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        jonathan.app.config['TESTING'] = True
        jonathan.app.config['MEDIA_DIR'] = "tests-media"
        self.app = jonathan.app.test_client()
        os.mkdir(jonathan.app.config['MEDIA_DIR'])
        os.mkdir(os.path.join(jonathan.app.config['MEDIA_DIR'], "testdir1"))
        os.mkdir(os.path.join(jonathan.app.config['MEDIA_DIR'], "testdir1", "testdir3"))
        os.mkdir(os.path.join(jonathan.app.config['MEDIA_DIR'], "testdir2"))
        file(os.path.join(jonathan.app.config['MEDIA_DIR'], "testdir1", "testfile1.mpg"), 'w').write("Test")
        file(os.path.join(jonathan.app.config['MEDIA_DIR'], "testdir1", "testfile2.txt"), 'w')
        file(os.path.join(jonathan.app.config['MEDIA_DIR'], "testdir1", "testdir3","testfile3.mpg"), 'w')

    def tearDown(self):
        shutil.rmtree(jonathan.app.config['MEDIA_DIR'])

    def test_root_path(self):
        response = self.app.get("/")
        assert "<span class=\"folder\">testdir1</span>" in response.data
        assert "<span class=\"folder\">testdir2</span>" in response.data

    def test_empty_directory(self):
        response = self.app.get("/testdir2/")
        assert not "class=\"file\"" in response.data
        assert not "class=\"folder\"" in response.data

    def test_not_empty_directory(self):
        response = self.app.get("/testdir1/")
        assert "<span class=\"folder\">testdir3</span>" in response.data
        assert "<span class=\"file\">testfile1.mpg</span>" in response.data

    def test_not_valid_extension_file(self):
        response = self.app.get("/testdir1/")
        assert not "<span class=\"file\">testfile2.txt</span>" in response.data

    def test_directory_inside_a_directory(self):
        response = self.app.get("/testdir1/testdir3/")
        assert "<span class=\"file\">testfile3.mpg</span>" in response.data

    def test_file_view(self):
        response = self.app.get("/testdir1/testfile1.mpg")
        assert "<a href=\"/media/testdir1/testfile1.mpg\">" in response.data

    def test_file_invalid_extension_view(self):
        response = self.app.get("/testdir1/testfile2.txt")
        assert "404 NOT FOUND" == response.status

    def test_file_data_view(self):
        response = self.app.get("/media/testdir1/testfile1.mpg")
        assert "Test" == response.data

    def test_file_invalid_extension_data_view(self):
        response = self.app.get("/media/testdir1/testfile2.txt")
        assert "404 NOT FOUND" == response.status

if __name__ == '__main__':
    unittest.main()
