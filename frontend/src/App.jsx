import React, { useState } from 'react';
import { Target, HelpCircle } from 'lucide-react';
import CurriculumForm from './components/CurriculumForm';
import ResultsDashboard from './components/ResultsDashboard';
import TopicList from './components/TopicList';
import LearningPath from './components/LearningPath';
import { analyzeCurriculums } from './services/api';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);

  const handleAnalyze = async (target, student) => {
    setIsLoading(true);
    setError(null);
    setAnalysisResult(null);

    try {
      const data = await analyzeCurriculums(target, student);
      setAnalysisResult(data);

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
            <h2 className="animate-in pb-4">Analysis Report</h2>
            <ResultsDashboard metrics={analysisResult.metrics} />
            <TopicList
              missingTopics={analysisResult.result?.missing_topics}
              weakTopics={analysisResult.result?.weak_topics}
            />
            <LearningPath path={analysisResult.result?.recommended_learning_order} />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
