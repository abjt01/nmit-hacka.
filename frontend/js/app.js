const App = () => {
  const [loading, setLoading] = React.useState(false);
  const [problems, setProblems] = React.useState([]);
  const [stats, setStats] = React.useState(null);
  const [numProblems, setNumProblems] = React.useState(12);
  const [category, setCategory] = React.useState("Mixed (All Categories)");
  const [error, setError] = React.useState(null);
  
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
    setError(null);
    
    try {
      console.log('🚀 Sending request...');
      
      const response = await fetch('http://localhost:8000/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          num_problems: parseInt(numProblems),
          category: category
        })
      });
      
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }
      
      const result = await response.json();
      console.log('✅ Result:', result);
      
      if (result.problems && Array.isArray(result.problems)) {
        setProblems(result.problems);
        setStats(result.stats);
      } else {
        setError('Invalid response format');
      }
      
    } catch (error) {
      console.error('❌ Error:', error);
      setError(error.message);
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
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(problems)
      });
      
      const result = await response.json();
      const blob = new Blob([result.html], { type: 'text/html' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'polysolve-ai-quiz.html';
      a.click();
      URL.revokeObjectURL(url);
      
      console.log('✅ Quiz exported');
    } catch (error) {
      alert('Error exporting: ' + error.message);
    }
  };
  
  return (
    <div className="container">
      <Header />
      
      <div className="control-panel">
        <h2 style={{ marginBottom: 'var(--space-md)' }}>⚙️ Generation Settings</h2>
        
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
          gap: 'var(--space-md)',
          marginBottom: 'var(--space-lg)'
        }}>
          <div className="form-group">
            <label>Number of Problems</label>
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
        </div>
        
        <div style={{ display: 'flex', gap: 'var(--space-md)', flexWrap: 'wrap' }}>
          <button 
            className="btn btn-primary" 
            onClick={handleGenerate}
            disabled={loading}
          >
            {loading ? '⏳ Generating & Validating...' : '🚀 Generate Problems'}
          </button>
          
          {problems.length > 0 && (
            <button className="btn btn-secondary" onClick={handleExport}>
              📥 Export Quiz (HTML)
            </button>
          )}
        </div>
        
        {error && (
          <div style={{
            marginTop: 'var(--space-md)',
            padding: 'var(--space-md)',
            background: 'var(--danger)',
            color: 'white',
            borderRadius: 'var(--radius-md)'
          }}>
            ⚠️ {error}
          </div>
        )}
      </div>
      
      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <p style={{ fontSize: '1.1rem', fontWeight: '600' }}>
            Generating {numProblems} validated problems...
          </p>
          <div style={{ 
            marginTop: 'var(--space-md)', 
            fontSize: '0.9rem', 
            color: 'var(--text-secondary)',
            lineHeight: '1.8'
          }}>
            <div>✓ Research Agent analyzing patterns</div>
            <div>✓ Generator creating unique problems</div>
            <div>✓ Solver A validating (algebraic)</div>
            <div>✓ Solver B validating (logical)</div>
            <div>✓ Checking for hallucinations</div>
          </div>
        </div>
      )}
      
      {problems.length > 0 && (
        <>
          <HallucinationMonitor problems={problems} />
          <ConfidenceHeatmap problems={problems} />
        </>
      )}
      
      {stats && <StatsPanel stats={stats} />}
      
      <ProblemViewer problems={problems} />
    </div>
  );
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
