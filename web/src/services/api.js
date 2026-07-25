const API_BASE = '/api/v1';

class ApiService {
  constructor() {
    this.token = localStorage.getItem('access_token') || null;
  }

  setToken(token) {
    this.token = token;
    if (token) localStorage.setItem('access_token', token);
    else localStorage.removeItem('access_token');
  }

  getHeaders() {
    const headers = { 'Content-Type': 'application/json' };
    if (this.token) headers['Authorization'] = `Bearer ${this.token}`;
    return headers;
  }

  async request(method, path, body = null, isFormData = false) {
    const opts = { method };
    if (!isFormData) {
      opts.headers = this.getHeaders();
      if (body) opts.body = JSON.stringify(body);
    } else {
      opts.headers = {};
      if (this.token) opts.headers['Authorization'] = `Bearer ${this.token}`;
      opts.body = body;
    }

    const res = await fetch(`${API_BASE}${path}`, opts);
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || 'Request failed');
    }
    if (res.status === 204) return null;
    return res.json();
  }

  // Auth
  login(email, password) {
    return this.request('POST', '/auth/login', { email, password });
  }
  register(data) {
    return this.request('POST', '/auth/register', data);
  }
  getMe() {
    return this.request('GET', '/auth/me');
  }

  // Properties
  getProperties(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request('GET', `/properties?${qs}`);
  }
  getProperty(id) {
    return this.request('GET', `/properties/${id}`);
  }
  createProperty(data) {
    return this.request('POST', '/properties/', data);
  }
  updateProperty(id, data) {
    return this.request('PUT', `/properties/${id}`, data);
  }
  deleteProperty(id) {
    return this.request('DELETE', `/properties/${id}`);
  }

  // Media
  uploadMedia(file, propertyId = null) {
    const fd = new FormData();
    fd.append('file', file);
    if (propertyId) fd.append('property_id', propertyId);
    return this.request('POST', '/media/upload', fd, true);
  }
}

const api = new ApiService();
window.api = api;
