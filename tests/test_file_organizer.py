from scripts.file_organizer import FlexibleFileOrganizer


def test_classify_file(tmp_path):
    organizer = FlexibleFileOrganizer(root_dir=tmp_path)
    category, dest = organizer.classify_file("session_analysis_log.txt")
    assert category == "analysis"
    assert dest == "Data/analytics/"


def test_organize_file(tmp_path):
    organizer = FlexibleFileOrganizer(root_dir=tmp_path)
    src = tmp_path / "sample_analysis_log.txt"
    src.write_text("dummy")
    success, _ = organizer.organize_file(str(src))
    assert success
    dest = tmp_path / "Data" / "analytics" / src.name
    assert dest.exists()


def test_clean_current_mess(tmp_path):
    organizer = FlexibleFileOrganizer(root_dir=tmp_path)
    file1 = tmp_path / "temp_test.log"
    file1.write_text("a")
    file2 = tmp_path / "example_analysis_data.txt"
    file2.write_text("b")
    results = organizer.clean_current_mess()
    assert results["moved"] == 2
    assert (tmp_path / "Data" / "temp" / file1.name).exists()
    assert (tmp_path / "Data" / "analytics" / file2.name).exists()
