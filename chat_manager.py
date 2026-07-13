from datetime import datetime


# =====================================================
# CREATE CHAT HISTORY
# =====================================================

def initialize_chat():

    return []


# =====================================================
# ADD MESSAGE
# =====================================================

def add_message(chat_history, role, message):

    chat_history.append(

        {

            "role": role,

            "message": message,

            "time": datetime.now().strftime("%H:%M:%S")

        }

    )

    return chat_history


# =====================================================
# CLEAR CHAT
# =====================================================

def clear_chat():

    return []


# =====================================================
# EXPORT CHAT
# =====================================================

def export_chat(chat_history):

    report = []

    report.append("InsightOS Chat History")

    report.append("=" * 50)

    report.append("")

    for item in chat_history:

        report.append(

            f"[{item['time']}] {item['role'].upper()}"

        )

        report.append(

            item["message"]

        )

        report.append("")

    return "\n".join(report)


# =====================================================
# CHAT LENGTH
# =====================================================

def total_messages(chat_history):

    return len(chat_history)


# =====================================================
# LAST MESSAGE
# =====================================================

def last_message(chat_history):

    if len(chat_history) == 0:

        return None

    return chat_history[-1]


# =====================================================
# USER QUESTIONS
# =====================================================

def user_questions(chat_history):

    return [

        item

        for item in chat_history

        if item["role"] == "user"

    ]


# =====================================================
# AI RESPONSES
# =====================================================

def ai_responses(chat_history):

    return [

        item

        for item in chat_history

        if item["role"] == "assistant"

    ]


# =====================================================
# SEARCH CHAT
# =====================================================

def search_chat(chat_history, query):

    query = query.lower()

    results = []

    for item in chat_history:

        if query in item["message"].lower():

            results.append(item)

    return results


# =====================================================
# CHAT STATISTICS
# =====================================================

def chat_statistics(chat_history):

    return {

        "Total Messages": len(chat_history),

        "User Messages": len(user_questions(chat_history)),

        "AI Messages": len(ai_responses(chat_history))

    }