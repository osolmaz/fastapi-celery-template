import requests
import time
import sys
import argparse


def create_data(api_url, content):
    """
    Sends a POST request to create data.

    Args:
        api_url (str): The base URL of the FastAPI application.
        content (str): The content to be sent in the POST request.

    Returns:
        str: The task URL to poll for task status.
    """
    endpoint = f"{api_url}/data/"
    payload = {"content": content}
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        data = response.json()
        task_url = data.get("task_url")
        if not task_url:
            print("Error: 'task_url' not found in the response.")
            sys.exit(1)
        return task_url
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        sys.exit(1)


def poll_task(task_url, poll_interval=2, timeout=60):
    """
    Polls the task URL to check the status of the Celery task.

    Args:
        task_url (str): The URL to poll for task status.
        poll_interval (int, optional): Seconds between polls. Defaults to 2.
        timeout (int, optional): Maximum seconds to wait for task completion. Defaults to 60.

    Returns:
        dict: The task result if successful.

    Raises:
        TimeoutError: If the task does not complete within the timeout period.
    """
    start_time = time.time()
    while True:
        try:
            response = requests.get(task_url)
            response.raise_for_status()
            data = response.json()
            status = data.get("status")
            # print(f"Task Status: {status}")
            print(data)
            if status == "SUCCESS":
                result = data.get("result")
                print("Task completed successfully.")
                return result
            elif status == "FAILURE":
                error = data.get("error")
                print(f"Task failed with error: {error}")
                sys.exit(1)
            elif status in ["PENDING", "STARTED", "RETRY"]:
                # Task is still in progress
                pass
            else:
                print(f"Unknown task status: {status}")
                sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(f"HTTP Request failed while polling: {e}")
            sys.exit(1)

        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            raise TimeoutError(f"Task did not complete within {timeout} seconds.")

        time.sleep(poll_interval)


def main():
    parser = argparse.ArgumentParser(
        description="Client to interact with FastAPI and Celery backend."
    )
    parser.add_argument(
        "--api-url",
        type=str,
        default="http://localhost:8000",
        help="Base URL of the FastAPI application (default: http://localhost:8000)",
    )
    parser.add_argument(
        "--content",
        type=str,
        default="hello world",
        help="Content to send in the POST request (default: 'hello world')",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=2,
        help="Seconds between polling attempts (default: 2)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Maximum seconds to wait for task completion (default: 60)",
    )
    args = parser.parse_args()

    api_url = args.api_url.rstrip("/")
    content = args.content
    poll_interval = args.poll_interval
    timeout = args.timeout

    print(f"Creating data with content: '{content}'")
    task_url = create_data(api_url, content)
    print(f"Task URL: {task_url}")

    try:
        print("Polling for task status...")
        result = poll_task(task_url, poll_interval, timeout)
        print(f"Task Result: {result}")
    except TimeoutError as te:
        print(str(te))
        sys.exit(1)


if __name__ == "__main__":
    main()
