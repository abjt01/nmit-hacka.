const App = () => {
  const [loading, setLoading] = React.useState(false);
  const [problems, setProblems] = React.useState([]);
  const [stats, setStats] = React.useState(null);
  const [numProblems, setNumProblems] = React.useState(12);
  const [category, setCategory] = React.useState("Mixed (All Categories)");
  
  const categories = [
    "Time, Speed & Distance",
    "Work & Time",
    "Pipes & Cisterns",
    "Profit, Loss & Discount",
    "Ratio, Mixtures & Sharing",
    "Age Problems",
    "Boats & Streams",
    "Allocation & Logical Math",
    "Mixed (All Categories)"
  ];
  
  const handleGenerate = async () => {
    setLoading(true);
    setProblems([]);
    setStats(null);
    
    try {
      const response = await fetch('http://localhost:8000/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          num_problems: parseInt(numProblems),
          category: category
        })
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Server error: ${errorText}`);
      }
      
      const result = await response.json();
      console.log('Result:', result);
      
      setProblems(result.problems || []);
      setStats(result.stats || {});
    } catch (error) {
      console.error('Error:', error);
      alert('Error generating problems: ' + error.message + '\n\nCheck:\n1. Backend running on port 8000\n2. GROQ_API_KEY in .env\n3. Browser console (F12) for details');
    } finally {
      setLoading(false);
    }
  };
  
  const handleExport = async () => {
    if (problems.length === 0) {
      alert('No problems to export');
      return;
    }
    
    try {
      const response = await fetch('http://localhost:8000/api/export/html', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(problems)
      });
      
      const result = await response.json();
      const blob = new Blob([result.html], { type: 'text/html' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'hydrahacks-quiz.html';
      a.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      alert('Error exporting: ' + error.message);
    }
  };
  
  return (
    <div className="container">
      <Header />
      
      <div className="control-panel">
        <h2 style={{ marginBottom: 'var(--space-lg)' }}>Generation Settings</h2>
        
        <div className="form-group">
          <label>Number of Problems (1-20)</label>
          <input 
            type="number" 
            min="1" 
            max="20" 
            value={numProblems}
            onChange={(e) => setNumProblems(e.target.value)}
          />
        </div>
        
        <div className="form-group">
          <label>Problem Category</label>
          <select 
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          >
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>
        
        <div style={{ display: 'flex', gap: 'var(--space-md)', marginTop: 'var(--space-lg)' }}>
          <button 
            className="btn btn-primary" 
            onClick={handleGenerate}
            disabled={loading}
          >
            {loading ? '⏳ Generating...' : '🚀 Generate Problems'}
          </button>
          
          {problems.length > 0 && (
            <button className="btn btn-secondary" onClick={handleExport}>
              📥 Export HTML Quiz
            </button>
          )}
        </div>
      </div>
      
      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <p>Generating {numProblems} problems for: {category}</p>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginTop: '10px' }}>
            This will use approximately {parseInt(numProblems) * 2 + 1} API calls
          </p>
        </div>
      )}
      
      {stats && (
        <div style={{ 
          background: 'var(--bg-secondary)', 
          padding: 'var(--space-lg)', 
          borderRadius: 'var(--radius-lg)',
          marginBottom: 'var(--space-xl)'
        }}>
          <h3 style={{ marginBottom: 'var(--space-md)' }}>📊 Generation Stats</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 'var(--space-md)' }}>
            <div>
              <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--accent-primary)' }}>
                {stats.total_generated || 0}
              </div>
              <div style={{ color: 'var(--text-secondary)' }}>Problems Generated</div>
            </div>
            <div>
              <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--success)' }}>
                {stats.total_api_calls || 0}
              </div>
              <div style={{ color: 'var(--text-secondary)' }}>Total API Calls</div>
            </div>
            <div>
              <div style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--warning)' }}>
                {stats.api_efficiency || 'N/A'}
              </div>
              <div style={{ color: 'var(--text-secondary)' }}>Efficiency</div>
            </div>
          </div>
        </div>
      )}
      
      <ProblemViewer problems={problems} />
    </div>
  );
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
