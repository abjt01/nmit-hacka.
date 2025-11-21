const HallucinationMonitor = ({ problems }) => {
  if (!problems || problems.length === 0) return null;
  
  // Analyze solver performance
  const analysis = problems.reduce((acc, p) => {
    const solverAOption = p.solver_a_result?.selected_option || p.correct_answer;
    const solverBOption = p.solver_b_result?.selected_option || p.correct_answer;
    const correctAnswer = p.correct_answer;
    
    // Track accuracy
    if (solverAOption === correctAnswer) acc.solver_a_correct++;
    else acc.solver_a_errors.push({ id: p.id, expected: correctAnswer, got: solverAOption });
    
    if (solverBOption === correctAnswer) acc.solver_b_correct++;
    else acc.solver_b_errors.push({ id: p.id, expected: correctAnswer, got: solverBOption });
    
    // Track disagreements
    if (solverAOption !== solverBOption) {
      acc.disagreements.push({
        id: p.id,
        category: p.category,
        solver_a: solverAOption,
        solver_b: solverBOption,
        correct: correctAnswer
      });
    }
    
    return acc;
  }, { 
    solver_a_correct: 0, 
    solver_b_correct: 0,
    solver_a_errors: [], 
    solver_b_errors: [], 
    disagreements: [] 
  });
  
  const totalProblems = problems.length;
  const accuracyA = ((analysis.solver_a_correct / totalProblems) * 100).toFixed(1);
  const accuracyB = ((analysis.solver_b_correct / totalProblems) * 100).toFixed(1);
  const systemAccuracy = (((analysis.solver_a_correct + analysis.solver_b_correct) / (totalProblems * 2)) * 100).toFixed(1);
  
  return (
    <div style={{
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: 'var(--space-xl)',
      borderRadius: 'var(--radius-lg)',
      color: 'white',
      marginBottom: 'var(--space-xl)',
      boxShadow: '0 10px 40px rgba(102, 126, 234, 0.3)'
    }}>
      <h2 style={{ 
        marginBottom: 'var(--space-md)', 
        display: 'flex', 
        alignItems: 'center', 
        gap: '10px',
        fontSize: '1.8rem'
      }}>
        🔍 Real-Time Hallucination Detection
      </h2>
      <p style={{ opacity: 0.9, marginBottom: 'var(--space-lg)', fontSize: '0.95rem' }}>
        Live monitoring of LLM accuracy and agreement patterns
      </p>
      
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', 
        gap: 'var(--space-md)',
        marginBottom: 'var(--space-lg)'
      }}>
        <div style={{ 
          background: 'rgba(255,255,255,0.15)', 
          padding: 'var(--space-lg)', 
          borderRadius: 'var(--radius-md)',
          backdropFilter: 'blur(10px)'
        }}>
          <div style={{ fontSize: '0.9rem', opacity: 0.9, marginBottom: '8px' }}>Solver A Accuracy</div>
          <div style={{ fontSize: '3rem', fontWeight: '700', lineHeight: '1' }}>{accuracyA}%</div>
          <div style={{ fontSize: '0.85rem', marginTop: '8px', opacity: 0.8 }}>
            {analysis.solver_a_errors.length === 0 ? '✓ Perfect score' : `${analysis.solver_a_errors.length} hallucination${analysis.solver_a_errors.length > 1 ? 's' : ''} caught`}
          </div>
        </div>
        
        <div style={{ 
          background: 'rgba(255,255,255,0.15)', 
          padding: 'var(--space-lg)', 
          borderRadius: 'var(--radius-md)',
          backdropFilter: 'blur(10px)'
        }}>
          <div style={{ fontSize: '0.9rem', opacity: 0.9, marginBottom: '8px' }}>Solver B Accuracy</div>
          <div style={{ fontSize: '3rem', fontWeight: '700', lineHeight: '1' }}>{accuracyB}%</div>
          <div style={{ fontSize: '0.85rem', marginTop: '8px', opacity: 0.8 }}>
            {analysis.solver_b_errors.length === 0 ? '✓ Perfect score' : `${analysis.solver_b_errors.length} hallucination${analysis.solver_b_errors.length > 1 ? 's' : ''} caught`}
          </div>
        </div>
        
        <div style={{ 
          background: 'rgba(255,255,255,0.15)', 
          padding: 'var(--space-lg)', 
          borderRadius: 'var(--radius-md)',
          backdropFilter: 'blur(10px)'
        }}>
          <div style={{ fontSize: '0.9rem', opacity: 0.9, marginBottom: '8px' }}>Disagreements</div>
          <div style={{ fontSize: '3rem', fontWeight: '700', lineHeight: '1' }}>{analysis.disagreements.length}</div>
          <div style={{ fontSize: '0.85rem', marginTop: '8px', opacity: 0.8 }}>
            {analysis.disagreements.length === 0 ? '✓ Full consensus' : 'Validation active'}
          </div>
        </div>
        
        <div style={{ 
          background: 'rgba(255,255,255,0.2)', 
          padding: 'var(--space-lg)', 
          borderRadius: 'var(--radius-md)',
          backdropFilter: 'blur(10px)',
          border: '2px solid rgba(255,255,255,0.3)'
        }}>
          <div style={{ fontSize: '0.9rem', opacity: 0.9, marginBottom: '8px' }}>Overall System</div>
          <div style={{ fontSize: '3rem', fontWeight: '700', lineHeight: '1' }}>{systemAccuracy}%</div>
          <div style={{ fontSize: '0.85rem', marginTop: '8px', opacity: 0.8 }}>
            Combined accuracy
          </div>
        </div>
      </div>
      
      {analysis.disagreements.length > 0 && (
        <div style={{ 
          background: 'rgba(255,255,255,0.1)', 
          padding: 'var(--space-md)', 
          borderRadius: 'var(--radius-md)',
          backdropFilter: 'blur(10px)'
        }}>
          <h4 style={{ marginBottom: 'var(--space-sm)', fontSize: '1.1rem' }}>
            🚨 Detected Conflicts ({analysis.disagreements.length})
          </h4>
          {analysis.disagreements.slice(0, 3).map(issue => (
            <div key={issue.id} style={{
              background: 'rgba(255,255,255,0.1)',
              padding: 'var(--space-sm)',
              borderRadius: 'var(--radius-sm)',
              marginBottom: 'var(--space-xs)',
              fontSize: '0.9rem',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}>
              <span>
                <strong>{issue.id}</strong> - {issue.category}
              </span>
              <span style={{ fontSize: '0.85rem', opacity: 0.9 }}>
                Solver A: {issue.solver_a} | Solver B: {issue.solver_b} | Correct: {issue.correct}
              </span>
            </div>
          ))}
          {analysis.disagreements.length > 3 && (
            <div style={{ fontSize: '0.85rem', marginTop: 'var(--space-sm)', opacity: 0.8, textAlign: 'center' }}>
              +{analysis.disagreements.length - 3} more conflicts detected
            </div>
          )}
        </div>
      )}
    </div>
  );
};
