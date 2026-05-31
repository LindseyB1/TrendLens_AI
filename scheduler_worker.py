import argparse
import json
import time
from datetime import datetime, timedelta
from pathlib import Path

from monitoring import (
    MONITORING_LOG_FILE,
    compare_source_changes,
    ensure_monitoring_folder,
    load_last_source_text,
    load_monitored_topics,
    log_monitoring_event,
    record_monitoring_check,
    save_last_source_text,
    update_topic_last_checked,
)


DEFAULT_CHECK_INTERVAL_HOURS = 5
DEFAULT_POLL_MINUTES = 15
SCHEDULER_STATUS_FILE = Path("Monitoring") / "scheduler_status.json"


def parse_datetime(value):
    if not value:
        return None

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
    ]

    for date_format in formats:
        try:
            return datetime.strptime(value, date_format)
        except ValueError:
            continue

    return None


def is_topic_due_for_check(topic, current_time=None):
    if current_time is None:
        current_time = datetime.now()

    interval_hours = int(
        topic.get("check_interval_hours", DEFAULT_CHECK_INTERVAL_HOURS)
    )

    last_checked_at = parse_datetime(topic.get("last_checked_at", ""))

    if last_checked_at is None:
        return True

    next_due_time = last_checked_at + timedelta(hours=interval_hours)

    return current_time >= next_due_time


def get_due_topics():
    topics = load_monitored_topics()
    current_time = datetime.now()

    due_topics = []

    for topic in topics:
        if topic.get("status", "active") != "active":
            continue

        if is_topic_due_for_check(topic, current_time):
            due_topics.append(topic)

    return due_topics


def save_scheduler_status(status_data):
    ensure_monitoring_folder()

    with open(SCHEDULER_STATUS_FILE, "w", encoding="utf-8") as file:
        json.dump(status_data, file, indent=4)

    return str(SCHEDULER_STATUS_FILE)


def load_scheduler_status():
    ensure_monitoring_folder()

    if not SCHEDULER_STATUS_FILE.exists():
        return {}

    try:
        with open(SCHEDULER_STATUS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception:
        return {}


def build_status_snapshot():
    topics = load_monitored_topics()
    due_topics = get_due_topics()

    snapshot = {
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_topics": len(topics),
        "due_topics": len(due_topics),
        "due_topic_names": [
            topic.get("topic_name", "Unnamed topic") for topic in due_topics
        ],
        "default_check_interval_hours": DEFAULT_CHECK_INTERVAL_HOURS,
        "scheduler_status_file": str(SCHEDULER_STATUS_FILE),
        "monitoring_log_file": str(MONITORING_LOG_FILE),
    }

    save_scheduler_status(snapshot)

    return snapshot


def print_status():
    snapshot = build_status_snapshot()

    print(json.dumps(snapshot, indent=4))

    return snapshot


def run_due_topic_scan():
    due_topics = get_due_topics()

    scan_result = {
        "scan_started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "due_topic_count": len(due_topics),
        "results": [],
    }

    if not due_topics:
        log_monitoring_event(
            "Scheduler scan completed. No topics were due for review.",
            scan_result,
        )

        save_scheduler_status(scan_result)

        return scan_result

    for topic in due_topics:
        topic_id = topic.get("topic_id")
        topic_name = topic.get("topic_name", "Unnamed topic")

        result = {
            "topic_id": topic_id,
            "topic_name": topic_name,
            "status": "due_for_review",
            "message": (
                "Topic is due for a five hour monitoring review. "
                "The current draft requires the user or approved source connector "
                "to provide updated public source text before a change comparison is run."
            ),
            "source_url": topic.get("source_url", ""),
            "last_checked_at": topic.get("last_checked_at", ""),
            "check_interval_hours": topic.get(
                "check_interval_hours",
                DEFAULT_CHECK_INTERVAL_HOURS,
            ),
        }

        update_topic_last_checked(topic_id)
        scan_result["results"].append(result)

    scan_result["scan_completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_monitoring_event(
        "Scheduler scan completed. Topics due for monitoring review were identified.",
        scan_result,
    )

    save_scheduler_status(scan_result)

    return scan_result


def run_manual_update_check(topic_id, updated_source_text):
    if not topic_id:
        raise ValueError("topic_id is required.")

    if not updated_source_text or not updated_source_text.strip():
        raise ValueError("updated_source_text is required.")

    topics = load_monitored_topics()

    matching_topic = None

    for topic in topics:
        if topic.get("topic_id") == topic_id:
            matching_topic = topic
            break

    if matching_topic is None:
        raise ValueError(f"No monitoring topic found for topic_id: {topic_id}")

    previous_source_text = load_last_source_text(topic_id)

    if not previous_source_text:
        save_last_source_text(
            topic_id=topic_id,
            source_text=updated_source_text,
            metadata={
                "topic_name": matching_topic.get("topic_name", "Unnamed topic"),
                "note": "Initial source text saved. No previous text was available for comparison.",
            },
        )

        update_topic_last_checked(topic_id)

        result = {
            "topic_id": topic_id,
            "topic_name": matching_topic.get("topic_name", "Unnamed topic"),
            "status": "initial_source_text_saved",
            "message": (
                "Initial source text was saved for this topic. "
                "A future update can now be compared against this baseline."
            ),
            "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        log_monitoring_event("Manual update check saved baseline text.", result)

        return result

    result = record_monitoring_check(
        topic_id=topic_id,
        topic_name=matching_topic.get("topic_name", "Unnamed topic"),
        previous_text=previous_source_text,
        updated_text=updated_source_text,
    )

    log_monitoring_event("Manual update check completed.", result)

    return result


def run_loop(poll_minutes=DEFAULT_POLL_MINUTES):
    ensure_monitoring_folder()

    log_monitoring_event(
        "Scheduler worker started.",
        {
            "poll_minutes": poll_minutes,
            "default_check_interval_hours": DEFAULT_CHECK_INTERVAL_HOURS,
        },
    )

    print("TrendLens AI scheduler worker started.")
    print(f"Polling every {poll_minutes} minutes.")
    print("Press CTRL C to stop.")

    try:
        while True:
            result = run_due_topic_scan()

            print(json.dumps(result, indent=4))

            time.sleep(poll_minutes * 60)

    except KeyboardInterrupt:
        stop_message = {
            "stopped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": "Scheduler worker stopped by user.",
        }

        log_monitoring_event("Scheduler worker stopped.", stop_message)

        print("\nScheduler worker stopped.")


def main():
    parser = argparse.ArgumentParser(
        description="TrendLens AI scheduler worker for semi automated monitoring."
    )

    parser.add_argument(
        "--status",
        action="store_true",
        help="Show scheduler status and due monitoring topics.",
    )

    parser.add_argument(
        "--scan-once",
        action="store_true",
        help="Run one monitoring scan and exit.",
    )

    parser.add_argument(
        "--loop",
        action="store_true",
        help="Run the scheduler worker loop.",
    )

    parser.add_argument(
        "--poll-minutes",
        type=int,
        default=DEFAULT_POLL_MINUTES,
        help="How often the worker should poll for due topics when running in loop mode.",
    )

    parser.add_argument(
        "--manual-topic-id",
        type=str,
        default="",
        help="Topic ID for a manual update check.",
    )

    parser.add_argument(
        "--manual-text-file",
        type=str,
        default="",
        help="Path to a text file containing updated public source text.",
    )

    args = parser.parse_args()

    ensure_monitoring_folder()

    if args.status:
        print_status()
        return

    if args.scan_once:
        result = run_due_topic_scan()
        print(json.dumps(result, indent=4))
        return

    if args.manual_topic_id and args.manual_text_file:
        text_file_path = Path(args.manual_text_file)

        if not text_file_path.exists():
            raise FileNotFoundError(f"Text file not found: {text_file_path}")

        updated_source_text = text_file_path.read_text(encoding="utf-8")

        result = run_manual_update_check(
            topic_id=args.manual_topic_id,
            updated_source_text=updated_source_text,
        )

        print(json.dumps(result, indent=4))
        return

    if args.loop:
        run_loop(poll_minutes=args.poll_minutes)
        return

    print_status()


if __name__ == "__main__":
    main()