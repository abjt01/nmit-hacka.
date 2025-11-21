const Header = () => {
  return (
    <div className="header">
      <div className="header-content">
        <div>
          <h1>🧮 PolySolve AI</h1>
          <p>Multi-Agent Quantitative Problem Generator</p>
          <p style={{ fontSize: '0.9rem', opacity: 0.9, marginTop: '5px' }}>
            Triple Validated: Research → Generator → Solver A → Solver B → SymPy
          </p>
        </div>
        <ThemeToggle />
      </div>
    </div>
  );
};
