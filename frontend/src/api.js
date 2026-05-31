const DEFAULT_API_BASE = process.env.REACT_APP_API_BASE_URL || '';

export const apiUrl = (path) => {
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  const base = DEFAULT_API_BASE.replace(/\/$/, '');

  if (!base) {
    return normalizedPath;
  }

  return `${base}${normalizedPath}`;
};