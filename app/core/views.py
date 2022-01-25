from django.core.cache import cache
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from .serializers import FibonacciSequenceSerializer


class FibonacciSequenceViewSet(views.APIView):

    def fibonacci(self, num):
        """Returns recursive calculated fibonacci number"""
        if str(num) in cache.keys('*'):
            return int(cache.get(f'{num}'))
        if num == 1:
            value = 1
        elif num == 2:
            value = 1
        elif num > 2:           
            value =  self.fibonacci(num -1) + self.fibonacci(num -2)
            
        cache.set(f'{num}', f'{value}', timeout=None)

        return value

    def fibonacci_sequence(self, fib_from, fib_to):
        """Returns list with fibonacci slice"""
        ints = []
        for x in range(1, fib_to+1):
            ints.append(self.fibonacci(x))

        return ints[fib_from-1:]

    def get(self, request):
        """Returns fibonacci slice in json format"""
        if self.request.query_params.get('from'):
            fib_from = int(self.request.query_params.get('from'))
        else:
            fib_from = 1
        if self.request.query_params.get('to'):
            fib_to = int(self.request.query_params.get('to'))
        else:
            return Response({
                'status' : 'Bad request',
                'message': '\'fib_to\' field is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
  
        fibonaccisequence = self.fibonacci_sequence(fib_from, fib_to)
        data = {'data': fibonaccisequence}
        results = FibonacciSequenceSerializer(data).data

        return Response(results)
