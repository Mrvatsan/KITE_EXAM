import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    unoptimized: true,
  },
  async rewrites() {
    const rawApiUrl = process.env.NEXT_PUBLIC_API_URL || process.env.BACKEND_URL;
    if (!rawApiUrl) {
      return [];
    }
    let target = rawApiUrl;
    if (!target.startsWith('http://') && !target.startsWith('https://')) {
      target = target.includes('.') ? `https://${target}` : `http://${target}:10000`;
    }
    return [
      {
        source: '/api/:path*',
        destination: `${target.replace(/\/$/, '')}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
