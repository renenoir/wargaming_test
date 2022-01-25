from django.test import TestCase
from django.urls import reverse

from django.core.cache import cache
from rest_framework.test import APIClient

from django_redis import get_redis_connection


FIBONACCI_URL = reverse('fibonacci')


class FibonacciApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        get_redis_connection("default").flushall()

    def test_fibonacci_slice(self):
        """Test returning fibonacci slice"""
        res = self.client.get(
            FIBONACCI_URL,
            {'fib_from': '5', 'fib_to': '10'}
        )
        self.assertEqual(res.data['data'], [5,8,13,21,34,55])
    
    def test_redis_cache(self):
        """Test that redis cache is working"""
        res = self.client.get(
            FIBONACCI_URL,
            {'fib_from': '10', 'fib_to': '15'}
        )
        redis_cache = []
        for x in range(10, 16):
            redis_cache.append(int(cache.get(f'{x}')))

        self.assertEqual(res.data['data'], redis_cache)

    
    def test_fibonacci_calculates_correctly(self):
        """Test that fibonacci number calculates correctly"""
        res = self.client.get(
            FIBONACCI_URL,
            {'fib_from': '10', 'fib_to': '15'}
        )
        
        self.assertEqual(
            res.data['data'][3], 
            (res.data['data'][1] + res.data['data'][2])
        )
