"use client";
import React, { useState, useEffect } from 'react';
import { allocateFaculty, getAllocatedFaculty } from '../../api';
import { motion, AnimatePresence } from 'framer-motion';
import { useRouter } from 'next/navigation';

export default function AdminFacultyAllocation() {
    const [counts, setCounts] = useState<any>({
        'CSE': 0, 'AI&ML': 0, 'AI&DS': 0, 'ECE': 0, 'CYS': 0, 'MECH': 0, 'CSBS': 0
    });
    const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
    const [session, setSession] = useState('FN');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [results, setResults] = useState<any[]>([]);
    const router = useRouter();

    useEffect(() => {
        const role = localStorage.getItem('role');
        if (role !== 'admin') router.push('/');
    }, []);

    const handleChange = (dept: string, val: string) => {
        setCounts({ ...counts, [dept]: parseInt(val) || 0 });
    };

    const handleAllocate = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        try {
            const res = await allocateFaculty(counts, date, session);
            setResults(res.data.allocations);
            alert('Allocation successful!');
        } catch (err: any) {
            setError(err.response?.data?.error || 'Allocation failed');
        } finally {
            setLoading(false);
        }
    };

    const handleFetchResults = async () => {
        setLoading(true);
        setError('');
        try {
            const res = await getAllocatedFaculty(date, session);
            setResults(res.data);
            if (res.data.length === 0) alert('No allocations found for this date/session.');
        } catch (err: any) {
            setError('Failed to fetch results');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 flex flex-col font-sans">
            {/* Navbar */}
            <div className="bg-gray-900 text-white px-8 py-4 flex justify-between items-center shadow-lg">
                <div className="flex items-center gap-4">
                    <button onClick={() => router.push('/admin/dashboard')} className="text-gray-400 hover:text-white transition">← Dashboard</button>
                    <h1 className="text-xl font-bold tracking-widest">FACULTY ALLOCATION CONTROL</h1>
                </div>
                <div className="flex items-center gap-4">
                    <span className="bg-indigo-600 px-3 py-1 rounded text-xs font-bold uppercase tracking-tighter">Admin Panel</span>
                </div>
            </div>

            <main className="flex-1 p-8 overflow-y-auto">
                <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">

                    {/* Input Panel */}
                    <div className="lg:col-span-1 space-y-6">
                        <motion.section
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            className="bg-white p-8 rounded-3xl shadow-xl border border-gray-200"
                        >
                            <h2 className="text-xl font-bold text-gray-800 mb-6 flex items-center gap-2">
                                <span>⚙️</span> Allocation Settings
                            </h2>

                            <form onSubmit={handleAllocate} className="space-y-6">
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-xs font-bold text-gray-400 uppercase mb-1">Date</label>
                                        <input
                                            type="date"
                                            value={date}
                                            onChange={(e) => setDate(e.target.value)}
                                            className="w-full p-2 border border-gray-200 rounded-lg text-sm font-bold bg-gray-50 focus:bg-white focus:ring-2 focus:ring-indigo-100"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-xs font-bold text-gray-400 uppercase mb-1">Session</label>
                                        <select
                                            value={session}
                                            onChange={(e) => setSession(e.target.value)}
                                            className="w-full p-2 border border-gray-200 rounded-lg text-sm font-bold bg-gray-50 focus:bg-white focus:ring-2 focus:ring-indigo-100"
                                        >
                                            <option value="FN">Morning (FN)</option>
                                            <option value="AN">Afternoon (AN)</option>
                                        </select>
                                    </div>
                                </div>

                                <div className="space-y-4">
                                    <label className="block text-xs font-bold text-gray-400 uppercase">Department Counts</label>
                                    <div className="grid grid-cols-2 gap-x-4 gap-y-3">
                                        {Object.keys(counts).map(dept => (
                                            <div key={dept} className="flex flex-col">
                                                <span className="text-[10px] font-bold text-gray-500 mb-1">{dept}</span>
                                                <input
                                                    type="number"
                                                    min="0"
                                                    value={counts[dept]}
                                                    onChange={(e) => handleChange(dept, e.target.value)}
                                                    className="w-full p-2 border border-gray-100 bg-gray-50 rounded-lg text-sm font-bold"
                                                />
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                {error && <p className="text-red-500 text-xs font-bold bg-red-50 p-3 rounded-lg">{error}</p>}

                                <div className="flex gap-3 pt-4">
                                    <button
                                        type="submit"
                                        disabled={loading}
                                        className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 rounded-xl shadow-lg transition-all active:scale-95 disabled:bg-gray-300"
                                    >
                                        {loading ? 'Processing...' : 'Allocate Now'}
                                    </button>
                                    <button
                                        type="button"
                                        onClick={handleFetchResults}
                                        className="px-4 bg-gray-100 hover:bg-gray-200 text-gray-600 font-bold py-3 rounded-xl transition"
                                    >
                                        👁️
                                    </button>
                                </div>
                            </form>
                        </motion.section>
                    </div>

                    {/* Results Table */}
                    <div className="lg:col-span-2">
                        <motion.section
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="bg-white rounded-3xl shadow-xl border border-gray-200 overflow-hidden min-h-[500px]"
                        >
                            <div className="px-8 py-6 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
                                <div>
                                    <h2 className="text-xl font-bold text-gray-800">Allocation Results</h2>
                                    <p className="text-gray-400 text-xs font-medium">Deterministic faculty-hall mapping for {date} ({session})</p>
                                </div>
                                <span className="text-indigo-600 font-black text-lg">{results.length} Halls</span>
                            </div>

                            <div className="overflow-x-auto">
                                <table className="w-full text-left">
                                    <thead>
                                        <tr className="bg-gray-100 text-gray-400 text-[10px] font-black uppercase tracking-widest border-b border-gray-200">
                                            <th className="px-8 py-4">Hall No</th>
                                            <th className="px-8 py-4">Faculty Name</th>
                                            <th className="px-8 py-4">Department</th>
                                            <th className="px-8 py-4">Course Details</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-gray-100 font-medium">
                                        {results.length > 0 ? (
                                            results.map((r, i) => (
                                                <tr key={i} className="hover:bg-indigo-50/20 transition-colors">
                                                    <td className="px-8 py-4"><span className="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-xs font-black">{r.hall_no}</span></td>
                                                    <td className="px-8 py-4">
                                                        <div className="flex flex-col">
                                                            <span className="text-gray-900 font-bold">{r.faculty_name}</span>
                                                            <span className="text-[10px] text-gray-400 font-mono">{r.faculty_reg_no}</span>
                                                        </div>
                                                    </td>
                                                    <td className="px-8 py-4"><span className="text-sm text-gray-600 font-bold">{r.department}</span></td>
                                                    <td className="px-8 py-4 max-w-xs">
                                                        <div className="truncate text-xs text-gray-500 font-bold">{r.course_title}</div>
                                                        <div className="text-[10px] text-indigo-400 font-black">{r.course_code}</div>
                                                    </td>
                                                </tr>
                                            ))
                                        ) : (
                                            <tr>
                                                <td colSpan={4} className="px-8 py-20 text-center text-gray-400 italic">
                                                    Enter counts and click "Allocate Now" to generate or "Eye" to view existing data.
                                                </td>
                                            </tr>
                                        )}
                                    </tbody>
                                </table>
                            </div>
                        </motion.section>
                    </div>
                </div>
            </main>
        </div>
    );
}
