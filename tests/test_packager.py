import os
from zipfile import ZipFile, is_zipfile
from beamin_controller.packager import Packager


def create_packaging_target(path):
    node_dir = path.mkdir('node')
    node_subdir = node_dir.mkdir('subdir')
    other_dir = path.mkdir('other')

    file1 = node_dir.join('file1.txt')
    file1.write_text('I am file 1', encoding='UTF-8')

    file2 = node_dir.join('file2.txt')
    file2.write_text('I am file 2', encoding='UTF-8')

    file4 = node_dir.join('file4.dog')
    file4.write_text('I am a dog.', encoding='UTF-8')

    file3 = node_subdir.join('file3.txt')
    file3.write_text('I am file 3', encoding='UTF-8')


def test_create_packager(tmpdir):
    packager = Packager(str(tmpdir), str(tmpdir.join('node.zip')))
    assert packager.root == str(tmpdir)


def test_create_packager_with_tilde(tmpdir):
    packager = Packager('~/folder', str(tmpdir.join('node.zip')))
    assert packager.root == os.path.join(os.environ['HOME'], 'folder')


def test_basic_zipping(tmpdir):
    create_packaging_target(tmpdir)
    zip_path = str(tmpdir.join('node.zip'))
    packager = Packager(str(tmpdir.join('node')), zip_path)
    packager.add_matching(['*'])

    assert is_zipfile(zip_path)

    with ZipFile(zip_path, 'r') as z:
        names = z.namelist()

        assert 'file1.txt' in names
        assert 'file2.txt' in names
        assert 'file4.dog' in names
        assert 'subdir/file3.txt' in names


def text_reject_when_zipping(tmpdir):
    create_packaging_target(tmpdir)
    zip_path = str(tmpdir.join('node.zip'))
    packager = Packager(str(tmpdir.join('node')), zip_path)
    packager.add_matching(['*.txt'], ['file2.txt'])

    with ZipFile(zip_path, 'r') as z:
        names = z.namelist()

        assert 'file1.txt' in names
        assert 'file2.txt' not in names
        assert 'file4.dog' not in names
        assert 'subdir/file3.txt' in names
