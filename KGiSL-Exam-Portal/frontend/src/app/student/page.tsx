"use client";
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';

export default function StudentLandingPage() {
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

    const navigationCards = [
        {
            title: 'Hall Seating',
            description: 'View your exam hall and seat details',
            icon: '🪑',
            route: '/student/hall-seating',
            gradient: 'from-blue-500 to-blue-700'
        },
        {
            title: 'Hall Ticket',
            description: 'Download your examination hall ticket',
            icon: '🎫',
            route: '/student/hall-ticket',
            gradient: 'from-purple-500 to-purple-700'
        },
        {
            title: 'Logout',
            description: 'Sign out from your account',
            icon: '🚪',
            action: handleLogout,
            gradient: 'from-red-500 to-red-700'
        }
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-indigo-100 via-purple-50 to-pink-100 flex items-center justify-center p-4 relative">
            {/* Background Image */}
            <div className="absolute inset-0 bg-cover bg-center z-0 opacity-20" style={{ backgroundImage: 'url("/bg.jpg")' }}></div>

            <div className="w-full max-w-6xl z-10">
                {/* Header */}
                <motion.div
                    initial={{ opacity: 0, y: -30 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-center mb-12"
                >
                    <h1 className="text-5xl font-bold text-indigo-900 mb-3 drop-shadow-lg">
                        Welcome, {student.name}
                    </h1>
                    <p className="text-xl text-indigo-700 font-medium">
                        Register Number: {student.register_no}
                    </p>
                </motion.div>

                {/* Navigation Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {navigationCards.map((card, index) => (
                        <motion.div
                            key={card.title}
                            initial={{ opacity: 0, y: 30 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.1 }}
                            whileHover={{ scale: 1.05, y: -10 }}
                            whileTap={{ scale: 0.95 }}
                            onClick={() => card.action ? card.action() : router.push(card.route!)}
                            className={`bg-gradient-to-br ${card.gradient} rounded-3xl shadow-2xl p-8 cursor-pointer transform transition-all duration-300 hover:shadow-3xl`}
                        >
                            <div className="text-center">
                                <div className="text-7xl mb-6 filter drop-shadow-lg">
                                    {card.icon}
                                </div>
                                <h2 className="text-3xl font-bold text-white mb-3 tracking-wide">
                                    {card.title}
                                </h2>
                                <p className="text-white/90 text-lg font-medium">
                                    {card.description}
                                </p>
                            </div>
                        </motion.div>
                    ))}
                </div>

                {/* Footer */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5 }}
                    className="text-center mt-12"
                >
                    <p className="text-indigo-600 text-sm">
                        KGiSL Institute of Technology - Exam Portal
                    </p>
                </motion.div>
            </div>
        </div>
    );
}
