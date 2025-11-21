const StatsPanel = ({ stats }) => {
  if (!stats) {
    return null;
  }
  
  return (
    <div>
      <h2 style={{ marginBottom: 'var(--space-lg)' }}>📊 Generation Statistics</h2>
      
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{stats.total_generated || 0}</div>
          <div className="stat-label">Problems Generated</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-value">{stats.total_api_calls || 0}</div>
          <div className="stat-label">API Calls Used</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-value">{stats.api_efficiency || 'N/A'}</div>
          <div className="stat-label">Efficiency Ratio</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-value">
            {stats.solver_agreement_rate 
              ? (stats.solver_agreement_rate * 100).toFixed(0) + '%'
              : 'N/A'}
          </div>
          <div className="stat-label">Solver Agreement</div>
        </div>
        
        {/* REMOVED: SymPy Verified stat */}
      </div>
      
      {stats.validation_failures && Object.keys(stats.validation_failures).length > 0 && (
        <div className="chart-container" style={{ marginTop: 'var(--space-lg)' }}>
          <h3 style={{ marginBottom: 'var(--space-md)' }}>⚠️ Validation Issues</h3>
          <div style={{ display: 'grid', gap: 'var(--space-sm)' }}>
            {Object.entries(stats.validation_failures).map(([error, count]) => (
              <div key={error} style={{ 
                display: 'flex', 
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: 'var(--space-md)',
                background: 'var(--bg-primary)',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-color)'
              }}>
                <span style={{ textTransform: 'capitalize' }}>
                  {error.replace(/_/g, ' ')}
                </span>
                <strong style={{ 
                  padding: '4px 12px',
                  background: 'var(--warning)',
                  color: 'white',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: '0.9rem'
                }}>
                  {count}
                </strong>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
