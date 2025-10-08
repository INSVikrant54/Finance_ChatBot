// Global variables
let currentUser = null;
let authToken = null;
let spendingChart = null;
let trendChart = null;
let notifications = [];

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
        logoutBtn.addEventListener('click', handleLogout);
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
        
        // Generate notifications after data is loaded
        setTimeout(() => {
            checkAndGenerateNotifications();
        }, 1000);
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
                const typeClass = transaction.transaction_type === 'income' ? 'text-success' : 'text-danger';
                const typeIcon = transaction.transaction_type === 'income' ? '↓' : '↑';
                
                row.innerHTML = `
                    <td>${new Date(transaction.date).toLocaleDateString()}</td>
                    <td>${transaction.description}</td>
                    <td><span class="badge bg-primary">${transaction.category}</span></td>
                    <td class="${typeClass}">₹${transaction.amount.toFixed(2)}</td>
                    <td><span class="badge ${transaction.transaction_type === 'income' ? 'bg-success' : 'bg-danger'}">${typeIcon} ${transaction.transaction_type}</span></td>
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
            
            // Spending Doughnut Chart - Modern Style
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
                                '#667eea', // Purple
                                '#f093fb', // Pink
                                '#4facfe', // Blue
                                '#43e97b', // Green
                                '#fa709a', // Rose
                                '#feca57', // Yellow
                                '#ff6348', // Red-Orange
                                '#1dd1a1', // Teal
                                '#5f27cd', // Deep Purple
                                '#00d2d3'  // Cyan
                            ],
                            borderWidth: 3,
                            borderColor: '#ffffff',
                            hoverBorderWidth: 5,
                            hoverBorderColor: '#ffffff',
                            hoverOffset: 15
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: true,
                        cutout: '65%', // Makes it a modern donut with bigger hole
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: {
                                    padding: 15,
                                    font: {
                                        size: 13,
                                        family: "'Segoe UI', sans-serif",
                                        weight: '500'
                                    },
                                    color: '#2c3e50',
                                    usePointStyle: true,
                                    pointStyle: 'circle'
                                }
                            },
                            tooltip: {
                                backgroundColor: 'rgba(44, 62, 80, 0.95)',
                                titleFont: {
                                    size: 14,
                                    weight: 'bold'
                                },
                                bodyFont: {
                                    size: 13
                                },
                                padding: 12,
                                borderColor: 'rgba(255, 255, 255, 0.3)',
                                borderWidth: 1,
                                displayColors: true,
                                callbacks: {
                                    label: function(context) {
                                        const label = context.label || '';
                                        const value = context.parsed || 0;
                                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                        const percentage = ((value / total) * 100).toFixed(1);
                                        return ` ${label}: ₹${value.toFixed(2)} (${percentage}%)`;
                                    }
                                }
                            }
                        },
                        animation: {
                            animateRotate: true,
                            animateScale: true,
                            duration: 1500,
                            easing: 'easeInOutQuart'
                        },
                        layout: {
                            padding: 10
                        }
                    }
                });
            }
        }
        
        // Load trend data
        const trendResponse = await fetch(`${API_BASE}/api/analytics/trends`, {
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
                            borderWidth: 3,
                            tension: 0.4,
                            fill: true,
                            pointRadius: 5,
                            pointHoverRadius: 7,
                            pointBackgroundColor: '#f5576c',
                            pointBorderColor: '#ffffff',
                            pointBorderWidth: 2,
                            pointHoverBackgroundColor: '#ffffff',
                            pointHoverBorderColor: '#f5576c',
                            pointHoverBorderWidth: 3
                        }, {
                            label: 'Income',
                            data: income,
                            borderColor: '#43e97b',
                            backgroundColor: 'rgba(67, 233, 123, 0.1)',
                            borderWidth: 3,
                            tension: 0.4,
                            fill: true,
                            pointRadius: 5,
                            pointHoverRadius: 7,
                            pointBackgroundColor: '#43e97b',
                            pointBorderColor: '#ffffff',
                            pointBorderWidth: 2,
                            pointHoverBackgroundColor: '#ffffff',
                            pointHoverBorderColor: '#43e97b',
                            pointHoverBorderWidth: 3
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: true,
                        interaction: {
                            mode: 'index',
                            intersect: false
                        },
                        plugins: {
                            legend: {
                                position: 'top',
                                labels: {
                                    padding: 15,
                                    font: {
                                        size: 13,
                                        family: "'Segoe UI', sans-serif",
                                        weight: '500'
                                    },
                                    color: '#2c3e50',
                                    usePointStyle: true,
                                    pointStyle: 'circle'
                                }
                            },
                            tooltip: {
                                backgroundColor: 'rgba(44, 62, 80, 0.95)',
                                titleFont: {
                                    size: 14,
                                    weight: 'bold'
                                },
                                bodyFont: {
                                    size: 13
                                },
                                padding: 12,
                                borderColor: 'rgba(255, 255, 255, 0.3)',
                                borderWidth: 1,
                                displayColors: true,
                                callbacks: {
                                    label: function(context) {
                                        return ` ${context.dataset.label}: ₹${context.parsed.y.toFixed(2)}`;
                                    }
                                }
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                grid: {
                                    color: 'rgba(189, 195, 199, 0.2)',
                                    drawBorder: false
                                },
                                ticks: {
                                    font: {
                                        size: 12
                                    },
                                    color: '#7f8c8d',
                                    callback: function(value) {
                                        return '₹' + value.toLocaleString();
                                    }
                                }
                            },
                            x: {
                                grid: {
                                    display: false,
                                    drawBorder: false
                                },
                                ticks: {
                                    font: {
                                        size: 12
                                    },
                                    color: '#7f8c8d'
                                }
                            }
                        },
                        animation: {
                            duration: 1500,
                            easing: 'easeInOutQuart'
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
    const transaction_type = document.getElementById('transactionType').value;
    const category = document.getElementById('transactionCategory').value;
    const date = document.getElementById('transactionDate').value;
    
    try {
        const response = await fetch(`${API_BASE}/api/transactions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ description, amount, transaction_type, category, date })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Close modal
            bootstrap.Modal.getInstance(document.getElementById('transactionModal')).hide();
            
            // Reset form
            e.target.reset();
            
            // Add notification
            if (transaction_type === 'income') {
                addNotification('success', '💰 Income Added', `Added ₹${amount.toFixed(2)} income in ${category}`, 'bi-cash-coin');
            } else {
                addNotification('info', '📝 Expense Tracked', `Spent ₹${amount.toFixed(2)} on ${category}`, 'bi-receipt');
            }
            
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
            addNotification('info', '🗑️ Transaction Deleted', 
                'Transaction removed from your records', 'bi-trash-fill');
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
            
            // Add notification
            addNotification('success', '🎯 Budget Created', 
                `Set ₹${amount.toFixed(2)} ${period} budget for ${category}`, 'bi-piggy-bank-fill');
            
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
            
            // Add notification
            const percentage = (current_amount / target_amount) * 100;
            addNotification('success', '🎯 Goal Created', 
                `${name}: ₹${current_amount.toFixed(2)} of ₹${target_amount.toFixed(2)} (${percentage.toFixed(0)}%)`, 
                'bi-trophy-fill');
            
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
    
    // Add typing indicator
    addTypingIndicator();
    
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
        
        // Remove typing indicator
        removeTypingIndicator();
        
        if (data.success) {
            // Add AI response with typing animation
            addChatMessageWithTyping(data.response, 'ai');
        } else {
            addChatMessage('Sorry, I encountered an error. Please try again.', 'ai');
        }
    } catch (error) {
        console.error('Error sending chat message:', error);
        removeTypingIndicator();
        addChatMessage('Sorry, I could not connect to the server. Please try again.', 'ai');
    }
}

function addTypingIndicator() {
    const messagesContainer = document.getElementById('chatMessages');
    
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typingIndicator';
    typingDiv.className = 'p-3 mb-2 rounded bg-light me-5';
    typingDiv.innerHTML = '<div class="typing-dots"><span>.</span><span>.</span><span>.</span></div>';
    
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

async function addChatMessageWithTyping(message, type) {
    const messagesContainer = document.getElementById('chatMessages');
    
    // Remove empty state if present
    if (messagesContainer.querySelector('.text-center')) {
        messagesContainer.innerHTML = '';
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `p-3 mb-2 rounded ${type === 'user' ? 'bg-primary text-white ms-5' : 'bg-light me-5'}`;
    messageDiv.textContent = '';
    
    messagesContainer.appendChild(messageDiv);
    
    // Typing animation - character by character
    let index = 0;
    const typingSpeed = 20; // milliseconds per character (slower = more realistic)
    
    function typeNextCharacter() {
        if (index < message.length) {
            messageDiv.textContent += message.charAt(index);
            index++;
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            setTimeout(typeNextCharacter, typingSpeed);
        }
    }
    
    // Small delay before starting to type
    setTimeout(typeNextCharacter, 300);
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

// =================== SMART FINANCE FUNCTIONS ===================

let smartFinanceOpen = false;
let emiCalculatorOpen = false;
let emiChart = null;

function toggleSmartFinance() {
    const panel = document.getElementById('smartFinancePanel');
    const btn = document.getElementById('smartFinanceBtn');
    
    if (smartFinanceOpen) {
        // Close panel
        panel.style.display = 'none';
        btn.innerHTML = '<i class="bi bi-stars"></i> <strong>Smart Finance</strong>';
        smartFinanceOpen = false;
    } else {
        // Close EMI Calculator if open
        if (emiCalculatorOpen) {
            toggleEMICalculator();
        }
        
        // Open panel
        panel.style.display = 'block';
        btn.innerHTML = '<i class="bi bi-x-circle"></i> <strong>Close Smart Finance</strong>';
        smartFinanceOpen = true;
        
        // Load all smart finance data
        loadSmartFinanceData();
    }
}

function toggleEMICalculator() {
    const panel = document.getElementById('emiCalculatorPanel');
    const btn = document.getElementById('emiCalculatorBtn');
    
    if (emiCalculatorOpen) {
        // Close panel
        panel.style.display = 'none';
        btn.innerHTML = '<i class="bi bi-calculator"></i> <strong>EMI Calculator</strong>';
        emiCalculatorOpen = false;
        
        // Destroy chart if exists
        if (emiChart) {
            emiChart.destroy();
            emiChart = null;
        }
    } else {
        // Close Smart Finance if open
        if (smartFinanceOpen) {
            toggleSmartFinance();
        }
        
        // Open panel
        panel.style.display = 'block';
        btn.innerHTML = '<i class="bi bi-x-circle"></i> <strong>Close EMI Calculator</strong>';
        emiCalculatorOpen = true;
        
        // Initialize EMI calculation
        updateEMI();
    }
}

function updateEMI() {
    // Get input values
    const loanAmount = parseFloat(document.getElementById('loanAmount').value);
    const interestRate = parseFloat(document.getElementById('interestRate').value);
    const loanTenure = parseFloat(document.getElementById('loanTenure').value);
    
    // Update display values
    document.getElementById('loanAmountDisplay').textContent = formatCurrency(loanAmount);
    document.getElementById('interestRateDisplay').textContent = interestRate.toFixed(1);
    document.getElementById('loanTenureDisplay').textContent = loanTenure;
    
    // Calculate EMI using formula: EMI = [P x R x (1+R)^N]/[(1+R)^N-1]
    const monthlyRate = interestRate / (12 * 100);
    const numberOfMonths = loanTenure * 12;
    
    let emi = 0;
    if (monthlyRate === 0) {
        emi = loanAmount / numberOfMonths;
    } else {
        const power = Math.pow(1 + monthlyRate, numberOfMonths);
        emi = (loanAmount * monthlyRate * power) / (power - 1);
    }
    
    const totalAmount = emi * numberOfMonths;
    const totalInterest = totalAmount - loanAmount;
    
    // Update result displays
    document.getElementById('monthlyEMI').textContent = formatCurrency(Math.round(emi));
    document.getElementById('principalAmount').textContent = formatCurrency(loanAmount);
    document.getElementById('totalInterest').textContent = formatCurrency(Math.round(totalInterest));
    document.getElementById('totalAmount').textContent = formatCurrency(Math.round(totalAmount));
    
    // Update pie chart
    updateEMIChart(loanAmount, totalInterest);
}

function updateEMIChart(principal, interest) {
    const ctx = document.getElementById('emiBreakdownChart');
    
    // Destroy existing chart if it exists
    if (emiChart) {
        emiChart.destroy();
    }
    
    // Create new chart with modern styling
    emiChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Principal Amount', 'Total Interest'],
            datasets: [{
                data: [principal, interest],
                backgroundColor: [
                    '#f093fb',
                    '#f5576c'
                ],
                borderColor: '#ffffff',
                borderWidth: 3,
                hoverBorderWidth: 5,
                hoverOffset: 15
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            cutout: '65%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            size: 13,
                            weight: '600'
                        },
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(44, 62, 80, 0.95)',
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    padding: 12,
                    cornerRadius: 8,
                    displayColors: true,
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ₹${value.toLocaleString('en-IN')} (${percentage}%)`;
                        }
                    }
                }
            },
            animation: {
                animateRotate: true,
                animateScale: true,
                duration: 1500,
                easing: 'easeInOutQuart'
            }
        }
    });
}

function formatCurrency(amount) {
    if (amount >= 10000000) {
        return '₹' + (amount / 10000000).toFixed(2) + ' Cr';
    } else if (amount >= 100000) {
        return '₹' + (amount / 100000).toFixed(2) + ' Lac';
    } else {
        return '₹' + amount.toLocaleString('en-IN');
    }
}

async function loadSmartFinanceData() {
    // Load all three components
    await Promise.all([
        loadFinancialHealthScore(),
        loadAIPredictions(),
        loadAISuggestions()
    ]);
}

// =================== FINANCIAL HEALTH SCORE ===================

async function loadFinancialHealthScore() {
    try {
        // Get user's financial summary
        const response = await fetch(`${API_BASE}/api/analytics/summary`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            const summary = data.data;
            const healthScore = calculateHealthScore(summary);
            displayHealthScore(healthScore);
        }
    } catch (error) {
        console.error('Error loading health score:', error);
        document.getElementById('healthScoreValue').textContent = 'Error';
    }
}

function calculateHealthScore(summary) {
    let score = 0;
    const metrics = {
        savingsRate: 0,
        budgetAdherence: 0,
        spendingTrend: 'stable'
    };
    
    // Calculate Savings Rate (40 points)
    const income = summary.income || 0;
    const expenses = summary.expenses || 0;
    
    if (income > 0) {
        const savingsRate = ((income - expenses) / income) * 100;
        metrics.savingsRate = Math.max(0, savingsRate);
        
        if (savingsRate >= 30) score += 40;
        else if (savingsRate >= 20) score += 30;
        else if (savingsRate >= 10) score += 20;
        else if (savingsRate >= 5) score += 10;
    }
    
    // Calculate Budget Adherence (30 points)
    const budgets = summary.budgets || [];
    if (budgets.length > 0) {
        let adherenceSum = 0;
        budgets.forEach(budget => {
            const spent = budget.spent || 0;
            const limit = budget.amount || 1;
            const adherence = Math.max(0, (1 - (spent / limit)) * 100);
            adherenceSum += Math.min(100, adherence);
        });
        const avgAdherence = adherenceSum / budgets.length;
        metrics.budgetAdherence = avgAdherence;
        
        if (avgAdherence >= 80) score += 30;
        else if (avgAdherence >= 60) score += 20;
        else if (avgAdherence >= 40) score += 10;
        else if (avgAdherence >= 20) score += 5;
    } else {
        score += 15; // Neutral score if no budgets
        metrics.budgetAdherence = 50;
    }
    
    // Calculate Spending Trend (30 points)
    if (income > expenses) {
        score += 30;
        metrics.spendingTrend = 'decreasing';
    } else if (income === expenses) {
        score += 20;
        metrics.spendingTrend = 'stable';
    } else {
        score += 10;
        metrics.spendingTrend = 'increasing';
    }
    
    return {
        score: Math.min(100, Math.round(score)),
        metrics: metrics
    };
}

function displayHealthScore(healthData) {
    const { score, metrics } = healthData;
    
    // Update score value
    document.getElementById('healthScoreValue').textContent = score;
    
    // Update metrics
    document.getElementById('savingsRateLabel').textContent = 
        `Savings Rate: ${metrics.savingsRate.toFixed(1)}%`;
    document.getElementById('budgetAdherenceLabel').textContent = 
        `Budget Adherence: ${metrics.budgetAdherence.toFixed(1)}%`;
    
    let trendText = '';
    if (metrics.spendingTrend === 'increasing') {
        trendText = 'Spending Trend: ⬆️ Increasing';
    } else if (metrics.spendingTrend === 'decreasing') {
        trendText = 'Spending Trend: ⬇️ Decreasing';
    } else {
        trendText = 'Spending Trend: ➡️ Stable';
    }
    document.getElementById('spendingTrendLabel').textContent = trendText;
    
    // Update health status
    let statusText = '';
    let statusColor = '';
    
    if (score >= 80) {
        statusText = '🎉 Excellent! Your finances are in great shape!';
        statusColor = '#27ae60';
    } else if (score >= 60) {
        statusText = '👍 Good! Keep up the positive habits!';
        statusColor = '#3498db';
    } else if (score >= 40) {
        statusText = '⚠️ Fair. There\'s room for improvement!';
        statusColor = '#f39c12';
    } else {
        statusText = '⚠️ Needs Attention. Let\'s work on this!';
        statusColor = '#e74c3c';
    }
    
    document.getElementById('healthStatusText').textContent = statusText;
    document.getElementById('healthStatus').style.background = statusColor;
    
    // Draw gauge chart
    drawHealthScoreGauge(score);
}

function drawHealthScoreGauge(score) {
    const canvas = document.getElementById('healthScoreGauge');
    const ctx = canvas.getContext('2d');
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Settings
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = 80;
    const lineWidth = 20;
    
    // Background arc (grey)
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0.75 * Math.PI, 2.25 * Math.PI);
    ctx.lineWidth = lineWidth;
    ctx.strokeStyle = '#ecf0f1';
    ctx.stroke();
    
    // Score arc (colored based on score)
    const startAngle = 0.75 * Math.PI;
    const endAngle = startAngle + (score / 100) * 1.5 * Math.PI;
    
    let gradient = ctx.createLinearGradient(0, 0, canvas.width, 0);
    if (score >= 80) {
        gradient.addColorStop(0, '#27ae60');
        gradient.addColorStop(1, '#2ecc71');
    } else if (score >= 60) {
        gradient.addColorStop(0, '#3498db');
        gradient.addColorStop(1, '#5dade2');
    } else if (score >= 40) {
        gradient.addColorStop(0, '#f39c12');
        gradient.addColorStop(1, '#f8c471');
    } else {
        gradient.addColorStop(0, '#e74c3c');
        gradient.addColorStop(1, '#ec7063');
    }
    
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, startAngle, endAngle);
    ctx.lineWidth = lineWidth;
    ctx.strokeStyle = gradient;
    ctx.lineCap = 'round';
    ctx.stroke();
}

// =================== AI PREDICTIONS ===================

async function loadAIPredictions() {
    const predictionContent = document.getElementById('predictionContent');
    predictionContent.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>';
    
    try {
        const response = await fetch(`${API_BASE}/api/analytics/predictions`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.success && data.data) {
            displayPredictions(data.data);
        } else {
            predictionContent.innerHTML = '<p class="text-muted">No prediction data available. Add more transactions to see predictions!</p>';
        }
    } catch (error) {
        console.error('Error loading predictions:', error);
        predictionContent.innerHTML = '<p class="text-danger">Error loading predictions. Please try again.</p>';
    }
}

function displayPredictions(predictions) {
    const predictionContent = document.getElementById('predictionContent');
    
    let html = '';
    
    // Display next month prediction
    if (predictions.next_month_prediction) {
        html += `
            <div class="prediction-summary">
                <div>Next Month Forecast</div>
                <h4>₹${predictions.next_month_prediction.toFixed(2)}</h4>
                ${predictions.trend ? `<span class="prediction-trend trend-${predictions.trend}">${predictions.trend.toUpperCase()}</span>` : ''}
            </div>
        `;
    }
    
    // Display category predictions
    if (predictions.category_predictions && Object.keys(predictions.category_predictions).length > 0) {
        html += '<div class="mt-3" style="width: 100%;">';
        for (const [category, amount] of Object.entries(predictions.category_predictions)) {
            html += `
                <div class="prediction-item">
                    <div class="prediction-category">
                        <span>${category}</span>
                        <span class="prediction-amount">₹${amount.toFixed(2)}</span>
                    </div>
                </div>
            `;
        }
        html += '</div>';
    }
    
    // Display confidence
    if (predictions.confidence) {
        html += `
            <div class="mt-3 text-center" style="color: #7f8c8d;">
                <small><i class="bi bi-info-circle"></i> Confidence: ${(predictions.confidence * 100).toFixed(0)}%</small>
            </div>
        `;
    }
    
    if (html === '') {
        html = '<p class="text-muted">No prediction data available yet.</p>';
    }
    
    predictionContent.innerHTML = html;
}

// =================== AI SAVINGS SUGGESTIONS ===================

async function loadAISuggestions() {
    const suggestionContent = document.getElementById('suggestionContent');
    suggestionContent.innerHTML = '<div class="spinner-border text-success" role="status"><span class="visually-hidden">Loading...</span></div>';
    
    try {
        const response = await fetch(`${API_BASE}/api/analytics/suggestions`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.success && data.data) {
            displaySuggestions(data.data);
        } else {
            suggestionContent.innerHTML = '<p class="text-muted">No suggestions available. Add income and expense data to get personalized suggestions!</p>';
        }
    } catch (error) {
        console.error('Error loading suggestions:', error);
        suggestionContent.innerHTML = '<p class="text-danger">Error loading suggestions. Please try again.</p>';
    }
}

function displaySuggestions(suggestions) {
    const suggestionContent = document.getElementById('suggestionContent');
    
    let html = '';
    
    if (suggestions.goals && suggestions.goals.length > 0) {
        suggestions.goals.forEach((goal, index) => {
            const priority = index === 0 ? 'high' : index === 1 ? 'medium' : 'low';
            
            html += `
                <div class="suggestion-item" style="width: 100%;">
                    <div class="suggestion-title">
                        <i class="bi bi-lightbulb-fill"></i>
                        <span>${goal.title}</span>
                        <span class="suggestion-priority priority-${priority}">${priority.toUpperCase()}</span>
                    </div>
                    <div class="suggestion-details">
                        ${goal.description}
                    </div>
                    <div class="suggestion-amount">
                        <div>
                            <strong>Target:</strong> ₹${goal.target_amount ? goal.target_amount.toFixed(2) : 'N/A'}
                        </div>
                        <div>
                            <strong>Monthly:</strong> ₹${goal.suggested_monthly ? goal.suggested_monthly.toFixed(2) : 'N/A'}
                        </div>
                    </div>
                </div>
            `;
        });
    }
    
    if (html === '') {
        html = '<p class="text-muted">No suggestions available yet.</p>';
    }
    
    suggestionContent.innerHTML = html;
}

// =================== NOTIFICATION SYSTEM ===================

function addNotification(type, title, message, icon = null) {
    const notification = {
        id: Date.now(),
        type: type, // 'warning', 'success', 'info', 'danger'
        title: title,
        message: message,
        icon: icon || getDefaultIcon(type),
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    
    notifications.unshift(notification); // Add to beginning
    
    // Keep only last 20 notifications
    if (notifications.length > 20) {
        notifications = notifications.slice(0, 20);
    }
    
    updateNotificationUI();
}

function getDefaultIcon(type) {
    const icons = {
        'warning': 'bi-exclamation-triangle-fill',
        'success': 'bi-check-circle-fill',
        'info': 'bi-info-circle-fill',
        'danger': 'bi-x-circle-fill'
    };
    return icons[type] || 'bi-bell-fill';
}

function updateNotificationUI() {
    const notificationList = document.getElementById('notificationList');
    const notificationBadge = document.getElementById('notificationBadge');
    
    // Update badge count
    if (notifications.length > 0) {
        notificationBadge.textContent = notifications.length;
        notificationBadge.style.display = 'inline';
    } else {
        notificationBadge.style.display = 'none';
    }
    
    // Update notification list
    if (notifications.length === 0) {
        notificationList.innerHTML = `
            <li class="text-center text-muted p-3">
                <i class="bi bi-bell-slash" style="font-size: 2rem;"></i>
                <p class="mb-0 mt-2">No notifications</p>
            </li>
        `;
        return;
    }
    
    let html = '';
    notifications.forEach(notif => {
        html += `
            <li class="notification-item notification-${notif.type}" onclick="dismissNotification(${notif.id})">
                <div class="notification-icon">
                    <i class="bi ${notif.icon}"></i>
                </div>
                <div class="notification-content">
                    <div class="notification-title">${notif.title}</div>
                    <div class="notification-text">${notif.message}</div>
                    <div class="notification-time">${notif.time}</div>
                </div>
            </li>
        `;
    });
    
    notificationList.innerHTML = html;
}

function dismissNotification(id) {
    notifications = notifications.filter(n => n.id !== id);
    updateNotificationUI();
}

function clearAllNotifications() {
    notifications = [];
    updateNotificationUI();
}

function checkAndGenerateNotifications() {
    // This function analyzes data and generates contextual notifications
    
    // Check budgets
    fetch(`${API_BASE}/api/budgets`, {
        headers: { 'Authorization': `Bearer ${authToken}` }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success && data.budgets) {
            data.budgets.forEach(budget => {
                const percentage = (budget.spent / budget.amount) * 100;
                
                if (percentage >= 100) {
                    addNotification(
                        'danger',
                        '⚠️ Budget Exceeded!',
                        `You've exceeded your ${budget.category} budget by ₹${(budget.spent - budget.amount).toFixed(2)}`,
                        'bi-exclamation-triangle-fill'
                    );
                } else if (percentage >= 90) {
                    addNotification(
                        'warning',
                        '⚡ Budget Alert',
                        `You're at ${percentage.toFixed(0)}% of your ${budget.category} budget (₹${budget.amount})`,
                        'bi-exclamation-circle-fill'
                    );
                } else if (percentage >= 75) {
                    addNotification(
                        'info',
                        '📊 Budget Update',
                        `${budget.category}: ${percentage.toFixed(0)}% used. ₹${(budget.amount - budget.spent).toFixed(2)} remaining`,
                        'bi-info-circle-fill'
                    );
                }
            });
        }
    })
    .catch(err => console.error('Error checking budgets:', err));
    
    // Check savings goals
    fetch(`${API_BASE}/api/savings-goals`, {
        headers: { 'Authorization': `Bearer ${authToken}` }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success && data.goals) {
            data.goals.forEach(goal => {
                const percentage = (goal.current_amount / goal.target_amount) * 100;
                
                if (percentage >= 100) {
                    addNotification(
                        'success',
                        '🎉 Goal Achieved!',
                        `Congratulations! You've reached your ${goal.name} goal of ₹${goal.target_amount.toFixed(2)}!`,
                        'bi-trophy-fill'
                    );
                } else if (percentage >= 75) {
                    addNotification(
                        'success',
                        '🎯 Almost There!',
                        `You're ${percentage.toFixed(0)}% towards your ${goal.name} goal. Just ₹${(goal.target_amount - goal.current_amount).toFixed(2)} to go!`,
                        'bi-bullseye'
                    );
                } else if (percentage >= 50) {
                    addNotification(
                        'info',
                        '💪 Keep Going!',
                        `You're halfway to your ${goal.name} goal! Current: ₹${goal.current_amount.toFixed(2)}`,
                        'bi-star-fill'
                    );
                }
            });
        }
    })
    .catch(err => console.error('Error checking goals:', err));
    
    // Check for high spending days
    fetch(`${API_BASE}/api/transactions?limit=10`, {
        headers: { 'Authorization': `Bearer ${authToken}` }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success && data.transactions) {
            const today = new Date().toDateString();
            const todayTransactions = data.transactions.filter(t => 
                new Date(t.date).toDateString() === today && t.transaction_type === 'expense'
            );
            
            const todayTotal = todayTransactions.reduce((sum, t) => sum + t.amount, 0);
            
            if (todayTotal > 2000) {
                addNotification(
                    'warning',
                    '💸 High Spending Alert',
                    `You've spent ₹${todayTotal.toFixed(2)} today across ${todayTransactions.length} transactions`,
                    'bi-cash-stack'
                );
            }
        }
    })
    .catch(err => console.error('Error checking transactions:', err));
    
    // Add motivational tip
    const tips = [
        { title: '💡 Smart Tip', message: 'Save 20% of your income automatically each month', type: 'info' },
        { title: '🎯 Pro Tip', message: 'Review your spending every Sunday to stay on track', type: 'info' },
        { title: '💰 Money Hack', message: 'Cook 3 meals at home this week to save ₹2,000+', type: 'info' },
        { title: '📊 Financial Wisdom', message: 'Track every expense, no matter how small', type: 'info' },
        { title: '🚀 Growth Tip', message: 'Invest your savings instead of letting them sit idle', type: 'info' }
    ];
    
    const randomTip = tips[Math.floor(Math.random() * tips.length)];
    
    // Add tip only if no other notifications exist
    if (notifications.length === 0) {
        addNotification(randomTip.type, randomTip.title, randomTip.message);
    }
}


