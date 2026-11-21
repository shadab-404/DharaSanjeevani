
import { useCallback, useEffect, useState } from "react";

import {
  getLatestSensor,
  getCrops,
  getAlerts,
  getIrrigationHistory,
} from "./services/api";

import {
  createCrop,
  deleteCrop,
} from "./services/cropService";

import "./App.css";

function App() {
  const [sensor, setSensor] = useState(null);
  const [crops, setCrops] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [irrigation, setIrrigation] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Crop form states
  const [cropForm, setCropForm] = useState({
    crop_name: "",
    season: "",
    soil_type: "",
    planting_date: "",
    notes: "",
  });

  const [cropLoading, setCropLoading] = useState(false);
  const [cropMessage, setCropMessage] = useState("");
  const [cropError, setCropError] = useState("");

  // Load dashboard data
  const loadDashboard = useCallback(async () => {
    try {
      const results = await Promise.allSettled([
        getLatestSensor(),
        getCrops(),
        getAlerts(),
        getIrrigationHistory(),
      ]);

      if (results[0].status === "fulfilled") {
        setSensor(results[0].value);
      }

      if (results[1].status === "fulfilled") {
        setCrops(results[1].value);
      }

      if (results[2].status === "fulfilled") {
        setAlerts(results[2].value);
      }

      if (results[3].status === "fulfilled") {
        setIrrigation(results[3].value);
      }

      const allFailed = results.every(
        (result) => result.status === "rejected"
      );

      setError(
        allFailed
          ? "Backend connection failed. Please check your server."
          : ""
      );
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }, []);

  // Initial load and automatic refresh
  useEffect(() => {
    const initialTimer = setTimeout(() => {
      loadDashboard();
    }, 0);

    const refreshTimer = setInterval(() => {
      loadDashboard();
    }, 10000);

    return () => {
      clearTimeout(initialTimer);
      clearInterval(refreshTimer);
    };
  }, [loadDashboard]);

  // Handle crop form changes
  const handleCropChange = (event) => {
    const { name, value } = event.target;

    setCropForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  // Add new crop
  const handleAddCrop = async (event) => {
    event.preventDefault();

    setCropLoading(true);
    setCropMessage("");
    setCropError("");

    try {
      const cropData = {
        ...cropForm,
        planting_date: cropForm.planting_date || null,
        soil_type: cropForm.soil_type || null,
        notes: cropForm.notes || null,
      };

      await createCrop(cropData);

      setCropMessage("Crop added successfully!");

      setCropForm({
        crop_name: "",
        season: "",
        soil_type: "",
        planting_date: "",
        notes: "",
      });

      await loadDashboard();
    } catch (err) {
      setCropError(err.message || "Failed to add crop.");
    } finally {
      setCropLoading(false);
    }
  };

  // Delete crop
  const handleDeleteCrop = async (cropId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this crop?"
    );

    if (!confirmed) return;

    setCropMessage("");
    setCropError("");

    try {
      await deleteCrop(cropId);

      setCropMessage("Crop deleted successfully!");

      await loadDashboard();
    } catch (err) {
      setCropError(err.message || "Failed to delete crop.");
    }
  };

  const latestIrrigation = irrigation[0];

  // Sensor cards
  const metrics = [
    {
      icon: "💧",
      title: "Soil Moisture",
      value: sensor?.soil_moisture,
      unit: "%",
    },
    {
      icon: "🌡️",
      title: "Temperature",
      value: sensor?.soil_temperature,
      unit: "°C",
    },
    {
      icon: "🧪",
      title: "Soil pH",
      value: sensor?.soil_ph,
      unit: "",
    },
    {
      icon: "🚰",
      title: "Water Level",
      value: sensor?.water_level,
      unit: "%",
    },
    {
      icon: "🌿",
      title: "Nitrogen",
      value: sensor?.nitrogen,
      unit: "",
    },
    {
      icon: "🧬",
      title: "Phosphorus",
      value: sensor?.phosphorus,
      unit: "",
    },
    {
      icon: "🌱",
      title: "Potassium",
      value: sensor?.potassium,
      unit: "",
    },
  ];

  return (
    <div className="app-layout">

      {/* Sidebar */}
      <aside className="sidebar">
        <h2 className="brand">🌱 SmartAgri</h2>

        <p className="nav-heading">MENU</p>

        <nav>
          <a href="#dashboard" className="nav-item active">
            ▦ Dashboard
          </a>

          <a href="#crops" className="nav-item">
            🌱 Crop Management
          </a>

          <a href="#irrigation" className="nav-item">
            💧 Irrigation
          </a>

          <a href="#alerts" className="nav-item">
            🔔 Alerts
          </a>

          <a href="#sensors" className="nav-item">
            📊 Sensor Monitoring
          </a>
        </nav>

        <div className="sidebar-footer">
          Smart Agriculture System
          <span>Version 1.0</span>
        </div>
      </aside>

      {/* Main Dashboard */}
      <main className="main-content" id="dashboard">

        {/* Header */}
        <header className="topbar">
          <div>
            <h1>Dashboard Overview</h1>
            <p>Monitor your farm in real time</p>
          </div>

          <button
            className="refresh-btn"
            onClick={loadDashboard}
          >
            ↻ Refresh
          </button>
        </header>

        {error && (
          <p className="error-message">{error}</p>
        )}

        {/* Welcome */}
        <section className="welcome-card">
          <div>
            <span className="welcome-label">
              SMART FARM MONITORING
            </span>

            <h2>Welcome to SmartAgri 🌾</h2>

            <p>
              Manage your crops, soil and irrigation
              from one place.
            </p>
          </div>

          <div className="welcome-icon">🌳</div>
        </section>

        {/* Sensor Monitoring */}
        <section id="sensors">
          <div className="section-heading">
            <h2>Soil & Water Monitoring</h2>

            <span className="live-label">
              ● Live data · Refreshes every 10 sec
            </span>
          </div>

          <div className="metrics-grid">
            {metrics.map((metric, index) => (
              <div className="metric-card" key={index}>
                <div className="metric-top">
                  <span>{metric.title}</span>

                  <span className="metric-icon">
                    {metric.icon}
                  </span>
                </div>

                <h2>
                  {loading
                    ? "..."
                    : metric.value ?? "--"}

                  <small>{metric.unit}</small>
                </h2>
              </div>
            ))}
          </div>

          <p className="muted">
            Last sensor reading:{" "}
            {sensor?.created_at
              ? new Date(sensor.created_at).toLocaleString()
              : "No reading available"}
          </p>
        </section>

        {/* Crop Management */}
        <section className="panel" id="crops">

          <div className="panel-heading">
            <h2>🌱 Crop Management</h2>
            <span>{crops.length} crops</span>
          </div>

          {/* Add Crop Form */}
          <div style={{ marginBottom: "25px" }}>
            <h3 style={{ marginBottom: "15px" }}>
              Add New Crop
            </h3>

            <form onSubmit={handleAddCrop}>

              <div className="crop-form-grid">

                <input
                  type="text"
                  name="crop_name"
                  placeholder="Crop name (e.g. Wheat)"
                  value={cropForm.crop_name}
                  onChange={handleCropChange}
                  required
                  minLength={2}
                  maxLength={100}
                />

                <select
                  name="season"
                  value={cropForm.season}
                  onChange={handleCropChange}
                  required
                >
                  <option value="">Select Season</option>
                  <option value="Kharif">Kharif</option>
                  <option value="Rabi">Rabi</option>
                  <option value="Zaid">Zaid</option>
                  <option value="Summer">Summer</option>
                  <option value="Winter">Winter</option>
                </select>

                <input
                  type="text"
                  name="soil_type"
                  placeholder="Soil type (e.g. Loamy)"
                  value={cropForm.soil_type}
                  onChange={handleCropChange}
                />

                <input
                  type="date"
                  name="planting_date"
                  value={cropForm.planting_date}
                  onChange={handleCropChange}
                />

              </div>

              <textarea
                name="notes"
                placeholder="Additional notes (optional)"
                value={cropForm.notes}
                onChange={handleCropChange}
                rows="3"
                style={{
                  width: "100%",
                  marginTop: "12px",
                  padding: "12px",
                  borderRadius: "8px",
                  border: "1px solid #ddd",
                  fontFamily: "inherit",
                  resize: "vertical",
                }}
              />

              <button
                type="submit"
                disabled={cropLoading}
                className="refresh-btn"
                style={{ marginTop: "12px" }}
              >
                {cropLoading ? "Saving..." : "+ Add Crop"}
              </button>

            </form>

            {cropMessage && (
              <p style={{ color: "green", marginTop: "12px" }}>
                {cropMessage}
              </p>
            )}

            {cropError && (
              <p style={{ color: "red", marginTop: "12px" }}>
                {cropError}
              </p>
            )}
          </div>

          <hr style={{ margin: "20px 0", border: "0", borderTop: "1px solid #eee" }} />

          {/* Crop List */}
          <h3 style={{ marginBottom: "12px" }}>
            Your Crops
          </h3>

          {crops.length === 0 ? (
            <p className="empty-state">
              No crops added yet.
            </p>
          ) : (
            crops.map((crop) => (
              <div
                className="list-item"
                key={crop.id}
              >
                <div>
                  <strong>{crop.crop_name}</strong>

                  <p>
                    {crop.soil_type || "Soil not specified"}
                  </p>

                  {crop.planting_date && (
                    <p>
                      Planted: {crop.planting_date}
                    </p>
                  )}
                </div>

                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "10px",
                  }}
                >
                  <span className="tag">
                    {crop.season}
                  </span>

                  <button
                    onClick={() => handleDeleteCrop(crop.id)}
                    style={{
                      background: "#fee2e2",
                      color: "#b91c1c",
                      border: "none",
                      padding: "8px 12px",
                      borderRadius: "6px",
                      cursor: "pointer",
                    }}
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))
          )}

        </section>

        {/* Irrigation */}
        <section className="panel" id="irrigation">

          <div className="panel-heading">
            <h2>💧 Irrigation Status</h2>
          </div>

          <div className="pump-status">
            <span className="pump-icon">🚿</span>

            <div>
              <strong>
                {latestIrrigation
                  ? latestIrrigation.pump_status
                    ? "Pump ON"
                    : "Pump OFF"
                  : "No records"}
              </strong>

              <p>
                Mode: {latestIrrigation?.mode || "--"}
              </p>
            </div>
          </div>

          <p className="muted">
            Latest irrigation record from database.
          </p>

        </section>

        {/* Alerts */}
        <section
          className="panel alerts-panel"
          id="alerts"
        >

          <div className="panel-heading">
            <h2>🔔 Recent Alerts</h2>

            <span>
              {alerts.filter(
                (alert) => !alert.is_resolved
              ).length} unresolved
            </span>
          </div>

          {alerts.length === 0 ? (
            <p className="empty-state">
              No alerts available.
            </p>
          ) : (
            alerts.slice(0, 5).map((alert) => (
              <div className="list-item" key={alert.id}>
                <div>
                  <strong>{alert.title}</strong>
                  <p>{alert.message}</p>
                </div>

                <span className={`tag ${alert.severity}`}>
                  {alert.severity}
                </span>
              </div>
            ))
          )}

        </section>

        {/* Irrigation History */}
        <section className="panel">

          <div className="panel-heading">
            <h2>📋 Recent Irrigation History</h2>
            <span>{irrigation.length} records</span>
          </div>

          {irrigation.slice(0, 5).map((item) => (
            <div className="list-item" key={item.id}>
              <div>
                <strong>
                  Pump {item.pump_status ? "ON" : "OFF"}
                </strong>

                <p>Mode: {item.mode}</p>
              </div>

              <span className="tag">
                Record #{item.id}
              </span>
            </div>
          ))}

          {irrigation.length === 0 && (
            <p className="empty-state">
              No irrigation history available.
            </p>
          )}

        </section>

        <footer className="footer">
          SmartAgri © 2026 · Smart Agriculture Monitoring
        </footer>

      </main>
    </div>
  );
}

export default App;

