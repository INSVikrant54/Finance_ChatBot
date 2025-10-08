#!/usr/bin/env python3
"""Script to generate clean HTML file"""

HTML_CONTENT = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FinanceAI - Personal Finance Assistant</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    
    <!-- Authentication Section (Shown when not logged in) -->
    <div id="authSection">
        <div class="auth-container">
            <div class="auth-card">
                <h1 class="text-center mb-4">
                    <i class="bi bi-robot"></i> FinanceAI
                </h1>
                <p class="text-center text-muted mb-4">Your Intelligent Personal Finance Assistant</p>
                
                <!-- Login/Register Tabs -->
                <ul class="nav nav-tabs mb-4" id="authTabs" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link active" id="login-tab" data-bs-toggle="tab" data-bs-target="#login" type="button" role="tab">Login</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="register-tab" data-bs-toggle="tab" data-bs-target="#register" type="button" role="tab">Register</button>
                    </li>
                </ul>
                
                <div class="tab-content" id="authTabContent">
                    <!-- Login Form -->
                    <div class="tab-pane fade show active" id="login" role="tabpanel">
                        <form id="loginForm">
                            <div class="mb-3">
                                <label for="loginUsername" class="form-label">Username</label>
                                <input type="text" class="form-control" id="loginUsername" placeholder="Enter username" required>
                            </div>
                            <div class="mb-3">
                                <label for="loginPassword" class="form-label">Password</label>
                                <input type="password" class="form-control" id="loginPassword" placeholder="Enter password" required>
                            </div>
                            <button type="submit" class="btn btn-primary w-100">
                                <i class="bi bi-box-arrow-in-right"></i> Login
                            </button>
                        </form>
                        <div class="mt-3 text-center">
                            <small class="text-muted">Demo: username="demo", password="demo123"</small>
                        </div>
                    </div>
                    
                    <!-- Register Form -->
                    <div class="tab-pane fade" id="register" role="tabpanel">
                        <form id="registerForm">
                            <div class="mb-3">
                                <label for="registerUsername" class="form-label">Username</label>
                                <input type="text" class="form-control" id="registerUsername" placeholder="Choose username" required>
                            </div>
                            <div class="mb-3">
                                <label for="registerEmail" class="form-label">Email</label>
                                <input type="email" class="form-control" id="registerEmail" placeholder="Enter email" required>
                            </div>
                            <div class="mb-3">
                                <label for="registerPassword" class="form-label">Password</label>
                                <input type="password" class="form-control" id="registerPassword" placeholder="Choose password" required>
                            </div>
                            <button type="submit" class="btn btn-success w-100">
                                <i class="bi bi-person-plus"></i> Register
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Main Application (Shown after login) -->
    <div id="mainApp" class="d-none">
        <!-- Navigation Bar -->
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container-fluid">
                <a class="navbar-brand" href="#">
                    <i class="bi bi-robot"></i> FinanceAI
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        <li class="nav-item">
                            <a class="nav-link active" href="#"><i class="bi bi-grid-1x2-fill"></i> Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#" data-bs-toggle="modal" data-bs-target="#chatModal">
                                <i class="bi bi-robot"></i> AI Chat
                            </a>
                        </li>
                    </ul>
                    <div class="d-flex align-items-center">
                        <span class="text-white me-3">Welcome, <span id="usernameDisplay"></span>!</span>
                        <button class="btn btn-outline-light btn-sm" id="logoutBtn">
                            <i class="bi bi-box-arrow-right"></i> Logout
                        </button>
                    </div>
                </div>
            </div>
        </nav>
        
        <!-- Main Content -->
        <div class="container-fluid py-4">
            <!-- Summary Cards -->
            <div class="row mb-4">
                <div class="col-md-3 mb-3">
                    <div class="card text-white h-100 gradient-purple">
                        <div class="card-body d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="card-subtitle mb-2">Total Balance</h6>
                                <h3 class="card-title mb-0" id="totalBalance">₹0</h3>
                            </div>
                            <i class="bi bi-wallet2 fs-1"></i>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 mb-3">
                    <div class="card text-white h-100 gradient-green">
                        <div class="card-body d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="card-subtitle mb-2">This Month Income</h6>
                                <h3 class="card-title mb-0" id="monthIncome">₹0</h3>
                            </div>
                            <i class="bi bi-arrow-down-circle fs-1"></i>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 mb-3">
                    <div class="card text-white h-100 gradient-red">
                        <div class="card-body d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="card-subtitle mb-2">This Month Expenses</h6>
                                <h3 class="card-title mb-0" id="monthExpenses">₹0</h3>
                            </div>
                            <i class="bi bi-arrow-up-circle fs-1"></i>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 mb-3">
                    <div class="card text-white h-100 gradient-blue">
                        <div class="card-body d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="card-subtitle mb-2">Savings Goals</h6>
                                <h3 class="card-title mb-0" id="goalsCount">0</h3>
                            </div>
                            <i class="bi bi-bullseye fs-1"></i>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Action Buttons -->
            <div class="row mb-4">
                <div class="col-12">
                    <button class="btn btn-primary me-2" data-bs-toggle="modal" data-bs-target="#transactionModal">
                        <i class="bi bi-plus-circle"></i> Add Transaction
                    </button>
                    <button class="btn btn-success me-2" data-bs-toggle="modal" data-bs-target="#budgetModal">
                        <i class="bi bi-journal-album"></i> Create Budget
                    </button>
                    <button class="btn btn-info me-2" data-bs-toggle="modal" data-bs-target="#goalModal">
                        <i class="bi bi-bullseye"></i> Add Savings Goal
                    </button>
                    <button class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#chatModal">
                        <i class="bi bi-robot"></i> Chat with AI
                    </button>
                </div>
            </div>
            
            <!-- Charts and Analytics -->
            <div class="row mb-4">
                <div class="col-md-6 mb-3">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title"><i class="bi bi-pie-chart"></i> Spending by Category</h5>
                            <canvas id="spendingDoughnutChart"></canvas>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 mb-3">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title"><i class="bi bi-bar-chart"></i> Monthly Trend</h5>
                            <canvas id="trendLineChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Recent Transactions -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title"><i class="bi bi-list-ul"></i> Recent Transactions</h5>
                            <div class="table-responsive">
                                <table class="table table-striped table-hover">
                                    <thead>
                                        <tr>
                                            <th>Date</th>
                                            <th>Description</th>
                                            <th>Category</th>
                                            <th>Amount</th>
                                            <th>Type</th>
                                            <th>Action</th>
                                        </tr>
                                    </thead>
                                    <tbody id="transactionsTable">
                                        <tr>
                                            <td colspan="6" class="text-center text-muted">No transactions yet. Add your first transaction!</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Budgets and Goals -->
            <div class="row">
                <div class="col-md-6 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title"><i class="bi bi-journal-album"></i> Active Budgets</h5>
                            <div id="budgetsList">
                                <p class="text-muted">No budgets set. Create one to track your spending!</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title"><i class="bi bi-bullseye"></i> Savings Goals</h5>
                            <div id="goalsList">
                                <p class="text-muted">No savings goals yet. Set a goal to start saving!</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Transaction Modal -->
    <div class="modal fade" id="transactionModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Add Transaction</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="transactionForm">
                        <div class="mb-3">
                            <label for="transactionDescription" class="form-label">Description</label>
                            <input type="text" class="form-control" id="transactionDescription" placeholder="e.g., Grocery shopping" required>
                        </div>
                        <div class="mb-3">
                            <label for="transactionAmount" class="form-label">Amount (₹)</label>
                            <input type="number" class="form-control" id="transactionAmount" step="0.01" placeholder="0.00" required>
                        </div>
                        <div class="mb-3">
                            <label for="transactionType" class="form-label">Type</label>
                            <select class="form-select" id="transactionType" required>
                                <option value="expense">Expense</option>
                                <option value="income">Income</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="transactionCategory" class="form-label">Category</label>
                            <select class="form-select" id="transactionCategory" required>
                                <option value="Food">Food</option>
                                <option value="Transport">Transport</option>
                                <option value="Shopping">Shopping</option>
                                <option value="Entertainment">Entertainment</option>
                                <option value="Bills">Bills</option>
                                <option value="Healthcare">Healthcare</option>
                                <option value="Education">Education</option>
                                <option value="Salary">Salary</option>
                                <option value="Investment">Investment</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="transactionDate" class="form-label">Date</label>
                            <input type="date" class="form-control" id="transactionDate" required>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">
                            <i class="bi bi-plus-circle"></i> Add Transaction
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Budget Modal -->
    <div class="modal fade" id="budgetModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Create Budget</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="budgetForm">
                        <div class="mb-3">
                            <label for="budgetCategory" class="form-label">Category</label>
                            <select class="form-select" id="budgetCategory" required>
                                <option value="Food">Food</option>
                                <option value="Transport">Transport</option>
                                <option value="Shopping">Shopping</option>
                                <option value="Entertainment">Entertainment</option>
                                <option value="Bills">Bills</option>
                                <option value="Healthcare">Healthcare</option>
                                <option value="Education">Education</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="budgetAmount" class="form-label">Budget Amount (₹)</label>
                            <input type="number" class="form-control" id="budgetAmount" step="0.01" placeholder="0.00" required>
                        </div>
                        <div class="mb-3">
                            <label for="budgetPeriod" class="form-label">Period</label>
                            <select class="form-select" id="budgetPeriod" required>
                                <option value="monthly">Monthly</option>
                                <option value="weekly">Weekly</option>
                                <option value="yearly">Yearly</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-success w-100">
                            <i class="bi bi-journal-album"></i> Create Budget
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Goal Modal -->
    <div class="modal fade" id="goalModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Add Savings Goal</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="goalForm">
                        <div class="mb-3">
                            <label for="goalName" class="form-label">Goal Name</label>
                            <input type="text" class="form-control" id="goalName" placeholder="e.g., Vacation Fund" required>
                        </div>
                        <div class="mb-3">
                            <label for="goalTarget" class="form-label">Target Amount (₹)</label>
                            <input type="number" class="form-control" id="goalTarget" step="0.01" placeholder="0.00" required>
                        </div>
                        <div class="mb-3">
                            <label for="goalCurrent" class="form-label">Current Amount (₹)</label>
                            <input type="number" class="form-control" id="goalCurrent" step="0.01" value="0" placeholder="0.00">
                        </div>
                        <div class="mb-3">
                            <label for="goalDeadline" class="form-label">Deadline (Optional)</label>
                            <input type="date" class="form-control" id="goalDeadline">
                        </div>
                        <button type="submit" class="btn btn-info w-100">
                            <i class="bi bi-bullseye"></i> Add Goal
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    
    <!-- AI Chat Modal -->
    <div class="modal fade" id="chatModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header bg-primary text-white">
                    <h5 class="modal-title"><i class="bi bi-robot"></i> AI Financial Assistant</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body chat-container" id="chatMessages">
                    <div class="text-center text-muted py-5">
                        <i class="bi bi-robot fs-1"></i>
                        <p class="mt-3">Hello! I'm your AI financial assistant. Ask me anything about your finances!</p>
                    </div>
                </div>
                <div class="modal-footer">
                    <form id="chatForm" class="w-100">
                        <div class="input-group">
                            <input type="text" class="form-control" id="chatInput" placeholder="Ask about your spending, budgets, or financial advice..." required>
                            <button type="submit" class="btn btn-primary">
                                <i class="bi bi-send"></i> Send
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Custom JS -->
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    
</body>
</html>
'''

if __name__ == '__main__':
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(HTML_CONTENT)
    print("✅ HTML file generated successfully!")
