"""URL source providers for different input methods"""

from abc import ABC, abstractmethod
from typing import List
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

from .models import URLTestRequest
from .excel_handler import ExcelReader


class URLProvider(ABC):
    """Abstract base class for URL providers"""
    
    @abstractmethod
    def get_urls(self) -> List[URLTestRequest]:
        """Get list of URLs to test"""
        pass


class DefinedListProvider(URLProvider):
    """Provides URLs from a defined Excel list"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.reader = ExcelReader(file_path)
    
    def get_urls(self) -> List[URLTestRequest]:
        """
        Load URLs from Excel file with 'root' and 'url' columns
        Root URL is read from first row and applied to all relative URLs
        """
        if not self.reader.exists():
            raise FileNotFoundError(f"File '{self.file_path}' not found!")
        
        rows = self.reader.read_rows(required_columns=['root', 'url'])
        
        # Get root URL from first row with non-empty root
        root_url = None
        for row in rows:
            if row['root']:
                root_url = row['root']
                break
        
        # Create URL test requests
        url_requests = []
        for row in rows:
            if row['url']:
                url_requests.append(URLTestRequest(
                    url=row['url'],
                    root_url=root_url
                ))
        
        print(f"\n[OK] Successfully loaded {len(url_requests)} URLs from defined list")
        print(f"[OK] Root URL: {root_url}")
        
        return url_requests


class SitemapProvider(URLProvider):
    """Provides URLs by parsing sitemap XML files"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.reader = ExcelReader(file_path)
    
    def get_urls(self) -> List[URLTestRequest]:
        """
        Load URLs from sitemaps listed in Excel file
        Supports optional custom root URL for each sitemap
        """
        if not self.reader.exists():
            raise FileNotFoundError(f"File '{self.file_path}' not found!")
        
        rows = self.reader.read_rows(required_columns=['sitemap_url'])
        
        # Extract sitemap URLs and their custom roots
        sitemaps = []
        for row in rows:
            if row['sitemap_url']:
                sitemap_url = row['sitemap_url']
                custom_root = row.get('root')  # Optional column
                sitemaps.append((sitemap_url, custom_root))
        
        print(f"\n[OK] Found {len(sitemaps)} sitemap(s) to parse")
        print("[INFO] Fetching URLs from sitemaps...")
        
        # Parse all sitemaps
        all_urls = []
        for idx, (sitemap_url, custom_root) in enumerate(sitemaps, 1):
            print(f"[INFO] Parsing sitemap {idx}/{len(sitemaps)}: {sitemap_url}")
            if custom_root:
                print(f"[INFO] Will replace URL roots with: {custom_root}")
            
            urls = self._parse_sitemap(sitemap_url, custom_root)
            all_urls.extend(urls)
            print(f"[OK] Found {len(urls)} URLs in this sitemap")
        
        # Remove duplicates by URL string
        unique_urls = []
        seen = set()
        for url_req in all_urls:
            if url_req.url not in seen:
                seen.add(url_req.url)
                unique_urls.append(url_req)
        
        print(f"\n[OK] Total unique URLs to test: {len(unique_urls)}")
        
        return unique_urls
    
    def _parse_sitemap(self, sitemap_url: str, custom_root: str = None) -> List[URLTestRequest]:
        """
        Parse a sitemap XML and extract URLs
        Does NOT recursively crawl sitemap indices to avoid complexity
        """
        try:
            response = requests.get(sitemap_url, timeout=30)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            
            # Define XML namespaces
            namespaces = {
                'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
                'news': 'http://www.google.com/schemas/sitemap-news/0.9',
                'image': 'http://www.google.com/schemas/sitemap-image/1.1'
            }
            
            # Check if this is a sitemap index (contains other sitemaps)
            sitemaps = root.findall('ns:sitemap', namespaces)
            if sitemaps:
                print(f"[INFO] Skipped sitemap index (contains other sitemaps): {sitemap_url}")
                print(f"[INFO] If you need URLs from this, add the specific sitemap URLs to sitemaps.xlsx")
                return []
            
            # Extract URLs from regular sitemap
            url_requests = []
            url_elements = root.findall('ns:url', namespaces)
            
            for url_element in url_elements:
                loc = url_element.find('ns:loc', namespaces)
                if loc is not None and loc.text:
                    url = loc.text
                    
                    # Apply custom root if provided
                    if custom_root:
                        url = self._replace_url_root(url, custom_root)
                    
                    url_requests.append(URLTestRequest(url=url))
            
            return url_requests
            
        except Exception as e:
            print(f"[WARNING] Could not parse sitemap {sitemap_url}: {str(e)}")
            return []
    
    def _replace_url_root(self, url: str, custom_root: str) -> str:
        """Replace the root/domain of a URL with a custom root"""
        parsed = urlparse(url)
        new_url = custom_root.rstrip('/') + parsed.path
        
        if parsed.query:
            new_url += '?' + parsed.query
        if parsed.fragment:
            new_url += '#' + parsed.fragment
        
        return new_url

