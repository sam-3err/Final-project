const API_URL = "http://127.0.0.1:8000/api/";

function getToken() {
  return localStorage.getItem("token");
}

function setToken(token) {
  if (token) localStorage.setItem("token", token);
  else localStorage.removeItem("token");
}

function getAuthHeaders() {
  const token = localStorage.getItem("token");
  return {
    "Content-Type": "application/json",
    ...(token && {"Authorization": `Bearer ${token}`})
  };
}


function getUserRole() {
  return localStorage.getItem('userRole') || 'USER';
}

function getUserId() {
  return localStorage.getItem('userId') || 1;
}

async function login(email, password) {
  console.log("🔐 Logging in...", email); 
  
  try {
    const response = await fetch(`${API_URL}users/login/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    
    console.log("Login response status:", response.status); 
    
    const data = await response.json();
    console.log("Login response data:", data); 
    
    if (data.access) {
      setToken(data.access);
      localStorage.setItem('userRole', data.user.role);
      localStorage.setItem('userId', data.user.id);
      
      console.log("✅ Login success, redirecting to:", data.user.role); 
      const rolePages = {
        'USER': 'dashboard.html',
        'MANAGER': 'manager.html', 
        'ADMIN': 'admin.html'
      };
      window.location.href = rolePages[data.user.role] || 'dashboard.html';
    } else {
      alert("❌ Invalid credentials");
    }
  } catch (error) {
    console.error("Login error:", error);
    alert("❌ Login failed");
  }
}

async function register(name, email, password, role) {
  console.log("📝 Registering...", {name, email, role}); 
  try {
    const response = await fetch(`${API_URL}users/register/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password, role })
    });
    
    const data = await response.json();
    console.log("Register response:", data); // DEBUG
    
    if (data.id) {
      alert("✅ Registration successful! Please login.");
     
      document.getElementById('mode').value = 'login';
      document.getElementById('authForm').reset();
      document.getElementById('registerFields').classList.add('hidden');
      document.getElementById('formTitle').textContent = 'Login to Task Manager';
      document.getElementById('submitBtn').textContent = 'Login';
      document.getElementById('toggleText').textContent = 'Need an account? Register';
    } else {
      alert("❌ Registration failed: " + JSON.stringify(data));
    }
  } catch (error) {
    console.error("Register error:", error);
    alert("❌ Registration failed");
  }
}

async function loadUserTasks() {
  const userId = getUserId();
  try {
    const response = await fetch(`${API_URL}tasks/user/${userId}/`, {
      headers: getAuthHeaders()
    });
    const data = await response.json();
    window.displayUserTasks?.(data.data || []);
window.updateUserStats?.(data.data || []);

  } catch (error) {
    console.error("Failed to load tasks");
  }
}
function displayUserTasks(tasks) {
  const tasksList = document.getElementById('tasksList');

  if (!tasks || tasks.length === 0) {
    tasksList.innerHTML = 'No tasks assigned yet. 🚀';
    return;
  }

  tasksList.innerHTML = tasks.map(t => `
    <div class="task-item" style="border-left: 4px solid ${
      t.status === 'COMPLETED' ? 'green' :
      t.status === 'PENDING' ? 'orange' : 'blue'
    }; padding: 10px; margin: 5px 0; background: #f9f9f9; border-radius: 6px;">
      <strong>${t.title}</strong>
      <br>${t.description.slice(0, 60)}...
      <br><small>Due: ${t.due_date}</small>
      <br><span style="color: ${
        t.status === 'COMPLETED' ? 'green' :
        t.status === 'PENDING' ? 'orange' : 'gray'
      }">Status: ${t.status}</span>

      <!-- Toggle status button -->
      <div style="margin-top: 6px;">
        <button 
          onclick="toggleTaskStatus(${t.id}, '${t.status}')" 
          class="btn btn-sm" 
          style="background: ${
            t.status === 'COMPLETED' ? '#6c757d' : '#28a745'
          }; color: white; padding: 4px 8px; font-size: 12px;">
          ${t.status === 'COMPLETED' ? 'Mark Pending' : 'Mark Completed'}
        </button>
      </div>
    </div>
  `).join('');
}
async function toggleTaskStatus(taskId, currentStatus) {
  const newStatus = currentStatus === 'COMPLETED' ? 'PENDING' : 'COMPLETED';

  try {
    const response = await fetch(`${API_URL}tasks/update/${taskId}/`, {
      method: 'PATCH',
      headers: getAuthHeaders(),
      body: JSON.stringify({ status: newStatus })
    });

    if (response.ok) {
      // Re‑load tasks after change
      await loadUserTasks();
    } else {
      const error = await response.json();
      console.error("Failed to update task:", error);
      alert("Failed to update task");
    }
  } catch (err) {
    console.error("Network error:", err);
    alert("Network error");
  }
}


function updateUserStats(tasks) {
  const total = tasks.length;
  const completed = tasks.filter(t => t.status === 'COMPLETED').length;
  const pending = total - completed;

  document.getElementById('totalTasks').textContent = total;
  document.getElementById('completedTasks').textContent = completed;
  document.getElementById('pendingTasks').textContent = pending;
}


function toggleAuthMode() {
  const mode = document.getElementById('mode');
  const registerFields = document.getElementById('registerFields');
  const formTitle = document.getElementById('formTitle');
  const submitBtn = document.getElementById('submitBtn');
  const toggleText = document.getElementById('toggleText');
  
  if (mode.value === 'login') {
    mode.value = 'register';
    registerFields.classList.remove('hidden');
    formTitle.textContent = 'Register for Task Manager';
    submitBtn.textContent = 'Register';
    toggleText.textContent = 'Already have account? Login';
  } else {
    mode.value = 'login';
    registerFields.classList.add('hidden');
    formTitle.textContent = 'Login to Task Manager';
    submitBtn.textContent = 'Login';
    toggleText.textContent = 'Need an account? Register';
  }
}

// ========== PAGE INITIALIZATION ==========
document.addEventListener('DOMContentLoaded', function() {
  console.log("Page loaded, token:", getToken() ? 'Yes' : 'No'); 
  
  // If on dashboard pages and no token, redirect to login
  const isDashboardPage = ['dashboard.html', 'manager.html', 'admin.html'].some(p => 
    window.location.pathname.includes(p)
  );
  
  if (isDashboardPage && !getToken()) {
    window.location.href = 'index.html';
    return;
  }
  
  
  const authForm = document.getElementById('authForm');
  if (authForm) {
    console.log("✅ Found auth form, attaching handler"); 
    
    authForm.addEventListener('submit', function(e) {
      e.preventDefault(); 
      console.log("✅ Form submitted!"); 
      
      const mode = document.getElementById('mode').value;
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value;
      
      if (mode === 'login') {
        login(email, password);
      } else {
        const name = document.getElementById('name').value.trim();
        const role = document.getElementById('role').value;
        if (!name || !email || !password) {
          alert('Please fill all fields');
          return;
        }
        register(name, email, password, role);
      }
    });
  }
});
