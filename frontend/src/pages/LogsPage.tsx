import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { apiClient, LogRecord } from '../api/client';
import { SearchFilter } from '../components/SearchFilter';
import { LogTable } from '../components/LogTable';
import { Pagination } from '../components/Pagination';

export const LogsPage = () => {
  const navigate = useNavigate();
  const { username, logout, isAuthenticated } = useAuth();
  const [logs, setLogs] = useState<LogRecord[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [total, setTotal] = useState(0);
  const [isReloading, setIsReloading] = useState(false);
  
  const [filters, setFilters] = useState({
    username: '',
    ip: '',
    status: '',
    fromTime: '',
    toTime: '',
    sortBy: 'login_time',
    sortOrder: 'DESC',
  });
  const [debouncedFilters, setDebouncedFilters] = useState(filters);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedFilters(filters);
    }, 500);

    return () => clearTimeout(timer);
  }, [filters]);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    
    fetchLogs(debouncedFilters);
  }, [isAuthenticated, page, pageSize, debouncedFilters]);

  const fetchLogs = async (activeFilters: typeof filters) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await apiClient.getLogs(page, pageSize, {
        username: activeFilters.username || undefined,
        ip: activeFilters.ip || undefined,
        status: activeFilters.status || undefined,
        from_time: activeFilters.fromTime || undefined,
        to_time: activeFilters.toTime || undefined,
        sort_by: activeFilters.sortBy,
        sort_order: activeFilters.sortOrder,
      });
      
      setLogs(response.data);
      setTotal(response.total);
    } catch (err: any) {
      setError(err.message || 'Failed to load logs');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFilterChange = (newFilters: typeof filters) => {
    setFilters(newFilters);
    setPage(1);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleHotReload = async () => {
    setIsReloading(true);
    setError(null);

    try {
      await apiClient.reloadLogs();
      await fetchLogs(filters);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to hot reload logs');
    } finally {
      setIsReloading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-100">
      <header className="sticky top-0 z-20 border-b border-slate-200 bg-white/90 backdrop-blur">
        <div className="mx-auto flex w-full max-w-7xl items-center justify-between px-4 py-4 sm:px-6">
          <h1 className="text-xl font-bold tracking-tight text-slate-900 sm:text-2xl">SSH Auth Log Monitor</h1>
          <div className="flex items-center gap-3 sm:gap-4">
            <span className="hidden text-sm text-slate-600 sm:inline">Welcome, {username}!</span>
            <button
              onClick={handleLogout}
              className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
            >
            Logout
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto w-full max-w-7xl space-y-5 px-4 py-6 sm:px-6">
        <div className="flex flex-wrap items-center justify-end gap-3">
          <button
            onClick={handleHotReload}
            disabled={isReloading || isLoading}
            className="rounded-lg bg-cyan-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-cyan-700 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isReloading ? 'Reloading...' : 'Hot Reload Logs'}
          </button>
        </div>

        <SearchFilter 
          filters={filters}
          onFilterChange={handleFilterChange}
          isLoading={isLoading}
        />

        {error && <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>}

        {isLoading ? (
          <div className="rounded-lg border border-slate-200 bg-white px-4 py-12 text-center text-sm text-slate-500">Loading logs...</div>
        ) : (
          <>
            <LogTable logs={logs} />
            
            {logs.length === 0 && !isLoading && (
              <div className="rounded-lg border border-slate-200 bg-white px-4 py-8 text-center text-sm text-slate-500">No logs found</div>
            )}
            
            <Pagination
              page={page}
              pageSize={pageSize}
              total={total}
              onPageChange={setPage}
              onPageSizeChange={(size) => {
                setPageSize(size);
                setPage(1);
              }}
            />
          </>
        )}
      </main>
    </div>
  );
};
