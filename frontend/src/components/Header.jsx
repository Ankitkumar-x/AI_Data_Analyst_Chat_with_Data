function Header() {
  return (
    <header className="app-header">
      <div>
        <h1>AI Data Analyst</h1>
        <p>Chat with Your Data</p>
      </div>

      <div className="header-status">
        <span className="status-dot"></span>
        AI Ready
      </div>
    </header>
  );
}

export default Header;