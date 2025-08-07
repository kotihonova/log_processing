from src.logparser import get_report_for_table, Endpoint


def test_get_report_basic_sorting():
    full_logs = [Endpoint(path='/api/context/...', count=43928, avg=0.019),
                 Endpoint(path='/api/homeworks/...', count=55312, avg=0.093),
                 Endpoint(path='/api/users/...', count=1447, avg=0.066)]
    result = get_report_for_table(full_logs)
    assert result[0].count == 55312


def test_get_report_empty_sorting():
    full_logs = []
    result = get_report_for_table(full_logs)
    assert len(result) == 0

