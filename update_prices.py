#!/usr/bin/env python3
"""
Price Updater for Claude Statusline
Updates model pricing information from the official repository
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import urllib.request
import urllib.error
import ssl

# Default source URL
DEFAULT_SOURCE_URL = "https://raw.githubusercontent.com/ersinkoc/claude-statusline/refs/heads/feature/visual-statusline/prices.json"


class PriceUpdater:
    """Updates model pricing information from remote source"""
    
    def __init__(self, source_url: str = DEFAULT_SOURCE_URL, local_file: Optional[Path] = None):
        """
        Initialize price updater
        
        Args:
            source_url: URL to fetch prices from
            local_file: Local prices.json file path
        """
        self.source_url = source_url
        self.local_file = local_file or (Path(__file__).parent / "prices.json")
        
        # Create SSL context for HTTPS
        self.ssl_context = ssl.create_default_context()
    
    def fetch_remote_prices(self) -> Dict[str, Any]:
        """
        Fetch prices from remote source
        
        Returns:
            Dictionary containing price data
            
        Raises:
            Exception: If fetching fails
        """
        try:
            print(f"Fetching prices from: {self.source_url}")
            
            # Create request with headers
            request = urllib.request.Request(
                self.source_url,
                headers={
                    'User-Agent': 'Claude-Statusline-PriceUpdater/1.0',
                    'Accept': 'application/json'
                }
            )
            
            # Fetch data
            with urllib.request.urlopen(request, context=self.ssl_context, timeout=10) as response:
                data = response.read()
                return json.loads(data.decode('utf-8'))
                
        except urllib.error.HTTPError as e:
            raise Exception(f"HTTP Error {e.code}: {e.reason}")
        except urllib.error.URLError as e:
            raise Exception(f"URL Error: {e.reason}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {e}")
        except Exception as e:
            raise Exception(f"Failed to fetch prices: {e}")
    
    def load_local_prices(self) -> Optional[Dict[str, Any]]:
        """
        Load current local prices
        
        Returns:
            Dictionary containing current prices or None if file doesn't exist
        """
        if not self.local_file.exists():
            return None
        
        try:
            with open(self.local_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load local prices: {e}")
            return None
    
    def backup_current_prices(self):
        """Create backup of current prices before updating"""
        if not self.local_file.exists():
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.local_file.parent / f"prices_backup_{timestamp}.json"
            
            with open(self.local_file, 'r', encoding='utf-8') as source:
                with open(backup_file, 'w', encoding='utf-8') as backup:
                    backup.write(source.read())
            
            print(f"Backup created: {backup_file}")
            
        except Exception as e:
            print(f"Warning: Could not create backup: {e}")
    
    def compare_prices(self, old_prices: Dict[str, Any], new_prices: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare old and new prices to find changes
        
        Args:
            old_prices: Current local prices
            new_prices: New remote prices
            
        Returns:
            Dictionary of changes
        """
        changes = {
            'new_models': [],
            'removed_models': [],
            'price_changes': [],
            'updated_fields': []
        }
        
        old_models = set(old_prices.get('models', {}).keys())
        new_models = set(new_prices.get('models', {}).keys())
        
        # Find new models
        for model in new_models - old_models:
            changes['new_models'].append(model)
            print(f"  + New model: {model}")
        
        # Find removed models
        for model in old_models - new_models:
            changes['removed_models'].append(model)
            print(f"  - Removed model: {model}")
        
        # Find price changes
        for model in old_models & new_models:
            old_model_data = old_prices['models'][model]
            new_model_data = new_prices['models'][model]
            
            # Check pricing fields
            for field in ['input', 'output', 'cache_write_5m', 'cache_read']:
                if field in old_model_data and field in new_model_data:
                    if old_model_data[field] != new_model_data[field]:
                        changes['price_changes'].append({
                            'model': model,
                            'field': field,
                            'old': old_model_data[field],
                            'new': new_model_data[field]
                        })
                        print(f"  ~ {model} {field}: ${old_model_data[field]} -> ${new_model_data[field]}")
        
        # Check metadata changes
        if old_prices.get('last_updated') != new_prices.get('last_updated'):
            changes['updated_fields'].append('last_updated')
            print(f"  ~ Updated date: {old_prices.get('last_updated')} -> {new_prices.get('last_updated')}")
        
        return changes
    
    def update_prices(self, force: bool = False, backup: bool = True) -> bool:
        """
        Update local prices from remote source
        
        Args:
            force: Force update even if no changes
            backup: Create backup before updating
            
        Returns:
            True if updated, False otherwise
        """
        try:
            # Fetch remote prices
            new_prices = self.fetch_remote_prices()
            
            # Validate structure
            if 'models' not in new_prices:
                raise Exception("Invalid price data: missing 'models' field")
            
            # Load current prices
            old_prices = self.load_local_prices()
            
            # Compare if we have existing prices
            if old_prices and not force:
                print("\nComparing prices...")
                changes = self.compare_prices(old_prices, new_prices)
                
                # Check if any changes
                total_changes = (
                    len(changes['new_models']) +
                    len(changes['removed_models']) +
                    len(changes['price_changes']) +
                    len(changes['updated_fields'])
                )
                
                if total_changes == 0:
                    print("[OK] Prices are already up to date!")
                    return False
                
                print(f"\nFound {total_changes} changes")
            
            # Create backup if requested
            if backup and old_prices:
                self.backup_current_prices()
            
            # Update local file
            with open(self.local_file, 'w', encoding='utf-8') as f:
                json.dump(new_prices, f, indent=2, ensure_ascii=False)
            
            print(f"[OK] Successfully updated prices.json")
            print(f"  Last updated: {new_prices.get('last_updated', 'Unknown')}")
            print(f"  Models: {len(new_prices.get('models', {}))}")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to update prices: {e}")
            return False
    
    def verify_prices(self) -> bool:
        """
        Verify that local prices are valid
        
        Returns:
            True if valid, False otherwise
        """
        try:
            if not self.local_file.exists():
                print("[ERROR] prices.json not found")
                return False
            
            with open(self.local_file, 'r', encoding='utf-8') as f:
                prices = json.load(f)
            
            # Check required fields
            required_fields = ['models', 'last_updated']
            for field in required_fields:
                if field not in prices:
                    print(f"[ERROR] Missing required field: {field}")
                    return False
            
            # Check model structure
            for model_id, model_data in prices['models'].items():
                required_model_fields = ['input', 'output', 'name']
                for field in required_model_fields:
                    if field not in model_data:
                        print(f"[ERROR] Model {model_id} missing field: {field}")
                        return False
            
            print(f"[OK] prices.json is valid")
            print(f"  Last updated: {prices.get('last_updated')}")
            print(f"  Models: {len(prices['models'])}")
            
            # Show active models
            active_models = [
                model_id for model_id, data in prices['models'].items()
                if data.get('active', False)
            ]
            print(f"  Active models: {len(active_models)}")
            
            return True
            
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON in prices.json: {e}")
            return False
        except Exception as e:
            print(f"[ERROR] Error verifying prices: {e}")
            return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Update Claude Statusline model prices',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python update_prices.py           # Update prices from default source
  python update_prices.py --verify  # Verify local prices
  python update_prices.py --force   # Force update even if unchanged
  python update_prices.py --no-backup  # Update without creating backup
  python update_prices.py --source https://example.com/prices.json  # Custom source
        """
    )
    
    parser.add_argument(
        '--source',
        default=DEFAULT_SOURCE_URL,
        help='Source URL for prices.json'
    )
    
    parser.add_argument(
        '--verify',
        action='store_true',
        help='Verify local prices without updating'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force update even if prices haven\'t changed'
    )
    
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Don\'t create backup before updating'
    )
    
    parser.add_argument(
        '--local-file',
        type=Path,
        help='Path to local prices.json file'
    )
    
    args = parser.parse_args()
    
    # Initialize updater
    updater = PriceUpdater(
        source_url=args.source,
        local_file=args.local_file
    )
    
    # Run requested action
    if args.verify:
        success = updater.verify_prices()
    else:
        print("Claude Statusline Price Updater")
        print("=" * 40)
        success = updater.update_prices(
            force=args.force,
            backup=not args.no_backup
        )
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()