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



class MonthlyEnrollmentsView(APIView):
    permission_classes = [IsAuthenticated]

    """"
    Monthly Enrollments (Client enrollment across all programs)
    """

    def get(self, request, *args, **kwargs):
        query = """
            SELECT
                EXTRACT(MONTH FROM e.enrolled_at) AS month,
                EXTRACT(YEAR FROM e.enrolled_at) AS year,
                COUNT(*) AS total_enrollments
            FROM
                enrollments_enrollment e
            GROUP BY
                year, month
            ORDER BY
                year DESC, month DESC;
        """
        
        result = execute_raw_sql(query)
        
        # Process the result into a more readable format (grouped by month and year)
        monthly_enrollments = {}
        for row in result:
            year = int(row[1])
            month = int(row[0])
            total_enrollments = row[2]

            if year not in monthly_enrollments:
                monthly_enrollments[year] = {}

            monthly_enrollments[year][month] = total_enrollments

        return Response(monthly_enrollments)
    


class MonthlyClientsAndProgramsView(APIView):
    permission_classes = [IsAuthenticated]
    """
    Monthly Clients and Programs (Client enrollment across all programs)
    """

    def get(self, request, *args, **kwargs):
        query = """
            SELECT
                EXTRACT(YEAR FROM e.enrolled_at) AS year,
                EXTRACT(MONTH FROM e.enrolled_at) AS month,
                COUNT(DISTINCT e.client_id) AS total_clients,
                COUNT(DISTINCT e.program_id) AS total_programs
            FROM
                enrollments_enrollment e
            JOIN
                clients_client c ON e.client_id = c.uuid
            JOIN
                programs_program p ON e.program_id = p.uuid
            GROUP BY
                year, month
            ORDER BY
                year DESC, month DESC;
        """
        
        result = execute_raw_sql(query)

        # Process the result into a more readable format
        monthly_data = {
            "months": [],
            "clients": [],
            "programs": []
        }

        for row in result:
            year = int(row[0])
            month = int(row[1])
            total_clients = row[2]
            total_programs = row[3]

            # Format month and year as "YYYY-MM"
            month_year = f"{year}-{month:02d}"
            monthly_data["months"].append(month_year)
            monthly_data["clients"].append(total_clients)
            monthly_data["programs"].append(total_programs)

        return Response(monthly_data)