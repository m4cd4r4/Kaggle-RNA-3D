"use client";

import { useState } from "react";

// Sample RNA structure data
const sampleStructures = [
  { id: "sample_1", name: "tRNA-Phe", length: 76, sequence: "GCGGAUUUAGCUCAGUUGGGAGAGCGCCAGACUGAAGAUCUGGAGGUCCUGUGUUCGAUCCACAGAAUUCGCACCA" },
  { id: "sample_2", name: "Riboswitch", length: 94, sequence: "GGCUUAUCAAGAGAGGUGGAGGGACUGGCCCGAUGAAACCCGGCAACCACUAGUCUAGCGUCAGCUUCGGCUGACGCUAGGCUAGUCC" },
  { id: "sample_3", name: "Hammerhead", length: 58, sequence: "GGCGAAAGUUGAGCGAAACUCGAAAGAGCGAAAGCGUUCUUAUACGGCGAAAGCC" },
];

// Simple 2D representation of RNA structure
function RNA2DViewer({ sequence }: { sequence: string }) {
  const nucleotideColors: Record<string, string> = {
    A: "#FF6B6B",
    U: "#4ECDC4",
    G: "#45B7D1",
    C: "#FFA07A",
  };

  return (
    <div className="flex flex-wrap gap-1 p-4">
      {sequence.split("").map((nuc, i) => (
        <div
          key={i}
          className="w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-bold shadow-md transition-transform hover:scale-125"
          style={{ backgroundColor: nucleotideColors[nuc] || "#888" }}
          title={`Position ${i + 1}: ${nuc}`}
        >
          {nuc}
        </div>
      ))}
    </div>
  );
}

// 3D-like backbone visualization (SVG-based)
function RNA3DBackbone({ sequence }: { sequence: string }) {
  const nucleotideColors: Record<string, string> = {
    A: "#FF6B6B",
    U: "#4ECDC4",
    G: "#45B7D1",
    C: "#FFA07A",
  };

  const helixPoints: { x: number; y: number; z: number }[] = [];
  const radius = 100;
  const pitch = 8;

  for (let i = 0; i < sequence.length; i++) {
    const angle = (i / sequence.length) * Math.PI * 4;
    helixPoints.push({
      x: 200 + radius * Math.cos(angle) * (1 + i * 0.01),
      y: 50 + i * pitch,
      z: radius * Math.sin(angle),
    });
  }

  // Sort by z for proper depth ordering
  const sortedIndices = helixPoints
    .map((p, i) => ({ z: p.z, i }))
    .sort((a, b) => a.z - b.z)
    .map((p) => p.i);

  return (
    <svg viewBox="0 0 400 700" className="w-full h-full">
      {/* Backbone lines */}
      <path
        d={helixPoints.map((p, i) => `${i === 0 ? "M" : "L"} ${p.x} ${p.y}`).join(" ")}
        fill="none"
        stroke="#ddd"
        strokeWidth="2"
      />

      {/* Nucleotides */}
      {sortedIndices.map((i) => {
        const p = helixPoints[i];
        const nuc = sequence[i];
        const size = 8 + (p.z + radius) / 25;
        const opacity = 0.5 + (p.z + radius) / (radius * 4);

        return (
          <g key={i}>
            <circle
              cx={p.x}
              cy={p.y}
              r={size}
              fill={nucleotideColors[nuc] || "#888"}
              opacity={opacity}
              className="transition-all duration-200 hover:opacity-100"
              style={{ filter: `drop-shadow(0 2px 4px rgba(0,0,0,0.2))` }}
            />
            <text
              x={p.x}
              y={p.y + 4}
              textAnchor="middle"
              fill="white"
              fontSize={size * 0.8}
              fontWeight="bold"
              opacity={opacity}
            >
              {nuc}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

export default function VisualizerPage() {
  const [selectedStructure, setSelectedStructure] = useState(sampleStructures[0]);
  const [customSequence, setCustomSequence] = useState("");
  const [viewMode, setViewMode] = useState<"2d" | "3d">("3d");

  const displaySequence = customSequence || selectedStructure.sequence;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">
          <span className="mr-3">🧬</span>
          RNA Structure Visualizer
        </h1>
        <p className="text-gray-600">
          Visualize RNA sequences and their predicted 3D structures
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Controls Panel */}
        <div className="lg:col-span-1 space-y-6">
          {/* Sample Structures */}
          <div className="glassmorphism rounded-xl p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Sample Structures</h3>
            <div className="space-y-2">
              {sampleStructures.map((structure) => (
                <button
                  key={structure.id}
                  onClick={() => {
                    setSelectedStructure(structure);
                    setCustomSequence("");
                  }}
                  className={`w-full text-left p-3 rounded-lg transition-all ${
                    selectedStructure.id === structure.id && !customSequence
                      ? "bg-gradient-to-r from-blue-500 to-purple-500 text-white"
                      : "bg-gray-100 hover:bg-gray-200 text-gray-700"
                  }`}
                >
                  <div className="font-medium">{structure.name}</div>
                  <div className="text-sm opacity-80">{structure.length} nucleotides</div>
                </button>
              ))}
            </div>
          </div>

          {/* Custom Sequence Input */}
          <div className="glassmorphism rounded-xl p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Custom Sequence</h3>
            <textarea
              value={customSequence}
              onChange={(e) => setCustomSequence(e.target.value.toUpperCase().replace(/[^AUGC]/g, ""))}
              placeholder="Enter RNA sequence (AUGC only)..."
              className="w-full h-32 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
            />
            <div className="mt-2 text-sm text-gray-500">
              {customSequence ? `${customSequence.length} nucleotides` : "Paste or type your sequence"}
            </div>
          </div>

          {/* View Mode Toggle */}
          <div className="glassmorphism rounded-xl p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">View Mode</h3>
            <div className="flex gap-2">
              <button
                onClick={() => setViewMode("2d")}
                className={`flex-1 py-2 px-4 rounded-lg transition-all ${
                  viewMode === "2d"
                    ? "bg-blue-500 text-white"
                    : "bg-gray-100 hover:bg-gray-200 text-gray-700"
                }`}
              >
                2D Linear
              </button>
              <button
                onClick={() => setViewMode("3d")}
                className={`flex-1 py-2 px-4 rounded-lg transition-all ${
                  viewMode === "3d"
                    ? "bg-purple-500 text-white"
                    : "bg-gray-100 hover:bg-gray-200 text-gray-700"
                }`}
              >
                3D Helix
              </button>
            </div>
          </div>

          {/* Nucleotide Legend */}
          <div className="glassmorphism rounded-xl p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Nucleotide Legend</h3>
            <div className="grid grid-cols-2 gap-3">
              {[
                { nuc: "A", name: "Adenine", color: "#FF6B6B" },
                { nuc: "U", name: "Uracil", color: "#4ECDC4" },
                { nuc: "G", name: "Guanine", color: "#45B7D1" },
                { nuc: "C", name: "Cytosine", color: "#FFA07A" },
              ].map(({ nuc, name, color }) => (
                <div key={nuc} className="flex items-center gap-2">
                  <div
                    className="w-6 h-6 rounded-full flex items-center justify-center text-white text-xs font-bold"
                    style={{ backgroundColor: color }}
                  >
                    {nuc}
                  </div>
                  <span className="text-sm text-gray-600">{name}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Visualization Panel */}
        <div className="lg:col-span-2">
          <div className="glassmorphism rounded-xl p-6 h-full min-h-[600px]">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-gray-900">
                {customSequence ? "Custom Sequence" : selectedStructure.name}
              </h3>
              <span className="text-sm text-gray-500">
                {displaySequence.length} nucleotides
              </span>
            </div>

            <div className="bg-white rounded-lg border border-gray-200 overflow-hidden" style={{ height: "500px" }}>
              {viewMode === "2d" ? (
                <div className="overflow-auto h-full p-4">
                  <RNA2DViewer sequence={displaySequence} />
                </div>
              ) : (
                <div className="h-full flex items-center justify-center">
                  <RNA3DBackbone sequence={displaySequence} />
                </div>
              )}
            </div>

            {/* Sequence Display */}
            <div className="mt-4 p-4 bg-gray-50 rounded-lg">
              <div className="text-sm font-medium text-gray-700 mb-2">Sequence:</div>
              <div className="font-mono text-xs break-all text-gray-600">
                {displaySequence}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
