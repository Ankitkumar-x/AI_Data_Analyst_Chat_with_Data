const API_BASE_URL = "http://127.0.0.1:8000";


export async function uploadDataset(file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/api/upload`,
    {
      method: "POST",
      body: formData,
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to upload dataset."
    );
  }

  return data;
}

export async function sendChatMessage(
    message,
    conversationHistory = null
) {
  const response = await fetch(
    `${API_BASE_URL}/api/chat`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        message: message,
        conversation_history: conversationHistory,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to get AI response."
    );
  }

  return data;
}

export async function getDashboardSummary() {
  const response = await fetch(
    `${API_BASE_URL}/api/dashboard`
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to load dashboard data."
    );
  }

  return data;
}

export async function getDashboardVisualizations() {
  const response = await fetch(
    `${API_BASE_URL}/api/dashboard/visualizations`
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to load dashboard visualizations."
    );
  }

  return data;
}