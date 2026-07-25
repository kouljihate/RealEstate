const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

const App = {
  currentPage: 'home',

  async init() {
    this.render(await this.homePage());
    this.bindNav();
    await this.restoreSession();
  },

  async restoreSession() {
    if (api.token) {
      try {
        const user = await api.getMe();
        this.setAuthUI(user);
      } catch {
        api.setToken(null);
        this.setAuthUI(null);
      }
    }
  },

  setAuthUI(user) {
    const loginLink = $('#loginLink');
    const registerLink = $('#registerLink');
    const dashboardLink = $('#dashboardLink');
    const logoutLink = $('#logoutLink');

    if (user) {
      loginLink.style.display = 'none';
      registerLink.style.display = 'none';
      dashboardLink.style.display = 'inline';
      logoutLink.style.display = 'inline';
      window.currentUser = user;
    } else {
      loginLink.style.display = 'inline';
      registerLink.style.display = 'inline';
      dashboardLink.style.display = 'none';
      logoutLink.style.display = 'none';
      window.currentUser = null;
    }
  },

  bindNav() {
    document.addEventListener('click', (e) => {
      const link = e.target.closest('a');
      if (!link || link.getAttribute('href').startsWith('http')) return;
      e.preventDefault();
      const href = link.getAttribute('href');
      if (href === '#') return;
      this.navigate(href);
    });

    $('#hamburger')?.addEventListener('click', () => {
      $('#navLinks').classList.toggle('open');
    });
  },

  async navigate(path) {
    const route = path.replace(/^\//, '') || 'home';
    this.currentPage = route;
    window.history.pushState({}, '', path);

    switch (route) {
      case 'home':
        this.render(await this.homePage());
        break;
      case 'properties':
        this.render(await this.propertiesPage());
        break;
      case 'login':
        this.render(this.loginPage());
        break;
      case 'register':
        this.render(this.registerPage());
        break;
      case 'dashboard':
        this.render(await this.dashboardPage());
        break;
      default:
        if (route.startsWith('properties/')) {
          const id = route.split('/')[1];
          this.render(await this.propertyDetailPage(id));
        } else {
          this.render('<h1>404 - Page Not Found</h1>');
        }
    }
  },

  render(html) {
    $('#app').innerHTML = html;
    this.bindPageEvents();
  },

  bindPageEvents() {
    // Login
    $('#loginForm')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      try {
        const data = await api.login(
          $('#loginEmail').value,
          $('#loginPassword').value
        );
        api.setToken(data.access_token);
        const user = await api.getMe();
        this.setAuthUI(user);
        this.navigate('/');
      } catch (err) {
        $('#loginError').textContent = err.message;
      }
    });

    // Register
    $('#registerForm')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      try {
        await api.register({
          email: $('#regEmail').value,
          username: $('#regUsername').value,
          password: $('#regPassword').value,
          full_name: $('#regFullName').value,
          phone: $('#regPhone').value,
        });
        this.navigate('/login');
      } catch (err) {
        $('#registerError').textContent = err.message;
      }
    });

    // Logout
    $('#logoutLink')?.addEventListener('click', (e) => {
      e.preventDefault();
      api.setToken(null);
      this.setAuthUI(null);
      this.navigate('/');
    });
  },

  // --- Pages ---

  async homePage() {
    let featured = [];
    try {
      const res = await api.getProperties({ size: 6 });
      featured = res.items || [];
    } catch {}

    return `
      <section class="hero">
        <div class="hero-content">
          <h1>Find Your Perfect Farm Land</h1>
          <p>Browse thousands of farm properties across the country</p>
          <a href="/properties" class="btn btn-primary">Browse Properties</a>
        </div>
      </section>
      <section class="section">
        <h2>Featured Properties</h2>
        <div class="property-grid">
          ${featured.map(p => `
            <div class="property-card">
              <div class="card-img">${p.photos?.length ? '<img src="/api/v1/media/'+p.photos[0]+'" alt=""/>' : '<div class="card-img-placeholder">📷</div>'}</div>
              <div class="card-body">
                <h3>${p.title}</h3>
                <p class="price">$${p.price?.toLocaleString()}</p>
                <p>${p.area_hectares} ha • ${p.location?.city}, ${p.location?.state}</p>
                <a href="/properties/${p.id}" class="btn btn-sm">View Details</a>
              </div>
            </div>
          `).join('')}
          ${featured.length === 0 ? '<p class="text-muted">No properties listed yet.</p>' : ''}
        </div>
      </section>
    `;
  },

  async propertiesPage() {
    const res = await api.getProperties({ size: 20 });
    const items = res?.items || [];

    return `
      <section class="section">
        <h1>Properties</h1>
        <div class="property-grid">
          ${items.map(p => `
            <div class="property-card">
              <div class="card-img">${p.photos?.length ? '<img src="/api/v1/media/'+p.photos[0]+'" alt=""/>' : '<div class="card-img-placeholder">📷</div>'}</div>
              <div class="card-body">
                <h3>${p.title}</h3>
                <p class="price">$${p.price?.toLocaleString()}</p>
                <p>${p.area_hectares} ha • ${p.location?.city}, ${p.location?.state}</p>
                <span class="badge badge-${p.status}">${p.status}</span>
                <a href="/properties/${p.id}" class="btn btn-sm">View Details</a>
              </div>
            </div>
          `).join('')}
          ${items.length === 0 ? '<p class="text-muted">No properties found.</p>' : ''}
        </div>
      </section>
    `;
  },

  async propertyDetailPage(id) {
    try {
      const p = await api.getProperty(id);
      return `
        <section class="section detail">
          <a href="/properties" class="btn btn-sm">&larr; Back</a>
          <h1>${p.title}</h1>
          <div class="detail-grid">
            <div class="detail-images">
              ${p.photos?.length ? p.photos.map(ph => `<img src="/api/v1/media/${ph}" alt="" class="detail-img"/>`).join('') : '<div class="card-img-placeholder" style="height:300px">📷 No photos</div>'}
            </div>
            <div class="detail-info">
              <h2 class="price">$${p.price?.toLocaleString()}</h2>
              <p><strong>Type:</strong> ${p.property_type}</p>
              <p><strong>Area:</strong> ${p.area_hectares} hectares</p>
              <p><strong>Location:</strong> ${p.location?.address}, ${p.location?.city}, ${p.location?.state}, ${p.location?.country}</p>
              <p><strong>Status:</strong> <span class="badge badge-${p.status}">${p.status}</span></p>
              <hr/>
              <p>${p.description}</p>
              ${p.features?.length ? `<hr/><h3>Features</h3><ul>${p.features.map(f => `<li>${f}</li>`).join('')}</ul>` : ''}
              <hr/>
              <p><strong>Water Access:</strong> ${p.water_access ? '✅' : '❌'}</p>
              <p><strong>Road Access:</strong> ${p.road_access ? '✅' : '❌'}</p>
              <p><strong>Electricity:</strong> ${p.electricity ? '✅' : '❌'}</p>
            </div>
          </div>
        </section>
      `;
    } catch (err) {
      return `<section class="section"><h1>Property not found</h1><p>${err.message}</p></section>`;
    }
  },

  loginPage() {
    return `
      <section class="section auth-page">
        <div class="auth-card">
          <h1>Login</h1>
          <form id="loginForm">
            <p id="loginError" class="error-msg"></p>
            <label>Email</label>
            <input type="email" id="loginEmail" required placeholder="your@email.com"/>
            <label>Password</label>
            <input type="password" id="loginPassword" required placeholder="••••••••"/>
            <button type="submit" class="btn btn-primary btn-block">Sign In</button>
          </form>
          <p class="text-center">Don't have an account? <a href="/register">Register</a></p>
        </div>
      </section>
    `;
  },

  registerPage() {
    return `
      <section class="section auth-page">
        <div class="auth-card">
          <h1>Create Account</h1>
          <form id="registerForm">
            <p id="registerError" class="error-msg"></p>
            <label>Full Name</label>
            <input type="text" id="regFullName" required placeholder="John Farmer"/>
            <label>Email</label>
            <input type="email" id="regEmail" required placeholder="farmer@example.com"/>
            <label>Username</label>
            <input type="text" id="regUsername" required placeholder="farmer123"/>
            <label>Phone</label>
            <input type="tel" id="regPhone" placeholder="+212600000000"/>
            <label>Password</label>
            <input type="password" id="regPassword" required placeholder="Min 8 characters"/>
            <button type="submit" class="btn btn-primary btn-block">Register</button>
          </form>
          <p class="text-center">Already registered? <a href="/login">Login</a></p>
        </div>
      </section>
    `;
  },

  async dashboardPage() {
    if (!window.currentUser) {
      return '<section class="section"><h1>Please log in</h1></section>';
    }
    return `
      <section class="section">
        <h1>Dashboard</h1>
        <div class="dashboard-card">
          <p><strong>Welcome, ${window.currentUser.full_name}!</strong></p>
          <p>Role: ${window.currentUser.role}</p>
          <p>Email: ${window.currentUser.email}</p>
          ${window.currentUser.role === 'admin' ? '<p class="badge badge-admin">Admin Access</p>' : ''}
        </div>
      </section>
    `;
  },
};

document.addEventListener('DOMContentLoaded', () => App.init());
window.addEventListener('popstate', () => App.navigate(window.location.pathname));
