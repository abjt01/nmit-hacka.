const ProblemViewer = ({ problems }) => {
  if (!problems || problems.length === 0) {
    return null;
  }
  
  return (
    <div>
      <h2 style={{ marginBottom: 'var(--space-lg)' }}>
        📚 Generated Problems ({problems.length})
      </h2>
      
      {problems.map((problem, idx) => (
        <div key={idx} className="problem-card">
          <div className="problem-header">
            <div className="problem-id">{problem.id}</div>
            <div style={{ display: 'flex', gap: 'var(--space-sm)', alignItems: 'center' }}>
              <span className={`difficulty-badge difficulty-medium`}>
                {problem.category}
              </span>
              <span style={{ 
                fontSize: '0.85rem', 
                padding: '4px 12px',
                background: 'var(--success)',
                color: 'white',
                borderRadius: 'var(--radius-sm)',
                fontWeight: '600'
              }}>
                ✓ {problem.validation_status}
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
          
          {/* Solver Comparison Section */}
          {problem.solver_a_result && problem.solver_b_result && (
            <div className="validation-section">
              <h4 style={{ marginBottom: 'var(--space-md)' }}>
                🔬 Triple Validation Results
              </h4>
              
              <div className="solver-comparison">
                <div className="solver-result">
                  <h4>Solver A</h4>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '5px' }}>
                    Algebraic
                  </div>
                  <div className="value">
                    {problem.solver_a_result.answer.toFixed(3)}
                  </div>
                  <div className="confidence">
                    Confidence: {(problem.solver_a_result.confidence * 100).toFixed(0)}%
                  </div>
                  <div style={{ 
                    marginTop: 'var(--space-sm)', 
                    fontSize: '0.85rem',
                    color: 'var(--text-secondary)',
                    fontStyle: 'italic'
                  }}>
                    Selected: <strong>{problem.correct_answer}</strong>
                  </div>
                </div>
                
                <div className="solver-result">
                  <h4>Ground Truth</h4>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '5px' }}>
                    SymPy Calculated
                  </div>
                  <div className="value" style={{ color: 'var(--success)' }}>
                    {problem.ground_truth ? problem.ground_truth.toFixed(3) : 'N/A'}
                  </div>
                  <div className="confidence">
                    Mathematical Truth
                  </div>
                  <div style={{ 
                    marginTop: 'var(--space-sm)', 
                    fontSize: '0.85rem',
                    color: 'var(--success)',
                    fontWeight: '600'
                  }}>
                    ✓ Verified
                  </div>
                </div>
                
                <div className="solver-result">
                  <h4>Solver B</h4>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '5px' }}>
                    Logical
                  </div>
                  <div className="value">
                    {problem.solver_b_result.answer.toFixed(3)}
                  </div>
                  <div className="confidence">
                    Confidence: {(problem.solver_b_result.confidence * 100).toFixed(0)}%
                  </div>
                  <div style={{ 
                    marginTop: 'var(--space-sm)', 
                    fontSize: '0.85rem',
                    color: 'var(--text-secondary)',
                    fontStyle: 'italic'
                  }}>
                    Selected: <strong>{problem.correct_answer}</strong>
                  </div>
                </div>
              </div>
              
              {problem.validation_score && (
                <div style={{ 
                  marginTop: 'var(--space-md)', 
                  textAlign: 'center',
                  padding: 'var(--space-md)',
                  background: 'var(--bg-primary)',
                  borderRadius: 'var(--radius-md)'
                }}>
                  <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '5px' }}>
                    Overall Validation Score
                  </div>
                  <div style={{ 
                    fontSize: '2rem',
                    fontWeight: '700',
                    color: 'var(--success)'
                  }}>
                    {(problem.validation_score * 100).toFixed(0)}%
                  </div>
                </div>
              )}
            </div>
          )}
          
          {/* Explanation Section */}
          <div style={{
            marginTop: 'var(--space-lg)',
            padding: 'var(--space-md)',
            background: 'var(--bg-tertiary)',
            borderRadius: 'var(--radius-md)',
            borderLeft: '4px solid var(--accent-primary)'
          }}>
            <h4 style={{ marginBottom: 'var(--space-sm)', color: 'var(--accent-primary)' }}>
              💡 Solution
            </h4>
            <div style={{ lineHeight: '1.7', color: 'var(--text-primary)' }}>
              {problem.explanation}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};
