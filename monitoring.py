import json
import re
from collections import Counter
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path


MONITORING_DIR = Path("Monitoring")
TOPICS_FILE = MONITORING_DIR / "monitored_topics.json"
LAST_SOURCE_TEXT_FILE = MONITORING_DIR / "last_source_text.json"
MONITORING_LOG_FILE = MONITORING_DIR / "monitoring_log.md"


STOPWORDS = {
    "the",
    "and",
    "for",
    "that",
    "with",
    "this",
    "from",
    "are",
    "was",
    "were",
    "has",
    "have",
    "had",
    "not",
    "but",
    "you",
    "your",
    "they",
    "their",
    "his",
    "her",
    "its",
    "our",
    "about",
    "into",
    "over",
    "under",
    "after",
    "before",
    "between",
    "during",
    "will",
    "would",
    "could",
    "should",
    "may",
    "might",
    "can",
    "also",
    "than",
    "then",
    "there",
    "here",
    "when",
    "where",
    "what",
    "who",
    "why",
    "how",
    "been",
    "being",
    "because",
    "through",
    "while",
    "which",
    "these",
    "those",
    "into",
    "onto",
    "per",
    "via",
}


def ensure_monitoring_folder():
    MONITORING_DIR.mkdir(exist_ok=True)


def safe_read_json(file_path, default_value):
    ensure_monitoring_folder()

    if not file_path.exists():
        return default_value

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        return default_value

    except Exception:
        return default_value


def safe_write_json(file_path, data):
    ensure_monitoring_folder()

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def create_topic_id(topic_name):
    cleaned_name = re.sub(r"[^a-zA-Z0-9]+", "_", topic_name.lower()).strip("_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if not cleaned_name:
        cleaned_name = "monitoring_topic"

    return f"{cleaned_name}_{timestamp}"


def load_monitored_topics():
    topics = safe_read_json(TOPICS_FILE, [])

    if isinstance(topics, list):
        return topics

    return []


def save_monitored_topic(topic_data):
    ensure_monitoring_folder()

    topics = load_monitored_topics()

    topic_name = topic_data.get("topic_name", "").strip()

    if not topic_name:
        raise ValueError("A monitoring topic name is required.")

    topic_record = {
        "topic_id": topic_data.get("topic_id") or create_topic_id(topic_name),
        "topic_name": topic_name,
        "topic_description": topic_data.get("topic_description", "").strip(),
        "source_url": topic_data.get("source_url", "").strip(),
        "check_interval_hours": int(topic_data.get("check_interval_hours", 5)),
        "created_at": topic_data.get("created_at")
        or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_checked_at": topic_data.get("last_checked_at", ""),
        "status": topic_data.get("status", "active"),
    }

    topics.append(topic_record)
    safe_write_json(TOPICS_FILE, topics)

    log_monitoring_event(
        "Saved monitoring topic.",
        {
            "topic_id": topic_record["topic_id"],
            "topic_name": topic_record["topic_name"],
            "check_interval_hours": topic_record["check_interval_hours"],
        },
    )

    return str(TOPICS_FILE)


def update_topic_last_checked(topic_id):
    topics = load_monitored_topics()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for topic in topics:
        if topic.get("topic_id") == topic_id:
            topic["last_checked_at"] = now
            topic["updated_at"] = now

    safe_write_json(TOPICS_FILE, topics)

    return now


def normalize_text(text):
    if not text:
        return ""

    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    normalized = re.sub(r"[ \t]+", " ", normalized)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    return normalized.strip()


def tokenize_text(text):
    normalized = normalize_text(text).lower()
    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9]{2,}\b", normalized)

    return [word for word in words if word not in STOPWORDS]


def get_text_stats(text):
    normalized = normalize_text(text)
    words = tokenize_text(normalized)
    sentences = re.split(r"[.!?]+", normalized)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    lines = [line.strip() for line in normalized.splitlines() if line.strip()]

    return {
        "character_count": len(normalized),
        "word_count": len(words),
        "sentence_count": len(sentences),
        "line_count": len(lines),
    }


def get_top_keywords(text, limit=12):
    words = tokenize_text(text)
    word_counts = Counter(words)

    return [word for word, count in word_counts.most_common(limit)]


def calculate_similarity(previous_text, updated_text):
    previous_normalized = normalize_text(previous_text)
    updated_normalized = normalize_text(updated_text)

    if not previous_normalized and not updated_normalized:
        return 1.0

    return round(
        SequenceMatcher(None, previous_normalized, updated_normalized).ratio(),
        3,
    )


def get_line_changes(previous_text, updated_text, limit=12):
    previous_lines = [
        line.strip()
        for line in normalize_text(previous_text).splitlines()
        if line.strip()
    ]

    updated_lines = [
        line.strip()
        for line in normalize_text(updated_text).splitlines()
        if line.strip()
    ]

    previous_set = set(previous_lines)
    updated_set = set(updated_lines)

    added_lines = [line for line in updated_lines if line not in previous_set]
    removed_lines = [line for line in previous_lines if line not in updated_set]

    return {
        "added_lines": added_lines[:limit],
        "removed_lines": removed_lines[:limit],
        "added_line_count": len(added_lines),
        "removed_line_count": len(removed_lines),
    }


def identify_possible_significant_updates(previous_text, updated_text):
    previous_lower = normalize_text(previous_text).lower()
    updated_lower = normalize_text(updated_text).lower()

    update_indicators = {
        "location_update": [
            "location",
            "area",
            "county",
            "city",
            "region",
            "near",
            "at",
        ],
        "casualty_or_injury_update": [
            "injured",
            "injury",
            "fatal",
            "fatality",
            "dead",
            "death",
            "hospital",
            "critical",
        ],
        "damage_or_infrastructure_update": [
            "damage",
            "power",
            "road",
            "bridge",
            "water",
            "utility",
            "infrastructure",
            "closure",
            "evacuation",
        ],
        "official_statement_update": [
            "official",
            "confirmed",
            "statement",
            "announced",
            "reported",
            "agency",
            "department",
            "sheriff",
            "police",
            "fire",
        ],
        "timeline_update": [
            "today",
            "yesterday",
            "tomorrow",
            "morning",
            "afternoon",
            "evening",
            "night",
            "hours",
            "days",
            "updated",
        ],
        "risk_or_public_guidance_update": [
            "warning",
            "advisory",
            "shelter",
            "avoid",
            "remain",
            "risk",
            "threat",
            "hazard",
            "guidance",
        ],
    }

    detected_updates = []

    for category, keywords in update_indicators.items():
        for keyword in keywords:
            keyword_added = keyword in updated_lower and keyword not in previous_lower

            if keyword_added:
                detected_updates.append(category)
                break

    return sorted(set(detected_updates))


def decide_meaningful_change(similarity_score, line_changes, significant_updates):
    added_line_count = line_changes.get("added_line_count", 0)
    removed_line_count = line_changes.get("removed_line_count", 0)

    if similarity_score < 0.85:
        return True

    if added_line_count >= 3 or removed_line_count >= 3:
        return True

    if significant_updates:
        return True

    return False


def compare_source_changes(previous_text, updated_text):
    previous_normalized = normalize_text(previous_text)
    updated_normalized = normalize_text(updated_text)

    if not previous_normalized and not updated_normalized:
        return {
            "changed": False,
            "meaningful_change": False,
            "change_summary": "No source text was provided.",
            "similarity_score": 1.0,
            "previous_stats": get_text_stats(previous_text),
            "updated_stats": get_text_stats(updated_text),
            "line_changes": {
                "added_lines": [],
                "removed_lines": [],
                "added_line_count": 0,
                "removed_line_count": 0,
            },
            "possible_significant_updates": [],
            "previous_keywords": [],
            "updated_keywords": [],
            "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    if previous_normalized == updated_normalized:
        return {
            "changed": False,
            "meaningful_change": False,
            "change_summary": "No changes detected between the previous source text and the updated source text.",
            "similarity_score": 1.0,
            "previous_stats": get_text_stats(previous_text),
            "updated_stats": get_text_stats(updated_text),
            "line_changes": {
                "added_lines": [],
                "removed_lines": [],
                "added_line_count": 0,
                "removed_line_count": 0,
            },
            "possible_significant_updates": [],
            "previous_keywords": get_top_keywords(previous_text),
            "updated_keywords": get_top_keywords(updated_text),
            "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    similarity_score = calculate_similarity(previous_text, updated_text)
    line_changes = get_line_changes(previous_text, updated_text)
    possible_significant_updates = identify_possible_significant_updates(
        previous_text,
        updated_text,
    )

    meaningful_change = decide_meaningful_change(
        similarity_score,
        line_changes,
        possible_significant_updates,
    )

    previous_stats = get_text_stats(previous_text)
    updated_stats = get_text_stats(updated_text)

    added_word_count = updated_stats["word_count"] - previous_stats["word_count"]

    if meaningful_change:
        change_summary = (
            "Meaningful change detected. The updated source text includes enough new, removed, "
            "or potentially significant information to justify analyst review."
        )
    else:
        change_summary = (
            "Minor change detected. The updated source text changed, but the difference may not "
            "be significant enough to require a full updated report."
        )

    result = {
        "changed": True,
        "meaningful_change": meaningful_change,
        "change_summary": change_summary,
        "similarity_score": similarity_score,
        "word_count_change": added_word_count,
        "previous_stats": previous_stats,
        "updated_stats": updated_stats,
        "line_changes": line_changes,
        "possible_significant_updates": possible_significant_updates,
        "previous_keywords": get_top_keywords(previous_text),
        "updated_keywords": get_top_keywords(updated_text),
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    log_monitoring_event("Compared source text for changes.", result)

    return result


def load_last_source_text(topic_id):
    saved_text_records = safe_read_json(LAST_SOURCE_TEXT_FILE, {})

    if not isinstance(saved_text_records, dict):
        return ""

    topic_record = saved_text_records.get(topic_id, {})

    if isinstance(topic_record, dict):
        return topic_record.get("source_text", "")

    return ""


def save_last_source_text(topic_id, source_text, metadata=None):
    ensure_monitoring_folder()

    if metadata is None:
        metadata = {}

    saved_text_records = safe_read_json(LAST_SOURCE_TEXT_FILE, {})

    if not isinstance(saved_text_records, dict):
        saved_text_records = {}

    saved_text_records[topic_id] = {
        "topic_id": topic_id,
        "source_text": source_text,
        "metadata": metadata,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    safe_write_json(LAST_SOURCE_TEXT_FILE, saved_text_records)

    log_monitoring_event(
        "Saved latest source text for topic.",
        {
            "topic_id": topic_id,
            "metadata": metadata,
        },
    )

    return str(LAST_SOURCE_TEXT_FILE)


def record_monitoring_check(topic_id, topic_name, previous_text, updated_text):
    comparison_result = compare_source_changes(previous_text, updated_text)

    check_record = {
        "topic_id": topic_id,
        "topic_name": topic_name,
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "comparison_result": comparison_result,
    }

    if comparison_result.get("changed"):
        save_last_source_text(
            topic_id=topic_id,
            source_text=updated_text,
            metadata={
                "topic_name": topic_name,
                "meaningful_change": comparison_result.get("meaningful_change"),
                "checked_at": check_record["checked_at"],
            },
        )

    update_topic_last_checked(topic_id)

    log_monitoring_event("Recorded monitoring check.", check_record)

    return check_record


def get_monitoring_status_summary():
    topics = load_monitored_topics()
    saved_text_records = safe_read_json(LAST_SOURCE_TEXT_FILE, {})

    active_topics = [
        topic for topic in topics if topic.get("status", "active") == "active"
    ]

    return {
        "topic_count": len(topics),
        "active_topic_count": len(active_topics),
        "saved_source_text_count": len(saved_text_records)
        if isinstance(saved_text_records, dict)
        else 0,
        "monitoring_interval_default_hours": 5,
        "monitoring_folder": str(MONITORING_DIR),
        "topics_file": str(TOPICS_FILE),
        "last_source_text_file": str(LAST_SOURCE_TEXT_FILE),
        "monitoring_log_file": str(MONITORING_LOG_FILE),
    }


def log_monitoring_event(message, event_data=None):
    ensure_monitoring_folder()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(MONITORING_LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"\n## {timestamp}\n")
        file.write(f"{message}\n")

        if event_data is not None:
            file.write("\n```json\n")
            file.write(json.dumps(event_data, indent=4))
            file.write("\n```\n")

    return str(MONITORING_LOG_FILE)


if __name__ == "__main__":
    ensure_monitoring_folder()

    sample_previous_text = """
    City officials reported a chemical spill near an industrial facility.
    Roads near the facility were closed while crews assessed the scene.
    """

    sample_updated_text = """
    City officials reported a chemical spill near an industrial facility.
    Roads near the facility were closed while crews assessed the scene.
    Fire officials confirmed that two nearby businesses were evacuated as a precaution.
    The county emergency management office issued public guidance to avoid the area.
    """

    result = compare_source_changes(sample_previous_text, sample_updated_text)

    print(json.dumps(result, indent=4))