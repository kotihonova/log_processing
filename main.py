import argparse
import sys
from typing import List, Generator, Dict
import json
from tabulate import tabulate


def get_log_item(filename: str) -> Generator:
    try:
        with open(filename, 'r') as file:
            for line in file:
                yield json.loads(line.strip())
    except FileNotFoundError as e:
        print(e)


def generate_average_report(logs_item: Dict, report: Dict):
    url = logs_item['url'].split('?')[0]
    if url not in report:
        report[url] = {
            'count': 1,
            'time': logs_item['response_time']
        }
    else:
        report[url]['count'] += 1
        report[url]['time'] += logs_item['response_time']
    return report


def get_report(filenames: List[str], report_name: str) -> Dict | None:
    report = {}
    for filename in filenames:
        for logs_item in get_log_item(filename):
            if report_name == 'average':
                report.update(generate_average_report(logs_item=logs_item, report=report))
            else:
                print('Report name not found', file=sys.stderr)
                return None
        if report_name == 'average':
            for item in report:
                report[item]['time'] = str(round(report[item]['time'] / report[item]['count'], 3))
    return report


def get_report_for_table(full_logs) -> List[List]:
    sorted_report = sorted(full_logs.items(),
                           key=lambda x: x[1]['count'], reverse=True)
    report_for_table = [[item[0], item[1]['count'], item[1]['time']] for item in sorted_report]
    return report_for_table


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Report generator',
        description='Script for report generation')
    parser.add_argument('-f', '--filename', nargs='+')
    parser.add_argument('-r', '--report')
    parser.add_argument('-d', '--date')
    args = parser.parse_args()

    full_report = get_report(args.filename, args.report)
    if full_report:
        print(tabulate(get_report_for_table(full_report)))
