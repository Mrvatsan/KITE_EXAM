"use client";
import React, { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';

export default function FacultyLayout({ children }: { children: React.ReactNode }) {
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);
    const [facultyName, setFacultyName] = useState('');
    const router = useRouter();
    const pathname = usePathname();

    useEffect(() => {
        const role = localStorage.getItem('role');
        const token = localStorage.getItem('facultyToken');
        const facultyDataStr = localStorage.getItem('facultyData');

        if (role !== 'faculty' || !token) {
            router.push('/');
            return;
        }

        if (facultyDataStr) {
            const data = JSON.parse(facultyDataStr);
            setFacultyName(data.name);
        }
    }, [router]);

    const handleLogout = () => {
        localStorage.clear();
        router.push('/');
    };

    const navItems = [
        { name: 'Dashboard', path: '/faculty/dashboard', icon: '📊' },
        { name: 'Hall Seating', path: '/faculty/seating', icon: '🪑' },
        { name: 'History', path: '/faculty/history', icon: '📜' },
        { name: 'Availability', path: '/faculty/availability', icon: '🗓️' },
    ];

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col font-sans">
            {/* Navbar */}
            <header className="bg-indigo-900 text-white px-6 py-4 flex justify-between items-center shadow-lg z-30 sticky top-0">
                <div className="flex items-center gap-4">
                    <button
                        onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                        className="text-2xl hover:bg-white/10 p-2 rounded-lg transition"
                    >
                        ☰
                    </button>
                    <h1 className="text-xl font-bold tracking-tight">KITE FACULTY PORTAL</h1>
                </div>
                <div className="flex items-center gap-6">
                    <div className="text-right hidden sm:block">
                        <p className="text-sm font-medium opacity-80">Welcome back,</p>
                        <p className="font-bold">{facultyName}</p>
                    </div>
                    <button
                        onClick={handleLogout}
                        className="bg-red-500 hover:bg-red-600 text-white px-5 py-2 rounded-full text-sm font-bold shadow-md transition-all active:scale-95"
                    >
                        Logout
                    </button>
                </div>
            </header>

            <div className="flex flex-1 relative overflow-hidden">
                {/* Sidebar */}
                <AnimatePresence mode="wait">
                    {isSidebarOpen && (
                        <motion.aside
                            initial={{ x: -250 }}
                            animate={{ x: 0 }}
                            exit={{ x: -250 }}
                            transition={{ type: 'spring', damping: 20, stiffness: 100 }}
                            className="w-64 bg-white border-r border-gray-200 shadow-xl z-20 hidden md:block h-[calc(100vh-68px)] sticky top-[68px]"
                        >
                            <nav className="p-4 space-y-2 mt-4">
                                {navItems.map((item) => (
                                    <Link
                                        key={item.path}
                                        href={item.path}
                                        className={`flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-all ${pathname === item.path
                                                ? 'bg-indigo-600 text-white shadow-indigo-200 shadow-lg'
                                                : 'text-gray-600 hover:bg-indigo-50 hover:text-indigo-600'
                                            }`}
                                    >
                                        <span className="text-xl">{item.icon}</span>
                                        {item.name}
                                    </Link>
                                ))}
                            </nav>
                        </motion.aside>
                    )}
                </AnimatePresence>

                {/* Main Content Area */}
                <main className="flex-1 overflow-y-auto bg-[#F8FAFC]">
                    <div className="p-6 md:p-8 max-w-7xl mx-auto">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    );
}
