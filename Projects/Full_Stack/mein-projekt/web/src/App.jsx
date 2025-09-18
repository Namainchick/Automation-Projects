import { useState } from "react";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function App() {
  const [a, setA] = useState("2");
  const [b, setB] = useState("3");
  const [sum, setSum] = useState(null);

  const [text, setText] = useState("Hallo");
  const [analysis, setAnalysis] = useState(null);

  const [loadingAdd, setLoadingAdd] = useState(false);
  const [loadingAnalyze, setLoadingAnalyze] = useState(false);
  const [error, setError] = useState(null);

  async function callAdd() {
    setLoadingAdd(true);
    setError(null);
    try {
      const res = await fetch(`${API}/add`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          a: Number.isFinite(Number(a)) ? Number(a) : 0,
          b: Number.isFinite(Number(b)) ? Number(b) : 0,
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setSum(data.result);
    } catch (e) {
      setError(e.message || "Fehler bei /add");
    } finally {
      setLoadingAdd(false);
    }
  }

  async function callAnalyze() {
    setLoadingAnalyze(true);
    setError(null);
    try {
      const res = await fetch(`${API}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setAnalysis(data);
    } catch (e) {
      setError(e.message || "Fehler bei /analyze");
    } finally {
      setLoadingAnalyze(false);
    }
  }

  return (
    <main style={{ maxWidth: 720, margin: "0 auto", padding: 24 }}>
      <h1>Frontend ↔ API ↔ Core (React + JSX)</h1>

      {error && (
        <div style={{ background: "#fee", border: "1px solid #f99", padding: 12, marginBottom: 16 }}>
          <strong>Fehler:</strong> {error}
        </div>
      )}

      <section style={{ marginBottom: 32 }}>
        <h2>Add</h2>
        <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 8 }}>
          <input
            value={a}
            onChange={(e) => setA(e.target.value)}
            placeholder="a"
            style={{ padding: 8, border: "1px solid #ddd", borderRadius: 6 }}
          />
          <input
            value={b}
            onChange={(e) => setB(e.target.value)}
            placeholder="b"
            style={{ padding: 8, border: "1px solid #ddd", borderRadius: 6 }}
          />
          <button
            onClick={callAdd}
            disabled={loadingAdd}
            style={{ padding: "8px 12px", borderRadius: 8, border: "1px solid #000", background: "#000", color: "#fff" }}
          >
            {loadingAdd ? "Berechne…" : "Berechnen"}
          </button>
        </div>
        {sum !== null && <p>Summe: <strong>{sum}</strong></p>}
      </section>

      <section>
        <h2>Analyze</h2>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={4}
          style={{ width: "100%", padding: 8, border: "1px solid #ddd", borderRadius: 6, marginBottom: 8 }}
        />
        <button
          onClick={callAnalyze}
          disabled={loadingAnalyze}
          style={{ padding: "8px 12px", borderRadius: 8, border: "1px solid #000", background: "#000", color: "#fff" }}
        >
          {loadingAnalyze ? "Analysiere…" : "Analysieren"}
        </button>

        {analysis && (
          <pre style={{ background: "#f7f7f7", padding: 12, borderRadius: 8, marginTop: 12 }}>
            {JSON.stringify(analysis, null, 2)}
          </pre>
        )}
      </section>

      <hr style={{ margin: "24px 0" }} />

      <p style={{ fontSize: 14, color: "#555" }}>
        API-URL: <code>{API}</code> (setze <code>VITE_API_URL</code> in <code>web/.env</code>)
      </p>
    </main>
  );
}
