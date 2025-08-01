const API_BASE = `${process.env.REACT_APP_BACKEND_URL}/api`;

class PortfolioAPI {
  async request(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  // Profile endpoints
  async getProfile() {
    return this.request('/profile');
  }

  async updateProfile(profileData) {
    return this.request('/profile', {
      method: 'PUT',
      body: JSON.stringify(profileData),
    });
  }

  // Skills endpoints
  async getSkills() {
    return this.request('/skills');
  }

  async updateSkills(skillsData) {
    return this.request('/skills', {
      method: 'PUT',
      body: JSON.stringify(skillsData),
    });
  }

  // Projects endpoints
  async getProjects(featured = null) {
    const query = featured !== null ? `?featured=${featured}` : '';
    return this.request(`/projects${query}`);
  }

  async getProject(projectId) {
    return this.request(`/projects/${projectId}`);
  }

  async createProject(projectData) {
    return this.request('/projects', {
      method: 'POST',
      body: JSON.stringify(projectData),
    });
  }

  async updateProject(projectId, projectData) {
    return this.request(`/projects/${projectId}`, {
      method: 'PUT',
      body: JSON.stringify(projectData),
    });
  }

  async deleteProject(projectId) {
    return this.request(`/projects/${projectId}`, {
      method: 'DELETE',
    });
  }

  // Certificates endpoints
  async getCertificates() {
    return this.request('/certificates');
  }

  async createCertificate(certificateData) {
    return this.request('/certificates', {
      method: 'POST',
      body: JSON.stringify(certificateData),
    });
  }

  async updateCertificate(certificateId, certificateData) {
    return this.request(`/certificates/${certificateId}`, {
      method: 'PUT',
      body: JSON.stringify(certificateData),
    });
  }

  async deleteCertificate(certificateId) {
    return this.request(`/certificates/${certificateId}`, {
      method: 'DELETE',
    });
  }

  // Education endpoints
  async getEducation() {
    return this.request('/education');
  }

  async createEducation(educationData) {
    return this.request('/education', {
      method: 'POST',
      body: JSON.stringify(educationData),
    });
  }

  async updateEducation(educationId, educationData) {
    return this.request(`/education/${educationId}`, {
      method: 'PUT',
      body: JSON.stringify(educationData),
    });
  }

  async deleteEducation(educationId) {
    return this.request(`/education/${educationId}`, {
      method: 'DELETE',
    });
  }
}

export const portfolioAPI = new PortfolioAPI();