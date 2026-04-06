export const getToken = (): string | null => {
  return localStorage.getItem('access_token');
};

export const setToken = (token: string): void => {
  localStorage.setItem('access_token', token);
};

export const clearToken = (): void => {
  localStorage.removeItem('access_token');
};

export const setUser = (username: string): void => {
  localStorage.setItem('username', username);
};

export const getUser = (): string | null => {
  return localStorage.getItem('username');
};

export const clearUser = (): void => {
  localStorage.removeItem('username');
};

export const clearAll = (): void => {
  localStorage.clear();
};
