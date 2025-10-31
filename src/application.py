"""Main application orchestrator"""

from .url_providers import URLProvider, DefinedListProvider, SitemapProvider
from .url_tester import URLTesterService
from .report_generator import ReportGenerator
from .models import TestConfig


class URLTestApplication:
    """Main application that orchestrates URL testing workflow"""
    
    def __init__(self, mode: str, config: TestConfig = None):
        """
        Args:
            mode: 'defined' or 'sitemap'
            config: Test configuration (uses defaults if None)
        """
        self.mode = mode
        self.config = config or TestConfig()
        
        # Initialize components
        self.url_provider = self._create_url_provider()
        self.tester_service = URLTesterService(self.config)
        self.report_generator = ReportGenerator(self.mode)
    
    def _create_url_provider(self) -> URLProvider:
        """Factory method to create appropriate URL provider"""
        if self.mode == "defined":
            return DefinedListProvider("urls_to_test.xlsx")
        elif self.mode == "sitemap":
            return SitemapProvider("sitemaps.xlsx")
        else:
            raise ValueError(f"Invalid mode: {self.mode}. Must be 'defined' or 'sitemap'")
    
    def run(self):
        """Execute the complete URL testing workflow"""
        print("=" * 60)
        print("           URL TESTER APPLICATION")
        print("=" * 60)
        
        try:
            # Step 1: Get URLs from provider
            url_requests = self.url_provider.get_urls()
            
            if not url_requests:
                print("\n[WARNING] No URLs to test!")
                return
            
            # Step 2: Test all URLs
            failed_results = self.tester_service.test_urls(url_requests)
            
            # Step 3: Generate report
            self.report_generator.generate_report(failed_results)
            
            print("\n" + "=" * 60)
            print("Testing completed successfully!")
            print("=" * 60)
        
        except KeyboardInterrupt:
            # Re-raise to be handled by main.py
            raise
            
        except FileNotFoundError as e:
            print(f"\nERROR: {str(e)}")
            print("Please make sure the file exists in the same folder as this application.")
            raise
        except ValueError as e:
            print(f"\nERROR: {str(e)}")
            raise
        except Exception as e:
            print(f"\nERROR: Unexpected error: {str(e)}")
            raise

