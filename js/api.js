const API_BASE = "http://127.0.0.1:8000";

async function generateBlog(notes) {

    const response = await fetch(`${API_BASE}/api/blog`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            notes: notes
        })
    });

    if (!response.ok) {
        throw new Error("Blog generation failed.");
    }

    return await response.json();
}


async function askReasoning(question) {

    const response = await fetch(`${API_BASE}/api/reasoning`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            question: question
        })
    });

    if (!response.ok) {
        throw new Error("Reasoning agent is unavailable.");
    }

    return await response.json();
}


async function askChat(message, history = []) {

    const response = await fetch(`${API_BASE}/api/chat`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: message,
            history: history
        })
    });

    if (!response.ok) {
        throw new Error("Chat assistant is unavailable.");
    }

    return await response.json();
}