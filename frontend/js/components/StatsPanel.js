const StatsPanel = ({ stats }) => {
  if (!stats) {
    return null;
  }
  
  return (
    <div>
      <h2 style={{ marginBottom: 'var(--space-lg)' }}>Performance Statistics</h2>
      
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{stats.total_generated || 0}</div>
          <div className="stat-label">Generated</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-value">{stats.total_valid || 0}</div>
          <div className="stat-label">Valid</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-value">
            {((stats.solver_agreement_rate || 0) * 100).toFixed(0)}%
          </div>
          <div className="stat-label">Solver Agreement</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-value">
            {((stats.ground_truth_accuracy || 0) * 100).toFixed(0)}%
          </div>
          <div className="stat-label">Ground Truth Accuracy</div>
        </div>
      </div>
      
      {stats.error_breakdown && Object.keys(stats.error_breakdown).length > 0 && (
        <div className="chart-container">
          <h3 style={{ marginBottom: 'var(--space-md)' }}>Error Breakdown</h3>
          <div style={{ display: 'grid', gap: 'var(--space-sm)' }}>
            {Object.entries(stats.error_breakdown).map(([error, count]) => (
              <div key={error} style={{ 
                display: 'flex', 
                justifyContent: 'space-between',
                padding: 'var(--space-sm)',
                background: 'var(--bg-primary)',
                borderRadius: 'var(--radius-sm)'
              }}>
                <span>{error.replace(/_/g, ' ')}</span>
                <strong>{count}</strong>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
