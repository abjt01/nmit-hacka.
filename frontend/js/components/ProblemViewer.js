const ProblemViewer = ({ problems }) => {
  const [selectedAnswers, setSelectedAnswers] = React.useState({});
  const [showAnswers, setShowAnswers] = React.useState({});
  
  if (!problems || problems.length === 0) {
    return null;
  }
  
  const handleAnswerSelect = (problemId, answer) => {
    setSelectedAnswers(prev => ({ ...prev, [problemId]: answer }));
  };
  
  const toggleAnswer = (problemId) => {
    setShowAnswers(prev => ({ ...prev, [problemId]: !prev[problemId] }));
  };
  
  return (
    <div>
      <h2 style={{ marginBottom: 'var(--space-lg)' }}>
        📚 Generated Problems ({problems.length})
      </h2>
      
      {problems.map((problem, idx) => {
        const userAnswer = selectedAnswers[problem.id];
        const isCorrect = userAnswer === problem.correct_answer;
        const showAnswer = showAnswers[problem.id];
        
        return (
          <div key={idx} className="problem-card">
            <div className="problem-header">
              <div className="problem-id">{problem.id}</div>
              <div style={{ display: 'flex', gap: 'var(--space-sm)', alignItems: 'center' }}>
                <span style={{ 
                  fontSize: '0.85rem', 
                  padding: '4px 12px',
                  background: 'var(--bg-tertiary)',
                  borderRadius: 'var(--radius-sm)',
                  fontWeight: '600'
                }}>
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
            
            {/* Answer Selection Dropdown */}
            <div style={{ margin: 'var(--space-lg) 0' }}>
              <label style={{ 
                display: 'block',
                marginBottom: 'var(--space-sm)',
                fontWeight: '600',
                color: 'var(--text-primary)'
              }}>
                Your Answer:
              </label>
              <select 
                className="form-control"
                value={userAnswer || ''}
                onChange={(e) => handleAnswerSelect(problem.id, e.target.value)}
                style={{ 
                  padding: 'var(--space-md)',
                  fontSize: '1rem',
                  maxWidth: '400px'
                }}
              >
                <option value="">-- Select your answer --</option>
                <option value="A">A) {problem.options.A}</option>
                <option value="B">B) {problem.options.B}</option>
                <option value="C">C) {problem.options.C}</option>
                <option value="D">D) {problem.options.D}</option>
              </select>
              
              {userAnswer && (
                <div style={{ marginTop: 'var(--space-md)' }}>
                  <button 
                    className="btn btn-primary"
                    onClick={() => toggleAnswer(problem.id)}
                    style={{ padding: 'var(--space-sm) var(--space-lg)' }}
                  >
                    {showAnswer ? '🙈 Hide Answer' : '👁️ Check Answer'}
                  </button>
                  
                  {showAnswer && (
                    <div style={{
                      marginTop: 'var(--space-md)',
                      padding: 'var(--space-md)',
                      background: isCorrect ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                      border: `2px solid ${isCorrect ? 'var(--success)' : 'var(--danger)'}`,
                      borderRadius: 'var(--radius-md)'
                    }}>
                      {isCorrect ? (
                        <div style={{ color: 'var(--success)', fontWeight: '600' }}>
                          ✅ Correct! Well done!
                        </div>
                      ) : (
                        <div>
                          <div style={{ color: 'var(--danger)', fontWeight: '600', marginBottom: 'var(--space-sm)' }}>
                            ❌ Incorrect. The correct answer is: {problem.correct_answer}
                          </div>
                          <div style={{ color: 'var(--text-secondary)' }}>
                            Correct option: {problem.options[problem.correct_answer]}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
            
            {/* Solver Comparison Section */}
            {problem.solver_a_result && problem.solver_b_result && (
              <div className="validation-section">
                <h4 style={{ marginBottom: 'var(--space-md)' }}>
                  🔬 Multi-Agent Validation
                </h4>
                
                <div className="solver-comparison">
                  <div className="solver-result">
                    <h4>Solver A</h4>
                    <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '5px' }}>
                      Algebraic Approach
                    </div>
                    <div className="value">
                      {problem.solver_a_result.answer.toFixed(3)}
                    </div>
                    <div className="confidence">
                      Confidence: {(problem.solver_a_result.confidence * 100).toFixed(0)}%
                    </div>
                    <div style={{ 
                      marginTop: 'var(--space-sm)', 
                      fontSize: '0.9rem',
                      color: 'var(--accent-primary)',
                      fontWeight: '600'
                    }}>
                      Selected: {problem.correct_answer}
                    </div>
                  </div>
                  
                  <div className="solver-result" style={{ borderLeft: '2px solid var(--border-color)', borderRight: '2px solid var(--border-color)' }}>
                    <h4>Agreement</h4>
                    <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '5px' }}>
                      Validation Status
                    </div>
                    <div style={{ 
                      fontSize: '3rem',
                      color: 'var(--success)'
                    }}>
                      {problem.validation_score ? '✓' : '○'}
                    </div>
                    <div className="confidence">
                      {problem.validation_score ? `${(problem.validation_score * 100).toFixed(0)}% Match` : 'Validating'}
                    </div>
                  </div>
                  
                  <div className="solver-result">
                    <h4>Solver B</h4>
                    <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '5px' }}>
                      Logical Approach
                    </div>
                    <div className="value">
                      {problem.solver_b_result.answer.toFixed(3)}
                    </div>
                    <div className="confidence">
                      Confidence: {(problem.solver_b_result.confidence * 100).toFixed(0)}%
                    </div>
                    <div style={{ 
                      marginTop: 'var(--space-sm)', 
                      fontSize: '0.9rem',
                      color: 'var(--accent-primary)',
                      fontWeight: '600'
                    }}>
                      Selected: {problem.correct_answer}
                    </div>
                  </div>
                </div>
              </div>
            )}
            
            {/* Solution (only visible after checking answer) */}
            {showAnswer && (
              <div style={{
                marginTop: 'var(--space-lg)',
                padding: 'var(--space-md)',
                background: 'var(--bg-tertiary)',
                borderRadius: 'var(--radius-md)',
                borderLeft: '4px solid var(--accent-primary)'
              }}>
                <h4 style={{ marginBottom: 'var(--space-sm)', color: 'var(--accent-primary)' }}>
                  💡 Detailed Solution
                </h4>
                <div style={{ lineHeight: '1.7', color: 'var(--text-primary)' }}>
                  {problem.explanation}
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};
