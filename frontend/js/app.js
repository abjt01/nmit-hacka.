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
      console.log('🚀 Sending request to backend...');
      
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
      
      console.log('📡 Response status:', response.status);
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Server error: ${errorText}`);
      }
      
      const result = await response.json();
      console.log('✅ Result received:', result);
      console.log('📊 Problems count:', result.problems?.length);
      
      // FIXED: Ensure problems array is set correctly
      if (result.problems && Array.isArray(result.problems)) {
        setProblems(result.problems);
        setStats(result.stats);
        console.log('✓ Problems state updated:', result.problems.length, 'problems');
      } else {
        console.error('❌ Invalid response format:', result);
        setError('Invalid response format from server');
      }
      
    } catch (error) {
      console.error('❌ Error:', error);
      setError(error.message);
      alert(`Error generating problems:\n\n${error.message}\n\nCheck:\n1. Backend running on port 8000\n2. GROQ_API_KEY in .env\n3. Browser console (F12) for details`);
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
      a.download = 'polysolve-ai-quiz.html';
      a.click();
      URL.revokeObjectURL(url);
      
      console.log('✅ Quiz exported successfully');
    } catch (error) {
      console.error('❌ Export error:', error);
      alert('Error exporting: ' + error.message);
    }
  };
  
  return (
    <div className="container">
      <Header />
      
      <div className="control-panel">
        <h2 style={{ marginBottom: 'var(--space-lg)' }}>⚙️ Generation Settings</h2>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 'var(--space-md)' }}>
          <div className="form-group">
            <label>Number of Problems</label>
            <input 
              type="number" 
              min="1" 
              max="20" 
              value={numProblems}
              onChange={(e) => setNumProblems(e.target.value)}
              placeholder="1-20"
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
        
        <div style={{ display: 'flex', gap: 'var(--space-md)', marginTop: 'var(--space-lg)', flexWrap: 'wrap' }}>
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
            Generating {numProblems} problems for: {category}
          </p>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginTop: '10px' }}>
            Multi-agent validation in progress...
          </p>
          <div style={{ marginTop: 'var(--space-md)', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
            <div>✓ Research Agent analyzing patterns</div>
            <div>✓ Generator creating problems</div>
            <div>✓ Solver A validating (algebraic)</div>
            <div>✓ Solver B validating (logical)</div>
            <div>✓ SymPy verifying ground truth</div>
          </div>
        </div>
      )}
      
      {stats && <StatsPanel stats={stats} />}
      
      {problems.length > 0 && (
        <div style={{
          marginBottom: 'var(--space-lg)',
          padding: 'var(--space-md)',
          background: 'var(--success)',
          color: 'white',
          borderRadius: 'var(--radius-md)',
          textAlign: 'center',
          fontWeight: '600'
        }}>
          ✅ Successfully generated {problems.length} validated problems!
        </div>
      )}
      
      <ProblemViewer problems={problems} />
    </div>
  );
};

// Render
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
