
```markdown
# ♻️ E-Waste Management System

A **Flask-based web application** that streamlines the process of collecting and managing electronic waste.  
It enables **users** to request pickup of e-waste items and allows **administrators** to manage, accept, reject, or complete those requests.

The project also integrates **Selenium WebDriver and IDE** for automated web testing.

---

## 📖 Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Installation Guide](#installation-guide)
6. [Running the Application](#running-the-application)
7. [Creating an Admin User](#creating-an-admin-user)
8. [Testing with Selenium](#testing-with-selenium)
9. [Screenshots](#screenshots)
10. [Contributing](#contributing)
11. [License](#license)

---

## 🧩 Overview

The **E-Waste Management System** provides an online platform for responsible disposal of electronic waste.  
Users can submit pickup requests for e-waste items, and admins can schedule, complete, or cancel requests.

This project demonstrates:
- Flask backend and routing  
- User authentication using Flask-Login  
- SQLite database integration with SQLAlchemy  
- Selenium automation for testing web workflows  

---

## 🚀 Features

### 👥 User Module
- Register and Login securely  
- Submit pickup requests (item type, quantity, location)  
- View request history and statuses  
- Cancel pending requests  

### 🛠️ Admin Module
- Admin-only login access  
- View all user pickup requests  
- Accept (Schedule), Complete, or Cancel requests  
- Manage workflow for e-waste collection  

### 🧪 Testing
- Automated testing using **Selenium WebDriver**  
- Record and playback tests using **Selenium IDE**  
- Bug detection, regression testing, and reporting  

---

## ⚙️ Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend** | HTML, CSS, Bootstrap |
| **Backend** | Python (Flask Framework) |
| **Database** | SQLite3 |
| **Testing** | Selenium WebDriver / IDE |
| **Version Control** | Git & GitHub |



---

## 🧰 Installation Guide

### Step 1: Clone the Repository
```bash
git clone https://github.com/<your-username>/e-waste-management.git
cd e-waste-management
````

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # For Windows
# OR
source venv/bin/activate   # For macOS/Linux
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Flask App Environment (only first time)

**Windows:**

```bash
set FLASK_APP=run.py
set FLASK_ENV=development
```

**macOS / Linux:**

```bash
export FLASK_APP=run.py
export FLASK_ENV=development
```

---

## ▶️ Running the Application

### Method 1: Using Flask CLI

```bash
flask run
```

### Method 2: Using Python

```bash
python run.py
```

After running the application, open your browser and visit:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

### 💡 Selenium Testing

After the Flask app is running,
open a **new terminal** and execute any of your Selenium scripts.

You can check the generated test results inside:

* `report_user`
* `report_admin`

---

```

```
