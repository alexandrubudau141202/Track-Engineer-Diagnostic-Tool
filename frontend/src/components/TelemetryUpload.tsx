import React, { useRef, useState, useCallback } from "react";
import { TelemetryPoint } from "../types/Scenario";

interface TelemetryUploadProps {
  onTelemetryLoaded: (telemetry: TelemetryPoint[]) => void;
}

export const TelemetryUpload: React.FC<TelemetryUploadProps> = ({
  onTelemetryLoaded,
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string>("");
  const [dataPoints, setDataPoints] = useState<number>(0);
  const [dragOver, setDragOver] = useState(false);

  const processFile = async (file: File) => {
    setLoading(true);
    setError(null);

    try {
      const text = await file.text();
      let telemetry: TelemetryPoint[] = [];

      if (file.name.endsWith(".json")) {
        telemetry = JSON.parse(text);
      } else if (file.name.endsWith(".csv")) {
        const lines = text.split("\n").filter((line) => line.trim());
        const headers = lines[0].split(",").map((h) => h.trim());

        for (let i = 1; i < lines.length; i++) {
          const values = lines[i].split(",");
          const point: any = {};
          headers.forEach((header, index) => {
            const value = values[index]?.trim();
            point[header] = isNaN(Number(value)) ? value : Number(value);
          });
          telemetry.push(point as TelemetryPoint);
        }
      } else {
        throw new Error("Unsupported format. Use .json or .csv");
      }

      setFileName(file.name);
      setDataPoints(telemetry.length);
      onTelemetryLoaded(telemetry);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to parse file";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) processFile(file);
  };

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDragOver(false);
      const file = e.dataTransfer.files?.[0];
      if (file) processFile(file);
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    []
  );

  return (
    <div className="card">
      <div className="section-header">
        <div className="section-icon bg-[#FFD600]/10 text-[#FFD600]">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M2 12h4l3-9 4 18 3-9h4"/></svg>
        </div>
        <h3 className="font-semibold text-sm text-white tracking-wide">
          Telemetry Data
        </h3>
      </div>

      <div className="p-5">
        <div
          onClick={() => fileInputRef.current?.click()}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`rounded-xl border-2 border-dashed p-8 text-center cursor-pointer transition-all duration-300 ${
            dragOver
              ? "border-[#FF6B00] bg-[#FF6B00]/[0.04] shadow-[0_0_30px_rgba(255,107,0,0.06)]"
              : fileName
              ? "border-emerald-500/20 bg-emerald-500/[0.02]"
              : "border-white/[0.06] bg-white/[0.01] hover:border-white/[0.12] hover:bg-white/[0.02]"
          }`}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".json,.csv"
            onChange={handleFileChange}
            className="hidden"
          />

          {!fileName ? (
            <div>
              <div className="w-12 h-12 rounded-xl bg-white/[0.03] border border-white/[0.06] flex items-center justify-center mx-auto mb-3">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="text-white/15"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
              </div>
              <p className="text-white/40 text-sm font-medium">
                Drop telemetry files here
              </p>
              <p className="text-white/20 text-xs mt-1">
                or click to browse &middot; JSON, CSV
              </p>
            </div>
          ) : (
            <div>
              <div className="w-10 h-10 rounded-full bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center mx-auto mb-3">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="text-emerald-400"><polyline points="20 6 9 17 4 12"/></svg>
              </div>
              <p className="text-emerald-400 text-sm font-medium">{fileName}</p>
              <p className="text-white/25 text-xs mt-1">
                {dataPoints.toLocaleString()} data points loaded
              </p>
            </div>
          )}
        </div>

        {loading && (
          <div className="mt-3 flex items-center gap-2 text-[#00D4FF] text-xs">
            <svg className="animate-spin h-3.5 w-3.5" viewBox="0 0 24 24" fill="none">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3"/>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
            </svg>
            Parsing telemetry data...
          </div>
        )}

        {error && (
          <div className="mt-3 flex items-start gap-2 text-red-400 text-xs">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="mt-0.5 shrink-0"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
            <span>{error}</span>
          </div>
        )}

        {fileName && !error && !loading && (
          <p className="mt-3 text-[11px] text-white/20">
            Ready for diagnosis with {dataPoints.toLocaleString()} telemetry points
          </p>
        )}
      </div>
    </div>
  );
};