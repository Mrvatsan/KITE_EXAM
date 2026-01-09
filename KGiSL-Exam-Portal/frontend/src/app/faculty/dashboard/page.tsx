"use client";
import React, { useEffect, useState } from 'react';
import { getFacultyDashboard } from '../../api';
import { motion } from 'framer-motion';

export default function FacultyDashboard() {
    const [duties, setDuties] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const token = localStorage.getItem('facultyToken');
        if (token) fetchDashboard(token);
    }, []);

    const fetchDashboard = async (token: string) => {
        try {
            setLoading(true);
            const res = await getFacultyDashboard(token);
            setDuties(res.data);
        } catch (err: any) {
            setError('Failed to fetch dashboard data');
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
                <h1 className="text-3xl font-extrabold text-gray-900">Assigned Duties</h1>
                <p className="text-gray-500 mt-2 font-medium">View and manage your invigilation duties.</p>
            </header>

            {error && (
                <div className="bg-red-50 border-l-4 border-red-400 p-4 text-red-700 font-medium rounded-r-lg">
                    {error}
                </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {duties.length > 0 ? (
                    duties.map((duty, idx) => (
                        <motion.div
                            key={duty.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: idx * 0.1 }}
                            className={`rounded-2xl shadow-xl overflow-hidden border ${duty.is_replaced ? 'bg-gray-50 border-gray-200' : 'bg-white border-white'}`}
                        >
                            <div className={`px-6 py-4 flex justify-between items-center ${duty.is_replaced ? 'bg-gray-200' : 'bg-indigo-600'} text-white`}>
                                <div className="flex flex-col">
                                    <div className="flex items-center gap-2">
                                        <span className="text-xl">{duty.is_replaced ? '🔄' : '🏛️'}</span>
                                        <span className="font-bold text-lg">{duty.is_replaced ? 'Duty Reassigned' : `Hall ${duty.hall_no}`}</span>
                                    </div>
                                    <span className="text-[10px] font-bold opacity-80 uppercase tracking-widest">{duty.exam_date}</span>
                                </div>
                                <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase ${duty.session === 'FN' ? 'bg-yellow-400 text-yellow-900' : 'bg-blue-400 text-blue-900'}`}>
                                    {duty.session === 'FN' ? 'Morning (FN)' : 'Afternoon (AN)'}
                                </span>
                            </div>

                            <div className="p-6 space-y-4">
                                <div className="flex items-center justify-between text-sm">
                                    <span className="text-gray-500 font-semibold uppercase tracking-wider">Location</span>
                                    <span className="text-indigo-900 font-bold">{duty.location}</span>
                                </div>
                                <hr className="border-gray-100" />
                                <div className="space-y-2">
                                    <span className="text-gray-500 text-xs font-bold uppercase tracking-widest">Course Details</span>
                                    <h3 className="text-xl font-bold text-gray-800 break-words">
                                        {duty.is_replaced ? 'REASSIGNED' : duty.course_title}
                                    </h3>
                                    {!duty.is_replaced && (
                                        <p className="text-indigo-600 font-mono font-bold text-sm">{duty.course_code}</p>
                                    )}
                                </div>

                                {duty.is_replaced && (
                                    <div className="mt-4 bg-amber-100 text-amber-700 p-3 rounded-xl text-xs font-bold flex items-center gap-2">
                                        <span>ℹ️</span> Your assignment has been successfully reassigned.
                                    </div>
                                )}
                            </div>
                        </motion.div>
                    ))
                ) : (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="col-span-full bg-white p-12 rounded-3xl text-center shadow-inner border-2 border-dashed border-gray-200"
                    >
                        <div className="text-6xl mb-4">🗓️</div>
                        <h3 className="text-xl font-bold text-gray-800">No active invigilation assigned</h3>
                        <p className="text-gray-500 mt-2 font-medium">Please check back later once the admin activates the schedule.</p>
                    </motion.div>
                )}
            </div>
        </div>
    );
}
