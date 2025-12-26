"use client";
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';

export default function HallSeatingPage() {
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

    // Helper function to determine block from hall number
    const getBlockFromHallNo = (hallNo: string): string => {
        const hallNum = parseInt(hallNo);
        if (isNaN(hallNum)) return 'Unknown';

        // 3-digit numbers (100-999) = Academic Block
        // 4+ digit numbers (1000+) = Innovation Block
        if (hallNum >= 100 && hallNum <= 999) {
            return 'Academic Block';
        } else if (hallNum >= 1000) {
            return 'Innovation Block (IT Tower)';
        }

        return 'Unknown';
    };

    // Helper function to determine floor from hall number based on block
    const getFloorFromHallNo = (hallNo: string, block: string): string => {
        const hallNum = parseInt(hallNo);
        if (isNaN(hallNum)) return 'Unknown';

        if (block === 'Academic Block') {
            // Use hundreds series for Academic Block
            if (hallNum >= 100 && hallNum <= 199) return 'Ground Floor';
            if (hallNum >= 200 && hallNum <= 299) return 'First Floor';
            if (hallNum >= 300 && hallNum <= 399) return 'Second Floor';
            if (hallNum >= 400 && hallNum <= 499) return 'Third Floor';
            if (hallNum >= 500 && hallNum <= 599) return 'Fourth Floor';
            if (hallNum >= 600 && hallNum <= 699) return 'Fifth Floor';
        } else if (block === 'Innovation Block (IT Tower)') {
            // Use thousands series for Innovation Block
            if (hallNum >= 1000 && hallNum <= 1999) return 'First Floor';
            if (hallNum >= 2000 && hallNum <= 2999) return 'Second Floor';
            if (hallNum >= 3000 && hallNum <= 3999) return 'Third Floor';
            if (hallNum >= 4000 && hallNum <= 4999) return 'Fourth Floor';
            if (hallNum >= 5000 && hallNum <= 5999) return 'Fifth Floor';
        }

        return 'Unknown';
    };

    if (!student) return null;

    const block = getBlockFromHallNo(student.hall_no);
    const floor = getFloorFromHallNo(student.hall_no, block);

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
                    <h1 className="text-xl font-bold tracking-widest uppercase">Hall Seating Details</h1>
                    <div className="flex gap-2">
                        <button onClick={handleBack} className="bg-indigo-500 hover:bg-indigo-600 px-3 py-1 rounded text-xs font-bold transition">Back</button>
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

                    <div className="bg-blue-800/50 p-4 rounded-lg border border-blue-700">
                        <label className="block text-blue-300 text-sm font-medium mb-1">Block:</label>
                        <p className="text-xl font-bold">{block}</p>
                    </div>

                    <div className="bg-blue-800/50 p-4 rounded-lg border border-blue-700">
                        <label className="block text-blue-300 text-sm font-medium mb-1">Floor:</label>
                        <p className="text-xl font-bold">{floor}</p>
                    </div>

                </div>
            </motion.div>
        </div>
    );
}
