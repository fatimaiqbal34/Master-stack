const API_BASE_URL = "http://127.0.0.1:8000";

// Helper function to handle response errors
async function handleResponse(response) {
    if (!response.ok) {
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
            const errorData = await response.json();
            if (errorData.detail) {
                errorMessage = errorData.detail;
            }
        } catch (e) {
            // Failed to parse JSON error, fallback to status text
        }
        throw new Error(errorMessage);
    }
    return await response.json();
}

// 1. Generate Blog API Call
async function generateBlog(notes) {
    const response = await fetch(`${API_BASE_URL}/api/blog`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ notes }),
    });

    return await handleResponse(response);
}

// 2. Ask Reasoning Agent API Call
async function askReasoning(question) {
    const response = await fetch(`${API_BASE_URL}/api/reasoning`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
    });

    return await handleResponse(response);
}

// 3. Chat Assistant API Call
async function askChat(message, history = []) {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message, history }),
    });

    return await handleResponse(response);
}