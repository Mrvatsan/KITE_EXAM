import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* output: 'export' removed for Render Web Service deployment */
  /* distDir: 'out' removed */
  images: {
    /* unoptimized: true removed (unless you really want it, but usually not needed for web service) */
  },
  env: {
    // Production API URL - update this for Render deployment
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  }
};

export default nextConfig;
