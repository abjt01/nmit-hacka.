const App = () => {
  const [loading, setLoading] = React.useState(false);
  const [problems, setProblems] = React.useState([]);
  const [stats, setStats] = React.useState(null);
  const [agents, setAgents] = React.useState([]);
  const [numProblems, setNumProblems] = React.useState(12);
  
  const handleGenerate = async () => {
    setLoading(true);
    setProblems([]);
    setStats(null);
    
    try {
      const config = {
        num_problems: parseInt(numProblems),
        categories: [
          "Time, Speed & Distance",
          "Work & Time",
          "Pipes & Cisterns"
        ],
        difficulty_distribution: {
          "EASY": 4,
          "MEDIUM": 5,
          "HARD": 3
        }
      };
      
      const result = await api.generateProblems(config);
      
      setProblems(result.problems);
      setStats(result.stats);
    } catch (error) {
      alert('Error generating problems: ' + error.message);
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
      const result = await api.exportHTML(problems);
      const blob = new Blob([result.html], { type: 'text/html' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'quant-quiz.html';
      a.click();
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
          <label>Number of Problems</label>
          <input 
            type="number" 
            min="1" 
            max="20" 
            value={numProblems}
            onChange={(e) => setNumProblems(e.target.value)}
          />
        </div>
        
        <div style={{ display: 'flex', gap: 'var(--space-md)' }}>
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
          <p>Generating and validating problems...</p>
        </div>
      )}
      
      <AgentStatus agents={agents} />
      
      {stats && <StatsPanel stats={stats} />}
      
      <ProblemViewer problems={problems} />
    </div>
  );
};

// Render
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
