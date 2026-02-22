#!/usr/bin/env python3
"""
Build a report from a project folder.

Usage:
    python build_report.py --project examples/WCC_Booster --type test_report
    python build_report.py --project examples/WCC_Booster --type test_report --word-only

Report types:
    test_report   — Shake table seismic test report
"""

import argparse
import importlib
import importlib.util
import os
import sys


# ── Builder registry ──────────────────────────────────────────────────────────
# Maps --type value to the builder module path.
# Add new report types here as the builder library grows.

BUILDERS = {
    'test_report': 'builders.test_report_builder',
}


# ── Path helpers ──────────────────────────────────────────────────────────────

def _ensure_lib_on_path():
    """Add the repo root and functions/ to sys.path."""
    this_dir = os.path.dirname(os.path.abspath(__file__))
    if this_dir not in sys.path:
        sys.path.insert(0, this_dir)


# ── Config loading ─────────────────────────────────────────────────────────────

def load_project_config(project_dir: str) -> dict:
    """Load project_config.py from the project folder and return project_info."""
    config_path = os.path.join(project_dir, 'project_config.py')
    if not os.path.isfile(config_path):
        print(f"ERROR: project_config.py not found in {project_dir}")
        sys.exit(1)

    spec = importlib.util.spec_from_file_location('project_config', config_path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    if not hasattr(mod, 'project_info'):
        print("ERROR: project_config.py must define a 'project_info' dict")
        sys.exit(1)

    return mod.project_info


def resolve_config(project_info: dict, report_type: str) -> dict:
    """Merge project_info with report-type-specific overrides.

    Resolution order: reports[type][key] → project_info[key]

    Returns a flat dict with all resolved settings for this report type.
    """
    if 'reports' not in project_info:
        print("ERROR: project_config.py has no 'reports' section.")
        print("       Add a 'reports' dict with at least one report type.")
        sys.exit(1)

    reports = project_info['reports']
    if report_type not in reports:
        print(f"ERROR: Report type '{report_type}' not configured in project_config.py.")
        print(f"       Available types: {list(reports.keys())}")
        sys.exit(1)

    # Merge: start with project_info (excluding 'reports'), override with type-specific settings
    resolved = {k: v for k, v in project_info.items() if k != 'reports'}
    resolved.update(reports[report_type])
    return resolved


# ── Builder dispatch ───────────────────────────────────────────────────────────

def load_builder(report_type: str):
    """Import and return the builder module for the given report type."""
    module_name = BUILDERS.get(report_type)
    if module_name is None:
        print(f"ERROR: Unknown report type '{report_type}'. Supported: {list(BUILDERS.keys())}")
        sys.exit(1)

    _ensure_lib_on_path()

    try:
        builder = importlib.import_module(module_name)
    except ImportError as e:
        print(f"ERROR: Could not import builder '{module_name}': {e}")
        sys.exit(1)

    return builder


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Build a report from a project folder.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python build_report.py --project examples/WCC_Booster --type test_report
  python build_report.py --project examples/WCC_Booster --type test_report --word-only
""")

    parser.add_argument('--project', default='.',
                        help='Path to project folder (default: current directory)')
    parser.add_argument('--type', dest='report_type', required=True,
                        choices=list(BUILDERS.keys()),
                        help=f"Report type: {' | '.join(BUILDERS.keys())}")
    parser.add_argument('--word-only', action='store_true',
                        help='Build Word doc only (default behavior — reserved for future PDF step)')

    args = parser.parse_args()

    project_dir = os.path.abspath(args.project)
    if not os.path.isdir(project_dir):
        print(f"ERROR: Project directory not found: {project_dir}")
        sys.exit(1)

    print(f"Project : {project_dir}")
    project_info = load_project_config(project_dir)
    print(f"Report  : {project_info.get('report_number', '???')}  type: {args.report_type}")

    resolved = resolve_config(project_info, args.report_type)
    builder  = load_builder(args.report_type)

    try:
        builder.run(project_dir, project_info, resolved, args)
    except NotImplementedError as e:
        print(f"ERROR: {e}")
        sys.exit(2)

    print("Done.")


if __name__ == '__main__':
    main()
