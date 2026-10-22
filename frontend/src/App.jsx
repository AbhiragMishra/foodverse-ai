import React, { useState, useEffect, useRef } from 'react';

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

// Helper: Generates a real synthetic image Blob using HTML5 Canvas
function createSyntheticImageBlob(type = "food") {
  const canvas = document.createElement("canvas");
  canvas.width = 300;
  canvas.height = 300;
  const ctx = canvas.getContext("2d");

  if (type === "fresh_apple") {
    ctx.fillStyle = "#166534";
    ctx.fillRect(0, 0, 300, 300);
    // Draw crisp green apple
    ctx.beginPath();
    ctx.arc(150, 160, 90, 0, Math.PI * 2);
    ctx.fillStyle = "#22c55e";
    ctx.fill();
    // Stem
    ctx.fillStyle = "#78350f";
    ctx.fillRect(145, 50, 10, 30);
  } else if (type === "spoiled_banana") {
    ctx.fillStyle = "#1e293b";
    ctx.fillRect(0, 0, 300, 300);
    // Draw brown decayed banana with spots
    ctx.beginPath();
    ctx.arc(150, 150, 85, 0, Math.PI * 2);
    ctx.fillStyle = "#713f12";
    ctx.fill();
    // Dark decay spots
    ctx.fillStyle = "#1c1917";
    ctx.beginPath(); ctx.arc(130, 130, 18, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(175, 170, 24, 0, Math.PI * 2); ctx.fill();
  } else {
    // Balanced colorful meal plate
    ctx.fillStyle = "#0f172a";
    ctx.fillRect(0, 0, 300, 300);
    ctx.beginPath();
    ctx.arc(150, 150, 110, 0, Math.PI * 2);
    ctx.fillStyle = "#e2e8f0";
    ctx.fill();
    // Rice
    ctx.beginPath(); ctx.arc(120, 140, 45, 0, Math.PI * 2); ctx.fillStyle = "#fef08a"; ctx.fill();
    // Greens
    ctx.beginPath(); ctx.arc(170, 120, 40, 0, Math.PI * 2); ctx.fillStyle = "#16a34a"; ctx.fill();
    // Protein
    ctx.beginPath(); ctx.arc(160, 180, 45, 0, Math.PI * 2); ctx.fillStyle = "#b45309"; ctx.fill();
  }

  return new Promise((resolve) => {
    canvas.toBlob((blob) => {
      resolve(new File([blob], `${type}.jpg`, { type: "image/jpeg" }));
    }, "image/jpeg");
  });
}

export default function App() {
  const [activeTab, setActiveTab] = useState("recognition");
  const [apiStatus, setApiStatus] = useState({ online: false, latency: null });

  // Real API ping on load
  useEffect(() => {
    const t0 = performance.now();
    fetch(`${API_BASE}/`)
      .then(r => r.json())
      .then(data => {
        const t1 = performance.now();
        setApiStatus({ online: data.status === "active", latency: Math.round(t1 - t0) });
      })
      .catch(() => setApiStatus({ online: false, latency: null }));
  }, []);

  const tabs = [
    { id: "recognition", label: "Food & Nutrition Scanner", icon: "📸" },
    { id: "freshness", label: "Freshness & Spoilage Inspector", icon: "🔬" },
    { id: "hygiene", label: "Kitchen Hygiene Auditor", icon: "🛡️" },
    { id: "kitchen", label: "Smart Cooking Assistant", icon: "👨‍🍳" },
    { id: "planner", label: "Precision Meal Planner", icon: "🥗" }
  ];

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Studio Header Bar */}
      <header style={{
        background: 'var(--bg-surface)',
        borderBottom: '1px solid var(--border-subtle)',
        padding: '16px 32px',
        position: 'sticky',
        top: 0,
        zIndex: 50
      }}>
        <div style={{ maxWidth: 1400, margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          {/* Logo & Identity */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
            <div style={{
              width: 36, height: 36, borderRadius: 8,
              background: 'linear-gradient(135deg, #10b981, #06b6d4)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: 18, fontWeight: 'bold', color: '#022c22'
            }}>
              🥑
            </div>
            <div>
              <div style={{ fontSize: '1.2rem', fontWeight: 800, color: 'var(--text-main)', letterSpacing: '-0.02em' }}>
                FoodVerse AI <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--emerald)', background: 'var(--emerald-subtle)', padding: '2px 8px', borderRadius: 4, marginLeft: 6 }}>STUDIO v2.0</span>
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>
                Multimodal Sensory Vision • Biochemical Spoilage • Contextual Meal Intelligence
              </div>
            </div>
          </div>

          {/* Real API Status Telemetry */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            <div style={{
              display: 'flex', alignItems: 'center', gap: 8,
              background: 'var(--bg-input)', padding: '6px 14px', borderRadius: 8,
              border: '1px solid var(--border-subtle)'
            }}>
              <span className="pulse-dot" style={{ background: apiStatus.online ? 'var(--emerald)' : 'var(--crimson)' }} />
              <span style={{ fontSize: '0.8rem', fontWeight: 700, color: apiStatus.online ? '#34d399' : '#f87171' }}>
                {apiStatus.online ? `API Live (${apiStatus.latency}ms)` : "API Offline"}
              </span>
            </div>
            <a
              href={`${API_BASE}/docs`}
              target="_blank"
              rel="noreferrer"
              style={{ fontSize: '0.8rem', color: 'var(--cyan)', textDecoration: 'none', fontWeight: 600 }}
            >
              Swagger Docs ↗
            </a>
          </div>
        </div>

        {/* Tab Selection Navigation */}
        <div style={{ maxWidth: 1400, margin: '14px auto 0', display: 'flex', gap: 8, overflowX: 'auto', paddingBottom: 4 }}>
          {tabs.map(tab => {
            const active = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  display: 'flex', alignItems: 'center', gap: 8,
                  padding: '9px 16px', borderRadius: 8,
                  fontSize: '0.85rem', fontWeight: active ? 700 : 500,
                  color: active ? '#f8fafc' : 'var(--text-muted)',
                  background: active ? 'var(--bg-surface-elevated)' : 'transparent',
                  border: active ? '1px solid var(--emerald)' : '1px solid transparent',
                  whiteSpace: 'nowrap'
                }}
              >
                <span>{tab.icon}</span>
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </header>

      {/* Main Testing Workbench */}
      <main style={{ flex: 1, maxWidth: 1400, margin: '0 auto', width: '100%', padding: '28px 32px' }}>
        {activeTab === "recognition" && <FoodRecognitionWorkbench />}
        {activeTab === "freshness" && <FreshnessWorkbench />}
        {activeTab === "hygiene" && <HygieneWorkbench />}
        {activeTab === "kitchen" && <KitchenWorkbench />}
        {activeTab === "planner" && <PlannerWorkbench />}
      </main>
    </div>
  );
}

// =========================================================================
// MODULE 1: FOOD RECOGNITION & NUTRITION WORKBENCH
// =========================================================================
function FoodRecognitionWorkbench() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [textContext, setTextContext] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [apiLatency, setApiLatency] = useState(null);
  const mediaRecorderRef = useRef(null);

  const handleFileChange = (e) => {
    const f = e.target.files[0];
    if (f) {
      setFile(f);
      setPreviewUrl(URL.createObjectURL(f));
    }
  };

  // Quick generator for testing without an external file
  const handleLoadTestMeal = async () => {
    const testFile = await createSyntheticImageBlob("meal_plate");
    setFile(testFile);
    setPreviewUrl(URL.createObjectURL(testFile));
    setTextContext("Steamed Jasmine Rice with Stir-Fried Chicken and Broccoli");
  };

  // Real microphone audio recording
  const toggleRecording = async () => {
    if (isRecording) {
      if (mediaRecorderRef.current) {
        mediaRecorderRef.current.stop();
        setIsRecording(false);
      }
    } else {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const recorder = new MediaRecorder(stream);
        const chunks = [];
        recorder.ondataavailable = e => chunks.push(e.data);
        recorder.onstop = () => {
          const blob = new Blob(chunks, { type: 'audio/wav' });
          setAudioBlob(blob);
        };
        recorder.start();
        mediaRecorderRef.current = recorder;
        setIsRecording(true);
      } catch (err) {
        alert("Microphone permission denied or unsupported in browser: " + err.message);
      }
    }
  };

  // Real API call to FastAPI backend
  const handleRunAnalysis = async (e) => {
    e.preventDefault();
    if (!file && !textContext.trim()) {
      alert("Please upload an image or provide text description to test the API.");
      return;
    }

    setLoading(true);
    setResponse(null);
    const t0 = performance.now();

    const formData = new FormData();
    if (file) formData.append("file", file);
    if (textContext.trim()) formData.append("text_context", textContext.trim());
    if (audioBlob) formData.append("audio_file", audioBlob, "voice_note.wav");

    try {
      const res = await fetch(`${API_BASE}/api/food-recognition/analyze`, {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      const t1 = performance.now();
      setApiLatency(Math.round(t1 - t0));
      setResponse({ status: res.status, data });
    } catch (err) {
      alert("API request failed: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="workbench-grid">
      {/* Left Input Panel */}
      <div className="panel">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f8fafc' }}>Input Parameters</h3>
          <button onClick={handleLoadTestMeal} className="btn-secondary" style={{ fontSize: '0.75rem', padding: '6px 12px' }}>
            ⚡ Load Test Meal Plate
          </button>
        </div>

        <form onSubmit={handleRunAnalysis}>
          {/* File Upload / Dropzone */}
          <div style={{ marginBottom: 18 }}>
            <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 6 }}>
              Meal Photo (Required or use Test Plate)
            </label>
            <div
              className="dropzone"
              onClick={() => document.getElementById("meal-file-input").click()}
            >
              {previewUrl ? (
                <div style={{ textAlign: 'center' }}>
                  <img src={previewUrl} alt="Upload preview" style={{ maxWidth: '100%', maxHeight: 180, borderRadius: 8, objectFit: 'contain' }} />
                  <p style={{ fontSize: '0.75rem', color: 'var(--emerald)', marginTop: 8 }}>Click to change photo ({file ? file.name : "Generated Plate"})</p>
                </div>
              ) : (
                <div>
                  <div style={{ fontSize: 28, marginBottom: 8 }}>📤</div>
                  <p style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-main)' }}>Click to select or drop food image</p>
                  <p style={{ fontSize: '0.72rem', color: 'var(--text-dim)', marginTop: 4 }}>Supports JPG, PNG, WebP</p>
                </div>
              )}
              <input id="meal-file-input" type="file" accept="image/*" onChange={handleFileChange} style={{ display: 'none' }} />
            </div>
          </div>

          {/* Text Context */}
          <div style={{ marginBottom: 18 }}>
            <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 6 }}>
              Dish Description or User Query
            </label>
            <input
              type="text"
              value={textContext}
              onChange={e => setTextContext(e.target.value)}
              placeholder="e.g. 200g grilled salmon with quinoa and steamed asparagus"
              style={{ width: '100%' }}
            />
          </div>

          {/* Voice Input Recorder */}
          <div style={{ marginBottom: 22, background: 'var(--bg-input)', padding: 12, borderRadius: 8, border: '1px solid var(--border-subtle)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div>
              <div style={{ fontSize: '0.8rem', fontWeight: 600, color: '#f8fafc' }}>Voice Note Recording</div>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>
                {audioBlob ? "✓ Voice note captured" : "Optional hands-free context"}
              </div>
            </div>
            <button
              type="button"
              onClick={toggleRecording}
              style={{
                padding: '8px 14px', borderRadius: 6, fontSize: '0.78rem', fontWeight: 700,
                background: isRecording ? 'var(--crimson)' : (audioBlob ? 'var(--emerald)' : 'var(--bg-surface-elevated)'),
                color: isRecording || audioBlob ? '#fff' : 'var(--text-main)',
                border: '1px solid var(--border-subtle)'
              }}
            >
              {isRecording ? "⏹️ Stop" : (audioBlob ? "🎙️ Re-record" : "🎙️ Record Mic")}
            </button>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-primary"
            style={{ width: '100%', fontSize: '0.95rem' }}
          >
            {loading ? "Calling /api/food-recognition/analyze..." : "Execute Multimodal Analysis"}
          </button>
        </form>
      </div>

      {/* Right Output Console */}
      <div className="panel">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f8fafc' }}>Live Analysis Console</h3>
          {apiLatency && (
            <span className="badge badge-emerald">
              HTTP {response?.status} • {apiLatency}ms
            </span>
          )}
        </div>

        {loading && (
          <div style={{ padding: 40, textAlign: 'center' }}>
            <div className="pulse-dot" style={{ width: 16, height: 16, background: 'var(--emerald)' }} />
            <p style={{ marginTop: 12, fontSize: '0.88rem', color: 'var(--text-muted)' }}>
              Executing backend computer vision pipeline & nutrition inference...
            </p>
          </div>
        )}

        {!loading && !response && (
          <div style={{ padding: 48, textAlign: 'center', color: 'var(--text-dim)' }}>
            <div style={{ fontSize: 36, marginBottom: 10 }}>🥗</div>
            <p style={{ fontWeight: 600, color: 'var(--text-muted)' }}>Awaiting Input</p>
            <p style={{ fontSize: '0.8rem', marginTop: 4 }}>
              Upload a meal photo or click "Load Test Meal Plate" on the left, then click Execute to test live API processing.
            </p>
          </div>
        )}

        {response && response.data && (
          <div>
            {/* Header info */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', paddingBottom: 16, borderBottom: '1px solid var(--border-subtle)' }}>
              <div>
                <span className="badge badge-cyan">{response.data.health_rating}</span>
                <h4 style={{ fontSize: '1.4rem', fontWeight: 800, color: '#f8fafc', marginTop: 6 }}>
                  {response.data.dish_name}
                </h4>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--emerald)' }}>
                  {response.data.health_score}<span style={{ fontSize: '0.9rem', color: 'var(--text-dim)' }}>/100</span>
                </div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', fontWeight: 600, textTransform: 'uppercase' }}>Health Score</div>
              </div>
            </div>

            {/* Macronutrient breakdown */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 10, margin: '20px 0' }}>
              <div style={{ background: 'var(--bg-input)', padding: 12, borderRadius: 8, border: '1px solid var(--border-subtle)' }}>
                <div style={{ fontSize: '1.25rem', fontWeight: 800, color: '#f59e0b' }}>{response.data.nutrition.calories}</div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)', fontWeight: 700 }}>CALORIES (KCAL)</div>
              </div>
              <div style={{ background: 'var(--bg-input)', padding: 12, borderRadius: 8, border: '1px solid var(--border-subtle)' }}>
                <div style={{ fontSize: '1.25rem', fontWeight: 800, color: '#06b6d4' }}>{response.data.nutrition.protein}g</div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)', fontWeight: 700 }}>PROTEIN</div>
              </div>
              <div style={{ background: 'var(--bg-input)', padding: 12, borderRadius: 8, border: '1px solid var(--border-subtle)' }}>
                <div style={{ fontSize: '1.25rem', fontWeight: 800, color: '#10b981' }}>{response.data.nutrition.carbs}g</div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)', fontWeight: 700 }}>CARBOHYDRATES</div>
              </div>
              <div style={{ background: 'var(--bg-input)', padding: 12, borderRadius: 8, border: '1px solid var(--border-subtle)' }}>
                <div style={{ fontSize: '1.25rem', fontWeight: 800, color: '#ef4444' }}>{response.data.nutrition.fats}g</div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)', fontWeight: 700 }}>FATS</div>
              </div>
              <div style={{ background: 'var(--bg-input)', padding: 12, borderRadius: 8, border: '1px solid var(--border-subtle)' }}>
                <div style={{ fontSize: '1.25rem', fontWeight: 800, color: '#10b981' }}>{response.data.nutrition.fiber}g</div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)', fontWeight: 700 }}>DIETARY FIBER</div>
              </div>
              <div style={{ background: 'var(--bg-input)', padding: 12, borderRadius: 8, border: '1px solid var(--border-subtle)' }}>
                <div style={{ fontSize: '1.25rem', fontWeight: 800, color: '#f59e0b' }}>{response.data.nutrition.sugar}g</div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)', fontWeight: 700 }}>SUGARS</div>
              </div>
            </div>

            {/* Insights & Recommendations */}
            <div style={{ marginBottom: 14 }}>
              <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: 6 }}>
                Dietary Insights & Safeguards
              </div>
              <ul style={{ paddingLeft: 18, fontSize: '0.85rem', color: '#cbd5e1', lineHeight: 1.6 }}>
                {response.data.dietary_insights?.map((ins, i) => <li key={i}>{ins}</li>)}
              </ul>
            </div>

            <div style={{ padding: 12, background: 'var(--bg-input)', borderRadius: 8, border: '1px solid var(--border-subtle)', fontSize: '0.82rem', color: '#94a3b8' }}>
              💡 <strong>Recommendation:</strong> {response.data.recommendations}
            </div>

            {/* Raw JSON Debug Viewer */}
            <details style={{ marginTop: 16 }}>
              <summary style={{ fontSize: '0.75rem', color: 'var(--text-dim)', cursor: 'pointer' }}>
                View Raw API JSON Payload
              </summary>
              <pre style={{
                marginTop: 8, padding: 12, background: '#070b12',
                borderRadius: 6, fontSize: '0.72rem', color: '#38bdf8',
                fontFamily: 'var(--font-mono)', overflowX: 'auto'
              }}>
                {JSON.stringify(response.data, null, 2)}
              </pre>
            </details>
          </div>
        )}
      </div>
    </div>
  );
}

// =========================================================================
// MODULE 2: FRESHNESS & SPOILAGE INSPECTOR WORKBENCH
// =========================================================================
function FreshnessWorkbench() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [foodType, setFoodType] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [apiLatency, setApiLatency] = useState(null);

  const handleSelectSample = async (type) => {
    const f = await createSyntheticImageBlob(type);
    setFile(f);
    setPreviewUrl(URL.createObjectURL(f));
    setFoodType(type === "fresh_apple" ? "Crisp Green Apple" : "Overripe Decayed Banana");
  };

  const handleInspect = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please upload a produce photo or click one of the synthetic test presets.");
      return;
    }

    setLoading(true);
    setResponse(null);
    const t0 = performance.now();

    const formData = new FormData();
    formData.append("file", file);
    if (foodType.trim()) formData.append("food_type", foodType.trim());

    try {
      const res = await fetch(`${API_BASE}/api/freshness-detector/analyze`, {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      const t1 = performance.now();
      setApiLatency(Math.round(t1 - t0));
      setResponse({ status: res.status, data });
    } catch (err) {
      alert("Freshness API call failed: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="workbench-grid">
      {/* Left Input Panel */}
      <div className="panel">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f8fafc' }}>Produce Inspection Form</h3>
        </div>

        {/* Quick Test Presets */}
        <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
          <button
            type="button"
            onClick={() => handleSelectSample("fresh_apple")}
            className="btn-secondary"
            style={{ fontSize: '0.75rem', padding: '6px 12px', flex: 1, color: '#34d399' }}
          >
            🍏 Generate Fresh Apple
          </button>
          <button
            type="button"
            onClick={() => handleSelectSample("spoiled_banana")}
            className="btn-secondary"
            style={{ fontSize: '0.75rem', padding: '6px 12px', flex: 1, color: '#f87171' }}
          >
            🍌 Generate Spoiled Fruit
          </button>
        </div>

        <form onSubmit={handleInspect}>
          {/* File Upload / Dropzone */}
          <div style={{ marginBottom: 16 }}>
            <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 6 }}>
              Visual Check Photo
            </label>
            <div
              className="dropzone"
              onClick={() => document.getElementById("freshness-file-input").click()}
            >
              {previewUrl ? (
                <div style={{ textAlign: 'center' }}>
                  <img src={previewUrl} alt="Inspection" style={{ maxWidth: '100%', maxHeight: 180, borderRadius: 8, objectFit: 'contain' }} />
                  <p style={{ fontSize: '0.75rem', color: 'var(--emerald)', marginTop: 8 }}>Click to change image</p>
                </div>
              ) : (
                <div>
                  <div style={{ fontSize: 28, marginBottom: 8 }}>🔬</div>
                  <p style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-main)' }}>Upload produce image for OpenCV scan</p>
                  <p style={{ fontSize: '0.72rem', color: 'var(--text-dim)', marginTop: 4 }}>Analyzes browning indices & texture degradation</p>
                </div>
              )}
              <input
                id="freshness-file-input"
                type="file"
                accept="image/*"
                onChange={e => {
                  const f = e.target.files[0];
                  if (f) {
                    setFile(f);
                    setPreviewUrl(URL.createObjectURL(f));
                  }
                }}
                style={{ display: 'none' }}
              />
            </div>
          </div>

          <div style={{ marginBottom: 20 }}>
            <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 6 }}>
              Produce Category / Description
            </label>
            <input
              type="text"
              value={foodType}
              onChange={e => setFoodType(e.target.value)}
              placeholder="e.g. Fuji Apple, Ripe Banana, Baby Spinach"
              style={{ width: '100%' }}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-primary"
            style={{ width: '100%', fontSize: '0.95rem' }}
          >
            {loading ? "Running Computer Vision & Spoilage Check..." : "Run Freshness Inspection"}
          </button>
        </form>
      </div>

      {/* Right Console Output */}
      <div className="panel">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f8fafc' }}>Freshness & Spoilage Output</h3>
          {apiLatency && (
            <span className="badge badge-emerald">
              HTTP {response?.status} • {apiLatency}ms
            </span>
          )}
        </div>

        {loading && (
          <div style={{ padding: 40, textAlign: 'center' }}>
            <div className="pulse-dot" style={{ width: 16, height: 16, background: 'var(--amber)' }} />
            <p style={{ marginTop: 12, fontSize: '0.88rem', color: 'var(--text-muted)' }}>
              Extracting HSV discoloration metrics, noise filtering & Laplacian texture variance...
            </p>
          </div>
        )}

        {!loading && !response && (
          <div style={{ padding: 48, textAlign: 'center', color: 'var(--text-dim)' }}>
            <div style={{ fontSize: 36, marginBottom: 10 }}>🍏</div>
            <p style={{ fontWeight: 600, color: 'var(--text-muted)' }}>Ready for Freshness Inspection</p>
            <p style={{ fontSize: '0.8rem', marginTop: 4 }}>
              Upload an image or generate a sample above to test OpenCV feature extraction and safety classification.
            </p>
          </div>
        )}

        {response && response.data && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingBottom: 16, borderBottom: '1px solid var(--border-subtle)' }}>
              <div>
                <span className={`badge ${response.data.freshness_status === 'Fresh' ? 'badge-emerald' : (response.data.freshness_status === 'Expiring Soon' ? 'badge-amber' : 'badge-crimson')}`}>
                  {response.data.freshness_status}
                </span>
                <h4 style={{ fontSize: '1.4rem', fontWeight: 800, color: '#f8fafc', marginTop: 6 }}>
                  {response.data.food_item}
                </h4>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '1.8rem', fontWeight: 800, color: response.data.freshness_score >= 70 ? 'var(--emerald)' : (response.data.freshness_score >= 40 ? 'var(--amber)' : 'var(--crimson)') }}>
                  {response.data.freshness_score}<span style={{ fontSize: '0.9rem', color: 'var(--text-dim)' }}>/100</span>
                </div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', fontWeight: 600, textTransform: 'uppercase' }}>Freshness Index</div>
              </div>
            </div>

            {/* OpenCV Features Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 10, margin: '18px 0' }}>
              <div style={{ background: 'var(--bg-input)', padding: 12, borderRadius: 8, border: '1px solid var(--border-subtle)' }}>
                <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#38bdf8' }}>{response.data.shelf_life_days} Days</div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', fontWeight: 700 }}>ESTIMATED SHELF LIFE</div>
              </div>
              <div style={{ background: 'var(--bg-input)', padding: 12, borderRadius: 8, border: '1px solid var(--border-subtle)' }}>
                <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#f8fafc' }}>{Math.round(response.data.visual_features.discoloration_index * 100)}%</div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', fontWeight: 700 }}>DISCOLORATION RATIO</div>
              </div>
              <div style={{ background: 'var(--bg-input)', padding: 12, borderRadius: 8, border: '1px solid var(--border-subtle)' }}>
                <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#f8fafc' }}>{Math.round(response.data.visual_features.surface_texture_roughness * 100)}%</div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', fontWeight: 700 }}>SURFACE ROUGHNESS</div>
              </div>
            </div>

            {/* Safety Verdict */}
            <div style={{
              padding: 14, borderRadius: 8, marginBottom: 14,
              background: response.data.freshness_status === 'Fresh' ? 'var(--emerald-subtle)' : (response.data.freshness_status === 'Expiring Soon' ? 'var(--amber-subtle)' : 'var(--crimson-subtle)'),
              border: `1px solid ${response.data.freshness_status === 'Fresh' ? 'rgba(16, 185, 129, 0.3)' : (response.data.freshness_status === 'Expiring Soon' ? 'rgba(245, 158, 11, 0.3)' : 'rgba(239, 68, 68, 0.3)')}`
            }}>
              <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-main)', textTransform: 'uppercase' }}>Safety Verdict</div>
              <p style={{ fontSize: '0.88rem', color: '#f8fafc', marginTop: 4, fontWeight: 600 }}>{response.data.safety_verdict}</p>
            </div>

            {/* Storage Advice */}
            <div style={{ fontSize: '0.84rem', color: '#cbd5e1', marginBottom: 12 }}>
              📦 <strong>Storage:</strong> {response.data.storage_recommendations}
            </div>

            {/* Zero Waste Tip */}
            <div style={{ fontSize: '0.84rem', color: '#34d399', background: 'var(--bg-input)', padding: 10, borderRadius: 6, border: '1px solid var(--border-subtle)' }}>
              ♻️ <strong>Zero-Waste Tip:</strong> {response.data.waste_reduction_tips}
            </div>

            {/* Raw JSON Debug Viewer */}
            <details style={{ marginTop: 16 }}>
              <summary style={{ fontSize: '0.75rem', color: 'var(--text-dim)', cursor: 'pointer' }}>
                View Raw API JSON Payload
              </summary>
              <pre style={{
                marginTop: 8, padding: 12, background: '#070b12',
                borderRadius: 6, fontSize: '0.72rem', color: '#38bdf8',
                fontFamily: 'var(--font-mono)', overflowX: 'auto'
              }}>
                {JSON.stringify(response.data, null, 2)}
              </pre>
            </details>
          </div>
        )}
      </div>
    </div>
  );
}

// =========================================================================
// MODULE 3: HYGIENE & SAFETY AUDITOR WORKBENCH
// =========================================================================
function HygieneWorkbench() {
  const [file, setFile] = useState(null);
  const [areaName, setAreaName] = useState("Commercial Prep Station 1");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [apiLatency, setApiLatency] = useState(null);

  const handleAudit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponse(null);
    const t0 = performance.now();

    // If user didn't pick a file, generate test kitchen image
    const auditFile = file || await createSyntheticImageBlob("fresh_apple");

    const formData = new FormData();
    formData.append("file", auditFile);
    formData.append("area_name", areaName);

    try {
      const res = await fetch(`${API_BASE}/api/hygiene-monitor/audit`, {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      const t1 = performance.now();
      setApiLatency(Math.round(t1 - t0));
      setResponse({ status: res.status, data });
    } catch (err) {
      alert("Hygiene API failed: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="workbench-grid">
      <div className="panel">
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f8fafc', marginBottom: 16 }}>Kitchen Footage Ingestion</h3>
        <form onSubmit={handleAudit}>
          <div style={{ marginBottom: 16 }}>
            <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 6 }}>
              Video Footage (.mp4) or Snapshot (.jpg)
            </label>
            <input
              type="file"
              accept="image/*,video/*"
              onChange={e => setFile(e.target.files[0])}
              style={{ width: '100%', padding: 10 }}
            />
            <p style={{ fontSize: '0.72rem', color: 'var(--text-dim)', marginTop: 4 }}>
              {file ? `Selected: ${file.name}` : "Leave blank to auto-generate a sample kitchen frame."}
            </p>
          </div>

          <div style={{ marginBottom: 20 }}>
            <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 6 }}>
              Facility Zone
            </label>
            <input
              type="text"
              value={areaName}
              onChange={e => setAreaName(e.target.value)}
              style={{ width: '100%' }}
            />
          </div>

          <button type="submit" disabled={loading} className="btn-primary" style={{ width: '100%' }}>
            {loading ? "Extracting Frames & Auditing..." : "Execute Hygiene Audit"}
          </button>
        </form>
      </div>

      <div className="panel">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f8fafc' }}>Hygiene Scorecard</h3>
          {apiLatency && (
            <span className="badge badge-emerald">
              HTTP {response?.status} • {apiLatency}ms
            </span>
          )}
        </div>

        {!loading && !response && (
          <div style={{ padding: 48, textAlign: 'center', color: 'var(--text-dim)' }}>
            <div style={{ fontSize: 36, marginBottom: 10 }}>🛡️</div>
            <p style={{ fontWeight: 600, color: 'var(--text-muted)' }}>Ready for Safety Audit</p>
            <p style={{ fontSize: '0.8rem', marginTop: 4 }}>
              Click Execute to ingest frames and evaluate PPE, glove usage, and sanitization levels.
            </p>
          </div>
        )}

        {response && response.data && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingBottom: 16, borderBottom: '1px solid var(--border-subtle)' }}>
              <div>
                <span className="badge badge-emerald">{response.data.compliance_grade}</span>
                <h4 style={{ fontSize: '1.3rem', fontWeight: 800, color: '#f8fafc', marginTop: 6 }}>
                  {response.data.facility_area}
                </h4>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--emerald)' }}>
                  {response.data.compliance_score}<span style={{ fontSize: '0.9rem', color: 'var(--text-dim)' }}>/100</span>
                </div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', fontWeight: 600, textTransform: 'uppercase' }}>Compliance</div>
              </div>
            </div>

            <div style={{ margin: '16px 0' }}>
              <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: 8 }}>
                Checklist Results ({response.data.indicators?.length} Indicators)
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                {response.data.indicators?.map((ind, i) => (
                  <div key={i} style={{ background: 'var(--bg-input)', padding: 10, borderRadius: 8, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <div style={{ fontSize: '0.85rem', fontWeight: 700, color: '#f8fafc' }}>{ind.indicator_name}</div>
                      <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>{ind.details}</div>
                    </div>
                    <span className="badge badge-emerald">✓ {ind.status}</span>
                  </div>
                ))}
              </div>
            </div>

            <div style={{ padding: 12, background: 'var(--bg-input)', borderRadius: 8, fontSize: '0.82rem', color: '#94a3b8' }}>
              📋 <strong>Audit Summary:</strong> {response.data.audit_summary}
            </div>

            {/* Raw JSON Debug Viewer */}
            <details style={{ marginTop: 16 }}>
              <summary style={{ fontSize: '0.75rem', color: 'var(--text-dim)', cursor: 'pointer' }}>
                View Raw API JSON Payload
              </summary>
              <pre style={{
                marginTop: 8, padding: 12, background: '#070b12',
                borderRadius: 6, fontSize: '0.72rem', color: '#38bdf8',
                fontFamily: 'var(--font-mono)', overflowX: 'auto'
              }}>
                {JSON.stringify(response.data, null, 2)}
              </pre>
            </details>
          </div>
        )}
      </div>
    </div>
  );
}

// =========================================================================
// MODULE 4: SMART COOKING ASSISTANT WORKBENCH
// =========================================================================
function KitchenWorkbench() {
  const [ingredients, setIngredients] = useState("Chicken breast, garlic, olive oil, baby spinach, cherry tomatoes");
  const [skill, setSkill] = useState("Beginner");
  const [loading, setLoading] = useState(false);
  const [recipe, setRecipe] = useState(null);

  const [chatQ, setChatQ] = useState("");
  const [chatA, setChatA] = useState(null);
  const [asking, setAsking] = useState(false);

  const handleGenerateRecipe = async (e) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData();
    formData.append("ingredients", ingredients);
    formData.append("skill_level", skill);

    try {
      const res = await fetch(`${API_BASE}/api/kitchen-assistant/generate-recipe`, {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      setRecipe(data);
    } catch (err) {
      alert("Recipe generation failed: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAskAssistant = async (e) => {
    e.preventDefault();
    if (!chatQ.trim()) return;
    setAsking(true);
    try {
      const res = await fetch(`${API_BASE}/api/kitchen-assistant/ask-assistant`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: chatQ })
      });
      const data = await res.json();
      setChatA(data);
    } catch (err) {
      alert("Assistant chat failed: " + err.message);
    } finally {
      setAsking(false);
    }
  };

  return (
    <div className="workbench-grid">
      <div style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>
        <div className="panel">
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f8fafc', marginBottom: 14 }}>Recipe Generator</h3>
          <form onSubmit={handleGenerateRecipe}>
            <div style={{ marginBottom: 14 }}>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 6 }}>
                Ingredients You Have
              </label>
              <textarea
                rows={3}
                value={ingredients}
                onChange={e => setIngredients(e.target.value)}
                style={{ width: '100%' }}
              />
            </div>

            <div style={{ marginBottom: 16 }}>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 6 }}>
                Target Skill Level
              </label>
              <select value={skill} onChange={e => setSkill(e.target.value)} style={{ width: '100%' }}>
                <option value="Beginner">Beginner (Simple steps, quick)</option>
                <option value="Intermediate">Intermediate (Flavor layering)</option>
                <option value="Advanced">Advanced (Chef techniques)</option>
              </select>
            </div>

            <button type="submit" disabled={loading} className="btn-primary" style={{ width: '100%' }}>
              {loading ? "Generating Procedural Steps..." : "Generate Custom Recipe"}
            </button>
          </form>
        </div>

        {/* Live Q&A Box */}
        <div className="panel">
          <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#f8fafc', marginBottom: 10 }}>Hands-Free Chef Q&A</h3>
          <form onSubmit={handleAskAssistant} style={{ display: 'flex', gap: 8 }}>
            <input
              type="text"
              placeholder="e.g. Can I use butter instead of olive oil?"
              value={chatQ}
              onChange={e => setChatQ(e.target.value)}
              style={{ flex: 1 }}
            />
            <button type="submit" disabled={asking} className="btn-secondary" style={{ color: 'var(--cyan)' }}>
              {asking ? "..." : "Ask"}
            </button>
          </form>
          {chatA && (
            <div style={{ marginTop: 12, padding: 12, background: 'var(--bg-input)', borderRadius: 8, fontSize: '0.84rem' }}>
              <p style={{ color: '#f8fafc' }}>{chatA.answer}</p>
              {chatA.actionable_tip && <p style={{ color: 'var(--emerald)', marginTop: 6 }}>💡 {chatA.actionable_tip}</p>}
            </div>
          )}
        </div>
      </div>

      <div className="panel">
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f8fafc', marginBottom: 16 }}>Procedural Cooking Guide</h3>
        {!recipe && !loading && (
          <div style={{ padding: 48, textAlign: 'center', color: 'var(--text-dim)' }}>
            <div style={{ fontSize: 36, marginBottom: 10 }}>🍳</div>
            <p style={{ fontWeight: 600, color: 'var(--text-muted)' }}>No Recipe Generated Yet</p>
            <p style={{ fontSize: '0.8rem', marginTop: 4 }}>
              Enter your ingredients on the left and click Generate to produce a timed procedural guide.
            </p>
          </div>
        )}

        {recipe && (
          <div>
            <div style={{ display: 'flex', gap: 12, fontSize: '0.78rem', color: 'var(--emerald)', fontWeight: 700, marginBottom: 4 }}>
              <span>⏱️ Prep: {recipe.prep_time_minutes}m</span>
              <span>🔥 Cook: {recipe.cook_time_minutes}m</span>
              <span>🍽️ Servings: {recipe.servings}</span>
            </div>
            <h4 style={{ fontSize: '1.4rem', fontWeight: 800, color: '#f8fafc' }}>{recipe.recipe_title}</h4>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', marginTop: 4, marginBottom: 16 }}>{recipe.description}</p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {recipe.steps?.map(s => (
                <div key={s.step_number} style={{ background: 'var(--bg-input)', padding: 14, borderRadius: 10, border: '1px solid var(--border-subtle)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontWeight: 800, color: '#f8fafc', fontSize: '0.88rem' }}>
                      Step {s.step_number}: <span style={{ color: 'var(--cyan)' }}>{s.action}</span>
                    </span>
                    <span style={{ fontSize: '0.72rem', color: 'var(--text-dim)', background: '#070b12', padding: '2px 8px', borderRadius: 4 }}>
                      {s.duration_minutes} min
                    </span>
                  </div>
                  <p style={{ fontSize: '0.84rem', color: '#cbd5e1', marginTop: 6, lineHeight: 1.5 }}>{s.instruction}</p>
                  {s.pro_tip && <div style={{ fontSize: '0.75rem', color: 'var(--emerald)', marginTop: 4 }}>💡 {s.pro_tip}</div>}
                </div>
              ))}
            </div>

            {/* Raw JSON Debug Viewer */}
            <details style={{ marginTop: 16 }}>
              <summary style={{ fontSize: '0.75rem', color: 'var(--text-dim)', cursor: 'pointer' }}>
                View Raw API JSON Payload
              </summary>
              <pre style={{
                marginTop: 8, padding: 12, background: '#070b12',
                borderRadius: 6, fontSize: '0.72rem', color: '#38bdf8',
                fontFamily: 'var(--font-mono)', overflowX: 'auto'
              }}>
                {JSON.stringify(recipe, null, 2)}
              </pre>
            </details>
          </div>
        )}
      </div>
    </div>
  );
}

// =========================================================================
// MODULE 5: PRECISION MEAL PLANNER WORKBENCH
// =========================================================================
function PlannerWorkbench() {
  const [profile, setProfile] = useState({
    name: "User",
    age: 26,
    gender: "male",
    weight_kg: 74,
    height_cm: 178,
    activity_level: "moderately_active",
    health_goal: "weight_loss",
    dietary_preference: "vegetarian",
    allergies: "peanuts, shellfish"
  });

  const [loading, setLoading] = useState(false);
  const [planResult, setPlanResult] = useState(null);

  const handleGeneratePlan = async (e) => {
    e.preventDefault();
    setLoading(true);
    setPlanResult(null);

    const payload = {
      profile: {
        name: profile.name,
        age: Number(profile.age),
        gender: profile.gender,
        weight_kg: Number(profile.weight_kg),
        height_cm: Number(profile.height_cm),
        activity_level: profile.activity_level,
        health_goal: profile.health_goal,
        dietary_preference: profile.dietary_preference,
        allergies: profile.allergies ? profile.allergies.split(",").map(s => s.trim()) : []
      },
      days: 1
    };

    try {
      const res = await fetch(`${API_BASE}/api/meal-planner/generate-plan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      setPlanResult(data);
    } catch (err) {
      alert("Meal planner API failed: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="workbench-grid">
      <div className="panel">
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f8fafc', marginBottom: 14 }}>Biometric & Dietary Setup</h3>
        <form onSubmit={handleGeneratePlan}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, marginBottom: 10 }}>
            <div>
              <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Age</label>
              <input type="number" value={profile.age} onChange={e => setProfile({...profile, age: e.target.value})} style={{ width: '100%' }} />
            </div>
            <div>
              <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Gender</label>
              <select value={profile.gender} onChange={e => setProfile({...profile, gender: e.target.value})} style={{ width: '100%' }}>
                <option value="male">Male</option>
                <option value="female">Female</option>
              </select>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, marginBottom: 10 }}>
            <div>
              <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Weight (kg)</label>
              <input type="number" value={profile.weight_kg} onChange={e => setProfile({...profile, weight_kg: e.target.value})} style={{ width: '100%' }} />
            </div>
            <div>
              <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Height (cm)</label>
              <input type="number" value={profile.height_cm} onChange={e => setProfile({...profile, height_cm: e.target.value})} style={{ width: '100%' }} />
            </div>
          </div>

          <div style={{ marginBottom: 10 }}>
            <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Health Goal</label>
            <select value={profile.health_goal} onChange={e => setProfile({...profile, health_goal: e.target.value})} style={{ width: '100%' }}>
              <option value="weight_loss">Weight Loss (-500 kcal)</option>
              <option value="muscle_gain">Muscle Gain (+350 kcal)</option>
              <option value="maintenance">Maintenance (Energy Balance)</option>
              <option value="keto">Keto Diet (High Healthy Fats)</option>
            </select>
          </div>

          <div style={{ marginBottom: 10 }}>
            <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Dietary Style</label>
            <select value={profile.dietary_preference} onChange={e => setProfile({...profile, dietary_preference: e.target.value})} style={{ width: '100%' }}>
              <option value="vegetarian">Vegetarian</option>
              <option value="vegan">Vegan (100% Plant-Based)</option>
              <option value="omnivore">Omnivore</option>
              <option value="pescatarian">Pescatarian</option>
            </select>
          </div>

          <div style={{ marginBottom: 18 }}>
            <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Allergies (Excluded Strictly)</label>
            <input
              type="text"
              value={profile.allergies}
              onChange={e => setProfile({...profile, allergies: e.target.value})}
              placeholder="e.g. peanuts, dairy, gluten"
              style={{ width: '100%' }}
            />
          </div>

          <button type="submit" disabled={loading} className="btn-primary" style={{ width: '100%' }}>
            {loading ? "Calculating Metabolism & Generating..." : "Generate Calibrated Meal Plan"}
          </button>
        </form>
      </div>

      <div className="panel">
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f8fafc', marginBottom: 16 }}>Calibrated Daily Plan</h3>

        {!planResult && !loading && (
          <div style={{ padding: 48, textAlign: 'center', color: 'var(--text-dim)' }}>
            <div style={{ fontSize: 36, marginBottom: 10 }}>🥗</div>
            <p style={{ fontWeight: 600, color: 'var(--text-muted)' }}>Awaiting User Metrics</p>
            <p style={{ fontSize: '0.8rem', marginTop: 4 }}>
              Fill in your biometric stats on the left and execute to compute scientific BMR/TDEE targets.
            </p>
          </div>
        )}

        {planResult && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingBottom: 16, borderBottom: '1px solid var(--border-subtle)' }}>
              <div>
                <span className="badge badge-emerald">{planResult.dietary_preference}</span>
                <h4 style={{ fontSize: '1.3rem', fontWeight: 800, color: '#f8fafc', marginTop: 6 }}>
                  Target: {planResult.target_calories_per_day} kcal / day
                </h4>
              </div>
            </div>

            {planResult.daily_plans?.map((day, idx) => (
              <div key={idx} style={{ marginTop: 14 }}>
                <div style={{ fontSize: '0.78rem', color: 'var(--cyan)', fontWeight: 700, marginBottom: 8 }}>
                  🎯 Focus: {day.daily_nutritional_focus}
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                  {day.meals?.map((m, mIdx) => (
                    <div key={mIdx} style={{ background: 'var(--bg-input)', padding: 12, borderRadius: 8, border: '1px solid var(--border-subtle)' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <span style={{ fontWeight: 800, fontSize: '0.88rem', color: '#f8fafc' }}>
                          {m.meal_type}: {m.dish_name}
                        </span>
                        <span style={{ fontWeight: 700, color: 'var(--emerald)', fontSize: '0.84rem' }}>
                          {m.calories} kcal
                        </span>
                      </div>
                      <div style={{ fontSize: '0.74rem', color: 'var(--text-dim)', marginTop: 4 }}>
                        Protein: {m.protein}g | Carbs: {m.carbs}g | Fats: {m.fats}g • Prep: {m.prep_time_minutes}m
                      </div>
                      {m.alternative_options && m.alternative_options.length > 0 && (
                        <div style={{ fontSize: '0.72rem', color: '#94a3b8', marginTop: 4 }}>
                          Substitutes: {m.alternative_options.join(", ")}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            ))}

            <div style={{ marginTop: 16, padding: 10, background: 'var(--emerald-subtle)', borderRadius: 6, fontSize: '0.78rem', color: '#34d399' }}>
              🛡️ {planResult.allergen_safeguards?.join(" ")}
            </div>

            {/* Raw JSON Debug Viewer */}
            <details style={{ marginTop: 16 }}>
              <summary style={{ fontSize: '0.75rem', color: 'var(--text-dim)', cursor: 'pointer' }}>
                View Raw API JSON Payload
              </summary>
              <pre style={{
                marginTop: 8, padding: 12, background: '#070b12',
                borderRadius: 6, fontSize: '0.72rem', color: '#38bdf8',
                fontFamily: 'var(--font-mono)', overflowX: 'auto'
              }}>
                {JSON.stringify(planResult, null, 2)}
              </pre>
            </details>
          </div>
        )}
      </div>
    </div>
  );
}
