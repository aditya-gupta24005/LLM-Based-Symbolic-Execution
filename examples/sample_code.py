"""
Sample Python Code for Testing the AST Analyzer
This file demonstrates various Python constructs
"""

# Import statements
import os
import sys
from typing import List, Dict, Optional

# Global constant
MAX_RETRIES = 3

# Class definition
class DataProcessor:
    """A sample data processor class"""
    
    def __init__(self, name: str, max_items: int = 100):
        self.name = name
        self.max_items = max_items
        self.items: List[Dict] = []
    
    def add_item(self, item: Dict) -> bool:
        """Add an item to the processor"""
        if len(self.items) < self.max_items:
            self.items.append(item)
            return True
        return False
    
    def process_items(self) -> List[Dict]:
        """Process all items"""
        results = []
        for item in self.items:
            processed = self._process_single(item)
            if processed:
                results.append(processed)
        return results
    
    def _process_single(self, item: Dict) -> Optional[Dict]:
        """Process a single item"""
        try:
            # Simulate processing
            result = {
                'id': item.get('id'),
                'value': item.get('value', 0) * 2,
                'status': 'processed'
            }
            return result
        except Exception as e:
            print(f"Error processing item: {e}")
            return None

# Function with multiple control structures
def calculate_fibonacci(n: int) -> List[int]:
    """Calculate Fibonacci sequence up to n terms"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    
    sequence = [0, 1]
    while len(sequence) < n:
        next_value = sequence[-1] + sequence[-2]
        sequence.append(next_value)
    
    return sequence

# Main execution block
if __name__ == "__main__":
    processor = DataProcessor("TestProcessor")
    
    # Add some test items
    for i in range(10):
        processor.add_item({'id': i, 'value': i * 10})
    
    # Process items
    results = processor.process_items()
    print(f"Processed {len(results)} items")
    
    # Calculate Fibonacci
    fib = calculate_fibonacci(10)
    print(f"Fibonacci sequence: {fib}")