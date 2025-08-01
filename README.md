# 🏥 Hospital Appointment Booking System

A comprehensive AI-powered hospital appointment booking system built with FastAPI, LangGraph, and Streamlit. The system uses multiple specialized agents to handle appointment booking, doctor availability checks, and general inquiries with natural language processing.

## 🎬 Demo Video

Watch the Hospital Appointment Booking System in action:

https://github.com/user-attachments/assets/multi-agent-appointment-booking-demo.mp4

*The demo showcases the multi-agent conversation flow, natural language processing capabilities, and seamless appointment booking experience.*

> **Note**: If the video doesn't play directly in GitHub, you can download it from the [`demo/`](demo/) folder in this repository.

## 🌟 Features

### 🤖 AI-Powered Agents
- **Supervisor Agent**: Routes conversations to appropriate specialized agents
- **Information Agent**: Handles doctor availability queries and information requests
- **Booking Agent**: Manages appointment booking, cancellation, and rescheduling with confirmation requirements

### 📅 Appointment Management
- **Book Appointments**: Schedule appointments with available doctors
- **Check Availability**: View doctor schedules by name or specialization
- **Cancel Appointments**: Cancel existing appointments with confirmation
- **Reschedule Appointments**: Move appointments to new dates/times
- **Patient ID Management**: Secure patient identification system

### 🏥 Medical Specializations Supported
- General Dentist
- Cosmetic Dentist
- Prosthodontist
- Pediatric Dentist
- Emergency Dentist
- Oral Surgeon
- Orthodontist
- General Medicine

### 🔧 Technical Features
- **Session Management**: Thread-based conversation tracking
- **Database Integration**: SQLite database with structured appointment data
- **Real-time Logging**: Comprehensive debugging and monitoring
- **Date Format Validation**: Consistent DD-MM-YYYY HH:MM format enforcement
- **Error Handling**: Robust error management and user feedback
- **RESTful API**: Clean FastAPI endpoints with automatic documentation

## 📋 Prerequisites

### For Manual Installation (Method 1)
- Python 3.12+
- pip (Python package installer)
- SQLite3
- Internet connection (for LLM API calls)
- Virtual environment support (recommended for isolation)

### For Docker Installation (Method 2) - Recommended
- Docker Engine 20.10+
- Docker Compose 2.0+
- Internet connection (for LLM API calls)
- 4GB+ available RAM

## 🚀 Installation

### Method 1: Manual Installation

1. **Open the folder**
   ```bash
   cd hospital_appointment_booking_app
   ```

2. **Create and activate virtual environment**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   # On Linux/Mac:
   source venv/bin/activate
   
   # On Windows:
   # venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your LLM API keys (Gemini API key required)
   ```

5. **Initialize the database**
   ```bash
   python database/populate_db.py
   ```

### Method 2: Docker Installation

1. **Open the folder**
   ```bash
   cd hospital_appointment_booking_app
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your LLM API keys (Gemini API key required)
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

   The database will be automatically initialized during the container build process.

## 🎯 Quick Start

### Method 1: Manual Start

1. **Start FastAPI Server**
   ```bash
   python main.py
   ```

2. **Start Streamlit UI** (in a new terminal)
   ```bash
   streamlit run streamlit_ui.py
   ```

### Method 2: Docker Compose

1. **Build and start all services**
   ```bash
   docker-compose up --build
   ```

2. **Run in detached mode** (optional)
   ```bash
   docker-compose up -d --build
   ```

3. **Stop services**
   ```bash
   docker-compose down
   ```

4. **View logs** (if running in detached mode)
   ```bash
   # View all logs
   docker-compose logs
   
   # View specific service logs
   docker-compose logs backend
   docker-compose logs frontend
   
   # Follow logs in real-time
   docker-compose logs -f
   ```

**Benefits of Docker Compose:**
- 🐳 Containerized environment for consistency
- 🚀 One-command deployment
- 🔧 Automatic service dependency management
- 📊 Isolated network environment
- 🔄 Easy scaling and management

## 🌐 Access Points

**Both methods (Manual & Docker) use the same URLs:**

- **Streamlit UI**: http://localhost:8501
- **FastAPI Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📖 Usage Guide

### 🗣️ Natural Language Interactions

The system understands natural language queries. Here are example interactions:

#### Checking Availability
```
"Check availability for Dr. John Doe on 01-08-2025"
"What slots are available for general dentist on 05-08-2025?"
"Show me orthodontist availability this week"
```

#### Booking Appointments
```
"Book an appointment with Dr. Jane Smith on 03-08-2025 at 2:30 PM"
"I need to schedule with a pediatric dentist"
"Book me with general medicine doctor for tomorrow morning"
```

#### Managing Appointments
```
"Cancel my appointment with Dr. John Doe on 01-08-2025 at 10:00"
"Reschedule my appointment from 01-08-2025 to 05-08-2025"
"Change my appointment time to 3:00 PM"
```

### 📅 Date Format Requirements

**Important**: Always use the format DD-MM-YYYY HH:MM for appointments
- ✅ Correct: `01-08-2025 14:30`
- ❌ Incorrect: `2025-08-01 2:30 PM`, `08/01/2025`

### 🔐 Patient ID Format

Patient IDs must be 7 or 8 digits:
- ✅ Valid: `1234567`, `12345678`
- ❌ Invalid: `123456`, `123456789`

## 🏗️ System Architecture

### Manual Deployment
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit UI  │────│   FastAPI Server │────│   LangGraph     │
│                 │    │                  │    │   Agent System  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                │                        │
                        ┌──────────────────┐    ┌─────────────────┐
                        │  SQLite Database │    │   LLM Provider  │
                        │                  │    │   (LLM API)    │
                        └──────────────────┘    └─────────────────┘
```

### Docker Deployment
```
┌─────────────────────────────────────────────────────────────────┐
│                        Docker Network                           │
│                                                                 │
│  ┌─────────────────┐    ┌──────────────────┐    ┌─────────────┐  │
│  │  Frontend       │────│   Backend        │────│ LangGraph   │  │
│  │  Container      │    │   Container      │    │ Agent       │  │
│  │  (Streamlit)    │    │   (FastAPI)      │    │ System      │  │
│  └─────────────────┘    └──────────────────┘    └─────────────┘  │
│         │                        │                      │        │
│         │                        │                      │        │
│  ┌─────────────────┐    ┌──────────────────┐    ┌─────────────┐  │
│  │   Port 8501     │    │  SQLite Database │    │ LLM Provider│  │
│  │   Exposed       │    │  Volume Mount    │    │ (External)  │  │
│  └─────────────────┘    └──────────────────┘    └─────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                │
                        ┌──────────────────┐
                        │   Port 8000      │
                        │   Exposed        │
                        └──────────────────┘
```

### 🔧 Core Components

#### **FastAPI Backend** (`main.py`)
- RESTful API endpoints
- Session management
- Request/response handling
- Comprehensive logging

#### **LangGraph Agent System** (`agent.py`)
- Multi-agent conversation management
- State-based dialog flow
- Tool integration
- Memory persistence

#### **Database Layer** (`database/`)
- SQLite database storage
- Doctor availability management
- Appointment tracking
- Data validation

#### **Tools & Functions** (`toolkit/`)
- Appointment booking logic
- Availability checking
- Database operations
- Data validation

## 🗂️ Project Structure

```
hospital_appointment_booking_app/
├── 📁 agents/                  # Agent base classes and configurations
├── 📁 database/               # Database files and population scripts
├── 📁 models/                 # Pydantic models for data validation
├── 📁 prompts/                # Agent prompts and instructions
├── 📁 toolkit/                # Tools and functions for agents
├── 📁 utils/                  # Utility functions and helpers
├── 📄 agent.py                # Main agent graph construction
├── 📄 main.py                 # FastAPI server application
├── 📄 streamlit_ui.py         # Streamlit user interface
├── 📄 requirements.txt        # Python dependencies
└── 📄 README.md               # This file
```

## 🛠️ Configuration

### Environment Variables

Create a `.env` file with:
```env
GOOGLE_API_KEY=gemini_api_key
HOST=0.0.0.0
PORT=8000
```

### Database Configuration

The system uses SQLite with the following schema:
- **Table**: `doctor_availability`
- **Columns**: `date`, `time_slot`, `specialization`, `doctor_name`, `is_available`, `patient_id`

## 🔍 Debugging

### Enable Debug Logging
The system includes comprehensive logging. Check server logs for:
- Node execution flow
- State transitions
- Tool calls
- Error details

### Common Issues

#### Manual Installation Issues
1. **Date Format Errors**: Ensure DD-MM-YYYY HH:MM format
2. **Patient ID Validation**: Use 7-8 digit numbers only
3. **Database Connection**: Check if `hospital.db` exists
4. **API Key Issues**: Verify LLM API key in `.env`
5. **Virtual Environment**: Ensure virtual environment is activated before running commands
   ```bash
   # Activate if not already active
   source venv/bin/activate
   
   # Deactivate when done
   deactivate
   ```

#### Docker Installation Issues
1. **Port Conflicts**: Ensure ports 8000 and 8501 are not in use
   ```bash
   # Check port usage
   sudo netstat -tlnp | grep -E ':(8000|8501)'
   
   # Stop conflicting services if needed
   docker-compose down
   ```

2. **Docker Service Issues**: Check container status
   ```bash
   # View running containers
   docker-compose ps
   
   # Check container logs
   docker-compose logs backend
   docker-compose logs frontend
   ```

3. **Build Issues**: Clean build if needed
   ```bash
   # Clean build
   docker-compose down
   docker-compose build --no-cache
   docker-compose up
   ```

4. **Environment Variables**: Ensure `.env` file exists and contains required keys
   ```bash
   # Check if .env file exists
   ls -la .env
   
   # Verify required variables
   grep -E "GOOGLE_API_KEY" .env
   ```

## 📊 Available Doctors & Schedule

### Doctor Availability
- **Available Dates**: July 31, 2025 - August 15, 2025
- **Available Days**: Monday to Friday
- **Time Slots**: 09:00 - 15:00 (hourly slots)

### Medical Staff

#### General Dentist
- John Doe
- Susan Davis
- Daniel Miller
- Sarah Wilson

#### Specialists
- **Cosmetic Dentist**: Jane Smith
- **Prosthodontist**: Emily Johnson
- **Pediatric Dentist**: Michael Green
- **Emergency Dentist**: Lisa Brown
- **Oral Surgeon**: Kevin Anderson
- **Orthodontist**: Robert Martinez
- **General Medicine**: Alex Turner

## 🔄 API Endpoints

### FastAPI Endpoints

- `POST /execute` - Main query processing endpoint
- `POST /generate-stream/` - Alternative processing endpoint
- `GET /health` - Health check endpoint
- `GET /` - API information endpoint
- `GET /docs` - Interactive API documentation

### Example API Usage

```bash
curl -X POST "http://localhost:8000/execute" \
     -H "Content-Type: application/json" \
     -H "X-THREAD-ID: your-session-id" \
     -d '{"query": "Check availability for Dr. John Doe on 01-08-2025"}'
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Support

For support and questions:
- Check the [API Documentation](http://localhost:8000/docs)
- Review the [Logging Documentation](LOGGING.md)
- Open an issue on GitHub

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Email notifications
- [ ] Calendar integration
- [ ] Payment processing
- [ ] Patient history tracking
- [ ] Doctor profiles and ratings
- [ ] Mobile app development
- [ ] SMS reminders

---

**Built with ❤️ using FastAPI, LangGraph, and Streamlit**