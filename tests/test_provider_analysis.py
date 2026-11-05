import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ProviderAnalysisTests(unittest.TestCase):
    def test_repeated_claim_ids_are_counted_consistently(self):
        rows = [
            ("C1", "PROV_A", 10),
            ("C1", "PROV_A", 20),
            ("C2", "PROV_A", 30),
            ("C1", "PROV_B", 40),
            ("C3", "PROV_B", 50),
            ("C4", "PROV_C", 60),
            ("C5", "PROV_C", 80),
            ("C6", "PROV_D", 0),
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            shutil.copy2(
                PROJECT_ROOT / "provider_analysis.py",
                temp_root / "provider_analysis.py",
            )
            pd.DataFrame(
                rows,
                columns=["CLM_ID", "PRVDR_NUM", "CLM_PMT_AMT"],
            ).to_csv(
                temp_root
                / "DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv",
                index=False,
            )

            result = subprocess.run(
                [sys.executable, "provider_analysis.py"],
                cwd=temp_root,
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("Repeated claim IDs: 1 (3 rows retained)", result.stdout)
            summary = pd.read_csv(
                temp_root / "outputs" / "provider_anomaly_results.csv"
            ).set_index("PRVDR_NUM")

        self.assertEqual(summary.loc["PROV_A", "total_claims"], 3)
        self.assertEqual(summary.loc["PROV_A", "total_claim_payments"], 60)
        self.assertEqual(summary.loc["PROV_A", "avg_claim"], 20)
        self.assertEqual(summary.loc["PROV_A", "max_claim"], 30)
        self.assertEqual(summary.loc["PROV_B", "total_claims"], 2)
        self.assertEqual(summary.loc["PROV_B", "total_claim_payments"], 90)


if __name__ == "__main__":
    unittest.main()
