from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ScrapeJob
from .tasks import scrape_coins
import uuid

class StartScrapingView(APIView):
    def post(self, request):
        coins = request.data.get('coins', [])
        if not coins:
            return Response({"error": "No coins provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        job = ScrapeJob.objects.create()
        print("task callled")
        # scrape_coins.delay(job.job_id, coins)
        scrape_coins.apply_async((job.job_id, coins), countdown=4)

        return Response({"job_id": job.job_id}, status=status.HTTP_200_OK)

class ScrapingStatusView(APIView):
    def get(self, request, job_id):
        try:
            job = ScrapeJob.objects.get(job_id=job_id)
        except ScrapeJob.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            "job_id": job.job_id,
            "status": job.status,
            "data": job.data
        }, status=status.HTTP_200_OK)
