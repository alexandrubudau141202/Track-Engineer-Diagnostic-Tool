// useScenario.ts - Custom hook for managing scenario state

import { useState } from "react";
import { ScenarioRequest, CarSetup, DriverFeedback, TrackConditions, TelemetryPoint, NOMINAL_SETUP, NOMINAL_FEEDBACK, NOMINAL_CONDITIONS } from "../types/Scenario";

export interface UseScenarioReturn {
  scenario: ScenarioRequest;
  updateSetup: (setup: Partial<CarSetup>) => void;
  updateFeedback: (feedback: Partial<DriverFeedback>) => void;
  updateConditions: (conditions: Partial<TrackConditions>) => void;
  setTelemetry: (telemetry: TelemetryPoint[]) => void;
  reset: () => void;
  isValid: () => boolean;
}

export const useScenario = (): UseScenarioReturn => {
  const [scenario, setScenario] = useState<ScenarioRequest>({
    scenario_id: `scenario_${Date.now()}`,
    car_setup: NOMINAL_SETUP,
    driver_feedback: NOMINAL_FEEDBACK,
    track_conditions: NOMINAL_CONDITIONS,
    telemetry: [],
    timestamp: new Date().toISOString(),
  });

  const updateSetup = (setup: Partial<CarSetup>) => {
    setScenario((prev) => ({
      ...prev,
      car_setup: { ...prev.car_setup, ...setup },
    }));
  };

  const updateFeedback = (feedback: Partial<DriverFeedback>) => {
    setScenario((prev) => ({
      ...prev,
      driver_feedback: { ...prev.driver_feedback, ...feedback },
    }));
  };

  const updateConditions = (conditions: Partial<TrackConditions>) => {
    setScenario((prev) => ({
      ...prev,
      track_conditions: { ...prev.track_conditions, ...conditions },
    }));
  };

  const setTelemetry = (telemetry: TelemetryPoint[]) => {
    setScenario((prev) => ({
      ...prev,
      telemetry,
    }));
  };

  const reset = () => {
    setScenario({
      scenario_id: `scenario_${Date.now()}`,
      car_setup: NOMINAL_SETUP,
      driver_feedback: NOMINAL_FEEDBACK,
      track_conditions: NOMINAL_CONDITIONS,
      telemetry: [],
      timestamp: new Date().toISOString(),
    });
  };

  const isValid = (): boolean => {
    return (
      Object.keys(scenario.car_setup).length > 0 &&
      Object.keys(scenario.driver_feedback).length > 0 &&
      Object.keys(scenario.track_conditions).length > 0
    );
  };

  return {
    scenario,
    updateSetup,
    updateFeedback,
    updateConditions,
    setTelemetry,
    reset,
    isValid,
  };
};