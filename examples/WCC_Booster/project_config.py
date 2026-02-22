"""Project configuration — Water Control Corporation WCC Booster Pump Systems.

This file is the single source of truth for all report types generated from this project.
The 'reports' dict holds type-specific overrides (template path, output path, etc.).

Usage:
    python build_report.py --project examples/WCC_Booster --type test_report
"""

project_info = {

    # ── Project identity ────────────────────────────────────────────────────────
    'report_number': '25075TR1.0',
    'title':         'Seismic Test Report 25075TR1.0',
    'subtitle':      'Water Control Corporation BP Series Booster Pump Systems',

    # ── Code references ─────────────────────────────────────────────────────────
    'test_standard': 'ICC-ES AC156-24 (2nd Ed.)',
    'codes_short':   'ASCE 7-22, ICC-ES AC156-24',
    'codes_long':    'ASCE/SEI 7-22 Minimum Design Loads and Associated Criteria for Buildings '
                     'and Other Structures; ICC-ES AC156-24 Acceptance Criteria for Seismic '
                     'Qualification by Shake-Table Testing of Nonstructural Components and Systems '
                     '(2nd Edition)',
    'Ip': 1.5,  # Functionality IS certified (Ip >= 1.5)

    # ── Parties ─────────────────────────────────────────────────────────────────
    'manufacturer': {
        'company':   'Water Control Corporation',
        'address':   '',
        'contact':   '',
        'witnesses': 'Josh Petersen – Water Control Corporation',
    },

    'lab': {
        'name':          'Environmental Testing Laboratory',
        'address':       '',
        'contact':       'Jeremy Lange, John Roberts',
        'witnesses':     'Jeremy Lange, John Roberts – Environmental Testing Laboratory',
        'table_short':   '10ft x 10ft Triaxial',
        'table_long':    ('10ft x 10ft Triaxial; Displacement: 10in; '
                          'Maximum Velocity: 75in/sec; Frequency Range: 0.1-100Hz'),
        'accreditation': ('Environmental Testing Laboratory is accredited to ISO 17025 '
                          'for the ICC-ES AC156-24 (2nd Ed.)'),
    },

    'engineer': {
        'company':   'Manwill Engineering LLC',
        'name':      'Derek Manwill, SE',
        'license':   'California License Number: S6266',
        'witnesses': 'Derek Manwill – Manwill Engineering LLC',
    },

    # ── Cover text ──────────────────────────────────────────────────────────────
    'testing_scope': (
        'Two Base Mounted Rigid BP Series Booster Pump Systems were tested for '
        'Water Control Corporation.'
    ),

    'revision_history': [
        {'rev': '0', 'date': '2/10/2026', 'description': 'Initial issue of report.'},
    ],

    # ── Seismic levels ──────────────────────────────────────────────────────────
    # One entry per certification level. Each level gets two rows in the summary
    # table (z/h=1 and z/h=0).
    'levels': [
        {
            'name':     '1',
            'Sds_zh1':  2.00,   # SDS at z/h = 1
            'Sds_zh0':  2.50,   # SDS at z/h = 0
            'Hf':       3.5,    # Height factor
            'Rmu':      1.3,    # Ductility factor
            'Aflx_h':   3.20,   # Flexible horizontal
            'Arig_h':   2.15,   # Rigid horizontal
            'Aflx_v':   1.68,   # Flexible vertical
            'Arig_v':   0.68,   # Rigid vertical
            'Arig_h_90': 1.94,  # 90% × ARIG-H (test pass threshold)
            'Arig_v_90': 0.61,  # 90% × ARIG-V
        },
    ],

    # ── Unit Under Test (UUT) list ───────────────────────────────────────────────
    'uuts': [
        {
            'number':       1,
            'model':        'BPAE50-35-3X2-1',
            'manufacturer': 'Water Control Corporation',
            'function':     'Booster Pump System',
            'serial':       'N/A',
            'mounting':     'Base Mounted Rigid',
            'depth':  32, 'width':  63, 'height': 63, 'weight': 757,
            'test_date': '1/5/2026',
            'level':     '1',
            'result':    'Pass',
            'nat_freq': {'fb': 9.1, 'ss': 12.3, 'v': 9.2},
            'construction': (
                'Carbon steel framing and base. Stainless steel manifolds. '
                'Cast iron pump head and base with aluminum housing.'
            ),
            'subcomponents': (
                'Grundfos - Vertical Pump (PFC99340970), '
                'Kobold - Optical Level Switch (NSD-6AUP1), '
                'Dwyer - Pressure Gauge (DWSGY-D10722N-GF), '
                'Dwyer - Pressure Switch (DA-01)'
            ),
            'function_testing': (
                'Function testing included applying power to each control panel to '
                'operate all internal electronics.'
            ),
            'notes': (
                'UUT 1 included two control panels, both the "A" and "E" options, '
                'which is reflected in the channel count.'
            ),
        },
        {
            'number':       2,
            'model':        'BPSE200-70-6X4-1',
            'manufacturer': 'Water Control Corporation',
            'function':     'Booster Pump System',
            'serial':       'N/A',
            'mounting':     'Base Mounted Rigid',
            'depth':  44, 'width':  97, 'height': 63, 'weight': 2263,
            'test_date': '1/5/2026',
            'level':     '1',
            'result':    'Pass',
            'nat_freq': {'fb': 5.2, 'ss': 11.0, 'v': 7.2},
            'construction': (
                'Carbon steel framing and base. Stainless steel manifolds. '
                'Cast iron pump head and base with aluminum housing.'
            ),
            'subcomponents': (
                'Grundfos - Vertical Pump (PFC99249174), '
                'Dwyer - Pressure Gauge (DWSGY-D10722N-GF), '
                'Grundfos - Horizontal Pump (CM5-4), '
                'Kobold - Flow Meter (DF-1)'
            ),
            'function_testing': (
                'Function testing included applying power to each control panel to '
                'operate all internal electronics.'
            ),
            'notes': (
                'UUT 2 included two control panels, both the "S" and "E" options, '
                'which is reflected in the channel count.'
            ),
        },
    ],

    # ── Seismic runs ────────────────────────────────────────────────────────────
    'runs': [
        {
            'name':         'Run 1',
            'date':         '1/5/2026',
            'level':        '1',
            'has_diagonal': False,  # True if a 45° axis was tested
            'peak_accel':   {'X': 2.81, 'Y': 2.84, 'Z': 2.11},
        },
    ],

    # ── Lab equipment calibration table ─────────────────────────────────────────
    'lab_equipment': [
        {'lab_id': '1456', 'ch': '1',   'description': 'Accelerometer',      'manufacturer': 'PCB Piezotronics',   'model': '353B34',            'serial': '150426', 'cal_date': '03/20/25', 'cal_due': '03/20/26'},
        {'lab_id': '1457', 'ch': '5',   'description': 'Accelerometer',      'manufacturer': 'PCB Piezotronics',   'model': '353B34',            'serial': '150427', 'cal_date': '03/20/25', 'cal_due': '03/20/26'},
        {'lab_id': '1458', 'ch': '9',   'description': 'Accelerometer',      'manufacturer': 'PCB Piezotronics',   'model': '353B34',            'serial': '150428', 'cal_date': '03/20/25', 'cal_due': '03/20/26'},
        {'lab_id': '1632', 'ch': '2',   'description': 'Accelerometer',      'manufacturer': 'PCB Piezotronics',   'model': '355B03',            'serial': '42509',  'cal_date': '03/12/25', 'cal_due': '03/12/26'},
        {'lab_id': '1636', 'ch': '6',   'description': 'Accelerometer',      'manufacturer': 'PCB Piezotronics',   'model': '355B03',            'serial': '42514',  'cal_date': '02/11/25', 'cal_due': '02/11/26'},
        {'lab_id': '1633', 'ch': '10',  'description': 'Accelerometer',      'manufacturer': 'PCB Piezotronics',   'model': '355B03',            'serial': '42511',  'cal_date': '03/12/25', 'cal_due': '03/12/26'},
        {'lab_id': '1656', 'ch': '3',   'description': 'Accelerometer',      'manufacturer': 'PCB Piezotronics',   'model': '355B03',            'serial': '42647',  'cal_date': '03/11/25', 'cal_due': '03/11/26'},
        {'lab_id': '1657', 'ch': '7',   'description': 'Accelerometer',      'manufacturer': 'PCB Piezotronics',   'model': '355B03',            'serial': '42548',  'cal_date': '03/24/25', 'cal_due': '03/24/26'},
        {'lab_id': '1658', 'ch': '11',  'description': 'Accelerometer',      'manufacturer': 'PCB Piezotronics',   'model': '355B03',            'serial': '42649',  'cal_date': '03/11/25', 'cal_due': '03/11/26'},
        {'lab_id': '1645', 'ch': '4',   'description': 'Accelerometer',      'manufacturer': 'PCB Piezotronics',   'model': '355B03',            'serial': '42587',  'cal_date': '03/24/25', 'cal_due': '03/24/26'},
        {'lab_id': '1644', 'ch': '8',   'description': 'Accelerometer',      'manufacturer': 'PCB Piezotronics',   'model': '355B03',            'serial': '42586',  'cal_date': '03/24/25', 'cal_due': '03/24/26'},
        {'lab_id': '1643', 'ch': '12',  'description': 'Accelerometer',      'manufacturer': 'PCB Piezotronics',   'model': '355B03',            'serial': '42585',  'cal_date': '03/24/25', 'cal_due': '03/24/26'},
        {'lab_id': '1640', 'ch': '13',  'description': 'Accelerometer',      'manufacturer': 'PCB Piezotronics',   'model': '355B03',            'serial': '42648',  'cal_date': '03/24/25', 'cal_due': '03/24/26'},
        {'lab_id': '1641', 'ch': '14',  'description': 'Accelerometer',      'manufacturer': 'PCB Piezotronics',   'model': '355B03',            'serial': '42578',  'cal_date': '03/24/25', 'cal_due': '03/24/26'},
        {'lab_id': '1642', 'ch': '15',  'description': 'Accelerometer',      'manufacturer': 'PCB Piezotronics',   'model': '355B03',            'serial': '42584',  'cal_date': '03/24/25', 'cal_due': '03/24/26'},
        {'lab_id': '1730', 'ch': 'N/A', 'description': 'Vibration Controller','manufacturer': 'Vibration Research', 'model': 'VR10500 Revolution','serial': 'N/A',    'cal_date': '01/10/25', 'cal_due': '01/10/26'},
        {'lab_id': '1731', 'ch': 'N/A', 'description': 'Vibration Controller','manufacturer': 'Vibration Research', 'model': 'VR10500 Revolution','serial': 'N/A',    'cal_date': '01/10/25', 'cal_due': '01/10/26'},
    ],

    # ── Report type overrides ────────────────────────────────────────────────────
    # Add a key here for each report type this project produces.
    # Keys here override the top-level project_info for that report type.
    'reports': {
        'test_report': {
            'template': '/tmp/template_report.docx',
            'output':   '/tmp/dp-test/25075TR1.0_Test_Report.docx',

            # Plot directories for each run (keyed by run name)
            # Point at local /tmp copies during development; change to Dropbox paths for production.
            'run_plots': {
                'Run 1': {
                    'seismic_dir': '/tmp/dp-test/plots_seismic/',
                    'trs_excel':   '/tmp/dp-test/Run_1_Table_TRSvsRRS.xlsx',
                },
            },

            # Resonance plot directories (keyed by UUT number)
            'resonance_dirs': {
                1: '/tmp/dp-test/uut1_res/',
                2: '/tmp/dp-test/uut2_res/',
            },
        },
    },
}
