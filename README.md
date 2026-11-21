# 🌱 SmartAgri – Smart Agriculture & IoT Monitoring System

**SmartAgri** is an intelligent agriculture monitoring platform designed to help farmers monitor soil conditions, track water availability, manage crops, and make smarter irrigation decisions using IoT and modern web technologies.

Our goal is to make agriculture smarter, more efficient, and data-driven.

## 🚀 Key Features

- 🌿 **Soil Monitoring:** Monitor soil moisture, temperature, and pH.
- 🧪 **Soil Fertility Monitoring:** Track Nitrogen (N), Phosphorus (P), and Potassium (K) values.
- 💧 **Water Level Monitoring:** Monitor tank water levels using ultrasonic sensors.
- ⚡ **Smart Irrigation:** Automatic irrigation decision-making based on soil moisture and water availability.
- 🎛️ **Manual Irrigation Control:** Support for manual irrigation commands.
- 🌾 **Crop Management:** Add, view, and manage crop information.
- 🔔 **Smart Alerts:** Generate alerts for important sensor conditions.
- 📊 **Live Dashboard:** Visualize sensor readings and irrigation information.
- 📡 **IoT Integration:** Designed to receive sensor data from ESP32 through a Raspberry Pi receiver.

## 🏗️ System Architecture

```text
Sensors
   |
   v
ESP32 Microcontroller
   |
   v
Raspberry Pi 4
   |
   v
FastAPI Backend
   |
   v
PostgreSQL Database
   |
   v
React Dashboard
```

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Frontend | React.js, Vite, CSS |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| IoT Controller | ESP32 |
| Edge Device | Raspberry Pi 4 |
| API Testing | Swagger UI |
| Version Control | Git & GitHub |

## 📁 Project Structure

```text
SmartAgri/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── App.jsx
│   └── package.json
│
├── firmware/
│   ├── esp32/
│   └── raspberry_pi/
│
├── ai/
├── docs/
├── .gitignore
└── README.md
```

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/shadab-404/SmartAgri.git
cd SmartAgri
```

### 2. Backend Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configure your database connection in the backend `.env` file.

Start the backend:

```bash
uvicorn app.main:app --reload --port 8000
```

Backend API:

`http://127.0.0.1:8000`

Swagger Documentation:

`http://127.0.0.1:8000/docs`

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
```

Create a `.env` file:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

Start the frontend:

```bash
npm run dev
```

### 4. IoT Receiver Setup

```bash
cd firmware/raspberry_pi
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn receiver:app --reload --host 0.0.0.0 --port 9000
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/sensors/data` | Submit sensor readings |
| GET | `/api/v1/sensors/latest` | Get latest readings |
| GET | `/api/v1/sensors/history` | Get sensor history |
| POST | `/api/v1/crops/` | Add a crop |
| GET | `/api/v1/crops/` | Get all crops |
| POST | `/api/v1/irrigation/control` | Irrigation control |
| GET | `/api/v1/irrigation/history` | Irrigation history |
| POST | `/api/v1/alerts/check` | Check sensor alerts |
| GET | `/api/v1/alerts/` | Get alerts |

## 🧠 Smart Irrigation Logic

The current backend includes a basic automatic irrigation decision system:

- Soil moisture below 30% → Irrigation ON decision.
- Soil moisture at or above 30% → Irrigation OFF decision.
- Water level below 10% → Irrigation OFF decision for water protection.

*Current automatic irrigation decisions are software-simulated; physical pump control requires completed hardware integration.*

## 🔮 Future Enhancements

- AI-based crop disease detection.
- Crop recommendation using soil parameters.
- Weather-based irrigation prediction.
- Real-time ESP32 sensor integration.
- Physical irrigation controller integration.
- Advanced soil fertility analysis.
- Mobile application for farmers.
- Multi-farm monitoring and analytics.

## 🎯 Project Vision

Our vision is to build an affordable and intelligent agriculture ecosystem that helps farmers make better decisions, reduce unnecessary water usage, and improve agricultural productivity.

## 👨‍💻 Development

**Project:** SmartAgri  
**Category:** Hardware & IoT  
**Repository:** https://github.com/shadab-404/SmartAgri

---

⭐ If you find this project interesting, consider giving the repository a star!

**Built with ❤️ for Smarter Agriculture.**
