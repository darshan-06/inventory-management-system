import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)
    if response is None:
        logger.error(f"Unhandled exception: {exc}, Context: {context}")

        if hasattr(exc, 'status_code') and exc.status_code == 500:
            return Response({'status':'error', 'error': 'Internal server error. Please try again later.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR )
        
        return Response({'error': 'An unexpected error occurred. Please try again later.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response
    

