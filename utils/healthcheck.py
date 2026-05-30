def pinghealthcheck(service:str='bot', fail:bool=False):
    import os
    from dotenv import load_dotenv
    import requests

    # Load environment variables from .env file
    load_dotenv()
    if service == 'backend':
        url = os.getenv('BACKEND_PUSH_HEALTHCHECK_URL') or os.getenv('PUSH_HEALTHCHECK_URL')
        fail_url = os.getenv('BACKEND_PUSH_HEALTHCHECK_FAIL_URL') or os.getenv('PUSH_HEALTHCHECK_FAIL_URL')
    else:
        url = os.getenv('PUSH_HEALTHCHECK_URL')
        fail_url = os.getenv('PUSH_HEALTHCHECK_FAIL_URL')

    if not url:
        print('Health check URL is not set in env (PUSH_HEALTHCHECK_URL).')
        return

    if fail:
        # Prefer explicit fail URL. If not provided, try deriving one from the success URL.
        if fail_url:
            url = fail_url
        else:
            url = url.replace('status=up', 'status=down').replace('msg=OK', 'msg=FAIL')
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Health check successful.")
        else:
            print(f"Health check failed with status code: {response.status_code}, check the URL in env")
    except requests.RequestException as e:
        print(f"An error occurred during the health check: {e}")