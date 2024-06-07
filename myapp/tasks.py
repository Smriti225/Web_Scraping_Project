from celery import shared_task
from .models import ScrapeJob
from .scraper import CoinMarketCapScraper
import json

@shared_task
def scrape_coins(job_id, coins):
    job = ScrapeJob.objects.get(job_id=job_id)
    job.status = 'IN_PROGRESS'
    job.save()
    scraper = CoinMarketCapScraper()
    results = {}
    print(f"data is fetched {scraper}")
    for coin in coins:
        results[coin] = scraper.scrape_coin(coin)
    
    scraper.close()

    job.data = results
    job.status = 'COMPLETED'
    job.save()
    
    return results
