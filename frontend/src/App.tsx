import "./styles.css";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export function App() {
  return (
    <main className="app-shell">
      <section className="workspace">
        <div>
          <p className="eyebrow">Tartip</p>
          <h1>Local infrastructure skeleton</h1>
          <p className="summary">
            Minimal frontend for the next BIM5D Cost-Schedule Matching
            development steps.
          </p>
        </div>
        <dl className="status-grid" aria-label="Local environment parameters">
          <div>
            <dt>Backend API</dt>
            <dd>{apiBaseUrl}</dd>
          </div>
          <div>
            <dt>Health endpoint</dt>
            <dd>{apiBaseUrl}/health</dd>
          </div>
        </dl>
      </section>
    </main>
  );
}
