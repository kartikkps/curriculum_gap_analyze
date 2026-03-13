import React from 'react';
import { AlertCircle, FileWarning } from 'lucide-react';
import './TopicList.css';

const TopicList = ({ missingTopics, weakTopics }) => {

  const getSeverityColor = (score) => {
    if (score >= 8) return 'high';
    if (score >= 5) return 'medium';
    return 'low';
  };

  if (!missingTopics?.length && !weakTopics?.length) return null;

  return (
    <div className="topic-list-container animate-in" style={{ animationDelay: '0.2s' }}>

      {missingTopics?.length > 0 && (
        <div className="topic-section glass-panel">
          <div className="section-header danger-text">
            <AlertCircle size={20}/>
            <h2>Missing Topics</h2>
            <span className="badge-count">{missingTopics.length}</span>
          </div>

          <ul className="topic-items">
            {missingTopics.map((topic, idx) => (
              <li key={idx} className="topic-item">
                <div className="topic-info">
                  <span className="topic-name">{topic.topic_name}</span>
                  {topic.reason && <p className="topic-desc">{topic.reason}</p>}
                </div>
                {topic.severity_score && (
                  <span className={`severity-badge ${getSeverityColor(topic.severity_score)}`}>
                    Severity: {topic.severity_score}/10
                  </span>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}

      {weakTopics?.length > 0 && (
        <div className="topic-section glass-panel mt-4">
          <div className="section-header warning-text">
            <FileWarning size={20}/>
            <h2>Weak Topics</h2>
            <span className="badge-count warning-bg">{weakTopics.length}</span>
          </div>

          <ul className="topic-items">
            {weakTopics.map((topic, idx) => (
              <li key={idx} className="topic-item weak">
                <span className="topic-name">{topic}</span>
                <span className="severity-badge medium">Needs Review</span>
              </li>
            ))}
          </ul>
        </div>
      )}

    </div>
  );
};

export default TopicList;
