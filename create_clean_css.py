"""
Create clean CSS file with proper text visibility
"""

css_content = """/* ========================================
   FINANCEAI - PROFESSIONAL GREY THEME
   Silver-Grey Color Palette with Animations
   FIXED TEXT VISIBILITY
   ======================================== */

/* Global Styles */
body {
    background: linear-gradient(135deg, #bdc3c7 0%, #2c3e50 100%);
    min-height: 100vh;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    overflow-x: hidden;
}

/* Card Styles - Silver Grey Theme */
.card {
    background: linear-gradient(145deg, #ffffff 0%, #f5f7fa 100%);
    border: 1px solid rgba(44, 62, 80, 0.1);
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(44, 62, 80, 0.1);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    animation: cardSlideIn 0.6s ease-out;
    position: relative;
    overflow: hidden;
}

.card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(189, 195, 199, 0.3), transparent);
    transition: left 0.5s;
}

.card:hover::before {
    left: 100%;
}

.card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 15px 35px rgba(44, 62, 80, 0.2);
    border-color: rgba(127, 140, 141, 0.3);
}

.card-icon {
    font-size: 2.5rem;
    opacity: 0.7;
    transition: all 0.3s ease;
    animation: float 3s ease-in-out infinite;
}

.card:hover .card-icon {
    opacity: 1;
    transform: scale(1.1) rotate(5deg);
}

/* TEXT VISIBILITY FIX - High Contrast for Gradient Cards */
.gradient-purple {
    background: linear-gradient(135deg, #7f8c8d 0%, #2c3e50 100%) !important;
    color: #ffffff !important;
    border: none;
}

.gradient-purple * {
    color: #ffffff !important;
    text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.8);
}

.gradient-purple h3,
.gradient-purple h6,
.gradient-purple .card-title,
.gradient-purple .card-subtitle {
    font-weight: 700 !important;
    letter-spacing: 0.5px;
}

.gradient-green {
    background: linear-gradient(135deg, #95a5a6 0%, #5f6f7a 100%) !important;
    color: #ffffff !important;
    border: none;
}

.gradient-green * {
    color: #ffffff !important;
    text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.8);
}

.gradient-green h3,
.gradient-green h6,
.gradient-green .card-title,
.gradient-green .card-subtitle {
    font-weight: 700 !important;
    letter-spacing: 0.5px;
}

.gradient-red {
    background: linear-gradient(135deg, #636e72 0%, #2d3436 100%) !important;
    color: #ffffff !important;
    border: none;
}

.gradient-red * {
    color: #ffffff !important;
    text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.8);
}

.gradient-red h3,
.gradient-red h6,
.gradient-red .card-title,
.gradient-red .card-subtitle {
    font-weight: 700 !important;
    letter-spacing: 0.5px;
}

.gradient-blue {
    background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%) !important;
    color: #ffffff !important;
    border: none;
}

.gradient-blue * {
    color: #ffffff !important;
    text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.8);
}

.gradient-blue h3,
.gradient-blue h6,
.gradient-blue .card-title,
.gradient-blue .card-subtitle {
    font-weight: 700 !important;
    letter-spacing: 0.5px;
}

/* All text-white cards get enhanced visibility */
.card.text-white * {
    color: #ffffff !important;
    text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.8);
    font-weight: 600 !important;
}

.card.text-white h1,
.card.text-white h2,
.card.text-white h3,
.card.text-white h4,
.card.text-white h5,
.card.text-white h6 {
    font-weight: 800 !important;
}

.card.text-white i {
    filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.6));
}

/* Button Styles - Grey Theme */
.btn-primary {
    background: linear-gradient(135deg, #7f8c8d 0%, #2c3e50 100%);
    border: none;
    box-shadow: 0 4px 15px rgba(44, 62, 80, 0.2);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.btn-primary::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
}

.btn-primary:hover::before {
    width: 300px;
    height: 300px;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(44, 62, 80, 0.3);
}

.btn-success {
    background: linear-gradient(135deg, #95a5a6 0%, #5f6f7a 100%);
    border: none;
}

.btn-danger {
    background: linear-gradient(135deg, #636e72 0%, #2d3436 100%);
    border: none;
}

.btn-info {
    background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%);
    border: none;
}

.btn-warning {
    background: linear-gradient(135deg, #bdc3c7 0%, #95a5a6 100%);
    border: none;
    color: #2c3e50;
}

/* Table Styles */
.table-responsive {
    max-height: 500px;
    overflow-y: auto;
    border-radius: 10px;
    animation: fadeIn 1s ease-out;
}

.table {
    animation: fadeIn 1s ease-out;
}

.table thead {
    position: sticky;
    top: 0;
    background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
    color: white;
    z-index: 1;
}

.table tbody tr {
    transition: all 0.3s ease;
}

.table tbody tr:hover {
    background-color: rgba(189, 195, 199, 0.1);
    transform: scale(1.01);
}

/* Badge Styles */
.badge {
    padding: 0.5em 1em;
    font-weight: 500;
    animation: fadeIn 0.5s ease-out;
}

/* Progress Bar Animations */
.progress {
    height: 8px;
    border-radius: 10px;
    overflow: visible;
    background: rgba(189, 195, 199, 0.2);
}

.progress-bar {
    background: linear-gradient(90deg, #7f8c8d 0%, #2c3e50 100%);
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(44, 62, 80, 0.3);
    animation: progressSlide 1s ease-out;
    position: relative;
    overflow: hidden;
}

.progress-bar::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
    animation: shimmer 2s infinite;
}

/* Chat Container */
#chatMessages {
    height: 400px;
    overflow-y: auto;
    padding: 20px;
    background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
    border-radius: 15px;
    animation: fadeIn 0.8s ease-out;
}

.chat-message {
    margin-bottom: 15px;
    padding: 12px 18px;
    border-radius: 18px;
    max-width: 70%;
    animation: slideDown 0.3s ease-out;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.chat-message:hover {
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    transform: translateY(-2px);
}

.user-message {
    background: linear-gradient(135deg, #7f8c8d 0%, #34495e 100%);
    color: white;
    margin-left: auto;
    text-align: right;
}

.ai-message {
    background: linear-gradient(135deg, #ecf0f1 0%, #bdc3c7 100%);
    color: #2c3e50;
}

/* Modal Styles */
.modal-content {
    border-radius: 15px;
    border: none;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    animation: modalZoomIn 0.3s ease-out;
}

.modal-header {
    background: linear-gradient(135deg, #7f8c8d 0%, #2c3e50 100%);
    color: white;
    border-radius: 15px 15px 0 0;
    border: none;
}

.modal-body {
    padding: 30px;
}

/* Form Styles */
.form-control,
.form-select {
    border: 2px solid rgba(189, 195, 199, 0.3);
    border-radius: 10px;
    padding: 12px;
    transition: all 0.3s ease;
}

.form-control:focus,
.form-select:focus {
    border-color: #7f8c8d;
    box-shadow: 0 0 0 0.2rem rgba(127, 140, 141, 0.25);
    transform: scale(1.02);
}

.form-label {
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 8px;
}

/* Auth Container - ENHANCED TEXT VISIBILITY */
.auth-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
    animation: fadeIn 0.8s ease-out;
}

.auth-card {
    background: white;
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    max-width: 450px;
    width: 100%;
    animation: cardZoomIn 0.5s ease-out;
}

.auth-card h1 {
    color: #2c3e50 !important;
    font-weight: 800 !important;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.auth-card .bi-robot {
    color: #7f8c8d !important;
    font-size: 3rem;
    filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.3));
}

.auth-card p {
    color: #34495e !important;
    font-weight: 600 !important;
    font-size: 1.1rem;
}

.auth-card .nav-link {
    color: #2c3e50;
    font-weight: 600;
}

.auth-card .nav-link.active {
    background: linear-gradient(135deg, #7f8c8d 0%, #2c3e50 100%);
    color: white;
}

/* Responsive */
@media (max-width: 768px) {
    .card {
        margin-bottom: 15px;
    }
    
    .chat-message {
        max-width: 85%;
    }
    
    .auth-card {
        padding: 30px 20px;
    }
}

/* Animations */
@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes cardSlideIn {
    from {
        opacity: 0;
        transform: translateY(50px) scale(0.9);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

@keyframes cardZoomIn {
    from {
        opacity: 0;
        transform: scale(0.8);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

@keyframes modalZoomIn {
    from {
        opacity: 0;
        transform: scale(0.7);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

@keyframes progressSlide {
    from {
        width: 0;
    }
}

@keyframes shimmer {
    0% {
        transform: translateX(-100%);
    }
    100% {
        transform: translateX(100%);
    }
}

@keyframes float {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-10px);
    }
}

/* Chart Container */
.chart-container {
    position: relative;
    height: 300px;
    animation: fadeIn 1s ease-out;
}

/* Scrollbar Styling */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(189, 195, 199, 0.1);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #7f8c8d 0%, #2c3e50 100%);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #2c3e50 0%, #7f8c8d 100%);
}

/* Loading Animation */
.loading {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid rgba(127, 140, 141, 0.3);
    border-radius: 50%;
    border-top-color: #7f8c8d;
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}
"""

# Write the CSS file
with open('static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css_content)

print("✅ Clean CSS file created with enhanced text visibility!")
print("✅ Text shadows added for better contrast")
print("✅ Font weights increased for dashboard balance and auth screen")
print("✅ All gradient cards now have high contrast white text")
