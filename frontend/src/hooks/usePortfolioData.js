import { useState, useEffect } from 'react';
import { portfolioAPI } from '../services/api';

export const usePortfolioData = () => {
  const [data, setData] = useState({
    profile: null,
    skills: null,
    projects: [],
    certificates: [],
    education: [],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAllData = async () => {
      setLoading(true);
      setError(null);

      try {
        const [profile, skills, projects, certificates, education] = await Promise.all([
          portfolioAPI.getProfile().catch(err => {
            console.warn('Profile fetch failed:', err);
            return null;
          }),
          portfolioAPI.getSkills().catch(err => {
            console.warn('Skills fetch failed:', err);
            return null;
          }),
          portfolioAPI.getProjects().catch(err => {
            console.warn('Projects fetch failed:', err);
            return [];
          }),
          portfolioAPI.getCertificates().catch(err => {
            console.warn('Certificates fetch failed:', err);
            return [];
          }),
          portfolioAPI.getEducation().catch(err => {
            console.warn('Education fetch failed:', err);
            return [];
          }),
        ]);

        setData({
          profile,
          skills,
          projects,
          certificates,
          education,
        });
      } catch (err) {
        console.error('Failed to fetch portfolio data:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAllData();
  }, []);

  const refreshData = async () => {
    setLoading(true);
    try {
      const [profile, skills, projects, certificates, education] = await Promise.all([
        portfolioAPI.getProfile(),
        portfolioAPI.getSkills(),
        portfolioAPI.getProjects(),
        portfolioAPI.getCertificates(),
        portfolioAPI.getEducation(),
      ]);

      setData({
        profile,
        skills,
        projects,
        certificates,
        education,
      });
      setError(null);
    } catch (err) {
      console.error('Failed to refresh portfolio data:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return {
    data,
    loading,
    error,
    refreshData,
  };
};