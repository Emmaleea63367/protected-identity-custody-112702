"""读取本地合成来源记录。"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterator

SOURCES = Path(__file__).resolve().parent / 'sources'


def source_names(directory: Path = SOURCES) -> tuple[str, ...]:
    """列出可提供记录的来源。"""
    return tuple(sorted(path.stem for path in directory.glob('*.jsonl')))


def read_source(name: str, directory: Path = SOURCES) -> Iterator[dict]:
    """按给出的到达顺序读取来源记录。"""
    if name not in source_names(directory):
        raise ValueError(f'未知来源 {name}')
    with (directory / f'{name}.jsonl').open(encoding='utf-8') as document:
        for line_number, line in enumerate(document, 1):
            row = json.loads(line)
            if not isinstance(row, dict) or type(row.get('seq')) is not int:
                raise ValueError(f'{name} 第 {line_number} 行缺少序号或对象结构')
            yield row


def main() -> None:
    parser = argparse.ArgumentParser(description='查看本地来源记录')
    parser.add_argument('source', choices=source_names(), nargs='?', help='来源名')
    parser.add_argument('--through', type=int, help='仅显示截至此到达序号的记录')
    args = parser.parse_args()
    if args.source is None:
        print('\n'.join(source_names()))
        return
    for record in read_source(args.source):
        if args.through is None or record['seq'] <= args.through:
            print(json.dumps(record, ensure_ascii=False))


if __name__ == '__main__':
    main()
