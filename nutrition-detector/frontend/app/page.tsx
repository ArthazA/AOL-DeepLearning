"use client";

import React, { useState } from "react";
import Image from "next/image";

interface NutritionItem {
  name: string;
  value: string;
}

interface PredictionResult {
  timestamp: string;
  original_image: string;
  categorized_image: string;
  items: string;
  nutrition: NutritionItem[];
}


export default function UploadPredict() {
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [history, setHistory] = useState<PredictionResult[]>([]);
  const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL!;

  const handleUpload = async () => {
    if (!imageFile) return;

    const formData = new FormData();
    formData.append("file", imageFile);

    const res = await fetch("http://127.0.0.1:8000/predict-image", {
      method: "POST",
      body: formData,
    });

    const data: PredictionResult = await res.json();
    setHistory((prev) => [data, ...prev]);
    setImageFile(null);
  };

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Upload & Analyze Image</h1>

      <input
        type="file"
        onChange={(e) => setImageFile(e.target.files?.[0] || null)}
        className="border p-2"
      />

      <button
        onClick={handleUpload}
        className="px-4 py-2 bg-blue-500 text-white rounded"
      >
        Upload
      </button>

      <table className="w-full border border-gray-400 mt-6">
        <thead>
          <tr className="bg-gray-200">
            <th className="border p-2">Time</th>
            <th className="border p-2">Original</th>
            <th className="border p-2">Result</th>
            <th className="border p-2">Items</th>
            <th className="border p-2">Nutrition</th>
          </tr>
        </thead>

        <tbody>
          {history.map((item, idx) => (
            <tr key={idx} className="text-center">
              <td className="border p-2">{item.timestamp}</td>

              <td className="border p-2">
                <div className="flex items-center justify-center">
                  <Image
                    src={`${BACKEND_URL}/${encodeURI(item.original_image)}`}
                    alt="original"
                    width={300}
                    height={200}
                    unoptimized
                  />
                </div>

              </td>

              <td className="border p-2">
                <div className="flex items-center justify-center">
                  <Image
                    src={`${BACKEND_URL}/${encodeURI(item.categorized_image)}`}
                    alt="categorized"
                    width={300}
                    height={200}
                    unoptimized
                  />
                </div>

                
              </td>

              <td className="border p-2">
                {item.items}
              </td>

              <td className="border p-2 text-left">
                <ul className="text-left">
                  {item.nutrition.map((n, i) => (
                    <li key={i}>
                      {n.name}: {n.value}
                    </li>
                  ))}
                </ul>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
