const ProblemViewer = ({ problems }) => {
  if (!problems || problems.length === 0) {
    return null;
  }
  
  return (
    <div>
      <h2 style={{ marginBottom: 'var(--space-lg)' }}>Generated Problems</h2>
      {problems.map((problem, idx) => (
        <div key={idx} className="problem-card">
          <div className="problem-header">
            <div className="problem-id">{problem.id}</div>
            <div style={{ display: 'flex', gap: 'var(--space-sm)', alignItems: 'center' }}>
              <span className={`difficulty-badge difficulty-${problem.difficulty.toLowerCase()}`}>
                {problem.difficulty}
              </span>
              <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                {problem.category}
              </span>
            </div>
          </div>
          
          <p className="problem-question">{problem.question}</p>
          
          <div className="options-grid">
            {Object.entries(problem.options).map(([key, value]) => (
              <div 
                key={key} 
                className={`option-card ${key === problem.correct_answer ? 'correct' : ''}`}
              >
                <strong>{key})</strong> {value}
              </div>
            ))}
          </div>
          
          {problem.solver_a_result && problem.solver_b_result && (
            <div className="validation-section">
              <h4>Validation Results</h4>
              <div className="solver-comparison">
                <div className="solver-result">
                  <h4>Solver A</h4>
                  <div className="value">{problem.solver_a_result.answer.toFixed(2)}</div>
                  <div className="confidence">
                    Confidence: {(problem.solver_a_result.confidence * 100).toFixed(0)}%
                  </div>
                </div>
                
                <div className="solver-result">
                  <h4>Ground Truth</h4>
                  <div className="value">{problem.ground_truth.toFixed(2)}</div>
                  <div className="confidence">SymPy Calculated</div>
                </div>
                
                <div className="solver-result">
                  <h4>Solver B</h4>
                  <div className="value">{problem.solver_b_result.answer.toFixed(2)}</div>
                  <div className="confidence">
                    Confidence: {(problem.solver_b_result.confidence * 100).toFixed(0)}%
                  </div>
                </div>
              </div>
              
              <div style={{ marginTop: 'var(--space-md)', textAlign: 'center' }}>
                <span style={{ 
                  padding: 'var(--space-xs) var(--space-md)', 
                  background: 'var(--success)', 
                  color: 'white', 
                  borderRadius: 'var(--radius-sm)',
                  fontWeight: '600'
                }}>
                  ✓ Validation Score: {(problem.validation_score * 100).toFixed(0)}%
                </span>
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};
