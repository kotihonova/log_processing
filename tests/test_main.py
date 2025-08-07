import pytest
from src.logparser import main
from .test_generate_report import preparing_mock_data_file


@pytest.fixture(scope='function')
def setup_argv(monkeypatch):
    def _setup_argv(filename, report_type, date=None):
        test_argv = ['logparser.py', '--filename', filename, '--report', report_type]
        monkeypatch.setattr('sys.argv', test_argv)

        if date is not None:
            test_argv.extend(['--date', date])

        monkeypatch.setattr('sys.argv', test_argv)
    return _setup_argv


def test_main_correct_way_with_date(preparing_mock_data_file, monkeypatch, setup_argv):
    setup_argv(preparing_mock_data_file, 'average', '2025-06-22')
    resp = main()
    assert resp is None


def test_main_wrong_report_name(preparing_mock_data_file, monkeypatch, setup_argv):
    setup_argv(preparing_mock_data_file, 'wrong_report_name')
    with pytest.raises(ValueError):
        resp = main()


def test_main_correct_way_with_swapped_month_and_day_date(preparing_mock_data_file, monkeypatch, setup_argv):
    setup_argv(preparing_mock_data_file, 'average', '2025-22-06')
    with pytest.raises(ValueError):
        resp = main()
