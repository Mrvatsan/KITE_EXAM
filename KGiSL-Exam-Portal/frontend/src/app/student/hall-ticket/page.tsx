"use client";
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import api from '../../api';
import Image from 'next/image';

interface Exam {
    course_code: string;
    course_title: string;
    exam_date: string;
    session: string;
}

interface HallTicketData {
    student: {
        name: string;
        register_no: string;
        department: string;
    };
    semesters: {
        [key: string]: Exam[];
    };
}

// Department code to full name mapping
const getDepartmentFullName = (deptCode: string): string => {
    const deptMap: { [key: string]: string } = {
        'AI&ML': 'B.E. Computer Science and Engineering\n(Artificial Intelligence and Machine Learning)',
        'AI&DS': 'B.E. Computer Science and Engineering\n(Artificial Intelligence and Data Science)',
        'CSE': 'B.E. Computer Science and Engineering',
        'ECE': 'B.E. Electronics and Communication Engineering',
        'IT': 'B.Tech. Information Technology',
        'MECH': 'B.E. Mechanical Engineering',
        'R&A': 'B.E. Robotics and Automation',
        'CSBS': 'B.E. Computer Science and Business Systems',
        'CYS': 'B.E. Cyber Security'
    };

    return deptMap[deptCode] || deptCode;
};

export default function HallTicketPage() {
    const [student, setStudent] = useState<any>(null);
    const [hallTicketData, setHallTicketData] = useState<HallTicketData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const router = useRouter();

    useEffect(() => {
        const role = localStorage.getItem('role');
        const data = localStorage.getItem('studentData');
        if (role !== 'student' || !data) {
            router.push('/');
            return;
        }
        const studentData = JSON.parse(data);
        setStudent(studentData);
        fetchHallTicket(studentData.register_no);
    }, []);

    const fetchHallTicket = async (registerNo: string) => {
        try {
            setLoading(true);
            const response = await api.get(`/api/hall-ticket/?register_no=${registerNo}`);
            setHallTicketData(response.data);
            setError('');
        } catch (err: any) {
            console.error('Hall ticket fetch error:', err);
            setError(err.response?.data?.error || 'Failed to fetch hall ticket data');
        } finally {
            setLoading(false);
        }
    };

    const handlePrint = () => {
        window.print();
    };

    const handleBack = () => {
        router.push('/student');
    };

    if (!student) return null;

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-100">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-indigo-600 mx-auto mb-4"></div>
                    <p className="text-xl text-gray-700">Loading hall ticket...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
                <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="bg-white rounded-xl shadow-xl p-8 max-w-md text-center"
                >
                    <div className="text-6xl mb-4">⚠️</div>
                    <h2 className="text-2xl font-bold text-red-600 mb-3">Error</h2>
                    <p className="text-gray-700 mb-6">{error}</p>
                    <button
                        onClick={handleBack}
                        className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-lg font-bold transition"
                    >
                        Go Back
                    </button>
                </motion.div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-100 p-4">
            {/* Print/Back Buttons - Hidden in print */}
            <div className="max-w-5xl mx-auto mb-4 flex justify-between print:hidden">
                <button
                    onClick={handleBack}
                    className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-lg font-bold transition shadow-lg"
                >
                    ← Back
                </button>
                <button
                    onClick={handlePrint}
                    className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-lg font-bold transition shadow-lg"
                >
                    🖨️ Print Hall Ticket
                </button>
            </div>

            {/* Hall Ticket Content */}
            {hallTicketData && Object.keys(hallTicketData.semesters).map((semester) => (
                <motion.div
                    key={semester}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="max-w-5xl mx-auto bg-white shadow-2xl rounded-lg overflow-hidden mb-8 print:shadow-none print:mb-12 print:break-after-page relative"
                >
                    {/* Watermark Logo */}
                    <div className="absolute inset-0 flex items-start justify-center pointer-events-none z-0 pt-[28rem]">
                        <Image
                            src="/kite-watermark.png"
                            alt="KITE Watermark"
                            width={500}
                            height={300}
                            className="opacity-75"
                            style={{ objectFit: 'contain' }}
                        />
                    </div>

                    {/* Header */}
                    <div className="border-4 border-blue-900 p-6 relative z-10">
                        {/* Top section with logo, institute name, and NAAC badge */}
                        <div className="flex items-start justify-between gap-6 pb-4 mb-4">
                            {/* KITE Logo - Top Left */}
                            <div className="flex-shrink-0 w-48">
                                <Image
                                    src="/kite-logo.png"
                                    alt="KITE Logo"
                                    width={180}
                                    height={180}
                                    className="object-contain"
                                    priority
                                />
                            </div>

                            {/* Institute Information - Center */}
                            <div className="flex-1 text-center">
                                <h1 className="text-2xl font-bold text-blue-900 mb-1" style={{ fontStyle: 'italic' }}>
                                    KGiSL Institute of Technology
                                </h1>
                                <p className="text-xs text-gray-700 leading-relaxed">
                                    Affiliated to Anna University, Approved by AICTE, Recognised by UGC,
                                </p>
                                <p className="text-xs text-gray-700">
                                    Accredited by NAAC & NBA
                                </p>
                                <p className="text-xs text-gray-700 mt-1">
                                    365, KGiSL Campus, Thudiyalur Road, Saravanampatti, Coimbatore-641035
                                </p>
                                <div className="mt-3 pt-3 border-t border-gray-300">
                                    <h2 className="text-sm font-bold text-black tracking-wide">
                                        OFFICE OF THE CONTROLLER OF EXAMINATIONS
                                    </h2>
                                </div>
                            </div>

                            {/* NAAC Badge - Top Right */}
                            <div className="flex-shrink-0 w-32">
                                <Image
                                    src="/naac-badge-v2.png"
                                    alt="NAAC Badge"
                                    width={120}
                                    height={120}
                                    className="object-contain"
                                    priority
                                />
                            </div>
                        </div>

                        <div className="text-center bg-blue-900 text-white py-3 mb-6">
                            <h3 className="text-base font-semibold">
                                HALL TICKET FOR THE END SEMESTER EXAMINATIONS - NOV/DEC 2025
                            </h3>
                        </div>

                        {/* Student Information */}
                        <div className="grid grid-cols-2 gap-4 mb-6 text-sm">
                            <div className="border border-gray-300 p-3 bg-white/70">
                                <span className="font-semibold">NAME OF THE CANDIDATE:</span>
                                <p className="text-lg font-bold mt-1">{hallTicketData.student.name}</p>
                            </div>
                            <div className="border border-gray-300 p-3 bg-white/70">
                                <span className="font-semibold">REGISTER NUMBER:</span>
                                <p className="text-lg font-bold mt-1">{hallTicketData.student.register_no}</p>
                            </div>
                            {/* Department with full name - Change 2 */}
                            <div className="border border-gray-300 p-3 bg-white/70">
                                <span className="font-semibold">DEPARTMENT:</span>
                                <p className="text-base font-bold mt-1 whitespace-pre-line leading-tight">
                                    {getDepartmentFullName(hallTicketData.student.department)}
                                </p>
                            </div>
                            <div className="border border-gray-300 p-3 bg-white/70">
                                <span className="font-semibold">SEMESTER:</span>
                                <p className="text-lg font-bold mt-1">{semester}</p>
                            </div>
                        </div>

                        {/* Exam Schedule Table */}
                        <div className="mb-6 relative z-10">
                            <table className="w-full border-collapse border-2 border-gray-800 bg-white/80">
                                <thead>
                                    <tr className="bg-blue-900 text-white">
                                        <th className="border border-gray-600 p-3 text-left font-bold">S.No</th>
                                        <th className="border border-gray-600 p-3 text-left font-bold">Course Code</th>
                                        <th className="border border-gray-600 p-3 text-left font-bold">Course Title</th>
                                        <th className="border border-gray-600 p-3 text-left font-bold">Exam Date</th>
                                        <th className="border border-gray-600 p-3 text-left font-bold">Session</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {hallTicketData.semesters[semester].map((exam, index) => (
                                        <tr key={index} className={index % 2 === 0 ? 'bg-white/60' : 'bg-gray-50/60'}>
                                            <td className="border border-gray-400 p-3">{index + 1}</td>
                                            <td className="border border-gray-400 p-3 font-semibold">{exam.course_code}</td>
                                            <td className="border border-gray-400 p-3">{exam.course_title}</td>
                                            <td className="border border-gray-400 p-3">{exam.exam_date}</td>
                                            <td className="border border-gray-400 p-3 font-semibold">{exam.session}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>

                        {/* Session Timings */}
                        <div className="bg-yellow-50/80 border-2 border-yellow-600 p-4 mb-4 relative z-10">
                            <h4 className="font-bold text-center text-lg mb-2 text-yellow-900">SESSION TIMINGS</h4>
                            <div className="text-center text-sm font-semibold">
                                <p>FN : 09:00 AM TO 12:00 PM</p>
                                <p>AN : 01:00 PM TO 04:00 PM</p>
                            </div>
                        </div>

                        {/* Instructions */}
                        <div className="text-xs text-gray-600 border-t-2 border-gray-300 pt-3 relative z-10">
                            <ol className="list-decimal list-inside space-y-1">
                                <li>In case of candidates who have been Readmitted/Transferred, this Hall Ticket is valid only for the current semester examinations.</li>
                                <li>Any discrepancy in the Name / Date of Birth and missing of Photograph or incorrect Photograph, if any is to be updated to the COE office for the correction.</li>
                                <li>Instructions printed overleaf are to be followed strictly.</li>
                            </ol>
                        </div>
                    </div>
                </motion.div>
            ))}

            <style jsx global>{`
                @media print {
                    body {
                        print-color-adjust: exact;
                        -webkit-print-color-adjust: exact;
                    }
                }
            `}</style>
        </div>
    );
}
