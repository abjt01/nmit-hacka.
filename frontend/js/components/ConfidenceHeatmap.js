const ConfidenceHeatmap = ({ problems }) => {
  if (!problems || problems.length === 0) return null;
  
  // Group by category and calculate average confidence
  const categoryData = problems.reduce((acc, p) => {
    const cat = p.category;
    if (!acc[cat]) {
      acc[cat] = {
        count: 0,
        total_confidence_a: 0,
        total_confidence_b: 0,
        problems: []
      };
    }
    
    acc[cat].count++;
    acc[cat].total_confidence_a += p.solver_a_result?.confidence || 0;
    acc[cat].total_confidence_b += p.solver_b_result?.confidence || 0;
    acc[cat].problems.push(p);
    
    return acc;
  }, {});
  
  // Calculate averages
  const heatmapData = Object.entries(categoryData).map(([category, data]) => {
    const avgConfA = (data.total_confidence_a / data.count) * 100;
    const avgConfB = (data.total_confidence_b / data.count) * 100;
    const avgOverall = (avgConfA + avgConfB) / 2;
    
    return {
      category,
      avgConfA,
      avgConfB,
      avgOverall,
      count: data.count
    };
  }).sort((a, b) => b.avgOverall - a.avgOverall);
  
  const getColor = (value) => {
    if (value >= 90) return '#10b981';
    if (value >= 75) return '#f59e0b';
    if (value >= 60) return '#ef4444';
    return '#dc2626';
  };
  
  return (
    <div style={{ 
      background: 'var(--bg-secondary)', 
      padding: 'var(--space-xl)', 
      borderRadius: 'var(--radius-lg)', 
      marginBottom: 'var(--space-xl)',
      boxShadow: '0 4px 12px var(--shadow)'
    }}>
      <h3 style={{ marginBottom: 'var(--space-md)', fontSize: '1.5rem' }}>
        🔥 Confidence Heatmap by Category
      </h3>
      <p style={{ color: 'var(--text-secondary)', marginBottom: 'var(--space-lg)', fontSize: '0.95rem' }}>
        Shows which problem types are easiest/hardest for the LLMs to solve
      </p>
      
      {heatmapData.map(item => {
        const color = getColor(item.avgOverall);
        
        return (
          <div key={item.category} style={{ marginBottom: 'var(--space-lg)' }}>
            <div style={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              marginBottom: 'var(--space-sm)',
              alignItems: 'center'
            }}>
              <div>
                <span style={{ fontWeight: '600', fontSize: '1.05rem' }}>{item.category}</span>
                <span style={{ 
                  marginLeft: 'var(--space-sm)', 
                  fontSize: '0.85rem', 
                  color: 'var(--text-secondary)' 
                }}>
                  ({item.count} problem{item.count > 1 ? 's' : ''})
                </span>
              </div>
              <span style={{ 
                fontWeight: '700', 
                color: color,
                fontSize: '1.2rem'
              }}>
                {item.avgOverall.toFixed(0)}%
              </span>
            </div>
            
            {/* Overall confidence bar */}
            <div style={{ 
              background: 'var(--bg-tertiary)', 
              borderRadius: 'var(--radius-base)', 
              height: '32px',
              marginBottom: 'var(--space-xs)',
              overflow: 'hidden',
              position: 'relative'
            }}>
              <div style={{ 
                width: `${item.avgOverall}%`, 
                background: `linear-gradient(90deg, ${color}, ${color}dd)`,
                height: '100%',
                transition: 'width 0.8s cubic-bezier(0.16, 1, 0.3, 1)',
                display: 'flex',
                alignItems: 'center',
                paddingLeft: 'var(--space-md)',
                color: 'white',
                fontWeight: '600',
                fontSize: '0.9rem'
              }}>
                {item.avgOverall >= 20 && `${item.avgOverall.toFixed(0)}% confidence`}
              </div>
            </div>
            
            {/* Solver breakdown */}
            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: '1fr 1fr', 
              gap: 'var(--space-xs)',
              fontSize: '0.85rem'
            }}>
              <div style={{ 
                background: 'var(--bg-primary)', 
                padding: 'var(--space-xs) var(--space-sm)',
                borderRadius: 'var(--radius-sm)',
                display: 'flex',
                justifyContent: 'space-between'
              }}>
                <span style={{ color: 'var(--text-secondary)' }}>Solver A:</span>
                <span style={{ fontWeight: '600' }}>{item.avgConfA.toFixed(0)}%</span>
              </div>
              <div style={{ 
                background: 'var(--bg-primary)', 
                padding: 'var(--space-xs) var(--space-sm)',
                borderRadius: 'var(--radius-sm)',
                display: 'flex',
                justifyContent: 'space-between'
              }}>
                <span style={{ color: 'var(--text-secondary)' }}>Solver B:</span>
                <span style={{ fontWeight: '600' }}>{item.avgConfB.toFixed(0)}%</span>
              </div>
            </div>
          </div>
        );
      })}
      
      <div style={{ 
        marginTop: 'var(--space-xl)', 
        paddingTop: 'var(--space-md)',
        borderTop: '1px solid var(--border-color)',
        fontSize: '0.85rem',
        color: 'var(--text-secondary)'
      }}>
        <strong>Interpretation:</strong> Higher confidence indicates the LLMs find these problems easier to solve accurately. 
        Lower confidence suggests more complex reasoning required.
      </div>
    </div>
  );
};
