import axios from 'axios';

const API_URL = 'http://localhost:8001';

export const analyzeCurriculums = async (targetText, studentText) => {
  try {
    const response = await axios.post(`${API_URL}/analyze`, {
      target_curriculum: targetText,
      student_curriculum: studentText,
      seed: 42
    });
    return response.data;
  } catch (error) {
    console.error("API Error during analysis:", error);
    throw new Error(error.response?.data?.detail || "Failed to analyze curriculums.");
  }
};
