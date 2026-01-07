"use client";
import React, { useEffect, useState } from 'react';
import { getFacultyDashboard, updateFacultyAvailability } from '../../api';
import { motion, AnimatePresence } from 'framer-motion';

export default function FacultyAvailability() {
    const [duties, setDuties] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedDuty, setSelectedDuty] = useState<any>(null);
    const [reason, setReason] = useState('');
    const [submitting, setSubmitting] = useState(false);
    const [msg, setMsg] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        const token = localStorage.getItem('facultyToken');
        if (token) fetchActiveDuties(token);
    }, []);

    const fetchActiveDuties = async (token: string) => {
        try {
            setLoading(true);
            const res = await getFacultyDashboard(token);
            // Only show duties that haven't been replaced yet
            setDuties(res.data.filter((d: any) => !d.is_replaced));
        } catch (err) {
            setError('Failed to fetch duties');
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!selectedDuty || !reason) return;

        const token = localStorage.getItem('facultyToken');
        if (!token) return;

        setSubmitting(true);
        setError('');
        setMsg('');

        try {
            await updateFacultyAvailability(token, selectedDuty.id, reason);
            setMsg('Availability marked. A replacement from your department has been auto-assigned.');
            setReason('');
            setSelectedDuty(null);
            fetchActiveDuties(token);
        } catch (err: any) {
            setError(err.response?.data?.error || 'Failed to update availability');
        } finally {
            setSubmitting(false);
        }
    };

    if (loading) return (
        <div className="flex items-center justify-center min-h-[60vh]">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
        </div>
    );

    return (
        <div className="max-w-4xl mx-auto space-y-8">
            <header>
                <h1 className="text-3xl font-extrabold text-gray-900">Mark Availability</h1>
                <p className="text-gray-500 mt-2 font-medium">If you are unable to attend your assigned duty, please mark yourself as unavailable.</p>
            </header>

            {msg && (
                <div className="bg-green-50 border-l-4 border-green-400 p-4 text-green-700 font-bold rounded-r-lg shadow-sm">
                    {msg}
                </div>
            )}

            {error && (
                <div className="bg-red-50 border-l-4 border-red-400 p-4 text-red-700 font-bold rounded-r-lg shadow-sm">
                    {error}
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Duty List */}
                <div className="space-y-4">
                    <h3 className="text-sm font-bold text-gray-400 uppercase tracking-widest">Select Assignment</h3>
                    {duties.length > 0 ? (
                        duties.map((duty) => (
                            <button
                                key={duty.id}
                                onClick={() => setSelectedDuty(duty)}
                                className={`w-full text-left p-6 rounded-2xl border-2 transition-all ${selectedDuty?.id === duty.id
                                        ? 'border-indigo-600 bg-white shadow-lg ring-4 ring-indigo-50'
                                        : 'border-gray-100 bg-gray-50 hover:border-gray-200'
                                    }`}
                            >
                                <div className="flex justify-between items-start mb-2">
                                    <span className="font-black text-indigo-900 text-lg">Hall {duty.hall_no}</span>
                                    <span className={`px-2 py-1 rounded text-[10px] font-black uppercase ${duty.session === 'FN' ? 'bg-yellow-100 text-yellow-700' : 'bg-blue-100 text-blue-700'}`}>
                                        {duty.session}
                                    </span>
                                </div>
                                <p className="text-sm font-bold text-gray-700 line-clamp-1">{duty.course_title}</p>
                                <p className="text-xs text-gray-400 font-medium mt-1">{duty.exam_date}</p>
                            </button>
                        ))
                    ) : (
                        <div className="bg-white p-8 rounded-2xl text-center border-2 border-dashed border-gray-100">
                            <p className="text-gray-400 font-medium">No pending assignments to mark.</p>
                        </div>
                    )}
                </div>

                {/* Replacement Form */}
                <div className="bg-white p-8 rounded-3xl shadow-xl border border-gray-100 h-fit">
                    <h3 className="text-xl font-bold text-gray-900 mb-6">Request Replacement</h3>
                    <AnimatePresence mode="wait">
                        {selectedDuty ? (
                            <motion.form
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.9 }}
                                onSubmit={handleSubmit}
                                className="space-y-6"
                            >
                                <div className="bg-indigo-50 p-4 rounded-xl">
                                    <p className="text-xs font-bold text-indigo-400 uppercase tracking-widest mb-1">Confirm Selection</p>
                                    <p className="font-bold text-indigo-900">Hall {selectedDuty.hall_no} - {selectedDuty.session}</p>
                                </div>

                                <div>
                                    <label className="block text-sm font-bold text-gray-700 mb-2">Reason for Unavailability</label>
                                    <textarea
                                        value={reason}
                                        onChange={(e) => setReason(e.target.value)}
                                        className="w-full p-4 rounded-xl border-gray-200 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-indigo-200 transition-all resize-none h-32 text-gray-800"
                                        placeholder="Please provide a valid reason (e.g., medical emergency, official duty elsewhere)..."
                                        required
                                    ></textarea>
                                </div>

                                <button
                                    type="submit"
                                    disabled={submitting}
                                    className="w-full py-4 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl shadow-lg transition-all active:scale-95 disabled:bg-gray-300"
                                >
                                    {submitting ? 'Processing Replacement...' : 'Submit Request'}
                                </button>

                                <p className="text-[10px] text-gray-400 text-center font-medium px-4">
                                    NOTIFICATION: By submitting, a replacement from your department will be automatically assigned. This action is final and auditable.
                                </p>
                            </motion.form>
                        ) : (
                            <div className="flex flex-col items-center justify-center py-12 text-center">
                                <span className="text-4xl mb-4">👈</span>
                                <p className="text-gray-500 font-medium">Please select an assignment from the left to request a replacement.</p>
                            </div>
                        )}
                    </AnimatePresence>
                </div>
            </div>
        </div>
    );
}
