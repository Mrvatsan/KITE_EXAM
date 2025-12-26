import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Exam Management System",
  description: "Portal for Students and Admins",
  icons: {
    icon: '/kite-logo.png',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
