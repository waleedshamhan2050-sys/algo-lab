#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مختبر الخوارزميات — نقطة الدخول.
Algo Lab entry point (SHIRAA 2026, Workshop 5).

    python3 main.py            # القائمة التفاعلية
    python3 main.py --demo     # العرض الكامل لأمثلة الورشة
    python3 main.py --test     # الفحص الشامل لكل المزايا
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from algo_lab import cli  # noqa: E402


def main():
    args = sys.argv[1:]
    if "--test" in args:
        # الفحص الشامل من مجلد tests (ولا يكتفي بفحص المنضدة وحدها)
        tests_dir = Path(__file__).resolve().parent / "tests"
        sys.path.insert(0, str(tests_dir))
        import test_algo_lab
        sys.exit(0 if test_algo_lab.run_all() else 1)
    cli.main(args)


if __name__ == "__main__":
    main()
