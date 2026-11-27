"""核对来源记录能按其原始格式读取。"""
import json
import subprocess
import sys
import unittest

from source_records import SOURCES, read_source, source_names


class SourceRecordsTest(unittest.TestCase):
    def test_records_have_unique_arrival_order_and_stable_fields(self):
        all_arrivals = set()
        for name in source_names():
            with self.subTest(source=name):
                rows = list(read_source(name))
                self.assertTrue(rows)
                self.assertTrue(all(row.keys() == rows[0].keys() for row in rows))
                arrivals = [row['seq'] for row in rows]
                self.assertTrue(all(value > 0 for value in arrivals))
                self.assertEqual(arrivals, sorted(set(arrivals)))
                self.assertFalse(all_arrivals.intersection(arrivals))
                all_arrivals.update(arrivals)
        self.assertTrue(all_arrivals)

    def test_cli_lists_sources_and_preserves_json(self):
        script = SOURCES.parent / 'source_records.py'
        listed = subprocess.check_output([sys.executable, script], text=True).splitlines()
        self.assertEqual(list(listed), list(source_names()))
        for name in listed:
            with self.subTest(source=name):
                expected = next(read_source(name))
                output = subprocess.check_output(
                    [sys.executable, script, name, '--through', str(expected['seq'])], text=True
                )
                self.assertEqual([json.loads(line) for line in output.splitlines()], [expected])

    def test_unknown_source_is_rejected(self):
        with self.assertRaisesRegex(ValueError, '未知来源'):
            list(read_source('../outside'))
