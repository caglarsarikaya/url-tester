"""
URL Tester Application - Refactored Version
Entry point for the URL testing application.
"""

import sys
import logging
from src.application import URLTestApplication
from src.models import TestConfig


# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass


def main():
    """Main entry point"""
    try:
        print("=" * 60)
        print("           URL TESTER APPLICATION")
        print("=" * 60)
        print("\nSelect testing mode:")
        print("  1. Defined URL list (from urls_to_test.xlsx)")
        print("  2. Sitemap parsing (from sitemaps.xlsx)")
        print()
        
        # Get user choice
        while True:
            choice = input("Enter your choice (1 or 2): ").strip()
            if choice in ['1', '2']:
                break
            print("Invalid choice. Please enter 1 or 2.")
        
        # Set mode based on choice
        mode = "defined" if choice == "1" else "sitemap"
        
        print()
        print("=" * 60)
        
        # Create configuration
        config = TestConfig(
            max_workers=100,  # 100 concurrent threads for fast testing
            timeout=5,        # 5 second timeout per request
            delay=0           # No delay between submissions
        )
        
        # Create and run application
        app = URLTestApplication(mode=mode, config=config)
        app.run()
        
    except KeyboardInterrupt:
        print("\n\n[WARNING] Testing interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        logging.error(f"Application error: {str(e)}", exc_info=True)
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Wait for user before closing
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()

