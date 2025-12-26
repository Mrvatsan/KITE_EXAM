import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',  // Enable static HTML export
  distDir: 'out',    // Output directory for static build
  images: {
    unoptimized: true  // Required for static export
  },
  env: {
    // Production API URL - update this for Render deployment
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  }
};

export default nextConfig;
