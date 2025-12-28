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

// --- Branding / Layout Components ---

const BrandingHeader = () => (
    <div className="flex flex-row items-start justify-between gap-4 pb-4 mb-4 border-b border-blue-900/10">
        {/* KITE Logo - Top Left */}
        <div className="flex-shrink-0 w-40">
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
            <h1 className="text-xl font-bold text-blue-900 mb-1 leading-tight italic">
                KGiSL Institute of Technology
            </h1>
            <p className="text-[10px] text-gray-700 leading-tight">
                Affiliated to Anna University, Approved by AICTE, Recognised by UGC,
            </p>
            <p className="text-[10px] text-gray-700 leading-tight">
                Accredited by NAAC & NBA
            </p>
            <p className="text-[10px] text-gray-700 mt-1 leading-tight">
                365, KGiSL Campus, Thudiyalur Road, Saravanampatti, Coimbatore-641035
            </p>
            <div className="mt-2 pt-2 border-t border-gray-300">
                <h2 className="text-sm font-bold text-black tracking-wide">
                    OFFICE OF THE CONTROLLER OF EXAMINATIONS
                </h2>
            </div>
        </div>

        {/* NAAC Badge - Top Right */}
        <div className="flex-shrink-0 w-28">
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
);

// Reusable A4 Page Container
// STRICT DIMENSIONS: 210mm x 297mm
const A4Page = ({ children, className = "" }: { children: React.ReactNode, className?: string }) => (
    <div className={`
        w-[210mm] h-[297mm] 
        bg-white shadow-2xl 
        mx-auto my-8 
        relative overflow-hidden
        print:shadow-none print:m-0 print:break-after-page print:h-[297mm]
        ${className}
    `}>
        {children}
    </div>
);

// Inner Content Frame with Blue Border
// STRICT PADDING: Consistent branding wrapper
const ContentFrame = ({ children }: { children: React.ReactNode }) => (
    <div className="w-full h-full p-[15mm]">
        <div className="w-full h-full border-4 border-blue-900 p-4 flex flex-col relative">
            {/* Watermark Logo (Background) */}
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none z-0">
                <Image
                    src="/kite-watermark.png"
                    alt="KITE Watermark"
                    width={500}
                    height={300}
                    className="opacity-[0.30] w-[500px]"
                    style={{ objectFit: 'contain' }}
                />
            </div>

            {/* Content (Foreground) */}
            <div className="relative z-10 flex flex-col h-full">
                {children}
            </div>
        </div>
    </div>
);

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
        <div className="min-h-screen bg-gray-100 overflow-auto print:overflow-hidden print:bg-white">
            {/* Control Bar */}
            <div className="sticky top-0 z-50 bg-gray-800 text-white p-4 shadow-md print:hidden flex justify-between items-center">
                <button
                    onClick={handleBack}
                    className="bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded font-bold text-sm"
                >
                    ← Back
                </button>
                <div className="text-sm font-medium opacity-80 hidden md:block">
                    A4 Viewing Mode • Use landscape for best mobile view
                </div>
                <button
                    onClick={handlePrint}
                    disabled={isDownloaded}
                    className={`${isDownloaded
                        ? 'bg-green-600 cursor-not-allowed'
                        : 'bg-indigo-600 hover:bg-indigo-500'
                        } text-white px-6 py-2 rounded font-bold flex items-center gap-2 text-sm shadow-sm transition-all`}
                >
                    {isDownloaded ? (
                        <><span>✅</span> Downloaded</>
                    ) : (
                        <><span>🖨️</span> Download PDF</>
                    )}
                </button>
            </div>

            {/* Scrollable Document Container */}
            <div className="w-full overflow-auto flex flex-col items-center py-8 print:p-0 print:block">

                {hallTicketData && Object.keys(hallTicketData.semesters).map((semester) => (
                    <div key={semester}>
                        {/* ---------------- PAGE 1 ---------------- */}
                        <A4Page>
                            <ContentFrame>
                                <BrandingHeader />

                                <div className="text-center bg-blue-900 text-white py-1 mb-4 print:py-1 -mx-4 md:mx-0">
                                    <h3 className="text-sm font-semibold tracking-wide">
                                        HALL TICKET FOR THE END SEMESTER EXAMINATIONS - NOV/DEC 2025
                                    </h3>
                                </div>

                                {/* Student Info Table - Fixed Grid */}
                                <div className="grid grid-cols-2 gap-x-4 gap-y-2 mb-4 text-sm">
                                    <div className="border border-gray-300 p-2 bg-white/80">
                                        <span className="font-semibold block text-[10px] text-gray-500">NAME OF THE CANDIDATE</span>
                                        <p className="font-bold uppercase text-[12pt]">{hallTicketData.student.name}</p>
                                    </div>
                                    <div className="border border-gray-300 p-2 bg-white/80">
                                        <span className="font-semibold block text-[10px] text-gray-500">REGISTER NUMBER</span>
                                        <p className="font-bold text-[12pt]">{hallTicketData.student.register_no}</p>
                                    </div>
                                    <div className="border border-gray-300 p-2 bg-white/80">
                                        <span className="font-semibold block text-[10px] text-gray-500">DEPARTMENT</span>
                                        <p className="font-bold text-[10pt] leading-tight">
                                            {getDepartmentFullName(hallTicketData.student.department)}
                                        </p>
                                    </div>
                                    <div className="border border-gray-300 p-2 bg-white/80">
                                        <span className="font-semibold block text-[10px] text-gray-500">SEMESTER</span>
                                        <p className="font-bold text-[12pt]">{semester}</p>
                                    </div>
                                </div>

                                {/* Exam Table */}
                                <div className="mb-4 flex-1">
                                    <table className="w-full border-collapse border border-gray-800 text-[10pt]">
                                        <thead>
                                            <tr className="bg-blue-900 text-white print:bg-gray-200 print:text-black">
                                                <th className="border border-gray-600 p-1 w-12 text-center">S.No</th>
                                                <th className="border border-gray-600 p-1 w-24 text-left">Course Code</th>
                                                <th className="border border-gray-600 p-1 text-left">Course Title</th>
                                                <th className="border border-gray-600 p-1 w-24 text-center">Date</th>
                                                <th className="border border-gray-600 p-1 w-20 text-center">Session</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {hallTicketData.semesters[semester].map((exam, index) => (
                                                <tr key={index} className="odd:bg-white even:bg-gray-50">
                                                    <td className="border border-gray-400 p-1 text-center">{index + 1}</td>
                                                    <td className="border border-gray-400 p-1 font-semibold">{exam.course_code}</td>
                                                    <td className="border border-gray-400 p-1">{exam.course_title}</td>
                                                    <td className="border border-gray-400 p-1 text-center whitespace-nowrap">{exam.exam_date}</td>
                                                    <td className="border border-gray-400 p-1 text-center font-bold">{exam.session}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>

                                {/* Timings */}
                                <div className="border-2 border-yellow-600 bg-yellow-50 p-2 mb-2">
                                    <h4 className="font-bold text-center text-sm text-yellow-900 mb-1">SESSION TIMINGS</h4>
                                    <div className="flex justify-center gap-12 text-xs font-bold text-gray-800">
                                        <span>FN : 09:00 AM TO 12:00 PM</span>
                                        <span>AN : 01:00 PM TO 04:00 PM</span>
                                    </div>
                                </div>

                                {/* Footer Image (Signatures) */}
                                <div className="mt-auto w-full">
                                    <Image
                                        src="/hall_ticket_footer.png"
                                        alt="Signatures"
                                        width={1000}
                                        height={300}
                                        className="w-full h-auto object-contain"
                                        priority
                                    />
                                </div>
                            </ContentFrame>
                        </A4Page>

                        {/* ---------------- PAGE 2 ---------------- */}
                        <A4Page>
                            <ContentFrame>
                                <div className="flex-1 flex flex-col p-2 bg-white/80">
                                    <h2 className="text-center text-lg font-bold underline mb-2 uppercase tracking-wide">
                                        INSTRUCTIONS TO THE CANDIDATE
                                    </h2>

                                    <div className="text-[9pt] text-gray-900 leading-tight text-justify">
                                        <ol className="list-decimal list-outside pl-6 space-y-1">
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

                                    <div className="mt-auto mb-4 text-right">
                                        <p className="font-bold text-sm">CONTROLLER OF EXAMINATIONS</p>
                                    </div>
                                </div>
                            </ContentFrame>
                        </A4Page>
                    </div>
                ))}
            </div>

            <style jsx global>{`
                @media print {
                    @page {
                        margin: 0;
                        size: A4 portrait;
                    }
                    body {
                        -webkit-print-color-adjust: exact;
                        print-color-adjust: exact;
                        background-color: white !important;
                    }
                }
            `}</style>
        </div>
    );
}
