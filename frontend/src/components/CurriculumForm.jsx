import React, { useState } from 'react';
import { Loader2, ArrowRight, BookOpen } from 'lucide-react';
import './CurriculumForm.css';

const CurriculumForm = ({ onAnalyze, isLoading }) => {
  const [target, setTarget] = useState('');
  const [student, setStudent] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (target.trim() && student.trim()) {
      onAnalyze(target, student);
    }
  };

  return (
    <div className="form-container glass-panel animate-in">
      <div className="form-header">
        <h2>Input Curriculums</h2>
        <p>Paste the syllabuses to identify knowledge gaps</p>
      </div>

      <form onSubmit={handleSubmit} className="curriculum-form">
        <div className="input-group">
          <div className="textarea-wrapper">
            <label htmlFor="target"><BookOpen size={16}/> Reference Curriculum (Target)</label>
            <textarea
              id="target"
              value={target}
              onChange={(e) => setTarget(e.target.value)}
              placeholder="e.g. Topics, chapters, or syllabus text..."
              required
            />
          </div>

          <div className="textarea-wrapper">
            <label htmlFor="student"><BookOpen size={16}/> Completed Curriculum (Student)</label>
            <textarea
              id="student"
              value={student}
              onChange={(e) => setStudent(e.target.value)}
              placeholder="e.g. Topics currently known or studied..."
              required
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={isLoading || !target.trim() || !student.trim()}
          className={`analyze-btn ${isLoading ? 'loading' : ''}`}
        >
          {isLoading ? (
            <><Loader2 className="spinner" size={18} /> Analyzing Gaps...</>
          ) : (
            <>Analyze Gaps <ArrowRight size={18} /></>
          )}
        </button>
      </form>
    </div>
  );
};

export default CurriculumForm;
