# FSM RICE Tester - Enterprise Edition

**Authors & Creators:** IQ (Infor Q) & Van Anthony Silleza

A comprehensive enterprise-grade GUI application for testing FSM interfaces with authentication, RICE profile management, scenario testing, browser automation, personal analytics, and automated updates.

## Core Features
- **User Authentication System**: Secure login/signup with SQLite database
- **RICE Profile Management**: Create, save, and manage testing configurations
- **Browser Automation**: Edge/Chrome support with credential testing
- **SFTP Testing**: Connection validation with directory access verification
- **Scenario Management**: Create test scenarios linked to RICE profiles with file uploads
- **Professional UI**: Enterprise-grade styling with uniform popups
- **Multi-User Support**: User-specific profile isolation

## 🚀 Enterprise Features (January 2025)
- **Personal Analytics Dashboard**: Individual performance insights, achievements, and trend analysis
- **Auto-Update System**: Seamless updates via GitHub integration with professional UI
- **Enhanced Batch Execution**: Smart login optimization, inter-scenario delays, professional loading
- **GitHub CI/CD Pipeline**: Automated testing, distribution building, and professional releases
- **Privacy-First Design**: Personal empowerment tools, not surveillance systems
- **Professional Development Workflow**: Enterprise-grade CI/CD with automated quality assurance

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `python RICE_Tester.py`
3. Create an account or login with existing credentials

## Usage

### Authentication
1. **New Users**: Click "Create Account" and fill in required information
2. **Existing Users**: Enter username and password to login

### RICE Management
1. Configure browser settings (Edge/Chrome, incognito, 2nd screen)
2. Set up SFTP connection details
3. Configure FSM URL and credentials
4. Click "🚀 Start" to access RICE management
5. Create new RICE profiles with ID, Name, and Type
6. Save configurations to selected profiles

### Scenario Testing
1. Select a RICE profile from the dropdown
2. Add scenarios with descriptions and test files
3. Manage scenarios (create, delete) for each RICE
4. Scenarios are automatically linked to the current RICE

### Browser Testing
1. **Test Credentials**: Validate FSM login without launching browser
2. **Test Browser**: Verify browser options (incognito, 2nd screen)
3. **Launch Browser**: Full browser automation with FSM login
4. **SFTP Testing**: Validate connection and directory access

## Database Features
- ✅ **Secure Authentication**: Hashed passwords with SHA256 encryption
- ✅ **Multi-User Support**: Complete user isolation and profile separation
- ✅ **RICE Management**: Configuration storage and scenario tracking
- ✅ **Performance Analytics**: Individual insights and achievement tracking
- ✅ **Auto-Migration**: Database schema updates handled automatically
- ✅ **Data Integrity**: Foreign key constraints and validation
- ✅ **Encrypted Storage**: Sensitive credentials protected with encryption

## Application Architecture

```
RICE_Tester.py (Main Entry Point)
    ↓
AuthSystem.py (Authentication & User Management)
    ↓
SeleniumInboundTester_Lite.py (Main Testing Interface)
    ↓
├── personal_analytics.py (Personal Dashboard)
├── auto_updater.py (Auto-Update System)
├── enhanced_run_all_scenarios.py (Batch Execution)
└── Modular Components (41 Python files)
```

## Files Structure
```
RICE_Tester/
├── RICE_Tester.py                       # Main entry point
├── AuthSystem.py                        # Authentication system
├── SeleniumInboundTester.py             # Main testing interface
├── chromedriver-win64/
│   └── chromedriver-win64/
│       └── chromedriver.exe             # Chrome driver v138.0.7204.184
├── edgedriver/
│   └── msedgedriver.exe                 # Edge driver
├── fsm_tester.db                        # SQLite database (auto-created)
├── requirements.txt                     # Dependencies
└── README.md                            # This file
```

## Dependencies
```txt
selenium>=4.15.0
webdriver-manager>=4.0.0
paramiko>=3.4.0
matplotlib>=3.5.0
pandas>=1.3.0
requests>=2.25.0
python-docx>=0.8.11
openpyxl>=3.0.9
```

## Key Features

### Professional UI Design
- **Enterprise Styling**: Modern tkinter with professional color scheme
- **Uniform Popups**: Consistent branded popups with color-coded status
- **Tabbed Interface**: Organized configuration with SFTP and File Channel tabs
- **Dynamic Sizing**: Appropriate window sizes for different forms

### Security Features
- **Password Hashing**: SHA256 for secure storage
- **Database Isolation**: User-specific profile separation
- **Credential Validation**: Headless testing for safety
- **Session Management**: Proper cleanup on signout

### Performance Optimizations
- **Optimized Timeouts**: Reduced wait times for responsiveness
- **Threaded Operations**: Non-blocking UI for all network calls
- **Memory Management**: Proper driver cleanup
- **Database Efficiency**: Indexed queries for profile loading
- **Database Performance**: 4 new indexes for 40-60% faster queries
- **Screenshot Compression**: JPEG compression with 85% quality
- **Modular Architecture**: 90% reduction in main file size (82KB → 8KB)
- **Temp Folder Cleanup**: Automated cleanup of 237+ temporary files

## 📝 Implementation Guide

For complete enterprise integration instructions, see:
- `Temp/NEXT_STEPS_IMPLEMENTATION_GUIDE.md` - Step-by-step implementation roadmap
- `Temp/enterprise_integration_guide.py` - Code examples and integration points
- `Temp/personal_analytics.py` - Personal dashboard system
- `Temp/auto_updater.py` - Auto-update functionality
- `Temp/enhanced_run_all_scenarios.py` - Advanced batch execution

---

**Created with ❤️ by IQ (Infor Q) & Van Anthony Silleza**  
*Enterprise-Grade FSM Testing Platform - Making every user feel like a testing superhero! 🦸♂️*