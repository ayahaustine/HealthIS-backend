from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import connection
from datetime import datetime


def execute_raw_sql(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()


class TotalClientsView(APIView):
    permission_classes = [IsAuthenticated]

    """
    Total Clients (with Growth from Last Month)
    """

    def get(self, request, *args, **kwargs):
        query_current_month = """
            SELECT COUNT(*) 
            FROM clients_client 
            WHERE created_at >= DATE_TRUNC('month', CURRENT_DATE);
        """
        query_last_month = """
            SELECT COUNT(*) 
            FROM clients_client 
            WHERE created_at >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 month'
            AND created_at < DATE_TRUNC('month', CURRENT_DATE);
        """
        
        result_current = execute_raw_sql(query_current_month)
        result_last = execute_raw_sql(query_last_month)
        
        current_count = result_current[0][0]
        last_count = result_last[0][0]
        
        growth_percentage = ((current_count - last_count) / last_count * 100) if last_count > 0 else 0
        
        return Response({
            "total_clients": current_count,
            "growth_percentage": growth_percentage
        })


class ActiveProgramsView(APIView):
    permission_classes = [IsAuthenticated]

    """
    Active Programs (with Growth from Last Month)
    """

    def get(self, request, *args, **kwargs):
        query_current_month = """
            SELECT COUNT(*) 
            FROM programs_program 
            WHERE status = 'active' 
            AND created_at >= DATE_TRUNC('month', CURRENT_DATE);
        """
        query_last_month = """
            SELECT COUNT(*) 
            FROM programs_program 
            WHERE status = 'active' 
            AND created_at >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 month' 
            AND created_at < DATE_TRUNC('month', CURRENT_DATE);
        """
        
        result_current = execute_raw_sql(query_current_month)
        result_last = execute_raw_sql(query_last_month)
        
        current_count = result_current[0][0]
        last_count = result_last[0][0]
        
        growth_percentage = ((current_count - last_count) / last_count * 100) if last_count > 0 else 0
        
        return Response({
            "active_programs": current_count,
            "growth_percentage": growth_percentage
        })


class EnrollmentsView(APIView):
    permission_classes = [IsAuthenticated]

    """
    Enrollments (with Growth from Last Month)
    """

    def get(self, request, *args, **kwargs):
        query_current_month = """
            SELECT COUNT(*) 
            FROM enrollments_enrollment 
            WHERE enrolled_at >= NOW() - INTERVAL '30 days';
        """
        query_last_month = """
            SELECT COUNT(*) 
            FROM enrollments_enrollment 
            WHERE enrolled_at >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 month' 
            AND enrolled_at < DATE_TRUNC('month', CURRENT_DATE);
        """
        
        result_current = execute_raw_sql(query_current_month)
        result_last = execute_raw_sql(query_last_month)
        
        current_count = result_current[0][0]
        last_count = result_last[0][0]
        
        growth_percentage = ((current_count - last_count) / last_count * 100) if last_count > 0 else 0
        
        return Response({
            "enrollments": current_count,
            "growth_percentage": growth_percentage
        })
