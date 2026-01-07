"use client";
import React, { useEffect, useState } from 'react';
import { getFacultyHistory } from '../../api';
import { motion } from 'framer-motion';

export default function FacultyHistory() {
    const [history, setHistory] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const token = localStorage.getItem('facultyToken');
        if (token) fetchHistory(token);
    }, []);

    const fetchHistory = async (token: string) => {
        try {
            setLoading(true);
            const res = await getFacultyHistory(token);
            setHistory(res.data);
        } catch (err) {
            setError('Failed to fetch allocation history');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return (
        <div className="flex items-center justify-center min-h-[60vh]">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
        </div>
    );

    return (
        <div className="space-y-8">
            <header>
                <h1 className="text-3xl font-extrabold text-gray-900">Allocation History</h1>
                <p className="text-gray-500 mt-2 font-medium">Your permanent record of invigilation duties.</p>
            </header>

            {error && (
                <div className="bg-red-50 border-l-4 border-red-400 p-4 text-red-700 font-medium rounded-r-lg">
                    {error}
                </div>
            )}

            <div className="bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-100">
                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-gray-50 text-gray-400 text-xs font-bold uppercase tracking-widest border-b border-gray-100">
                                <th className="px-8 py-4">Date</th>
                                <th className="px-8 py-4">Session</th>
                                <th className="px-8 py-4">Hall</th>
                                <th className="px-8 py-4">Location</th>
                                <th className="px-8 py-4">Course</th>
                                <th className="px-8 py-4">Status</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-100">
                            {history.length > 0 ? (
                                history.map((item, idx) => (
                                    <motion.tr
                                        key={idx}
                                        initial={{ opacity: 0 }}
                                        animate={{ opacity: 1 }}
                                        transition={{ delay: idx * 0.02 }}
                                        className="hover:bg-gray-50 transition-colors group"
                                    >
                                        <td className="px-8 py-4 font-bold text-gray-900">{item.date}</td>
                                        <td className="px-8 py-4">
                                            <span className={`px-2 py-1 rounded text-[10px] font-black uppercase ${item.session === 'FN' ? 'bg-yellow-100 text-yellow-700' : 'bg-blue-100 text-blue-700'}`}>
                                                {item.session}
                                            </span>
                                        </td>
                                        <td className="px-8 py-4 font-mono font-bold text-indigo-600">{item.hall}</td>
                                        <td className="px-8 py-4 text-xs font-bold text-gray-500">{item.location}</td>
                                        <td className="px-8 py-4">
                                            <div className="flex flex-col">
                                                <span className="text-sm font-bold text-gray-800">{item.course_title}</span>
                                                <span className="text-xs text-gray-400 font-medium">{item.course_code}</span>
                                            </div>
                                        </td>
                                        <td className="px-8 py-4">
                                            {item.status === 'Replaced' ? (
                                                <span className="bg-red-50 text-red-600 px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1 w-fit">
                                                    <span className="w-1.5 h-1.5 bg-red-600 rounded-full"></span> Replaced
                                                </span>
                                            ) : (
                                                <span className="bg-green-50 text-green-600 px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1 w-fit">
                                                    <span className="w-1.5 h-1.5 bg-green-600 rounded-full"></span> Completed
                                                </span>
                                            )}
                                        </td>
                                    </motion.tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan={5} className="px-8 py-12 text-center text-gray-400 font-medium italic">
                                        No history found. Your duty records will appear here after your first assignment.
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
