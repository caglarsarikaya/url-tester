"""Core domain models for URL testing application"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class URLTestRequest:
    """Represents a URL to be tested"""
    url: str
    root_url: Optional[str] = None
    
    def get_full_url(self) -> str:
        """Construct full URL by combining root and path if needed"""
        if self.root_url and not self.url.startswith(('http://', 'https://')):
            return self.root_url.rstrip('/') + '/' + self.url.lstrip('/')
        return self.url


@dataclass
class TestResult:
    """Represents the result of a URL test"""
    source_url: str  # Original URL from Excel/sitemap
    tested_url: str  # Actual URL that was tested
    status_code: str | int
    error_message: str
    tested_at: str
    
    @property
    def is_success(self) -> bool:
        """Check if test was successful (status 200)"""
        return self.status_code == 200
    
    def to_dict(self) -> dict:
        """Convert to dictionary for Excel export"""
        return {
            'source': self.source_url,
            'tested_url': self.tested_url,
            'status_code': str(self.status_code),
            'error_message': self.error_message,
            'tested_at': self.tested_at
        }


@dataclass
class TestConfig:
    """Configuration for URL testing"""
    max_workers: int = 100
    timeout: int = 5
    delay: float = 0
    user_agent: str = 'URL-Tester/1.0'

