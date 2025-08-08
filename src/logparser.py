import argparse
from typing import List, Generator, NamedTuple, Tuple
import json
from pathlib import Path
from tabulate import tabulate
from collections import Counter, defaultdict
from datetime import datetime
from hashlib import md5
from functools import lru_cache

class Endpoint(NamedTuple):
    path  : str
    count : int | None
    avg   : float | None


def get_log_item(filename: str) -> Generator:
    with open(filename, 'r') as file:
        for line in file:
            yield json.loads(line.strip())

@lru_cache(maxsize=128)
def get_key(url: str) -> str:
    return md5(url.encode('ascii')).hexdigest()


def generate_average_report(filenames: List[str],  date: str | None = None) -> List | None:
    timing = defaultdict(float)
    mapping = {}
    counter = Counter()

    for filename in filenames:
        if not Path(filename).is_file():
            raise FileNotFoundError(filename)

        for logs_item in get_log_item(filename):
            if date and date not in logs_item['@timestamp']:
                continue
            key = get_key(logs_item['url'])
            if key not in mapping:
                mapping[key] = logs_item['url']

            timing[key] += logs_item['response_time']
            counter[key] += 1

    report = []
    for key, count in counter.most_common():
        url = mapping[key]
        average_response = round(timing[key] / counter[key], 3)

        report.append(
            Endpoint(
                url, count,
                average_response
            )
        )
    return report


def get_report_for_table(full_logs: List[Tuple]) -> List[Tuple]:
    sorted_report = sorted(full_logs,
                           key=lambda x: x.count, reverse=True)
    return sorted_report


def main():
    parser = argparse.ArgumentParser(
        prog='Report generator',
        description='Script for report generation')
    parser.add_argument('-f', '--filename', nargs='+')
    parser.add_argument('-r', '--report')
    parser.add_argument('-d', '--date')
    args = parser.parse_args()
    if args.report != 'average':
        raise ValueError('Wrong report name {args.report}')

    if args.date and not datetime.strptime(args.date, '%Y-%m-%d'):
        raise ValueError('Wrong date format{args.date}, should be YYYY-MM-DD')

    full_report = generate_average_report(args.filename, args.date)
    if full_report:
        print(tabulate(
            get_report_for_table(full_report))
        )


if __name__ == '__main__':
    main()