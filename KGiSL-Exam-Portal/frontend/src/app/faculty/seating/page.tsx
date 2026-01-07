"use client";
import React, { useEffect, useState } from 'react';
import { getFacultyDashboard, getFacultyStudents } from '../../api';
import { motion } from 'framer-motion';

export default function FacultySeating() {
    const [assignments, setAssignments] = useState<any[]>([]);
    const [selectedAssignment, setSelectedAssignment] = useState<any>(null);
    const [students, setStudents] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const token = localStorage.getItem('facultyToken');
        if (token) fetchInitialData(token);
    }, []);

    const fetchInitialData = async (token: string) => {
        try {
            setLoading(true);
            const res = await getFacultyDashboard(token);
            setAssignments(res.data);

            if (res.data.length > 0) {
                const first = res.data[0];
                setSelectedAssignment(first);
                fetchStudents(token, first.hall_no, first.session);
            } else {
                setLoading(false);
            }
        } catch (err) {
            setError('Failed to fetch assignment details');
            setLoading(false);
        }
    };

    const fetchStudents = async (token: string, hall: string, session: string) => {
        try {
            setLoading(true);
            const res = await getFacultyStudents(token, hall, session);
            setStudents(res.data.students || []);
        } catch (err) {
            setError('Failed to fetch student list');
        } finally {
            setLoading(false);
        }
    };

    const handleAssignmentChange = (idx: number) => {
        const token = localStorage.getItem('facultyToken');
        const selected = assignments[idx];
        setSelectedAssignment(selected);
        if (token) fetchStudents(token, selected.hall_no, selected.session);
    };

    if (loading && assignments.length === 0) return (
        <div className="flex items-center justify-center min-h-[60vh]">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
        </div>
    );

    return (
        <div className="space-y-8">
            <header className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-extrabold text-gray-900">Hall Seating</h1>
                    <p className="text-gray-500 mt-2 font-medium">List of students assigned to your halls/sessions.</p>
                </div>

                {assignments.length > 1 && (
                    <div className="bg-white p-2 rounded-xl shadow-sm border border-gray-200 flex gap-2">
                        {assignments.map((a, i) => (
                            <button
                                key={i}
                                onClick={() => handleAssignmentChange(i)}
                                className={`px-4 py-2 rounded-lg text-sm font-bold transition-all ${selectedAssignment?.id === a.id ? 'bg-indigo-600 text-white shadow-md' : 'text-gray-600 hover:bg-gray-100'}`}
                            >
                                Hall {a.hall_no} ({a.session})
                            </button>
                        ))}
                    </div>
                )}
            </header>

            {error && (
                <div className="bg-red-50 border-l-4 border-red-400 p-4 text-red-700 font-medium rounded-r-lg">
                    {error}
                </div>
            )}

            {selectedAssignment ? (
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-100"
                >
                    <div className="bg-gradient-to-r from-indigo-700 to-indigo-900 px-8 py-6 text-white">
                        <div className="flex flex-wrap items-center gap-x-8 gap-y-2">
                            <div>
                                <span className="text-indigo-200 text-xs font-bold uppercase tracking-widest">Hall Number</span>
                                <h2 className="text-2xl font-black">{selectedAssignment.hall_no}</h2>
                            </div>
                            <div>
                                <span className="text-indigo-200 text-xs font-bold uppercase tracking-widest">Session</span>
                                <h2 className="text-2xl font-black">{selectedAssignment.session}</h2>
                            </div>
                            <div className="md:ml-auto text-right">
                                <span className="text-indigo-200 text-xs font-bold uppercase tracking-widest">Course</span>
                                <h2 className="text-lg font-bold">{selectedAssignment.course_title}</h2>
                                <p className="text-indigo-300 font-mono text-xs">{selectedAssignment.course_code}</p>
                            </div>
                        </div>
                    </div>

                    <div className="overflow-x-auto">
                        <table className="w-full text-left border-collapse">
                            <thead>
                                <tr className="bg-gray-50 text-gray-400 text-xs font-bold uppercase tracking-widest border-b border-gray-100">
                                    <th className="px-8 py-4">Seat No</th>
                                    <th className="px-8 py-4">Register Number</th>
                                    <th className="px-8 py-4">Student Name</th>
                                    <th className="px-8 py-4">Department</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-100">
                                {students.length > 0 ? (
                                    students.map((student, idx) => (
                                        <motion.tr
                                            key={student.register_no}
                                            initial={{ opacity: 0 }}
                                            animate={{ opacity: 1 }}
                                            transition={{ delay: idx * 0.02 }}
                                            className="hover:bg-indigo-50/30 transition-colors group"
                                        >
                                            <td className="px-8 py-4 font-mono font-bold text-gray-500 group-hover:text-indigo-600">{student.seat_no}</td>
                                            <td className="px-8 py-4 font-bold text-gray-900 tracking-tight">{student.register_no}</td>
                                            <td className="px-8 py-4 text-gray-700 font-medium">{student.name}</td>
                                            <td className="px-8 py-4">
                                                <span className="bg-indigo-50 text-indigo-700 px-3 py-1 rounded-full text-xs font-bold">
                                                    {student.department}
                                                </span>
                                            </td>
                                        </motion.tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan={4} className="px-8 py-12 text-center text-gray-400 font-medium italic">
                                            No students found for this hall/session.
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </motion.div>
            ) : !loading && (
                <div className="p-12 text-center bg-gray-100 rounded-3xl border-2 border-dashed border-gray-300">
                    <p className="text-gray-500 font-bold">No active assignments to show seeding for.</p>
                </div>
            )}
        </div>
    );
}
