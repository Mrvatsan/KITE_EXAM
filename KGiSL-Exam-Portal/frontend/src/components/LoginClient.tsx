"use client";
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { loginAdmin, loginStudent, loginFaculty, getBaseApiUrl } from '../app/api';
import { useRouter } from 'next/navigation';

export default function LoginClient() {
    const [role, setRole] = useState('student'); // 'student', 'admin', or 'faculty'
    const [identifier, setIdentifier] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [showConfig, setShowConfig] = useState(false);
    const [backendUrl, setBackendUrl] = useState('');
    const router = useRouter();

    useEffect(() => {
        setBackendUrl(getBaseApiUrl());
    }, []);

    const saveBackendUrl = () => {
        if (backendUrl.trim()) {
            localStorage.setItem('API_URL', backendUrl.trim());
            setError('');
            setShowConfig(false);
        }
    };

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            let res;
            if (role === 'admin') {
                res = await loginAdmin(identifier, password);
                localStorage.setItem('role', 'admin');
                localStorage.setItem('username', res.data.username);
                router.push('/admin/dashboard');
            } else if (role === 'faculty') {
                res = await loginFaculty(identifier, password);
                localStorage.setItem('role', 'faculty');
                localStorage.setItem('facultyToken', res.data.token);
                localStorage.setItem('facultyData', JSON.stringify(res.data));
                router.push('/faculty/dashboard');
            } else {
                res = await loginStudent(identifier, password);
                localStorage.setItem('role', 'student');
                localStorage.setItem('studentData', JSON.stringify(res.data));
                router.push('/student');
            }
        } catch (err: any) {
            console.error('Login error:', err);
            if (err.response?.data?.error) {
                setError(err.response.data.error);
            } else if (err.code === 'ECONNABORTED' || err.message?.includes('timeout')) {
                setError('Backend is waking up (Render free tier takes ~50s on cold start). Please wait 10 seconds and click Login again.');
            } else if (!err.response) {
                const currentApi = getBaseApiUrl();
                setError(`Cannot reach Backend API at (${currentApi}). If your backend is waking up on Render or has a custom URL, you can check settings below.`);
                setShowConfig(true);
            } else {
                setError(err.message || 'Login failed');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-200 relative">
            <div className="absolute inset-0 bg-cover bg-center z-0" style={{ backgroundImage: 'url("/bg.jpg")' }}></div>
            <div className="absolute inset-0 bg-black opacity-30 z-0"></div>

            <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass-effect p-8 rounded-2xl shadow-2xl w-full max-w-md z-10 relative bg-white/30 backdrop-blur-xl border border-white/40"
            >
                <div className="text-center mb-6">
                    <h1 className="text-3xl font-bold text-indigo-900 drop-shadow-sm">KGiSL Exam Portal</h1>
                </div>

                <div className="flex bg-white/50 p-1 rounded-full mb-8 w-fit mx-auto shadow-inner">
                    <button
                        onClick={() => { setRole('student'); setError(''); }}
                        className={`px-6 py-2 rounded-full text-sm font-bold transition-all ${role === 'student' ? 'bg-white text-indigo-900 shadow-md' : 'text-gray-700 hover:text-indigo-800'}`}
                    >
                        Student
                    </button>
                    <button
                        onClick={() => { setRole('faculty'); setError(''); }}
                        className={`px-6 py-2 rounded-full text-sm font-bold transition-all ${role === 'faculty' ? 'bg-white text-indigo-900 shadow-md' : 'text-gray-700 hover:text-indigo-800'}`}
                    >
                        Faculty
                    </button>
                    <button
                        onClick={() => { setRole('admin'); setError(''); }}
                        className={`px-6 py-2 rounded-full text-sm font-bold transition-all ${role === 'admin' ? 'bg-white text-indigo-900 shadow-md' : 'text-gray-700 hover:text-indigo-800'}`}
                    >
                        Admin
                    </button>
                </div>

                <div className="text-center mb-6">
                    <h2 className="text-white text-lg font-medium tracking-wide">
                        {role === 'student' ? 'Student Login' : role === 'faculty' ? 'Faculty Login' : 'Admin Login'}
                    </h2>
                </div>

                <form onSubmit={handleLogin} className="space-y-5">
                    <div>
                        <input
                            type="text"
                            value={identifier}
                            onChange={(e) => setIdentifier(e.target.value)}
                            className="w-full px-5 py-3 rounded-lg border-0 bg-white/80 placeholder-gray-500 text-gray-900 focus:ring-2 focus:ring-indigo-300 focus:bg-white transition-all shadow-sm"
                            placeholder={role === 'admin' ? 'Username' : role === 'faculty' ? 'Faculty ID / Staff Code' : 'Register Number'}
                            required
                        />
                    </div>

                    <div>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full px-5 py-3 rounded-lg border-0 bg-white/80 placeholder-gray-500 text-gray-900 focus:ring-2 focus:ring-indigo-300 focus:bg-white transition-all shadow-sm"
                            placeholder="Password"
                            required
                        />
                    </div>

                    {error && (
                        <div className="text-red-100 bg-red-600/80 p-3 rounded-lg text-center text-xs font-semibold leading-relaxed shadow">
                            {error}
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full py-3 rounded-lg bg-white text-indigo-900 font-bold text-lg shadow-lg hover:bg-gray-50 hover:shadow-xl transition-all transform hover:-translate-y-1 disabled:opacity-75"
                    >
                        {loading ? 'Connecting to Backend...' : 'Login'}
                    </button>

                    <div className="text-center pt-1">
                        <button
                            type="button"
                            onClick={() => setShowConfig(!showConfig)}
                            className="text-xs text-white/80 hover:text-white underline"
                        >
                            {showConfig ? 'Hide API URL Settings' : '⚙️ Backend Server Settings'}
                        </button>
                    </div>

                    {showConfig && (
                        <div className="bg-black/40 p-3 rounded-lg space-y-2 text-left border border-white/20">
                            <label className="text-xs text-white font-medium block">
                                Backend API URL:
                            </label>
                            <input
                                type="text"
                                value={backendUrl}
                                onChange={(e) => setBackendUrl(e.target.value)}
                                placeholder="https://exam-portal-backend.onrender.com"
                                className="w-full px-3 py-1.5 rounded text-xs bg-white text-gray-900 border"
                            />
                            <div className="flex gap-2">
                                <button
                                    type="button"
                                    onClick={saveBackendUrl}
                                    className="bg-indigo-600 hover:bg-indigo-700 text-white text-xs px-3 py-1 rounded font-bold"
                                >
                                    Save & Apply
                                </button>
                                <button
                                    type="button"
                                    onClick={() => {
                                        localStorage.removeItem('API_URL');
                                        setBackendUrl(getBaseApiUrl());
                                        setError('');
                                    }}
                                    className="bg-gray-600 hover:bg-gray-700 text-white text-xs px-2 py-1 rounded"
                                >
                                    Reset Default
                                </button>
                            </div>
                        </div>
                    )}
                </form>
            </motion.div>
        </div>
    );
}
