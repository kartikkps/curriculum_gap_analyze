import React from 'react';
import { Target, Activity } from 'lucide-react';
import './ResultsDashboard.css';

const ResultsDashboard = ({ metrics }) => {
  if (!metrics) return null;

  const { gap_score, coverage_percentage, topic_similarity_score } = metrics;

  const gapPercentage = (gap_score * 100).toFixed(1);
  const coverage = coverage_percentage.toFixed(1);
  const similarity = (topic_similarity_score * 100).toFixed(1);

  return (
    <div className="dashboard-container animate-in" style={{ animationDelay: '0.1s' }}>
      <div className="metric-card glass-panel">
        <div className="metric-icon primary"><Target size={24}/></div>
        <div className="metric-content">
          <h3>Coverage</h3>
          <div className="metric-value">{coverage}%</div>
          <div className="progress-bar-bg">
            <div className="progress-bar-fill success" style={{ width: `${coverage}%` }}></div>
          </div>
        </div>
      </div>

      <div className="metric-card glass-panel">
        <div className="metric-icon secondary"><Activity size={24}/></div>
        <div className="metric-content">
          <h3>Gap Score</h3>
          <div className="metric-value">{gapPercentage}%</div>
          <div className="progress-bar-bg">
            <div className="progress-bar-fill danger" style={{ width: `${gapPercentage}%` }}></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsDashboard;
