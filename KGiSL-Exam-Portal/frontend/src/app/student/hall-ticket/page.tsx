"use client";
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import api from '../../api';

// Simplified HallTicketPage component
// Displays a "Not yet generated" message for students when hall tickets are pending.
export default function HallTicketPage() {
    const [student, setStudent] = useState<any>(null);
    const router = useRouter();

    useEffect(() => {
        const role = localStorage.getItem('role');
        const data = localStorage.getItem('studentData');
        if (role !== 'student' || !data) {
            router.push('/');
            return;
        }
        setStudent(JSON.parse(data));
    }, []);

    const handleBack = () => {
        router.push('/student');
    };

    if (!student) return null;

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
            <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="bg-white rounded-2xl shadow-2xl p-10 max-w-lg text-center border-t-8 border-indigo-600"
            >
                <div className="text-7xl mb-6">🎫</div>
                <h2 className="text-3xl font-extrabold text-gray-800 mb-4 tracking-tight">Hall Ticket</h2>

                <div className="bg-blue-50 border-l-4 border-blue-500 p-6 mb-8 text-left rounded-r-lg">
                    <p className="text-blue-900 font-semibold text-lg leading-relaxed">
                        Not yet generated, hall ticket will display on end semester exam.
                    </p>
                </div>

                <div className="space-y-4">
                    <div className="text-sm text-gray-500 font-medium">
                        KGiSL Institute of Technology - Office of the COE
                    </div>
                    <button
                        onClick={handleBack}
                        className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-4 rounded-xl font-bold transition-all shadow-lg hover:shadow-indigo-200 w-full text-lg transform active:scale-95"
                    >
                        Go Back to Dashboard
                    </button>
                </div>
            </motion.div>
        </div>
    );
}
