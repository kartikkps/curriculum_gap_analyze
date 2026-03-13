import React, { useState } from 'react';
import { Target, HelpCircle } from 'lucide-react';
import CurriculumForm from './components/CurriculumForm';
import ResultsDashboard from './components/ResultsDashboard';
import TopicList from './components/TopicList';
import LearningPath from './components/LearningPath';
import RunTranscript from './components/RunTranscript';
import { analyzeCurriculums, getRunLogs } from './services/api';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [runLogs, setRunLogs] = useState([]);

  const handleReset = () => {
    setAnalysisResult(null);
    setRunLogs([]);
    setError(null);
  };

  const handleAnalyze = async (target, student, seed) => {
    setIsLoading(true);
    setError(null);
    setAnalysisResult(null);
    setRunLogs([]);

    try {
      const data = await analyzeCurriculums(target, student, seed);
      setAnalysisResult(data);
      
      if (data.run_id) {
        const logs = await getRunLogs(data.run_id);
        setRunLogs(logs);
      }

      setTimeout(() => setIsLoading(false), 800);
    } catch (err) {
      setError(err.message || 'An unexpected error occurred.');
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header animate-in">
        <Target size={48} color="var(--accent-primary)" style={{ marginBottom: '1rem' }} />
        <h1>Curriculum Gap Analyzer</h1>
        <p>Identify knowledge gaps instantly and build optimal learning paths.</p>
      </header>

      <main>
        <CurriculumForm onAnalyze={handleAnalyze} isLoading={isLoading} />

        {error && (
          <div className="glass-panel animate-in" style={{ padding: '1rem', marginTop: '2rem', borderLeft: '4px solid var(--accent-primary)' }}>
             <p style={{ color: 'var(--accent-primary)', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <HelpCircle size={18}/> {error}
             </p>
          </div>
        )}

        {analysisResult && !isLoading && (
          <div style={{ marginTop: '3rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingBottom: '1rem' }}>
              <h2 className="animate-in" style={{ margin: 0 }}>Analysis Report</h2>
              <button 
                onClick={handleReset}
                style={{
                  background: 'transparent',
                  border: '1px solid var(--border-subtle)',
                  color: 'var(--text-secondary)',
                  padding: '6px 12px',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontSize: '0.85rem'
                }}
              >
                Start Over
              </button>
            </div>
            
            <ResultsDashboard metrics={analysisResult.metrics} />
            <TopicList
              missingTopics={analysisResult.result?.missing_topics}
              weakTopics={analysisResult.result?.weak_topics}
            />
            <LearningPath path={analysisResult.result?.recommended_learning_order} />
            
            <RunTranscript logs={runLogs} />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
