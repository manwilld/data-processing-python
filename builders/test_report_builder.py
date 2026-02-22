"""Test report builder module.

Called by build_report.py when --type test_report is specified.
"""

import os
import sys


def run(project_dir: str, project_info: dict, resolved: dict, args):
    """Build the test report Word document.

    Parameters
    ----------
    project_dir : str
        Absolute path to the project folder.
    project_info : str
        Raw project_info dict from project_config.py.
    resolved : dict
        Merged config (project_info + reports['test_report'] overrides).
    args : argparse.Namespace
        CLI args (e.g. args.word_only).
    """
    # Ensure functions/ is importable
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from functions.test_report_generator import TestReportGenerator

    output_path = resolved.get('output')
    if not output_path:
        print("ERROR: 'output' path not set in reports['test_report'] config.")
        raise SystemExit(1)

    # Create output directory if needed
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    gen = TestReportGenerator(resolved)
    gen.generate(output_path)
    print(f"Report saved: {os.path.abspath(output_path)}")
