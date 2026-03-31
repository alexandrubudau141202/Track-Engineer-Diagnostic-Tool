// useAPI.ts - Custom hook for backend API calls

import { useState, useCallback } from "react";
import { ScenarioRequest } from "../types/Scenario";
import { DiagnosisResponse } from "../types/Diagnosis";

interface UseAPIReturn {
  loading: boolean;
  error: string | null;
  result: DiagnosisResponse | null;
  diagnose: (scenario: ScenarioRequest) => Promise<void>;
  validateScenario: (scenario: ScenarioRequest) => Promise<boolean>;
  uploadTelemetry: (file: File) => Promise<any>;
  downloadPDF: (scenarioId: string) => void;
  reset: () => void;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const useAPI = (): UseAPIReturn => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<DiagnosisResponse | null>(null);

  const reset = useCallback(() => {
    setError(null);
    setResult(null);
    setLoading(false);
  }, []);

  const diagnose = useCallback(async (scenario: ScenarioRequest) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/api/scenarios/diagnose`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(scenario),
      });

      if (!response.ok) {
        throw new Error(`Diagnosis failed: ${response.statusText}`);
      }

      const data: DiagnosisResponse = await response.json();
      setResult(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Unknown error";
      setError(errorMessage);
      setResult(null);
    } finally {
      setLoading(false);
    }
  }, []);

  const validateScenario = useCallback(async (scenario: ScenarioRequest): Promise<boolean> => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/scenarios/validate-scenario`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(scenario),
      });

      if (!response.ok) {
        throw new Error("Validation failed");
      }

      const data = await response.json();
      return data.status === "valid";
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Validation error";
      setError(errorMessage);
      return false;
    }
  }, []);

  const uploadTelemetry = useCallback(async (file: File) => {
    setLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_BASE_URL}/api/scenarios/upload-telemetry`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }

      const data = await response.json();
      return data;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Upload failed";
      setError(errorMessage);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const downloadPDF = useCallback((scenarioId: string) => {
    const link = document.createElement("a");
    link.href = `${API_BASE_URL}/api/scenarios/reports/${scenarioId}.pdf`;
    link.download = `gt3r_diagnosis_${scenarioId}.pdf`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }, []);

  return {
    loading,
    error,
    result,
    diagnose,
    validateScenario,
    uploadTelemetry,
    downloadPDF,
    reset,
  };
};