"use client";
import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { getAdminAlternationRequests, approveAlternationRequest } from '../../api';
import { motion, AnimatePresence } from 'framer-motion';

export default function AdminFacultyRequests() {
    const [requests, setRequests] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [statusFilter, setStatusFilter] = useState('PENDING');
    const [actioning, setActioning] = useState<number | null>(null);
    const router = useRouter();

    useEffect(() => {
        const role = localStorage.getItem('role');
        if (role !== 'admin') router.push('/');
        fetchRequests();
    }, [statusFilter]);

    const fetchRequests = async () => {
        try {
            setLoading(true);
            const res = await getAdminAlternationRequests(statusFilter);
            setRequests(res.data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleAction = async (requestId: number, action: 'APPROVE' | 'REJECT') => {
        if (!confirm(`Are you sure you want to ${action.toLowerCase()} this request?`)) return;

        setActioning(requestId);
        try {
            await approveAlternationRequest(requestId, action);
            fetchRequests();
        } catch (err: any) {
            alert(err.response?.data?.error || 'Action failed');
        } finally {
            setActioning(null);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col">
            <header className="bg-white border-b border-gray-200 px-8 py-6 flex justify-between items-center sticky top-0 z-10">
                <div>
                    <h1 className="text-2xl font-black text-gray-900 tracking-tight">Faculty Alternation Requests</h1>
                    <p className="text-gray-500 text-sm font-medium">Review and manage faculty department-level reassignments.</p>
                </div>
                <button
                    onClick={() => router.push('/admin/dashboard')}
                    className="px-4 py-2 border border-gray-200 rounded-xl text-sm font-bold text-gray-600 hover:bg-gray-50 transition"
                >
                    Back to Dashboard
                </button>
            </header>

            <main className="p-8 max-w-6xl mx-auto w-full space-y-8">
                {/* Filters */}
                <div className="bg-white p-4 rounded-2xl shadow-sm border border-gray-200 flex gap-2">
                    {['PENDING', 'APPROVED', 'REJECTED'].map((s) => (
                        <button
                            key={s}
                            onClick={() => setStatusFilter(s)}
                            className={`px-6 py-2 rounded-xl text-xs font-black transition-all ${statusFilter === s
                                ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-100'
                                : 'text-gray-400 hover:bg-gray-50'}`}
                        >
                            {s}
                        </button>
                    ))}
                </div>

                {loading ? (
                    <div className="flex justify-center py-20">
                        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-indigo-600"></div>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 gap-4">
                        <AnimatePresence>
                            {requests.length > 0 ? (
                                requests.map((req) => (
                                    <motion.div
                                        key={req.id}
                                        initial={{ opacity: 0, scale: 0.95 }}
                                        animate={{ opacity: 1, scale: 1 }}
                                        exit={{ opacity: 0, scale: 0.95 }}
                                        className="bg-white p-6 rounded-3xl shadow-sm border border-gray-200 group hover:border-indigo-200 transition-all flex flex-col md:flex-row justify-between items-center gap-6"
                                    >
                                        <div className="flex-1 space-y-3">
                                            <div className="flex items-center gap-3">
                                                <div className="h-10 w-10 bg-indigo-50 rounded-full flex items-center justify-center text-indigo-600 font-black">
                                                    {req.faculty_name[0]}
                                                </div>
                                                <div>
                                                    <h3 className="font-black text-gray-900 text-lg leading-tight">{req.faculty_name}</h3>
                                                    <p className="text-[10px] text-gray-400 font-bold uppercase tracking-widest">{req.faculty_reg_no} • {req.department}</p>
                                                </div>
                                            </div>

                                            <div className="bg-gray-50 p-4 rounded-2xl text-sm">
                                                <p className="text-gray-500 font-bold text-[10px] uppercase mb-1">Reason for request</p>
                                                <p className="text-gray-700 font-medium leading-relaxed italic">"{req.reason}"</p>
                                            </div>
                                        </div>

                                        <div className="w-full md:w-auto flex flex-col items-center md:items-end gap-2 px-6 py-4 bg-gray-50 md:bg-transparent rounded-2xl">
                                            <div className="text-right">
                                                <span className="block text-xl font-black text-indigo-900 leading-none">Hall {req.hall_no}</span>
                                                <span className="text-[10px] font-bold text-gray-400 uppercase">{req.exam_date} • {req.session}</span>
                                            </div>

                                            {statusFilter === 'PENDING' && (
                                                <div className="flex gap-2 mt-2 w-full">
                                                    <button
                                                        onClick={() => handleAction(req.id, 'APPROVE')}
                                                        disabled={actioning === req.id}
                                                        className="flex-1 px-4 py-2 bg-green-500 hover:bg-green-600 text-white text-xs font-black rounded-xl shadow-lg shadow-green-100 transition disabled:bg-gray-200"
                                                    >
                                                        {actioning === req.id ? '...' : 'APPROVE'}
                                                    </button>
                                                    <button
                                                        onClick={() => handleAction(req.id, 'REJECT')}
                                                        disabled={actioning === req.id}
                                                        className="flex-1 px-4 py-2 bg-red-400 hover:bg-red-500 text-white text-xs font-black rounded-xl transition disabled:bg-gray-200"
                                                    >
                                                        REJECT
                                                    </button>
                                                </div>
                                            )}
                                        </div>
                                    </motion.div>
                                ))
                            ) : (
                                <div className="py-20 text-center bg-white rounded-3xl border-2 border-dashed border-gray-100">
                                    <p className="text-gray-400 font-medium italic">No requests found for this category.</p>
                                </div>
                            )}
                        </AnimatePresence>
                    </div>
                )}
            </main>
        </div>
    );
}
