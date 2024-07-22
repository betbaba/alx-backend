#!/usr/bin/env python3
"""Hypemedia pagination
"""
import csv
import math
from typing import List, Tuple, Dict, Any


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Arguments:
                page: int
                page_size: int
            Returns:
                list of records in a given page
        """
        data = []
        assert page > 0
        assert page_size > 0
        start, end = index_range(page, page_size)
        index = 0
        returned = self.dataset()
        if start > len(returned):
            return []
        while start < end:
            data.append(returned[start])
            index += 1
            start += 1
        return data

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """Arguments:
                page: int
                page_size: int
           Returns:
                dictionary
        """
        total_pages = math.ceil(len(self.dataset()) / page_size)
        data = self.get_page(page, page_size)
        next_page = page + 1 if page + 1 <= total_pages else None
        prev_page = page - 1 if page > 1 else None
        page_size = len(data)
        hyper = {'page_size': page_size, 'page': page, 'data': data,
                 'next_page': next_page, 'prev_page': prev_page,
                 'total_pages': total_pages}
        return hyper


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """ return a tuple of size two containing a start index and an end index
    """
    startIndex = (page - 1) * page_size
    endIndex = startIndex + page_size
    return (startIndex, endIndex)
