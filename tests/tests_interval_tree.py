import pytest

from datastructures.intervaltree import IntervalTree
from datastructures.avltree import AVLTree
from datastructures.intervaltree import IntervalNode

class TestIntervalTree:
    @pytest.fixture
    def intervaltree(self) -> IntervalTree:
        tree = IntervalTree()
        tree.insert(low=15, high=20, stock_name='APPLE', stock_symbol='AAPL')
        tree.insert(low=10, high=30, stock_name='MICROSOFT' , stock_symbol='MSFT')
        tree.insert(low=17, high=19, stock_name='GOOGLE', stock_symbol='GOOGL')
        tree.insert(low=5, high=20, stock_name='AMAZON', stock_symbol='AMZN')
        tree.insert(low=12, high=15,stock_name='TESLA', stock_symbol='TSLA')
        tree.insert(low=30, high=40, stock_name='NETFLIX', stock_symbol='NFLX')
        
        return tree
    
    def test_insert(self, intervaltree: IntervalTree) -> None:
        assert intervaltree._tree._root.key == 15
        assert intervaltree._tree._root._value.intervals_at_low._root.key == 20
        assert intervaltree._tree._root._value.max_end == 40
        
    def test_delete(self, intervaltree: IntervalTree) -> None:
        intervaltree._tree.print_tree(intervaltree._tree._root)
        intervaltree.delete(15, 20)
        intervaltree._tree.print_tree(intervaltree._tree._root)
        assert intervaltree._tree._root.key == 17
        assert intervaltree._tree._root._value.intervals_at_low._root.key == 19
        assert intervaltree._tree._root._value.max_end == 40
        
    def test_range_search(self, intervaltree: IntervalTree) -> None:
        assert intervaltree.range_search(14, 20) == [(15, 20, 'APPLE'), (17, 19, 'GOOGLE')]
        
    def test_bottom_k(self, intervaltree: IntervalTree) -> None:
        assert intervaltree.bottom_k_stocks(3) == [('AMAZON', 5), ('MICROSOFT', 10), ('TESLA', 12)]
        
    def test_top_k(self, intervaltree: IntervalTree) -> None:
        assert intervaltree.top_k_stocks(3) == [('NETFLIX', 30), ('GOOGLE', 17), ('APPLE', 15)]