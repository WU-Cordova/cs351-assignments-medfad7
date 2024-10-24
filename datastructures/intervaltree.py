from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

from datastructures.avltree import AVLTree, AVLNode


class IntervalNode:
    key: int # low
    high: int # high
    value: str # Stock Name
    stock_symbol: str
    height: int = 1
    max_end: int = 0
    intervals_at_low: AVLTree
    
    def __init__(self, key: int, high: int, value: str, stock_symbol: str):
        self.key = key
        self.high = high
        self.value = value
        self.stock_symbol = stock_symbol
        self.height = 1
        self.max_end = high
        self.intervals_at_low = AVLTree()

class IntervalTree:
    def __init__(self):
        self._tree = AVLTree()
    
    def insert(self, low: int, high: int, stock_symbol: str, stock_name: str) -> None:
        # Search for the node with the given 'low'
        node = self._tree.search_node(low)

        # Create a new IntervalNode
        new_node = IntervalNode(key=low, high=high, value=stock_name, stock_symbol=stock_symbol)

        if node is None:
            # If no node exists with the 'low' key, insert a new one
            new_node.intervals_at_low.insert(key=high, value=stock_name)
            self._tree.insert(key=low, value=new_node)
        else:
            # If the node already exists, insert into its intervals_at_low
            node._value.intervals_at_low.insert(key=high, value=stock_name)
        
        # Update max_end recursively
        self._update_max_end(self._tree._root)

    def _update_max_end(self, node: AVLNode) -> int:
        if node is None:
            return 0

        # Max end from the left and right subtrees
        left_max = self._update_max_end(node._left)
        right_max = self._update_max_end(node._right)

        # Get the maximum high from intervals_at_low and the current node's high
        if node._value.intervals_at_low.is_empty():
            max_at_low = node._value.high
        else:
            # The max high value either comes from the current node's high or the intervals_at_low AVL tree
            max_at_low = max(node._value.high, node._value.intervals_at_low.get_max()._key)
        
        # Update the current node's max_end
        node._value.max_end = max(left_max, right_max, max_at_low)
        
        return node._value.max_end

    def delete(self, low: int, high: int) -> None:
        # Search for the node with the given low value
        node = self._tree.search_node(low)
        if node is None:
            return  # Node doesn't exist, nothing to delete
        
        # Delete from intervals_at_low first
        if node._value.intervals_at_low is not None:
            node._value.intervals_at_low.delete(key=high)
        
        # If no more intervals at this low value, delete the main node
        if node._value.intervals_at_low.is_empty():
            self._tree.delete(key=low)
        else:
            # Update max_end
            self._update_max_end(self._tree._root)

    # Other methods (e.g., for querying overlapping intervals, top_k, bottom_k) remain the same


    def range_search(self, low: int, high: int) -> List[Tuple[int, int, Any]]:
        """
        Find all intervals where both the low and high values fit within the given range [low, high].
        Use max_end metadata in each node to prune subtrees that fall outside the query range.
        """
        def _range_search(node: AVLNode, low: int, high: int) -> List[Tuple[int, int, Any]]:
            if node is None:
                return []

            result = []

            # Prune the search if the max_end in this subtree is less than the query low value
            if node._value.max_end < low:
                return result

            # Check if the current node's interval is fully within the range
            if low <= node._key and node._value.high <= high:
                result.append((node._key, node._value.high, node._value.value))

            # Search the left subtree if there's a possibility of relevant intervals
            if node._left is not None and node._left._value.max_end >= low:
                result += _range_search(node._left, low, high)

            # Search the right subtree if there's a possibility of relevant intervals
            if node._key <= high:
                result += _range_search(node._right, low, high)

            return result

        return _range_search(self._tree._root, low, high)

    
    def top_k_stocks(self, k: int) -> List[Tuple[str, int]]:
        def _top_k_stocks(node: AVLNode, k: int) -> List[Tuple[str, int]]:
            if node is None:
                return []
            
            left = _top_k_stocks(node._left, k)
            right = _top_k_stocks(node._right, k)
            
            result = left + [(node._value.value, node._value.key)] + right
            result.sort(key=lambda x: x[1], reverse=True)
            
            return result[:k]
        
        return _top_k_stocks(self._tree._root, k)
    
    def bottom_k_stocks(self, k: int) -> List[Tuple[str, int]]:
        def _bottom_k_stocks(node: AVLNode, k: int) -> List[Tuple[str, int]]:
            if node is None:
                return []
            
            left = _bottom_k_stocks(node._left, k)
            right = _bottom_k_stocks(node._right, k)
            
            result = left + [(node._value.value, node._value.key)] + right
            result.sort(key=lambda x: x[1])
            
            return result[:k]
        
        return _bottom_k_stocks(self._tree._root, k)