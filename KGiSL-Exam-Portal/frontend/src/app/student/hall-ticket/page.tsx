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
    const [isDownloaded, setIsDownloaded] = useState(false);
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
        setIsDownloaded(true);
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
        <div className="min-h-screen bg-gray-100 flex flex-col items-center py-8 print:block print:bg-white print:p-0">
            {/* Print/Back Buttons - Hidden in print */}
            <div className="w-full max-w-[210mm] mb-4 flex justify-between print:hidden px-4 md:px-0">
                <button
                    onClick={handleBack}
                    className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 md:px-6 md:py-3 rounded-lg font-bold transition shadow-lg text-sm md:text-base"
                >
                    ← Back
                </button>
                <button
                    onClick={handlePrint}
                    disabled={isDownloaded}
                    className={`${isDownloaded
                        ? 'bg-green-600 cursor-not-allowed opacity-80'
                        : 'bg-indigo-600 hover:bg-indigo-700'
                        } text-white px-4 py-2 md:px-6 md:py-3 rounded-lg font-bold transition shadow-lg flex items-center gap-2 text-sm md:text-base`}
                >
                    {isDownloaded ? (
                        <>
                            <span>✅</span> <span className="hidden md:inline">Downloaded</span>
                        </>
                    ) : (
                        <>
                            <span>🖨️</span> <span className="hidden md:inline">Download</span><span className="md:hidden">Print</span>
                        </>
                    )}
                </button>
            </div>

            {/* Hall Ticket Content */}
            {hallTicketData && Object.keys(hallTicketData.semesters).map((semester) => (
                <div key={semester} className="w-full flex flex-col items-center">
                    {/* Page 1: Hall Ticket Details */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="w-full max-w-[210mm] min-h-[297mm] bg-white shadow-2xl overflow-hidden mb-8 print:max-w-none print:w-full print:shadow-none print:mb-0 relative print:h-[297mm] print:flex print:flex-col"
                    >
                        {/* Watermark Logo */}
                        <div className="absolute inset-x-0 top-[20rem] md:top-[28rem] flex justify-center pointer-events-none z-0 print:fixed print:top-[30%] print:left-0 print:w-full">
                            <Image
                                src="/kite-watermark.png"
                                alt="KITE Watermark"
                                width={500}
                                height={300}
                                className="opacity-75 w-64 md:w-[500px]"
                                style={{ objectFit: 'contain' }}
                            />
                        </div>

                        {/* Main Content Container with Standard Padding */}
                        <div className="p-8 h-full flex flex-col relative z-10 print:p-8">

                            <div className="border-4 border-blue-900 p-4 flex-1 flex flex-col print:border-2">
                                {/* Top section with logo, institute name, and NAAC badge */}
                                <div className="flex flex-col md:flex-row items-center md:items-start justify-between gap-4 pb-4 mb-4 print:flex-row print:items-start print:gap-4">
                                    {/* KITE Logo - Top Left */}
                                    <div className="flex-shrink-0 w-32 md:w-40 print:w-32">
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
                                        <h1 className="text-lg md:text-xl font-bold text-blue-900 mb-1 leading-tight" style={{ fontStyle: 'italic' }}>
                                            KGiSL Institute of Technology
                                        </h1>
                                        <p className="text-[10px] md:text-xs text-gray-700 leading-tight">
                                            Affiliated to Anna University, Approved by AICTE, Recognised by UGC,
                                        </p>
                                        <p className="text-[10px] md:text-xs text-gray-700 leading-tight">
                                            Accredited by NAAC & NBA
                                        </p>
                                        <p className="text-[10px] md:text-xs text-gray-700 mt-1 leading-tight">
                                            365, KGiSL Campus, Thudiyalur Road, Saravanampatti, Coimbatore-641035
                                        </p>
                                        <div className="mt-2 pt-2 border-t border-gray-300">
                                            <h2 className="text-xs md:text-sm font-bold text-black tracking-wide">
                                                OFFICE OF THE CONTROLLER OF EXAMINATIONS
                                            </h2>
                                        </div>
                                    </div>

                                    {/* NAAC Badge - Top Right */}
                                    <div className="flex-shrink-0 w-24 md:w-28 print:w-24">
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

                                <div className="text-center bg-blue-900 text-white py-1 mb-4">
                                    <h3 className="text-xs md:text-sm font-semibold">
                                        HALL TICKET FOR THE END SEMESTER EXAMINATIONS - NOV/DEC 2025
                                    </h3>
                                </div>

                                {/* Student Information */}
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mb-4 text-sm print:grid-cols-2 print:gap-4">
                                    <div className="border border-gray-300 p-2 bg-white/70">
                                        <span className="font-semibold block text-xs">NAME OF THE CANDIDATE:</span>
                                        <p className="text-sm md:text-base font-bold mt-1 uppercase">{hallTicketData.student.name}</p>
                                    </div>
                                    <div className="border border-gray-300 p-2 bg-white/70">
                                        <span className="font-semibold block text-xs">REGISTER NUMBER:</span>
                                        <p className="text-sm md:text-base font-bold mt-1">{hallTicketData.student.register_no}</p>
                                    </div>
                                    <div className="border border-gray-300 p-2 bg-white/70">
                                        <span className="font-semibold block text-xs">DEPARTMENT:</span>
                                        <p className="text-xs md:text-sm font-bold mt-1 whitespace-pre-line leading-tight">
                                            {getDepartmentFullName(hallTicketData.student.department)}
                                        </p>
                                    </div>
                                    <div className="border border-gray-300 p-2 bg-white/70">
                                        <span className="font-semibold block text-xs">SEMESTER:</span>
                                        <p className="text-sm md:text-base font-bold mt-1">{semester}</p>
                                    </div>
                                </div>

                                {/* Exam Schedule Table */}
                                <div className="mb-4 relative z-10 overflow-x-auto">
                                    <table className="w-full border-collapse border-2 border-gray-800 bg-white/80 text-xs">
                                        <thead>
                                            <tr className="bg-blue-900 text-white print:bg-gray-300 print:text-black">
                                                <th className="border border-gray-600 p-2 text-left font-bold whitespace-nowrap">S.No</th>
                                                <th className="border border-gray-600 p-2 text-left font-bold whitespace-nowrap">Course Code</th>
                                                <th className="border border-gray-600 p-2 text-left font-bold">Course Title</th>
                                                <th className="border border-gray-600 p-2 text-left font-bold whitespace-nowrap">Exam Date</th>
                                                <th className="border border-gray-600 p-2 text-left font-bold">Session</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {hallTicketData.semesters[semester].map((exam, index) => (
                                                <tr key={index} className={index % 2 === 0 ? 'bg-white/60' : 'bg-gray-50/60'}>
                                                    <td className="border border-gray-400 p-2 text-center">{index + 1}</td>
                                                    <td className="border border-gray-400 p-2 font-semibold whitespace-nowrap">{exam.course_code}</td>
                                                    <td className="border border-gray-400 p-2 min-w-[150px]">{exam.course_title}</td>
                                                    <td className="border border-gray-400 p-2 whitespace-nowrap">{exam.exam_date}</td>
                                                    <td className="border border-gray-400 p-2 font-semibold">{exam.session}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>

                                {/* Session Timings */}
                                <div className="bg-yellow-50/80 border-2 border-yellow-600 p-2 mb-2 relative z-10">
                                    <h4 className="font-bold text-center text-sm mb-1 text-yellow-900">SESSION TIMINGS</h4>
                                    <div className="text-center text-xs font-semibold flex flex-col md:flex-row justify-center gap-1 md:gap-8 print:flex-row print:gap-8">
                                        <p>FN : 09:00 AM TO 12:00 PM</p>
                                        <p>AN : 01:00 PM TO 04:00 PM</p>
                                    </div>
                                </div>

                                {/* Footer Image - Pushed to bottom */}
                                <div className="mt-auto relative z-10 w-full pt-4">
                                    <Image
                                        src="/hall_ticket_footer.png"
                                        alt="Signatures and Instructions Part 1"
                                        width={1000}
                                        height={300}
                                        className="w-full h-auto object-contain"
                                        priority
                                    />
                                </div>
                            </div>
                        </div>
                    </motion.div>

                    {/* Page 2: Instructions Continuation */}
                    <div className="w-full max-w-[210mm] min-h-[297mm] bg-white shadow-2xl overflow-hidden mb-8 print:max-w-none print:w-full print:shadow-none print:mb-0 print:break-before-page print:h-[297mm]">
                        <div className="p-8 h-full flex flex-col relative print:p-8">
                            <h2 className="text-center text-base md:text-lg font-bold underline mb-4 uppercase">INSTRUCTIONS TO THE CANDIDATE</h2>

                            <div className="text-xs md:text-sm text-gray-800 leading-relaxed space-y-2 text-justify">
                                <ol className="list-decimal list-outside pl-5 space-y-2">
                                    <li>Admission to the Examination is provisional.</li>

                                    <li>The Hall Ticket is issued subject to the candidate satisfying the Attendance and other requirements as per Rules, Regulations and Instructions by the Institution from time to time. If found later that the candidate fails to comply with the above requirements, the examinations written by the candidate will be treated as cancelled.</li>

                                    <li>A seat marked with Register Number will be allotted to each candidate. Candidate will occupy the allotted seat at least 10 minutes before the commencement of the examinations. In no case, candidate shall be allowed to occupy a seat other than the seat allotted to him/her.</li>

                                    <li>Normally the Candidate will not be permitted to enter the hall after the commencement of the examination. Only on extraordinary circumstances, the candidates will be permitted during the first thirty minutes of the examination after obtaining a written permission form the Principal / C.S Under any circumstances the Candidate shall not permitted to enter the hall after the expiry of first thirty minutes.</li>

                                    <li>Candidate shall not be allowed to leave the examination hall before the expiry of 45 minutes from the commencement of examination. The candidate who leaves the examination hall during the period allotted for a paper will not be permitted to enter the hall again.</li>

                                    <li>Candidate who is suffering from infectious diseases of any kind shall not be admitted to the examination hall.</li>

                                    <li>Strict silence should be maintained in the examination hall.</li>

                                    <li>Candidate is required to bring his / her own pens, pencils and erasers. Candidates should use only blue or black pens while answering his / her papers.</li>

                                    <li>Before proceeding to write answers in answer book, the candidate should write his / her register number, semester, course code, title, date, session of the examination at the appropriate space provided in the first page of the answer book and nowhere else in the answer book or in any additional attachment like drawing sheet, smith chart etc.</li>

                                    <li>If a candidate writes his/her register number on any part of the answer book / sheets other than one provided for or puts any special mark or writes anything which may disclose, in any way, the identity of the Candidate, he / she will render himself / herself liable for disciplinary action.</li>

                                    <li>Writing of wrong register number in the answer book, will entail rejection of the answer book.</li>

                                    <li>Candidate is not allowed to exceed the prescribed time assigned to each other.</li>

                                    <li>Candidate shall not talk to their colleagues during the examination.</li>

                                    <li>Candidate shall not carry any written/printed matter, any paper material, cell phone, smart watch, pen drive, ipad, programmable calculator, any unauthorized data sheet/table into the examination hall and if anything is found in his / her possession he / she shall be liable for disciplinary action.</li>

                                    <li>No Candidate shall pass any part or whole of answer papers or question papers to any other candidate. No candidate shall allow another candidate to copy from his/her answer paper or copy from the answer paper of another candidate. If found committing such malpractice, the involved candidates shall be liable for disciplinary action.</li>

                                    <li>Candidate found guilty or using unfair means of any nature shall be liable for disciplinary action.</li>

                                    <li>Candidate will have to hand over the answer book to the Invigilator / Chief Superintendent before leaving the examination hall.</li>

                                    <li>Candidate should produce the hall ticket on demand by the Invigilator / Chief Superintendent / Anna University Representative / Squad members.</li>

                                    <li>Candidate shall not write anything in the Hall Ticket.</li>

                                    <li>Candidates shall write only the Register no. in the space provided in the Question Paper. Any other writings in the Question Paper are strictly prohibited.</li>
                                </ol>
                            </div>

                            <div className="mt-8 md:mt-12 mb-4 md:mb-8 text-right font-bold text-gray-900 text-xs md:text-base print:mt-auto">
                                <p>CONTROLLER OF EXAMINATIONS</p>
                            </div>
                        </div>
                    </div>
                </div>
            ))}

            <style jsx global>{`
                @media print {
                    @page {
                        margin: 0;
                        size: A4;
                    }
                    body {
                        print-color-adjust: exact;
                        -webkit-print-color-adjust: exact;
                        background-color: white;
                    }
                }
            `}</style>
        </div>
    );
}
