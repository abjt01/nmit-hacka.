const AgentStatus = ({ agents }) => {
  if (!agents || agents.length === 0) {
    return null;
  }
  
  return (
    <div className="agent-status-grid">
      {agents.map((agent, idx) => (
        <div key={idx} className="agent-card">
          <div className="agent-header">
            <div className="agent-name">{agent.name}</div>
            <span className={`status-badge status-${agent.status}`}>
              {agent.status}
            </span>
          </div>
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${agent.progress}%` }}
            ></div>
          </div>
          {agent.message && (
            <p style={{ marginTop: '8px', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
              {agent.message}
            </p>
          )}
        </div>
      ))}
    </div>
  );
};
