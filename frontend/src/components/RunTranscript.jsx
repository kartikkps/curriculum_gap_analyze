import React from 'react';
import { Activity, Clock, Terminal, ChevronRight } from 'lucide-react';
import './RunTranscript.css';

const RunTranscript = ({ logs }) => {
  if (!logs || logs.length === 0) return null;

  return (
    <div className="transcript-container glass-panel animate-in" style={{ animationDelay: '0.4s' }}>
      <div className="section-header">
        <Terminal size={20}/>
        <h2>Agent Run Transcript</h2>
      </div>

      <div className="transcript-logs">
        {logs.map((log, index) => {
          const isTransition = !!log.transition;
          const isTool = !!log.tool;
          
          return (
            <div key={index} className={`log-entry ${isTransition ? 'transition' : isTool ? 'tool' : 'info'}`}>
              <div className="log-timestamp">
                 <Clock size={12}/> {new Date(log.timestamp).toLocaleTimeString([], { hour12: false, hour: '2-digit', minute:'2-digit', second:'2-digit'})}
              </div>
              
              {isTransition && (
                <div className="log-content transition-content">
                  <Activity size={14} className="icon-pulse"/>
                  <span className="state-pill">{log.transition.from}</span>
                  <ChevronRight size={14} className="chevron"/>
                  <span className="state-pill active">{log.transition.to}</span>
                </div>
              )}

              {isTool && (
                <div className="log-content tool-content">
                   <div className="tool-header">
                      <span className="tool-name">Tool: {log.tool}</span>
                   </div>
                   {log.inputs && (
                     <div className="code-block">
                        <span className="code-label">Input</span>
                        <pre>{JSON.stringify(log.inputs, null, 2)}</pre>
                     </div>
                   )}
                   {log.outputs && (
                     <div className="code-block success">
                        <span className="code-label">Output</span>
                        <pre>{JSON.stringify(log.outputs, null, 2)}</pre>
                     </div>
                   )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default RunTranscript;
