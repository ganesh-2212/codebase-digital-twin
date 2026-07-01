// src/api/api.js

const BASE_URL = "http://localhost:8000";

export async function askRepository(question) {
    const response = await fetch(
        `${BASE_URL}/ask`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                query: question,
            }),
        }
    );

    return response.json();
}

export async function predictImpact(component) {
    const response = await fetch(
        `${BASE_URL}/impact`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                component,
            }),
        }
    );

    return response.json();
}