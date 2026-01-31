"use client";
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { uploadDataset, getDatasets, toggleDataset, deleteStudents, openFacultyExcel, syncFacultyExcel } from '../../api';
import { motion } from 'framer-motion';

// AdminDashboard Component
// Allows administrators to manage hall seating, allocations, and faculty data.
// Features Google Sheet integration for opening and syncing faculty records.
export default function AdminDashboard() {
    const [datasets, setDatasets] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const [msg, setMsg] = useState('');
    const router = useRouter();

    useEffect(() => {
        const role = localStorage.getItem('role');
        if (role !== 'admin') router.push('/');
        fetchDatasets();
    }, []);

    const fetchDatasets = async () => {
        try {
            const res = await getDatasets();
            setDatasets(res.data);
        } catch (e) { console.error(e); }
    };

    const handleUpload = async (e: any) => {
        const file = e.target.files[0];
        if (!file) return;
        setLoading(true);
        setMsg('Uploading...');
        try {
            await uploadDataset(file);
            setMsg('');
            alert('Hall seating is uploaded');
            fetchDatasets();
        } catch (err: any) {
            setMsg('');
            alert(err.response?.data?.error || 'Upload failed');
        } finally {
            setLoading(false);
        }
    };

    const handleToggle = async (id: number) => {
        await toggleDataset(id);
        fetchDatasets();
    };

    const handleRefresh = async () => {
        if (confirm('Are you sure you want to delete all previous allocations?')) {
            setLoading(true);
            setMsg('Deleting...');
            try {
                await deleteStudents();
                setMsg('');
                alert('The previous allocation is deleted. Now you can upload the new hall seating.');
                fetchDatasets();
            } catch (err: any) {
                setMsg('');
                alert('Delete failed');
            } finally {
                setLoading(false);
            }
        }
    };

    const handleOpenExcel = async () => {
        setLoading(true);
        setMsg('Opening Google Sheet...');
        try {
            const res = await openFacultyExcel();
            setMsg('');
            if (res.data.url) {
                window.open(res.data.url, '_blank');
            } else {
                alert('No URL returned');
            }
        } catch (err: any) {
            setMsg('');
            alert('Failed to open Excel: ' + (err.response?.data?.error || err.message));
        } finally {
            setLoading(false);
        }
    };

    const handleSyncExcel = async () => {
        setLoading(true);
        setMsg('Syncing Database...');
        try {
            const res = await syncFacultyExcel();
            setMsg('');
            const stats = res.data.stats;
            alert(`Sync Complete!\nCreated: ${stats.created}\nUpdated: ${stats.updated}\nDeleted: ${stats.deleted}`);
        } catch (err: any) {
            setMsg('');
            alert('Sync failed: ' + (err.response?.data?.error || err.message));
        } finally {
            setLoading(false);
        }
    };

    // Assuming we just show the LATEST dataset status for the "Main Control" feel
    const latestDataset = datasets.length > 0 ? datasets[0] : null;

    const handleLogout = () => {
        localStorage.clear();
        router.push('/');
    };

    return (
        <div className="min-h-screen bg-gray-100 flex flex-col">
            {/* Navbar */}
            <div className="bg-gray-900 text-white px-6 py-4 flex justify-between items-center shadow-md">
                <h1 className="text-xl font-bold tracking-wider">EXAM MANAGEMENT SYSTEM</h1>
                <div className="flex items-center gap-4">
                    <span className="bg-gray-700 px-3 py-1 rounded text-sm font-medium">End Semester Exam</span>
                    <button onClick={handleLogout} className="bg-red-500 hover:bg-red-600 px-4 py-1 rounded text-sm font-bold transition shadow-lg">Logout</button>
                </div>
            </div>

            {/* Main Content */}
            <div className="flex-1 flex items-center justify-center p-6">
                <motion.div
                    initial={{ scale: 0.9, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="bg-white rounded-3xl shadow-2xl p-10 w-full max-w-lg text-center border border-gray-200"
                >
                    <h2 className="text-2xl font-bold text-gray-800 mb-8">Admin Controls</h2>

                    {/* Status Indicator */}
                    <div className="bg-gray-50 rounded-lg p-4 mb-8 flex items-center justify-between border border-gray-200">
                        <span className="text-gray-600 font-semibold">Dataset Status:</span>
                        <div className="flex items-center gap-2">
                            {latestDataset?.is_active ? (
                                <span className="text-green-600 font-bold">ACTIVE ✓</span>
                            ) : (
                                <span className="text-red-500 font-bold">INACTIVE X</span>
                            )}
                            {latestDataset && (
                                <button
                                    onClick={() => handleToggle(latestDataset.id)}
                                    className={`px-4 py-1 rounded text-white text-sm font-bold transition ${latestDataset.is_active ? 'bg-red-500 hover:bg-red-600' : 'bg-green-500 hover:bg-green-600 shadow-md'}`}
                                >
                                    Toggle
                                </button>
                            )}
                        </div>
                    </div>

                    {/* Actions */}
                    <div className="space-y-4">
                        <label className="block w-full cursor-pointer group">
                            <div className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 rounded-lg shadow-lg flex items-center justify-center gap-2 transition transform group-hover:-translate-y-1">
                                <span>📤 Upload Seating Plan</span>
                            </div>
                            <input type="file" className="hidden" onChange={handleUpload} accept=".xls,.xlsx" />
                        </label>
                        {loading && <p className="text-sm text-blue-600 animate-pulse font-medium">{msg}</p>}

                        <button onClick={handleRefresh} className="w-full bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 rounded-lg shadow-lg flex items-center justify-center gap-2 transition transform hover:-translate-y-1">
                            <span>🔄 Refresh Seating Plans</span>
                        </button>

                        <button onClick={() => router.push('/admin/faculty-allocation')} className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 rounded-lg shadow-lg flex items-center justify-center gap-2 transition transform hover:-translate-y-1">
                            <span>👨‍🏫 Faculty Allocation</span>
                        </button>

                        <div className="grid grid-cols-2 gap-3">
                            <button onClick={handleOpenExcel} className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3 rounded-lg shadow-lg flex items-center justify-center gap-2 transition transform hover:-translate-y-1">
                                <span>📂 FACULTY DATA</span>
                            </button>
                            <button onClick={handleSyncExcel} className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg shadow-lg flex items-center justify-center gap-2 transition transform hover:-translate-y-1">
                                <span>🔄 Sync from Sheet</span>
                            </button>
                        </div>

                        <button onClick={() => router.push('/admin/faculty-requests')} className="w-full bg-cyan-600 hover:bg-cyan-700 text-white font-bold py-3 rounded-lg shadow-lg flex items-center justify-center gap-2 transition transform hover:-translate-y-1">
                            <span>🔄 Alternation Requests</span>
                        </button>
                    </div>
                </motion.div>
            </div>
        </div>
    );
}
