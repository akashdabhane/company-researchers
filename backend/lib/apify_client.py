import os
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

APIFY_API_KEY = os.getenv("APIFY_API_KEY", "")

apify_client = ApifyClient(APIFY_API_KEY) if APIFY_API_KEY else None


def run_apify_actor(actor_id: str, run_input: dict, timeout_secs: int = 120):
    """
    Executes an Apify actor and returns the dataset items as a list of dicts.
    Returns empty list if APIFY_API_KEY is missing or if the run fails.
    """
    if not APIFY_API_KEY or not apify_client:
        print(f"[Apify Warning] APIFY_API_KEY not set. Skipping actor run for '{actor_id}'.")
        return None

    try:
        print(f"[Apify] Launching actor '{actor_id}'...")
        run = apify_client.actor(actor_id).call(run_input=run_input, timeout_secs=timeout_secs)
        
        items = []
        if run and "defaultDatasetId" in run:
            dataset_items = apify_client.dataset(run["defaultDatasetId"]).list_items()
            items = dataset_items.items
            
        print(f"[Apify] Actor '{actor_id}' returned {len(items)} items.")
        return items
    except Exception as e:
        print(f"[Apify Error] Exception while running actor '{actor_id}': {e}")
        return None

