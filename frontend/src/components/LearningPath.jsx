import React from 'react';
import { Route, CheckCircle2 } from 'lucide-react';
import './LearningPath.css';

const LearningPath = ({ path }) => {
  if (!path || path.length === 0) return null;

  return (
    <div className="learning-path-container glass-panel animate-in" style={{ animationDelay: '0.3s' }}>
      <div className="section-header info-text">
        <Route size={20}/>
        <h2>Recommended Learning Path</h2>
      </div>

      <div className="timeline">
        {path.map((topic, index) => (
          <div key={index} className="timeline-item">
            <div className="timeline-marker">
              <div className="marker-dot"></div>
              {index < path.length - 1 && <div className="marker-line"></div>}
            </div>
            <div className="timeline-content">
              <div className="step-number">Step {index + 1}</div>
              <div className="step-title">{topic}</div>
            </div>
          </div>
        ))}
      </div>

      <div className="path-footer">
        <CheckCircle2 size={16} className="success-icon"/>
        <p>Complete these to close the knowledge gap completely.</p>
      </div>
    </div>
  );
};

export default LearningPath;
