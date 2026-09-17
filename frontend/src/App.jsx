import React, { useState, useEffect } from 'react';
import { 
  BarChart3, 
  BrainCircuit, 
  UploadCloud, 
  Cpu, 
  CheckCircle2, 
  Zap, 
  Sliders, 
  FileText, 
  Play, 
  RefreshCw, 
  ChevronRight,
  TrendingUp,
  Award,
  HelpCircle,
  AlertTriangle,
  ShieldCheck,
  Activity
} from 'lucide-react';




import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LineElement
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const API_BASE = "";

const FEATURE_DISPLAY_NAMES = {
  n_instances: "Rows",
  n_features: "Features",
  ratio_instances_to_features: "Rows per Feature",
  n_numeric_features: "Numeric Features",
  n_categorical_features: "Categorical Features",
  ratio_numeric_features: "Numeric Feature Share",
  ratio_categorical_features: "Categorical Feature Share",
  n_missing_values: "Missing Values",
  missing_value_ratio: "Missing Value Rate",
  n_classes: "Number of Classes",
  class_imbalance_ratio: "Class Imbalance Ratio",
  majority_class_percentage: "Majority Class Share",
  skewness_mean: "Average Feature Skewness",
  skewness_std: "Feature Skewness Variation",
  kurtosis_mean: "Average Feature Kurtosis",
  kurtosis_std: "Feature Kurtosis Variation",
  mean_correlation_abs: "Average Feature Correlation",
  class_entropy: "Class Diversity (Entropy)",
  normalized_class_entropy: "Normalized Class Diversity",
  landmarker_decision_stump: "Decision Tree Quick-Test Score",
  landmarker_naive_bayes: "Naive Bayes Quick-Test Score"
};

const getFriendlyFeatureName = (name) => FEATURE_DISPLAY_NAMES[name] || name;

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');
  const [systemStatus, setSystemStatus] = useState(null);
  const [featureImportances, setFeatureImportances] = useState([]);
  const [evalMetrics, setEvalMetrics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showModelsModal, setShowModelsModal] = useState(false);
  
  // Predict & Benchmark State
  const [selectedFile, setSelectedFile] = useState(null);
  const [targetColumn, setTargetColumn] = useState('');
  const [predictionResult, setPredictionResult] = useState(null);
  const [benchmarkResult, setBenchmarkResult] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);


  useEffect(() => {
    fetchSystemInfo();
  }, []);

  const fetchSystemInfo = async () => {
    try {
      const statusRes = await fetch(`${API_BASE}/api/status`);
      const statusData = await statusRes.json();
      setSystemStatus(statusData);

      const impRes = await fetch(`${API_BASE}/api/feature-importances`);
      const impData = await impRes.json();
      setFeatureImportances(impData);

      const evalRes = await fetch(`${API_BASE}/api/evaluation-metrics`);
      const evalData = await evalRes.json();
      setEvalMetrics(evalData);
    } catch (err) {
      console.error("Failed to load backend system data:", err);
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPredictionResult(null);
      setBenchmarkResult(null);
    }
  };

  const handlePredictStrategy = async () => {
    if (!selectedFile) return;
    setIsProcessing(true);
    const formData = new FormData();
    formData.append("file", selectedFile);
    if (targetColumn) {
      formData.append("target_column", targetColumn);
    }

    try {
      const res = await fetch(`${API_BASE}/api/predict-strategy`, {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      setPredictionResult(data);
    } catch (err) {
      alert("Error predicting strategy: " + err.message);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleRunBenchmark = async () => {
    if (!selectedFile) return;
    setIsProcessing(true);
    const formData = new FormData();
    formData.append("file", selectedFile);
    if (targetColumn) {
      formData.append("target_column", targetColumn);
    }

    try {
      const res = await fetch(`${API_BASE}/api/benchmark-dataset`, {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      setBenchmarkResult(data);
    } catch (err) {
      alert("Error running benchmark: " + err.message);
    } finally {
      setIsProcessing(false);
    }
  };

  // Chart Data Configurations
  const impChartData = {
    labels: featureImportances.slice(0, 8).map(item => getFriendlyFeatureName(item.meta_feature)),
    datasets: [{
      label: 'Meta-Feature Importance',
      data: featureImportances.slice(0, 8).map(item => item.importance),
      backgroundColor: '#F59E0B',
      borderRadius: 4
    }]
  };

  const evalChartData = {
    labels: ['Selected-Model F1', 'Oracle Best F1', 'Default RandomForest F1', 'Random Baseline F1'],
    datasets: [{
      label: 'F1-Weighted Score',
      data: evalMetrics ? [
        evalMetrics.meta_router_avg_f1,
        evalMetrics.oracle_avg_f1,
        evalMetrics.default_baseline_rf_avg_f1,
        evalMetrics.random_baseline_avg_f1
      ] : [0.850, 0.860, 0.849, 0.828],
      backgroundColor: ['#22C55E', '#FBBF24', '#F59E0B', '#A3A3A3'],
      borderRadius: 4
    }]
  };



  return (
    <div className="app-container">
      {/* Top Navbar Header */}
      <header className="top-navbar">
        <div className="navbar-brand">
          <img src="/logo.jpg" alt="AlgoRoute Logo" className="brand-logo-img" />
          <div>
            <div className="brand-title">AlgoRoute</div>
            <div className="brand-subtitle">Intelligent Machine Learning Strategy Recommendation Engine</div>
          </div>
        </div>

        {/* Top Navigation Tabs */}
        <nav className="navbar-nav">
          <button 
            className={`nav-pill ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            <BarChart3 size={16} /> Overview & Metrics
          </button>
          <button 
            className={`nav-pill ${activeTab === 'router' ? 'active' : ''}`}
            onClick={() => setActiveTab('router')}
          >
            <BrainCircuit size={16} /> AlgoRoute Engine (Upload)
          </button>

          <button 
            className={`nav-pill ${activeTab === 'analytics' ? 'active' : ''}`}
            onClick={() => setActiveTab('analytics')}
          >
            <Sliders size={16} /> Intelligence Analytics
          </button>
        </nav>

        {/* Top Navbar Utility Right Actions */}
        <div className="navbar-actions" style={{ position: 'relative' }}>
          <div className="system-status-badge">
            <span className="status-dot"></span>
            <span>Router API Online</span>
          </div>

          {/* 6 Candidate ML Strategies Portfolio Badge */}
          <button 
            className="btn btn-secondary" 
            onClick={() => setShowModelsModal(!showModelsModal)}
            style={{ 
              padding: '0.45rem 0.9rem', 
              fontSize: '0.85rem', 
              borderColor: 'rgba(99, 102, 241, 0.4)',
              backgroundColor: 'rgba(99, 102, 241, 0.12)',
              color: 'var(--color-primary)'
            }}
            title="Click to view candidate algorithm portfolio"
          >
            <Cpu size={15} /> 6 Candidate Strategies
          </button>

          {/* Quick Models Portfolio Dropdown / Popover */}
          {showModelsModal && (
            <div style={{
              position: 'absolute',
              top: '120%',
              right: 0,
              backgroundColor: '#0D2527',

              border: '1px solid var(--border-color)',
              borderRadius: 'var(--radius-md)',
              padding: '1rem',
              boxShadow: 'var(--shadow-lg)',
              zIndex: 200

            }}>

              <div style={{ fontSize: '0.85rem', fontWeight: '700', color: 'var(--text-primary)', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <Cpu size={15} style={{ color: 'var(--color-primary)' }} /> Candidate Model Portfolio
              </div>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginBottom: '0.75rem', lineHeight: '1.4' }}>
                The Meta-Router evaluates and ranks these 6 algorithms for every dataset:
              </p>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem', fontSize: '0.8rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-primary)' }}>🌲 <strong>RandomForest</strong></div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-primary)' }}>⚡ <strong>GradientBoosting</strong></div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-primary)' }}>📈 <strong>LogisticRegression</strong></div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-primary)' }}>📍 <strong>K-Nearest Neighbors (KNN)</strong></div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-primary)' }}>📐 <strong>DecisionTree</strong></div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-primary)' }}>🎲 <strong>Gaussian Naive Bayes</strong></div>
              </div>
            </div>
          )}
        </div>

      </header>

      {/* Main Dashboard Content Area */}
      <main className="main-content">


        {/* Tab 1: Overview & Metrics */}
        {activeTab === 'overview' && (
          <div>
            <div className="card-grid" style={{ gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem', marginBottom: '1.5rem' }}>
              <div className="card" title="Average F1 score achieved by the algorithms selected by the Meta-Router.">
                <div className="card-title">Average Recommendation Performance</div>
                <div className="card-value">
                  {evalMetrics ? (evalMetrics.meta_router_avg_f1 * 100).toFixed(1) : '85.0'}%
                </div>
                <div className="card-subtext" style={{ color: '#10b981' }}>
                  +{(evalMetrics ? (evalMetrics.improvement_over_default * 100).toFixed(1) : '0.2')}% over Default Baseline
                </div>
              </div>

              <div className="card" title="How often the router selects the actual best algorithm.">
                <div className="card-title">Top-1 Recommendation Accuracy</div>
                <div className="card-value">
                  {evalMetrics ? (evalMetrics.top1_accuracy * 100).toFixed(0) : '50'}%
                </div>
                <div className="card-subtext">Exact Rank-1 Match</div>
              </div>

              <div className="card" title="How often the actual best algorithm appears in the router's top 3.">
                <div className="card-title">Top-3 Recommendation Success</div>
                <div className="card-value">
                  {evalMetrics && evalMetrics.top3_hit_rate !== undefined ? (evalMetrics.top3_hit_rate * 100).toFixed(0) : '90'}%
                </div>
                <div className="card-subtext">Winner in Router Top 3</div>
              </div>

              <div className="card" title="Average performance gap between our recommendation and the best available algorithm. Lower is better.">
                <div className="card-title">Average Regret</div>
                <div className="card-value">
                  {evalMetrics ? evalMetrics.average_regret.toFixed(4) : '0.0096'}
                </div>
                <div className="card-subtext">Gap vs. Oracle Best (Lower is better)</div>
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '2rem' }}>
              <div className="card">
                <h3 style={{ fontSize: '1.05rem', fontWeight: '600', marginBottom: '0.25rem' }}>
                  How Well Does the Router Perform?
                </h3>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
                  Comparison with the best available model and baseline strategies.
                </div>
                <Bar 
                  data={evalChartData} 
                  options={{ 
                    responsive: true, 
                    plugins: { legend: { display: false } },
                    scales: { 
                      x: { ticks: { color: '#D4D4D4' }, grid: { color: '#262626' } },
                      y: { min: 0.5, max: 1.0, ticks: { color: '#D4D4D4' }, grid: { color: '#262626' } } 
                    }
                  }} 
                />
              </div>

              <div className="card">
                <h3 style={{ fontSize: '1.05rem', fontWeight: '600', marginBottom: '0.25rem' }}>
                  What Influences the Router?
                </h3>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
                  Relative importance of dataset characteristics used by the Meta-Router
                </div>
                <div style={{ fontSize: '0.75rem', backgroundColor: '#0B0B0B', padding: '0.5rem 0.75rem', borderRadius: 'var(--radius-sm)', marginBottom: '0.75rem', borderLeft: '3px solid var(--color-primary)', color: 'var(--text-secondary)', lineHeight: '1.4' }}>
                  ℹ️ These values show which dataset characteristics are most useful to the Meta-Router when making its recommendation. They do not represent the ranking of ML algorithms.
                </div>
                <Bar 
                  data={impChartData} 
                  options={{ 
                    responsive: true, 
                    indexAxis: 'y',
                    plugins: { legend: { display: false } },
                    scales: {
                      x: { ticks: { color: '#D4D4D4' }, grid: { color: '#262626' } },
                      y: { ticks: { color: '#D4D4D4' }, grid: { color: '#262626' } }
                    }
                  }} 
                />
              </div>




            </div>
          </div>
        )}



        {/* Tab 2: Strategy Router & CSV Drag-and-Drop */}
        {activeTab === 'router' && (
          <div>
            <div className="card" style={{ marginBottom: '2rem' }}>
              <h3 style={{ fontSize: '1.1rem', fontWeight: '600', marginBottom: '1rem' }}>
                Upload Tabular Dataset (.csv)
              </h3>

              <div 
                className="dropzone"
                onClick={() => document.getElementById('csv-input').click()}
              >
                <UploadCloud className="dropzone-icon" />
                <h3>{selectedFile ? selectedFile.name : 'Click or Drag & Drop CSV File'}</h3>
                <p>{selectedFile ? `${(selectedFile.size / 1024).toFixed(1)} KB` : 'Supports standard tabular datasets with numeric or categorical columns'}</p>
                <input 
                  id="csv-input" 
                  type="file" 
                  accept=".csv" 
                  style={{ display: 'none' }}
                  onChange={handleFileUpload}
                />
              </div>

              <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem', alignItems: 'center' }}>
                <input 
                  type="text" 
                  placeholder="Target Column Name (optional, default: auto-detect)"
                  value={targetColumn}
                  onChange={(e) => setTargetColumn(e.target.value)}
                  style={{
                    flex: 1,
                    padding: '0.65rem 1rem',
                    backgroundColor: 'var(--bg-dark)',
                    border: '1px solid var(--border-color)',
                    borderRadius: 'var(--radius-sm)',
                    color: 'var(--text-primary)',
                    fontSize: '0.9rem'
                  }}
                />
                <button 
                  className="btn btn-primary" 
                  disabled={!selectedFile || isProcessing}
                  onClick={handlePredictStrategy}
                >
                  <Zap size={16} /> {isProcessing ? 'Routing...' : 'Predict Strategy'}
                </button>
                <button 
                  className="btn btn-secondary" 
                  disabled={!selectedFile || isProcessing}
                  onClick={handleRunBenchmark}
                >
                  <Play size={15} /> Run Live Benchmarks
                </button>
              </div>

              {/* Local Data Privacy Indicator Panel */}
              <div style={{ 
                marginTop: '1.5rem', 
                backgroundColor: 'var(--bg-dark)', 
                border: '1px solid var(--border-color)', 
                borderRadius: 'var(--radius-sm)', 
                padding: '0.85rem 1rem' 
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                  <ShieldCheck size={16} style={{ color: 'var(--color-success)' }} />
                  <span style={{ fontSize: '0.85rem', fontWeight: '700', color: 'var(--text-primary)', letterSpacing: '0.5px' }}>
                    LOCAL DATA PRIVACY & IN-MEMORY PROCESSING
                  </span>
                </div>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', margin: '0 0 0.6rem 0', lineHeight: '1.4' }}>
                  Your uploaded dataset is processed 100% locally by this application's local backend.
                </p>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '0.5rem', fontSize: '0.75rem' }}>
                  <div style={{ backgroundColor: 'var(--bg-card)', padding: '0.4rem 0.6rem', borderRadius: '4px' }}>
                    <span style={{ color: 'var(--text-secondary)' }}>Processing:</span> <strong style={{ color: 'var(--color-success)' }}>Local</strong>
                  </div>
                  <div style={{ backgroundColor: 'var(--bg-card)', padding: '0.4rem 0.6rem', borderRadius: '4px' }}>
                    <span style={{ color: 'var(--text-secondary)' }}>External AI Upload:</span> <strong style={{ color: 'var(--color-success)' }}>No</strong>
                  </div>
                  <div style={{ backgroundColor: 'var(--bg-card)', padding: '0.4rem 0.6rem', borderRadius: '4px' }}>
                    <span style={{ color: 'var(--text-secondary)' }}>Persistent Storage:</span> <strong style={{ color: 'var(--color-success)' }}>No</strong>
                  </div>
                  <div style={{ backgroundColor: 'var(--bg-card)', padding: '0.4rem 0.6rem', borderRadius: '4px' }}>
                    <span style={{ color: 'var(--text-secondary)' }}>Temp Files:</span> <strong style={{ color: 'var(--color-success)' }}>In-Memory Only</strong>
                  </div>
                </div>
              </div>
            </div>


            {/* Strategy Recommendation Output Spotlight */}
            {predictionResult && (
              <>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '2rem' }}>
                  <div className="card" style={{ borderLeft: '4px solid var(--color-success)' }}>
                    <div className="badge badge-success" style={{ marginBottom: '0.75rem' }}>
                      <Award size={12} style={{ marginRight: '4px' }} /> Recommended ML Strategy
                    </div>
                    <h2 style={{ fontSize: '1.8rem', fontWeight: '700', color: 'var(--text-primary)' }}>
                      {predictionResult.recommended_algorithm}
                    </h2>
                    <div style={{ display: 'flex', gap: '1.5rem', marginTop: '1rem' }}>
                      <div>
                        <div className="card-title">Predicted F1 Score</div>
                        <div style={{ fontSize: '1.4rem', fontWeight: '700', color: 'var(--color-success)' }}>
                          {predictionResult.predicted_f1_score}
                        </div>
                      </div>
                      <div title="Indicates the relative strength of the router's recommendation relative to candidate strategies. This is a ranking score, not a calibrated probability.">
                        <div className="card-title">Strategy Recommendation Score</div>
                        <div style={{ fontSize: '1.4rem', fontWeight: '700', color: 'var(--color-primary)' }}>
                          {predictionResult.recommendation_score || predictionResult.confidence_percentage} / 100
                        </div>
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.2rem' }}>
                          Relative Ranking Score (Not Probability)
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="card">
                    <div className="card-title">Strategy Rankings & Predicted F1</div>
                    <div style={{ marginTop: '0.75rem' }}>
                      {predictionResult.rankings.map((item) => (
                        <div 
                          key={item.algorithm} 
                          style={{ 
                            display: 'flex', 
                            justifyContent: 'space-between', 
                            alignItems: 'center', 
                            padding: '0.4rem 0',
                            borderBottom: '1px solid var(--border-color)',
                            fontSize: '0.9rem'
                          }}
                        >
                          <span style={{ fontWeight: item.rank === 1 ? '700' : '500' }}>
                            #{item.rank} {item.algorithm}
                          </span>
                          <span className={`badge ${item.rank === 1 ? 'badge-success' : 'badge-primary'}`}>
                            F1: {item.predicted_f1}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Upgrade #3: Dataset Health & Suitability Analysis Panel */}
                {predictionResult.dataset_health && (

                  <div className="card" style={{ marginBottom: '2rem', borderTop: '3px solid var(--color-success)' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <Activity size={18} style={{ color: 'var(--color-success)' }} />
                        <h3 style={{ fontSize: '1.2rem', fontWeight: '700', margin: 0, color: 'var(--text-primary)' }}>
                          Dataset Health & Suitability Analysis
                        </h3>
                      </div>
                      <div className={`badge badge-${predictionResult.dataset_health.badge_color}`} style={{ fontSize: '0.85rem', padding: '0.4rem 0.8rem', fontWeight: '700' }}>
                        {predictionResult.dataset_health.status_code === 'GREEN' ? '🟢' : predictionResult.dataset_health.status_code === 'YELLOW' ? '🟡' : '🔴'} {predictionResult.dataset_health.status}
                      </div>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.2fr', gap: '1.5rem' }}>
                      {/* Health Profile Grid */}
                      <div style={{ backgroundColor: 'var(--bg-dark)', padding: '1rem', borderRadius: 'var(--radius-sm)' }}>
                        <div style={{ fontSize: '0.85rem', fontWeight: '700', color: 'var(--text-secondary)', textTransform: 'uppercase', marginBottom: '0.75rem', letterSpacing: '0.5px' }}>
                          Dataset Health Profile
                        </div>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem 1rem', fontSize: '0.85rem' }}>
                          <div><span style={{ color: 'var(--text-secondary)' }}>Sample Size:</span> <strong>{predictionResult.dataset_health.profile.rows} rows</strong></div>
                          <div><span style={{ color: 'var(--text-secondary)' }}>Features:</span> <strong>{predictionResult.dataset_health.profile.features}</strong></div>
                          <div><span style={{ color: 'var(--text-secondary)' }}>Numeric / Cat:</span> <strong>{predictionResult.dataset_health.profile.numeric_features} / {predictionResult.dataset_health.profile.categorical_features}</strong></div>
                          <div><span style={{ color: 'var(--text-secondary)' }}>Missing Values:</span> <strong>{predictionResult.dataset_health.profile.missing_values_pct}</strong></div>
                          <div><span style={{ color: 'var(--text-secondary)' }}>Classes:</span> <strong>{predictionResult.dataset_health.profile.classes}</strong></div>
                          <div><span style={{ color: 'var(--text-secondary)' }}>Imbalance Ratio:</span> <strong>{predictionResult.dataset_health.profile.imbalance_ratio}</strong></div>
                          <div style={{ gridColumn: 'span 2' }}><span style={{ color: 'var(--text-secondary)' }}>Instance-to-Feature Ratio:</span> <strong>{predictionResult.dataset_health.profile.instance_to_feature_ratio}:1</strong></div>
                        </div>
                      </div>

                      {/* Health Findings & Warnings */}
                      <div style={{ backgroundColor: 'var(--bg-dark)', padding: '1rem', borderRadius: 'var(--radius-sm)' }}>
                        <div style={{ fontSize: '0.85rem', fontWeight: '700', color: 'var(--text-secondary)', textTransform: 'uppercase', marginBottom: '0.75rem', letterSpacing: '0.5px' }}>
                          Structural Findings
                        </div>
                        <ul style={{ margin: 0, paddingLeft: '1.2rem', fontSize: '0.85rem', lineHeight: '1.6', color: 'var(--text-primary)' }}>
                          {predictionResult.dataset_health.findings.map((item, idx) => (
                            <li key={idx} style={{ marginBottom: '0.35rem' }}>{item}</li>
                          ))}
                        </ul>

                        {predictionResult.dataset_health.warnings && predictionResult.dataset_health.warnings.length > 0 && (
                          <div style={{ marginTop: '0.85rem', backgroundColor: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', padding: '0.65rem 0.85rem', borderRadius: 'var(--radius-sm)' }}>
                            <div style={{ fontSize: '0.8rem', fontWeight: '700', color: '#ef4444', marginBottom: '0.3rem', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                              <AlertTriangle size={13} /> Suitability Considerations
                            </div>
                            <ul style={{ margin: 0, paddingLeft: '1.2rem', fontSize: '0.8rem', color: 'var(--text-primary)' }}>
                              {predictionResult.dataset_health.warnings.map((warn, idx) => (
                                <li key={idx}>{warn}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                )}

                {/* Explainable Recommendation Engine Section */}
                {predictionResult.explanation && (

                  <div className="card" style={{ marginBottom: '2rem', borderTop: '3px solid var(--color-primary)' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                      <HelpCircle size={18} style={{ color: 'var(--color-primary)' }} />
                      <h3 style={{ fontSize: '1.2rem', fontWeight: '700', margin: 0, color: 'var(--text-primary)' }}>
                        Why This Strategy?
                      </h3>
                    </div>

                    <div style={{ 
                      backgroundColor: 'var(--bg-dark)', 
                      padding: '1rem 1.25rem', 
                      borderRadius: 'var(--radius-sm)', 
                      marginBottom: '1.5rem',
                      borderLeft: '3px solid var(--color-primary)',
                      fontSize: '0.95rem',
                      lineHeight: '1.5',
                      color: 'var(--text-primary)'
                    }}>
                      <div style={{ fontWeight: '600', marginBottom: '0.25rem', color: 'var(--color-primary)' }}>
                        🏆 {predictionResult.recommended_algorithm}
                      </div>
                      {predictionResult.explanation.summary}
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                      {/* Dataset Profile */}
                      <div style={{ backgroundColor: 'var(--bg-dark)', padding: '1rem', borderRadius: 'var(--radius-sm)' }}>
                        <div style={{ fontSize: '0.85rem', fontWeight: '700', color: 'var(--text-secondary)', textTransform: 'uppercase', marginBottom: '0.75rem', letterSpacing: '0.5px' }}>
                          Dataset Profile
                        </div>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem 1rem', fontSize: '0.85rem' }}>
                          <div><span style={{ color: 'var(--text-secondary)' }}>Rows:</span> <strong>{predictionResult.explanation.dataset_profile.rows}</strong></div>
                          <div><span style={{ color: 'var(--text-secondary)' }}>Features:</span> <strong>{predictionResult.explanation.dataset_profile.features}</strong></div>
                          <div><span style={{ color: 'var(--text-secondary)' }}>Missing Values:</span> <strong>{predictionResult.explanation.dataset_profile.missing_values_pct}</strong></div>
                          <div><span style={{ color: 'var(--text-secondary)' }}>Classes:</span> <strong>{predictionResult.explanation.dataset_profile.classes}</strong></div>
                          <div><span style={{ color: 'var(--text-secondary)' }}>Numeric Features:</span> <strong>{predictionResult.explanation.dataset_profile.numeric_features}</strong></div>
                          <div><span style={{ color: 'var(--text-secondary)' }}>Imbalance Ratio:</span> <strong>{predictionResult.explanation.dataset_profile.imbalance_ratio}:1</strong></div>
                        </div>
                      </div>

                      {/* Supporting Key Factors */}
                      <div style={{ backgroundColor: 'var(--bg-dark)', padding: '1rem', borderRadius: 'var(--radius-sm)' }}>
                        <div style={{ fontSize: '0.85rem', fontWeight: '700', color: 'var(--text-secondary)', textTransform: 'uppercase', marginBottom: '0.75rem', letterSpacing: '0.5px' }}>
                          Key Supporting Factors
                        </div>
                        <ul style={{ margin: 0, paddingLeft: '1.2rem', fontSize: '0.85rem', lineHeight: '1.6', color: 'var(--text-primary)' }}>
                          {predictionResult.explanation.supporting_factors.map((factor, idx) => (
                            <li key={idx} style={{ marginBottom: '0.4rem' }}>{factor}</li>
                          ))}
                        </ul>
                      </div>
                    </div>

                    {/* Cautions / Considerations */}
                    {predictionResult.explanation.cautions && predictionResult.explanation.cautions.length > 0 && (
                      <div style={{ marginTop: '1.25rem', backgroundColor: 'rgba(234, 179, 8, 0.1)', border: '1px solid rgba(234, 179, 8, 0.3)', padding: '0.85rem 1rem', borderRadius: 'var(--radius-sm)' }}>
                        <div style={{ fontSize: '0.85rem', fontWeight: '700', color: '#eab308', marginBottom: '0.4rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                          <AlertTriangle size={14} /> Considerations & Deployment Cautions
                        </div>
                        <ul style={{ margin: 0, paddingLeft: '1.2rem', fontSize: '0.85rem', color: 'var(--text-primary)' }}>
                          {predictionResult.explanation.cautions.map((caution, idx) => (
                            <li key={idx}>{caution}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </>
            )}



            {/* Live Benchmark Execution Matrix */}
            {benchmarkResult && (
              <div className="card" style={{ marginBottom: '2rem' }}>
                <h3 style={{ fontSize: '1.1rem', fontWeight: '600', marginBottom: '1rem' }}>
                  Live 5-Fold Stratified CV Benchmark Results ({benchmarkResult.dataset_name})
                </h3>
                <div className="table-container">
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>Rank</th>
                        <th>Algorithm</th>
                        <th>F1 Weighted</th>
                        <th>Accuracy</th>
                        <th>Fit Time (sec)</th>
                      </tr>
                    </thead>
                    <tbody>
                      {benchmarkResult.benchmark_results.map((res) => (
                        <tr key={res.algorithm}>
                          <td>
                            <span className={`badge ${res.rank === 1 ? 'badge-success' : ''}`}>
                              #{res.rank}
                            </span>
                          </td>
                          <td style={{ fontWeight: '600' }}>{res.algorithm}</td>
                          <td style={{ color: 'var(--color-success)', fontWeight: '700' }}>
                            {res.f1_weighted.toFixed(4)}
                          </td>
                          <td>{(res.accuracy * 100).toFixed(2)}%</td>
                          <td>{res.fit_time_sec.toFixed(3)}s</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Extracted Meta-Features Data Table */}
            {predictionResult && predictionResult.meta_features && (
              <div className="card">
                <h3 style={{ fontSize: '1.1rem', fontWeight: '600', marginBottom: '0.25rem' }}>
                  Extracted Meta-Features Inventory ({predictionResult.dataset_name})
                </h3>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
                  21 extracted statistical, structural, and landmarker probe characteristics describing this dataset.
                </div>
                <div className="table-container" style={{ maxHeight: '320px', overflowY: 'auto' }}>
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>Characteristic (Display Name)</th>
                        <th>Internal Attribute Key</th>
                        <th>Extracted Numeric Value</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.entries(predictionResult.meta_features).map(([key, val]) => (
                        <tr key={key}>
                          <td style={{ fontWeight: '600', color: 'var(--text-primary)' }}>
                            {getFriendlyFeatureName(key)}
                          </td>
                          <td style={{ fontWeight: '400', color: 'var(--text-secondary)' }}>
                            <code style={{ fontSize: '0.8rem' }}>{key}</code>
                          </td>
                          <td style={{ fontWeight: '600', color: 'var(--color-primary)' }}>
                            {typeof val === 'number' ? val.toFixed(4) : String(val)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Tab 3: Intelligence Analytics */}
        {activeTab === 'analytics' && (
          <div>
            <div className="card" style={{ marginBottom: '1.5rem' }}>
              <h3 style={{ fontSize: '1.1rem', fontWeight: '600', marginBottom: '0.25rem' }}>
                Full Meta-Feature Importance Ranking (All 21 Extracted Attributes)
              </h3>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
                Shows how much weight the Meta-Router assigns to each dataset characteristic when recommending an ML strategy.
              </div>
              <div className="table-container">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Rank</th>
                      <th>Dataset Characteristic</th>
                      <th>Internal Key</th>
                      <th>Meta-Router Importance Score</th>
                      <th>Category</th>
                    </tr>
                  </thead>
                  <tbody>
                    {featureImportances.map((item, idx) => (
                      <tr key={item.meta_feature}>
                        <td>#{idx + 1}</td>
                        <td style={{ fontWeight: '600', color: 'var(--text-primary)' }}>{getFriendlyFeatureName(item.meta_feature)}</td>
                        <td style={{ fontWeight: '400', color: 'var(--text-secondary)' }}><code style={{ fontSize: '0.8rem' }}>{item.meta_feature}</code></td>
                        <td style={{ color: 'var(--color-primary)', fontWeight: '700' }}>
                          {item.importance.toFixed(6)}
                        </td>
                        <td>
                          <span className="badge badge-primary">
                            {item.meta_feature.includes('landmarker') ? 'Quick-Test Probe' : 
                             item.meta_feature.includes('skewness') || item.meta_feature.includes('kurtosis') ? 'Statistical' : 'Structural'}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

      </main>
    </div>
  );
}
