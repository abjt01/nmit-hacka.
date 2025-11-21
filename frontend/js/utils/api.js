const API_BASE_URL = 'http://localhost:8000';

const api = {
  async generateProblems(config) {
    const response = await fetch(`${API_BASE_URL}/api/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(config),
    });
    
    if (!response.ok) {
      throw new Error('Failed to generate problems');
    }
    
    return response.json();
  },
  
  async getStatus() {
    const response = await fetch(`${API_BASE_URL}/api/status`);
    return response.json();
  },
  
  async getProblems() {
    const response = await fetch(`${API_BASE_URL}/api/problems`);
    return response.json();
  },
  
  async exportHTML(problems) {
    const response = await fetch(`${API_BASE_URL}/api/export/html`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(problems),
    });
    return response.json();
  }
};
