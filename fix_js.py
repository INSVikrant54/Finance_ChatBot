#!/usr/bin/env python3
"""Generate fixed main.js file"""

JS_CONTENT = """// Global variables
let currentUser = null;
let authToken = null;
let spendingChart = null;
let trendChart = null;

// API base URL
const API_BASE = '';

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in
    authToken = localStorage.getItem('authToken');
    const userData = localStorage.getItem('userData');
    
    if (authToken && userData) {
        currentUser = JSON.parse(userData);
        showMainApp();
        loadDashboard();
    } else {
        showAuthSection();
    }
    
    // Set up event listeners
    setupEventListeners();
});

// ===================  AUTH FUNCTIONS ===================

function setupEventListeners() {
    // Auth
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    document.getElementById('registerForm').addEventListener('submit', handleRegister);
    
    // Logout
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('submit', handleLogout);
    }
    
    // Forms (only if they exist)
    const transactionForm = document.getElementById('transactionForm');
    if (transactionForm) {
        transactionForm.addEventListener('submit', handleAddTransaction);
    }
    
    const budgetForm = document.getElementById('budgetForm');
    if (budgetForm) {
        budgetForm.addEventListener('submit', handleAddBudget);
    }
    
    const goalForm = document.getElementById('goalForm');
    if (goalForm) {
        goalForm.addEventListener('submit', handleAddGoal);
    }
    
    const chatForm = document.getElementById('chatForm');
    if (chatForm) {
        chatForm.addEventListener('submit', handleChatSubmit);
    }
}

function showAuthSection() {
    document.getElementById('authSection').style.display = 'block';
    document.getElementById('mainApp').classList.add('d-none');
}

function showMainApp() {
    document.getElementById('authSection').style.display = 'none';
    document.getElementById('mainApp').classList.remove('d-none');
    
    // Update username display
    if (currentUser) {
        const usernameDisplay = document.getElementById('usernameDisplay');
        if (usernameDisplay) {
            usernameDisplay.textContent = currentUser.username;
        }
    }
    
    // Set today's date as default for transaction date
    const transactionDate = document.getElementById('transactionDate');
    if (transactionDate) {
        const today = new Date().toISOString().split('T')[0];
        transactionDate.value = today;
    }
}

async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    
    if (!username || !password) {
        alert('Please enter both username and password');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            authToken = data.token;
            currentUser = data.user;
            localStorage.setItem('authToken', authToken);
            localStorage.setItem('userData', JSON.stringify(currentUser));
            
            // Show main app
            showMainApp();
            loadDashboard();
        } else {
            alert('Login failed: ' + (data.error || 'Invalid credentials'));
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Login error. Please make sure the server is running.');
    }
}

async function handleRegister(e) {
    e.preventDefault();
    
    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    
    if (!username || !email || !password) {
        alert('Please fill in all fields');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            authToken = data.token;
            currentUser = data.user;
            localStorage.setItem('authToken', authToken);
            localStorage.setItem('userData', JSON.stringify(currentUser));
            
            // Show main app
            showMainApp();
            loadDashboard();
        } else {
            alert('Registration failed: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Registration error:', error);
        alert('Registration error. Please try again.');
    }
}

function handleLogout(e) {
    if (e) e.preventDefault();
    
    fetch(`${API_BASE}/api/logout`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${authToken}` }
    }).finally(() => {
        localStorage.removeItem('authToken');
        localStorage.removeItem('userData');
        authToken = null;
        currentUser = null;
        showAuthSection();
    });
}

// =================== DASHBOARD FUNCTIONS ===================

async function loadDashboard() {
    try {
        await loadSummary();
        await loadTransactions();
        await loadBudgets();
        await loadGoals();
        await loadCharts();
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

async function loadSummary() {
    try {
        const response = await fetch(`${API_BASE}/api/dashboard`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('totalBalance').textContent = `₹${data.data.balance.toFixed(2)}`;
            document.getElementById('monthIncome').textContent = `₹${data.data.month_income.toFixed(2)}`;
            document.getElementById('monthExpenses').textContent = `₹${data.data.month_expenses.toFixed(2)}`;
            document.getElementById('goalsCount').textContent = data.data.goals_count;
        }
    } catch (error) {
        console.error('Error loading summary:', error);
    }
}

async function loadTransactions() {
    try {
        const response = await fetch(`${API_BASE}/api/transactions`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();
        
        if (data.success) {
            const tbody = document.getElementById('transactionsTable');
            tbody.innerHTML = '';
            
            if (data.transactions.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">No transactions yet. Add your first transaction!</td></tr>';
                return;
            }
            
            data.transactions.forEach(transaction => {
                const row = document.createElement('tr');
                const typeClass = transaction.type === 'income' ? 'text-success' : 'text-danger';
                const typeIcon = transaction.type === 'income' ? '↓' : '↑';
                
                row.innerHTML = `
                    <td>${new Date(transaction.date).toLocaleDateString()}</td>
                    <td>${transaction.description}</td>
                    <td><span class="badge bg-primary">${transaction.category}</span></td>
                    <td class="${typeClass}">₹${transaction.amount.toFixed(2)}</td>
                    <td><span class="badge ${transaction.type === 'income' ? 'bg-success' : 'bg-danger'}">${typeIcon} ${transaction.type}</span></td>
                    <td><button class="btn btn-sm btn-danger" onclick="deleteTransaction(${transaction.id})"><i class="bi bi-trash"></i></button></td>
                `;
                tbody.appendChild(row);
            });
        }
    } catch (error) {
        console.error('Error loading transactions:', error);
    }
}

async function loadBudgets() {
    try {
        const response = await fetch(`${API_BASE}/api/budgets`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();
        
        if (data.success) {
            const container = document.getElementById('budgetsList');
            container.innerHTML = '';
            
            if (data.budgets.length === 0) {
                container.innerHTML = '<p class="text-muted">No budgets set. Create one to track your spending!</p>';
                return;
            }
            
            data.budgets.forEach(budget => {
                const percentage = (budget.spent / budget.amount) * 100;
                const progressClass = percentage > 90 ? 'bg-danger' : percentage > 70 ? 'bg-warning' : 'bg-success';
                
                const budgetCard = document.createElement('div');
                budgetCard.className = 'mb-3';
                budgetCard.innerHTML = `
                    <div class="d-flex justify-content-between align-items-center mb-1">
                        <strong>${budget.category}</strong>
                        <span>₹${budget.spent.toFixed(2)} / ₹${budget.amount.toFixed(2)}</span>
                    </div>
                    <div class="progress">
                        <div class="progress-bar ${progressClass}" role="progressbar" style="width: ${Math.min(percentage, 100)}%" 
                             aria-valuenow="${percentage}" aria-valuemin="0" aria-valuemax="100"></div>
                    </div>
                    <small class="text-muted">${budget.period}</small>
                `;
                container.appendChild(budgetCard);
            });
        }
    } catch (error) {
        console.error('Error loading budgets:', error);
    }
}

async function loadGoals() {
    try {
        const response = await fetch(`${API_BASE}/api/savings-goals`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();
        
        if (data.success) {
            const container = document.getElementById('goalsList');
            container.innerHTML = '';
            
            if (data.goals.length === 0) {
                container.innerHTML = '<p class="text-muted">No savings goals yet. Set a goal to start saving!</p>';
                return;
            }
            
            data.goals.forEach(goal => {
                const percentage = (goal.current_amount / goal.target_amount) * 100;
                
                const goalCard = document.createElement('div');
                goalCard.className = 'mb-3';
                goalCard.innerHTML = `
                    <div class="d-flex justify-content-between align-items-center mb-1">
                        <strong>${goal.name}</strong>
                        <span>${percentage.toFixed(0)}%</span>
                    </div>
                    <div class="progress mb-1">
                        <div class="progress-bar bg-info" role="progressbar" style="width: ${Math.min(percentage, 100)}%" 
                             aria-valuenow="${percentage}" aria-valuemin="0" aria-valuemax="100"></div>
                    </div>
                    <small class="text-muted">₹${goal.current_amount.toFixed(2)} / ₹${goal.target_amount.toFixed(2)}</small>
                `;
                container.appendChild(goalCard);
            });
        }
    } catch (error) {
        console.error('Error loading goals:', error);
    }
}

async function loadCharts() {
    try {
        const response = await fetch(`${API_BASE}/api/analytics/category-spending`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();
        
        if (data.success && data.data.length > 0) {
            const categories = data.data.map(item => item.category);
            const amounts = data.data.map(item => item.amount);
            
            // Spending Doughnut Chart
            const ctx1 = document.getElementById('spendingDoughnutChart');
            if (ctx1) {
                if (spendingChart) {
                    spendingChart.destroy();
                }
                spendingChart = new Chart(ctx1, {
                    type: 'doughnut',
                    data: {
                        labels: categories,
                        datasets: [{
                            data: amounts,
                            backgroundColor: [
                                '#667eea', '#764ba2', '#f093fb', '#f5576c',
                                '#4facfe', '#00f2fe', '#43e97b', '#38f9d7',
                                '#fa709a', '#fee140'
                            ]
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: true,
                        plugins: {
                            legend: {
                                position: 'bottom'
                            }
                        }
                    }
                });
            }
        }
        
        // Load trend data
        const trendResponse = await fetch(`${API_BASE}/api/analytics/spending-trends`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const trendData = await trendResponse.json();
        
        if (trendData.success && trendData.data.length > 0) {
            const months = trendData.data.map(item => item.month);
            const expenses = trendData.data.map(item => item.expenses);
            const income = trendData.data.map(item => item.income);
            
            // Trend Line Chart
            const ctx2 = document.getElementById('trendLineChart');
            if (ctx2) {
                if (trendChart) {
                    trendChart.destroy();
                }
                trendChart = new Chart(ctx2, {
                    type: 'line',
                    data: {
                        labels: months,
                        datasets: [{
                            label: 'Expenses',
                            data: expenses,
                            borderColor: '#f5576c',
                            backgroundColor: 'rgba(245, 87, 108, 0.1)',
                            tension: 0.4
                        }, {
                            label: 'Income',
                            data: income,
                            borderColor: '#43e97b',
                            backgroundColor: 'rgba(67, 233, 123, 0.1)',
                            tension: 0.4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: true,
                        plugins: {
                            legend: {
                                position: 'top'
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            }
        }
    } catch (error) {
        console.error('Error loading charts:', error);
    }
}

// =================== TRANSACTION FUNCTIONS ===================

async function handleAddTransaction(e) {
    e.preventDefault();
    
    const description = document.getElementById('transactionDescription').value;
    const amount = parseFloat(document.getElementById('transactionAmount').value);
    const type = document.getElementById('transactionType').value;
    const category = document.getElementById('transactionCategory').value;
    const date = document.getElementById('transactionDate').value;
    
    try {
        const response = await fetch(`${API_BASE}/api/transactions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ description, amount, type, category, date })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Close modal
            bootstrap.Modal.getInstance(document.getElementById('transactionModal')).hide();
            
            // Reset form
            e.target.reset();
            
            // Reload dashboard
            loadDashboard();
            
            alert('Transaction added successfully!');
        } else {
            alert('Error adding transaction: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error adding transaction:', error);
        alert('Error adding transaction. Please try again.');
    }
}

async function deleteTransaction(id) {
    if (!confirm('Are you sure you want to delete this transaction?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/transactions/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();
        
        if (data.success) {
            loadDashboard();
            alert('Transaction deleted!');
        } else {
            alert('Error deleting transaction');
        }
    } catch (error) {
        console.error('Error deleting transaction:', error);
        alert('Error deleting transaction');
    }
}

// =================== BUDGET FUNCTIONS ===================

async function handleAddBudget(e) {
    e.preventDefault();
    
    const category = document.getElementById('budgetCategory').value;
    const amount = parseFloat(document.getElementById('budgetAmount').value);
    const period = document.getElementById('budgetPeriod').value;
    
    try {
        const response = await fetch(`${API_BASE}/api/budgets`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ category, amount, period })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Close modal
            bootstrap.Modal.getInstance(document.getElementById('budgetModal')).hide();
            
            // Reset form
            e.target.reset();
            
            // Reload dashboard
            loadDashboard();
            
            alert('Budget created successfully!');
        } else {
            alert('Error creating budget: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error creating budget:', error);
        alert('Error creating budget. Please try again.');
    }
}

// =================== GOAL FUNCTIONS ===================

async function handleAddGoal(e) {
    e.preventDefault();
    
    const name = document.getElementById('goalName').value;
    const target_amount = parseFloat(document.getElementById('goalTarget').value);
    const current_amount = parseFloat(document.getElementById('goalCurrent').value) || 0;
    const deadline = document.getElementById('goalDeadline').value;
    
    try {
        const response = await fetch(`${API_BASE}/api/savings-goals`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ name, target_amount, current_amount, deadline })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Close modal
            bootstrap.Modal.getInstance(document.getElementById('goalModal')).hide();
            
            // Reset form
            e.target.reset();
            
            // Reload dashboard
            loadDashboard();
            
            alert('Savings goal added successfully!');
        } else {
            alert('Error adding goal: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error adding goal:', error);
        alert('Error adding goal. Please try again.');
    }
}

// =================== CHAT FUNCTIONS ===================

async function handleChatSubmit(e) {
    e.preventDefault();
    
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addChatMessage(message, 'user');
    
    // Clear input
    input.value = '';
    
    try {
        const response = await fetch(`${API_BASE}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ message })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Add AI response to chat
            addChatMessage(data.response, 'ai');
        } else {
            addChatMessage('Sorry, I encountered an error. Please try again.', 'ai');
        }
    } catch (error) {
        console.error('Error sending chat message:', error);
        addChatMessage('Sorry, I could not connect to the server. Please try again.', 'ai');
    }
}

function addChatMessage(message, type) {
    const messagesContainer = document.getElementById('chatMessages');
    
    // Remove empty state if present
    if (messagesContainer.querySelector('.text-center')) {
        messagesContainer.innerHTML = '';
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `p-3 mb-2 rounded ${type === 'user' ? 'bg-primary text-white ms-5' : 'bg-light me-5'}`;
    messageDiv.textContent = message;
    
    messagesContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Utility function to format currency
function formatCurrency(amount) {
    return `₹${amount.toFixed(2)}`;
}

console.log('FinanceAI app loaded successfully!');
"""

if __name__ == '__main__':
    with open('static/js/main.js', 'w', encoding='utf-8') as f:
        f.write(JS_CONTENT)
    print("✅ JavaScript file generated successfully!")
