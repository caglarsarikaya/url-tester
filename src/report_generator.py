"""Report generation service"""

from typing import List
from datetime import datetime
from .models import TestResult
from .excel_handler import ExcelWriter


class ReportGenerator:
    """Generates Excel reports from test results"""
    
    def __init__(self, mode: str):
        """
        Args:
            mode: 'defined' or 'sitemap' - determines column headers
        """
        self.mode = mode
    
    def generate_report(self, results: List[TestResult], output_file: str = None):
        """
        Generate Excel report for failed tests
        
        Args:
            results: List of test results (should only contain failures)
            output_file: Output file path (auto-generated if None)
        """
        if not results:
            print("\n[SUCCESS] No errors found! All URLs returned status 200.")
            return
        
        # Generate output filename if not provided
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"test_results_{timestamp}.xlsx"
        
        # Prepare headers based on mode
        if self.mode == "defined":
            headers = ['url_from_excel', 'tested_url', 'status_code', 'error_message', 'tested_at']
        else:  # sitemap
            headers = ['url_from_sitemap', 'tested_url', 'status_code', 'error_message', 'tested_at']
        
        # Convert results to dictionaries
        rows = []
        for result in results:
            row_dict = {
                headers[0]: result.source_url,  # First header is the source column
                'tested_url': result.tested_url,
                'status_code': str(result.status_code),
                'error_message': result.error_message,
                'tested_at': result.tested_at
            }
            rows.append(row_dict)
        
        # Write to Excel
        writer = ExcelWriter(output_file)
        writer.write_data(headers, rows)
        
        print(f"\n[OK] Error report saved to: {output_file}")
        print(f"[INFO] Total errors reported: {len(results)}")

