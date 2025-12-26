"use client";
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';

export default function StudentDashboard() {
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

    const handleLogout = () => {
        localStorage.clear();
        router.push('/');
    };

    if (!student) return null;

    return (
        <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4 relative">
            {/* Background Image Placeholder */}
            <div className="absolute inset-0 bg-cover bg-center z-0" style={{ backgroundImage: 'url("https://images.unsplash.com/photo-1562774053-701939374585?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80")' }}></div>
            <div className="absolute inset-0 bg-white/90 z-0"></div>

            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="bg-blue-900 text-white w-full max-w-4xl rounded-2xl shadow-2xl overflow-hidden z-10 grid grid-cols-1 md:grid-cols-2 relative border border-blue-800"
            >
                {/* Header Strip inside Card */}
                <div className="md:col-span-2 bg-blue-950 px-8 py-4 flex justify-between items-center border-b border-blue-800">
                    <h1 className="text-xl font-bold tracking-widest uppercase">SinthanAI Login Portal</h1>
                    <div className="flex gap-2">
                        <span className="bg-white text-blue-900 px-3 py-1 rounded text-xs font-bold">Student</span>
                        <button onClick={handleLogout} className="bg-red-500 hover:bg-red-600 px-3 py-1 rounded text-xs font-bold transition">Logout</button>
                    </div>
                </div>

                {/* Data Grid */}
                <div className="md:col-span-2 p-8 grid grid-cols-1 md:grid-cols-2 gap-y-6 gap-x-12">

                    <div className="bg-blue-800/50 p-4 rounded-lg border border-blue-700">
                        <label className="block text-blue-300 text-sm font-medium mb-1">Register number:</label>
                        <p className="text-xl font-bold">{student.register_no}</p>
                    </div>

                    <div className="bg-blue-800/50 p-4 rounded-lg border border-blue-700">
                        <label className="block text-blue-300 text-sm font-medium mb-1">Name:</label>
                        <p className="text-xl font-bold">{student.name}</p>
                    </div>

                    <div className="bg-blue-800/50 p-4 rounded-lg border border-blue-700">
                        <label className="block text-blue-300 text-sm font-medium mb-1">Course code:</label>
                        <p className="text-xl font-bold">{student.course_code}</p>
                    </div>

                    <div className="bg-blue-800/50 p-4 rounded-lg border border-blue-700">
                        <label className="block text-blue-300 text-sm font-medium mb-1">Course Title:</label>
                        <p className="text-xl font-bold">{student.course_title}</p>
                    </div>

                    <div className="bg-blue-800/50 p-4 rounded-lg border border-blue-700">
                        <label className="block text-blue-300 text-sm font-medium mb-1">Exam date:</label>
                        <p className="text-xl font-bold">{student.exam_date}</p>
                    </div>

                    <div className="bg-blue-800/50 p-4 rounded-lg border border-blue-700">
                        <label className="block text-blue-300 text-sm font-medium mb-1">Session:</label>
                        <p className="text-xl font-bold">{student.session}</p>
                    </div>

                    <div className="bg-blue-800/50 p-4 rounded-lg border border-blue-700">
                        <label className="block text-blue-300 text-sm font-medium mb-1">Hall No:</label>
                        <p className="text-xl font-bold">{student.hall_no}</p>
                    </div>

                    <div className="bg-blue-800/50 p-4 rounded-lg border border-blue-700">
                        <label className="block text-blue-300 text-sm font-medium mb-1">Seat No.:</label>
                        <p className="text-xl font-bold">{student.seat_no}</p>
                    </div>

                </div>
            </motion.div>
        </div>
    );
}
