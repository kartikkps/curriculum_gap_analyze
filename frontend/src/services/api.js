import axios from 'axios';

const API_URL = 'http://localhost:8001';

export const analyzeCurriculums = async (targetText, studentText, seedValue = 42) => {
  try {
    const response = await axios.post(`${API_URL}/analyze`, {
      target_curriculum: targetText,
      student_curriculum: studentText,
      seed: seedValue
    });
    return response.data;
  } catch (error) {
    console.error("API Error during analysis:", error);
    throw new Error(error.response?.data?.detail || "Failed to analyze curriculums.");
  }
};

export const getRunLogs = async (runId) => {
  try {
    const response = await axios.get(`${API_URL}/runs/${runId}`);
    return response.data.logs;
  } catch (error) {
    console.error("Failed to fetch run logs:", error);
    return [];
  }
};
