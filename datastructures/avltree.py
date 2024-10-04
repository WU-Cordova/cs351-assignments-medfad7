from __future__ import annotations

from dataclasses import dataclass
from collections import deque
from typing import Callable, Generic, List, Optional, Sequence, Tuple
from datastructures.iavltree import IAVLTree, K, V

class AVLNode(Generic[K,V]):
    def __init__(self, key: K, value: V, left: Optional[AVLNode]=None, right: Optional[AVLNode]=None):
        self._key = key
        self._value = value
        self._left = left
        self._right = right
        self._height = 1
        
    @property
    def key(self) -> K:
        return self._key
    
    @property
    def get_height(self) -> int:
        return self._height
    
    @property
    def balance_factor(self) -> int:
        left_height = self._left.get_height if self._left else 0
        right_height = self._right.get_height if self._right else 0
        return left_height - right_height
    
    @key.setter
    def key(self, new_key: K) -> None:
        self._key = new_key


class AVLTree(IAVLTree[K,V], Generic[K,V]):
    def __init__(self, stating_sequence: Optional[Sequence[Tuple]]=None):
        self._root = None
        if stating_sequence:
            for key, value in stating_sequence:
                self.insert(key, value)
                
    def __str__(self) -> str:
        return str(self.inorder())
        
    def print_tree(self, node: Optional[AVLNode], level=0, prefix="Root: "):
        if node is not None:
            print(" " * (level * 4) + prefix + str(node._key))
            self.print_tree(node._left, level + 1, "L--- ")
            self.print_tree(node._right, level + 1, "R--- ")
            
    def balance(self, node: AVLNode) -> AVLNode:
        if node.balance_factor > 1:
            if node._left.balance_factor < 0:
                node._left = self.rotate_left(node._left)
            return self.rotate_right(node)
        elif node.balance_factor < -1:
            if node._right.balance_factor > 0:
                node._right = self.rotate_right(node._right)
            return self.rotate_left(node)
        return node
                
    def update_height(self, node: AVLNode) -> None:
        left_height = node._left.get_height if node._left else 0
        right_height = node._right.get_height if node._right else 0
        node._height = max(left_height, right_height) + 1
        
    def rotate_right(self, node: AVLNode) -> AVLNode:
        new_root = node._left
        node._left = new_root._right
        new_root._right = node
        self.update_height(node)
        self.update_height(new_root)
        return new_root

    def rotate_left(self, node: AVLNode) -> AVLNode:
        new_root = node._right
        node._right = new_root._left
        new_root._left = node
        self.update_height(node)
        self.update_height(new_root)
        return new_root
    
    def _min_value_node(self, node: AVLNode) -> AVLNode:
        current = node
        while current._left is not None:
            current = current._left
        return current
    
    def insert(self, key: K, value: V) -> None:
        def _insert(node: AVLNode, key: K, value: V) -> AVLNode:
            if node is None:
                return AVLNode(key, value)
            if key < node.key:
                node._left = _insert(node._left, key, value)
            else:
                node._right = _insert(node._right, key, value)
            self.update_height(node)
            return self.balance(node)
        self._root = _insert(self._root, key, value)

    def search(self, key: K) -> V | None:
        def _search(node: AVLNode, key: K) -> V | None:
            if node is None:
                return None
            if key == node.key:
                return node._value
            if key < node.key:
                return _search(node._left, key)
            return _search(node._right, key)
        return _search(self._root, key)

    def delete(self, key: K) -> None:
        def _delete(node: AVLNode, key: K) -> AVLNode:
            if node is None:
                return None
            if key < node.key:
                node._left = _delete(node._left, key)
            elif key > node.key:
                node._right = _delete(node._right, key)
            else:
                if node._left is None:
                    return node._right
                if node._right is None:
                    return node._left
                temp = self._min_value_node(node._right)
                node._key = temp._key
                node._value = temp._value
                node._right = _delete(node._right, temp._key)
            self.update_height(node)
            return self.balance(node)
        self._root = _delete(self._root, key)

    def inorder(self, visit: Callable[[V], None] | None = None) -> List[K]:
        def _inorder(node: AVLNode, visit: Callable[[V], None] | None, keys: List[K]) -> List[K]:
            if node is not None:
                _inorder(node._left, visit, keys)
                if visit:
                    visit(node._value)
                keys.append(node._key)
                _inorder(node._right, visit, keys)
            return keys
        return _inorder(self._root, visit, [])

    def preorder(self, visit: Callable[[V], None] | None = None) -> List[K]:
        def _preorder(node: AVLNode, visit: Callable[[V], None] | None, keys: List[K]) -> List[K]:
            if node is not None:
                if visit:
                    visit(node._value)
                keys.append(node._key)
                _preorder(node._left, visit, keys)
                _preorder(node._right, visit, keys)
            return keys
        return _preorder(self._root, visit, [])

    def postorder(self, visit: Callable[[V], None] | None = None) -> List[K]:
        def _postorder(node: AVLNode, visit: Callable[[V], None] | None, keys: List[K]) -> List[K]:
            if node is not None:
                _postorder(node._left, visit, keys)
                _postorder(node._right, visit, keys)
                if visit:
                    visit(node._value)
                keys.append(node._key)
            return keys
        return _postorder(self._root, visit, [])
    
    def bforder(self, visit: Callable[[V], None] | None = None) -> List[K]:
        keys = []
        q = deque()
        q.append(self._root)
        while q:
            node = q.popleft()
            if node is not None:
                if visit:
                    visit(node._value)
                keys.append(node._key)
                q.append(node._left)
                q.append(node._right)
        return keys

    def size(self) -> int:
        def _size(node: AVLNode) -> int:
            if node is None:
                return 0
            return 1 + _size(node._left) + _size(node._right)
        return _size(self._root)
