import os
import tempfile
import json
import pytest
from src.logparser import generate_average_report, Endpoint


@pytest.fixture(scope='package')
def preparing_mock_data_file():
    mock_data = [
        {"@timestamp": "2025-06-22T13:59:48+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET",
         "response_time": 0.22, "http_user_agent": "..."},
        {"@timestamp": "2025-06-22T13:59:48+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET",
         "response_time": 0.2, "http_user_agent": "..."},
        {"@timestamp": "2025-06-22T13:59:51+00:00", "status": 200, "url": "/api/context/...", "request_method": "GET",
         "response_time": 0.036, "http_user_agent": "..."}
    ]
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as temp_file:
        for item in mock_data:
            temp_file.write(json.dumps(item) + '\n')
        temp_filename = temp_file.name
    yield temp_filename
    os.unlink(temp_filename)


def test_generate_average_report_result_is_list(preparing_mock_data_file: str):
    result = generate_average_report([preparing_mock_data_file])
    assert isinstance(result, list)


def test_generate_average_report_correct_result_len(preparing_mock_data_file: str):
    result = generate_average_report([preparing_mock_data_file])
    assert len(result) == 2


def test_generate_average_report_result_is_endpoint(preparing_mock_data_file: str):
    result = generate_average_report([preparing_mock_data_file])
    assert isinstance(result[0], Endpoint)


def test_generate_average_report_file_not_found(preparing_mock_data_file: str):
    with pytest.raises(FileNotFoundError):
        result = generate_average_report([preparing_mock_data_file,
                                  'non_existed_file.log'])


def test_generate_average_report_empty_file():
    mock_data = []
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as temp_file:
        for item in mock_data:
            temp_file.write(json.dumps(item))
        temp_filename = temp_file.name
    result = generate_average_report([temp_filename])
    assert len(result) == 0
    os.unlink(temp_filename)


def test_generate_average_report_with_date(preparing_mock_data_file: str):
    result = generate_average_report([preparing_mock_data_file], '2025-06-22')
    assert len(result) == 2
    assert result[0].count == 2


def test_generate_average_report_with_non_existed_date(preparing_mock_data_file: str):
    result = generate_average_report([preparing_mock_data_file], '2025-06-23')
    assert len(result) == 0


def test_generate_average_report_multiply_files(preparing_mock_data_file: str):
    mock_data = [
        {"@timestamp": "2025-06-28T06:38:03+00:00", "status": 200, "url": "/api/context/...", "request_method": "GET",
         "response_time": 0.008, "http_user_agent": "..."},
        {"@timestamp": "2025-06-28T06:38:04+00:00", "status": 200, "url": "/api/context/...", "request_method": "GET",
         "response_time": 0.008, "http_user_agent": "..."},
        {"@timestamp": "2025-06-28T06:38:05+00:00", "status": 200, "url": "/api/context/...", "request_method": "GET",
         "response_time": 0.012, "http_user_agent": "..."}
    ]
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as second_file:
        for item in mock_data:
            second_file.write(json.dumps(item) + '\n')
        second_filename = second_file.name
    result = generate_average_report([preparing_mock_data_file, second_filename])
    assert len(result) == 2
    assert result[0].count + result[1].count == 6
    os.unlink(second_filename)
