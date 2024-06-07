from celery import shared_task
from .models import ScrapeJob
from .scraper import CoinMarketCapScraper
import json

@shared_task
def scrape_coins(job_id, coins):
    print(job_id, coins)
    print("task initiated")
    job = ScrapeJob.objects.get(job_id=job_id)
    job.status = 'IN_PROGRESS'
    job.save()
    print("data is fetching")
    scraper = CoinMarketCapScraper()
    results = {}
    print(f"data is fetched {scraper}")
    for coin in coins:
        print(coin)
        results[coin] = scraper.scrape_coin(coin)
    
    scraper.close()

    job.data = results
    job.status = 'COMPLETED'
    job.save()
    
    return results
