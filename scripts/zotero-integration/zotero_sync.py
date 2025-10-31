#!/usr/bin/env python3
"""
Zotero Sync Script with PDF Caching and Manifest Generation.

This script:
1. Fetches group library metadata from Zotero API
2. Downloads and caches PDF attachments to /zotero-cache/
3. Generates zotero-manifest.json with metadata, paths, and links
4. Manages cache (cleanup, deduplication)
"""

import os
import sys
import json
import argparse
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import requests
from urllib.parse import quote


@dataclass
class ZoteroAttachment:
    """Represents a Zotero attachment (PDF)."""
    key: str
    parent_item: str
    title: str
    filename: str
    url: str
    md5: Optional[str] = None
    cached_path: Optional[str] = None
    size_bytes: Optional[int] = None


@dataclass
class ZoteroManifestItem:
    """Complete item metadata for the manifest."""
    key: str
    version: int
    item_type: str
    title: str
    creators: List[Dict[str, str]]
    abstract: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    date: Optional[str] = None
    tags: List[str] = None
    collections: List[str] = None
    attachments: List[str] = None  # Keys of attachment items
    zotero_url: str = ""
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.collections is None:
            self.collections = []
        if self.attachments is None:
            self.attachments = []


class ZoteroSync:
    """Handles syncing with Zotero API and managing local cache."""
    
    def __init__(self, group_id: str, api_key: Optional[str] = None, cache_dir: str = "zotero-cache"):
        self.group_id = group_id
        self.api_key = api_key
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.base_url = f"https://api.zotero.org/groups/{group_id}"
        self.headers = {
            "User-Agent": "weird-science-zotero-sync/1.0",
            "Zotero-API-Version": "3"
        }
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
    
    def fetch_all_items(self, limit: int = 100) -> List[Dict]:
        """Fetch all items from the Zotero group library."""
        all_items = []
        start = 0
        
        print(f"Fetching items from Zotero group {self.group_id}...")
        
        while True:
            url = f"{self.base_url}/items"
            params = {
                "limit": limit,
                "start": start,
                "format": "json",
                "include": "data"
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
                response.raise_for_status()
                
                items = response.json()
                if not items:
                    break
                
                all_items.extend(items)
                print(f"  Fetched {len(all_items)} items so far...")
                
                # Check if there are more items
                total_results = response.headers.get("Total-Results")
                if total_results and len(all_items) >= int(total_results):
                    break
                
                start += limit
                
            except requests.exceptions.RequestException as e:
                print(f"Error fetching items: {e}", file=sys.stderr)
                break
        
        print(f"Total items fetched: {len(all_items)}")
        return all_items
    
    def download_attachment(self, attachment_key: str, parent_key: str, filename: str) -> Optional[Path]:
        """Download a PDF attachment and cache it locally."""
        # Sanitize filename
        safe_filename = "".join(c for c in filename if c.isalnum() or c in "._- ").strip()
        if not safe_filename:
            safe_filename = f"attachment_{attachment_key}.pdf"
        
        # Create parent item directory
        parent_dir = self.cache_dir / parent_key
        parent_dir.mkdir(parents=True, exist_ok=True)
        
        cached_file = parent_dir / safe_filename
        
        # Skip if already cached
        if cached_file.exists():
            print(f"  Already cached: {cached_file.name}")
            return cached_file
        
        # Download the file
        url = f"{self.base_url}/items/{attachment_key}/file"
        
        try:
            print(f"  Downloading: {filename}...")
            response = requests.get(url, headers=self.headers, timeout=60, stream=True)
            response.raise_for_status()
            
            # Write to file
            with open(cached_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"  ✓ Cached: {cached_file.name} ({cached_file.stat().st_size} bytes)")
            return cached_file
            
        except requests.exceptions.RequestException as e:
            print(f"  Error downloading {filename}: {e}", file=sys.stderr)
            return None
    
    def process_items(self, items: List[Dict]) -> Tuple[List[ZoteroManifestItem], List[ZoteroAttachment]]:
        """Process raw Zotero items into structured manifest items and attachments."""
        manifest_items = []
        attachments = []
        attachment_map = {}  # attachment_key -> parent_key
        
        # First pass: identify attachments and their parents
        for item in items:
            data = item.get("data", {})
            item_type = data.get("itemType", "")
            
            if item_type == "attachment":
                parent_item = data.get("parentItem")
                if parent_item:
                    attachment_map[data.get("key")] = parent_item
        
        # Second pass: process main items
        for item in items:
            data = item.get("data", {})
            key = data.get("key")
            item_type = data.get("itemType", "")
            
            # Skip attachments and notes in main items list
            if item_type in ["attachment", "note"]:
                continue
            
            # Extract creators
            creators = []
            for creator in data.get("creators", []):
                creator_dict = {
                    "creatorType": creator.get("creatorType", ""),
                    "firstName": creator.get("firstName", ""),
                    "lastName": creator.get("lastName", ""),
                    "name": creator.get("name", "")
                }
                creators.append(creator_dict)
            
            # Extract tags
            tags = [tag.get("tag", "") for tag in data.get("tags", [])]
            
            # Find attachments for this item
            item_attachments = [att_key for att_key, parent in attachment_map.items() if parent == key]
            
            manifest_item = ZoteroManifestItem(
                key=key,
                version=data.get("version", 0),
                item_type=item_type,
                title=data.get("title", "Untitled"),
                creators=creators,
                abstract=data.get("abstractNote"),
                doi=data.get("DOI"),
                url=data.get("url"),
                date=data.get("date"),
                tags=tags,
                collections=data.get("collections", []),
                attachments=item_attachments,
                zotero_url=f"https://www.zotero.org/groups/{self.group_id}/items/{key}"
            )
            manifest_items.append(manifest_item)
        
        # Third pass: process attachment items
        for item in items:
            data = item.get("data", {})
            item_type = data.get("itemType", "")
            
            if item_type == "attachment" and data.get("contentType") == "application/pdf":
                key = data.get("key")
                parent_item = data.get("parentItem")
                
                if parent_item:
                    attachment = ZoteroAttachment(
                        key=key,
                        parent_item=parent_item,
                        title=data.get("title", "Untitled"),
                        filename=data.get("filename", f"{key}.pdf"),
                        url=data.get("url", ""),
                        md5=data.get("md5")
                    )
                    attachments.append(attachment)
        
        return manifest_items, attachments
    
    def download_all_attachments(self, attachments: List[ZoteroAttachment]) -> None:
        """Download all PDF attachments."""
        if not attachments:
            print("No PDF attachments to download.")
            return
        
        print(f"\nDownloading {len(attachments)} PDF attachments...")
        
        for i, attachment in enumerate(attachments, 1):
            print(f"\n[{i}/{len(attachments)}] {attachment.filename}")
            
            cached_path = self.download_attachment(
                attachment.key,
                attachment.parent_item,
                attachment.filename
            )
            
            if cached_path:
                attachment.cached_path = str(cached_path.relative_to(self.cache_dir))
                attachment.size_bytes = cached_path.stat().st_size
    
    def generate_manifest(self, 
                         manifest_items: List[ZoteroManifestItem], 
                         attachments: List[ZoteroAttachment]) -> Dict:
        """Generate the complete manifest JSON."""
        manifest = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "group_id": self.group_id,
            "total_items": len(manifest_items),
            "total_attachments": len(attachments),
            "items": [asdict(item) for item in manifest_items],
            "attachments": [asdict(att) for att in attachments]
        }
        return manifest
    
    def save_manifest(self, manifest: Dict, filepath: str = None) -> None:
        """Save manifest to JSON file."""
        if filepath is None:
            filepath = self.cache_dir / "zotero-manifest.json"
        else:
            filepath = Path(filepath)
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Manifest saved to: {filepath}")
        print(f"  Items: {manifest['total_items']}")
        print(f"  Attachments: {manifest['total_attachments']}")


def main():
    parser = argparse.ArgumentParser(
        description="Sync Zotero group library with PDF caching and manifest generation"
    )
    parser.add_argument(
        "--group-id",
        default=os.environ.get("ZOTERO_GROUP_ID", "6182921"),
        help="Zotero group ID (default: %(default)s)"
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("ZOTERO_API_KEY"),
        help="Zotero API key for private access"
    )
    parser.add_argument(
        "--cache-dir",
        default="zotero-cache",
        help="Directory for caching PDFs (default: %(default)s)"
    )
    parser.add_argument(
        "--generate-manifest",
        action="store_true",
        default=True,
        help="Generate zotero-manifest.json (default: True)"
    )
    parser.add_argument(
        "--download-pdfs",
        action="store_true",
        default=True,
        help="Download PDF attachments (default: True)"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("Zotero Sync - PDF Caching and Manifest Generation")
    print("=" * 70)
    print(f"Group ID: {args.group_id}")
    print(f"Cache Directory: {args.cache_dir}")
    print(f"API Key: {'*' * 8 if args.api_key else 'Not provided (public access)'}")
    print()
    
    # Initialize syncer
    syncer = ZoteroSync(args.group_id, args.api_key, args.cache_dir)
    
    # Fetch all items
    raw_items = syncer.fetch_all_items()
    
    if not raw_items:
        print("No items found in the library.")
        return 0
    
    # Process items
    print("\nProcessing items...")
    manifest_items, attachments = syncer.process_items(raw_items)
    print(f"  Main items: {len(manifest_items)}")
    print(f"  Attachments: {len(attachments)}")
    
    # Download PDFs if requested
    if args.download_pdfs:
        syncer.download_all_attachments(attachments)
    
    # Generate and save manifest
    if args.generate_manifest:
        manifest = syncer.generate_manifest(manifest_items, attachments)
        syncer.save_manifest(manifest)
    
    print("\n" + "=" * 70)
    print("Sync complete!")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
