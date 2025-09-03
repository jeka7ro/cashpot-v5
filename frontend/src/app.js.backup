import React, { createContext, useContext, useEffect, useMemo, useState, useCallback } from 'react';
import * as XLSX from 'xlsx';
import './app.css';



const BACKEND_URL = 'http://localhost:8002';
const API = `${BACKEND_URL}/api`;

// Module-level cache to survive component remounts
let __historyDataCache__ = null;
let __historyFiltersCache__ = null;

// Helper function to format dates as dd.mm.yyyy
const formatDateDDMMYYYY = (date) => {
  if (!date) return '';
  const d = new Date(date);
  const day = String(d.getDate()).padStart(2, '0');
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const year = d.getFullYear();
  return `${day}.${month}.${year}`;
};

// Calendar Component
const Calendar = ({ value, onChange, placeholder = "Select date", allowManualInput = false }) => {
  const [showCalendar, setShowCalendar] = useState(false);
  const [currentDate, setCurrentDate] = useState(new Date());

  // Fix: Use local date formatting to avoid timezone issues
  const formatDate = (date) => {
    if (!date) return '';
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  const formatDisplayDate = (date) => {
    if (!date) return placeholder;
    if (typeof date === 'string') {
      // If already dd.mm.yyyy, return as is
      if (/^\d{2}\.\d{2}\.\d{4}$/.test(date)) return date;
      // If yyyy-mm-dd, convert to dd.mm.yyyy
      if (/^\d{4}-\d{2}-\d{2}$/.test(date)) {
        const [y, m, d] = date.split('-');
        return `${d}.${m}.${y}`;
      }
    }
    const d = new Date(date);
    if (Number.isNaN(d.getTime())) return placeholder;
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    return `${day}.${month}.${year}`;
  };

  const parseManual = (text) => {
    const m = text.match(/^(\d{1,2})\.(\d{1,2})\.(\d{4})$/);
    if (!m) return null;
    const day = parseInt(m[1], 10);
    const monthIndex = parseInt(m[2], 10) - 1;
    const year = parseInt(m[3], 10);
    const dt = new Date(year, monthIndex, day);
    return Number.isNaN(dt.getTime()) ? null : dt;
  };

  const getDaysInMonth = (date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const startDate = new Date(firstDay);
    startDate.setDate(startDate.getDate() - firstDay.getDay());
    
    const days = [];
    const current = new Date(startDate);
    
    for (let i = 0; i < 42; i++) {
      days.push(new Date(current));
      current.setDate(current.getDate() + 1);
    }
    
    return days;
  };

  const handleDateClick = (date) => {
    const formattedDate = formatDate(date);
    onChange(formattedDate);
    setShowCalendar(false);
  };

  // English month names
  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];
  // English day names
  const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  const days = getDaysInMonth(currentDate);
  const selectedDateObj = value ? new Date(value) : null;

  return (
    <div className="calendar-container">
      <div
        className="calendar-input"
        onClick={(e) => {
          // Toggle only when clicking the icon area; let input focus without toggling
          const target = e.target;
          if (target && target.classList && target.classList.contains('calendar-icon')) {
            setShowCalendar((s) => !s);
          }
        }}
      >
        {allowManualInput ? (
          <input
            type="text"
            placeholder={placeholder}
            value={value ? formatDisplayDate(value) : ''}
            onChange={(e) => {
              const dt = parseManual(e.target.value);
              if (dt) {
                onChange(formatDate(dt));
                setCurrentDate(dt);
              } else if (e.target.value.trim() === '') {
                onChange('');
              }
            }}
            onClick={(e) => e.stopPropagation()}
            onFocus={(e) => e.stopPropagation()}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--text-primary)'
            }}
            inputMode="numeric"
            pattern="\\d{2}\\.\\d{2}\\.\\d{4}"
          />
        ) : (
          <span className="calendar-value">{formatDisplayDate(value)}</span>
        )}
        <span className="calendar-icon" onClick={() => setShowCalendar((s) => !s)}>📅</span>
      </div>
      
      {showCalendar && (
        <div className="calendar-popup">
          <div className="calendar-header">
            <button 
              type="button"
              onClick={() => setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1))}
              className="calendar-nav"
            >
              ‹
            </button>
            <span className="calendar-month">
              {monthNames[currentDate.getMonth()]} {currentDate.getFullYear()}
            </span>
            <button 
              type="button"
              onClick={() => setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1))}
              className="calendar-nav"
            >
              ›
            </button>
          </div>
          
          <div className="calendar-grid">
            <div className="calendar-weekdays">
              {dayNames.map(day => (
                <div key={day} className="calendar-weekday">{day}</div>
              ))}
            </div>
            
            <div className="calendar-days">
              {days.map((day, index) => {
                const isCurrentMonth = day.getMonth() === currentDate.getMonth();
                const isSelected = selectedDateObj && 
                  day.getDate() === selectedDateObj.getDate() &&
                  day.getMonth() === selectedDateObj.getMonth() &&
                  day.getFullYear() === selectedDateObj.getFullYear();
                const isToday = day.toDateString() === new Date().toDateString();
                
                return (
                  <button
                    key={index}
                    type="button"
                    className={`calendar-day ${!isCurrentMonth ? 'other-month' : ''} ${isSelected ? 'selected' : ''} ${isToday ? 'today' : ''}`}
                    onClick={() => handleDateClick(day)}
                  >
                    {day.getDate()}
                  </button>
                );
              })}
            </div>
          </div>
          
          <div className="calendar-footer">
            <button 
              type="button"
              onClick={() => handleDateClick(new Date())}
              className="calendar-today-btn"
            >
              Today
            </button>
            <button 
              type="button"
              onClick={() => {
                onChange('');
                setShowCalendar(false);
              }}
              className="calendar-clear-btn"
              style={{ 
                backgroundColor: 'var(--danger-color)', 
                color: 'white',
                border: 'none',
                padding: '8px 12px',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '12px'
              }}
            >
              Clear
            </button>
            <button 
              type="button"
              onClick={() => setShowCalendar(false)}
              className="calendar-close-btn"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

// Auth Context
const AuthContext = createContext();

// Avatar Upload Component
const AvatarUpload = ({ entityType, entityId, currentAvatar, onAvatarChange, showCustomNotification }) => {
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const { user } = useAuth();

  const handleFileUpload = async (file) => {
    if (!file || !file.type.startsWith('image/')) {
      showCustomNotification('Please select a valid image file', 'error');
      return;
    }

    if (file.size > 5 * 1024 * 1024) { // 5MB limit
      showCustomNotification('File size must be less than 5MB', 'error');
      return;
    }

    setUploading(true);
    try {
      console.log('Starting avatar upload for:', { entityType, entityId, file: file.name });
      
      // Convert file to base64
      const base64 = await new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = () => {
          let base64Data = reader.result.split(',')[1];
          // Add padding if needed
          while (base64Data.length % 4) {
            base64Data += '=';
          }
          resolve(base64Data);
        };
        reader.readAsDataURL(file);
      });

      const uploadData = {
        filename: `avatar_${Date.now()}.${file.name.split('.').pop()}`,
        original_filename: file.name,
        file_size: file.size,
        mime_type: file.type,
        file_data: base64,
        entity_type: entityType,
        entity_id: entityId
      };

      console.log('Uploading to:', `${API}/attachments`);
      console.log('Upload data:', { ...uploadData, file_data: 'base64_data' });

      // Upload to backend
      const response = await fetch(`${API}/attachments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(uploadData)
      });

      console.log('Response status:', response.status);
      console.log('Response headers:', response.headers);

      if (response.ok) {
        const attachment = await response.json();
        console.log('Upload successful:', attachment);
        onAvatarChange(attachment);
        showCustomNotification('Avatar uploaded successfully', 'success');
      } else {
        const errorText = await response.text();
        console.error('Upload failed with status:', response.status);
        console.error('Error response:', errorText);
        throw new Error(`Upload failed: ${response.status} - ${errorText}`);
      }
    } catch (error) {
      console.error('Upload error:', error);
      showCustomNotification(`Failed to upload avatar: ${error.message}`, 'error');
    } finally {
      setUploading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFileUpload(file);
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) handleFileUpload(file);
  };

  useEffect(() => {
    if(entityType === 'game_mixes') {
      console.log('AVATAR UPLOAD GAME MIX:', {entityType, entityId, currentAvatar});
    }
  }, [entityType, entityId, currentAvatar]);

  return (
    <div className="avatar-upload-container">
      <div
        className={`avatar-upload ${dragOver ? 'drag-over' : ''}`}
        onDrop={handleDrop}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onClick={() => document.getElementById(`avatar-input-${entityId}`)?.click()}
      >
        {currentAvatar ? (
          <img
            src={`data:${currentAvatar.mime_type};base64,${currentAvatar.file_data}`}
            alt="Avatar"
            className="avatar-preview"
          />
        ) : (
          <div className="avatar-placeholder">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
            </svg>
            <span>Click or drag to upload avatar</span>
          </div>
        )}
        {uploading && (
          <div className="upload-overlay">
            <div className="spinner"></div>
          </div>
        )}
      </div>
      <input
        type="file"
        id={`avatar-input-${entityId}`}
        accept="image/*"
        style={{ display: 'none' }}
        onChange={handleFileSelect}
      />
    </div>
  );
};

// File Upload Component for PDF and other documents
const FileUpload = ({ entityType, entityId, onFileUpload, acceptedTypes = ['application/pdf', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'image/png', 'image/jpeg'], maxSizeMB = 50, showCustomNotification }) => {
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const { user } = useAuth();

  const handleFileUpload = async (file) => {
    // Validate file type
    if (!acceptedTypes.includes(file.type)) {
      showCustomNotification(`Please select a valid file type. Accepted types: ${acceptedTypes.join(', ')}`, 'error');
      return;
    }

    // Validate file size
    if (file.size > maxSizeMB * 1024 * 1024) {
      showCustomNotification(`File size must be less than ${maxSizeMB}MB`, 'error');
      return;
    }

    setUploading(true);
    try {
      // Convert file to base64
      const base64 = await new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
          const result = reader.result;
          // Extract base64 data from data URL
          const base64Data = result.split(',')[1];
          if (!base64Data) {
            reject(new Error('Failed to convert file to base64'));
            return;
          }
          resolve(base64Data);
        };
        reader.onerror = () => reject(new Error('Failed to read file'));
        reader.readAsDataURL(file);
      });

      // Upload to backend
      const response = await fetch(`${API}/attachments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          filename: `document_${Date.now()}.${file.name.split('.').pop()}`,
          original_filename: file.name,
          file_size: file.size,
          mime_type: file.type,
          file_data: base64,
          entity_type: entityType,
          entity_id: entityId
        })
      });

      if (response.ok) {
        const attachment = await response.json();
        onFileUpload(attachment);
        showCustomNotification('File uploaded successfully!', 'success');
      } else {
        throw new Error('Upload failed');
      }
    } catch (error) {
      console.error('Upload error:', error);
      showCustomNotification('Failed to upload file', 'error');
    } finally {
      setUploading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFileUpload(file);
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) handleFileUpload(file);
  };

  return (
    <div style={{
      display: 'inline-block',
      position: 'relative'
    }}>
      <button
        onClick={() => document.getElementById(`file-input-${entityId}`)?.click()}
        onDrop={handleDrop}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '4px',
          padding: '4px 8px',
          backgroundColor: dragOver ? 'var(--accent-color)' : 'var(--background-secondary)',
          color: dragOver ? 'white' : 'var(--text-primary)',
          border: `1px dashed ${dragOver ? 'var(--accent-color)' : '#ddd'}`,
          borderRadius: '4px',
          cursor: 'pointer',
          fontSize: '11px',
          fontWeight: '500',
          transition: 'all 0.2s ease',
          minWidth: '60px',
          justifyContent: 'center'
        }}
        title="Click to upload or drag files here"
      >
        <span style={{ fontSize: '12px' }}>📎</span>
        <span>Upload</span>
        {uploading && (
          <span style={{ 
            fontSize: '10px', 
            marginLeft: '2px',
            animation: 'pulse 1s infinite'
          }}>
            ...
          </span>
        )}
      </button>
      <input
        id={`file-input-${entityId}`}
        type="file"
        accept={acceptedTypes.join(',')}
        onChange={handleFileSelect}
        style={{ display: 'none' }}
      />
    </div>
  );
};

// Custom hook for fetching files
const useFiles = (entityType, entityId) => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchFiles = async () => {
    if (!entityType || !entityId) return;
    setLoading(true);
    try {
      const url = `${API}/attachments/${entityType}/${entityId}`;
      const response = await fetch(url, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      if (response.ok) {
        const attachments = await response.json();
        // Filter out avatar files, keep only documents
        const documentAttachments = attachments.filter(att => 
          !att.mime_type.startsWith('image/') || 
          (!att.filename.includes('avatar') && !att.filename.includes('custom_avatar'))
        );
        setFiles(documentAttachments);
      }
    } catch (error) {
      console.error('Error fetching files:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFiles();
  }, [entityType, entityId]);

  return { files, setFiles, loading, refetch: fetchFiles };
};
// File Display Component
const FileDisplay = ({ entityType, entityId, onFileDelete, showCustomNotification }) => {
  const { files, loading, refetch } = useFiles(entityType, entityId);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [fileToDelete, setFileToDelete] = useState(null);

  const handleDownload = async (attachment) => {
    try {
      const response = await fetch(`${API}/attachments/${attachment.id}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      
      if (response.ok) {
        const data = await response.json();
        
        // Convert base64 to blob
        const byteCharacters = atob(data.file_data);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
          byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], { type: data.mime_type });
        
        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = data.filename || attachment.original_filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
    } catch (error) {
      console.error('Download error:', error);
              showCustomNotification('Failed to download file: ' + error.message, 'error');
    }
  };

  const handlePreview = async (attachment) => {
    try {
      const response = await fetch(`${API}/attachments/${attachment.id}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      
      if (response.ok) {
        const data = await response.json();
        
        // Convert base64 to blob with error handling
        try {
          // Clean the base64 data (remove any whitespace or invalid characters)
          const cleanBase64 = data.file_data.replace(/[\n\r\s]/g, '');
          
          const byteCharacters = atob(cleanBase64);
          const byteNumbers = new Array(byteCharacters.length);
          for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
          }
          const byteArray = new Uint8Array(byteNumbers);
          const blob = new Blob([byteArray], { type: data.mime_type });
          
          // Create preview URL
          const url = window.URL.createObjectURL(blob);
          
          // For PDFs, try to open in new tab
          if (data.mime_type === 'application/pdf') {
            const newWindow = window.open(url, '_blank');
            if (!newWindow) {
              // If popup blocked, try to download instead
              const link = document.createElement('a');
              link.href = url;
              link.download = data.original_filename || 'document.pdf';
              link.click();
            }
          } else {
            // For other files, open in new tab
            window.open(url, '_blank');
          }
          
          // Clean up URL after a delay
          setTimeout(() => window.URL.revokeObjectURL(url), 5000);
        } catch (base64Error) {
          console.error('Base64 conversion error:', base64Error);
          throw new Error('Failed to convert file data for preview');
        }
      } else {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
    } catch (error) {
      console.error('Preview error:', error);
              showCustomNotification('Failed to preview file: ' + error.message, 'error');
    }
  };

  const handleDelete = async (attachment) => {
    setFileToDelete(attachment);
    setShowDeleteConfirm(true);
  };

  const confirmDelete = async () => {
    if (!fileToDelete) return;
    
    try {
      const response = await fetch(`${API}/attachments/${fileToDelete.id}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      
      if (response.ok) {
        refetch();
        if (onFileDelete) onFileDelete(attachment);
      } else {
        throw new Error('Delete failed');
      }
      
      // Clean up and close modal
      setShowDeleteConfirm(false);
      setFileToDelete(null);
      refetch();
      
      if (onFileDelete) {
        onFileDelete();
      }
    } catch (error) {
      console.error('Delete error:', error);
              showCustomNotification('Failed to delete file', 'error');
      setShowDeleteConfirm(false);
      setFileToDelete(null);
    }
  };

  const cancelDelete = () => {
    setShowDeleteConfirm(false);
    setFileToDelete(null);
  };

  const getFileIcon = (mimeType) => {
    if (mimeType === 'application/pdf') return '📄';
    if (mimeType.includes('excel') || mimeType.includes('spreadsheet')) return '📊';
    if (mimeType.startsWith('image/')) return '🖼️';
    return '📎';
  };



  if (loading) {
    return <div className="file-display-loading">Loading files...</div>;
  }

  if (files.length === 0) {
    return (
      <div style={{ 
        textAlign: 'center', 
        padding: '8px',
        color: 'var(--text-primary)',
        fontSize: '13px'
      }}>
        <p style={{ marginBottom: '8px' }}>No files attached</p>
        <FileUpload
          entityType={entityType}
          entityId={entityId}
          onFileUpload={() => refetch()}
          showCustomNotification={showCustomNotification}
        />
      </div>
    );
  }

  return (
    <div style={{ padding: '8px' }}>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center', 
        marginBottom: '8px',
        fontSize: '13px',
        fontWeight: '500',
        color: 'var(--text-primary)'
      }}>
        <span>Files ({files.length})</span>
      </div>
      <div style={{ 
        display: 'flex', 
        flexDirection: 'column', 
        gap: '4px',
        maxHeight: '150px',
        overflowY: 'auto'
      }}>
        {files.map((file) => (
          <div key={file.id} style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '6px 8px',
            backgroundColor: 'var(--background-secondary)',
            borderRadius: '4px',
            fontSize: '12px',
            border: '1px solid #eee'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', flex: 1 }}>
              <span style={{ fontSize: '14px' }}>{getFileIcon(file.mime_type)}</span>
              <span style={{ 
                fontWeight: '500', 
                color: 'var(--text-primary)',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap',
                maxWidth: '180px'
              }}>
                {file.original_filename}
              </span>
              <span style={{ 
                color: 'var(--text-secondary)', 
                fontSize: '10px',
                whiteSpace: 'nowrap'
              }}>
                ({(file.file_size / 1024 / 1024).toFixed(1)} MB)
              </span>
            </div>
            <div style={{ display: 'flex', gap: '2px' }}>
              <button 
                onClick={() => handlePreview(file)}
                title="Preview"
                style={{
                  padding: '2px 4px',
                  border: 'none',
                  background: 'transparent',
                  cursor: 'pointer',
                  borderRadius: '3px',
                  fontSize: '11px'
                }}
              >
                👁️
              </button>
              <button 
                onClick={() => handleDownload(file)}
                title="Download"
                style={{
                  padding: '2px 4px',
                  border: 'none',
                  background: 'transparent',
                  cursor: 'pointer',
                  borderRadius: '3px',
                  fontSize: '11px'
                }}
              >
                ⬇️
              </button>
              <button 
                onClick={() => handleDelete(file)}
                title="Delete"
                style={{
                  padding: '2px 4px',
                  border: 'none',
                  background: 'transparent',
                  cursor: 'pointer',
                  borderRadius: '3px',
                  fontSize: '11px',
                  color: '#e74c3c'
                }}
              >
                🗑️
              </button>
            </div>
          </div>
        ))}
      </div>
      
      {/* Custom Delete Confirmation Modal */}
      {showDeleteConfirm && fileToDelete && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.6)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 9999,
          fontFamily: 'var(--font-family)'
        }}>
          <div style={{
            backgroundColor: 'var(--bg-secondary)',
            borderRadius: '12px',
            padding: '24px',
            maxWidth: '450px',
            width: '90%',
            boxShadow: 'var(--glass-shadow)',
            border: '1px solid var(--border-color)',
            position: 'relative',
            backdropFilter: 'var(--glass-blur)'
          }}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              marginBottom: '20px'
            }}>
              <span style={{
                fontSize: '28px',
                color: '#ff4757'
              }}>⚠️</span>
              <h3 style={{
                margin: 0,
                color: 'var(--text-primary)',
                fontSize: '20px',
                fontWeight: '600',
                fontFamily: 'var(--font-family)'
              }}>
                Delete Confirmation
              </h3>
            </div>
            
            <p style={{
              margin: '0 0 24px 0',
              color: 'var(--text-secondary)',
              fontSize: '15px',
              lineHeight: '1.6',
              fontFamily: 'var(--font-family)'
            }}>
              Are you sure you want to delete the file <strong style={{color: 'var(--text-primary)'}}>"{fileToDelete.original_filename}"</strong>?
              <br />
              <span style={{color: '#ff4757', fontSize: '13px'}}>This action cannot be undone.</span>
            </p>
            
            <div style={{
              display: 'flex',
              gap: '12px',
              justifyContent: 'flex-end'
            }}>
              <button
                onClick={cancelDelete}
                style={{
                  padding: '10px 20px',
                  border: '2px solid var(--border-color)',
                  borderRadius: '8px',
                  backgroundColor: 'transparent',
                  color: 'var(--text-secondary)',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: '500',
                  transition: 'all 0.2s ease',
                  fontFamily: 'var(--font-family)'
                }}
                onMouseOver={(e) => {
                  e.target.style.backgroundColor = 'var(--bg-tertiary)';
                  e.target.style.borderColor = 'var(--accent-color)';
                }}
                onMouseOut={(e) => {
                  e.target.style.backgroundColor = 'transparent';
                  e.target.style.borderColor = 'var(--border-color)';
                }}
              >
                Cancel
              </button>
              <button
                onClick={confirmDelete}
                style={{
                  padding: '10px 20px',
                  border: 'none',
                  borderRadius: '8px',
                  background: 'var(--gradient-danger)',
                  color: 'white',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: '500',
                  transition: 'all 0.2s ease',
                  fontFamily: 'var(--font-family)'
                }}
                onMouseOver={(e) => {
                  e.target.style.transform = 'translateY(-1px)';
                  e.target.style.boxShadow = '0 4px 12px rgba(255, 71, 87, 0.4)';
                }}
                onMouseOut={(e) => {
                  e.target.style.transform = 'translateY(0)';
                  e.target.style.boxShadow = 'none';
                }}
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};



// Component for displaying slot attachments count
const AttachmentIndicator = ({ slotId, onClick }) => {
  const [attachmentCount, setAttachmentCount] = useState(0);
  const [loading, setLoading] = useState(false);

  const fetchAttachmentCount = async () => {
    if (!slotId) return;
    setLoading(true);
    try {
      const response = await fetch(`${API}/attachments/slots/${slotId}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      if (response.ok) {
        const data = await response.json();
        console.log('Fetched attachments for slot', slotId, ':', data);
        // Filtrează doar documentele (nu avatarurile)
        const documentAttachments = data.filter(att => 
          !att.mime_type.startsWith('image/') || 
          (!att.filename.includes('avatar') && !att.filename.includes('custom_avatar'))
        );
        console.log('Document attachments for slot', slotId, ':', documentAttachments);
        setAttachmentCount(documentAttachments.length);
      } else {
        console.error('Failed to fetch attachments for slot', slotId, ':', response.status);
      }
    } catch (error) {
      console.error('Error fetching slot attachments:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAttachmentCount();
  }, [slotId]);

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '0px' }}>
      <button 
        className="btn-attachment"
        title="View Slot Attachments"
        onClick={onClick}
        style={{ 
          fontSize: '14px', 
          padding: '2px 4px',
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          width: '32px',
          height: '32px',
          cursor: 'pointer',
          border: 'none',
          backgroundColor: '#d1e7ff',
          borderRadius: '50%',
          color: '#1e3a8a',
          marginRight: '0px'
        }}
      >
        📎
      </button>
      {attachmentCount > 0 && (
        <div style={{
          backgroundColor: '#3182ce',
          color: 'white',
          borderRadius: '50%',
          width: '18px',
          height: '18px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '11px',
          fontWeight: 'bold',
          minWidth: '18px',
          marginLeft: '-2px'
        }}>
          {attachmentCount}
        </div>
      )}
    </div>
  );
};

// Component for displaying generic entity attachments count
const GenericAttachmentIndicator = ({ entityType, entityId, onClick }) => {
  const [attachmentCount, setAttachmentCount] = useState(0);
  const [loading, setLoading] = useState(false);

  const fetchAttachmentCount = async () => {
    if (!entityId || !entityType) return;
    setLoading(true);
    try {
      const response = await fetch(`${API}/attachments/${entityType}/${entityId}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      if (response.ok) {
        const data = await response.json();
        console.log('Fetched attachments for', entityType, entityId, ':', data);
        // Filtrează doar documentele (nu avatarurile)
        const documentAttachments = data.filter(att => 
          !att.mime_type.startsWith('image/') || 
          (!att.filename.includes('avatar') && !att.filename.includes('custom_avatar'))
        );
        console.log('Document attachments for', entityType, entityId, ':', documentAttachments);
        setAttachmentCount(documentAttachments.length);
      } else {
        console.error('Failed to fetch attachments for', entityType, entityId, ':', response.status);
      }
    } catch (error) {
      console.error('Error fetching attachments:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAttachmentCount();
  }, [entityId, entityType]);

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '0px' }}>
      <button 
        className="btn-attachment"
        title={`View ${entityType} Attachments`}
        onClick={(e) => {
          console.log('🔗 GenericAttachmentIndicator clicked:', { entityType, entityId });
          e.preventDefault();
          e.stopPropagation();
          onClick();
        }}
        style={{ 
          fontSize: '14px', 
          padding: '2px 4px',
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          width: '32px',
          height: '32px',
          cursor: 'pointer',
          border: 'none',
          backgroundColor: '#d1e7ff',
          borderRadius: '50%',
          color: '#1e3a8a',
          marginRight: '0px'
        }}
      >
        📎
      </button>
      {attachmentCount > 0 && (
        <div style={{
          backgroundColor: '#3182ce',
          color: 'white',
          borderRadius: '50%',
          width: '18px',
          height: '18px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '11px',
          fontWeight: 'bold',
          minWidth: '18px',
          marginLeft: '-2px'
        }}>
          {attachmentCount}
        </div>
      )}
    </div>
  );
};

// Component for displaying CVT attachments count
const CvtAttachmentIndicator = ({ cvtId, onClick }) => {
  const [attachmentCount, setAttachmentCount] = useState(0);
  const [loading, setLoading] = useState(false);

  const fetchAttachmentCount = async () => {
    if (!cvtId) return;
    setLoading(true);
    try {
      const response = await fetch(`${API}/attachments/metrology/${cvtId}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      if (response.ok) {
        const data = await response.json();
        console.log('Fetched attachments for CVT', cvtId, ':', data);
        // Filtrează doar documentele (nu avatarurile)
        const documentAttachments = data.filter(att => 
          !att.mime_type.startsWith('image/') || 
          (!att.filename.includes('avatar') && !att.filename.includes('custom_avatar'))
        );
        console.log('Document attachments for CVT', cvtId, ':', documentAttachments);
        setAttachmentCount(documentAttachments.length);
      } else {
        console.error('Failed to fetch attachments for CVT', cvtId, ':', response.status);
      }
    } catch (error) {
      console.error('Error fetching CVT attachments:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAttachmentCount();
  }, [cvtId]);

  return (
    <button 
      className="btn-attachment"
      title="View CVT Attachments"
      onClick={onClick}
      style={{ 
        fontSize: '14px', 
        padding: '2px 4px',
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        width: '32px',
        height: '32px',
        cursor: 'pointer',
        border: 'none',
        backgroundColor: '#d1e7ff',
        borderRadius: '50%',
        color: '#1e3a8a'
      }}
    >
      📎
    </button>
  );
};

// Custom hook for fetching avatars
const useAvatar = (entityType, entityId) => {
  const [avatar, setAvatar] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchAvatar = async () => {
    if (!entityType || !entityId) return;
    
    // Skip avatar fetch for entity types that don't exist in backend
    const skipAvatarTypes = ['jackpots', 'metrology', 'metrology2', 'commission_dates'];
    if (skipAvatarTypes.includes(entityType)) {
      setAvatar(null);
      setLoading(false);
      return;
    }
    
    setLoading(true);
    try {
      let url;
      if (entityType === 'game_mixes') {
        url = `${API}/attachments/game_mixes/${entityId}`;
      } else {
        url = `${API}/attachments/${entityType}/${entityId}`;
      }
      const response = await fetch(url, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      if (response.ok) {
        const attachments = await response.json();
        const avatarAttachment = attachments.find(att => 
          att.mime_type.startsWith('image/') && 
          (att.filename.includes('avatar') || att.filename.includes('custom_avatar'))
        );
        setAvatar(avatarAttachment || null);
      }
    } catch (error) {
      console.error('Error fetching avatar:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAvatar();
  }, [entityType, entityId]);

  return { avatar, setAvatar, loading, refetch: fetchAvatar };
};

// Helper function to generate initials from entity name
const generateInitials = (name, entityType) => {
  if (!name || typeof name !== 'string') {
    return '?';
  }
  // Extrage doar litere și cifre, ignoră simboluri
  const words = name.trim().split(/\s+|-/).filter(Boolean);
  
  // Pentru Cabinets: 4 caractere (prima literă din primul cuvânt + primele 3 din al doilea)
  if (entityType === 'cabinets' && words.length >= 2) {
    const first = words[0].match(/[A-Za-z]/);
    const second = words[1].match(/[A-Za-z0-9]{1,3}/);
    const result = `${first ? first[0].toUpperCase() : ''}${second ? second[0].toUpperCase() : ''}` || '?';
    return result;
  }
  
  // Pentru Slots: primele 2 caractere din serial number
  if (entityType === 'slots') {
    const result = name.substring(0, 2).toUpperCase() || '?';
    return result;
  }
  
  // Pentru restul: 1 + 2 (prima literă din primul cuvânt + primele 2 din al doilea)
  if (words.length >= 2) {
    const first = words[0].match(/[A-Za-z]/);
    const second = words[1].match(/[A-Za-z0-9]{1,2}/);
    const result = `${first ? first[0].toUpperCase() : ''}${second ? second[0].toUpperCase() : ''}` || '?';
    return result;
  } else if (words.length === 1) {
    const match = words[0].match(/[A-Za-z0-9]{1,2}/);
    const result = match ? match[0].toUpperCase() : '?';
    return result;
  }
  return '?';
};
// Custom Avatar Editor Component
const CustomAvatarEditor = ({ entityType, entityId, currentAvatar, onAvatarChange, entityName, showCustomNotification }) => {
  const [customText, setCustomText] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [showEditor, setShowEditor] = useState(false);

  useEffect(() => {
    if (entityName) {
      setCustomText(generateInitials(entityName, entityType));
    } else {
      setCustomText(generateInitials('Unknown', entityType));
    }
  }, [entityName, entityType]);

  const handleSaveCustomAvatar = async () => {
    if (customText.trim()) {
      try {
        // Creează un canvas pentru a genera avatar-ul personalizat
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 200;
        canvas.height = 200;

        // Fundal albastru
        ctx.fillStyle = '#1976d2';
        ctx.fillRect(0, 0, 200, 200);

        // Text alb bold, font adaptiv, shadow pentru contrast
        ctx.font = 'bold 90px Arial, sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = '#fff';
        ctx.shadowColor = '#000';
        ctx.shadowBlur = 8;
        const text = customText.substring(0, 8).toUpperCase();
        ctx.fillText(text, 100, 100);
        ctx.shadowBlur = 0;

        // Convertește la base64
        const dataURL = canvas.toDataURL('image/png');
        
        // Creează obiectul avatar pentru upload
        const avatarData = {
          filename: `custom_avatar_${entityType}_${entityId}_${Date.now()}.png`,
          original_filename: `custom_avatar_${entityType}_${entityId}.png`,
          file_size: Math.round((dataURL.length * 3) / 4), // Aproximare dimensiune
          mime_type: 'image/png',
          file_data: dataURL.split(',')[1], // Elimină prefixul data:image/png;base64,
          entity_type: entityType,
          entity_id: entityId
        };

        // Upload la backend
        const response = await fetch(`${API}/attachments`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(avatarData)
        });

        if (response.ok) {
          const uploadedAvatar = await response.json();
          onAvatarChange(uploadedAvatar);
          showCustomNotification('Custom avatar saved successfully!', 'success');
        } else {
          throw new Error('Failed to save avatar');
        }
      } catch (error) {
        console.error('Error saving custom avatar:', error);
                  showCustomNotification('Failed to save custom avatar. Please try again.', 'error');
      }
      
      setIsEditing(false);
      setShowEditor(false);
    }
  };

  const handleCancel = () => {
    setCustomText(generateInitials(entityName || 'Unknown', entityType));
    setIsEditing(false);
    setShowEditor(false);
  };

  return (
    <div className="custom-avatar-editor">
      <div className="avatar-preview-section">
        <div className="avatar-preview">
          <div
            className="custom-avatar-display"
            style={{
              width: '68px',
              height: '68px',
              background: '#1976d2',
              color: '#ffffff',
              fontWeight: 'bold',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              borderRadius: '50%',
              fontSize: entityType === 'cabinets' ? '16px' : '20px', // Font mai mic pentru cabinete
              cursor: 'pointer',
              border: '2px solid #ddd',
              boxShadow: '0 4px 8px rgba(0, 0, 0, 0.3)'
            }}
            onClick={() => setShowEditor(!showEditor)}
            title="Click to edit custom avatar"
          >
            {customText.substring(0, 8).toUpperCase()}
          </div>
        </div>
        
        <div className="avatar-actions">
          <button
            type="button"
            className="btn-edit-avatar"
            onClick={() => setShowEditor(!showEditor)}
            style={{
              padding: '4px 8px',
              fontSize: '12px',
              background: '#1976d2',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              marginTop: '8px'
            }}
          >
            ✏️ Edit Custom Avatar
          </button>
        </div>
      </div>

      {showEditor && (
        <div className="avatar-editor-modal">
          <div className="editor-content">
            <h4>Custom Avatar Editor</h4>
            <div className="editor-input">
              <label>Custom Text (max 8 characters):</label>
              <input
                type="text"
                value={customText}
                onChange={(e) => setCustomText(e.target.value.substring(0, 8))}
                maxLength={8}
                placeholder="Enter custom text"
                style={{
                  padding: '8px',
                  border: '1px solid #ddd',
                  borderRadius: '4px',
                  fontSize: '14px',
                  width: '200px'
                }}
              />
            </div>
            
            <div className="editor-preview">
              <h5>Preview:</h5>
              <div
                className="preview-avatar"
                style={{
                  width: '120px',
                  height: '120px',
                  background: '#1976d2',
                  color: '#ffffff',
                  fontWeight: 'bold',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  borderRadius: '50%',
                  fontSize: '36px', // Font proporțional pentru 120px
                  margin: '10px auto',
                  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)'
                }}
              >
                {customText.substring(0, 8).toUpperCase()}
              </div>
            </div>

            <div className="editor-actions">
              <button
                type="button"
                onClick={handleSaveCustomAvatar}
                style={{
                  padding: '8px 16px',
                  background: '#4caf50',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  marginRight: '8px'
                }}
              >
                Save Avatar
              </button>
              <button
                type="button"
                onClick={handleCancel}
                style={{
                  padding: '8px 16px',
                  background: '#f44336',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Avatar Display Component (for tables)
const AvatarDisplay = ({ entityType, entityId, size = 50, entityName, rectangular, blueBgIfNoAvatar }) => {
  const { avatar, loading } = useAvatar(entityType, entityId || 'temp');

  // Game Mixes: avatar dreptunghiular 20x95 sau text pe fundal albastru
  if (entityType === 'game_mixes') {
    const width = 20, height = 95;
    if (loading) {
      return (
        <div className="avatar-display loading rectangular" style={{ width, height }}>
          <div className="spinner-small"></div>
        </div>
      );
    }
    if (avatar) {
      return (
        <img
          src={`data:${avatar.mime_type};base64,${avatar.file_data}`}
          alt="Avatar"
          className="avatar-display rectangular"
          style={{ width, height, objectFit: 'cover' }}
        />
      );
    }
    
    return (
      <div
        className="avatar-display rectangular blue-bg-avatar"
        style={{
          width,
          height,
          background: '#1976d2',
          color: '#fff',
          fontWeight: 'bold',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          borderRadius: 4,
          fontSize: 12,
          whiteSpace: 'normal',
          wordBreak: 'break-word',
          textAlign: 'center',
          padding: '0 4px',
          lineHeight: '1.1',
          overflow: 'visible',
        }}
        title={entityName}
      >
        <span style={{width: '100%', wordBreak: 'break-word', whiteSpace: 'normal'}}>{entityName}</span>
      </div>
    );
  }

  // Restul modulelor: avatar rotund/pătrat 50x50, cu inițiale dacă nu există poză, fundal transparent
  let width = 50, height = 50;
  if (loading) {
    return (
      <div className="avatar-display loading" style={{ width, height }}>
        <div className="spinner-small"></div>
      </div>
    );
  }
  if (avatar) {
    return (
      <img
        src={`data:${avatar.mime_type};base64,${avatar.file_data}`}
        alt="Avatar"
        className="avatar-display"
        style={{ width, height, objectFit: 'cover', borderRadius: '50%' }}
      />
    );
  }
  // Inițiale cu fundal albastru pentru toate avatarele editabile
  const initials = generateInitials(entityName || 'Unknown', entityType) || '?';
  
  // Calculează dimensiunea fontului proporțională cu dimensiunea avatar-ului
  // Pentru cabinete, font mai mic pentru a încăpea 4 caractere
  const fontSize = entityType === 'cabinets' 
    ? Math.max(8, Math.min(width * 0.25, 16)) // Pentru cabinete: între 8px și 16px
    : Math.max(12, Math.min(width * 0.4, 24)); // Pentru restul: între 12px și 24px
  
  return (
    <div
      className="avatar-display"
      style={{
        width,
        height,
        borderRadius: '50%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontWeight: 700,
        fontSize: `${fontSize}px`, // Font proporțional cu dimensiunea avatar-ului
        color: '#ffffff', // Text alb pentru toate
        background: '#1976d2', // Background albastru pentru toate
        boxShadow: '0 4px 8px rgba(0,0,0,0.3)', // Umbră pentru toate
      }}
      title={entityName}
    >
      {initials}
    </div>
  );
};

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Auto-logout after 15 minutes of inactivity
  useEffect(() => {
    let inactivityTimer;

    const resetTimer = () => {
      clearTimeout(inactivityTimer);
      inactivityTimer = setTimeout(() => {
        if (user) {
          localStorage.removeItem('token');
          setUser(null);
          showCustomNotification('You have been logged out due to inactivity.', 'warning');
        }
      }, 15 * 60 * 1000); // 15 minutes
    };

    const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];

    if (user) {
      // Start timer
      resetTimer();
      
      // Add event listeners for user activity
      events.forEach(event => {
        document.addEventListener(event, resetTimer, true);
      });
    }

    return () => {
      clearTimeout(inactivityTimer);
      events.forEach(event => {
        document.removeEventListener(event, resetTimer, true);
      });
    };
  }, [user]);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      fetch(`${API}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      })
        .then(res => res.json())
        .then(data => {
          if (data.id) {
            setUser(data);
          } else {
            localStorage.removeItem('token');
          }
        })
        .catch(() => localStorage.removeItem('token'))
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (username, password) => {
    const response = await fetch(`${API}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    if (response.ok) {
      localStorage.setItem('token', data.access_token);
      
      // Încarcă permisiunile imediat după login
      const meResponse = await fetch(`${API}/auth/me`, {
        headers: { 'Authorization': `Bearer ${data.access_token}` }
      });
      if (meResponse.ok) {
        const userData = await meResponse.json();
        setUser(userData);
      } else {
        setUser(data.user);
      }
      
      return true;
    }
    throw new Error(data.detail || 'Login failed');
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

const useAuth = () => useContext(AuthContext);

// Helper function for entity display names
const getEntityDisplayName = (type) => {
  const names = {
    companies: 'Company',
    locations: 'Location',
    providers: 'Provider',
    cabinets: 'Cabinet',
    slots: 'Slot Machine',
    gamemixes: 'Game Mix',
    invoices: 'Invoice',
    onjn: 'ONJN Report',
    legal: 'Legal Document',
    users: 'User',
    jackpots: 'Jackpot',
    metrology: 'Metrology',
    metrology2: 'Metrology',
    comision_date: 'Comision Date'
  };
  return names[type] || type;
};
// Bulk Edit Form Component
const BulkEditForm = ({ entityType, selectedItems, onSave, onClose, companies, locations, providers, cabinets, gameMixes, slotMachines }) => {
  const [formData, setFormData] = useState({});

  const handleChange = (field, value) => {
    // If setting status to inactive for slots, show confirmation
    if (field === 'status' && value === 'inactive' && entityType === 'slots') {
      setShowBulkStatusConfirm(true);
      setBulkStatusData({ field, value, entityType });
      return; // Wait for confirmation
    }
    
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  const getCommonFields = (type) => {
    const commonFields = {
      companies: ['name', 'email', 'phone', 'status'],
      locations: ['name', 'address', 'status'], 
      providers: ['email', 'phone', 'status'],
      cabinets: ['status'],
      slots: ['cabinet_id', 'game_mix_id', 'provider_id', 'model', 'serial_number', 'denomination', 'max_bet', 'rtp', 'gaming_places', 'commission_date', 'invoice_number', 'status', 'location_id', 'production_year', 'ownership_type', 'owner_company_id', 'lease_provider_id', 'lease_contract_number'],
      gamemixes: ['status'],
      invoices: ['status'],
      onjn: ['status'],
      legal: ['status'],
      users: ['role', 'is_active'],
      metrology: ['certificate_number', 'issue_date', 'issuing_authority', 'description'],
      metrology2: ['certificate_number', 'issue_date', 'issuing_authority', 'cvt_type', 'cvt_expiry_date', 'description'],
      comision_date: ['event_name', 'commission_date', 'serial_numbers'],
      jackpots: ['jackpot_type']
    };
    return commonFields[type] || ['status'];
  };

  const renderField = (field) => {
    switch (field) {
      case 'status':
        // Handle different status options based on entity type
        const getStatusOptions = () => {
          if (entityType === 'invoices') {
            return [
              { value: 'pending', label: 'Pending' },
              { value: 'paid', label: 'Paid' },
              { value: 'overdue', label: 'Overdue' }
            ];
          }
          // Default status options for other entities
          return [
            { value: 'active', label: 'Active' },
            { value: 'inactive', label: 'Inactive' }
          ];
        };

        return (
          <div className="form-group" key={field}>
            <label>Status</label>
            <select
              value={formData.status || ''}
              onChange={(e) => handleChange('status', e.target.value)}
            >
              <option value="">Keep unchanged</option>
              {getStatusOptions().map(option => (
                <option key={option.value} value={option.value}>{option.label}</option>
              ))}
            </select>
          </div>
        );
      case 'role':
        return (
          <div className="form-group" key={field}>
            <label>Role</label>
            <select
              value={formData.role || ''}
              onChange={(e) => handleChange('role', e.target.value)}
            >
              <option value="">Keep unchanged</option>
              <option value="admin">Admin</option>
              <option value="manager">Manager</option>
              <option value="operator">Operator</option>
            </select>
          </div>
        );
      case 'is_active':
        return (
          <div className="form-group" key={field}>
            <label>
              <input
                type="checkbox"
                checked={formData.is_active || false}
                onChange={(e) => handleChange('is_active', e.target.checked)}
              />
              Is Active
            </label>
          </div>
        );
      default:
        // Handle slots specific fields
        if (entityType === 'slots') {
          switch (field) {
            case 'cabinet_id':
              return (
                <div className="form-group" key={field}>
                  <label>Cabinet</label>
                  <select
                    value={formData[field] || ''}
                    onChange={(e) => handleChange(field, e.target.value)}
                  >
                    <option value="">Keep unchanged</option>
                    {cabinets && cabinets.map(cabinet => (
                      <option key={cabinet.id} value={cabinet.id}>
                        {cabinet.name} - {cabinet.model || 'No Model'}
                      </option>
                    ))}
                  </select>
                </div>
              );
            case 'game_mix_id':
              return (
                <div className="form-group" key={field}>
                  <label>Game Mix</label>
                  <select
                    value={formData[field] || ''}
                    onChange={(e) => handleChange(field, e.target.value)}
                  >
                    <option value="">Keep unchanged</option>
                    {gameMixes && gameMixes.map(gameMix => (
                      <option key={gameMix.id} value={gameMix.id}>
                        {gameMix.name} ({gameMix.game_count} games)
                      </option>
                    ))}
                  </select>
                </div>
              );
            case 'provider_id':
              return (
                <div className="form-group" key={field}>
                  <label>Provider</label>
                  <select
                    value={formData[field] || ''}
                    onChange={(e) => handleChange(field, e.target.value)}
                  >
                    <option value="">Keep unchanged</option>
                    {providers && providers.map(provider => (
                      <option key={provider.id} value={provider.id}>
                        {provider.company_name}
                      </option>
                    ))}
                  </select>
                </div>
              );
            case 'location_id':
              return (
                <div className="form-group" key={field}>
                  <label>Location</label>
                  <select
                    value={formData[field] || ''}
                    onChange={(e) => handleChange(field, e.target.value)}
                  >
                    <option value="">Keep unchanged</option>
                    {locations && locations.map(location => (
                      <option key={location.id} value={location.id}>
                        {location.name} - {location.city}
                      </option>
                    ))}
                  </select>
                </div>
              );
            case 'ownership_type':
              return (
                <div className="form-group" key={field}>
                  <label>Ownership Type</label>
                  <select
                    value={formData[field] || ''}
                    onChange={(e) => handleChange(field, e.target.value)}
                  >
                    <option value="">Keep unchanged</option>
                    <option value="property">Property</option>
                    <option value="rent">Rent</option>
                  </select>
                </div>
              );
            case 'owner_company_id':
              return (
                <div className="form-group" key={field}>
                  <label>Owner Company</label>
                  <select
                    value={formData[field] || ''}
                    onChange={(e) => handleChange(field, e.target.value)}
                  >
                    <option value="">Keep unchanged</option>
                    {companies && companies.map(company => (
                      <option key={company.id} value={company.id}>
                        {company.name}
                      </option>
                    ))}
                  </select>
                </div>
              );
            case 'lease_provider_id':
              return (
                <div className="form-group" key={field}>
                  <label>Lease Provider</label>
                  <select
                    value={formData[field] || ''}
                    onChange={(e) => handleChange(field, e.target.value)}
                  >
                    <option value="">Keep unchanged</option>
                    {providers && providers.map(provider => (
                      <option key={provider.id} value={provider.id}>
                        {provider.company_name}
                      </option>
                    ))}
                  </select>
                </div>
              );
            case 'denomination':
            case 'max_bet':
            case 'rtp':
              return (
                <div className="form-group" key={field}>
                  <label>{field.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}</label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    value={formData[field] || ''}
                    onChange={(e) => handleChange(field, parseFloat(e.target.value))}
                    placeholder={`Enter new ${field.replace('_', ' ')} (leave empty to keep unchanged)`}
                  />
                </div>
              );
            case 'gaming_places':
            case 'production_year':
              return (
                <div className="form-group" key={field}>
                  <label>{field.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}</label>
                  <input
                    type="number"
                    min="1"
                    value={formData[field] || ''}
                    onChange={(e) => handleChange(field, parseInt(e.target.value))}
                    placeholder={`Enter new ${field.replace('_', ' ')} (leave empty to keep unchanged)`}
                  />
                </div>
              );
            case 'commission_date':
              return (
                <div className="form-group" key={field}>
                  <label>Commission Date</label>
                  <Calendar
                    value={formData[field] || ''}
                    onChange={(date) => handleChange(field, date)}
                    placeholder="Select new commission date (leave empty to keep unchanged)"
                  />
                </div>
              );
            case 'model':
            case 'serial_number':
            case 'invoice_number':
            case 'lease_contract_number':
              return (
                <div className="form-group" key={field}>
                  <label>{field.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}</label>
                  <input
                    type="text"
                    value={formData[field] || ''}
                    onChange={(e) => handleChange(field, e.target.value)}
                    placeholder={`Enter new ${field.replace('_', ' ')} (leave empty to keep unchanged)`}
                  />
                </div>
              );
            default:
              return (
                <div className="form-group" key={field}>
                  <label>{field.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}</label>
                  <input
                    type="text"
                    value={formData[field] || ''}
                    onChange={(e) => handleChange(field, e.target.value)}
                    placeholder={`Enter new ${field.replace('_', ' ')} (leave empty to keep unchanged)`}
                  />
                </div>
              );
          }
        }
        
        // Handle comision_date specific fields
        if (entityType === 'comision_date') {
          switch (field) {
            case 'event_name':
              return (
                <div className="form-group" key={field}>
                  <label>Event Name</label>
                  <input
                    type="text"
                    value={formData[field] || ''}
                    onChange={(e) => handleChange(field, e.target.value)}
                    placeholder="Enter new event name (leave empty to keep unchanged)"
                  />
                </div>
              );
            case 'commission_date':
              return (
                <div className="form-group" key={field}>
                  <label>Commission Date</label>
                  <Calendar
                    value={formData[field] || ''}
                    onChange={(date) => handleChange(field, date)}
                    placeholder="Select new commission date (leave empty to keep unchanged)"
                  />
                </div>
              );
            case 'serial_numbers':
              return (
                <div className="form-group" key={field}>
                  <label>Serial Numbers</label>
                  <textarea
                    value={formData[field] || ''}
                    onChange={(e) => handleChange(field, e.target.value)}
                    rows="3"
                    placeholder="Enter new serial numbers separated by spaces (leave empty to keep unchanged)"
                  />
                </div>
              );
            default:
              return (
                <div className="form-group" key={field}>
                  <label>{field.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}</label>
                  <input
                    type="text"
                    value={formData[field] || ''}
                    onChange={(e) => handleChange(field, e.target.value)}
                    placeholder={`Enter new ${field.replace('_', ' ')} (leave empty to keep unchanged)`}
                  />
                </div>
              );
          }
        }
        
        // Handle other entity types
        return (
          <div className="form-group" key={field}>
            <label>{field.charAt(0).toUpperCase() + field.slice(1)}</label>
            <input
              type={field.includes('email') ? 'email' : 'text'}
              value={formData[field] || ''}
              onChange={(e) => handleChange(field, e.target.value)}
              placeholder={`Enter new ${field} (leave empty to keep unchanged)`}
            />
          </div>
        );
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content bulk-edit-modal">
        <h2>Bulk Edit {getEntityDisplayName(entityType)}</h2>
        <p>Editing {selectedItems.length} items. Only filled fields will be updated.</p>
        <form onSubmit={handleSubmit} className="bulk-edit-form">
          {getCommonFields(entityType).map(field => renderField(field))}
          <div className="form-actions">
            <button type="submit" className="btn-primary">
              Update {selectedItems.length} Items
            </button>
            <button type="button" className="btn-secondary" onClick={onClose}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const { login } = useAuth();

  // Load saved credentials on component mount
  useEffect(() => {
    const savedCredentials = localStorage.getItem('savedCredentials');
    if (savedCredentials) {
      const { username: savedUsername, password: savedPassword } = JSON.parse(savedCredentials);
      setUsername(savedUsername || '');
      setPassword(savedPassword || '');
      setRememberMe(true);
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    
    try {
      await login(username, password);
      
      // Save credentials if remember me is checked
      if (rememberMe) {
        localStorage.setItem('savedCredentials', JSON.stringify({
          username: username,
          password: password
        }));
      } else {
        // Remove saved credentials if remember me is unchecked
        localStorage.removeItem('savedCredentials');
      }
      
      // User state will trigger useEffect to load dashboard data
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-background">
        <img 
          src="https://images.unsplash.com/photo-1563753159011-f1d8b8272c8c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwzfHxwcm9mZXNzaW9uYWwlMjBkYXNoYm9hcmR8ZW58MHx8fGJsYWNrfDE3NTIxNDI5NTZ8MA&ixlib=rb-4.1.0&q=85"
          alt="Professional dashboard"
          className="login-bg-image"
        />
        <div className="login-overlay"></div>
      </div>
      
      <div className="login-card">
        <div className="login-header" style={{ textAlign: 'center' }}>
          <img 
            src="/logo.png" 
            alt="CASHPOT Logo" 
            style={{
              width: '300px',
              height: 'auto',
              maxWidth: '100%',
              marginBottom: '20px',
              display: 'block',
              margin: '0 auto 20px auto'
            }}
          />
        </div>
        
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="username" style={{ color: 'white' }}>Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="form-input"
              placeholder="Enter your username"
              style={{ color: 'white' }}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password" style={{ color: 'white' }}>Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="form-input"
              placeholder="Enter your password"
              style={{ color: 'white' }}
            />
          </div>

          <div className="form-group">
            <label className="remember-me-label">
              <input
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                className="remember-me-checkbox"
              />
              <span className="remember-me-text" style={{ color: 'white' }}>Remember my password</span>
            </label>
          </div>
          
          {error && <div className="error-message">{error}</div>}
          
          <button type="submit" disabled={loading} className="login-button">
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
        
        <div className="login-footer">
          <p>Demo Admin: admin / password</p>
          <p>Contact your administrator for access</p>
        </div>
      </div>
    </div>
  );
};
// Generic Entity Form Component
const EntityForm = ({ entityType, entity, onSave, onClose, companies, locations, providers, cabinets, gameMixes, invoices, users, slotMachines, metrology, jackpots, showCustomNotification }) => {
  const [formData, setFormData] = useState({});
  
  // Avatar state
  const { avatar, setAvatar } = useAvatar(entityType, entity?.id);
  
  const handleAvatarChange = (newAvatar) => {
    setAvatar(newAvatar);
  };



  useEffect(() => {
    // Initialize form data based on entity type
    if (entity) {
      setFormData(entity);
    } else {
      setFormData(getDefaultFormData(entityType));
    }
  }, [entity, entityType]);

  const getDefaultFormData = (type) => {
    const defaults = {
      companies: {
        name: '',
        registration_number: '',
        tax_id: '',
        address: '',
        phone: '',
        email: '',
        website: '',
        contact_person: ''
      },
      locations: {
        name: '',
        address: '',
        city: '',
        county: '',
        country: 'Romania',
        postal_code: '',
        company_id: '',
        manager_id: '',
        manager_phone: '',
        manager_email: '',
        contact_person_type: 'manual',
        contact_person_id: '',
        contact_person: '',
        contact_email: '',
        contact_phone: ''
      },
      providers: {
        name: '',
        company_name: '',
        contact_person: '',
        email: '',
        phone: '',
        address: '',
        website: ''
      },
      cabinets: {
        name: '',
        model: '',
        provider_id: ''
      },
      slots: {
        cabinet_id: '',
        game_mix_id: '',
        provider_id: '',
        model: '',
        production_year: new Date().getFullYear(),
        location_id: '',
        ownership_type: '',
        owner_company_id: '',
        lease_provider_id: '',
        serial_number: '',
        denomination: 0.10,
        max_bet: 100.00,
        rtp: 95.00,
        gaming_places: 1,
        commission_date: '',
        invoice_number: '',
        cvt_end_date: '',
        jackpot_name: ''
      },
      gamemixes: {
        name: '',
        description: '',
        provider_id: '',
        games: []
      },
      invoices: {
        invoice_number: '',
        company_id: '',
        location_id: '',
        serial_numbers: '',
        issue_date: new Date().toISOString().split('T')[0],
        due_date: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        amount: 0,
        currency: 'EUR',
        status: 'pending',
        description: '',
        transaction_type: '',
        buyer_id: '',
        seller_id: ''
      },
      onjn: {
        report_number: '',
        report_type: 'monthly',
        company_id: '',
        location_id: '',
        report_date: '',
        equipment_data: {}
      },
      legal: {
        title: '',
        document_type: 'license',
        company_id: '',
        location_id: '',
        issue_date: '',
        issuing_authority: '',
        description: ''
      },
      metrology: {
        serial_number: '',
        certificate_number: '',
        certificate_type: 'calibration',
        issue_date: new Date().toISOString().split('T')[0],
        expiry_date: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toISOString().split('T')[0], // Default 1 year expiry
        issuing_authority: '',
        status: 'active',
        description: ''
      },
      metrology2: {
        serial_number: '',
        certificate_number: '',
        issue_date: new Date().toISOString().split('T')[0],
        issuing_authority: '',
        status: 'active',
        description: ''
      },
              jackpots: {
          serial_number: '',
          jackpot_name: '',
          jackpot_type: 'progressive',
          increment_rate: 0.1,
          level_1: '',
          level_2: '',
          level_3: '',
          level_4: '',
          level_5: '',
          description: ''
        },
        comision_date: {
          event_name: '',
          commission_date: new Date().toISOString().split('T')[0],
          serial_numbers: ''
        }
    };
    return defaults[type] || {};
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  const handleChange = (field, value) => {
    setFormData(prev => {
      const newData = { ...prev, [field]: value };
      
      // Debug: Log transaction_type changes
      if (entityType === 'invoices' && field === 'transaction_type') {
        console.log('🔄 Transaction Type changed:', value);
        console.log('🔄 Previous formData:', prev);
        console.log('🔄 New formData:', newData);
      }
      
      // If provider changes in slots form, reset cabinet and game mix selection
      if (entityType === 'slots' && field === 'provider_id') {
        newData.cabinet_id = '';
        newData.game_mix_id = '';
        newData.model = ''; // Reset model when provider changes
      }
      
      // If cabinet changes in slots form, auto-fill model from selected cabinet
      if (entityType === 'slots' && field === 'cabinet_id' && value) {
        const selectedCabinet = cabinets.find(cabinet => cabinet.id === value);
        if (selectedCabinet) {
          newData.model = selectedCabinet.model || `${selectedCabinet.name} Model`;
        } else {
          newData.model = '';
        }
      }
      
      // If serial number changes in slots form, auto-fill ownership details based on invoice
      if (entityType === 'slots' && field === 'serial_number' && value) {
        console.log('🔍 Serial number changed to:', value);
        console.log('📋 Available invoices:', invoices.length);
        console.log('📋 Available companies:', companies.length);
        console.log('📋 Available providers:', providers.length);
        
        // Find existing slot machine with this serial number
        const existingSlot = slotMachines.find(slot => slot.serial_number === value);
        if (existingSlot) {
          newData.commission_date = existingSlot.commission_date || '';
          newData.invoice_number = existingSlot.invoice_number || '';
          console.log('🎰 Found existing slot:', existingSlot);
        }
        
        // Find invoice with this serial number and auto-fill ownership details
        console.log('🔍 Searching for serial number in invoices...');
        invoices.forEach((invoice, index) => {
          console.log(`📄 Invoice ${index + 1}:`, {
            invoice_number: invoice.invoice_number,
            serial_numbers: invoice.serial_numbers,
            transaction_type: invoice.transaction_type,
            buyer_id: invoice.buyer_id,
            seller_id: invoice.seller_id
          });
        });
        
        const invoiceWithSerial = invoices.find(invoice => 
          invoice.serial_numbers && 
          invoice.serial_numbers.split(/\s+/).includes(value)
        );
        
        if (invoiceWithSerial) {
          console.log('🔍 Found invoice for serial number:', value);
          console.log('📄 Invoice transaction type:', invoiceWithSerial.transaction_type);
          console.log('🏢 Buyer ID:', invoiceWithSerial.buyer_id);
          console.log('🏪 Seller ID:', invoiceWithSerial.seller_id);
          console.log('📄 Invoice number:', invoiceWithSerial.invoice_number);
          console.log('📅 Issue date:', invoiceWithSerial.issue_date);
          console.log('🔄 Current formData before changes:', prev);
          
          if (invoiceWithSerial.transaction_type === 'buy') {
            // For buy transactions: Property (Owned) + Buyer Company
            const buyerCompany = companies.find(c => c.id === invoiceWithSerial.buyer_id);
            newData.ownership_type = 'property';
            newData.owner_company_id = invoiceWithSerial.buyer_id || '';
            newData.invoice_number = invoiceWithSerial.invoice_number || '';
            // Convert date to ISO string format for Calendar component
            // Use commission_date if available, otherwise use issue_date
            const dateToUse = invoiceWithSerial.commission_date || invoiceWithSerial.issue_date;
            if (dateToUse) {
              const date = new Date(dateToUse);
              newData.commission_date = date.toISOString().split('T')[0];
              console.log('📅 Date to use:', dateToUse);
              console.log('📅 Converted date:', newData.commission_date);
            } else {
              newData.commission_date = '';
            }
            // Set CVT End Date and Jackpot Name from invoice
            if (invoiceWithSerial.cvt_end_date) {
              const cvtDate = new Date(invoiceWithSerial.cvt_end_date);
              newData.cvt_end_date = cvtDate.toISOString().split('T')[0];
              console.log('📅 Set cvt_end_date to:', invoiceWithSerial.cvt_end_date);
            }
            
            if (invoiceWithSerial.jackpots && invoiceWithSerial.jackpots.length > 0) {
              if (invoiceWithSerial.jackpots.length === 1) {
                newData.jackpot_name = invoiceWithSerial.jackpots[0];
              } else {
                newData.jackpot_name = 'Multiple Jackpots';
              }
              console.log('🎰 Set jackpot_name to:', newData.jackpot_name);
            }
            
            // Set CVT End Date from Metrology table
            const metrologyData = metrology.find(m => m.serial_number === value);
            if (metrologyData && metrologyData.cvt_end_date) {
              const cvtDate = new Date(metrologyData.cvt_end_date);
              newData.cvt_end_date = cvtDate.toISOString().split('T')[0];
              console.log('📅 Set cvt_end_date from Metrology to:', metrologyData.cvt_end_date);
            }
            
            // Set Jackpot Name from Jackpots table
            const jackpotsData = jackpots.filter(j => j.serial_number === value);
            if (jackpotsData && jackpotsData.length > 0) {
              if (jackpotsData.length === 1) {
                newData.jackpot_name = jackpotsData[0].jackpot_name;
              } else {
                newData.jackpot_name = 'Multiple Jackpots';
              }
              console.log('🎰 Set jackpot_name from Jackpots to:', newData.jackpot_name);
            }
            
            console.log('🟢 Buy transaction - Property Owned by:', buyerCompany?.name);
            console.log('🏢 Set owner_company_id to:', invoiceWithSerial.buyer_id);
            console.log('📄 Set invoice_number to:', invoiceWithSerial.invoice_number);
            console.log('📅 Set commission_date to:', invoiceWithSerial.issue_date);
            console.log('🏠 Set ownership_type to: property');
          } else if (invoiceWithSerial.transaction_type === 'rent') {
            // For rent transactions: Rent (Leased) + Seller Provider
            const sellerProvider = providers.find(p => p.id === invoiceWithSerial.seller_id);
            newData.ownership_type = 'rent';
            newData.lease_provider_id = invoiceWithSerial.seller_id || '';
            newData.invoice_number = invoiceWithSerial.invoice_number || '';
            // Convert date to ISO string format for Calendar component
            // Use commission_date if available, otherwise use issue_date
            const dateToUse = invoiceWithSerial.commission_date || invoiceWithSerial.issue_date;
            if (dateToUse) {
              const date = new Date(dateToUse);
              newData.commission_date = date.toISOString().split('T')[0];
              console.log('📅 Date to use:', dateToUse);
              console.log('📅 Converted date:', newData.commission_date);
            } else {
              newData.commission_date = '';
            }
            // Set CVT End Date and Jackpot Name from invoice
            if (invoiceWithSerial.cvt_end_date) {
              const cvtDate = new Date(invoiceWithSerial.cvt_end_date);
              newData.cvt_end_date = cvtDate.toISOString().split('T')[0];
              console.log('📅 Set cvt_end_date to:', invoiceWithSerial.cvt_end_date);
            }
            
            if (invoiceWithSerial.jackpots && invoiceWithSerial.jackpots.length > 0) {
              if (invoiceWithSerial.jackpots.length === 1) {
                newData.jackpot_name = invoiceWithSerial.jackpots[0];
              } else {
                newData.jackpot_name = 'Multiple Jackpots';
              }
              console.log('🎰 Set jackpot_name to:', newData.jackpot_name);
            }
            
            // Set CVT End Date from Metrology table
            const metrologyData = metrology.find(m => m.serial_number === value);
            if (metrologyData && metrologyData.cvt_end_date) {
              const cvtDate = new Date(metrologyData.cvt_end_date);
              newData.cvt_end_date = cvtDate.toISOString().split('T')[0];
              console.log('📅 Set cvt_end_date from Metrology to:', metrologyData.cvt_end_date);
            }
            
            // Set Jackpot Name from Jackpots table
            const jackpotsData = jackpots.filter(j => j.serial_number === value);
            if (jackpotsData && jackpotsData.length > 0) {
              if (jackpotsData.length === 1) {
                newData.jackpot_name = jackpotsData[0].name;
              } else {
                newData.jackpot_name = 'Multiple Jackpots';
              }
              console.log('🎰 Set jackpot_name from Jackpots to:', newData.jackpot_name);
            }
            
            console.log('🔵 Rent transaction - Leased from:', sellerProvider?.name);
            console.log('🏪 Set lease_provider_id to:', invoiceWithSerial.seller_id);
            console.log('📄 Set invoice_number to:', invoiceWithSerial.invoice_number);
            console.log('📅 Set commission_date to:', invoiceWithSerial.issue_date);
            console.log('🏠 Set ownership_type to: rent');
          } else if (invoiceWithSerial.transaction_type === 'sell') {
            // For sell transactions: Property (Owned) + Buyer Company
            const buyerCompany = companies.find(c => c.id === invoiceWithSerial.buyer_id);
            newData.ownership_type = 'property';
            newData.owner_company_id = invoiceWithSerial.buyer_id || '';
            newData.invoice_number = invoiceWithSerial.invoice_number || '';
            // Convert date to ISO string format for Calendar component
            // Use commission_date if available, otherwise use issue_date
            const dateToUse = invoiceWithSerial.commission_date || invoiceWithSerial.issue_date;
            if (dateToUse) {
              const date = new Date(dateToUse);
              newData.commission_date = date.toISOString().split('T')[0];
              console.log('📅 Date to use:', dateToUse);
              console.log('📅 Converted date:', newData.commission_date);
            } else {
              newData.commission_date = '';
            }
            // Set CVT End Date and Jackpot Name from invoice
            if (invoiceWithSerial.cvt_end_date) {
              const cvtDate = new Date(invoiceWithSerial.cvt_end_date);
              newData.cvt_end_date = cvtDate.toISOString().split('T')[0];
              console.log('📅 Set cvt_end_date to:', invoiceWithSerial.cvt_end_date);
            }
            
            if (invoiceWithSerial.jackpots && invoiceWithSerial.jackpots.length > 0) {
              if (invoiceWithSerial.jackpots.length === 1) {
                newData.jackpot_name = invoiceWithSerial.jackpots[0];
              } else {
                newData.jackpot_name = 'Multiple Jackpots';
              }
              console.log('🎰 Set jackpot_name to:', newData.jackpot_name);
            }
            
            // Set CVT End Date from Metrology table
            const metrologyData = metrology.find(m => m.serial_number === value);
            if (metrologyData && metrologyData.cvt_end_date) {
              const cvtDate = new Date(metrologyData.cvt_end_date);
              newData.cvt_end_date = cvtDate.toISOString().split('T')[0];
              console.log('📅 Set cvt_end_date from Metrology to:', metrologyData.cvt_end_date);
            }
            
            // Set Jackpot Name from Jackpots table
            const jackpotsData = jackpots.filter(j => j.serial_number === value);
            if (jackpotsData && jackpotsData.length > 0) {
              if (jackpotsData.length === 1) {
                newData.jackpot_name = jackpotsData[0].name;
              } else {
                newData.jackpot_name = 'Multiple Jackpots';
              }
              console.log('🎰 Set jackpot_name from Jackpots to:', newData.jackpot_name);
            }
            
            console.log('🟡 Sell transaction - Property Owned by:', buyerCompany?.name);
            console.log('🏢 Set owner_company_id to:', invoiceWithSerial.buyer_id);
            console.log('📄 Set invoice_number to:', invoiceWithSerial.invoice_number);
            console.log('📅 Set commission_date to:', invoiceWithSerial.issue_date);
            console.log('🏠 Set ownership_type to: property');
          }
          
          console.log('🔄 Final newData after auto-fill:', {
            ownership_type: newData.ownership_type,
            owner_company_id: newData.owner_company_id,
            lease_provider_id: newData.lease_provider_id,
            invoice_number: newData.invoice_number,
            commission_date: newData.commission_date,
            cvt_end_date: newData.cvt_end_date,
            jackpot_name: newData.jackpot_name
          });
          console.log('🔄 About to update formData with newData');
        } else {
          console.log('❌ No invoice found for serial number:', value);
        }
      }
      
      // If manager changes in locations form, auto-fill phone and email
      if (entityType === 'locations' && field === 'manager_id') {
        if (value) {
          const selectedManager = Array.isArray(users) ? users.find(user => user.id === value) : null;
          if (selectedManager) {
            newData.manager_phone = selectedManager.phone || '';
            newData.manager_email = selectedManager.email || '';
          }
        } else {
          // Clear manager details if no manager is selected
          newData.manager_phone = '';
          newData.manager_email = '';
        }
      }
      
      // If contact person changes in locations form, auto-fill contact details
      if (entityType === 'locations' && field === 'contact_person_id') {
        if (value) {
          const selectedContact = Array.isArray(users) ? users.find(user => user.id === value) : null;
          if (selectedContact) {
            newData.contact_person = `${selectedContact.first_name || ''} ${selectedContact.last_name || ''}`.trim() || selectedContact.username;
            newData.contact_email = selectedContact.email || '';
            newData.contact_phone = selectedContact.phone || '';
          }
        } else {
          // Clear contact details if no contact person is selected
          newData.contact_person = '';
          newData.contact_email = '';
          newData.contact_phone = '';
        }
      }
      
      return newData;
    });
  };

  const handleGamesChange = (games) => {
    const gameArray = games.split('\n').filter(game => game.trim());
    setFormData(prev => ({ ...prev, games: gameArray }));
  };
  const renderFormFields = () => {
    switch (entityType) {
      case 'companies':
        return (
          <>
            <div className="form-group">
              <label>Company Name *</label>
              <input
                type="text"
                value={formData.name || ''}
                onChange={(e) => handleChange('name', e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Registration Number *</label>
              <input
                type="text"
                value={formData.registration_number || ''}
                onChange={(e) => handleChange('registration_number', e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Tax ID *</label>
              <input
                type="text"
                value={formData.tax_id || ''}
                onChange={(e) => handleChange('tax_id', e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Address *</label>
              <input
                type="text"
                value={formData.address || ''}
                onChange={(e) => handleChange('address', e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>📞 Phone *</label>
              <input
                type="tel"
                value={formData.phone || ''}
                onChange={(e) => handleChange('phone', e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>📧 Email *</label>
              <input
                type="email"
                value={formData.email || ''}
                onChange={(e) => handleChange('email', e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Website</label>
              <input
                type="url"
                value={formData.website || ''}
                onChange={(e) => handleChange('website', e.target.value)}
              />
            </div>
            <div className="form-group">
              <label>Company Logo</label>
              <div className="avatar-section">
                <AvatarUpload
                  entityType="companies"
                  entityId={entity?.id || 'temp'}
                  currentAvatar={avatar}
                  onAvatarChange={handleAvatarChange}
                  showCustomNotification={showCustomNotification}
                />
              </div>
              <div className="form-group">
                <label>Custom Avatar Editor</label>
                <CustomAvatarEditor
                  entityType="companies"
                  entityId={entity?.id || 'temp'}
                  currentAvatar={avatar}
                  onAvatarChange={handleAvatarChange}
                  entityName={formData.name}
                  showCustomNotification={showCustomNotification}
                />
              </div>
            </div>
            <div className="form-group">
              <label>Company Documents</label>
              <FileUpload
                entityType="companies"
                entityId={entity?.id || 'temp'}
                onFileUpload={() => fetchFiles && fetchFiles()}
                showCustomNotification={showCustomNotification}
              />
              <FileDisplay
                entityType="companies"
                entityId={entity?.id || 'temp'}
                showCustomNotification={showCustomNotification}
              />
            </div>
          </>
        );

      case 'locations':
        return (
          <>
            <div className="form-group">
              <label>Location Name *</label>
              <input
                type="text"
                value={formData.name || ''}
                onChange={(e) => handleChange('name', e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Company *</label>
              <select
                value={formData.company_id || ''}
                onChange={(e) => handleChange('company_id', e.target.value)}
                required
              >
                <option value="">Select Company</option>
                {companies.map(company => (
                  <option key={company.id} value={company.id}>{company.name}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Address *</label>
              <input
                type="text"
                value={formData.address || ''}
                onChange={(e) => handleChange('address', e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>City *</label>
              <input
                type="text"
                value={formData.city || ''}
                onChange={(e) => handleChange('city', e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>County *</label>
              <input
                type="text"
                value={formData.county || ''}
                onChange={(e) => handleChange('county', e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Country</label>
              <input
                type="text"
                value={formData.country || 'Romania'}
                onChange={(e) => handleChange('country', e.target.value)}
              />
            </div>
            <div className="form-group">
              <label>Postal Code *</label>
              <input
                type="text"
                value={formData.postal_code || ''}
                onChange={(e) => handleChange('postal_code', e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Manager</label>
              <select
                value={formData.manager_id || ''}
                onChange={(e) => handleChange('manager_id', e.target.value)}
              >
                <option value="">Select Manager</option>
                {users.map(user => (
                  <option key={user.id} value={user.id}>
                    {user.first_name && user.last_name ? 
                      `${user.first_name} ${user.last_name}` : 
                      user.username} - {user.email}
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Manager Phone</label>
              <input
                type="text"
                value={formData.manager_phone || ''}
                onChange={(e) => handleChange('manager_phone', e.target.value)}
                placeholder="Auto-populated when manager is selected"
                readOnly
              />
            </div>
            <div className="form-group">
              <label>Manager Email</label>
              <input
                type="email"
                value={formData.manager_email || ''}
                onChange={(e) => handleChange('manager_email', e.target.value)}
                placeholder="Auto-populated when manager is selected"
                readOnly
              />
            </div>
            <div className="form-group">
              <label>Contact Person Type</label>
              <select
                value={formData.contact_person_type || 'manual'}
                onChange={(e) => handleChange('contact_person_type', e.target.value)}
              >
                <option value="manual">Manual Entry</option>
                <option value="user">Select from Users</option>
              </select>
            </div>
            {formData.contact_person_type === 'user' ? (
              <div className="form-group">
                <label>Contact Person (User)</label>
                <select
                  value={formData.contact_person_id || ''}
                  onChange={(e) => handleChange('contact_person_id', e.target.value)}
                >
                  <option value="">Select User</option>
                  {users.map(user => (
                    <option key={user.id} value={user.id}>
                      {user.first_name && user.last_name ? 
                        `${user.first_name} ${user.last_name}` : 
                        user.username} - {user.email}
                    </option>
                  ))}
                </select>
              </div>
            ) : (
              <>
                <div className="form-group">
                  <label>Contact Person Name</label>
                  <input
                    type="text"
                    value={formData.contact_person || ''}
                    onChange={(e) => handleChange('contact_person', e.target.value)}
                    placeholder="Enter contact person name"
                  />
                </div>
                <div className="form-group">
                  <label>Contact Person Email</label>
                  <input
                    type="email"
                    value={formData.contact_email || ''}
                    onChange={(e) => handleChange('contact_email', e.target.value)}
                    placeholder="Enter contact person email"
                  />
                </div>
                <div className="form-group">
                  <label>Contact Person Phone</label>
                  <input
                    type="tel"
                    value={formData.contact_phone || ''}
                    onChange={(e) => handleChange('contact_phone', e.target.value)}
                    placeholder="Enter contact person phone"
                  />
                </div>
              </>
            )}
            <div className="form-group">
              <label>Location Avatar</label>
              <div className="avatar-section">
                <AvatarUpload
                  entityType="locations"
                  entityId={entity?.id || 'temp'}
                  currentAvatar={avatar}
                  onAvatarChange={handleAvatarChange}
                  showCustomNotification={showCustomNotification}
                />
              </div>
              <div className="form-group">
                <label>Custom Avatar Editor</label>
                <CustomAvatarEditor
                  entityType="locations"
                  entityId={entity?.id || 'temp'}
                  currentAvatar={avatar}
                  onAvatarChange={handleAvatarChange}
                  entityName={formData.name}
                  showCustomNotification={showCustomNotification}
                />
              </div>
            </div>
            <div className="form-group">
              <label>Location Documents</label>
              <FileUpload
                entityType="locations"
                entityId={entity?.id || 'temp'}
                onFileUpload={() => fetchFiles && fetchFiles()}
                showCustomNotification={showCustomNotification}
              />
              <FileDisplay
                entityType="locations"
                entityId={entity?.id || 'temp'}
                showCustomNotification={showCustomNotification}
              />
            </div>
          </>
        );

      case 'providers':
        return (
          <>
            <div className="form-group">
              <label>Provider Name *</label>
              <input
                type="text"
                value={formData.name || ''}
                onChange={(e) => handleChange('name', e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Company Name *</label>
              <input
                type="text"
                value={formData.company_name || ''}
                onChange={(e) => handleChange('company_name', e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Contact Person *</label>
              <input
                type="text"
                value={formData.contact_person || ''}
                onChange={(e) => handleChange('contact_person', e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>📧 Email *</label>
              <input
                type="email"
                value={formData.email || ''}
                onChange={(e) => handleChange('email', e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>📞 Phone *</label>
              <input
                type="tel"
                value={formData.phone || ''}
                onChange={(e) => handleChange('phone', e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Address *</label>
              <input
                type="text"
                value={formData.address || ''}
                onChange={(e) => handleChange('address', e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Website</label>
              <input
                type="url"
                value={formData.website || ''}
                onChange={(e) => handleChange('website', e.target.value)}
              />
            </div>
            <div className="form-group">
              <label>Provider Logo</label>
              <div className="avatar-section">
                <AvatarUpload
                  entityType="providers"
                  entityId={entity?.id || 'temp'}
                  currentAvatar={avatar}
                  onAvatarChange={handleAvatarChange}
                  showCustomNotification={showCustomNotification}
                />
              </div>
              <div className="form-group">
                <label>Custom Avatar Editor</label>
                <CustomAvatarEditor
                  entityType="providers"
                  entityId={entity?.id || 'temp'}
                  currentAvatar={avatar}
                  onAvatarChange={handleAvatarChange}
                  entityName={formData.name}
                  showCustomNotification={showCustomNotification}
                />
              </div>
            </div>
            <div className="form-group">
              <label>Provider Documents</label>
              <FileUpload
                entityType="providers"
                entityId={entity?.id || 'temp'}
                onFileUpload={() => fetchFiles && fetchFiles()}
                showCustomNotification={showCustomNotification}
              />
              <FileDisplay
                entityType="providers"
                entityId={entity?.id || 'temp'}
                showCustomNotification={showCustomNotification}
              />
            </div>
          </>
        );
      case 'cabinets':
        return (
          <>
            <div className="form-group">
              <label>Name *</label>
              <input
                type="text"
                value={formData.name || ''}
                onChange={(e) => handleChange('name', e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Model</label>
              <input
                type="text"
                value={formData.model || ''}
                onChange={(e) => handleChange('model', e.target.value)}
                placeholder="Optional model name"
              />
            </div>
            <div className="form-group">
              <label>Provider *</label>
              <select
                value={formData.provider_id || ''}
                onChange={(e) => handleChange('provider_id', e.target.value)}
                required
              >
                <option value="">Select Provider</option>
                {providers.map(provider => (
                  <option key={provider.id} value={provider.id}>{provider.name}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Cabinet Logo</label>
              <div className="avatar-section">
                <AvatarUpload
                  entityType="cabinets"
                  entityId={entity?.id || 'temp'}
                  currentAvatar={avatar}
                  onAvatarChange={handleAvatarChange}
                  showCustomNotification={showCustomNotification}
                />
              </div>
            </div>
            <div className="form-group">
              <label>Custom Avatar Editor</label>
              <CustomAvatarEditor
                entityType="cabinets"
                entityId={entity?.id || 'temp'}
                currentAvatar={avatar}
                onAvatarChange={handleAvatarChange}
                entityName={formData.name}
                showCustomNotification={showCustomNotification}
              />
            </div>
            <div className="form-group">
              <label>Cabinet Documents</label>
              <FileUpload
                entityType="cabinets"
                entityId={entity?.id || 'temp'}
                onFileUpload={() => fetchFiles && fetchFiles()}
                showCustomNotification={showCustomNotification}
              />
              <FileDisplay
                entityType="cabinets"
                entityId={entity?.id || 'temp'}
                showCustomNotification={showCustomNotification}
              />
            </div>
          </>
        );
      case 'slots':
        return (
          <>
            {/* Section 1: Basic Information */}
            <div style={{ 
              backgroundColor: 'var(--background-secondary)', 
              padding: '20px', 
              borderRadius: '8px', 
              marginBottom: '20px',
              border: '1px solid var(--border-color)'
            }}>
              <h3 style={{ 
                margin: '0 0 20px 0', 
                color: 'var(--text-primary)', 
                fontSize: '16px',
                fontWeight: '600',
                borderBottom: '2px solid var(--accent-color)',
                paddingBottom: '8px'
              }}>
                📋 Basic Information
              </h3>
              
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
                {/* Left Column - Basic Info */}
                <div>
                  <div className="form-group">
                    <label>Provider *</label>
                    <select
                      value={formData.provider_id || ''}
                      onChange={(e) => handleChange('provider_id', e.target.value)}
                      required
                    >
                      <option value="">Select Provider</option>
                      {providers.map(provider => (
                        <option key={provider.id} value={provider.id}>{provider.name}</option>
                      ))}
                    </select>
                  </div>
                  
                  <div className="form-group">
                    <label>Game Mix *</label>
                    <select
                      value={formData.game_mix_id || ''}
                      onChange={(e) => handleChange('game_mix_id', e.target.value)}
                      required
                    >
                      <option value="">Select Game Mix</option>
                      {gameMixes
                        .filter(mix => {
                          if (!formData.provider_id) return true;
                          return mix.provider_id === formData.provider_id;
                        })
                        .map(mix => {
                          const provider = providers.find(p => p.id === mix.provider_id);
                          return (
                            <option key={mix.id} value={mix.id}>
                              {mix.name} ({provider ? provider.name : 'Unknown Provider'})
                            </option>
                          );
                        })}
                    </select>
                  </div>
                  
                  <div className="form-group">
                    <label>Cabinet *</label>
                    <select
                      value={formData.cabinet_id || ''}
                      onChange={(e) => handleChange('cabinet_id', e.target.value)}
                      required
                    >
                      <option value="">Select Cabinet</option>
                      {cabinets
                        .filter(cabinet => {
                          if (!formData.provider_id) return true;
                          return cabinet.provider_id === formData.provider_id;
                        })
                        .map(cabinet => {
                          const provider = providers.find(p => p.id === cabinet.provider_id);
                          return (
                            <option key={cabinet.id} value={cabinet.id}>
                              {cabinet.name} ({provider ? provider.name : 'Unknown Provider'})
                            </option>
                          );
                        })}
                    </select>
                  </div>
                </div>
                
                {/* Right Column - Basic Info */}
                <div>
                  <div className="form-group">
                    <label>Serial Number *</label>
                    <input
                      type="text"
                      value={formData.serial_number || ''}
                      onChange={(e) => handleChange('serial_number', e.target.value)}
                      required

                    />

                  </div>
                  
                  <div className="form-group">
                    <label>Model *</label>
                    <input
                      type="text"
                      value={formData.model || ''}
                      readOnly
                      required

                    />

                  </div>
                  
                  <div className="form-group">
                    <label>Location *</label>
                    <select
                      value={formData.location_id || ''}
                      onChange={(e) => handleChange('location_id', e.target.value)}
                      required
                    >
                      <option value="">All Locations</option>
                      {locations.map(location => (
                        <option key={location.id} value={location.id}>{location.name}</option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Section 2: Ownership & Documentation */}
            <div style={{ 
              backgroundColor: 'var(--background-secondary)', 
              padding: '20px', 
              borderRadius: '8px', 
              marginBottom: '20px',
              border: '1px solid var(--border-color)'
            }}>
              <h3 style={{ 
                margin: '0 0 20px 0', 
                color: 'var(--text-primary)', 
                fontSize: '16px',
                fontWeight: '600',
                borderBottom: '2px solid var(--accent-color)',
                paddingBottom: '8px'
              }}>
                📄 Ownership & Documentation
              </h3>
              
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
                <div className="form-group">
                  <label>Ownership Type *</label>
                  <select
                    value={formData.ownership_type || ''}
                    onChange={(e) => handleChange('ownership_type', e.target.value)}
                    required
                  >
                    <option value="">Select Ownership Type</option>
                    <option value="property">Property (Owned)</option>
                    <option value="rent">Rent (Leased)</option>
                  </select>
                </div>
                
                <div className="form-group">
                  <label>Owner Company</label>
                  <select
                    value={formData.ownership_type === 'rent' ? 
                      (providers.find(p => p.id === formData.lease_provider_id)?.name || '') : 
                      (companies.find(c => c.id === formData.owner_company_id)?.name || '')}
                    onChange={(e) => {
                      const selectedName = e.target.value;
                      if (formData.ownership_type === 'rent') {
                        const provider = providers.find(p => p.name === selectedName);
                        handleChange('lease_provider_id', provider?.id || '');
                      } else {
                        const company = companies.find(c => c.name === selectedName);
                        handleChange('owner_company_id', company?.id || '');
                      }
                    }}
                  >
                    <option value="">Select {formData.ownership_type === 'rent' ? 'Provider' : 'Company'}</option>
                    {formData.ownership_type === 'rent' 
                      ? providers.map(provider => (
                          <option key={provider.id} value={provider.name}>
                            {provider.name}
                          </option>
                        ))
                      : companies.map(company => (
                          <option key={company.id} value={company.name}>
                            {company.name}
                          </option>
                        ))
                    }
                  </select>
                </div>
              </div>
              
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginTop: '20px' }}>
                <div className="form-group">
                  <label>Invoice Number</label>
                  <select
                    value={formData.invoice_number || ''}
                    onChange={(e) => handleChange('invoice_number', e.target.value)}
                  >
                    <option value="">Select Invoice</option>
                    {invoices.map(invoice => (
                      <option key={invoice.id} value={invoice.invoice_number}>
                        {invoice.invoice_number} - {invoice.amount}€ ({invoice.serial_numbers})
                      </option>
                    ))}
                  </select>
                </div>
                
                <div className="form-group">
                  <label>Commission Date</label>
                  <Calendar
                    value={formData.commission_date}
                    onChange={(date) => handleChange('commission_date', date)}
                    placeholder="Select commission date"
                  />
                </div>
              </div>
              
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginTop: '20px' }}>
                <div className="form-group">
                  <label>CVT End Date</label>
                  <Calendar
                    value={formData.cvt_end_date}
                    onChange={(date) => handleChange('cvt_end_date', date)}
                    placeholder="Select CVT end date"
                  />
                </div>
                
                <div className="form-group">
                  <label>Jackpot Name</label>
                  <input
                    type="text"
                    value={formData.jackpot_name || ''}
                    onChange={(e) => handleChange('jackpot_name', e.target.value)}
                    placeholder="Enter jackpot name"
                  />
                </div>
              </div>
            </div>
            
            {/* Section 3: Financial & Technical Details */}
            <div style={{ 
              backgroundColor: 'var(--background-secondary)', 
              padding: '20px', 
              borderRadius: '8px', 
              marginBottom: '20px',
              border: '1px solid var(--border-color)'
            }}>
              <h3 style={{ 
                margin: '0 0 20px 0', 
                color: 'var(--text-primary)', 
                fontSize: '16px',
                fontWeight: '600',
                borderBottom: '2px solid var(--accent-color)',
                paddingBottom: '8px'
              }}>
                💰 Financial & Technical Details
              </h3>
              
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '20px' }}>
                <div className="form-group">
                  <label>Denomination (€) *</label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.denomination || ''}
                    onChange={(e) => handleChange('denomination', parseFloat(e.target.value))}
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label>Max Bet (€) *</label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.max_bet || ''}
                    onChange={(e) => handleChange('max_bet', parseFloat(e.target.value))}
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label>RTP (%) *</label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.rtp || ''}
                    onChange={(e) => handleChange('rtp', parseFloat(e.target.value))}
                    required
                  />
                </div>
              </div>
              
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginTop: '20px' }}>
                <div className="form-group">
                  <label>Production Year *</label>
                  <input
                    type="number"
                    min="1980"
                    max={new Date().getFullYear()}
                    value={formData.production_year || ''}
                    onChange={(e) => handleChange('production_year', parseInt(e.target.value))}
                    required

                  />
                </div>
                
                <div className="form-group">
                  <label>Gaming Places *</label>
                  <input
                    type="number"
                    value={formData.gaming_places || ''}
                    onChange={(e) => handleChange('gaming_places', parseInt(e.target.value))}
                    required
                  />
                </div>
              </div>
            </div>
            
            {/* Section 4: Avatar & Documents */}
            <div style={{ 
              backgroundColor: 'var(--background-secondary)', 
              padding: '20px', 
              borderRadius: '8px',
              border: '1px solid var(--border-color)'
            }}>
              <h3 style={{ 
                margin: '0 0 20px 0', 
                color: 'var(--text-primary)', 
                fontSize: '16px',
                fontWeight: '600',
                borderBottom: '2px solid var(--accent-color)',
                paddingBottom: '8px'
              }}>
                🖼️ Avatar & Documents
              </h3>
              
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '20px' }}>
                <div className="form-group">
                  <label>Slot Machine Avatar</label>
                  <div className="avatar-section">
                    <AvatarUpload
                      entityType="slots"
                      entityId={entity?.id || 'temp'}
                      currentAvatar={avatar}
                      onAvatarChange={handleAvatarChange}
                      showCustomNotification={showCustomNotification}
                    />
                  </div>
                </div>
                
                <div className="form-group">
                  <label>Custom Avatar Editor</label>
                  <CustomAvatarEditor
                    entityType="slots"
                    entityId={entity?.id || 'temp'}
                    currentAvatar={avatar}
                    onAvatarChange={handleAvatarChange}
                    entityName={formData.serial_number}
                    showCustomNotification={showCustomNotification}
                  />
                </div>
                
                <div className="form-group">
                  <label>Slot Machine Documents</label>
                  <FileUpload
                    entityType="slots"
                    entityId={entity?.id || 'temp'}
                    onFileUpload={() => fetchFiles && fetchFiles()}
                    showCustomNotification={showCustomNotification}
                  />
                  <FileDisplay
                    entityType="slots"
                    entityId={entity?.id || 'temp'}
                    showCustomNotification={showCustomNotification}
                  />
                </div>
              </div>
            </div>
          </>
        );

      case 'gamemixes':
        return (
          <>
            <div className="form-group">
              <label>Mix Name *</label>
              <input
                type="text"
                value={formData.name || ''}
                onChange={(e) => handleChange('name', e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Description *</label>
              <textarea
                value={formData.description || ''}
                onChange={(e) => handleChange('description', e.target.value)}
                required
                rows="3"
              />
            </div>
            <div className="form-group">
              <label>Provider *</label>
              <select
                value={formData.provider_id || ''}
                onChange={(e) => handleChange('provider_id', e.target.value)}
                required
              >
                <option value="">Select Provider</option>
                {providers.map(provider => (
                  <option key={provider.id} value={provider.id}>{provider.name}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Games (one per line) *</label>
              <textarea
                value={(formData.games || []).join('\n')}
                onChange={(e) => handleGamesChange(e.target.value)}
                required
                rows="8"
                placeholder="Enter game names, one per line"
              />
            </div>
            <div className="form-group">
              <label>Game Mix Avatar</label>
              <div className="avatar-section">
                <AvatarUpload
                  entityType="game_mixes"
                  entityId={entity?.id || 'temp'}
                  currentAvatar={avatar}
                  onAvatarChange={handleAvatarChange}
                  showCustomNotification={showCustomNotification}
                />
              </div>
              <div className="form-group">
                <label>Custom Avatar Editor</label>
                <CustomAvatarEditor
                  entityType="game_mixes"
                  entityId={entity?.id || 'temp'}
                  currentAvatar={avatar}
                  onAvatarChange={handleAvatarChange}
                  entityName={formData.name}
                  showCustomNotification={showCustomNotification}
                />
              </div>
            </div>
            <div className="form-group">
              <label>Game Mix Documents</label>
              <FileUpload
                entityType="game_mixes"
                entityId={entity?.id || 'temp'}
                onFileUpload={() => fetchFiles && fetchFiles()}
                showCustomNotification={showCustomNotification}
              />
              <FileDisplay
                entityType="game_mixes"
                entityId={entity?.id || 'temp'}
                showCustomNotification={showCustomNotification}
              />
            </div>
          </>
        );

      case 'invoices':
        return (
          <>
            <div className="form-group">
              <label>Invoice Number *</label>
              <input
                type="text"
                value={formData.invoice_number || ''}
                onChange={(e) => handleChange('invoice_number', e.target.value)}
                required
                placeholder="e.g., INV-2025-001"
              />
            </div>
            <div className="form-group">
              <label>Company *</label>
              <select
                value={formData.company_id || ''}
                onChange={(e) => handleChange('company_id', e.target.value)}
                required
              >
                <option value="">Select Company</option>
                {companies.map(company => (
                  <option key={company.id} value={company.id}>{company.name}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Location *</label>
              <select
                value={formData.location_id || ''}
                onChange={(e) => handleChange('location_id', e.target.value)}
                required
              >
                <option value="">All Locations</option>
                {locations.map(location => (
                  <option key={location.id} value={location.id}>{location.name}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Customer</label>
              <select
                value={formData.buyer_id || ''}
                onChange={(e) => handleChange('buyer_id', e.target.value)}
              >
                <option value="">Select Customer (Company)</option>
                {companies.map(company => (
                  <option key={company.id} value={company.id}>{company.name}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Seller</label>
              <select
                value={formData.seller_id || ''}
                onChange={(e) => handleChange('seller_id', e.target.value)}
              >
                <option value="">Select Seller (Provider)</option>
                {providers.map(provider => (
                  <option key={provider.id} value={provider.id}>{provider.name}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Transaction Type</label>
              <select
                value={formData.transaction_type || ''}
                onChange={(e) => handleChange('transaction_type', e.target.value)}
              >
                <option value="">Select Transaction Type</option>
                <option value="rent">Rent</option>
                <option value="buy">Buy</option>
                <option value="sell">Sell</option>
              </select>
            </div>
            <div className="form-group">
              <label>Serial Numbers *</label>
              <input
                type="text"
                value={formData.serial_numbers || ''}
                onChange={(e) => handleChange('serial_numbers', e.target.value)}
                required
                placeholder="e.g., SER001 SER002 SER003 (space separated)"
              />
              <small className="field-help">Enter one or multiple serial numbers separated by spaces</small>
            </div>
            <div className="form-group">
              <label>Issue Date *</label>
              <Calendar
                value={formData.issue_date}
                onChange={(date) => handleChange('issue_date', date)}
                placeholder="Select issue date"
              />
            </div>
            <div className="form-group">
              <label>Due Date *</label>
              <Calendar
                value={formData.due_date}
                onChange={(date) => handleChange('due_date', date)}
                placeholder="Select due date"
              />
            </div>
            <div className="form-group">
              <label>Amount (€) *</label>
              <input
                type="number"
                step="0.01"
                value={formData.amount || ''}
                onChange={(e) => handleChange('amount', parseFloat(e.target.value))}
                required
                placeholder="0.00"
              />
            </div>
            <div className="form-group">
              <label>Currency</label>
              <select
                value={formData.currency || 'EUR'}
                onChange={(e) => handleChange('currency', e.target.value)}
              >
                <option value="EUR">EUR (€)</option>
                <option value="RON">RON (Lei)</option>
                <option value="USD">USD ($)</option>
              </select>
            </div>
            <div className="form-group">
              <label>Status</label>
              <select
                value={formData.status || 'pending'}
                onChange={(e) => handleChange('status', e.target.value)}
              >
                <option value="pending">Pending</option>
                <option value="paid">Paid</option>
                <option value="overdue">Overdue</option>
              </select>
            </div>
            <div className="form-group">
              <label>Description *</label>
              <textarea
                value={formData.description || ''}
                onChange={(e) => handleChange('description', e.target.value)}
                required
                rows="3"
                placeholder="Invoice description or notes"
              />
            </div>
          </>
        );
      case 'metrology':
        return (
          <>
            <div className="form-group">
              <label>Serial Numbers *</label>
              <textarea 
                value={formData.serial_number || ''} 
                onChange={(e) => handleChange('serial_number', e.target.value)} 
                required 
                placeholder="Enter serial numbers separated by space (e.g., 188686 2547364 100393)"
                rows="3"
              />
            </div>
            <div className="form-group">
              <label>Certificate Number *</label>
              <input type="text" value={formData.certificate_number || ''} onChange={(e) => handleChange('certificate_number', e.target.value)} required />
            </div>
            <div className="form-group">
              <label>Certificate Type *</label>
              <select value={formData.certificate_type || ''} onChange={(e) => handleChange('certificate_type', e.target.value)} required>
                <option value="">Select Type</option>
                <option value="calibration">Calibration</option>
                <option value="verification">Verification</option>
                <option value="certification">Certification</option>
              </select>
            </div>
            <div className="form-group">
              <label>Issue Date *</label>
              <Calendar value={formData.issue_date} onChange={(date) => handleChange('issue_date', date)} />
            </div>
            <div className="form-group">
              <label>Expiry Date *</label>
              <Calendar value={formData.expiry_date} onChange={(date) => handleChange('expiry_date', date)} />
            </div>
            <div className="form-group">
              <label>Calibration Interval (months) *</label>
              <input 
                type="number" 
                            value=""
            onChange={(e) => {}} 
                required 
                min="1" 
                max="60" 
              />
            </div>
            
            <div className="form-group">
              <label>Issuing Authority *</label>
              <select value={formData.issuing_authority || ''} onChange={(e) => handleChange('issuing_authority', e.target.value)} required>
                <option value="">Select Issuing Authority</option>
                <option value="BRML">BRML</option>
                <option value="BMM">BMM</option>
                <option value="METRON">METRON</option>
                <option value="INSPECTION SLOT">INSPECTION SLOT</option>
                <option value="RMC">RMC</option>
              </select>
            </div>


            <div className="form-group">
              <label>CVT Type</label>
              <select value={formData.cvt_type || ''} onChange={(e) => handleChange('cvt_type', e.target.value)}>
                <option value="">Select CVT Type</option>
                <option value="initial">Initial</option>
                <option value="periodic">Periodic</option>
                <option value="reparation">Reparation</option>
              </select>
            </div>
            <div className="form-group">
              <label>CVT End Date</label>
              <Calendar value={formData.cvt_expiry_date} onChange={(date) => handleChange('cvt_expiry_date', date)} />
            </div>
            <div className="form-group">
              <label>Description *</label>
              <textarea value={formData.description || ''} onChange={(e) => handleChange('description', e.target.value)} required rows="3" />
            </div>
            <div className="form-group">
              <label>Metrology Documents</label>
              <FileUpload 
                entityType="metrology" 
                entityId={entity?.id || 'temp'} 
                onFileUpload={() => fetchFiles && fetchFiles()} 
                showCustomNotification={showCustomNotification} 
              />
              <FileDisplay 
                entityType="metrology" 
                entityId={entity?.id || 'temp'} 
                showCustomNotification={showCustomNotification} 
              />
            </div>
          </>
        );

      case 'metrology2':
        return (
          <>
            <div className="form-group">
              <label>Serial Numbers *</label>
              <textarea 
                value={formData.serial_number || ''} 
                onChange={(e) => handleChange('serial_number', e.target.value)} 
                required 
                placeholder="Enter serial numbers separated by space (e.g., 188686 2547364 100393)"
                rows="3"
              />
            </div>
            <div className="form-group">
              <label>Certificate Number *</label>
              <input type="text" value={formData.certificate_number || ''} onChange={(e) => handleChange('certificate_number', e.target.value)} required />
            </div>
            <div className="form-group">
              <label>Issue Date *</label>
              <Calendar value={formData.issue_date} onChange={(date) => handleChange('issue_date', date)} />
            </div>
            
            <div className="form-group">
              <label>Issuing Authority *</label>
              <select value={formData.issuing_authority || ''} onChange={(e) => handleChange('issuing_authority', e.target.value)} required>
                <option value="">Select Issuing Authority</option>
                <option value="BRML">BRML</option>
                <option value="BMM">BMM</option>
                <option value="METRON">METRON</option>
                <option value="INSPECTION SLOT">INSPECTION SLOT</option>
                <option value="RMC">RMC</option>
              </select>
            </div>


            <div className="form-group">
              <label>CVT Type</label>
              <select value={formData.cvt_type || ''} onChange={(e) => handleChange('cvt_type', e.target.value)}>
                <option value="">Select CVT Type</option>
                <option value="initial">Initial</option>
                <option value="periodic">Periodic</option>
                <option value="reparation">Reparation</option>
              </select>
            </div>
            <div className="form-group">
              <label>CVT End Date</label>
              <Calendar value={formData.cvt_expiry_date} onChange={(date) => handleChange('cvt_expiry_date', date)} />
            </div>
            <div className="form-group">
              <label>Description *</label>
              <textarea value={formData.description || ''} onChange={(e) => handleChange('description', e.target.value)} required rows="3" />
            </div>
            <div className="form-group">
              <label>Metrology Documents</label>
              <FileUpload 
                entityType="metrology" 
                entityId={entity?.id || 'temp'} 
                onFileUpload={() => fetchFiles && fetchFiles()} 
                showCustomNotification={showCustomNotification} 
              />
              <FileDisplay 
                entityType="metrology" 
                entityId={entity?.id || 'temp'} 
                showCustomNotification={showCustomNotification} 
              />
            </div>
          </>
        );

      case 'jackpots':
        return (
          <>
            <div className="form-group">
              <label>Serial Number *</label>
              <input
                type="text"
                value={formData.serial_number || ''}
                onChange={(e) => handleChange('serial_number', e.target.value)}
                placeholder="Enter slot machine serial number"
                required
              />
            </div>
            <div className="form-group">
              <label>Jackpot Name *</label>
              <input
                type="text"
                value={formData.jackpot_name || ''}
                onChange={(e) => handleChange('jackpot_name', e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Jackpot Type *</label>
              <select
                value={formData.jackpot_type || 'progressive'}
                onChange={(e) => handleChange('jackpot_type', e.target.value)}
                required
              >
                <option value="progressive">Progressive</option>
                <option value="fixed">Fixed</option>
                <option value="mystery">Mystery</option>
              </select>
            </div>
                          <div className="form-group">
                <label>Increment Rate (%) *</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.increment_rate || 0.1}
                  onChange={(e) => handleChange('increment_rate', parseFloat(e.target.value))}
                  required
                />
              </div>
              <div className="form-group">
                <label>Level 1</label>
                <input
                  type="text"
                  value={formData.level_1 || ''}
                  onChange={(e) => handleChange('level_1', e.target.value)}
                  placeholder="e.g., 111-222"
                />
              </div>
              <div className="form-group">
                <label>Level 2</label>
                <input
                  type="text"
                  value={formData.level_2 || ''}
                  onChange={(e) => handleChange('level_2', e.target.value)}
                  placeholder="e.g., 222-333"
                />
              </div>
              <div className="form-group">
                <label>Level 3</label>
                <input
                  type="text"
                  value={formData.level_3 || ''}
                  onChange={(e) => handleChange('level_3', e.target.value)}
                  placeholder="e.g., 333-555"
                />
              </div>
              <div className="form-group">
                <label>Level 4</label>
                <input
                  type="text"
                  value={formData.level_4 || ''}
                  onChange={(e) => handleChange('level_4', e.target.value)}
                  placeholder="e.g., 555-888"
                />
              </div>
              <div className="form-group">
                <label>Level 5</label>
                <input
                  type="text"
                  value={formData.level_5 || ''}
                  onChange={(e) => handleChange('level_5', e.target.value)}
                  placeholder="e.g., 888-999"
                />
              </div>
            <div className="form-group">
              <label>Description *</label>
              <textarea
                value={formData.description || ''}
                onChange={(e) => handleChange('description', e.target.value)}
                rows="3"
                placeholder="Additional details about the jackpot"
                required
              />
            </div>
          </>
        );

      case 'comision_date':
        return (
          <>
            <div className="form-group">
              <label>📝 Event Name *</label>
              <input
                type="text"
                value={formData.event_name || ''}
                onChange={(e) => handleChange('event_name', e.target.value)}
                placeholder="Enter event name (e.g., COM-001, Summer Event, etc.)"
                required
              />
              <small style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>
                Enter a descriptive name for this commission event
              </small>
            </div>
            <div className="form-group">
              <label>📅 Commission Date *</label>
              <Calendar
                value={formData.commission_date || ''}
                onChange={(value) => handleChange('commission_date', value)}
                placeholder="Select commission date"
              />
            </div>
            <div className="form-group">
              <label>🔢 Serial Numbers *</label>
              <textarea
                value={formData.serial_numbers || ''}
                onChange={(e) => handleChange('serial_numbers', e.target.value)}
                rows="4"
                placeholder="Enter serial numbers separated by spaces (e.g., SN001 SN002 SN003)"
                required
              />
              <small style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>
                Enter one or more serial numbers separated by spaces
              </small>
            </div>
          </>
        );

      default:
        return <div>Form not implemented for {entityType}</div>;
    }
  };

  const getTitle = () => {
    const titles = {
      companies: 'Company',
      locations: 'Location',
      providers: 'Provider',
      cabinets: 'Cabinet',
      slots: 'Slot Machine',
      gamemixes: 'Game Mix',
      invoices: 'Invoice',
      onjn: 'ONJN Report',
      legal: 'Legal Document',
      metrology: 'Metrology',
      jackpots: 'Jackpot',
      comision_date: 'Comision Date'
    };
    return titles[entityType] || 'Entity';
  };

  return (
    <div className="user-edit-modal">
      <div className="modal-backdrop" onClick={onClose}></div>
      <div className="modal-content">
        <div className="modal-header">
          <h2>{entity ? `Edit ${getTitle()}` : `Create ${getTitle()}`}</h2>
          <button className="modal-close" onClick={onClose}>✕</button>
        </div>

        <form onSubmit={handleSubmit} className="user-form">
          <div className="form-section">
            <div className="form-grid">
              {renderFormFields()}
            </div>
          </div>

          <div className="form-actions">
            <button type="button" onClick={onClose} className="btn-cancel">
              Cancel
            </button>
            <button type="submit" className="btn-save">
              {entity ? `Update ${getTitle()}` : `Create ${getTitle()}`}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
// User Edit Form Component
const UserEditForm = ({ user, onSave, onClose, companies, locations, showCustomNotification }) => {
  const [formData, setFormData] = useState({
    username: user?.username || '',
    email: user?.email || '',
    phone: user?.phone || '',
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    role: user?.role || 'operator',
    password: '',
    is_active: user?.is_active !== false,
    assigned_locations: user?.assigned_locations || [],
    permissions: {
      modules: {
        dashboard: true,
        companies: true,
        locations: true,
        providers: true,
        cabinets: true,
        game_mixes: true,
        slot_machines: true,
        invoices: true,
        onjn_reports: true,
        legal_documents: true,
        metrology: true,
        jackpots: true,
        users: true
      },
      actions: {
        companies: { create: true, read: true, update: true, delete: true },
        locations: { create: true, read: true, update: true, delete: true },
        providers: { create: true, read: true, update: true, delete: true },
        cabinets: { create: true, read: true, update: true, delete: true },
        game_mixes: { create: true, read: true, update: true, delete: true },
        slot_machines: { create: true, read: true, update: true, delete: true },
        invoices: { create: true, read: true, update: true, delete: true },
        onjn_reports: { create: true, read: true, update: true, delete: true },
        legal_documents: { create: true, read: true, update: true, delete: true },
        metrology: { create: true, read: true, update: true, delete: true },
        jackpots: { create: true, read: true, update: true, delete: true },
        users: { create: true, read: true, update: true, delete: true }
      },
      accessible_companies: user?.permissions?.accessible_companies || [],
      accessible_locations: user?.permissions?.accessible_locations || []
    }
  });

  // Avatar state
  const { avatar, setAvatar } = useAvatar('users', user?.id);

  const handleAvatarChange = (newAvatar) => {
    setAvatar(newAvatar);
  };

  useEffect(() => {
    if (user?.permissions) {
      setFormData(prev => ({
        ...prev,
        permissions: {
          modules: { ...prev.permissions.modules, ...user.permissions.modules },
          actions: { ...prev.permissions.actions, ...user.permissions.actions },
          accessible_companies: user.permissions.accessible_companies || [],
          accessible_locations: user.permissions.accessible_locations || []
        }
      }));
    }
  }, [user]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  const handleModuleChange = (module, checked) => {
    setFormData(prev => ({
      ...prev,
      permissions: {
        ...prev.permissions,
        modules: {
          ...prev.permissions.modules,
          [module]: checked
        }
      }
    }));
  };

  const handleActionChange = (module, action, checked) => {
    setFormData(prev => ({
      ...prev,
      permissions: {
        ...prev.permissions,
        actions: {
          ...prev.permissions.actions,
          [module]: {
            ...prev.permissions.actions[module],
            [action]: checked
          }
        }
      }
    }));
  };

  const handleCompanyChange = (companyId, checked) => {
    setFormData(prev => ({
      ...prev,
      permissions: {
        ...prev.permissions,
        accessible_companies: checked 
          ? [...prev.permissions.accessible_companies, companyId]
          : prev.permissions.accessible_companies.filter(id => id !== companyId)
      }
    }));
  };

  const handleLocationChange = (locationId, checked) => {
    setFormData(prev => ({
      ...prev,
      permissions: {
        ...prev.permissions,
        accessible_locations: checked 
          ? [...prev.permissions.accessible_locations, locationId]
          : prev.permissions.accessible_locations.filter(id => id !== locationId)
      },
      assigned_locations: checked 
        ? [...prev.assigned_locations, locationId]
        : prev.assigned_locations.filter(id => id !== locationId)
    }));
  };

  // Select All functions
  const handleSelectAllModules = (checked) => {
    setFormData(prev => ({
      ...prev,
      permissions: {
        ...prev.permissions,
        modules: modules.reduce((acc, module) => {
          acc[module.key] = checked;
          return acc;
        }, {})
      }
    }));
  };

  const handleSelectAllActions = (checked) => {
    setFormData(prev => ({
      ...prev,
      permissions: {
        ...prev.permissions,
        actions: modules.filter(m => m.key !== 'dashboard').reduce((acc, module) => {
          acc[module.key] = actions.reduce((actionAcc, action) => {
            actionAcc[action.key] = checked;
            return actionAcc;
          }, {});
          return acc;
        }, {})
      }
    }));
  };

  const handleSelectAllCompanies = (checked) => {
    setFormData(prev => ({
      ...prev,
      permissions: {
        ...prev.permissions,
        accessible_companies: checked ? companies.map(c => c.id) : []
      }
    }));
  };

  const handleSelectAllLocations = (checked) => {
    setFormData(prev => ({
      ...prev,
      permissions: {
        ...prev.permissions,
        accessible_locations: checked ? locations.map(l => l.id) : []
      }
    }));
  };

  const modules = [
    { key: 'dashboard', label: 'Dashboard', icon: '📊' },
    { key: 'companies', label: 'Companies', icon: '🏢' },
    { key: 'locations', label: 'Locations', icon: '📍' },
    { key: 'providers', label: 'Providers', icon: '🎮' },
    { key: 'cabinets', label: 'Cabinets', icon: '🎰' },
    { key: 'game_mixes', label: 'Game Mixes', icon: '🎲' },
    { key: 'slot_machines', label: 'Slot Machines', icon: '🎯' },
    { key: 'invoices', label: 'Invoices', icon: '💰' },
    { key: 'onjn_reports', label: 'ONJN Reports', icon: '📋' },
    { key: 'legal_documents', label: 'Legal Documents', icon: '📄' },
    { key: 'users', label: 'Users', icon: '👥' }
  ];

  const actions = [
    { key: 'create', label: 'Create', icon: '➕' },
    { key: 'read', label: 'Read', icon: '👁️' },
    { key: 'update', label: 'Update', icon: '✏️' },
    { key: 'delete', label: 'Delete', icon: '🗑️' }
  ];
  return (
    <div className="user-edit-modal">
      <div className="modal-backdrop" onClick={onClose}></div>
      <div className="modal-content">
        <div className="modal-header">
          <h2>{user ? 'Edit User' : 'Create User'}</h2>
          <button className="modal-close" onClick={onClose}>✕</button>
        </div>

        <form onSubmit={handleSubmit} className="user-form">
          {/* Basic User Information */}
          <div className="form-section">
            <h3>User Information</h3>
            <div className="form-grid">
              <div className="form-group">
                <label>Username</label>
                <input
                  type="text"
                  value={formData.username}
                  onChange={(e) => setFormData(prev => ({ ...prev, username: e.target.value }))}
                  required
                />
              </div>
              <div className="form-group">
                <label>📧 Email</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
                  required
                />
              </div>
              <div className="form-group">
                <label>📞 Phone</label>
                <input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => setFormData(prev => ({ ...prev, phone: e.target.value }))}
                  placeholder="Enter phone number"
                />
              </div>
              <div className="form-group">
                <label>First Name</label>
                <input
                  type="text"
                  value={formData.first_name}
                  onChange={(e) => setFormData(prev => ({ ...prev, first_name: e.target.value }))}
                  placeholder="Enter first name"
                />
              </div>
              <div className="form-group">
                <label>Last Name</label>
                <input
                  type="text"
                  value={formData.last_name}
                  onChange={(e) => setFormData(prev => ({ ...prev, last_name: e.target.value }))}
                  placeholder="Enter last name"
                />
              </div>
              <div className="form-group">
                <label>Role</label>
                <select
                  value={formData.role}
                  onChange={(e) => setFormData(prev => ({ ...prev, role: e.target.value }))}
                >
                  <option value="admin">Admin</option>
                  <option value="manager">Manager</option>
                  <option value="operator">Operator</option>
                </select>
              </div>
              <div className="form-group">
                <label>Password {user && '(leave empty to keep current)'}</label>
                <input
                  type="password"
                  value={formData.password}
                  onChange={(e) => setFormData(prev => ({ ...prev, password: e.target.value }))}
                  placeholder={user ? "Leave empty to keep current" : "Enter password"}
                />
              </div>
            </div>
            <div className="form-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={formData.is_active}
                  onChange={(e) => setFormData(prev => ({ ...prev, is_active: e.target.checked }))}
                />
                Active User
              </label>
            </div>
          </div>

          {/* Avatar Upload Section */}
          {user && (
            <div className="form-section">
              <h3>Profile Avatar</h3>
              <div className="avatar-section">
                <AvatarUpload
                  entityType="users"
                  entityId={user.id}
                  currentAvatar={avatar}
                  onAvatarChange={handleAvatarChange}
                  showCustomNotification={showCustomNotification}
                />
              </div>
            </div>
          )}

          {/* Module Access */}
          <div className="form-section">
            <h3>Module Access</h3>
            <div className="select-all-row">
              <label className="checkbox-label select-all-label">
                <input
                  type="checkbox"
                  checked={modules.every(module => formData.permissions.modules[module.key])}
                  onChange={(e) => handleSelectAllModules(e.target.checked)}
                />
                <span style={{ fontWeight: 'bold', color: 'var(--accent-color)' }}>Select All Modules</span>
              </label>
            </div>
            <div className="permissions-grid">
              {modules.map(module => (
                <div key={module.key} className="permission-item">
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={formData.permissions.modules[module.key]}
                      onChange={(e) => handleModuleChange(module.key, e.target.checked)}
                    />
                    <span className="module-icon">{module.icon}</span>
                    {module.label}
                  </label>
                </div>
              ))}
            </div>
          </div>

          {/* Action Permissions */}
          <div className="form-section">
            <h3>Action Permissions</h3>
            <div className="select-all-row">
              <label className="checkbox-label select-all-label">
                <input
                  type="checkbox"
                  checked={modules.filter(m => m.key !== 'dashboard').every(module => 
                    actions.every(action => formData.permissions.actions[module.key]?.[action.key])
                  )}
                  onChange={(e) => handleSelectAllActions(e.target.checked)}
                />
                <span style={{ fontWeight: 'bold', color: 'var(--accent-color)' }}>Select All Actions</span>
              </label>
            </div>
            <div className="actions-table">
              <div className="actions-header">
                <div className="module-col">Module</div>
                {actions.map(action => (
                  <div key={action.key} className="action-col">
                    <span className="action-icon">{action.icon}</span>
                    {action.label}
                  </div>
                ))}
              </div>
              {modules.filter(m => m.key !== 'dashboard').map(module => (
                <div key={module.key} className="actions-row">
                  <div className="module-col">
                    <span className="module-icon">{module.icon}</span>
                    {module.label}
                  </div>
                  {actions.map(action => (
                    <div key={action.key} className="action-col">
                      <input
                        type="checkbox"
                        checked={formData.permissions.actions[module.key]?.[action.key] || false}
                        onChange={(e) => handleActionChange(module.key, action.key, e.target.checked)}
                        disabled={!formData.permissions.modules[module.key]}
                      />
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>

          {/* Company Access */}
          <div className="form-section">
            <h3>Company Access</h3>
            <div className="select-all-row">
              <label className="checkbox-label select-all-label">
                <input
                  type="checkbox"
                  checked={companies.every(company => formData.permissions.accessible_companies.includes(company.id))}
                  onChange={(e) => handleSelectAllCompanies(e.target.checked)}
                />
                <span style={{ fontWeight: 'bold', color: 'var(--accent-color)' }}>Select All Companies</span>
              </label>
            </div>
            <div className="access-grid">
              {companies.map(company => (
                <div key={company.id} className="access-item">
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={formData.permissions.accessible_companies.includes(company.id)}
                      onChange={(e) => handleCompanyChange(company.id, e.target.checked)}
                    />
                    🏢 {company.name}
                  </label>
                </div>
              ))}
            </div>
          </div>

          {/* Location Access */}
          <div className="form-section">
            <h3>Location Access</h3>
            <div className="select-all-row">
              <label className="checkbox-label select-all-label">
                <input
                  type="checkbox"
                  checked={locations.every(location => formData.permissions.accessible_locations.includes(location.id))}
                  onChange={(e) => handleSelectAllLocations(e.target.checked)}
                />
                <span style={{ fontWeight: 'bold', color: 'var(--accent-color)' }}>Select All Locations</span>
              </label>
            </div>
            <div className="access-grid">
              {locations.map(location => (
                <div key={location.id} className="access-item">
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={formData.permissions.accessible_locations.includes(location.id)}
                      onChange={(e) => handleLocationChange(location.id, e.target.checked)}
                    />
                    📍 {location.name}
                  </label>
                </div>
              ))}
            </div>
          </div>

          <div className="form-actions">
            <button type="button" onClick={onClose} className="btn-cancel">
              Cancel
            </button>
            <button type="submit" className="btn-save">
              {user ? 'Update User' : 'Create User'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
// Dashboard Component
const ScheduleChangeForm = ({ slot, providers, cabinets, gameMixes, locations, users, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    newStatus: slot.status === 'active' ? 'inactive' : 'active',
    provider_id: slot.provider_id || '',
    game_mix_id: slot.game_mix_id || '',
    cabinet_id: slot.cabinet_id || '',
    model: slot.model || '',
    location_id: slot.location_id || '',
    scheduledDate: new Date().toISOString().split('T')[0],
    scheduledTime: new Date().toLocaleTimeString('en-GB', { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: false 
    })
  });

  // Dacă există modificări programate, să le afișeze
  const existingChanges = slot.existingChanges || [];

  // Auto-fill model when cabinet is selected
  useEffect(() => {
    if (formData.cabinet_id) {
      const selectedCabinet = cabinets.find(cabinet => cabinet.id === formData.cabinet_id);
      if (selectedCabinet && selectedCabinet.model) {
        setFormData(prev => ({
          ...prev,
          model: selectedCabinet.model
        }));
      }
    }
  }, [formData.cabinet_id, cabinets]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const scheduledDateTime = new Date(`${formData.scheduledDate}T${formData.scheduledTime}`).toISOString();
    onSave({
      newStatus: formData.newStatus,
      provider_id: formData.provider_id,
      game_mix_id: formData.game_mix_id,
      cabinet_id: formData.cabinet_id,
      model: formData.model,
      location_id: formData.location_id,
      scheduledDateTime: scheduledDateTime
    });
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Slot Information */}
      <div style={{ 
        backgroundColor: 'var(--bg-secondary)', 
        padding: '16px', 
        borderRadius: '8px',
        border: '1px solid var(--border-color)'
      }}>
        <h3 style={{ margin: '0 0 12px 0', color: 'var(--text-primary)', fontSize: '16px' }}>
          Slot Machine: {slot.serial_number || slot.id}
        </h3>
        <p style={{ margin: '0', color: 'var(--text-secondary)', fontSize: '14px' }}>
          Current Status: <strong style={{ color: 'var(--text-primary)' }}>{slot.status}</strong>
        </p>
      </div>

      {/* Existing Scheduled Changes */}
      {existingChanges.length > 0 && (
        <div style={{ 
          backgroundColor: '#fff3cd', 
          padding: '16px', 
          borderRadius: '8px',
          border: '1px solid #ffeaa7',
          marginBottom: '20px'
        }}>
          <h3 style={{ 
            margin: '0 0 16px 0', 
            color: '#856404', 
            fontSize: '16px',
            fontWeight: '600',
            borderBottom: '2px solid #f39c12',
            paddingBottom: '8px'
          }}>
            ⏰ Existing Scheduled Changes
          </h3>
          {existingChanges.map((change, index) => (
            <div key={change.id} style={{ 
              backgroundColor: 'white', 
              padding: '12px', 
              borderRadius: '6px',
              border: '1px solid #ffeaa7',
              marginBottom: '8px'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <strong style={{ color: '#856404' }}>Change #{index + 1}</strong>
                <span style={{ color: '#856404', fontSize: '12px' }}>
                  Scheduled for: {new Date(change.scheduledDateTime).toLocaleString()}
                </span>
              </div>
              <div style={{ color: '#856404', fontSize: '14px' }}>
                <div style={{ marginBottom: '8px' }}>
                  <strong>Modified by:</strong> {(() => {
                    // Caută utilizatorul complet în lista de utilizatori
                    const user = Array.isArray(users) ? users.find(u => u.username === change.userName) : null;
                    if (user && user.first_name && user.last_name) {
                      return `${user.first_name} ${user.last_name}`;
                    } else if (user && user.username) {
                      return user.username;
                    } else {
                      return change.userName || 'Unknown User';
                    }
                  })()}
                </div>
                
                {/* Tabel cu modificările */}
                <div style={{ 
                  border: '1px solid #dee2e6', 
                  borderRadius: '4px', 
                  overflow: 'hidden',
                  marginTop: '8px'
                }}>
                  <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px' }}>
                    <thead>
                      <tr style={{ backgroundColor: '#f8f9fa', borderBottom: '1px solid #dee2e6' }}>
                        <th style={{ padding: '8px', textAlign: 'left', borderRight: '1px solid #dee2e6', fontWeight: 'bold' }}>Field</th>
                        <th style={{ padding: '8px', textAlign: 'left', borderRight: '1px solid #dee2e6', fontWeight: 'bold' }}>Old Value</th>
                        <th style={{ padding: '8px', textAlign: 'left', fontWeight: 'bold' }}>New Value</th>
                      </tr>
                    </thead>
                    <tbody>
                      {/* Status - Always show */}
                      <tr style={{ borderBottom: '1px solid #f1f3f4' }}>
                        <td style={{ padding: '8px', borderRight: '1px solid #f1f3f4', fontWeight: 'bold' }}>Status</td>
                        <td style={{ padding: '8px', borderRight: '1px solid #f1f3f4' }}>
                          {change.changes?.status?.old || change.oldValue || '-'}
                        </td>
                        <td style={{ padding: '8px' }}>
                          {change.changes?.status?.new || change.newValue || '-'}
                        </td>
                      </tr>
                      
                      {/* Provider - Always show */}
                      <tr style={{ borderBottom: '1px solid #f1f3f4' }}>
                        <td style={{ padding: '8px', borderRight: '1px solid #f1f3f4', fontWeight: 'bold' }}>Provider</td>
                        <td style={{ padding: '8px', borderRight: '1px solid #f1f3f4' }}>
                          {(() => {
                            const providerId = change.changes?.provider_id?.old || change.provider_id?.old;
                            const oldProvider = providers.find(p => p.id === providerId);
                            return oldProvider ? oldProvider.name : (providerId || '-');
                          })()}
                        </td>
                        <td style={{ padding: '8px' }}>
                          {(() => {
                            const providerId = change.changes?.provider_id?.new || change.provider_id?.new;
                            const newProvider = providers.find(p => p.id === providerId);
                            return newProvider ? newProvider.name : (providerId || '-');
                          })()}
                        </td>
                      </tr>
                      
                      {/* Game Mix - Always show */}
                      <tr style={{ borderBottom: '1px solid #f1f3f4' }}>
                        <td style={{ padding: '8px', borderRight: '1px solid #f1f3f4', fontWeight: 'bold' }}>Game Mix</td>
                        <td style={{ padding: '8px', borderRight: '1px solid #f1f3f4' }}>
                          {(() => {
                            const gameMixId = change.changes?.game_mix_id?.old || change.game_mix_id?.old;
                            const oldGameMix = gameMixes.find(g => g.id === gameMixId);
                            return oldGameMix ? oldGameMix.name : (gameMixId || '-');
                          })()}
                        </td>
                        <td style={{ padding: '8px' }}>
                          {(() => {
                            const gameMixId = change.changes?.game_mix_id?.new || change.game_mix_id?.new;
                            const newGameMix = gameMixes.find(g => g.id === gameMixId);
                            return newGameMix ? newGameMix.name : (gameMixId || '-');
                          })()}
                        </td>
                      </tr>
                      
                      {/* Cabinet - Always show */}
                      <tr style={{ borderBottom: '1px solid #f1f3f4' }}>
                        <td style={{ padding: '8px', borderRight: '1px solid #f1f3f4', fontWeight: 'bold' }}>Cabinet</td>
                        <td style={{ padding: '8px', borderRight: '1px solid #f1f3f4' }}>
                          {(() => {
                            const cabinetId = change.changes?.cabinet_id?.old || change.cabinet_id?.old;
                            const oldCabinet = cabinets.find(c => c.id === cabinetId);
                            return oldCabinet ? oldCabinet.name : (cabinetId || '-');
                          })()}
                        </td>
                        <td style={{ padding: '8px' }}>
                          {(() => {
                            const cabinetId = change.changes?.cabinet_id?.new || change.cabinet_id?.new;
                            const newCabinet = cabinets.find(c => c.id === cabinetId);
                            return newCabinet ? newCabinet.name : (cabinetId || '-');
                          })()}
                        </td>
                      </tr>
                      
                      {/* Model - Always show */}
                      <tr style={{ borderBottom: '1px solid #f1f3f4' }}>
                        <td style={{ padding: '8px', borderRight: '1px solid #f1f3f4', fontWeight: 'bold' }}>Model</td>
                        <td style={{ padding: '8px', borderRight: '1px solid #f1f3f4' }}>
                          {change.changes?.model?.old || change.model?.old || '-'}
                        </td>
                        <td style={{ padding: '8px' }}>
                          {change.changes?.model?.new || change.model?.new || '-'}
                        </td>
                      </tr>
                      
                      {/* Location - Always show */}
                      <tr style={{ borderBottom: '1px solid #f1f3f4' }}>
                        <td style={{ padding: '8px', borderRight: '1px solid #f1f3f4', fontWeight: 'bold' }}>Location</td>
                        <td style={{ padding: '8px', borderRight: '1px solid #f1f3f4' }}>
                          {(() => {
                            const locationId = change.changes?.location_id?.old || change.location_id?.old;
                            const oldLocation = locations.find(l => l.id === locationId);
                            return oldLocation ? oldLocation.name : (locationId || '-');
                          })()}
                        </td>
                        <td style={{ padding: '8px' }}>
                          {(() => {
                            const locationId = change.changes?.location_id?.new || change.location_id?.new;
                            const newLocation = locations.find(l => l.id === locationId);
                            return newLocation ? newLocation.name : (locationId || '-');
                          })()}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Basic Fields */}
      <div style={{ 
        backgroundColor: 'var(--bg-secondary)', 
        padding: '16px', 
        borderRadius: '8px',
        border: '1px solid var(--border-color)',
        marginBottom: '20px'
      }}>
        <h3 style={{ 
          margin: '0 0 16px 0', 
          color: 'var(--text-primary)', 
          fontSize: '16px',
          fontWeight: '600',
          borderBottom: '2px solid var(--accent-color)',
          paddingBottom: '8px'
        }}>
          📋 Basic Information
        </h3>
        
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
          {/* Left Column */}
          <div>
            <div className="form-group">
              <label>Provider *</label>
              <select
                value={formData.provider_id}
                onChange={(e) => handleChange('provider_id', e.target.value)}
                required
                style={{
                  width: '100%',
                  padding: '8px',
                  border: '1px solid var(--border-color)',
                  borderRadius: '4px',
                  backgroundColor: 'var(--bg-secondary)',
                  color: 'var(--text-primary)'
                }}
              >
                <option value="">Select Provider</option>
                {providers.map(provider => (
                  <option key={provider.id} value={provider.id}>{provider.name}</option>
                ))}
              </select>
            </div>
            
            <div className="form-group">
              <label>Game Mix *</label>
              <select
                value={formData.game_mix_id}
                onChange={(e) => handleChange('game_mix_id', e.target.value)}
                required
                style={{
                  width: '100%',
                  padding: '8px',
                  border: '1px solid var(--border-color)',
                  borderRadius: '4px',
                  backgroundColor: 'var(--bg-secondary)',
                  color: 'var(--text-primary)'
                }}
              >
                <option value="">Select Game Mix</option>
                {gameMixes
                  .filter(mix => {
                    if (!formData.provider_id) return true;
                    return mix.provider_id === formData.provider_id;
                  })
                  .map(mix => {
                    const provider = providers.find(p => p.id === mix.provider_id);
                    return (
                      <option key={mix.id} value={mix.id}>
                        {mix.name} ({provider ? provider.name : 'Unknown Provider'})
                      </option>
                    );
                  })}
              </select>
            </div>
            
            <div className="form-group">
              <label>Cabinet *</label>
              <select
                value={formData.cabinet_id}
                onChange={(e) => handleChange('cabinet_id', e.target.value)}
                required
                style={{
                  width: '100%',
                  padding: '8px',
                  border: '1px solid var(--border-color)',
                  borderRadius: '4px',
                  backgroundColor: 'var(--bg-secondary)',
                  color: 'var(--text-primary)'
                }}
              >
                <option value="">Select Cabinet</option>
                {cabinets
                  .filter(cabinet => {
                    if (!formData.provider_id) return true;
                    return cabinet.provider_id === formData.provider_id;
                  })
                  .map(cabinet => {
                    const provider = providers.find(p => p.id === cabinet.provider_id);
                    return (
                      <option key={cabinet.id} value={cabinet.id}>
                        {cabinet.name} ({provider ? provider.name : 'Unknown Provider'})
                      </option>
                    );
                  })}
              </select>
            </div>
          </div>
          
          {/* Right Column */}
          <div>
            <div className="form-group">
              <label>Model *</label>
              <input
                type="text"
                value={formData.model}
                onChange={(e) => handleChange('model', e.target.value)}
                required
                placeholder="Auto-filled from selected cabinet"
                style={{
                  width: '100%',
                  padding: '8px',
                  border: '1px solid var(--border-color)',
                  borderRadius: '4px',
                  backgroundColor: 'var(--bg-secondary)',
                  color: 'var(--text-primary)'
                }}
              />
              <small style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>
                Model is automatically filled based on the selected cabinet
              </small>
            </div>
            
            <div className="form-group">
              <label>Location *</label>
              <select
                value={formData.location_id}
                onChange={(e) => handleChange('location_id', e.target.value)}
                required
                style={{
                  width: '100%',
                  padding: '8px',
                  border: '1px solid var(--border-color)',
                  borderRadius: '4px',
                  backgroundColor: 'var(--bg-secondary)',
                  color: 'var(--text-primary)'
                }}
              >
                <option value="">All Locations</option>
                {locations.map(location => (
                  <option key={location.id} value={location.id}>{location.name}</option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Status Change */}
      <div>
        <label style={{ 
          display: 'block', 
          marginBottom: '8px', 
          color: 'var(--text-primary)', 
          fontWeight: '600',
          fontSize: '14px'
        }}>
          New Status:
        </label>
        <div style={{ display: 'flex', gap: '12px' }}>
          <label style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '8px', 
            cursor: 'pointer',
            padding: '8px 12px',
            borderRadius: '6px',
            backgroundColor: formData.newStatus === 'active' ? 'var(--accent-color)' : 'transparent',
            color: formData.newStatus === 'active' ? 'white' : 'var(--text-primary)',
            border: '1px solid var(--border-color)'
          }}>
            <input
              type="radio"
              name="status"
              value="active"
              checked={formData.newStatus === 'active'}
              onChange={(e) => handleChange('newStatus', e.target.value)}
              style={{ display: 'none' }}
            />
            Active
          </label>
          <label style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '8px', 
            cursor: 'pointer',
            padding: '8px 12px',
            borderRadius: '6px',
            backgroundColor: formData.newStatus === 'inactive' ? '#dc3545' : 'transparent',
            color: formData.newStatus === 'inactive' ? 'white' : 'var(--text-primary)',
            border: '1px solid var(--border-color)'
          }}>
            <input
              type="radio"
              name="status"
              value="inactive"
              checked={formData.newStatus === 'inactive'}
              onChange={(e) => handleChange('newStatus', e.target.value)}
              style={{ display: 'none' }}
            />
            Inactive
          </label>
        </div>
      </div>

      {/* Date and Time Selection */}
      <div style={{ display: 'flex', gap: '16px' }}>
        <div style={{ flex: 1 }}>
          <label style={{ 
            display: 'block', 
            marginBottom: '8px', 
            color: 'var(--text-primary)', 
            fontWeight: '600',
            fontSize: '14px'
          }}>
            Date:
          </label>
          <input
            type="date"
            value={formData.scheduledDate}
            onChange={(e) => handleChange('scheduledDate', e.target.value)}
            style={{
              width: '100%',
              padding: '10px',
              border: '1px solid var(--border-color)',
              borderRadius: '6px',
              backgroundColor: 'var(--bg-secondary)',
              color: 'var(--text-primary)',
              fontSize: '14px'
            }}
          />
        </div>
        <div style={{ flex: 1 }}>
          <label style={{ 
            display: 'block', 
            marginBottom: '8px', 
            color: 'var(--text-primary)', 
            fontWeight: '600',
            fontSize: '14px'
          }}>
            Time:
          </label>
          <input
            type="time"
            value={formData.scheduledTime}
            onChange={(e) => handleChange('scheduledTime', e.target.value)}
            style={{
              width: '100%',
              padding: '10px',
              border: '1px solid var(--border-color)',
              borderRadius: '6px',
              backgroundColor: 'var(--bg-secondary)',
              color: 'var(--text-primary)',
              fontSize: '14px'
            }}
          />
        </div>
      </div>

      {/* Action Buttons */}
      <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end', marginTop: '20px' }}>
        <button
          type="button"
          onClick={onCancel}
          style={{
            padding: '10px 20px',
            border: '1px solid var(--border-color)',
            borderRadius: '8px',
            backgroundColor: 'transparent',
            color: 'var(--text-primary)',
            cursor: 'pointer',
            fontSize: '14px',
            fontWeight: '500'
          }}
        >
          Cancel
        </button>
        <button
          type="submit"
          style={{
            padding: '10px 20px',
            border: 'none',
            borderRadius: '8px',
            backgroundColor: 'var(--accent-color)',
            color: 'white',
            cursor: 'pointer',
            fontSize: '14px',
            fontWeight: '600'
          }}
        >
          Schedule Change
        </button>
      </div>
    </form>
  );
};
const Dashboard = () => {
  const { user, logout } = useAuth();
  const [stats, setStats] = useState(null);
  const [companies, setCompanies] = useState([]);
  const [locations, setLocations] = useState([]);
  const [providers, setProviders] = useState([]);
  const [cabinets, setCabinets] = useState([]);
  const [slotMachines, setSlotMachines] = useState([]);
  const [gameMixes, setGameMixes] = useState([]);
  const [invoices, setInvoices] = useState([]);
  const [onjnReports, setOnjnReports] = useState([]);
  const [legalDocuments, setLegalDocuments] = useState([]);

  const [metrology, setMetrology] = useState([]);
  const [jackpots, setJackpots] = useState([]);
  const [comisionDates, setComisionDates] = useState([]);
  const [showReportDetailsModal, setShowReportDetailsModal] = useState(false);
  const [selectedReportDetails, setSelectedReportDetails] = useState(null);
  const [users, setUsers] = useState([]);
  const [editingUser, setEditingUser] = useState(null);
  const [showUserForm, setShowUserForm] = useState(false);
  const [editingEntity, setEditingEntity] = useState(null);
  const [selectedItems, setSelectedItems] = useState([]);
  const [showEntityForm, setShowEntityForm] = useState(false);
  const [showBulkEditForm, setShowBulkEditForm] = useState(false);
  const [bulkEditType, setBulkEditType] = useState('');
  const [bulkEditData, setBulkEditData] = useState({});
  const [searchTerm, setSearchTerm] = useState('');
  const [entityType, setEntityType] = useState('');
  const [companiesLocations, setCompaniesLocations] = useState({ companies: [], locations: [] });
  const [activeView, setActiveView] = useState(() => {
    const savedView = localStorage.getItem('activeView');
    return savedView || 'dashboard';
  });
  const [loading, setLoading] = useState(true);
  // Initialize theme from localStorage or default to 'light'
  const [theme, setTheme] = useState(() => {
    const savedTheme = localStorage.getItem('theme');
    return savedTheme || 'light';
  });
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(() => {
    try { return localStorage.getItem('sidebarCollapsed') === '1'; } catch { return false; }
  });
  const toggleSidebar = () => {
    setIsSidebarCollapsed(prev => {
      const next = !prev;
      try { localStorage.setItem('sidebarCollapsed', next ? '1' : '0'); } catch {}
      return next;
    });
  };

  // Click-to-filter states for slot machines table
  const [selectedLocationFilter, setSelectedLocationFilter] = useState(null);
  const [selectedProviderFilter, setSelectedProviderFilter] = useState(null);
  const [selectedCabinetFilter, setSelectedCabinetFilter] = useState(null);
  const [selectedGameMixFilter, setSelectedGameMixFilter] = useState(null);
  const [selectedInvoiceFilter, setSelectedInvoiceFilter] = useState(null);
  const [selectedContractFilter, setSelectedContractFilter] = useState(null);
  const [selectedSerialFilter, setSelectedSerialFilter] = useState(null);
  const [selectedCompanyFilter, setSelectedCompanyFilter] = useState(null);
  const [selectedRTPFilter, setSelectedRTPFilter] = useState(null);
  const [selectedPlacesFilter, setSelectedPlacesFilter] = useState(null);
  const [selectedCvtDateFilter, setSelectedCvtDateFilter] = useState(null);

  // Provider avatar filter state
  const [selectedProviderAvatarFilter, setSelectedProviderAvatarFilter] = useState(null);

  // Invoice popup state
  const [showInvoicePopup, setShowInvoicePopup] = useState(false);
  const [selectedInvoice, setSelectedInvoice] = useState(null);
  const [showAddCvtDatePopup, setShowAddCvtDatePopup] = useState(false);
  
  // Jackpot popup state
  const [selectedJackpots, setSelectedJackpots] = useState(null);
  
  // Invoice slots popup state
  const [selectedInvoiceSlots, setSelectedInvoiceSlots] = useState(null);

  // Slot attachments modal state
  const [showSlotAttachmentsModal, setShowSlotAttachmentsModal] = useState(false);
  const [selectedSlotId, setSelectedSlotId] = useState(null);
  const [showEntityAttachmentsModal, setShowEntityAttachmentsModal] = useState(false);
  const [selectedEntityType, setSelectedEntityType] = useState(null);
  const [selectedEntityId, setSelectedEntityId] = useState(null);

  // Change history modal state
  const [showChangeHistoryModal, setShowChangeHistoryModal] = useState(false);
  const [changeHistoryData, setChangeHistoryData] = useState([]);
  const [selectedHistoryEntityType, setSelectedHistoryEntityType] = useState('');
  const [selectedHistoryEntityId, setSelectedHistoryEntityId] = useState('');

  // All modifications history modal state
  const [showAllModificationsModal, setShowAllModificationsModal] = useState(false);
  const [allModificationsData, setAllModificationsData] = useState([]);
  const [selectedAllModificationsEntityType, setSelectedAllModificationsEntityType] = useState('');
  const [selectedAllModificationsEntityId, setSelectedAllModificationsEntityId] = useState('');

  // CVT attachments modal state
  const [showCvtAttachments, setShowCvtAttachments] = useState(false);
  const [selectedCvtForAttachments, setSelectedCvtForAttachments] = useState(null);

  // Marketing module state
  const [marketingCampaigns, setMarketingCampaigns] = useState([]);
  const [showMarketingForm, setShowMarketingForm] = useState(false);
  const emptyMarketingForm = {
    type: 'promotion',
    name: '',
    description: '',
    locations: [],
    start_at: '',
    end_at: '',
    payouts: [] // {date:'', location_id:'', amount:''}
  };
  const [marketingForm, setMarketingForm] = useState(emptyMarketingForm);
  const [savingMarketing, setSavingMarketing] = useState(false);

  const fetchMarketingCampaigns = async () => {
    try {
      const headers = { Authorization: `Bearer ${localStorage.getItem('token')}` };
      const res = await fetch(`${API}/marketing/campaigns`, { headers });
      if (res.ok) {
        const data = await res.json();
        setMarketingCampaigns(data);
      }
    } catch (e) {
      console.error('Failed to load marketing campaigns', e);
    }
  };

  useEffect(() => {
    if (activeView === 'marketing') {
      fetchMarketingCampaigns();
    }
  }, [activeView]);

  // Bulk delete confirmation modal state
  const [showBulkDeleteConfirm, setShowBulkDeleteConfirm] = useState(false);
  const [bulkDeleteType, setBulkDeleteType] = useState('');
  
  // Individual delete confirmation modal state
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [fileToDelete, setFileToDelete] = useState(null);

  // Metrology popup state
  const [selectedMetrology, setSelectedMetrology] = useState(null);
  
  // Metrology search state
  const [metrologySearchTerm, setMetrologySearchTerm] = useState('');

  // Commission Date Details Page state
  const [showCommissionDateDetailsPage, setShowCommissionDateDetailsPage] = useState(false);
  const [selectedCommissionDate, setSelectedCommissionDate] = useState(null);
  const [showJackpotDetailsPage, setShowJackpotDetailsPage] = useState(false);
  const [selectedJackpot, setSelectedJackpot] = useState(null);
  const [showMetrologyDetailsPage, setShowMetrologyDetailsPage] = useState(false);
  const [showInvoiceDetailsPage, setShowInvoiceDetailsPage] = useState(false);
  const [showLocationDetailsPage, setShowLocationDetailsPage] = useState(false);
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [showHistoryChangesPage, setShowHistoryChangesPage] = useState(false);
  const handleCloseHistoryChanges = useCallback(() => setShowHistoryChangesPage(false), []);

  // Notification system state
  const [showNotification, setShowNotification] = useState(false);
  const [notificationMessage, setNotificationMessage] = useState('');
  const [notificationType, setNotificationType] = useState('success'); // 'success', 'error', 'warning', 'info'

  // Scheduled changes and history state
  const [scheduledChanges, setScheduledChanges] = useState(() => {
    const saved = localStorage.getItem('scheduledChanges');
    return saved ? JSON.parse(saved) : [];
  });
  const [changeHistory, setChangeHistory] = useState(() => {
    const saved = localStorage.getItem('changeHistory');
    return saved ? JSON.parse(saved) : [];
  });
  const [showScheduledChangesModal, setShowScheduledChangesModal] = useState(false);
  const [showHistoryModal, setShowHistoryModal] = useState(false);
  const [showScheduledChangeForSlot, setShowScheduledChangeForSlot] = useState(null);
  const [showBulkStatusConfirm, setShowBulkStatusConfirm] = useState(false);
  const [bulkStatusData, setBulkStatusData] = useState(null);

  // Schedule change modal states
  const [showScheduleChangeModal, setShowScheduleChangeModal] = useState(false);
  const [scheduleChangeData, setScheduleChangeData] = useState(null);
  
  // Cancel confirmation modal states
  const [showCancelConfirmation, setShowCancelConfirmation] = useState(false);
  const [cancelConfirmationData, setCancelConfirmationData] = useState(null);
  const [confirmModalData, setConfirmModalData] = useState({
    isOpen: false,
    title: '',
    message: '',
    onConfirm: null,
    onCancel: null
  });
  
  const [editDateTimeModal, setEditDateTimeModal] = useState({
    isOpen: false,
    scheduledChange: null,
    newDateTime: '',
    onSave: null,
    onCancel: null
  });

  // Timer state for countdown display
  const [timerTick, setTimerTick] = useState(Date.now());

  // User avatar hook
  const { avatar } = useAvatar('users', user?.id);

  // Save theme preference to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('theme', theme);
  }, [theme]);

  // Save active view to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('activeView', activeView);
  }, [activeView]);

  // Save scheduled changes and history to localStorage
  useEffect(() => {
    localStorage.setItem('scheduledChanges', JSON.stringify(scheduledChanges));
  }, [scheduledChanges]);

  useEffect(() => {
    localStorage.setItem('changeHistory', JSON.stringify(changeHistory));
  }, [changeHistory]);

  // Custom notification function
  const showCustomNotification = (message, type = 'success') => {
    setNotificationMessage(message);
    setNotificationType(type);
    setShowNotification(true);
    setTimeout(() => {
      setShowNotification(false);
    }, 4000);
  };

  const handleCancelScheduledChanges = () => {
    if (cancelConfirmationData) {
      const { slotId, changesCount } = cancelConfirmationData;
      // Șterge modificările programate pentru acest slot
      setScheduledChanges(prev => 
        prev.filter(change => 
          !(change.entityType === 'slots' && change.itemId === slotId)
        )
      );
      showCustomNotification(`${changesCount} scheduled changes cancelled`, 'success');
      setShowCancelConfirmation(false);
      setCancelConfirmationData(null);
      setShowScheduledChangeForSlot(null);
    }
  };

  const handleEditScheduledDateTime = (scheduledChange) => {
    // Use the scheduled date/time (future date) instead of current date/time
    const scheduledDateTime = new Date(scheduledChange.scheduledDateTime);
    const formattedDateTime = scheduledDateTime.toISOString().slice(0, 16); // YYYY-MM-DDTHH:MM
    
    setEditDateTimeModal({
      isOpen: true,
      scheduledChange: scheduledChange,
      newDateTime: formattedDateTime,
      onSave: (newDateTime) => {
        // Update the scheduled change with new date/time
        setScheduledChanges(prev => 
          prev.map(change => 
            change.id === scheduledChange.id 
              ? { ...change, scheduledDateTime: newDateTime }
              : change
          )
        );
        
        // Close both modals
        setEditDateTimeModal({ isOpen: false, scheduledChange: null, newDateTime: '', onSave: null, onCancel: null });
        setShowScheduledChangeForSlot(null);
        showCustomNotification('Scheduled date/time updated successfully', 'success');
      },
      onCancel: () => {
        setEditDateTimeModal({ isOpen: false, scheduledChange: null, newDateTime: '', onSave: null, onCancel: null });
      }
    });
  };

  const handleScheduledChange = async (entityType, itemId, action, oldValue, newValue, scheduledDateTime) => {
    try {
      console.log('Scheduling change:', { entityType, itemId, action, oldValue, newValue, scheduledDateTime });
      
      const change = {
        id: Date.now() + Math.random(),
        entityType,
        itemId,
        action,
        oldValue,
        newValue,
        scheduledDateTime,
        timestamp: new Date().toISOString(),
        userName: user?.username || 'Unknown User'
      };

      setScheduledChanges(prev => [...prev, change]);
      
      // Save to backend change history
      try {
        const changeHistoryData = {
          entity_type: entityType,
          entity_id: itemId,
          field_name: action,
          old_value: oldValue || '',
          new_value: newValue || '',
          scheduled_datetime: scheduledDateTime
        };
        
        await fetch(`${API}/change-history`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(changeHistoryData)
        });
      } catch (error) {
        console.error('Error saving change history to backend:', error);
      }
      
      const timeUntilExecution = new Date(scheduledDateTime).getTime() - Date.now();
      const minutes = Math.floor(timeUntilExecution / (1000 * 60));
      const seconds = Math.floor((timeUntilExecution % (1000 * 60)) / 1000);
      
      showCustomNotification(
        `Change scheduled successfully. Will execute in ${minutes}:${seconds.toString().padStart(2, '0')}`,
        'success'
      );
    } catch (error) {
      console.error('Error scheduling change:', error);
      showCustomNotification('Error scheduling change', 'error');
    }
  };

  useEffect(() => {
    if (user) {
      // Încarcă datele imediat în background
      fetchDashboardData();
      loadChangeHistoryCount('slots');
    }
  }, [user]);

  // Timer tick effect for scheduled changes
  useEffect(() => {
    if (showHistoryChangesPage) {
      // Pause schedule executor while All History Changes is open to avoid flicker
      return;
    }
    const timerTick = () => {
      const now = Date.now();
      const expiredChanges = scheduledChanges.filter(change => 
        new Date(change.scheduledDateTime).getTime() <= now
      );

      if (expiredChanges.length > 0) {
        console.log('Applying expired scheduled changes:', expiredChanges);
        
        expiredChanges.forEach(async (change) => {
          // Apply the change
          console.log('Applying change:', change);
          
          try {
            // Apply changes to backend based on entity type
            if (change.entityType === 'slots') {
              const token = localStorage.getItem('token');
              const headers = { 
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
              };
              
              // Get current slot data
              const currentSlot = slotMachines.find(slot => slot.id === change.itemId);
              if (!currentSlot) {
                console.error('Slot not found:', change.itemId);
                return;
              }
              
              // Prepare updated data based on changes
              const updatedData = { ...currentSlot };
              
              if (change.changes) {
                // Apply comprehensive changes
                if (change.changes.status) {
                  updatedData.status = change.changes.status.new;
                }
                if (change.changes.provider_id) {
                  updatedData.provider_id = change.changes.provider_id.new;
                }
                if (change.changes.game_mix_id) {
                  updatedData.game_mix_id = change.changes.game_mix_id.new;
                }
                if (change.changes.cabinet_id) {
                  updatedData.cabinet_id = change.changes.cabinet_id.new;
                }
                if (change.changes.model) {
                  updatedData.model = change.changes.model.new;
                }
                if (change.changes.location_id) {
                  updatedData.location_id = change.changes.location_id.new;
                }
              } else {
                // Fallback for old format
                if (change.action === 'status_change') {
                  updatedData.status = change.newValue;
                }
              }
              
              // Update slot in backend
              const response = await fetch(`${API}/slot-machines/${change.itemId}`, {
                method: 'PUT',
                headers,
                body: JSON.stringify(updatedData)
              });
              
              if (!response.ok) {
                throw new Error(`Failed to update slot: ${response.statusText}`);
              }
              
              // Refresh data after successful update
              await fetchDashboardData();
              
              console.log('Slot updated successfully:', change.itemId);
            }
          
          // Add to history
          const historyEntry = {
            id: Date.now() + Math.random(),
            entityType: change.entityType,
            itemId: change.itemId,
            action: change.action,
            oldValue: change.oldValue,
            newValue: change.newValue,
            timestamp: new Date().toISOString(),
            executed: true,
              reason: 'Scheduled change executed',
              userName: change.userName || user?.username || 'Unknown User'
          };
          
          setChangeHistory(prev => [historyEntry, ...prev]);

            // Save to backend change history
            try {
              const changeHistoryData = {
                entity_type: change.entityType,
                entity_id: change.itemId,
                field_name: change.action,
                old_value: change.oldValue || '',
                new_value: change.newValue || '',
                scheduled_datetime: change.scheduledDateTime
              };
              
              await fetch(`${API}/change-history`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify(changeHistoryData)
              });
            } catch (error) {
              console.error('Error saving change history to backend:', error);
            }
            
          } catch (error) {
            console.error('Error applying scheduled change:', error);
            showCustomNotification(`Error applying scheduled change: ${error.message}`, 'error');
          }
        });

        // Remove expired changes from scheduled changes
        setScheduledChanges(prev => 
          prev.filter(change => 
            new Date(change.scheduledDateTime).getTime() > now
          )
        );

        showCustomNotification(`${expiredChanges.length} scheduled changes have been applied`, 'success');
      }
    };

    const interval = setInterval(timerTick, 1000);
    return () => clearInterval(interval);
  }, [scheduledChanges, showHistoryChangesPage]);

  // Timer tick for countdown display updates
  useEffect(() => {
    if (showHistoryChangesPage) {
      // Pause the visual countdown ticker to stop re-renders while page is open
      return;
    }
    const interval = setInterval(() => setTimerTick(Date.now()), 1000);
    return () => clearInterval(interval);
  }, [showHistoryChangesPage]);

  // Initialize timer state and clean up expired changes on mount
  useEffect(() => {
    const now = Date.now();
    const validChanges = scheduledChanges.filter(change => 
      new Date(change.scheduledDateTime).getTime() > now
    );
    
    if (validChanges.length !== scheduledChanges.length) {
      setScheduledChanges(validChanges);
    }
  }, []);

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };
      
      const [statsRes, companiesRes, locationsRes, providersRes, cabinetsRes, slotMachinesRes, gameMixesRes, invoicesRes, onjnRes, legalRes, metrologyRes, jackpotsRes, comisionDatesRes, usersRes, adminDataRes] = await Promise.all([
        fetch(`${API}/dashboard/stats`, { headers }),
        fetch(`${API}/companies`, { headers }),
        fetch(`${API}/locations`, { headers }),
        fetch(`${API}/providers`, { headers }),
        fetch(`${API}/cabinets`, { headers }),
        fetch(`${API}/slot-machines`, { headers }),
        fetch(`${API}/game-mixes`, { headers }),
        fetch(`${API}/invoices`, { headers }),
        fetch(`${API}/onjn-reports`, { headers }),
        fetch(`${API}/legal-documents`, { headers }),
        fetch(`${API}/metrology`, { headers }),
        fetch(`${API}/jackpots`, { headers }),
        fetch(`${API}/comision-dates`, { headers }),
        fetch(`${API}/users`, { headers }),
        user?.role === 'admin' ? fetch(`${API}/admin/companies-locations`, { headers }) : Promise.resolve({ json: () => ({ companies: [], locations: [] }) })
      ]);
      
      // Handle responses that might return errors for non-admin users
      const [statsData, companiesData, locationsData, providersData, cabinetsData, slotMachinesData, gameMixesData, invoicesData, onjnData, legalData, metrologyData, jackpotsData, comisionDatesData, usersData, adminData] = await Promise.all([
        statsRes.json(),
        companiesRes.json(),
        locationsRes.json(),
        providersRes.json(),
        cabinetsRes.json(),
        slotMachinesRes.json(),
        gameMixesRes.json(),
        invoicesRes.json(),
        onjnRes.json(),
        legalRes.json(),
        metrologyRes.json(),
        jackpotsRes.json(),
        comisionDatesRes.json(),
        usersRes.ok ? usersRes.json() : [], // Return empty array if users endpoint fails
        adminDataRes.ok ? adminDataRes.json() : { companies: [], locations: [] }
      ]);
      
      setStats(statsData);
      setCompanies(companiesData);
      setLocations(locationsData);
      setProviders(providersData);
      setCabinets(cabinetsData);
      setSlotMachines(slotMachinesData);
      setGameMixes(gameMixesData);
      setInvoices(invoicesData);
      setOnjnReports(onjnData);
      setLegalDocuments(legalData);

      setMetrology(metrologyData);
      setJackpots(jackpotsData);
      setComisionDates(comisionDatesData);
      console.log('📊 Updated comisionDates:', comisionDatesData.length, 'items');
      console.log('📊 comisionDatesData:', comisionDatesData);
      console.log('📊 First comision date event_name:', comisionDatesData[0]?.event_name);
      
                    setUsers(usersData);
      setCompaniesLocations(adminData);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSlotStatusChange = async (slot, newStatus) => {
    if (slot.status === newStatus) return;
    
    // If setting to inactive, show confirmation dialog
    if (newStatus === 'inactive') {
      setConfirmModalData({
        isOpen: true,
        title: '⚠️ WARNING!',
        message: `Slot "${slot.serial_number}" will be set as INACTIVE.\n\nThis slot will disappear from the Slot Machines list and will be moved to Warehouse.\n\nDo you want to continue?`,
        onConfirm: () => {
          setConfirmModalData({ isOpen: false, title: '', message: '', onConfirm: null, onCancel: null });
          handleStatusChange(slot, 'inactive');
        },
        onCancel: () => {
          setConfirmModalData({ isOpen: false, title: '', message: '', onConfirm: null, onCancel: null });
        }
      });
      return;
    }
    
    // For active status, proceed directly
    await handleStatusChange(slot, newStatus);
  };

  const handleStatusChange = async (slot, newStatus) => {
    try {
      const token = localStorage.getItem('token');
      
      // Create a simple update object with only the necessary fields
      const updateData = {
        cabinet_id: slot.cabinet_id,
        game_mix_id: slot.game_mix_id,
        provider_id: slot.provider_id,
        model: slot.model,
        serial_number: slot.serial_number,
        denomination: slot.denomination,
        max_bet: slot.max_bet,
        rtp: slot.rtp,
        gaming_places: slot.gaming_places,
        commission_date: slot.commission_date,
        invoice_number: slot.invoice_number,
        status: newStatus
      };
      
      const response = await fetch(`${API}/slot-machines/${slot.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(updateData)
      });
      
      if (response.ok) {
        // Force refresh all data
        await fetchDashboardData();
        
        // Show success message with specific info for inactive status
        if (newStatus === 'inactive') {
          showCustomNotification(
            `✅ Slot "${slot.serial_number}" set as INACTIVE and moved to Warehouse!`, 
            'success'
          );
        } else {
          const statusText = newStatus === 'active' ? 'active' : 'inactive';
                      showCustomNotification(`✅ Slot status updated successfully to: ${statusText}`, 'success');
        }
      } else {
        const errorData = await response.json();
        showCustomNotification(`Update error: ${errorData.detail || 'Unknown error'}`, 'error');
      }
    } catch (error) {
      showCustomNotification('Connection error: ' + error.message, 'error');
    }
  };

  // Funcția handleMetrologyDateChange pentru editarea datelor CVT


  // Navigation items with permission checks
  const navigationItems = user ? [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    ...(user?.permissions?.modules?.companies ? [{ id: 'companies', label: 'Companies', icon: '🏢', count: companies.length }] : []),
    ...(user?.permissions?.modules?.locations ? [{ id: 'locations', label: 'Locations', icon: '📍', count: locations.length }] : []),
    ...(user?.permissions?.modules?.providers ? [{ id: 'providers', label: 'Providers', icon: '🎮', count: providers.length }] : []),
    ...(user?.permissions?.modules?.cabinets ? [{ id: 'cabinets', label: 'Cabinets', icon: '🎰', count: cabinets.length }] : []),
    ...(user?.permissions?.modules?.game_mixes ? [{ id: 'gamemixes', label: 'Game Mixes', icon: '🎲', count: gameMixes.length }] : []),
    ...(user?.permissions?.modules?.slot_machines ? [{ id: 'slots', label: 'Slots', icon: '🍒', count: slotMachines.filter(s => s.status !== 'inactive').length }] : []),
    ...(user?.permissions?.modules?.slot_machines ? [{ id: 'warehouse', label: 'Warehouse', icon: '📦', count: slotMachines.filter(s => s.status === 'inactive').length }] : []),
    ...(user?.permissions?.modules?.metrology ? [{ id: 'metrology2', label: 'Metrology CVT', icon: '🔬', count: metrology.length }] : []),
    ...(user?.permissions?.modules?.jackpots ? [{ id: 'jackpots', label: 'Jackpots', icon: '🎰', count: jackpots.length }] : []),
    { id: 'marketing', label: 'Marketing', icon: '📣', count: marketingCampaigns.length },
    ...(user?.permissions?.modules?.invoices ? [{ id: 'invoices', label: 'Invoices', icon: '💰', count: invoices.length }] : []),
    ...(user?.permissions?.modules?.onjn_reports ? [{ id: 'onjn', label: 'ONJN Reports', icon: '📋', count: onjnReports.length + comisionDates.length }] : []),
    ...(user?.permissions?.modules?.legal_documents ? [{ id: 'legal', label: 'Legal Documents', icon: '📄', count: legalDocuments.length }] : []),
    ...(user?.role === 'admin' ? [{ id: 'users', label: 'Users', icon: '👥', count: users.length }] : []),
  ] : [];

  const handleEditUser = (userData) => {
    setEditingUser(userData);
    setShowUserForm(true);
  };

  const handleCloseUserForm = () => {
    setEditingUser(null);
    setShowUserForm(false);
  };

  const handleSaveUser = async (userData) => {
    try {
      console.log('👤 Saving user data:', userData);
      console.log('📞 Phone field:', userData.phone);
      
      const token = localStorage.getItem('token');
      const method = editingUser ? 'PUT' : 'POST';
      const url = editingUser ? `${API}/users/${editingUser.id}` : `${API}/users`;
      
      console.log('🌐 URL:', url);
      console.log('📋 Method:', method);
      
      const response = await fetch(url, {
        method,
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(userData)
      });

      if (response.ok) {
        const responseData = await response.json();
        console.log('✅ Server response:', responseData);
        console.log('📞 Phone in response:', responseData.phone);
        
        await fetchDashboardData(); // Refresh data
        handleCloseUserForm();
        showCustomNotification('✅ User saved successfully!', 'success');
      } else {
        const errorData = await response.json();
        console.error('❌ Server error:', errorData);
        showCustomNotification(`❌ Failed to save user: ${errorData.detail || 'Unknown error'}`, 'error');
        console.error('Failed to save user');
      }
    } catch (error) {
      showCustomNotification(`❌ Error saving user: ${error.message}`, 'error');
      console.error('Error saving user:', error);
    }
  };

  // Generic entity handlers
  const handleAddEntity = (type) => {
    setEntityType(type);
    setEditingEntity(null);
    setShowEntityForm(true);
  };

  const handleEditEntity = (entityData, type) => {
    setEntityType(type);
    setEditingEntity(entityData);
    setShowEntityForm(true);
  };

  const handleCloseEntityForm = () => {
    setEditingEntity(null);
    setShowEntityForm(false);
    setEntityType('');
  };
  const handleSaveEntity = async (entityData) => {
    try {
      // Debug: Log the data being saved for slots
      if (entityType === 'slots') {
        console.log('🎰 Saving slot machine data:', entityData);
        console.log('🔍 Fields present:', Object.keys(entityData));
        console.log('📋 Production year:', entityData.production_year);
        console.log('📍 Location ID:', entityData.location_id);
        console.log('🏠 Ownership type:', entityData.ownership_type);
      }
      
      // Debug: Log the data being saved for locations
      if (entityType === 'locations') {
        console.log('📍 Saving location data:', entityData);
        console.log('🔍 Fields present:', Object.keys(entityData));
        console.log('👤 Contact person:', entityData.contact_person);
        console.log('📧 Contact email:', entityData.contact_email);
        console.log('📞 Contact phone:', entityData.contact_phone);
        console.log('🆔 Contact person ID:', entityData.contact_person_id);
        console.log('📝 Contact person type:', entityData.contact_person_type);
      }
      
      // Debug: Log the data being saved for invoices
      if (entityType === 'invoices') {
        console.log('🧾 Saving invoice data:', entityData);
        console.log('🔍 Fields present:', Object.keys(entityData));
        console.log('📊 Status:', entityData.status);
        console.log('💰 Amount:', entityData.amount);
        console.log('📅 Issue date:', entityData.issue_date);
        console.log('📅 Due date:', entityData.due_date);
        console.log('🏢 Buyer ID:', entityData.buyer_id);
        console.log('🏪 Seller ID:', entityData.seller_id);
        console.log('📍 Location ID:', entityData.location_id);
        console.log('🔄 Transaction Type:', entityData.transaction_type);
        console.log('🔄 Transaction Type (raw):', entityData.transaction_type);
        console.log('🔄 All invoice fields:', JSON.stringify(entityData, null, 2));
      }
      
      // Debug: Log the data being saved for jackpots
      if (entityType === 'jackpots') {
        console.log('🎰 Saving jackpot data:', entityData);
        console.log('🔍 Fields present:', Object.keys(entityData));
        console.log('🔢 Serial number:', entityData.serial_number);
        console.log('🏷️ Jackpot name:', entityData.jackpot_name);
        console.log('📊 Jackpot type:', entityData.jackpot_type);
                  console.log('📊 Increment rate:', entityData.increment_rate);
        console.log('📝 Description:', entityData.description);
      }
      
      // Debug: Log the data being saved for comision_date
      if (entityType === 'comision_date') {
        console.log('📅 Saving comision date data:', entityData);
        console.log('🔍 Fields present:', Object.keys(entityData));
        console.log('📝 Event name:', entityData.event_name);
        console.log('📅 Commission date:', entityData.commission_date);
        console.log('🔢 Serial numbers:', entityData.serial_numbers);
      }
      
      const token = localStorage.getItem('token');
      const method = editingEntity ? 'PUT' : 'POST';
      const endpoint = getEntityEndpoint(entityType);
      const url = editingEntity ? `${API}/${endpoint}/${editingEntity.id || editingEntity._id}` : `${API}/${endpoint}`;
      
      console.log('🌐 API URL:', url);
      console.log('📤 Request body:', JSON.stringify(entityData, null, 2));
      
      const response = await fetch(url, {
        method,
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(entityData)
      });

      console.log('📡 Response status:', response.status);

      if (response.ok) {
        const responseData = await response.json();
        console.log('✅ Save successful, response data:', responseData);
        
        // Force refresh data with cache busting
        await fetchDashboardData(); // Refresh data
        console.log('🔄 Data refreshed after save');
        
        // Force re-render by updating state
        if (entityType === 'comision_date') {
          console.log('🔄 Forcing comision dates refresh...');
          // Force a small delay to ensure backend has processed the update
          setTimeout(async () => {
            try {
              const token = localStorage.getItem('token');
              const response = await fetch(`${API}/comision-dates`, { 
                headers: { 
                  'Authorization': `Bearer ${token}`,
                  'Cache-Control': 'no-cache',
                  'Pragma': 'no-cache'
                } 
              });
              if (response.ok) {
                const freshData = await response.json();
                console.log('🔄 Fresh comision dates data:', freshData);
                console.log('🔄 First item event_name:', freshData[0]?.event_name);
                console.log('🔄 All items event_names:', freshData.map(item => ({ id: item.id, event_name: item.event_name })));
                setComisionDates(freshData);
                console.log('🔄 State updated with fresh data');
                
                // Also refresh ONJN reports to update the combined data
                const onjnResponse = await fetch(`${API}/onjn-reports`, { 
                  headers: { 
                    'Authorization': `Bearer ${token}`,
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache'
                  } 
                });
                if (onjnResponse.ok) {
                  const onjnData = await onjnResponse.json();
                  setOnjnReports(onjnData);
                  console.log('🔄 ONJN reports refreshed');
                }
                
                // Force a second refresh after a longer delay to ensure UI updates
                setTimeout(async () => {
                  try {
                    const secondResponse = await fetch(`${API}/comision-dates`, { 
                      headers: { 
                        'Authorization': `Bearer ${token}`,
                        'Cache-Control': 'no-cache',
                        'Pragma': 'no-cache'
                      } 
                    });
                    if (secondResponse.ok) {
                      const secondData = await secondResponse.json();
                      console.log('🔄 Second refresh comision dates data:', secondData);
                      setComisionDates(secondData);
                      console.log('🔄 Second refresh completed');
                    }
                  } catch (error) {
                    console.error('Error in second refresh:', error);
                  }
                }, 1000);
              }
            } catch (error) {
              console.error('Error refreshing comision dates:', error);
            }
          }, 500);
        }
        
        handleCloseEntityForm();
        showCustomNotification(`✅ ${getEntityDisplayName(entityType)} saved successfully!`, 'success');
      } else {
        const error = await response.json();
        console.error('❌ Failed to save entity:', error);
        console.error('📡 Response status:', response.status, response.statusText);
                  showCustomNotification(`❌ Failed to save ${getEntityDisplayName(entityType)}: ${error.detail || 'Unknown error'}`, 'error');
      }
    } catch (error) {
      console.error('Error saving entity:', error);
              showCustomNotification(`❌ Error saving ${getEntityDisplayName(entityType)}: ${error.message}`, 'error');
    }
  };

  const handleDeleteEntity = async (entityId, type) => {
    console.log('🔥 DELETE REQUESTED:', entityId, type);
    
    // Set the item to delete and show confirmation modal
    setFileToDelete({ id: entityId, type: type });
    setShowDeleteConfirm(true);
  };
  const confirmDeleteEntity = async () => {
    const { id: entityId, type } = fileToDelete;
    console.log('🔥 CONFIRMING DELETE:', entityId, type);

    try {
      const token = localStorage.getItem('token');
      const endpoint = getEntityEndpoint(type);
      console.log('📍 DELETE URL:', `${API}/${endpoint}/${entityId}`);
      
      const response = await fetch(`${API}/${endpoint}/${entityId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      console.log('📡 DELETE Response:', response.status, response.statusText);

      if (response.ok) {
        console.log('✅ Delete successful, refreshing data...');
        showCustomNotification('✅ Item deleted successfully!', 'success');
        console.log('🔄 Calling fetchDashboardData...');
        try {
        await fetchDashboardData(); // Refresh data
          console.log('✅ fetchDashboardData completed');
        } catch (error) {
          console.error('❌ Error in fetchDashboardData:', error);
        }
      } else {
        const error = await response.json();
        console.error('❌ DELETE Failed:', error);
        showCustomNotification('❌ Failed to delete: ' + (error.detail || 'Unknown error'), 'error');
      }
    } catch (error) {
      console.error('💥 Delete exception:', error);
      showCustomNotification('❌ Error deleting: ' + error.message, 'error');
    } finally {
      setShowDeleteConfirm(false);
      setFileToDelete(null);
    }
  };

  const cancelDeleteEntity = () => {
    setShowDeleteConfirm(false);
    setFileToDelete(null);
  };
  const getEntityEndpoint = (type) => {
    const endpoints = {
      companies: 'companies',
      locations: 'locations',
      providers: 'providers',
      cabinets: 'cabinets',
      slots: 'slot-machines',
      gamemixes: 'game-mixes',
      invoices: 'invoices',
      onjn: 'onjn-reports',
      legal: 'legal-documents',
      metrology: 'metrology',
      metrology2: 'metrology',
      jackpots: 'jackpots',
      comision_date: 'comision-dates'
    };
    return endpoints[type] || type;
  };

  // Bulk Edit Handler
  const handleBulkEdit = (entityType) => {
    if (selectedItems.length === 0) {
              showCustomNotification('Please select items to bulk edit', 'warning');
      return;
    }
    setBulkEditType(entityType);
    setBulkEditData({});
    setShowBulkEditForm(true);
  };

  const handleBulkDelete = async (entityType) => {
    console.log('🔥 BULK DELETE CLICKED:', entityType);
    console.log('🔥 Selected items:', selectedItems);
    console.log('🔥 Selected items length:', selectedItems.length);
    
    if (selectedItems.length === 0) {
      showCustomNotification('❌ Please select items to delete first!', 'error');
      return;
    }

    // Show confirmation modal instead of browser confirm
    console.log('🔥 Setting bulk delete modal to show');
    setBulkDeleteType(entityType);
    setShowBulkDeleteConfirm(true);
    console.log('🔥 Modal should be visible now');
  };

  const confirmBulkDelete = async () => {
    const entityType = bulkDeleteType;
    console.log('🔥 Confirming bulk delete for:', entityType);
    try {
      console.log('🚀 Starting bulk delete...');
      const endpoint = getEntityEndpoint(entityType);
      const token = localStorage.getItem('token');
      
      // Delete each item individually
      let successCount = 0;
      for (const itemId of selectedItems) {
        console.log(`🗑️ Deleting ${itemId}...`);
        
        const response = await fetch(`${API}/${endpoint}/${itemId}`, {
          method: 'DELETE',
          headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
          successCount++;
          console.log(`✅ Deleted ${itemId}`);
        } else {
          console.error(`❌ Failed to delete ${itemId}`);
        }
      }

      showCustomNotification(`✅ Successfully deleted ${successCount} of ${selectedItems.length} items!`, 'success');
      await fetchDashboardData();
      setSelectedItems([]);
      console.log('🔄 Data refreshed, selections cleared');
      
    } catch (error) {
      console.error('💥 Bulk delete error:', error);
      showCustomNotification('❌ Bulk delete failed: ' + error.message, 'error');
    } finally {
      setShowBulkDeleteConfirm(false);
      setBulkDeleteType('');
    }
  };

  const cancelBulkDelete = () => {
    console.log('🔥 Canceling bulk delete');
    setShowBulkDeleteConfirm(false);
    setBulkDeleteType('');
  };

  const confirmBulkStatus = () => {
    if (bulkStatusData) {
      setFormData(prev => ({
        ...prev,
        [bulkStatusData.field]: bulkStatusData.value
      }));
      setShowBulkStatusConfirm(false);
      setBulkStatusData(null);
    }
  };

  const cancelBulkStatus = () => {
    setShowBulkStatusConfirm(false);
    setBulkStatusData(null);
  };

  // Bulk Duplicate Handler for Slots
  const handleBulkDuplicate = async (entityType) => {
    console.log('🔄 BULK DUPLICATE CLICKED:', entityType);
    console.log('🔄 Selected items:', selectedItems);
    
    if (selectedItems.length === 0) {
      showCustomNotification('❌ Please select items to duplicate first!', 'error');
      return;
    }

    if (entityType !== 'slots') {
      showCustomNotification('❌ Duplication is only available for slots!', 'error');
      return;
    }

    try {
      console.log('🚀 Starting bulk duplicate...');
      const token = localStorage.getItem('token');
      
      // Get all existing slot serial numbers to avoid conflicts
      const existingSerials = slotMachines.map(slot => slot.serial_number);
      console.log('📋 Existing serials:', existingSerials);
      
      let successCount = 0;
      for (let i = 0; i < selectedItems.length; i++) {
        const itemId = selectedItems[i];
        console.log(`🔄 Duplicating ${itemId}...`);
        
        // Find the original slot
        const originalSlot = slotMachines.find(slot => slot.id === itemId);
        if (!originalSlot) {
          console.error(`❌ Original slot not found: ${itemId}`);
          continue;
        }
        
        // Generate new serial number
        const baseSerial = originalSlot.serial_number;
        let newSerial = `${baseSerial}-1`;
        let counter = 1;
        
        // Find next available serial number
        while (existingSerials.includes(newSerial)) {
          counter++;
          newSerial = `${baseSerial}-${counter}`;
        }
        
        // Add new serial to existing list to avoid conflicts in same batch
        existingSerials.push(newSerial);
        
        // Create duplicate slot data
        const duplicateData = {
          ...originalSlot,
          serial_number: newSerial,
          status: 'active' // Set to active by default
        };
        
        // Remove id and created_at to create new record
        delete duplicateData.id;
        delete duplicateData.created_at;
        delete duplicateData.created_by;
        
        console.log('📤 Creating duplicate with data:', duplicateData);
        
        const response = await fetch(`${API}/slot-machines`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(duplicateData)
        });
        
        if (response.ok) {
          successCount++;
          console.log(`✅ Duplicated ${originalSlot.serial_number} -> ${newSerial}`);
        } else {
          const errorText = await response.text();
          console.error(`❌ Failed to duplicate ${originalSlot.serial_number}:`, errorText);
        }
      }

              showCustomNotification(`✅ Successfully duplicated ${successCount} of ${selectedItems.length} slots!`, 'success');
      await fetchDashboardData();
      setSelectedItems([]);
      console.log('🔄 Data refreshed, selections cleared');
      
    } catch (error) {
      console.error('💥 Bulk duplicate error:', error);
              showCustomNotification('❌ Bulk duplicate failed: ' + error.message, 'error');
    }
  };
  // Handle item selection for bulk edit
  const handleItemSelection = (itemId, checked) => {
    if (checked) {
      setSelectedItems([...selectedItems, itemId]);
    } else {
      setSelectedItems(selectedItems.filter(id => id !== itemId));
    }
  };
  // Handle select all
  const handleSelectAll = (items, checked) => {
    if (checked) {
      setSelectedItems(items.map(item => item.id));
    } else {
      setSelectedItems([]);
    }
  };

  // Bulk Edit Save Handler
  const handleBulkEditSave = async () => {
    try {
      let updatePromises;
      
      if (bulkEditType === 'metrology') {
        // For metrology, selectedItems are metrology record IDs directly
        updatePromises = selectedItems.map(async (metrologyId) => {
          // Update the metrology record directly
          const response = await fetch(`${API}/metrology/${metrologyId}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify(bulkEditData)
          });
          return response.ok;
        });
      } else {
        // For other entity types, use the standard approach
        updatePromises = selectedItems.map(async (itemId) => {
          const endpoint = getEntityEndpoint(bulkEditType);
          const response = await fetch(`${API}/${endpoint}/${itemId}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify(bulkEditData)
          });
          return response.ok;
        });
      }

      const results = await Promise.all(updatePromises);
      const successCount = results.filter(Boolean).length;
      
      if (successCount === selectedItems.length) {
        showCustomNotification(`✅ Successfully updated ${successCount} ${getEntityDisplayName(bulkEditType)} items!`, 'success');
      } else {
                  showCustomNotification(`⚠️ Updated ${successCount} of ${selectedItems.length} items. Some updates failed.`, 'warning');
      }

      await fetchDashboardData();
      setShowBulkEditForm(false);
      setSelectedItems([]);
    } catch (error) {
      console.error('Bulk edit error:', error);
              showCustomNotification(`❌ Bulk edit failed: ${error.message}`, 'error');
    }
  };

  // Export Handler - Excel Format
  const handleExport = (entityType) => {
    const data = {
      companies: companies,
      locations: locations,
      providers: providers,
      cabinets: cabinets,
      slots: slotMachines,
      gamemixes: gameMixes,
      invoices: invoices,
      onjn: onjnReports,
      legal: legalDocuments,
      users: users
    };

    const exportData = data[entityType] || [];
    
    if (exportData.length === 0) {
      showCustomNotification('No data to export', 'warning');
      return;
    }

    // Prepare data for Excel - remove internal fields and format properly
    const excelData = exportData.map(item => {
      const cleanItem = { ...item };
      // Remove internal fields
      delete cleanItem.id;
      delete cleanItem.created_at;
      delete cleanItem.created_by;
      delete cleanItem.password_hash;
      
      // Format dates
      if (cleanItem.commission_date) {
        cleanItem.commission_date = new Date(cleanItem.commission_date).toISOString().split('T')[0];
      }
      if (cleanItem.issue_date) {
        cleanItem.issue_date = new Date(cleanItem.issue_date).toISOString().split('T')[0];
      }
      if (cleanItem.due_date) {
        cleanItem.due_date = new Date(cleanItem.due_date).toISOString().split('T')[0];
      }
      if (cleanItem.report_date) {
        cleanItem.report_date = new Date(cleanItem.report_date).toISOString().split('T')[0];
      }
      
      return cleanItem;
    });

    // Create Excel workbook
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.json_to_sheet(excelData);
    
    // Auto-width columns
    const colWidths = Object.keys(excelData[0] || {}).map(key => ({
      wch: Math.max(key.length, 15)
    }));
    ws['!cols'] = colWidths;
    
    XLSX.utils.book_append_sheet(wb, ws, getEntityDisplayName(entityType));
    
    // Download file
    const fileName = `${entityType}_export_${new Date().toISOString().split('T')[0]}.xlsx`;
    XLSX.writeFile(wb, fileName);
    
            showCustomNotification(`✅ ${exportData.length} ${getEntityDisplayName(entityType)} items exported to Excel successfully!`, 'success');
  };
  // Import Handler - Excel Format
  const handleImport = (entityType) => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.xlsx,.xls';
    input.onchange = async (e) => {
      const file = e.target.files[0];
      if (!file) return;
      
      try {
        const arrayBuffer = await file.arrayBuffer();
        const workbook = XLSX.read(arrayBuffer, { type: 'array' });
        const sheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[sheetName];
        const importData = XLSX.utils.sheet_to_json(worksheet);
        
        if (importData.length === 0) {
          showCustomNotification('No data found in Excel file', 'error');
          return;
        }
        
        // Validate required fields based on entity type
        const requiredFields = getRequiredFields(entityType);
        const missingFields = requiredFields.filter(field => 
          !Object.keys(importData[0]).includes(field)
        );
        
        if (missingFields.length > 0) {
                      showCustomNotification(`Missing required columns: ${missingFields.join(', ')}`, 'error');
          return;
        }
        
        // Show preview and confirm import
                  // Show import confirmation notification instead of browser confirm
          showCustomNotification(
            `Found ${importData.length} rows in Excel file. Proceed with import?`,
            'info'
          );
          const confirmImport = true; // Always proceed for now
        
        if (confirmImport) {
          // Process import (for now, just show success - actual API calls would go here)
          console.log(`Importing ${importData.length} ${entityType}:`, importData);
          showCustomNotification(`✅ Ready to import ${importData.length} ${getEntityDisplayName(entityType)} items!\n\n(Note: Actual import functionality would process these items through the API)`, 'success');
        }
        
      } catch (error) {
        console.error('Import error:', error);
                  showCustomNotification(`❌ Error reading Excel file: ${error.message}`, 'error');
      }
    };
    input.click();
  };

  // Search Filter Function
  const filterData = (data, searchTerm) => {
    if (!searchTerm) return data;
    
    const search = searchTerm.toLowerCase();
    return data.filter(item => {
      // Special handling for users to search in first_name and last_name
      if (item.first_name || item.last_name) {
        const fullName = `${item.first_name || ''} ${item.last_name || ''}`.trim();
        if (fullName.toLowerCase().includes(search)) return true;
      }
      
      // Search through all string and number fields
      return Object.values(item).some(value => {
        if (value === null || value === undefined) return false;
        return String(value).toLowerCase().includes(search);
      });
    });
  };

  // Get required fields for validation
  const getRequiredFields = (entityType) => {
    const fields = {
      companies: ['name', 'email', 'phone'],
      locations: ['name', 'address', 'city'],
      providers: ['name', 'email'],
      cabinets: ['name', 'model'],
      slots: ['model', 'denomination'],
      gamemixes: ['name'],
      invoices: ['invoice_number', 'amount'],
      onjn: ['report_number'],
      legal: ['document_type', 'title'],
      users: ['username', 'email', 'first_name', 'last_name', 'role'],
      metrology: ['serial_number', 'certificate_number', 'issue_date'],
              jackpots: ['serial_number', 'jackpot_type', 'increment_rate', 'description']
    };
    return fields[entityType] || ['name'];
  };

  // Toggle functions for click-to-filter functionality
  const toggleLocationFilter = (locationId) => {
    setSelectedLocationFilter(selectedLocationFilter === locationId ? null : locationId);
  };

  const toggleProviderFilter = (providerId) => {
    setSelectedProviderFilter(selectedProviderFilter === providerId ? null : providerId);
  };

  const toggleCabinetFilter = (cabinetId) => {
    setSelectedCabinetFilter(selectedCabinetFilter === cabinetId ? null : cabinetId);
  };

  const toggleGameMixFilter = (gameMixId) => {
    setSelectedGameMixFilter(selectedGameMixFilter === gameMixId ? null : gameMixId);
  };

  const toggleInvoiceFilter = (invoiceNumber) => {
    setSelectedInvoiceFilter(selectedInvoiceFilter === invoiceNumber ? null : invoiceNumber);
  };

  const toggleContractFilter = (contractNumber) => {
    setSelectedContractFilter(selectedContractFilter === contractNumber ? null : contractNumber);
  };

  const toggleSerialFilter = (serialNumber) => {
    setSelectedSerialFilter(selectedSerialFilter === serialNumber ? null : serialNumber);
  };

  const toggleCompanyFilter = (companyId) => {
    setSelectedCompanyFilter(selectedCompanyFilter === companyId ? null : companyId);
  };

  const toggleRTPFilter = (rtp) => {
    setSelectedRTPFilter(selectedRTPFilter === rtp ? null : rtp);
  };

  const togglePlacesFilter = (places) => {
    setSelectedPlacesFilter(selectedPlacesFilter === places ? null : places);
  };

  // Toggle function for CVT date filter
  const toggleCvtDateFilter = (cvtDate) => {
    setSelectedCvtDateFilter(selectedCvtDateFilter === cvtDate ? null : cvtDate);
  };

  // Toggle function for provider avatar filter
  const toggleProviderAvatarFilter = (providerId) => {
    setSelectedProviderAvatarFilter(selectedProviderAvatarFilter === providerId ? null : providerId);
  };

  const handleInvoiceClick = (invoice) => {
    setSelectedInvoice(invoice);
    setShowInvoiceDetailsPage(true);
  };

  const handleCloseInvoicePopup = () => {
    setShowInvoicePopup(false);
    setSelectedInvoice(null);
  };

  // Add CVT Date popup handlers
  const handleOpenAddCvtDatePopup = () => {
    setShowAddCvtDatePopup(true);
  };

  const handleCloseAddCvtDatePopup = () => {
    setShowAddCvtDatePopup(false);
  };
  
  const handleCloseJackpotPopup = () => {
    setSelectedJackpots(null);
  };
  
  const handleCloseInvoiceSlotsPopup = () => {
    setSelectedInvoiceSlots(null);
  };

  const handleOpenSlotAttachments = (slotId) => {
    setSelectedSlotId(slotId);
    setShowSlotAttachmentsModal(true);
  };

  const handleCloseSlotAttachments = () => {
    setShowSlotAttachmentsModal(false);
    setSelectedSlotId(null);
  };

  const handleOpenEntityAttachments = (entityType, entityId) => {
    console.log('🔗 Opening entity attachments:', { entityType, entityId });
    setSelectedEntityType(entityType);
    setSelectedEntityId(entityId);
    setShowEntityAttachmentsModal(true);
  };

  const handleCloseEntityAttachments = () => {
    setShowEntityAttachmentsModal(false);
    setSelectedEntityType(null);
    setSelectedEntityId(null);
  };

  const handleOpenCvtAttachments = (cvtId) => {
    setSelectedCvtForAttachments(cvtId);
    setShowCvtAttachments(true);
  };

  const handleCloseCvtAttachments = () => {
    setShowCvtAttachments(false);
    setSelectedCvtForAttachments(null);
  };

  // Change history functions
  const handleOpenChangeHistory = async (entityType, entityId) => {
    try {
      // If entityId is 'all', we'll show a message that we need to select a specific provider
      if (entityId === 'all') {
        showCustomNotification('Please select a specific provider to view its change history', 'info');
        return;
      }
      
      const response = await fetch(`${API}/change-history/${entityType}/${entityId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (response.ok) {
        const historyData = await response.json();
        setChangeHistoryData(historyData);
        setSelectedHistoryEntityType(entityType);
        setSelectedHistoryEntityId(entityId);
        setShowChangeHistoryModal(true);
      } else {
        showCustomNotification('Failed to load change history', 'error');
      }
    } catch (error) {
      console.error('Error loading change history:', error);
      showCustomNotification('Failed to load change history', 'error');
    }
  };

  const handleOpenGlobalChangeHistory = async (entityType) => {
    try {
      const response = await fetch(`${API}/change-history/${entityType}/all`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (response.ok) {
        const historyData = await response.json();
        setChangeHistoryData(historyData);
        setSelectedHistoryEntityType(entityType);
        setSelectedHistoryEntityId('all');
        setShowChangeHistoryModal(true);
      } else {
        showCustomNotification('Failed to load change history', 'error');
      }
    } catch (error) {
      console.error('Error loading change history:', error);
      showCustomNotification('Failed to load change history', 'error');
    }
  };

  // Funcție pentru a încărca numărul de înregistrări din istoric
  const loadChangeHistoryCount = async (entityType) => {
    try {
      const response = await fetch(`${API}/change-history/${entityType}/all`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (response.ok) {
        const historyData = await response.json();
        // Actualizează changeHistoryData pentru a afișa badge-ul corect
        if (entityType === 'slots') {
          setChangeHistoryData(historyData);
          setSelectedHistoryEntityType(entityType);
        }
      }
    } catch (error) {
      console.error('Error loading change history count:', error);
    }
  };

  const handleCloseChangeHistory = () => {
    setShowChangeHistoryModal(false);
    setChangeHistoryData([]);
    setSelectedHistoryEntityType('');
    setSelectedHistoryEntityId('');
  };

  // Funcții pentru All Modifications History
  const handleOpenAllModificationsHistory = async (entityType) => {
    try {
      const response = await fetch(`${API}/change-history/${entityType}/all`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (response.ok) {
        const modificationsData = await response.json();
        setAllModificationsData(modificationsData);
        setSelectedAllModificationsEntityType(entityType);
        setSelectedAllModificationsEntityId('all');
        setShowAllModificationsModal(true);
      } else {
        showCustomNotification('Failed to load all modifications history', 'error');
      }
    } catch (error) {
      console.error('Error loading all modifications history:', error);
      showCustomNotification('Failed to load all modifications history', 'error');
    }
  };

  const handleCloseAllModificationsHistory = () => {
    setShowAllModificationsModal(false);
    setAllModificationsData([]);
    setSelectedAllModificationsEntityType('');
    setSelectedAllModificationsEntityId('');
  };

  const handleMetrologyClick = (metrologyData) => {
    setSelectedMetrology(metrologyData);
  };

  const handleCloseMetrologyPopup = () => {
    setSelectedMetrology(null);
  };

  const handleOpenCommissionDateDetails = (commissionDate) => {
    setSelectedCommissionDate(commissionDate);
    setShowCommissionDateDetailsPage(true);
  };

  const handleCloseCommissionDateDetails = () => {
    setShowCommissionDateDetailsPage(false);
    setSelectedCommissionDate(null);
  };

  const handleShowJackpotDetails = (jackpot) => {
    setSelectedJackpot(jackpot);
    setShowJackpotDetailsPage(true);
  };

  const handleCloseJackpotDetails = () => {
    setShowJackpotDetailsPage(false);
    setSelectedJackpot(null);
  };

  const handleShowMetrologyDetails = (metrology) => {
    setSelectedMetrology(metrology);
    setShowMetrologyDetailsPage(true);
    // Nu seta selectedMetrology pentru MetrologyPopup
  };

  const handleCloseMetrologyDetails = () => {
    setShowMetrologyDetailsPage(false);
    setSelectedMetrology(null);
  };

  const handleShowInvoiceDetails = (invoice) => {
    setSelectedInvoice(invoice);
    setShowInvoiceDetailsPage(true);
  };

  const handleCloseInvoiceDetails = () => {
    setShowInvoiceDetailsPage(false);
    setSelectedInvoice(null);
  };

  const handleShowLocationDetails = (location) => {
    setSelectedLocation(location);
    setShowLocationDetailsPage(true);
  };

  const handleCloseLocationDetails = () => {
    setShowLocationDetailsPage(false);
    setSelectedLocation(null);
  };
  const renderTable = (title, data, columns, actions, entityType) => {
    // Apply search filter
    let filteredData = filterData(data, searchTerm);
    
    // Apply click-to-filter for slot machines
    if (entityType === 'slots') {
      // Apply provider avatar filter FIRST
      if (selectedProviderAvatarFilter) {
        filteredData = filteredData.filter(slot => slot.provider_id === selectedProviderAvatarFilter);
      }
      if (selectedLocationFilter) {
        filteredData = filteredData.filter(slot => slot.location_id === selectedLocationFilter);
      }
      if (selectedProviderFilter) {
        filteredData = filteredData.filter(slot => slot.provider_id === selectedProviderFilter);
      }
      if (selectedCabinetFilter) {
        filteredData = filteredData.filter(slot => slot.cabinet_id === selectedCabinetFilter);
      }
      if (selectedGameMixFilter) {
        filteredData = filteredData.filter(slot => slot.game_mix_id === selectedGameMixFilter);
      }
      if (selectedInvoiceFilter) {
        filteredData = filteredData.filter(slot => slot.invoice_number === selectedInvoiceFilter);
      }
      if (selectedContractFilter) {
        filteredData = filteredData.filter(slot => slot.lease_contract_number === selectedContractFilter);
      }
      if (selectedSerialFilter) {
        filteredData = filteredData.filter(slot => slot.serial_number === selectedSerialFilter);
      }
      if (selectedCompanyFilter) {
        filteredData = filteredData.filter(slot => slot.owner_company_id === selectedCompanyFilter);
      }
      if (selectedRTPFilter) {
        filteredData = filteredData.filter(slot => slot.rtp === selectedRTPFilter);
      }
      if (selectedPlacesFilter) {
        filteredData = filteredData.filter(slot => slot.gaming_places === selectedPlacesFilter);
      }
                      if (selectedCvtDateFilter) {
                  filteredData = filteredData.filter(slot => {
                    // Find metrology record for this slot
                    const metrologyItem = metrology.find(m => {
                      if (!m.serial_number) return false;
                      
                      // Try both newline and space separation
                      const serialNumbersNewline = m.serial_number.split('\n').filter(s => s.trim());
                      const serialNumbersSpace = m.serial_number.split(' ').filter(s => s.trim());
                      
                      // Use the one that has more items (more likely to be correct)
                      const serialNumbers = serialNumbersNewline.length > serialNumbersSpace.length ? 
                        serialNumbersNewline : serialNumbersSpace;
                      
                      return serialNumbers.includes(slot.serial_number);
                    });
                    
                    return metrologyItem?.cvt_expiry_date === selectedCvtDateFilter;
                  });
                }
    }
    
    return (
      <div className="table-container">
        <div className="table-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <h2>{title}</h2>
          </div>
          <div className="table-actions">
            <div className="search-container">
              <input
                type="text"
                placeholder={`Search ${title.toLowerCase()}...`}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
              <span className="search-icon">🔍</span>
            </div>
            {/* Additional buttons - First */}
            {actions?.additionalButtons && actions.additionalButtons.map((button, index) => (
              <button 
                key={index}
                className="btn-secondary"
                onClick={button.onClick}
                title={button.label}
                style={button.style || {}}
              >
                <span className="icon">{button.icon}</span>
                {button.label}
              </button>
            ))}
            

            
            <button 
              className="btn-primary"
              onClick={() => actions?.onAdd && actions.onAdd()}
            >
              <span className="icon">➕</span>
              Add {entityType === 'slots' ? 'Slot' : entityType === 'metrology' ? 'Metrologie' : title.slice(0, -1)}
            </button>
            <button 
              className="btn-secondary"
              onClick={() => actions?.onBulkEdit && actions.onBulkEdit()}
              title="Bulk Edit Selected"
            >
              <span className="icon">📝</span>
              Bulk Edit ({selectedItems.length})
            </button>
            <button 
              className="btn-danger"
              onClick={() => actions?.onBulkDelete && actions.onBulkDelete()}
              title="Bulk Delete Selected"
            >
              <span className="icon">🗑️</span>
              Bulk Delete ({selectedItems.length})
            </button>
            {entityType === 'slots' && (
              <button 
                className="btn-warning"
                onClick={() => actions?.onBulkDuplicate && actions.onBulkDuplicate()}
                title="Duplicate Selected Slots"
              >
                <span className="icon">🔄</span>
                Duplicate ({selectedItems.length})
              </button>
            )}
            <button 
              className="btn-success"
              onClick={() => actions?.onExport && actions.onExport()}
              title="Export Data"
            >
              <span className="icon">📤</span>
              Export
            </button>
            <button 
              className="btn-info"
              onClick={() => actions?.onImport && actions.onImport()}
              title="Import Data"
            >
              <span className="icon">📥</span>
              Import
            </button>
          </div>



            {/* Change History button for Providers */}
            {entityType === 'providers' && (
              <button 
                className="btn-secondary"
                onClick={() => {
                  // Show a dropdown or modal to select which provider's history to view
                  const providerNames = providers.map(p => p.name);
                  const selectedProvider = prompt('Select a provider to view change history:\n\n' + providerNames.map((name, index) => `${index + 1}. ${name}`).join('\n') + '\n\nEnter the number:');
                  
                  if (selectedProvider && !isNaN(selectedProvider)) {
                    const providerIndex = parseInt(selectedProvider) - 1;
                    if (providerIndex >= 0 && providerIndex < providers.length) {
                      const selectedProviderData = providers[providerIndex];
                      handleOpenChangeHistory('providers', selectedProviderData.id);
                    } else {
                      showCustomNotification('Invalid selection', 'error');
                    }
                  }
                }}
                title="View Change History"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  padding: '8px 12px',
                  borderRadius: '6px',
                  border: '1px solid var(--border-color)',
                  background: 'var(--background-secondary)',
                  color: 'var(--text-primary)',
                  cursor: 'pointer',
                  fontSize: '13px',
                  fontWeight: '500',
                  transition: 'all 0.2s ease'
                }}
                onMouseEnter={(e) => {
                  e.target.style.background = 'var(--accent-color)';
                  e.target.style.color = 'white';
                }}
                onMouseLeave={(e) => {
                  e.target.style.background = 'var(--background-secondary)';
                  e.target.style.color = 'var(--text-primary)';
                }}
              >
                <span style={{ fontSize: '14px' }}>📋</span>
                Change History
              </button>
            )}
        </div>
        
        {/* Provider filter avatars for Slot Machines - SECOND ROW */}
        {entityType === 'slots' && (
          <div style={{
            margin: '8px 0 0 0',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            position: 'relative',
            padding: '12px 0',
            minHeight: '60px'
          }}>
            {/* Avatar-urile centrate */}
            <div style={{ flex: 1 }}></div>
            <div style={{
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              gap: '8px',
              flex: 1
            }}>
            {providers.map(provider => (
              <div
                key={provider.id}
                className={`provider-avatar-filter ${selectedProviderAvatarFilter === provider.id ? 'active' : ''}`}
                onClick={() => toggleProviderAvatarFilter(provider.id)}
                title={`Filter by ${provider.name}`}
              >
                <AvatarDisplay entityType="providers" entityId={provider.id} size={30} />
              </div>
            ))}
            </div>
            
            {/* Iconițele în dreapta */}
            <div style={{ 
              display: 'flex', 
              gap: '8px', 
              flex: 1,
              justifyContent: 'flex-end',
              marginRight: '40px',
              alignItems: 'center'
            }}>
              {/* Iconița Timer - Afișează acțiunile programate */}
              <div style={{ position: 'relative' }}>
                <button
                  style={{
                    width: '30px',
                    height: '30px',
                    borderRadius: '50%',
                    border: 'none',
                    background: 'var(--bg-secondary)',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '14px',
                    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)',
                    transition: 'all 0.2s ease'
                  }}
                  onClick={() => {
                    // Deschide modal cu acțiuni programate pentru slot-uri
                    const slotScheduledChanges = scheduledChanges.filter(change => 
                      change.entityType === 'slots'
                    );
                    if (slotScheduledChanges.length > 0) {
                      setShowScheduledChangesModal(true);
                    }
                  }}
                  title="Scheduled actions"
                >
                  ⏱️
                </button>
                {/* Badge cu numărul de acțiuni programate */}
                {(() => {
                  const slotScheduledChanges = scheduledChanges.filter(change => 
                    change.entityType === 'slots'
                  );
                  if (slotScheduledChanges.length > 0) {
                    return (
                      <div style={{
                        position: 'absolute',
                        top: '-3px',
                        right: '-3px',
                        backgroundColor: '#ef4444',
                        color: 'white',
                        borderRadius: '50%',
                        width: '16px',
                        height: '16px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '10px',
                        fontWeight: 'bold',
                        zIndex: 1002
                      }}>
                        {slotScheduledChanges.length}
                      </div>
                    );
                  }
                  return null;
                })()}
              </div>



              {/* All History Changes icon - same format as timer icon */}
              <div style={{ position: 'relative' }}>
                <button
                  style={{
                    width: '30px',
                    height: '30px',
                    borderRadius: '50%',
                    border: 'none',
                    background: 'var(--bg-secondary)',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '14px',
                    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)',
                    transition: 'all 0.2s ease'
                  }}
                  onClick={() => setShowHistoryChangesPage(true)}
                  title="All History Changes"
                >
                  📊
                </button>
              </div>
            </div>
          </div>
        )}
        
        {/* Active Filters Display for Slot Machines */}
        {entityType === 'slots' && (selectedProviderAvatarFilter || selectedLocationFilter || selectedProviderFilter || selectedCabinetFilter || selectedGameMixFilter || selectedInvoiceFilter || selectedContractFilter) && (
          <div className="active-filters-info">
            <strong>Active Filters:</strong>
            {selectedProviderAvatarFilter && (
              <span className="filter-tag">
                👤 Provider: {providers.find(p => p.id === selectedProviderAvatarFilter)?.name || 'Unknown'}
                <button onClick={() => setSelectedProviderAvatarFilter(null)} className="filter-remove">×</button>
              </span>
            )}
            {selectedLocationFilter && (
              <span className="filter-tag">
                📍 Location: {locations.find(l => l.id === selectedLocationFilter)?.name || 'Unknown'}
                <button onClick={() => setSelectedLocationFilter(null)} className="filter-remove">×</button>
              </span>
            )}
            {selectedProviderFilter && (
              <span className="filter-tag">
                🏢 Provider: {providers.find(p => p.id === selectedProviderFilter)?.name || 'Unknown'}
                <button onClick={() => setSelectedProviderFilter(null)} className="filter-remove">×</button>
              </span>
            )}
            {selectedCabinetFilter && (
              <span className="filter-tag">
                🏛️ Cabinet: {cabinets.find(c => c.id === selectedCabinetFilter)?.name || 'Unknown'}
                <button onClick={() => setSelectedCabinetFilter(null)} className="filter-remove">×</button>
              </span>
            )}
            {selectedGameMixFilter && (
              <span className="filter-tag">
                🎮 Game Mix: {gameMixes.find(gm => gm.id === selectedGameMixFilter)?.name || 'Unknown'}
                <button onClick={() => setSelectedGameMixFilter(null)} className="filter-remove">×</button>
              </span>
            )}
            {selectedInvoiceFilter && (
              <span className="filter-tag">
                📄 Invoice: {selectedInvoiceFilter}
                <button onClick={() => setSelectedInvoiceFilter(null)} className="filter-remove">×</button>
              </span>
            )}
            {selectedContractFilter && (
              <span className="filter-tag">
                📋 Contract: {selectedContractFilter}
                <button onClick={() => setSelectedContractFilter(null)} className="filter-remove">×</button>
              </span>
            )}
            {selectedCvtDateFilter && (
              <span className="filter-tag">
                📅 CVT Date: {formatDateDDMMYYYY(selectedCvtDateFilter)}
                <button onClick={() => setSelectedCvtDateFilter(null)} className="filter-remove">×</button>
              </span>
            )}
        </div>
        )}
        <div className="table-content">
          {filteredData.length < data.length && (
            <div className="search-results-info">
              Showing {filteredData.length} of {data.length} results for "{searchTerm}"
            </div>
          )}
          <table className="data-table">
            <thead>
              <tr>
                <th>
                  <input
                    type="checkbox"
                    checked={filteredData.length > 0 && selectedItems.length === filteredData.length}
                    onChange={(e) => handleSelectAll(filteredData, e.target.checked)}
                  />
                </th>
                <th>#</th>
                {columns.map(col => (
                  <th key={col.key}>{col.label}</th>
                ))}
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredData.length === 0 && searchTerm ? (
                <tr>
                  <td colSpan={columns.length + 3} style={{ textAlign: 'center', padding: '2rem' }}>
                    No results found for "{searchTerm}"
                  </td>
                </tr>
              ) : filteredData.length === 0 ? (
                <tr>
                  <td colSpan={columns.length + 3} style={{ textAlign: 'center', padding: '2rem' }}>
                    No {title.toLowerCase()} found
                  </td>
                </tr>
              ) : (
                filteredData.map((item, index) => (
                  <tr key={item.id}>
                    <td>
                      <input
                        type="checkbox"
                        checked={selectedItems.includes(item.id)}
                        onChange={(e) => handleItemSelection(item.id, e.target.checked)}
                      />
                    </td>
                    <td>{index + 1}</td>
                    {columns.map(col => (
                      <td key={`${item.id}-${col.key}`}>
                        {col.render ? col.render(item) : item[col.key] || 'N/A'}
                      </td>
                    ))}
                    <td>
                      {entityType === 'slots' || entityType === 'metrology' ? (
                        <>
                          <div className="table-row-actions-vertical" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                            <div style={{ display: 'flex', gap: '8px', justifyContent: 'center', alignItems: 'center' }}>
                            <button 
                              className="btn-edit"
                              onClick={() => actions?.onEdit && actions.onEdit(item)}
                              title="Edit"
                              style={{ 
                                fontSize: '12px', 
                                padding: '2px 4px',
                                display: 'inline-flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                width: '32px',
                                height: '32px',
                                border: 'none',
                                backgroundColor: '#d1e7ff',
                                borderRadius: '50%',
                                color: '#1e3a8a',
                                cursor: 'pointer'
                              }}
                            >
                              ✏️
                            </button>
                            <button 
                              className="btn-delete"
                              onClick={(e) => {
                                e.preventDefault();
                                e.stopPropagation();
                                handleDeleteEntity(item.id, entityType);
                              }}
                              title={`Delete ${entityType === 'slots' ? 'Slot Machine' : entityType === 'metrology' ? 'CVT Record' : entityType === 'companies' ? 'Company' : entityType === 'locations' ? 'Location' : entityType === 'providers' ? 'Provider' : entityType === 'cabinets' ? 'Cabinet' : entityType === 'gamemixes' ? 'Game Mix' : entityType === 'jackpots' ? 'Jackpot' : entityType === 'invoices' ? 'Invoice' : entityType === 'onjn' ? 'ONJN Report' : entityType === 'legal' ? 'Legal Document' : entityType === 'users' ? 'User' : 'Record'}`}
                              style={{ 
                                fontSize: '12px', 
                                padding: '2px 4px',
                                display: 'inline-flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                width: '32px',
                                height: '32px',
                                border: 'none',
                                backgroundColor: '#d1e7ff',
                                borderRadius: '50%',
                                color: '#1e3a8a',
                                cursor: 'pointer'
                              }}
                            >
                              🗑️
                            </button>
                              {entityType === 'slots' ? (
                            <AttachmentIndicator slotId={item.id} onClick={() => handleOpenSlotAttachments(item.id)} />
                              ) : (
                                <GenericAttachmentIndicator 
                                  entityType={item.entityType === 'comision_dates' ? 'comision_dates' : (item.type === 'comision_date' ? 'comision_dates' : (entityType === 'onjn' ? 'onjn_reports' : entityType))} 
                                  entityId={item.id} 
                                  onClick={() => handleOpenEntityAttachments(item.entityType === 'comision_dates' ? 'comision_dates' : (item.type === 'comision_date' ? 'comision_dates' : (entityType === 'onjn' ? 'onjn_reports' : entityType)), item.id)} 
                                />
                              )}
                            {(() => {
                              const changes = scheduledChanges.filter(change => change.entityType === 'slots' && change.itemId === item.id);
                                if (changes.length > 0) {
                              const change = changes[0];
                              const scheduledDateTime = new Date(change.scheduledDateTime);
                                  const msLeft = scheduledDateTime.getTime() - timerTick;
                              
                              const formatCountdown = (ms) => {
                                if (ms <= 0) return '00:00';
                                const totalSeconds = Math.floor(ms / 1000);
                                const minutes = Math.floor(totalSeconds / 60);
                                const seconds = totalSeconds % 60;
                                return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                              };
                              
                              return (
                                <button 
                                  className="btn-timer"
                                  onClick={() => setShowScheduledChangeForSlot(item.id)}
                                      title="View scheduled action"
                                  style={{ 
                                    fontSize: '12px', 
                                    padding: '2px 4px',
                                    display: 'inline-flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    width: '32px',
                                    height: '32px',
                                    border: 'none',
                                    backgroundColor: '#d1e7ff',
                                    borderRadius: '50%',
                                    color: '#1e3a8a',
                                    cursor: 'pointer',
                                    position: 'relative'
                                  }}
                                >
                                  ⏱️
                                    </button>
                                  );
                                } else {
                                  return (
                                    <button 
                                      className="btn-timer"
                                      onClick={() => {
                                        setScheduleChangeData(item);
                                        setShowScheduleChangeModal(true);
                                      }}
                                      title="Schedule Changes for Slot Machine"
                                      style={{ 
                                        fontSize: '12px', 
                                        padding: '2px 4px',
                                        display: 'inline-flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                        width: '32px',
                                        height: '32px',
                                        border: 'none',
                                        backgroundColor: '#d1e7ff',
                                        borderRadius: '50%',
                                        color: '#1e3a8a',
                                        cursor: 'pointer'
                                      }}
                                    >
                                      ⏱️
                                </button>
                              );
                                }
                            })()}
                          </div>
                          {(entityType === 'slots' || entityType === 'warehouse') && (
                               <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '8px', marginTop: '4px' }}>
                              <label className="switch" style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                                <input
                                  type="checkbox"
                                  checked={item.status === 'active'}
                                  onChange={e => handleSlotStatusChange(item, e.target.checked ? 'active' : 'inactive')}
                                  style={{ display: 'none' }}
                                />
                                <span style={{
                                  width: 36,
                                  height: 20,
                                  background: item.status === 'active' ? 'var(--accent-color)' : '#ccc',
                                  borderRadius: 12,
                                  position: 'relative',
                                  transition: 'background 0.2s',
                                  display: 'inline-block',
                                  marginRight: 6
                                }}>
                                  <span style={{
                                    position: 'absolute',
                                    left: item.status === 'active' ? 18 : 2,
                                    top: 2,
                                    width: 16,
                                    height: 16,
                                    background: '#fff',
                                    borderRadius: '50%',
                                    boxShadow: '0 1px 4px rgba(0,0,0,0.15)',
                                    transition: 'left 0.2s'
                                  }} />
                                </span>
                                <span style={{ fontSize: 14, color: item.status === 'active' ? 'var(--accent-color)' : '#888', fontWeight: 600 }}>
                                  {item.status === 'active' ? '🟢' : '🔴'}
                                </span>
                              </label>
                                 
                                 {/* Timer cu timp rămas - clickabil */}
                                 {(() => {
                                   const changes = scheduledChanges.filter(change => change.entityType === 'slots' && change.itemId === item.id);
                                   if (changes.length > 0) {
                                     const change = changes[0];
                                     const scheduledDateTime = new Date(change.scheduledDateTime);
                                     const msLeft = scheduledDateTime.getTime() - timerTick;
                                     
                                     const formatCountdown = (ms) => {
                                       if (ms <= 0) return '00:00';
                                       const totalSeconds = Math.floor(ms / 1000);
                                       const totalMinutes = Math.floor(totalSeconds / 60);
                                       const totalHours = Math.floor(totalMinutes / 60);
                                       const totalDays = Math.floor(totalHours / 24);
                                       
                                       if (totalDays > 0) {
                                         // Afișează zile, ore, minute
                                         const remainingHours = totalHours % 24;
                                         const remainingMinutes = totalMinutes % 60;
                                         return `${totalDays}d ${remainingHours}h ${remainingMinutes}m`;
                                       } else if (totalHours > 0) {
                                         // Afișează ore, minute
                                         const remainingMinutes = totalMinutes % 60;
                                         return `${totalHours}h ${remainingMinutes}m`;
                                       } else {
                                         // Afișează minute, secunde
                                         const minutes = totalMinutes;
                                         const seconds = totalSeconds % 60;
                                         return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                                       }
                                     };
                                     
                                     return (
                                       <button 
                                         onClick={() => setShowScheduledChangeForSlot(item.id)}
                                         title="Edit scheduled action"
                                         style={{ 
                                           fontSize: '13.9px',
                                           fontWeight: 'bold',
                                           color: '#FF8C00',
                                           background: 'none',
                                           border: 'none',
                                           cursor: 'pointer',
                                           padding: '4px 8px',
                                           borderRadius: '4px',
                                           transition: 'background-color 0.2s'
                                         }}
                                         onMouseEnter={(e) => e.target.style.backgroundColor = '#f0f0f0'}
                                         onMouseLeave={(e) => e.target.style.backgroundColor = 'transparent'}
                                       >
                                         {formatCountdown(msLeft)}
                                       </button>
                                     );
                                   }
                                   return null;
                                 })()}
                            </div>
                          )}
                        </div>
                        </>
                      ) : (
                      <div className="table-row-actions" style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px'
                      }}>
                        <button 
                          className="btn-edit"
                          onClick={() => actions?.onEdit && actions.onEdit(item)}
                          title={`Edit ${entityType === 'slots' ? 'Slot Machine' : entityType === 'metrology' ? 'CVT Record' : entityType === 'companies' ? 'Company' : entityType === 'locations' ? 'Location' : entityType === 'providers' ? 'Provider' : entityType === 'cabinets' ? 'Cabinet' : entityType === 'gamemixes' ? 'Game Mix' : entityType === 'jackpots' ? 'Jackpot' : entityType === 'invoices' ? 'Invoice' : entityType === 'onjn' ? 'ONJN Report' : entityType === 'legal' ? 'Legal Document' : entityType === 'users' ? 'User' : 'Record'}`}
                          style={{ 
                            fontSize: '12px', 
                            padding: '2px 4px',
                            display: 'inline-flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            width: '32px',
                            height: '32px',
                            backgroundColor: '#d1e7ff',
                            borderRadius: '50%',
                            color: '#1e3a8a',
                            border: 'none',
                            cursor: 'pointer'
                                                    }}
                        >
                            ✏️
                        </button>
                        <button 
                          className="btn-delete"
                          onClick={(e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            handleDeleteEntity(item.id, entityType);
                          }}
                          title={`Delete ${entityType === 'slots' ? 'Slot Machine' : entityType === 'metrology' ? 'CVT Record' : entityType === 'companies' ? 'Company' : entityType === 'locations' ? 'Location' : entityType === 'providers' ? 'Provider' : entityType === 'cabinets' ? 'Cabinet' : entityType === 'gamemixes' ? 'Game Mix' : entityType === 'jackpots' ? 'Jackpot' : entityType === 'invoices' ? 'Invoice' : entityType === 'onjn' ? 'ONJN Report' : entityType === 'legal' ? 'Legal Document' : entityType === 'users' ? 'User' : 'Record'}`}
                          style={{ 
                            fontSize: '12px', 
                            padding: '2px 4px',
                            display: 'inline-flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            width: '32px',
                            height: '32px',
                              border: 'none',
                            backgroundColor: '#d1e7ff',
                            borderRadius: '50%',
                            color: '#1e3a8a',
                            cursor: 'pointer'
                          }}
                        >
                            🗑️
                        </button>
                          {entityType === 'slots' ? (
                            <AttachmentIndicator slotId={item.id} onClick={() => handleOpenSlotAttachments(item.id)} />
                          ) : entityType === 'onjn' && item.type === 'comision_date' ? (
                            <GenericAttachmentIndicator entityType="comision_dates" entityId={item.id} onClick={() => handleOpenEntityAttachments("comision_dates", item.id)} />
                          ) : (
                            <GenericAttachmentIndicator entityType={entityType} entityId={item.id} onClick={() => handleOpenEntityAttachments(entityType, item.id)} />
                          )}
                          {entityType === 'slots' && (
                          <button 
                              className="btn-timer"
                            onClick={() => {
                                console.log('Timer button clicked for:', item.id, entityType);
                                showCustomNotification(`Timer clicked for slot: ${item.id}`, 'info');
                                handleEditEntity(item, entityType);
                            }}
                              title="Schedule Changes for Slot Machine"
                            style={{ 
                              fontSize: '14px', 
                                padding: '6px',
                                display: 'inline-block',
                              width: '32px',
                              height: '32px',
                                backgroundColor: '#ff4757',
                              borderRadius: '50%',
                                color: '#ffffff',
                                border: '2px solid #ff0000',
                                cursor: 'pointer',
                                marginLeft: '4px',
                                marginRight: '4px',
                                textAlign: 'center',
                                lineHeight: '20px',
                                zIndex: 9999,
                                position: 'relative'
                              }}
                            >
                              ⏱️
                          </button>
                          )}
                      </div>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    );
  };
  const renderDashboard = () => (
    <div className="dashboard-overview">
      <div className="dashboard-header">
      </div>
      
      {stats && (
        <div className="stats-grid">
          <div className="stat-card clickable" onClick={() => {
            if (showCommissionDateDetailsPage) {
              setShowCommissionDateDetailsPage(false);
              setSelectedCommissionDate(null);
            }
            if (showJackpotDetailsPage) {
              setShowJackpotDetailsPage(false);
              setSelectedJackpot(null);
            }
            if (showMetrologyDetailsPage) {
              setShowMetrologyDetailsPage(false);
              setSelectedMetrology(null);
            }
            if (showLocationDetailsPage) {
              setShowLocationDetailsPage(false);
              setSelectedLocation(null);
            }
            if (showInvoiceDetailsPage) {
              setShowInvoiceDetailsPage(false);
              setSelectedInvoice(null);
            }
            setActiveView('companies');
          }}>
            <div className="stat-icon" style={{ backgroundColor: '#3182ce' }}>📊</div>
            <div className="stat-content">
              <h3>Total Companies</h3>
              <p className="stat-value">{stats.total_companies}</p>
            </div>
          </div>
          <div className="stat-card clickable" onClick={() => {
            if (showCommissionDateDetailsPage) {
              setShowCommissionDateDetailsPage(false);
              setSelectedCommissionDate(null);
            }
            if (showJackpotDetailsPage) {
              setShowJackpotDetailsPage(false);
              setSelectedJackpot(null);
            }
            if (showMetrologyDetailsPage) {
              setShowMetrologyDetailsPage(false);
              setSelectedMetrology(null);
            }
            if (showLocationDetailsPage) {
              setShowLocationDetailsPage(false);
              setSelectedLocation(null);
            }
            if (showInvoiceDetailsPage) {
              setShowInvoiceDetailsPage(false);
              setSelectedInvoice(null);
            }
            setActiveView('locations');
          }}>
            <div className="stat-icon" style={{ backgroundColor: '#3182ce' }}>📍</div>
            <div className="stat-content">
              <h3>Total Locations</h3>
              <p className="stat-value">{stats.total_locations}</p>
            </div>
          </div>
          <div className="stat-card clickable" onClick={() => {
            if (showCommissionDateDetailsPage) {
              setShowCommissionDateDetailsPage(false);
              setSelectedCommissionDate(null);
            }
            if (showJackpotDetailsPage) {
              setShowJackpotDetailsPage(false);
              setSelectedJackpot(null);
            }
            if (showMetrologyDetailsPage) {
              setShowMetrologyDetailsPage(false);
              setSelectedMetrology(null);
            }
            if (showLocationDetailsPage) {
              setShowLocationDetailsPage(false);
              setSelectedLocation(null);
            }
            if (showInvoiceDetailsPage) {
              setShowInvoiceDetailsPage(false);
              setSelectedInvoice(null);
            }
            setActiveView('providers');
          }}>
            <div className="stat-icon" style={{ backgroundColor: '#3182ce' }}>🎮</div>
            <div className="stat-content">
              <h3>Gaming Providers</h3>
              <p className="stat-value">{stats.total_providers}</p>
            </div>
          </div>
          <div className="stat-card clickable" onClick={() => {
            if (showCommissionDateDetailsPage) {
              setShowCommissionDateDetailsPage(false);
              setSelectedCommissionDate(null);
            }
            if (showJackpotDetailsPage) {
              setShowJackpotDetailsPage(false);
              setSelectedJackpot(null);
            }
            if (showMetrologyDetailsPage) {
              setShowMetrologyDetailsPage(false);
              setSelectedMetrology(null);
            }
            if (showLocationDetailsPage) {
              setShowLocationDetailsPage(false);
              setSelectedLocation(null);
            }
            if (showInvoiceDetailsPage) {
              setShowInvoiceDetailsPage(false);
              setSelectedInvoice(null);
            }
            setActiveView('cabinets');
          }}>
            <div className="stat-icon" style={{ backgroundColor: '#ef4444' }}>🎰</div>
            <div className="stat-content">
              <h3>Gaming Cabinets</h3>
              <p className="stat-value">{stats.total_cabinets}</p>
            </div>
          </div>
          <div className="stat-card clickable" onClick={() => {
            if (showCommissionDateDetailsPage) {
              setShowCommissionDateDetailsPage(false);
              setSelectedCommissionDate(null);
            }
            if (showJackpotDetailsPage) {
              setShowJackpotDetailsPage(false);
              setSelectedJackpot(null);
            }
            if (showMetrologyDetailsPage) {
              setShowMetrologyDetailsPage(false);
              setSelectedMetrology(null);
            }
            if (showLocationDetailsPage) {
              setShowLocationDetailsPage(false);
              setSelectedLocation(null);
            }
            if (showInvoiceDetailsPage) {
              setShowInvoiceDetailsPage(false);
              setSelectedInvoice(null);
            }
            setActiveView('slots');
          }}>
            <div className="stat-icon" style={{ backgroundColor: '#8b5cf6' }}>🎯</div>
            <div className="stat-content">
              <h3>Slot Machines</h3>
              <p className="stat-value">{stats.total_slot_machines}</p>
            </div>
          </div>
          <div className="stat-card clickable" onClick={() => {
            if (showCommissionDateDetailsPage) {
              setShowCommissionDateDetailsPage(false);
              setSelectedCommissionDate(null);
            }
            if (showJackpotDetailsPage) {
              setShowJackpotDetailsPage(false);
              setSelectedJackpot(null);
            }
            if (showMetrologyDetailsPage) {
              setShowMetrologyDetailsPage(false);
              setSelectedMetrology(null);
            }
            if (showLocationDetailsPage) {
              setShowLocationDetailsPage(false);
              setSelectedLocation(null);
            }
            if (showInvoiceDetailsPage) {
              setShowInvoiceDetailsPage(false);
              setSelectedInvoice(null);
            }
            setActiveView('dashboard');
          }}>
            <div className="stat-icon" style={{ backgroundColor: '#06b6d4' }}>⚡</div>
            <div className="stat-content">
              <h3>Active Equipment</h3>
              <p className="stat-value">{stats.active_equipment}</p>
            </div>
          </div>
          <div className="stat-card clickable" onClick={() => {
            if (showCommissionDateDetailsPage) {
              setShowCommissionDateDetailsPage(false);
              setSelectedCommissionDate(null);
            }
            if (showJackpotDetailsPage) {
              setShowJackpotDetailsPage(false);
              setSelectedJackpot(null);
            }
            if (showMetrologyDetailsPage) {
              setShowMetrologyDetailsPage(false);
              setSelectedMetrology(null);
            }
            if (showLocationDetailsPage) {
              setShowLocationDetailsPage(false);
              setSelectedLocation(null);
            }
            if (showInvoiceDetailsPage) {
              setShowInvoiceDetailsPage(false);
              setSelectedInvoice(null);
            }
            setActiveView('invoices');
          }}>
            <div className="stat-icon" style={{ backgroundColor: '#3182ce' }}>💰</div>
            <div className="stat-content">
              <h3>Invoices</h3>
              <p className="stat-value">{stats.total_invoices}</p>
            </div>
          </div>
          <div className="stat-card clickable" onClick={() => {
            if (showCommissionDateDetailsPage) {
              setShowCommissionDateDetailsPage(false);
              setSelectedCommissionDate(null);
            }
            if (showJackpotDetailsPage) {
              setShowJackpotDetailsPage(false);
              setSelectedJackpot(null);
            }
            if (showMetrologyDetailsPage) {
              setShowMetrologyDetailsPage(false);
              setSelectedMetrology(null);
            }
            if (showLocationDetailsPage) {
              setShowLocationDetailsPage(false);
              setSelectedLocation(null);
            }
            if (showInvoiceDetailsPage) {
              setShowInvoiceDetailsPage(false);
              setSelectedInvoice(null);
            }
            setActiveView('onjn');
          }}>
            <div className="stat-icon" style={{ backgroundColor: '#3182ce' }}>📋</div>
            <div className="stat-content">
              <h3>ONJN Reports</h3>
              <p className="stat-value">{stats.total_onjn_reports}</p>
            </div>
          </div>
          <div className="stat-card clickable" onClick={() => {
            if (showCommissionDateDetailsPage) {
              setShowCommissionDateDetailsPage(false);
              setSelectedCommissionDate(null);
            }
            if (showJackpotDetailsPage) {
              setShowJackpotDetailsPage(false);
              setSelectedJackpot(null);
            }
            if (showMetrologyDetailsPage) {
              setShowMetrologyDetailsPage(false);
              setSelectedMetrology(null);
            }
            if (showLocationDetailsPage) {
              setShowLocationDetailsPage(false);
              setSelectedLocation(null);
            }
            if (showInvoiceDetailsPage) {
              setShowInvoiceDetailsPage(false);
              setSelectedInvoice(null);
            }
            setActiveView('legal');
          }}>
            <div className="stat-icon" style={{ backgroundColor: '#ef4444' }}>📄</div>
            <div className="stat-content">
              <h3>Legal Documents</h3>
              <p className="stat-value">{stats.total_legal_documents}</p>
            </div>
          </div>
          {user?.role === 'admin' && (
                      <div className="stat-card clickable" onClick={() => {
            if (showCommissionDateDetailsPage) {
              setShowCommissionDateDetailsPage(false);
              setSelectedCommissionDate(null);
            }
            if (showJackpotDetailsPage) {
              setShowJackpotDetailsPage(false);
              setSelectedJackpot(null);
            }
            if (showMetrologyDetailsPage) {
              setShowMetrologyDetailsPage(false);
              setSelectedMetrology(null);
            }
            if (showLocationDetailsPage) {
              setShowLocationDetailsPage(false);
              setSelectedLocation(null);
            }
            if (showInvoiceDetailsPage) {
              setShowInvoiceDetailsPage(false);
              setSelectedInvoice(null);
            }
            setActiveView('users');
          }}>
              <div className="stat-icon" style={{ backgroundColor: '#8b5cf6' }}>👥</div>
              <div className="stat-content">
                <h3>Total Users</h3>
                <p className="stat-value">{stats.total_users}</p>
              </div>
            </div>
          )}
        </div>
      )}

      {stats && stats.recent_activities.length > 0 && (
        <div className="recent-activities">
          <h3>Recent Activities</h3>
          <div className="activities-list">
            {stats.recent_activities.map((activity, index) => (
              <div key={index} className="activity-item">
                <div className="activity-icon">
                  {activity.type === 'company' && '🏢'}
                  {activity.type === 'location' && '📍'}
                  {activity.type === 'provider' && '🎮'}
                  {activity.type === 'cabinet' && '🎰'}
                </div>
                <div className="activity-details">
                  <p><strong>{activity.name}</strong> was {activity.action}</p>
                  <p className="activity-date">{formatDateDDMMYYYY(activity.date)}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
  // Invoice Popup Component
  const InvoicePopup = ({ invoice, onClose }) => {
    if (!invoice) return null;

    // Find location, buyer and seller based on invoice data
    const location = locations.find(location => location.id === invoice.location_id);
    const buyer = companies.find(company => company.id === invoice.buyer_id);
    const seller = providers.find(provider => provider.id === invoice.seller_id);

    // Format amount in Romanian format (15.00,68)
    const formatAmount = (amount) => {
      if (!amount) return '0,00';
      const num = parseFloat(amount);
      if (isNaN(num)) return '0,00';
      
      // Convert to string with 2 decimal places
      const formatted = num.toFixed(2);
      // Split by decimal point
      const parts = formatted.split('.');
      // Add thousands separator (.) and replace decimal point with comma
      const integerPart = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.');
      return `${integerPart},${parts[1]}`;
    };

    // Remove euro symbol from Denomin and Maxbet
    const cleanDescription = (description) => {
      if (!description) return 'No description';
      return description
        .replace(/€/g, '') // Remove euro symbol
        .replace(/EUR/g, '') // Remove EUR text
        .replace(/\s+/g, ' ') // Remove extra spaces
        .trim();
    };

    return (
      <div className="modal-overlay" onClick={onClose}>
        <div className="modal-content invoice-popup" onClick={(e) => e.stopPropagation()}>
          <div className="modal-header">
            <h2>Invoice Details - {invoice.invoice_number}</h2>
            <button className="modal-close" onClick={onClose}>×</button>
          </div>
          <div className="invoice-details">
            <div className="invoice-grid">
              <div className="invoice-field">
                <label>Invoice Number:</label>
                <span>{invoice.invoice_number}</span>
              </div>
              <div className="invoice-field">
                <label>Issue Date:</label>
                <span>{formatDateDDMMYYYY(invoice.issue_date)}</span>
              </div>
              <div className="invoice-field">
                <label>Due Date:</label>
                <span>{formatDateDDMMYYYY(invoice.due_date)}</span>
              </div>
              <div className="invoice-field">
                <label>Amount:</label>
                <span>{formatAmount(invoice.amount)} {invoice.currency || 'EUR'}</span>
              </div>
              <div className="invoice-field">
                <label>Description:</label>
                <span>{cleanDescription(invoice.description)}</span>
              </div>
              <div className="invoice-field">
                <label>Status:</label>
                <span className={`status-badge ${invoice.status || 'pending'}`}>
                  {invoice.status || 'Pending'}
                </span>
              </div>
              <div className="invoice-field">
                <label>Serial Numbers:</label>
                <span>{invoice.serial_numbers || 'N/A'}</span>
              </div>
              <div className="invoice-field">
                <label>Location:</label>
                <span>{location ? location.name : 'N/A'}</span>
              </div>
                              <div className="invoice-field">
                  <label>Customer:</label>
                  <span>{buyer ? buyer.name : 'N/A'}</span>
                </div>
              <div className="invoice-field">
                <label>Seller:</label>
                <span>{seller ? seller.name : 'N/A'}</span>
              </div>
                              <div className="invoice-field">
                  <label>Customer Contact Person:</label>
                  <span>{buyer ? buyer.contact_person : 'N/A'}</span>
                </div>
              <div className="invoice-field">
                <label>Email:</label>
                <span>
                  <span style={{ marginRight: '8px', fontSize: '16px' }}>📧</span>
                  {buyer ? buyer.email : 'N/A'}
                </span>
              </div>
              <div className="invoice-field">
                <label>Phone:</label>
                <span>
                  <span style={{ marginRight: '8px', fontSize: '16px' }}>📞</span>
                  {buyer ? buyer.phone : 'N/A'}
                </span>
              </div>
              <div className="invoice-field">
                <label>Created At:</label>
                <span>{invoice.created_at ? new Date(invoice.created_at).toLocaleString() : 'N/A'}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };
  // Jackpot Popup Component
  const JackpotPopup = ({ jackpots, onClose }) => {
    return (
      <div className="modal-overlay" onClick={onClose}>
        <div className="modal-content" onClick={e => e.stopPropagation()}>
          <div className="modal-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <h2>Jackpot Details</h2>
              <div style={{
                backgroundColor: '#3182ce',
                color: 'white',
                borderRadius: '50%',
                width: '28px',
                height: '28px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '14px',
                fontWeight: 'bold',
                minWidth: '28px'
              }}>
                {jackpots.length}
              </div>
            </div>
            <button className="modal-close" onClick={onClose}>×</button>
          </div>
          <div className="modal-body">
            {jackpots.map((jackpot, index) => (
              <div key={jackpot.id} className="jackpot-item">
                <div className="jackpot-header">
                  <h3>{jackpot.jackpot_name || 'No Name'}</h3>
                  <span className={`jackpot-type ${jackpot.jackpot_type?.toLowerCase()}`}>
                    {jackpot.jackpot_type || 'Unknown'}
                  </span>
                </div>
                
                <div className="jackpot-details">
                  <div>
                    <div className="detail-label">Serial Numbers</div>
                    <div className="detail-value">{jackpot.serial_number || 'N/A'}</div>
                  </div>
                  
                  <div>
                    <div className="detail-label">Increment Percentage</div>
                    <div className="detail-value">
                      {typeof jackpot.increment_rate === 'number' ? `${jackpot.increment_rate}%` : 'N/A'}
                    </div>
                  </div>
                  
                  {jackpot.level_1 && (
                    <div>
                      <div className="detail-label">Level 1</div>
                      <div className="detail-value">{jackpot.level_1}</div>
                    </div>
                  )}
                  
                  {jackpot.level_2 && (
                    <div>
                      <div className="detail-label">Level 2</div>
                      <div className="detail-value">{jackpot.level_2}</div>
                    </div>
                  )}
                  
                  {jackpot.level_3 && (
                    <div>
                      <div className="detail-label">Level 3</div>
                      <div className="detail-value">{jackpot.level_3}</div>
                    </div>
                  )}
                  
                  {jackpot.level_4 && (
                    <div>
                      <div className="detail-label">Level 4</div>
                      <div className="detail-value">{jackpot.level_4}</div>
                    </div>
                  )}
                  
                  {jackpot.level_5 && (
                    <div>
                      <div className="detail-label">Level 5</div>
                      <div className="detail-value">{jackpot.level_5}</div>
                    </div>
                  )}
                  
                  <div>
                    <div className="detail-label">Created Date</div>
                    <div className="detail-value">
                      {jackpot.created_at ? formatDateDDMMYYYY(jackpot.created_at) : 'N/A'}
                    </div>
                  </div>
                </div>
                
                {(jackpot.description || jackpot.details) && (
                  <div className="jackpot-description">
                    <div className="detail-label">Description</div>
                    <div className="detail-value">{jackpot.description || jackpot.details}</div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };
  // Invoice Slots Popup Component
  const InvoiceSlotsPopup = ({ slots, onClose }) => {
    return (
      <div className="modal-overlay" onClick={onClose}>
        <div className="modal-content" onClick={e => e.stopPropagation()}>
          <div className="modal-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <h2>Invoice Slot Details</h2>
              <div style={{
                backgroundColor: '#3182ce',
                color: 'white',
                borderRadius: '50%',
                width: '28px',
                height: '28px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '14px',
                fontWeight: 'bold',
                minWidth: '28px'
              }}>
                {slots.length}
              </div>
            </div>
            <button className="modal-close" onClick={onClose}>×</button>
          </div>
          <div className="modal-body">
            {slots.map((slot, index) => (
              <div key={slot.id} className="jackpot-item">
                <div className="jackpot-header">
                  <h3>Slot: {slot.serial_number || 'Unknown Serial'}</h3>
                  <span className={`jackpot-type ${slot.status?.toLowerCase()}`}>
                    {slot.status || 'Unknown Status'}
                  </span>
                </div>
                
                <div className="jackpot-details">
                  <div>
                    <div className="detail-label">Provider</div>
                    <div className="detail-value">
                      {(() => {
                        const provider = providers.find(p => p.id === slot.provider_id);
                        return provider ? provider.name : 'Unknown Provider';
                      })()}
                    </div>
                  </div>
                  
                  <div>
                    <div className="detail-label">Location</div>
                    <div className="detail-value">
                      {(() => {
                        const location = locations.find(l => l.id === slot.location_id);
                        return location ? location.name : 'Unknown Location';
                      })()}
                    </div>
                  </div>
                  
                  <div>
                    <div className="detail-label">Game Mix</div>
                    <div className="detail-value">
                      {(() => {
                        const gameMix = gameMixes.find(gm => gm.id === slot.game_mix_id);
                        return gameMix ? gameMix.name : 'Unknown Game Mix';
                      })()}
                    </div>
                  </div>
                  
                  <div>
                    <div className="detail-label">Cabinet</div>
                    <div className="detail-value">
                      {(() => {
                        const cabinet = cabinets.find(c => c.id === slot.cabinet_id);
                        return cabinet ? cabinet.name : 'Unknown Cabinet';
                      })()}
                    </div>
                  </div>
                  
                  <div>
                    <div className="detail-label">Production Year</div>
                    <div className="detail-value">{slot.production_year || 'N/A'}</div>
                  </div>
                  
                  <div>
                    <div className="detail-label">RTP</div>
                    <div className="detail-value">{slot.rtp ? `${slot.rtp}%` : 'N/A'}</div>
                  </div>
                  
                  <div>
                    <div className="detail-label">Max Bet</div>
                    <div className="detail-value">{slot.max_bet || 'N/A'}</div>
                  </div>
                  
                  <div>
                    <div className="detail-label">Denomination</div>
                    <div className="detail-value">{slot.denomination || 'N/A'}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
    };
  
  // Metrology Popup Component
  const MetrologyPopup = ({ metrology, onClose }) => {
    if (!metrology) return null;

    return (
      <div className="modal-overlay" onClick={onClose}>
        <div className="modal-content" onClick={e => e.stopPropagation()}>
          <div className="modal-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <h2>Metrology Details</h2>
            </div>
            <button className="modal-close" onClick={onClose}>×</button>
          </div>
          <div className="modal-body">
            <div className="jackpot-item">
              <div className="jackpot-header">
                <h3>Certificate: {metrology.certificate_number || 'No Certificate Number'}</h3>
                <span className={`jackpot-type ${metrology.certificate_type?.toLowerCase()}`}>
                  {metrology.certificate_type || 'Unknown Type'}
                </span>
              </div>
              
              <div className="jackpot-details">
                <div>
                  <div className="detail-label">Serial Numbers</div>
                  <div className="detail-value">{metrology.serial_number || 'N/A'}</div>
                </div>
                
                <div>
                  <div className="detail-label">Issue Date</div>
                  <div className="detail-value">
                    {metrology.issue_date ? formatDateDDMMYYYY(metrology.issue_date) : 'N/A'}
                  </div>
                </div>
                
                <div>
                  <div className="detail-label">Expiry Date</div>
                  <div className="detail-value">
                    {metrology.expiry_date ? formatDateDDMMYYYY(metrology.expiry_date) : 'N/A'}
                  </div>
                </div>
                
                <div>
                  <div className="detail-label">Issuing Authority</div>
                  <div className="detail-value">{metrology.issuing_authority || 'N/A'}</div>
                </div>
                
                <div>
                  <div className="detail-label">Calibration Interval</div>
                  <div className="detail-value">N/A</div>
                </div>
                
                {metrology.cvt_type && (
                  <div>
                    <div className="detail-label">CVT Type</div>
                    <div className="detail-value">{metrology.cvt_type}</div>
                  </div>
                )}
                
                {metrology.cvt_expiry_date && (
                  <div>
                    <div className="detail-label">CVT Expiry Date</div>
                    <div className="detail-value">
                      {formatDateDDMMYYYY(metrology.cvt_expiry_date)}
                    </div>
                  </div>
                )}
                
                <div>
                  <div className="detail-label">Status</div>
                  <div className="detail-value">{metrology.status || 'N/A'}</div>
                </div>
                
                <div>
                  <div className="detail-label">Created Date</div>
                  <div className="detail-value">
                    {metrology.created_at ? formatDateDDMMYYYY(metrology.created_at) : 'N/A'}
                  </div>
                </div>
              </div>
              
              {metrology.description && (
                <div className="jackpot-description">
                  <div className="detail-label">Description</div>
                  <div className="detail-value">{metrology.description}</div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  };
  // Add CVT Date Popup Component
  const AddCvtDatePopup = ({ onClose }) => {
    const [formData, setFormData] = useState({
      serial_numbers: '',
      cvt_date: '',
      cvt_end_date: '',
      cvt_type: 'periodic',
      provider_filter: '',
      cabinet_filter: '',
      game_mix_filter: '',
      license_date_filter: '',
      search_term: ''
    });

    const [filteredSlots, setFilteredSlots] = useState([]);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [validationErrors, setValidationErrors] = useState({});

    const handleChange = (field, value) => {
      setFormData(prev => ({
        ...prev,
        [field]: value
      }));
      
      // Clear validation error when user starts typing
      if (validationErrors[field]) {
        setValidationErrors(prev => ({
          ...prev,
          [field]: null
        }));
      }
    };

    const validateForm = () => {
      const errors = {};
      const serialNumbers = formData.serial_numbers.split(' ').filter(sn => sn.trim());
      
      if (!formData.serial_numbers.trim()) {
        errors.serial_numbers = 'Serial numbers are required';
      } else if (serialNumbers.length === 0) {
        errors.serial_numbers = 'Please enter at least one valid serial number';
      }
      
      if (!formData.cvt_date) {
        errors.cvt_date = 'CVT date is required';
      }
      
      if (!formData.cvt_end_date) {
        errors.cvt_end_date = 'CVT end date is required';
      } else if (formData.cvt_date && formData.cvt_end_date && formData.cvt_end_date <= formData.cvt_date) {
        errors.cvt_end_date = 'End date must be after start date';
      }
      
      setValidationErrors(errors);
      return Object.keys(errors).length === 0;
    };

    const handleSubmit = async (e) => {
      e.preventDefault();
      
      if (!validateForm()) {
        return;
      }
      
      setIsSubmitting(true);
      
      try {
        const token = localStorage.getItem('token');
        const serialNumbers = formData.serial_numbers.split(' ').filter(sn => sn.trim());
        
        // Create metrology records for each serial number
        const promises = serialNumbers.map(async (serialNumber) => {
          const metrologyData = {
            serial_number: serialNumber.trim(),
            certificate_number: `CVT-${serialNumber}-${new Date().getFullYear()}`,
            certificate_type: 'calibration',
            issue_date: formData.cvt_date,

            issuing_authority: 'ANM',
            cvt_expiry_date: formData.cvt_end_date,
            cvt_type: formData.cvt_type,
            status: 'active',
            description: `CVT ${formData.cvt_type} certificate for ${serialNumber}`
          };

          const response = await fetch(`${API}/metrology`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(metrologyData)
          });

          if (!response.ok) {
            throw new Error(`Failed to create CVT for ${serialNumber}`);
          }

          return response.json();
        });

        await Promise.all(promises);
        showCustomNotification(`✅ Successfully created CVT records for ${serialNumbers.length} slot(s)!`, 'success');
        onClose();
        fetchDashboardData(); // Refresh data
      } catch (error) {
        console.error('Error creating CVT records:', error);
        showCustomNotification(`❌ Error creating CVT records: ${error.message}`, 'error');
      } finally {
        setIsSubmitting(false);
      }
    };

    // Filter slots based on search criteria
    useEffect(() => {
      let filtered = slotMachines.filter(slot => slot.status === 'active');
      
      if (formData.provider_filter) {
        filtered = filtered.filter(slot => slot.provider_id === formData.provider_filter);
      }
      
      if (formData.cabinet_filter) {
        filtered = filtered.filter(slot => slot.cabinet_id === formData.cabinet_filter);
      }
      
      if (formData.game_mix_filter) {
        filtered = filtered.filter(slot => slot.game_mix_id === formData.game_mix_filter);
      }
      
      if (formData.license_date_filter) {
        filtered = filtered.filter(slot => slot.commission_date === formData.license_date_filter);
      }
      
      if (formData.search_term) {
        const searchLower = formData.search_term.toLowerCase();
        filtered = filtered.filter(slot => 
          slot.serial_number.toLowerCase().includes(searchLower)
        );
      }
      
      setFilteredSlots(filtered);
    }, [formData, slotMachines]);
    const selectedSerials = formData.serial_numbers.split(' ').filter(sn => sn.trim());
    return (
      <div className="modal-overlay">
        <div className="modal-content" style={{ 
          maxWidth: '1000px', 
          width: '95vw',
          maxHeight: '90vh', 
          overflow: 'auto',
          background: 'var(--bg-secondary)',
          borderRadius: '16px',
          boxShadow: '0 25px 50px rgba(0,0,0,0.4)',
          border: '1px solid var(--border-color)'
        }}>
          <div className="modal-header" style={{
            background: 'linear-gradient(135deg, var(--bg-primary) 0%, var(--accent-color) 100%)',
            borderBottom: '2px solid var(--border-color)',
            padding: '24px 32px',
            borderRadius: '16px 16px 0 0',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <h2 style={{ 
              margin: 0, 
              color: 'var(--text-primary)', 
              fontSize: '1.8rem',
              fontWeight: 'bold',
              textShadow: '0 2px 4px rgba(0,0,0,0.3)'
            }}>
              🔧 CVT Metrology Administration
            </h2>
            <button 
              className="modal-close" 
              onClick={onClose}
              style={{
                background: 'rgba(255,255,255,0.1)',
                border: '1px solid rgba(255,255,255,0.2)',
                fontSize: '1.8rem',
                cursor: 'pointer',
                color: 'var(--text-primary)',
                padding: '8px 12px',
                borderRadius: '8px',
                transition: 'all 0.3s ease',
                backdropFilter: 'blur(10px)'
              }}
              onMouseOver={(e) => {
                e.target.style.background = 'rgba(255,255,255,0.2)';
                e.target.style.transform = 'scale(1.1)';
              }}
              onMouseOut={(e) => {
                e.target.style.background = 'rgba(255,255,255,0.1)';
                e.target.style.transform = 'scale(1)';
              }}
            >
              ✕
            </button>
          </div>
          
          <form onSubmit={handleSubmit} className="modal-form" style={{ padding: '32px' }}>
            {/* Quick Actions */}
            <div style={{ 
              background: 'linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%)', 
              padding: '24px', 
              borderRadius: '12px', 
              marginBottom: '24px',
              border: '2px solid var(--border-color)',
              boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
            }}>
              <h3 style={{ 
                margin: '0 0 16px 0', 
                color: 'var(--text-primary)', 
                fontSize: '1.3rem',
                fontWeight: 'bold',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}>
                ⚡ Quick Actions
              </h3>
              <div style={{ 
                display: 'flex', 
                gap: '16px', 
                flexWrap: 'wrap',
                alignItems: 'center'
              }}>
                <button
                  type="button"
                  onClick={() => {
                    const allSerials = filteredSlots.map(slot => slot.serial_number).join(' ');
                    handleChange('serial_numbers', allSerials);
                  }}
                  style={{
                    background: 'linear-gradient(135deg, var(--accent-color) 0%, #0056b3 100%)',
                    color: 'white',
                    border: 'none',
                    padding: '12px 20px',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    fontSize: '1rem',
                    fontWeight: 'bold',
                    transition: 'all 0.3s ease',
                    boxShadow: '0 4px 8px rgba(0,0,0,0.2)'
                  }}
                  onMouseOver={(e) => {
                    e.target.style.transform = 'translateY(-2px)';
                    e.target.style.boxShadow = '0 6px 12px rgba(0,0,0,0.3)';
                  }}
                  onMouseOut={(e) => {
                    e.target.style.transform = 'translateY(0)';
                    e.target.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
                  }}
                >
                  📋 Select All ({filteredSlots.length})
                </button>
                <button
                  type="button"
                  onClick={() => handleChange('serial_numbers', '')}
                  style={{
                    background: 'linear-gradient(135deg, var(--danger-color) 0%, #c53030 100%)',
                    color: 'white',
                    border: 'none',
                    padding: '12px 20px',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    fontSize: '1rem',
                    fontWeight: 'bold',
                    transition: 'all 0.3s ease',
                    boxShadow: '0 4px 8px rgba(0,0,0,0.2)'
                  }}
                  onMouseOver={(e) => {
                    e.target.style.transform = 'translateY(-2px)';
                    e.target.style.boxShadow = '0 6px 12px rgba(0,0,0,0.3)';
                  }}
                  onMouseOut={(e) => {
                    e.target.style.transform = 'translateY(0)';
                    e.target.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
                  }}
                >
                  🗑️ Clear All
                </button>
                <div style={{ 
                  background: 'var(--bg-secondary)',
                  padding: '12px 16px',
                  borderRadius: '8px',
                  border: '1px solid var(--border-color)',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px'
                }}>
                  <span style={{ fontSize: '1.2rem' }}>🎯</span>
                  <span style={{ 
                    color: 'var(--text-primary)', 
                    fontSize: '1rem',
                    fontWeight: 'bold'
                  }}>
                    Selected: <span style={{ color: 'var(--accent-color)' }}>{selectedSerials.length}</span> slot(s)
                  </span>
                </div>
              </div>
            </div>

            {/* Filters Section */}
            <div style={{ 
              background: 'linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%)', 
              padding: '24px', 
              borderRadius: '12px', 
              marginBottom: '24px',
              border: '2px solid var(--border-color)',
              boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
            }}>
              <h3 style={{ 
                margin: '0 0 20px 0', 
                color: 'var(--text-primary)', 
                fontSize: '1.3rem',
                fontWeight: 'bold',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}>
                🔍 Advanced Filters
              </h3>
              <div style={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
                gap: '20px' 
              }}>
                <div className="form-group">
                  <label style={{ 
                    color: 'var(--text-primary)', 
                    marginBottom: '8px', 
                    display: 'block',
                    fontSize: '1rem',
                    fontWeight: 'bold'
                  }}>
                    🏢 Provider
                  </label>
                  <select
                    value={formData.provider_filter}
                    onChange={(e) => handleChange('provider_filter', e.target.value)}
                    style={{
                      width: '100%',
                      padding: '14px 16px',
                      border: '2px solid var(--border-color)',
                      borderRadius: '8px',
                      background: 'var(--bg-secondary)',
                      color: 'var(--text-primary)',
                      fontSize: '1rem',
                      transition: 'all 0.3s ease',
                      cursor: 'pointer'
                    }}
                    onFocus={(e) => {
                      e.target.style.borderColor = 'var(--accent-color)';
                      e.target.style.boxShadow = '0 0 0 3px rgba(0, 212, 255, 0.1)';
                    }}
                    onBlur={(e) => {
                      e.target.style.borderColor = 'var(--border-color)';
                      e.target.style.boxShadow = 'none';
                    }}
                  >
                    <option value="">🌐 All Providers</option>
                    {providers.map(provider => (
                      <option key={provider.id} value={provider.id}>🏢 {provider.name}</option>
                    ))}
                  </select>
                </div>
                
                <div className="form-group">
                  <label style={{ 
                    color: 'var(--text-primary)', 
                    marginBottom: '8px', 
                    display: 'block',
                    fontSize: '1rem',
                    fontWeight: 'bold'
                  }}>
                    🎰 Cabinet
                  </label>
                  <select
                    value={formData.cabinet_filter}
                    onChange={(e) => handleChange('cabinet_filter', e.target.value)}
                    style={{
                      width: '100%',
                      padding: '14px 16px',
                      border: '2px solid var(--border-color)',
                      borderRadius: '8px',
                      background: 'var(--bg-secondary)',
                      color: 'var(--text-primary)',
                      fontSize: '1rem',
                      transition: 'all 0.3s ease',
                      cursor: 'pointer'
                    }}
                    onFocus={(e) => {
                      e.target.style.borderColor = 'var(--accent-color)';
                      e.target.style.boxShadow = '0 0 0 3px rgba(0, 212, 255, 0.1)';
                    }}
                    onBlur={(e) => {
                      e.target.style.borderColor = 'var(--border-color)';
                      e.target.style.boxShadow = 'none';
                    }}
                  >
                    <option value="">🎰 All Cabinets</option>
                    {cabinets.map(cabinet => (
                      <option key={cabinet.id} value={cabinet.id}>🎰 {cabinet.name}</option>
                    ))}
                  </select>
                </div>
                
                <div className="form-group">
                  <label style={{ 
                    color: 'var(--text-primary)', 
                    marginBottom: '8px', 
                    display: 'block',
                    fontSize: '1rem',
                    fontWeight: 'bold'
                  }}>
                    🎮 Game Mix
                  </label>
                  <select
                    value={formData.game_mix_filter}
                    onChange={(e) => handleChange('game_mix_filter', e.target.value)}
                    style={{
                      width: '100%',
                      padding: '14px 16px',
                      border: '2px solid var(--border-color)',
                      borderRadius: '8px',
                      background: 'var(--bg-secondary)',
                      color: 'var(--text-primary)',
                      fontSize: '1rem',
                      transition: 'all 0.3s ease',
                      cursor: 'pointer'
                    }}
                    onFocus={(e) => {
                      e.target.style.borderColor = 'var(--accent-color)';
                      e.target.style.boxShadow = '0 0 0 3px rgba(0, 212, 255, 0.1)';
                    }}
                    onBlur={(e) => {
                      e.target.style.borderColor = 'var(--border-color)';
                      e.target.style.boxShadow = 'none';
                    }}
                  >
                    <option value="">🎮 All Game Mixes</option>
                    {gameMixes.map(gameMix => (
                      <option key={gameMix.id} value={gameMix.id}>🎮 {gameMix.name}</option>
                    ))}
                  </select>
                </div>
                
                <div className="form-group">
                  <label style={{ 
                    color: 'var(--text-primary)', 
                    marginBottom: '8px', 
                    display: 'block',
                    fontSize: '1rem',
                    fontWeight: 'bold'
                  }}>
                    📅 License Date
                  </label>
                  <input
                    type="date"
                    value={formData.license_date_filter}
                    onChange={(e) => handleChange('license_date_filter', e.target.value)}
                    style={{
                      width: '100%',
                      padding: '14px 16px',
                      border: '2px solid var(--border-color)',
                      borderRadius: '8px',
                      background: 'var(--bg-secondary)',
                      color: 'var(--text-primary)',
                      fontSize: '1rem',
                      transition: 'all 0.3s ease'
                    }}
                    onFocus={(e) => {
                      e.target.style.borderColor = 'var(--accent-color)';
                      e.target.style.boxShadow = '0 0 0 3px rgba(0, 212, 255, 0.1)';
                    }}
                    onBlur={(e) => {
                      e.target.style.borderColor = 'var(--border-color)';
                      e.target.style.boxShadow = 'none';
                    }}
                  />
                </div>
              </div>
              
              <div className="form-group" style={{ marginTop: '20px' }}>
                <label style={{ 
                  color: 'var(--text-primary)', 
                  marginBottom: '8px', 
                  display: 'block',
                  fontSize: '1rem',
                  fontWeight: 'bold'
                }}>
                  🔍 Search Serial Numbers
                </label>
                <input
                  type="text"
                  value={formData.search_term}
                  onChange={(e) => handleChange('search_term', e.target.value)}
                  placeholder="🔍 Enter serial numbers to search..."
                  style={{
                    width: '100%',
                    padding: '16px 20px',
                    border: '2px solid var(--border-color)',
                    borderRadius: '10px',
                    background: 'var(--bg-secondary)',
                    color: 'var(--text-primary)',
                    fontSize: '1.1rem',
                    transition: 'all 0.3s ease'
                  }}
                  onFocus={(e) => {
                    e.target.style.borderColor = 'var(--accent-color)';
                    e.target.style.boxShadow = '0 0 0 3px rgba(0, 212, 255, 0.1)';
                    e.target.style.transform = 'scale(1.02)';
                  }}
                  onBlur={(e) => {
                    e.target.style.borderColor = 'var(--border-color)';
                    e.target.style.boxShadow = 'none';
                    e.target.style.transform = 'scale(1)';
                  }}
                />
              </div>
            </div>
            
            {/* CVT Information Section */}
            <div style={{ 
              background: 'linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%)', 
              padding: '24px', 
              borderRadius: '12px', 
              marginBottom: '24px',
              border: '2px solid var(--border-color)',
              boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
            }}>
              <h3 style={{ 
                margin: '0 0 20px 0', 
                color: 'var(--text-primary)', 
                fontSize: '1.3rem',
                fontWeight: 'bold',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}>
                📋 CVT Information
              </h3>
              <div style={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', 
                gap: '20px' 
              }}>
                <div className="form-group">
                  <label style={{ 
                    color: 'var(--text-primary)', 
                    marginBottom: '8px', 
                    display: 'block',
                    fontSize: '1rem',
                    fontWeight: 'bold'
                  }}>
                    🎰 Slot Serial Numbers *
                  </label>
                  <textarea
                    value={formData.serial_numbers}
                    onChange={(e) => handleChange('serial_numbers', e.target.value)}
                    placeholder="🎰 Enter serial numbers separated by spaces (e.g., SN001 SN002 SN003)"
                    rows="4"
                    required
                    style={{
                      width: '100%',
                      padding: '16px 20px',
                      border: validationErrors.serial_numbers ? '3px solid #ff4444' : '2px solid var(--border-color)',
                      borderRadius: '10px',
                      background: 'var(--bg-secondary)',
                      color: 'var(--text-primary)',
                      fontSize: '1.1rem',
                      resize: 'vertical',
                      transition: 'all 0.3s ease',
                      fontFamily: 'monospace'
                    }}
                    onFocus={(e) => {
                      if (!validationErrors.serial_numbers) {
                        e.target.style.borderColor = 'var(--accent-color)';
                        e.target.style.boxShadow = '0 0 0 3px rgba(0, 212, 255, 0.1)';
                      }
                    }}
                    onBlur={(e) => {
                      if (!validationErrors.serial_numbers) {
                        e.target.style.borderColor = 'var(--border-color)';
                        e.target.style.boxShadow = 'none';
                      }
                    }}
                  />
                  {validationErrors.serial_numbers && (
                    <div style={{ 
                      color: '#ff4444', 
                      fontSize: '0.9rem', 
                      marginTop: '8px',
                      padding: '8px 12px',
                      background: 'rgba(255, 68, 68, 0.1)',
                      borderRadius: '6px',
                      border: '1px solid rgba(255, 68, 68, 0.3)'
                    }}>
                      ⚠️ {validationErrors.serial_numbers}
                    </div>
                  )}
                  <div style={{ 
                    marginTop: '8px',
                    padding: '8px 12px',
                    background: 'var(--bg-primary)',
                    borderRadius: '6px',
                    border: '1px solid var(--border-color)'
                  }}>
                    <small style={{ 
                      color: 'var(--text-secondary)', 
                      fontSize: '0.9rem',
                      fontWeight: 'bold'
                    }}>
                      📊 Available slots: <span style={{ color: 'var(--accent-color)' }}>{filteredSlots.length}</span>
                    </small>
                  </div>
                </div>
                
                <div className="form-group">
                  <label style={{ 
                    color: 'var(--text-primary)', 
                    marginBottom: '8px', 
                    display: 'block',
                    fontSize: '1rem',
                    fontWeight: 'bold'
                  }}>
                    📅 CVT Start Date *
                  </label>
                  <input
                    type="date"
                    value={formData.cvt_date}
                    onChange={(e) => handleChange('cvt_date', e.target.value)}
                    required
                    style={{
                      width: '100%',
                      padding: '16px 20px',
                      border: validationErrors.cvt_date ? '3px solid #ff4444' : '2px solid var(--border-color)',
                      borderRadius: '10px',
                      background: 'var(--bg-secondary)',
                      color: 'var(--text-primary)',
                      fontSize: '1.1rem',
                      transition: 'all 0.3s ease'
                    }}
                    onFocus={(e) => {
                      if (!validationErrors.cvt_date) {
                        e.target.style.borderColor = 'var(--accent-color)';
                        e.target.style.boxShadow = '0 0 0 3px rgba(0, 212, 255, 0.1)';
                      }
                    }}
                    onBlur={(e) => {
                      if (!validationErrors.cvt_date) {
                        e.target.style.borderColor = 'var(--border-color)';
                        e.target.style.boxShadow = 'none';
                      }
                    }}
                  />
                  {validationErrors.cvt_date && (
                    <div style={{ 
                      color: '#ff4444', 
                      fontSize: '0.9rem', 
                      marginTop: '8px',
                      padding: '8px 12px',
                      background: 'rgba(255, 68, 68, 0.1)',
                      borderRadius: '6px',
                      border: '1px solid rgba(255, 68, 68, 0.3)'
                    }}>
                      ⚠️ {validationErrors.cvt_date}
                    </div>
                  )}
                </div>
                
                <div className="form-group">
                  <label style={{ 
                    color: 'var(--text-primary)', 
                    marginBottom: '8px', 
                    display: 'block',
                    fontSize: '1rem',
                    fontWeight: 'bold'
                  }}>
                    📅 CVT End Date *
                  </label>
                  <input
                    type="date"
                    value={formData.cvt_end_date}
                    onChange={(e) => handleChange('cvt_end_date', e.target.value)}
                    required
                    style={{
                      width: '100%',
                      padding: '16px 20px',
                      border: validationErrors.cvt_end_date ? '3px solid #ff4444' : '2px solid var(--border-color)',
                      borderRadius: '10px',
                      background: 'var(--bg-secondary)',
                      color: 'var(--text-primary)',
                      fontSize: '1.1rem',
                      transition: 'all 0.3s ease'
                    }}
                    onFocus={(e) => {
                      if (!validationErrors.cvt_end_date) {
                        e.target.style.borderColor = 'var(--accent-color)';
                        e.target.style.boxShadow = '0 0 0 3px rgba(0, 212, 255, 0.1)';
                      }
                    }}
                    onBlur={(e) => {
                      if (!validationErrors.cvt_end_date) {
                        e.target.style.borderColor = 'var(--border-color)';
                        e.target.style.boxShadow = 'none';
                      }
                    }}
                  />
                  {validationErrors.cvt_end_date && (
                    <div style={{ 
                      color: '#ff4444', 
                      fontSize: '0.9rem', 
                      marginTop: '8px',
                      padding: '8px 12px',
                      background: 'rgba(255, 68, 68, 0.1)',
                      borderRadius: '6px',
                      border: '1px solid rgba(255, 68, 68, 0.3)'
                    }}>
                      ⚠️ {validationErrors.cvt_end_date}
                    </div>
                  )}
                </div>
                
                <div className="form-group">
                  <label style={{ 
                    color: 'var(--text-primary)', 
                    marginBottom: '8px', 
                    display: 'block',
                    fontSize: '1rem',
                    fontWeight: 'bold'
                  }}>
                    🔧 CVT Type *
                  </label>
                  <select
                    value={formData.cvt_type}
                    onChange={(e) => handleChange('cvt_type', e.target.value)}
                    required
                    style={{
                      width: '100%',
                      padding: '16px 20px',
                      border: '2px solid var(--border-color)',
                      borderRadius: '10px',
                      background: 'var(--bg-secondary)',
                      color: 'var(--text-primary)',
                      fontSize: '1.1rem',
                      transition: 'all 0.3s ease',
                      cursor: 'pointer'
                    }}
                    onFocus={(e) => {
                      e.target.style.borderColor = 'var(--accent-color)';
                      e.target.style.boxShadow = '0 0 0 3px rgba(0, 212, 255, 0.1)';
                    }}
                    onBlur={(e) => {
                      e.target.style.borderColor = 'var(--border-color)';
                      e.target.style.boxShadow = 'none';
                    }}
                  >
                    <option value="periodic">🔄 Periodic Verification</option>
                    <option value="reparation">🔧 Reparation Verification</option>
                  </select>
                </div>
              </div>
            </div>
            
            {/* Available Slots Section */}
            <div style={{ 
              background: 'linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%)', 
              padding: '24px', 
              borderRadius: '12px', 
              marginBottom: '24px',
              border: '2px solid var(--border-color)',
              boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
            }}>
              <h3 style={{ 
                margin: '0 0 20px 0', 
                color: 'var(--text-primary)', 
                fontSize: '1.3rem',
                fontWeight: 'bold',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}>
                🎰 Available Slots
              </h3>
              <div style={{ 
                maxHeight: '300px', 
                overflow: 'auto', 
                border: '2px solid var(--border-color)', 
                padding: '20px',
                borderRadius: '10px',
                background: 'var(--bg-secondary)',
                boxShadow: 'inset 0 2px 4px rgba(0,0,0,0.1)'
              }}>
                {filteredSlots.length === 0 ? (
                  <div style={{ 
                    color: 'var(--text-secondary)', 
                    fontStyle: 'italic',
                    textAlign: 'center',
                    padding: '40px 20px',
                    background: 'var(--bg-primary)',
                    borderRadius: '8px',
                    border: '2px dashed var(--border-color)'
                  }}>
                    <div style={{ fontSize: '3rem', marginBottom: '16px' }}>🔍</div>
                    <div style={{ fontSize: '1.2rem', fontWeight: 'bold', marginBottom: '8px' }}>
                      No slots match the current filters
                    </div>
                    <div style={{ fontSize: '1rem' }}>
                      Try adjusting your search criteria
                    </div>
                  </div>
                ) : (
                  <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 1fr))', 
                    gap: '12px' 
                  }}>
                    {filteredSlots.map(slot => (
                      <div key={slot.id} 
                        style={{ 
                          padding: '12px 16px', 
                          border: selectedSerials.includes(slot.serial_number) ? '3px solid var(--accent-color)' : '2px solid var(--border-color)', 
                          borderRadius: '10px',
                          fontSize: '1rem',
                          cursor: 'pointer',
                          backgroundColor: selectedSerials.includes(slot.serial_number) ? 'var(--accent-color)' : 'var(--bg-primary)',
                          color: selectedSerials.includes(slot.serial_number) ? 'white' : 'var(--text-primary)',
                          transition: 'all 0.3s ease',
                          textAlign: 'center',
                          fontWeight: selectedSerials.includes(slot.serial_number) ? 'bold' : 'normal',
                          boxShadow: selectedSerials.includes(slot.serial_number) ? '0 4px 12px rgba(0, 212, 255, 0.3)' : '0 2px 4px rgba(0,0,0,0.1)',
                          transform: selectedSerials.includes(slot.serial_number) ? 'scale(1.05)' : 'scale(1)'
                        }}
                        onClick={() => {
                          const currentSerials = formData.serial_numbers.split(' ').filter(sn => sn.trim());
                          if (currentSerials.includes(slot.serial_number)) {
                            // Remove if already selected
                            const newSerials = currentSerials.filter(sn => sn !== slot.serial_number);
                            handleChange('serial_numbers', newSerials.join(' '));
                          } else {
                            // Add if not selected
                            const newSerials = [...currentSerials, slot.serial_number];
                            handleChange('serial_numbers', newSerials.join(' '));
                          }
                        }}
                        onMouseOver={(e) => {
                          if (!selectedSerials.includes(slot.serial_number)) {
                            e.target.style.background = 'var(--bg-hover)';
                            e.target.style.transform = 'scale(1.02)';
                            e.target.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
                          }
                        }}
                        onMouseOut={(e) => {
                          if (!selectedSerials.includes(slot.serial_number)) {
                            e.target.style.background = 'var(--bg-primary)';
                            e.target.style.transform = 'scale(1)';
                            e.target.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
                          }
                        }}
                      >
                        {slot.serial_number}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
            
            {/* Action Buttons */}
            <div style={{ 
              display: 'flex', 
              gap: '16px', 
              justifyContent: 'flex-end',
              padding: '24px 0 0 0',
              borderTop: '2px solid var(--border-color)',
              marginTop: '24px'
            }}>
              <button 
                type="button" 
                onClick={onClose}
                style={{
                  background: 'linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%)',
                  color: 'var(--text-primary)',
                  border: '2px solid var(--border-color)',
                  padding: '16px 32px',
                  borderRadius: '10px',
                  cursor: 'pointer',
                  fontSize: '1.1rem',
                  fontWeight: 'bold',
                  transition: 'all 0.3s ease',
                  boxShadow: '0 4px 8px rgba(0,0,0,0.1)'
                }}
                onMouseOver={(e) => {
                  e.target.style.background = 'linear-gradient(135deg, var(--bg-hover) 0%, var(--bg-secondary) 100%)';
                  e.target.style.transform = 'translateY(-2px)';
                  e.target.style.boxShadow = '0 6px 12px rgba(0,0,0,0.2)';
                }}
                onMouseOut={(e) => {
                  e.target.style.background = 'linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%)';
                  e.target.style.transform = 'translateY(0)';
                  e.target.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
                }}
              >
                ❌ Cancel
              </button>
              <button 
                type="submit" 
                disabled={isSubmitting}
                style={{
                  background: isSubmitting 
                    ? 'linear-gradient(135deg, var(--text-secondary) 0%, #666 100%)' 
                    : 'linear-gradient(135deg, var(--accent-color) 0%, #0056b3 100%)',
                  color: 'white',
                  border: 'none',
                  padding: '16px 32px',
                  borderRadius: '10px',
                  cursor: isSubmitting ? 'not-allowed' : 'pointer',
                  fontSize: '1.1rem',
                  fontWeight: 'bold',
                  transition: 'all 0.3s ease',
                  opacity: isSubmitting ? 0.7 : 1,
                  boxShadow: isSubmitting 
                    ? '0 2px 4px rgba(0,0,0,0.1)' 
                    : '0 4px 12px rgba(0, 212, 255, 0.3)'
                }}
                onMouseOver={(e) => {
                  if (!isSubmitting) {
                    e.target.style.transform = 'translateY(-2px)';
                    e.target.style.boxShadow = '0 6px 16px rgba(0, 212, 255, 0.4)';
                  }
                }}
                onMouseOut={(e) => {
                  if (!isSubmitting) {
                    e.target.style.transform = 'translateY(0)';
                    e.target.style.boxShadow = '0 4px 12px rgba(0, 212, 255, 0.3)';
                  }
                }}
              >
                {isSubmitting ? '⏳ Creating CVT Records...' : '✅ Create CVT Records'}
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  };

  // Report Details Modal Component
  const ReportDetailsModal = ({ report, onClose }) => {
    if (!report) return null;

    const renderCommissionDateDetails = () => {
      const serials = report.serial_numbers ? report.serial_numbers.split(/\s+/).filter(s => s.trim()) : [];
      const associatedSlots = slotMachines.filter(slot => 
        serials.includes(slot.serial_number)
      );

      // Funcție pentru a găsi informațiile asociate
      const getSlotDetails = (slot) => {
        const location = locations.find(loc => loc.id === slot.location_id);
        const provider = providers.find(prov => prov.id === slot.provider_id);
        const cabinet = cabinets.find(cab => cab.id === slot.cabinet_id);
        const gameMix = gameMixes.find(gm => gm.id === slot.game_mix_id);
        const metrology = metrologyData.find(met => met.serial_number === slot.serial_number);
        const jackpot = jackpots.find(jp => jp.serial_number === slot.serial_number);

        return {
          location: location?.name || 'N/A',
          provider: provider?.name || 'N/A',
          cabinet: cabinet?.name || 'N/A',
          gameMix: gameMix?.name || 'N/A',
          gamingPlaces: slot.gaming_places || 'N/A',
          cvtDate: metrology?.expiry_date ? formatDateDDMMYYYY(metrology.expiry_date) : 'N/A',
          jackpot: jackpot ? `${jackpot.jackpot_name} (${jackpot.jackpot_type})` : 'N/A'
        };
      };

      return (
        <div style={{ padding: '20px' }}>
          <h3 style={{ color: '#3182ce', marginBottom: '20px', borderBottom: '2px solid #3182ce', paddingBottom: '10px' }}>
            📅 Commission Date Details: {report.event_name || 'Unnamed Event'}
          </h3>
          
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px' }}>
            <div>
              <strong style={{ color: 'var(--text-primary)' }}>📅 Commission Date:</strong>
              <p style={{ color: 'var(--text-secondary)' }}>{formatDateDDMMYYYY(report.commission_date)}</p>
            </div>
            <div>
              <strong style={{ color: 'var(--text-primary)' }}>📊 Number of Slots:</strong>
              <p style={{ color: 'var(--text-secondary)' }}>{serials.length}</p>
            </div>
            <div>
              <strong style={{ color: 'var(--text-primary)' }}>📝 Created:</strong>
              <p style={{ color: 'var(--text-secondary)' }}>{formatDateDDMMYYYY(report.created_at)}</p>
            </div>
            <div>
              <strong style={{ color: 'var(--text-primary)' }}>👤 Created by:</strong>
              <p style={{ color: 'var(--text-secondary)' }}>
                {(() => {
                  const user = Array.isArray(users) ? users.find(u => u.id === report.created_by || u.username === report.created_by) : null;
                  return user ? `${user.first_name} ${user.last_name}` : report.created_by || 'Unknown';
                })()}
              </p>
            </div>
          </div>

          {associatedSlots.length > 0 && (
            <div>
              <h4 style={{ color: '#3182ce', marginBottom: '15px' }}>🎰 Slot Details for Each Serial Number</h4>
              <div style={{ maxHeight: '400px', overflowY: 'auto', border: '1px solid #e5e7eb', borderRadius: '8px', padding: '10px' }}>
                <table style={{ 
                  width: '100%', 
                  borderCollapse: 'collapse',
                  fontSize: '13px'
                }}>
                  <thead>
                    <tr style={{ 
                      backgroundColor: '#f1f5f9', 
                      borderBottom: '2px solid #e2e8f0'
                    }}>
                      <th style={{ 
                        padding: '10px 6px', 
                        textAlign: 'left', 
                        fontWeight: 'bold',
                        color: 'var(--text-primary)',
                        borderBottom: '1px solid #e2e8f0',
                        fontSize: '12px'
                      }}>
                        Serial Number
                      </th>
                      <th style={{ 
                        padding: '10px 6px', 
                        textAlign: 'left', 
                        fontWeight: 'bold',
                        color: 'var(--text-primary)',
                        borderBottom: '1px solid #e2e8f0',
                        fontSize: '12px'
                      }}>
                        Location
                      </th>
                      <th style={{ 
                        padding: '10px 6px', 
                        textAlign: 'left', 
                        fontWeight: 'bold',
                        color: 'var(--text-primary)',
                        borderBottom: '1px solid #e2e8f0',
                        fontSize: '12px'
                      }}>
                        Provider
                      </th>
                      <th style={{ 
                        padding: '10px 6px', 
                        textAlign: 'left', 
                        fontWeight: 'bold',
                        color: 'var(--text-primary)',
                        borderBottom: '1px solid #e2e8f0',
                        fontSize: '12px'
                      }}>
                        Cabinet
                      </th>
                      <th style={{ 
                        padding: '10px 6px', 
                        textAlign: 'left', 
                        fontWeight: 'bold',
                        color: 'var(--text-primary)',
                        borderBottom: '1px solid #e2e8f0',
                        fontSize: '12px'
                      }}>
                        Game Mix
                      </th>
                      <th style={{ 
                        padding: '10px 6px', 
                        textAlign: 'left', 
                        fontWeight: 'bold',
                        color: 'var(--text-primary)',
                        borderBottom: '1px solid #e2e8f0',
                        fontSize: '12px'
                      }}>
                        Gaming Places
                      </th>
                      <th style={{ 
                        padding: '10px 6px', 
                        textAlign: 'left', 
                        fontWeight: 'bold',
                        color: 'var(--text-primary)',
                        borderBottom: '1px solid #e2e8f0',
                        fontSize: '12px'
                      }}>
                        CVT Date of End
                      </th>
                      <th style={{ 
                        padding: '10px 6px', 
                        textAlign: 'left', 
                        fontWeight: 'bold',
                        color: 'var(--text-primary)',
                        borderBottom: '1px solid #e2e8f0',
                        fontSize: '12px'
                      }}>
                        Jackpots
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {associatedSlots.map((slot, index) => {
                      const details = getSlotDetails(slot);
                      return (
                        <tr key={slot.id} style={{ 
                          backgroundColor: index % 2 === 0 ? '#ffffff' : '#f8fafc',
                          borderBottom: '1px solid #e2e8f0'
                        }}>
                          <td style={{ 
                            padding: '10px 6px', 
                            fontWeight: 'bold',
                            color: 'var(--text-primary)',
                            fontSize: '12px'
                          }}>
                            {slot.serial_number}
                          </td>
                          <td style={{ 
                            padding: '10px 6px', 
                            color: 'var(--text-secondary)',
                            fontSize: '12px'
                          }}>
                            {details.location}
                          </td>
                          <td style={{ 
                            padding: '10px 6px', 
                            color: 'var(--text-secondary)',
                            fontSize: '12px'
                          }}>
                            {details.provider}
                          </td>
                          <td style={{ 
                            padding: '10px 6px', 
                            color: 'var(--text-secondary)',
                            fontSize: '12px'
                          }}>
                            {details.cabinet}
                          </td>
                          <td style={{ 
                            padding: '10px 6px', 
                            color: 'var(--text-secondary)',
                            fontSize: '12px'
                          }}>
                            {details.gameMix}
                          </td>
                          <td style={{ 
                            padding: '10px 6px', 
                            color: 'var(--text-secondary)',
                            fontSize: '12px'
                          }}>
                            {details.gamingPlaces}
                          </td>
                          <td style={{ 
                            padding: '10px 6px', 
                            color: 'var(--text-secondary)',
                            fontSize: '12px'
                          }}>
                            {details.cvtDate}
                          </td>
                          <td style={{ 
                            padding: '10px 6px', 
                            color: 'var(--text-secondary)',
                            fontSize: '12px'
                          }}>
                            {details.jackpot}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      );
    };

    const renderOnjnReportDetails = () => {
      const serials = report.serial_numbers ? report.serial_numbers.split(/\s+/).filter(s => s.trim()) : [];

      return (
        <div style={{ padding: '20px' }}>
          <h3 style={{ color: '#3182ce', marginBottom: '20px', borderBottom: '2px solid #3182ce', paddingBottom: '10px' }}>
            📋 ONJN Report Details
          </h3>
          
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px' }}>
            <div>
              <strong style={{ color: 'var(--text-primary)' }}>📋 Event Name:</strong>
              <p style={{ color: 'var(--text-secondary)' }}>{report.report_number}</p>
            </div>
            <div>
              <strong style={{ color: 'var(--text-primary)' }}>📄 Report Type:</strong>
              <p style={{ color: 'var(--text-secondary)' }}>{report.report_type}</p>
            </div>
            <div>
              <strong style={{ color: 'var(--text-primary)' }}>👤 Persona de care a fost creat:</strong>
              <p style={{ color: 'var(--text-secondary)' }}>
                {(() => {
                  const user = Array.isArray(users) ? users.find(u => u.id === report.created_by || u.username === report.created_by) : null;
                  return user ? `${user.first_name} ${user.last_name}` : report.created_by || 'N/A';
                })()}
              </p>
            </div>
            <div>
              <strong style={{ color: 'var(--text-primary)' }}>💼 Transaction Type:</strong>
              <p style={{ color: 'var(--text-secondary)' }}>{report.transaction_type || 'N/A'}</p>
            </div>
            <div>
              <strong style={{ color: 'var(--text-primary)' }}>📅 Report Date:</strong>
              <p style={{ color: 'var(--text-secondary)' }}>{formatDateDDMMYYYY(report.report_date)}</p>
            </div>
            <div>
              <strong style={{ color: 'var(--text-primary)' }}>⏳ Status:</strong>
              <p style={{ color: 'var(--text-secondary)' }}>{report.submission_date ? 
                `✅ Submitted: ${formatDateDDMMYYYY(report.submission_date)}` : 
                '⏳ Not submitted'
              }</p>
            </div>
            {report.serial_numbers && (
              <>
                <div>
                  <strong style={{ color: 'var(--text-primary)' }}>🎰 Serial Numbers:</strong>
                  <p style={{ wordBreak: 'break-all', color: 'var(--text-secondary)' }}>{report.serial_numbers}</p>
                </div>
                <div>
                  <strong style={{ color: 'var(--text-primary)' }}>📊 Number of Slots:</strong>
                  <p style={{ color: 'var(--text-secondary)' }}>{serials.length}</p>
                </div>
              </>
            )}
          </div>
        </div>
      );
    };

    return (
      <div className="modal-overlay" onClick={onClose}>
        <div className="modal-content" onClick={e => e.stopPropagation()}>
          <div className="modal-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <h2 style={{ color: 'var(--text-primary)' }}>{report.type === 'comision_date' ? 'Commission Date Details' : 'ONJN Report Details'}</h2>
              <div style={{
                backgroundColor: '#3182ce',
                color: 'white',
                borderRadius: '50%',
                width: '28px',
                height: '28px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '14px',
                fontWeight: 'bold',
                minWidth: '28px'
              }}>
                {report.type === 'comision_date' ? '📅' : '📋'}
              </div>
            </div>
            <button 
              className="modal-close" 
              onClick={onClose}
              style={{ 
                background: 'none', 
                border: 'none', 
                fontSize: '24px', 
                cursor: 'pointer',
                color: '#666'
              }}
            >
              ×
            </button>
          </div>
          
          <div className="modal-body">
            {report.type === 'comision_date' ? renderCommissionDateDetails() : renderOnjnReportDetails()}
          </div>
          
          <div className="modal-footer">
            <button 
              onClick={onClose}
              style={{
                backgroundColor: '#3182ce',
                color: 'white',
                border: 'none',
                padding: '10px 20px',
                borderRadius: '6px',
                cursor: 'pointer',
                fontWeight: 'bold'
              }}
            >
              Close
            </button>
          </div>
        </div>
      </div>
    );
  };

  // Commission Date Details Page Component
  const CommissionDateDetailsPage = ({ commissionDate, onClose }) => {
    if (!commissionDate) return null;

    const serials = commissionDate.serial_numbers ? commissionDate.serial_numbers.split(/\s+/).filter(s => s.trim()) : [];
    const associatedSlots = slotMachines.filter(slot => 
      serials.includes(slot.serial_number)
    );

    // Funcție pentru a găsi informațiile asociate
    const getSlotDetails = (slot) => {
      const location = locations.find(loc => loc.id === slot.location_id);
      const provider = providers.find(prov => prov.id === slot.provider_id);
      const cabinet = cabinets.find(cab => cab.id === slot.cabinet_id);
      const gameMix = gameMixes.find(gm => gm.id === slot.game_mix_id);
      const metrologyItem = metrology.find(met => met.serial_number === slot.serial_number);
      const jackpot = jackpots.find(jp => jp.serial_number === slot.serial_number);
      const user = Array.isArray(users) ? users.find(u => u.username === commissionDate.created_by) : null;

      return {
        location: location?.name || 'N/A',
        provider: provider?.name || 'N/A',
        cabinet: cabinet?.name || 'N/A',
        gameMix: gameMix?.name || 'N/A',
        gamingPlaces: slot.gaming_places || 'N/A',
        cvtDate: metrologyItem?.expiry_date ? formatDateDDMMYYYY(metrologyItem.expiry_date) : 'N/A',
        jackpot: jackpot ? `${jackpot.jackpot_name} (${jackpot.jackpot_type})` : 'N/A',
        createdBy: user ? `${user.first_name} ${user.last_name}` : commissionDate.created_by || 'Unknown'
      };
    };

    return (
      <div className="app-layout" data-theme={theme}>


        {/* Content */}
        <div className="layout-container">
          <div className="main-content">
            <div className="content-body">
              <div style={{ padding: '20px' }}>
                {/* Header Info */}
                <div style={{ 
                  background: 'var(--bg-secondary)', 
                  borderRadius: '12px', 
                  padding: '24px', 
                  marginBottom: '24px',
                  border: '1px solid var(--border-color)'
                }}>
                  <div style={{ 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    alignItems: 'center', 
                    marginBottom: '16px' 
                  }}>
                    <h1 style={{ 
                      color: 'var(--text-primary)', 
                      margin: '0',
                      fontSize: '24px',
                      fontWeight: '700'
                    }}>
                      📅 {commissionDate.event_name || 'Unnamed Event'}
                    </h1>
                    <button 
                      onClick={onClose}
                      style={{
                        background: 'var(--gradient-primary)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '8px',
                        padding: '8px 16px',
                        cursor: 'pointer',
                        fontSize: '14px',
                        fontWeight: '600',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px'
                      }}
                    >
                      ← Back
                    </button>
                  </div>
                  
                  <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
                    gap: '16px' 
                  }}>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>📅 Commission Date:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {formatDateDDMMYYYY(commissionDate.commission_date)}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>📊 Number of Slots:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {serials.length}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>🎮 Total Gaming Places:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {associatedSlots.reduce((total, slot) => total + (parseInt(slot.gaming_places) || 0), 0)}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>📝 Created:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {formatDateDDMMYYYY(commissionDate.created_at)}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>👤 Created by:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {getSlotDetails({}).createdBy}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Table */}
                {associatedSlots.length > 0 && (
                  <div style={{ 
                    background: 'var(--bg-secondary)', 
                    borderRadius: '12px', 
                    padding: '24px',
                    border: '1px solid var(--border-color)'
                  }}>
                    <div style={{ 
                      display: 'flex', 
                      justifyContent: 'space-between', 
                      alignItems: 'center',
                      marginBottom: '20px'
                    }}>
                      <h2 style={{ 
                        color: 'var(--text-primary)', 
                        fontSize: '20px',
                        fontWeight: '600',
                        margin: '0'
                      }}>
                        🎰 Slot Details for Each Serial Number
                      </h2>
                      <button
                        onClick={() => {
                          console.log('Export button clicked');
                          console.log('Associated slots:', associatedSlots);
                          
                          if (!associatedSlots || associatedSlots.length === 0) {
                            console.log('No slots to export');
                            return;
                          }
                          
                          const data = associatedSlots.map((slot, index) => {
                            const details = getSlotDetails(slot);
                            console.log('Slot details:', details);
                            return {
                              'ID': index + 1,
                              'Serial Number': slot.serial_number || 'N/A',
                              'Location': details.location || 'N/A',
                              'Provider': details.provider || 'N/A',
                              'Cabinet': details.cabinet || 'N/A',
                              'Game Mix': details.gameMix || 'N/A',
                              'Gaming Places': details.gamingPlaces || 'N/A',
                              'CVT Date of End': details.cvtDate || 'N/A',
                              'Jackpots': details.jackpot || 'N/A'
                            };
                          });
                          
                          console.log('Export data:', data);
                          
                          // Create CSV content
                          const headers = Object.keys(data[0] || {});
                          const csvContent = [
                            headers.join(','),
                            ...data.map(row => headers.map(header => `"${row[header]}"`).join(','))
                          ].join('\n');
                          
                          console.log('CSV content:', csvContent);
                          
                          // Create and download file
                          const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
                          const link = document.createElement('a');
                          const url = URL.createObjectURL(blob);
                          link.setAttribute('href', url);
                          link.setAttribute('download', `${commissionDate.event_name || 'Commission_Date'}_${formatDateDDMMYYYY(commissionDate.commission_date)}.csv`);
                          link.style.visibility = 'hidden';
                          document.body.appendChild(link);
                          link.click();
                          document.body.removeChild(link);
                          
                          console.log('Export completed');
                        }}
                        style={{
                          background: 'var(--gradient-primary)',
                          color: 'white',
                          border: 'none',
                          borderRadius: '8px',
                          padding: '8px 16px',
                          cursor: 'pointer',
                          fontSize: '14px',
                          fontWeight: '600',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '8px'
                        }}
                      >
                        📊 Export to XLS
                      </button>
                    </div>
                    
                    <div style={{ 
                      maxHeight: '600px', 
                      overflowY: 'auto', 
                      border: '1px solid var(--border-color)', 
                      borderRadius: '8px'
                    }}>
                      <table style={{ 
                        width: '100%', 
                        borderCollapse: 'collapse',
                        fontSize: '14px'
                      }}>
                        <thead>
                          <tr style={{ 
                            backgroundColor: 'var(--bg-tertiary)', 
                            borderBottom: '2px solid var(--border-color)'
                          }}>
                            <th style={{ 
                              padding: '12px 8px', 
                              textAlign: 'left', 
                              fontWeight: 'bold',
                              color: 'var(--text-primary)',
                              borderBottom: '1px solid var(--border-color)',
                              fontSize: '13px'
                            }}>
                              ID
                            </th>
                            <th style={{ 
                              padding: '12px 8px', 
                              textAlign: 'left', 
                              fontWeight: 'bold',
                              color: 'var(--text-primary)',
                              borderBottom: '1px solid var(--border-color)',
                              fontSize: '13px'
                            }}>
                              Serial Number
                            </th>
                            <th style={{ 
                              padding: '12px 8px', 
                              textAlign: 'left', 
                              fontWeight: 'bold',
                              color: 'var(--text-primary)',
                              borderBottom: '1px solid var(--border-color)',
                              fontSize: '13px'
                            }}>
                              Location
                            </th>
                            <th style={{ 
                              padding: '12px 8px', 
                              textAlign: 'left', 
                              fontWeight: 'bold',
                              color: 'var(--text-primary)',
                              borderBottom: '1px solid var(--border-color)',
                              fontSize: '13px'
                            }}>
                              Provider
                            </th>
                            <th style={{ 
                              padding: '12px 8px', 
                              textAlign: 'left', 
                              fontWeight: 'bold',
                              color: 'var(--text-primary)',
                              borderBottom: '1px solid var(--border-color)',
                              fontSize: '13px'
                            }}>
                              Cabinet
                            </th>
                            <th style={{ 
                              padding: '12px 8px', 
                              textAlign: 'left', 
                              fontWeight: 'bold',
                              color: 'var(--text-primary)',
                              borderBottom: '1px solid var(--border-color)',
                              fontSize: '13px'
                            }}>
                              Game Mix
                            </th>
                            <th style={{ 
                              padding: '12px 8px', 
                              textAlign: 'left', 
                              fontWeight: 'bold',
                              color: 'var(--text-primary)',
                              borderBottom: '1px solid var(--border-color)',
                              fontSize: '13px'
                            }}>
                              Gaming Places
                            </th>
                            <th style={{ 
                              padding: '12px 8px', 
                              textAlign: 'left', 
                              fontWeight: 'bold',
                              color: 'var(--text-primary)',
                              borderBottom: '1px solid var(--border-color)',
                              fontSize: '13px'
                            }}>
                              CVT Date of End
                            </th>
                            <th style={{ 
                              padding: '12px 8px', 
                              textAlign: 'left', 
                              fontWeight: 'bold',
                              color: 'var(--text-primary)',
                              borderBottom: '1px solid var(--border-color)',
                              fontSize: '13px'
                            }}>
                              Jackpots
                            </th>
                          </tr>
                        </thead>
                        <tbody>
                          {associatedSlots.map((slot, index) => {
                            const details = getSlotDetails(slot);
                            return (
                              <tr key={slot.id} style={{ 
                                backgroundColor: index % 2 === 0 ? 'var(--bg-secondary)' : 'var(--bg-tertiary)',
                                borderBottom: '1px solid var(--border-color)'
                              }}>
                                <td style={{ 
                                  padding: '12px 8px', 
                                  fontWeight: 'bold',
                                  color: 'var(--text-primary)',
                                  fontSize: '13px'
                                }}>
                                  {index + 1}
                                </td>
                                <td style={{ 
                                  padding: '12px 8px', 
                                  fontWeight: 'bold',
                                  color: 'var(--text-primary)',
                                  fontSize: '13px'
                                }}>
                                  {slot.serial_number}
                                </td>
                                <td style={{ 
                                  padding: '12px 8px', 
                                  color: 'var(--text-secondary)',
                                  fontSize: '13px'
                                }}>
                                  {details.location}
                                </td>
                                <td style={{ 
                                  padding: '12px 8px', 
                                  color: 'var(--text-secondary)',
                                  fontSize: '13px'
                                }}>
                                  {details.provider}
                                </td>
                                <td style={{ 
                                  padding: '12px 8px', 
                                  color: 'var(--text-secondary)',
                                  fontSize: '13px'
                                }}>
                                  {details.cabinet}
                                </td>
                                <td style={{ 
                                  padding: '12px 8px', 
                                  color: 'var(--text-secondary)',
                                  fontSize: '13px'
                                }}>
                                  {details.gameMix}
                                </td>
                                <td style={{ 
                                  padding: '12px 8px', 
                                  color: 'var(--text-secondary)',
                                  fontSize: '13px'
                                }}>
                                  {details.gamingPlaces}
                                </td>
                                <td style={{ 
                                  padding: '12px 8px', 
                                  color: 'var(--text-secondary)',
                                  fontSize: '13px'
                                }}>
                                  {details.cvtDate}
                                </td>
                                <td style={{ 
                                  padding: '12px 8px', 
                                  color: 'var(--text-secondary)',
                                  fontSize: '13px'
                                }}>
                                  {details.jackpot}
                                </td>

                              </tr>
                            );
                          })}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
    };

  // Jackpot Details Page Component
  const JackpotDetailsPage = ({ jackpot, onClose }) => {
    if (!jackpot) return null;

    // Funcție pentru a găsi toate sloturile asociate cu acest jackpot
    const getAssociatedSlots = () => {
      return slotMachines.filter(slot => slot.serial_number === jackpot.serial_number);
    };

    // Funcție pentru a obține detaliile unui slot
    const getSlotDetails = (slot) => {
      const location = locations.find(loc => loc.id === slot?.location_id);
      const provider = providers.find(prov => prov.id === slot?.provider_id);
      const cabinet = cabinets.find(cab => cab.id === slot?.cabinet_id);
      const gameMix = gameMixes.find(gm => gm.id === slot?.game_mix_id);

      return {
        id: slot.id || slot._id,
        serialNumber: slot.serial_number || 'N/A',
        location: location?.name || 'N/A',
        provider: provider?.name || 'N/A',
        cabinet: cabinet?.name || 'N/A',
        gameMix: gameMix?.name || 'N/A',
        gamingPlaces: slot?.gaming_places || 'N/A',
        cvtEndDate: slot?.cvt_end_date ? formatDateDDMMYYYY(slot.cvt_end_date) : 'N/A'
      };
    };

    const associatedSlots = getAssociatedSlots();
    const slotDetails = associatedSlots.map(getSlotDetails);

    // Funcție pentru export XLS
    const handleExportToXLS = () => {
      const data = slotDetails.map((slot, index) => ({
        'ID': index + 1,
        'Serial Number': slot.serialNumber,
        'Location': slot.location,
        'Provider': slot.provider,
        'Cabinet': slot.cabinet,
        'Game Mix': slot.gameMix,
        'Gaming Places': slot.gamingPlaces,
        'CVT Date of End': slot.cvtEndDate,
        'Jackpots': jackpot.jackpot_name
      }));

      const ws = XLSX.utils.json_to_sheet(data);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'Jackpot Slots');
      
      const fileName = `jackpot_${jackpot.jackpot_name}_slots_${formatDateDDMMYYYY(new Date())}.xlsx`;
      XLSX.writeFile(wb, fileName);
    };

    return (
      <div className="app-layout" data-theme={theme}>


        {/* Content */}
        <div className="layout-container">
          <div className="main-content">
            <div className="content-body">
              <div style={{ padding: '20px' }}>
                {/* Header Info */}
                <div style={{ 
                  background: 'var(--bg-secondary)', 
                  borderRadius: '12px', 
                  padding: '24px', 
                  marginBottom: '24px',
                  border: '1px solid var(--border-color)'
                }}>
                  <div style={{ 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    alignItems: 'center', 
                    marginBottom: '16px' 
                  }}>
                    <h1 style={{ 
                      color: 'var(--text-primary)', 
                      margin: '0',
                      fontSize: '24px',
                      fontWeight: '700'
                    }}>
                      🎰 {jackpot.jackpot_name || 'Unnamed Jackpot'}
                    </h1>
                    <button 
                      onClick={onClose}
                      style={{
                        background: 'var(--gradient-primary)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '8px',
                        padding: '8px 16px',
                        cursor: 'pointer',
                        fontSize: '14px',
                        fontWeight: '600',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px'
                      }}
                    >
                      ← Back
                    </button>
                  </div>
                  
                  <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
                    gap: '16px' 
                  }}>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>🎰 Jackpot Type:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {jackpot.jackpot_type}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>📊 Increment Rate:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {jackpot.increment_rate}%
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>🎯 Serial Number:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {jackpot.serial_number}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>📝 Created:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {formatDateDDMMYYYY(jackpot.created_at)}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>👤 Created by:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {(() => {
                          const user = Array.isArray(users) ? users.find(u => u.username === jackpot.created_by) : null;
                          return user ? `${user.first_name} ${user.last_name}` : jackpot.created_by || 'Unknown';
                        })()}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>⏰ Last Reset:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {formatDateDDMMYYYY(jackpot.last_reset_date)}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Jackpot Levels */}
                {(jackpot.level_1 || jackpot.level_2 || jackpot.level_3 || jackpot.level_4 || jackpot.level_5) && (
                  <div style={{ 
                    background: 'var(--bg-secondary)', 
                    borderRadius: '12px', 
                    padding: '24px',
                    marginBottom: '24px',
                    border: '1px solid var(--border-color)'
                  }}>
                    <h2 style={{ 
                      color: 'var(--text-primary)', 
                      fontSize: '20px',
                      fontWeight: '600',
                      margin: '0 0 20px 0'
                    }}>
                      🏆 Jackpot Levels
                    </h2>
                    <div style={{ 
                      display: 'grid', 
                      gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', 
                      gap: '16px' 
                    }}>
                      {jackpot.level_1 && (
                        <div style={{ 
                          padding: '12px', 
                          background: 'var(--bg-tertiary)', 
                          borderRadius: '8px',
                          border: '1px solid var(--border-color)'
                        }}>
                          <strong style={{ color: 'var(--text-primary)', fontSize: '12px' }}>Level 1:</strong>
                          <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0', fontSize: '14px' }}>
                            {jackpot.level_1}
                          </p>
                        </div>
                      )}
                      {jackpot.level_2 && (
                        <div style={{ 
                          padding: '12px', 
                          background: 'var(--bg-tertiary)', 
                          borderRadius: '8px',
                          border: '1px solid var(--border-color)'
                        }}>
                          <strong style={{ color: 'var(--text-primary)', fontSize: '12px' }}>Level 2:</strong>
                          <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0', fontSize: '14px' }}>
                            {jackpot.level_2}
                          </p>
                        </div>
                      )}
                      {jackpot.level_3 && (
                        <div style={{ 
                          padding: '12px', 
                          background: 'var(--bg-tertiary)', 
                          borderRadius: '8px',
                          border: '1px solid var(--border-color)'
                        }}>
                          <strong style={{ color: 'var(--text-primary)', fontSize: '12px' }}>Level 3:</strong>
                          <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0', fontSize: '14px' }}>
                            {jackpot.level_3}
                          </p>
                        </div>
                      )}
                      {jackpot.level_4 && (
                        <div style={{ 
                          padding: '12px', 
                          background: 'var(--bg-tertiary)', 
                          borderRadius: '8px',
                          border: '1px solid var(--border-color)'
                        }}>
                          <strong style={{ color: 'var(--text-primary)', fontSize: '12px' }}>Level 4:</strong>
                          <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0', fontSize: '14px' }}>
                            {jackpot.level_4}
                          </p>
                        </div>
                      )}
                      {jackpot.level_5 && (
                        <div style={{ 
                          padding: '12px', 
                          background: 'var(--bg-tertiary)', 
                          borderRadius: '8px',
                          border: '1px solid var(--border-color)'
                        }}>
                          <strong style={{ color: 'var(--text-primary)', fontSize: '12px' }}>Level 5:</strong>
                          <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0', fontSize: '14px' }}>
                            {jackpot.level_5}
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Slot Details Table */}
                <div style={{ 
                  background: 'var(--bg-secondary)', 
                  borderRadius: '12px', 
                  padding: '24px',
                  border: '1px solid var(--border-color)'
                }}>
                  <div style={{ 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    alignItems: 'center',
                    marginBottom: '20px'
                  }}>
                    <h2 style={{ 
                      color: 'var(--text-primary)', 
                      fontSize: '20px',
                      fontWeight: '600',
                      margin: '0'
                    }}>
                      🎰 Slot Details for Each Serial Number
                    </h2>
                    <button
                      onClick={handleExportToXLS}
                      style={{
                        background: 'var(--gradient-primary)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '8px',
                        padding: '8px 16px',
                        cursor: 'pointer',
                        fontSize: '14px',
                        fontWeight: '600',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px'
                      }}
                    >
                      📊 Export to XLS
                    </button>
                  </div>
                  
                  {slotDetails.length > 0 ? (
                    <div style={{ overflowX: 'auto' }}>
                      <table style={{
                        width: '100%',
                        borderCollapse: 'collapse',
                        color: 'var(--text-primary)'
                      }}>
                        <thead>
                          <tr style={{
                            background: 'var(--bg-tertiary)',
                            borderBottom: '2px solid var(--border-color)'
                          }}>
                            <th style={{
                              padding: '12px',
                              textAlign: 'left',
                              fontWeight: '600',
                              fontSize: '14px',
                              borderBottom: '1px solid var(--border-color)'
                            }}>ID</th>
                            <th style={{
                              padding: '12px',
                              textAlign: 'left',
                              fontWeight: '600',
                              fontSize: '14px',
                              borderBottom: '1px solid var(--border-color)'
                            }}>Serial Number</th>
                            <th style={{
                              padding: '12px',
                              textAlign: 'left',
                              fontWeight: '600',
                              fontSize: '14px',
                              borderBottom: '1px solid var(--border-color)'
                            }}>Location</th>
                            <th style={{
                              padding: '12px',
                              textAlign: 'left',
                              fontWeight: '600',
                              fontSize: '14px',
                              borderBottom: '1px solid var(--border-color)'
                            }}>Provider</th>
                            <th style={{
                              padding: '12px',
                              textAlign: 'left',
                              fontWeight: '600',
                              fontSize: '14px',
                              borderBottom: '1px solid var(--border-color)'
                            }}>Cabinet</th>
                            <th style={{
                              padding: '12px',
                              textAlign: 'left',
                              fontWeight: '600',
                              fontSize: '14px',
                              borderBottom: '1px solid var(--border-color)'
                            }}>Game Mix</th>
                            <th style={{
                              padding: '12px',
                              textAlign: 'left',
                              fontWeight: '600',
                              fontSize: '14px',
                              borderBottom: '1px solid var(--border-color)'
                            }}>Gaming Places</th>
                            <th style={{
                              padding: '12px',
                              textAlign: 'left',
                              fontWeight: '600',
                              fontSize: '14px',
                              borderBottom: '1px solid var(--border-color)'
                            }}>CVT Date of End</th>
                            <th style={{
                              padding: '12px',
                              textAlign: 'left',
                              fontWeight: '600',
                              fontSize: '14px',
                              borderBottom: '1px solid var(--border-color)'
                            }}>Jackpots</th>
                          </tr>
                        </thead>
                        <tbody>
                          {slotDetails.map((slot, index) => (
                            <tr key={slot.id} style={{
                              borderBottom: '1px solid var(--border-color)',
                              background: index % 2 === 0 ? 'var(--bg-secondary)' : 'var(--bg-tertiary)'
                            }}>
                              <td style={{
                                padding: '12px',
                                fontSize: '14px',
                                color: 'var(--text-secondary)'
                              }}>{index + 1}</td>
                              <td style={{
                                padding: '12px',
                                fontSize: '14px',
                                color: 'var(--text-secondary)'
                              }}>{slot.serialNumber}</td>
                              <td style={{
                                padding: '12px',
                                fontSize: '14px',
                                color: 'var(--text-secondary)'
                              }}>{slot.location}</td>
                              <td style={{
                                padding: '12px',
                                fontSize: '14px',
                                color: 'var(--text-secondary)'
                              }}>{slot.provider}</td>
                              <td style={{
                                padding: '12px',
                                fontSize: '14px',
                                color: 'var(--text-secondary)'
                              }}>{slot.cabinet}</td>
                              <td style={{
                                padding: '12px',
                                fontSize: '14px',
                                color: 'var(--text-secondary)'
                              }}>{slot.gameMix}</td>
                              <td style={{
                                padding: '12px',
                                fontSize: '14px',
                                color: 'var(--text-secondary)'
                              }}>{slot.gamingPlaces}</td>
                              <td style={{
                                padding: '12px',
                                fontSize: '14px',
                                color: 'var(--text-secondary)'
                              }}>{slot.cvtEndDate}</td>
                              <td style={{
                                padding: '12px',
                                fontSize: '14px',
                                color: 'var(--text-secondary)'
                              }}>{jackpot.jackpot_name}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  ) : (
                    <div style={{
                      textAlign: 'center',
                      padding: '40px',
                      color: 'var(--text-secondary)',
                      fontSize: '16px'
                    }}>
                      No associated slots found for this jackpot.
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Metrology Details Page Component
  const MetrologyDetailsPage = ({ metrology, onClose }) => {
    if (!metrology) return null;

    // Funcție pentru a găsi toate sloturile asociate cu acest CVT
    const getAssociatedSlots = () => {
      if (!metrology.serial_number) return [];
      
      // Try both newline and space separation
      const serialNumbersNewline = metrology.serial_number.split('\n').filter(s => s.trim());
      const serialNumbersSpace = metrology.serial_number.split(' ').filter(s => s.trim());
      
      // Use the one that has more items (more likely to be correct)
      const serialNumbers = serialNumbersNewline.length > serialNumbersSpace.length ? 
        serialNumbersNewline : serialNumbersSpace;
      
      return slotMachines.filter(slot => serialNumbers.includes(slot.serial_number));
    };

    // Funcție pentru a obține detaliile unui slot
    const getSlotDetails = (slot) => {
      const location = locations.find(loc => loc.id === slot?.location_id);
      const provider = providers.find(prov => prov.id === slot?.provider_id);
      const cabinet = cabinets.find(cab => cab.id === slot?.cabinet_id);
      const gameMix = gameMixes.find(gm => gm.id === slot?.game_mix_id);

      return {
        id: slot.id || slot._id,
        serialNumber: slot.serial_number || 'N/A',
        location: location?.name || 'N/A',
        provider: provider?.name || 'N/A',
        cabinet: cabinet?.name || 'N/A',
        gameMix: gameMix?.name || 'N/A',
        gamingPlaces: slot?.gaming_places || 'N/A',
        cvtEndDate: metrology?.cvt_expiry_date ? formatDateDDMMYYYY(metrology.cvt_expiry_date) : 'N/A'
      };
    };

    const associatedSlots = getAssociatedSlots();
    const slotDetails = associatedSlots.map(getSlotDetails);

    // Funcție pentru export XLS
    const handleExportToXLS = () => {
      const data = slotDetails.map((slot, index) => ({
        'ID': index + 1,
        'Serial Number': slot.serialNumber,
        'Location': slot.location,
        'Provider': slot.provider,
        'Cabinet': slot.cabinet,
        'Game Mix': slot.gameMix,
        'Gaming Places': slot.gamingPlaces,
        'CVT Date of End': slot.cvtEndDate,
        'CVT Certificate': metrology.certificate_number
      }));

      const ws = XLSX.utils.json_to_sheet(data);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'CVT Slots');
      
      const fileName = `cvt_${metrology.certificate_number}_slots_${formatDateDDMMYYYY(new Date())}.xlsx`;
      XLSX.writeFile(wb, fileName);
    };

    return (
      <div className="app-layout" data-theme={theme}>


        {/* Content */}
        <div className="layout-container">
          <div className="main-content">
            <div className="content-body">
              <div style={{ padding: '20px' }}>
                {/* Header Info */}
                <div style={{ 
                  background: 'var(--bg-secondary)', 
                  borderRadius: '12px', 
                  padding: '24px', 
                  marginBottom: '24px',
                  border: '1px solid var(--border-color)'
                }}>
                  <div style={{ 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    alignItems: 'center', 
                    marginBottom: '16px' 
                  }}>
                    <h1 style={{ 
                      color: 'var(--text-primary)', 
                      margin: '0',
                      fontSize: '24px',
                      fontWeight: '700'
                    }}>
                      📋 {metrology.certificate_number || 'Unnamed CVT Certificate'}
                    </h1>
                    <button 
                      onClick={onClose}
                      style={{
                        background: 'var(--gradient-primary)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '8px',
                        padding: '8px 16px',
                        cursor: 'pointer',
                        fontSize: '14px',
                        fontWeight: '600',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px'
                      }}
                    >
                      ← Back
                    </button>
                  </div>
                  
                  <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
                    gap: '16px' 
                  }}>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>📋 Certificate Number:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {metrology.certificate_number}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>📅 Issue Date:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {formatDateDDMMYYYY(metrology.issue_date)}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>🏢 Issuing Authority:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {metrology.issuing_authority}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>📝 Status:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {metrology.status}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>👤 Created by:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {(() => {
                          const user = Array.isArray(users) ? users.find(u => u.username === metrology.created_by) : null;
                          return user ? `${user.first_name} ${user.last_name}` : metrology.created_by || 'Unknown';
                        })()}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>📅 Created:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {formatDateDDMMYYYY(metrology.created_at)}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Slot Details Table */}
                <div style={{ 
                  background: 'var(--bg-secondary)', 
                  borderRadius: '12px', 
                  padding: '24px',
                  border: '1px solid var(--border-color)'
                }}>
                  <div style={{ 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    alignItems: 'center',
                    marginBottom: '20px'
                  }}>
                    <h2 style={{ 
                      color: 'var(--text-primary)', 
                      fontSize: '20px',
                      fontWeight: '600',
                      margin: '0'
                    }}>
                      🎰 Slot Details for Each Serial Number
                    </h2>
                    <button
                      onClick={handleExportToXLS}
                      style={{
                        background: 'var(--gradient-primary)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '8px',
                        padding: '8px 16px',
                        cursor: 'pointer',
                        fontSize: '14px',
                        fontWeight: '600',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px'
                      }}
                    >
                      📊 Export to XLS
                    </button>
                  </div>
                  
                  {slotDetails.length > 0 ? (
                    <div style={{ overflowX: 'auto' }}>
                      <table style={{
                        width: '100%',
                        borderCollapse: 'collapse',
                        color: 'var(--text-primary)'
                      }}>
                        <thead>
                          <tr style={{
                            background: 'var(--bg-tertiary)',
                            borderBottom: '2px solid var(--border-color)'
                          }}>
                            <th style={{
                              padding: '12px',
                              textAlign: 'left',
                              fontWeight: '600',
                              fontSize: '14px',
                              borderBottom: '1px solid var(--border-color)'
                            }}>ID</th>
                            <th style={{
                              padding: '12px',
                              textAlign: 'left',
                              fontWeight: '600',
                              fontSize: '14px',
                              borderBottom: '1px solid var(--border-color)'
                            }}>Serial Number</th>
                            <th style={{
                              padding: '12px',
                              textAlign: 'left',
                              fontWeight: '600',
                              fontSize: '14px',
                              borderBottom: '1px solid var(--border-color)'
                            }}>Location</th>
                            <th style={{
                              padding: '12px',
                              textAlign: 'left',
                              fontWeight: '600',
                              fontSize: '14px',
                              borderBottom: '1px solid var(--border-color)'
                            }}>Provider</th>
                            <th style={{
                              padding: '12px',
                              textAlign: 'left',
                              fontWeight: '600',
                              fontSize: '14px',
                              borderBottom: '1px solid var(--border-color)'
                            }}>Cabinet</th>
                            <th style={{
                              padding: '12px',
                              textAlign: 'left',
                              fontWeight: '600',
                              fontSize: '14px',
                              borderBottom: '1px solid var(--border-color)'
                            }}>Game Mix</th>
                            <th style={{
                              padding: '12px',
                              textAlign: 'left',
                              fontWeight: '600',
                              fontSize: '14px',
                              borderBottom: '1px solid var(--border-color)'
                            }}>Gaming Places</th>
                            <th style={{
                              padding: '12px',
                              textAlign: 'left',
                              fontWeight: '600',
                              fontSize: '14px',
                              borderBottom: '1px solid var(--border-color)'
                            }}>CVT Date of End</th>
                            <th style={{
                              padding: '12px',
                              textAlign: 'left',
                              fontWeight: '600',
                              fontSize: '14px',
                              borderBottom: '1px solid var(--border-color)'
                            }}>CVT Certificate</th>
                          </tr>
                        </thead>
                        <tbody>
                          {slotDetails.map((slot, index) => (
                            <tr key={slot.id} style={{
                              borderBottom: '1px solid var(--border-color)',
                              background: index % 2 === 0 ? 'var(--bg-secondary)' : 'var(--bg-tertiary)'
                            }}>
                              <td style={{
                                padding: '12px',
                                fontSize: '14px',
                                color: 'var(--text-secondary)'
                              }}>{index + 1}</td>
                              <td style={{
                                padding: '12px',
                                fontSize: '14px',
                                color: 'var(--text-secondary)'
                              }}>{slot.serialNumber}</td>
                              <td style={{
                                padding: '12px',
                                fontSize: '14px',
                                color: 'var(--text-secondary)'
                              }}>{slot.location}</td>
                              <td style={{
                                padding: '12px',
                                fontSize: '14px',
                                color: 'var(--text-secondary)'
                              }}>{slot.provider}</td>
                              <td style={{
                                padding: '12px',
                                fontSize: '14px',
                                color: 'var(--text-secondary)'
                              }}>{slot.cabinet}</td>
                              <td style={{
                                padding: '12px',
                                fontSize: '14px',
                                color: 'var(--text-secondary)'
                              }}>{slot.gameMix}</td>
                              <td style={{
                                padding: '12px',
                                fontSize: '14px',
                                color: 'var(--text-secondary)'
                              }}>{slot.gamingPlaces}</td>
                              <td style={{
                                padding: '12px',
                                fontSize: '14px',
                                color: 'var(--text-secondary)'
                              }}>{slot.cvtEndDate}</td>
                              <td style={{
                                padding: '12px',
                                fontSize: '14px',
                                color: 'var(--text-secondary)'
                              }}>{metrology.certificate_number}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  ) : (
                    <div style={{
                      textAlign: 'center',
                      padding: '40px',
                      color: 'var(--text-secondary)',
                      fontSize: '16px'
                    }}>
                      No associated slots found for this CVT certificate.
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Location Details Page Component
  const LocationDetailsPage = ({ location, onClose }) => {
    if (!location) return null;

    // Funcție pentru a găsi toate sloturile din această sală
    const getLocationSlots = () => {
      return slotMachines.filter(slot => slot.location_id === location.id);
    };

    // Funcție pentru a obține detaliile unui slot
    const getSlotDetails = (slot) => {
      const provider = providers.find(prov => prov.id === slot?.provider_id);
      const cabinet = cabinets.find(cab => cab.id === slot?.cabinet_id);
      const gameMix = gameMixes.find(gm => gm.id === slot?.game_mix_id);
      const company = companies.find(comp => comp.id === slot?.owner_company_id);
      const creator = users.find(u => u.id === slot?.created_by || u.username === slot?.created_by);
      const modifier = users.find(u => u.id === slot?.updated_by || u.username === slot?.updated_by);

      return {
        id: slot.id || slot._id,
        serialNumber: slot.serial_number || 'N/A',
        location: location?.name || 'N/A',
        provider: provider?.name || 'N/A',
        cabinet: cabinet?.name || 'N/A',
        gameMix: gameMix?.name || 'N/A',
        gamingPlaces: slot?.gaming_places || 'N/A',
        ownershipType: slot?.ownership_type || 'N/A',
        productionYear: slot?.production_year || 'N/A',
        rtp: slot?.rtp || 'N/A',
        cvtEndDate: (() => {
          const associatedMetrology = metrology.filter(mt => {
            if (!mt.serial_number) return false;
            const metrologySerialNumbers = mt.serial_number.split(/\s+/).filter(s => s.trim());
            return metrologySerialNumbers.includes(slot.serial_number);
          });
          if (associatedMetrology.length === 0) return 'No CVT';
          if (associatedMetrology.length === 1) {
            return associatedMetrology[0].cvt_expiry_date ? formatDateDDMMYYYY(associatedMetrology[0].cvt_expiry_date) : 'No End Date';
          }
          return `Multiple CVT (${associatedMetrology.length})`;
        })(),
        jackpotName: (() => {
          const associatedJackpots = jackpots.filter(jp => {
            if (!jp.serial_number) return false;
            const jackpotSerialNumbers = jp.serial_number.split(/\s+/).filter(s => s.trim());
            return jackpotSerialNumbers.includes(slot.serial_number);
          });
          if (associatedJackpots.length === 0) return 'No Jackpot';
          if (associatedJackpots.length === 1) {
            return associatedJackpots[0].jackpot_name || 'No Name';
          }
          return `Multiple Jackpots (${associatedJackpots.length})`;
        })(),
        commissionDate: (() => {
          const associatedComisionDates = comisionDates.filter(cd => {
            if (!cd.serial_numbers) return false;
            const comisionSerialNumbers = cd.serial_numbers.split(/\s+/).filter(s => s.trim());
            return comisionSerialNumbers.includes(slot.serial_number);
          });
          if (associatedComisionDates.length === 0) return 'No Commission Date';
          if (associatedComisionDates.length === 1) {
            return formatDateDDMMYYYY(associatedComisionDates[0].commission_date);
          }
          return `Multiple Dates (${associatedComisionDates.length})`;
        })(),
        createdBy: creator && creator.first_name && creator.last_name ? `${creator.first_name} ${creator.last_name}` : creator ? creator.username : slot?.created_by || 'Unknown',
        modifiedBy: modifier && modifier.first_name && modifier.last_name ? `${modifier.first_name} ${modifier.last_name}` : modifier ? modifier.username : slot?.updated_by || 'N/A',
        createdAt: slot?.created_at ? formatDateDDMMYYYY(slot.created_at) : 'N/A'
      };
    };

    const locationSlots = getLocationSlots();
    const slotDetails = locationSlots.map(getSlotDetails);

    // Funcție pentru export XLS
    const handleExportToXLS = () => {
      const data = slotDetails.map((slot, index) => ({
        'ID': index + 1,
        'Serial Number': slot.serialNumber,
        'Location': slot.location,
        'Provider': slot.provider,
        'Cabinet': slot.cabinet,
        'Game Mix': slot.gameMix,
        'Gaming Places': slot.gamingPlaces,
        'Ownership Type': slot.ownershipType,
        'Production Year': slot.productionYear,
        'RTP': slot.rtp,
        'CVT End Date': slot.cvtEndDate,
        'Jackpot Name': slot.jackpotName,
        'Commission Date': slot.commissionDate,
        'Created By': slot.createdBy,
        'Modified By': slot.modifiedBy,
        'Created At': slot.createdAt
      }));

      const ws = XLSX.utils.json_to_sheet(data);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'Location Slots');
      
      const fileName = `location_${location.name}_slots_${formatDateDDMMYYYY(new Date())}.xlsx`;
      XLSX.writeFile(wb, fileName);
    };

    return (
      <div className="app-layout" data-theme={theme}>

        {/* Content */}
        <div className="layout-container">
          <div className="main-content">
            <div className="content-body">
              <div style={{ padding: '20px' }}>
                {/* Header Info */}
                <div style={{ 
                  background: 'var(--bg-secondary)', 
                  borderRadius: '12px', 
                  padding: '24px', 
                  marginBottom: '24px',
                  border: '1px solid var(--border-color)'
                }}>
                  <div style={{ 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    alignItems: 'center', 
                    marginBottom: '16px' 
                  }}>
                    <h1 style={{ 
                      color: 'var(--text-primary)', 
                      margin: '0',
                      fontSize: '24px',
                      fontWeight: '700'
                    }}>
                      🏢 {location.name || 'Unnamed Location'}
                    </h1>
                    <button 
                      onClick={onClose}
                      style={{
                        background: 'var(--gradient-primary)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '8px',
                        padding: '8px 16px',
                        cursor: 'pointer',
                        fontSize: '14px',
                        fontWeight: '600',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px'
                      }}
                    >
                      ← Back
                    </button>
                  </div>
                  
                  <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
                    gap: '16px' 
                  }}>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>🏢 Location Name:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {location.name}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>📍 Address:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {location.address || 'N/A'}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>📊 Number of Slots:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {locationSlots.length}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>🎮 Total Gaming Places:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {locationSlots.reduce((total, slot) => total + (parseInt(slot.gaming_places) || 0), 0)}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Slots Table */}
                {locationSlots.length > 0 && (
                  <div style={{ 
                    background: 'var(--bg-secondary)', 
                    borderRadius: '12px', 
                    padding: '24px',
                    border: '1px solid var(--border-color)'
                  }}>
                    <div style={{ 
                      display: 'flex', 
                      justifyContent: 'space-between', 
                      alignItems: 'center',
                      marginBottom: '20px'
                    }}>
                      <h2 style={{ 
                        color: 'var(--text-primary)', 
                        fontSize: '20px',
                        fontWeight: '600',
                        margin: '0'
                      }}>
                        🎰 All Slots in {location.name}
                      </h2>
                      <button
                        onClick={handleExportToXLS}
                        style={{
                          background: 'var(--gradient-primary)',
                          color: 'white',
                          border: 'none',
                          borderRadius: '8px',
                          padding: '8px 16px',
                          cursor: 'pointer',
                          fontSize: '14px',
                          fontWeight: '600',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '8px'
                        }}
                      >
                        📊 Export to XLS
                      </button>
                    </div>
                    <div className="table-responsive">
                      <table className="data-table">
                        <thead>
                          <tr>
                            <th>ID</th>
                            <th>Serial Number</th>
                            <th>Provider</th>
                            <th>Cabinet</th>
                            <th>Game Mix</th>
                            <th>Gaming Places</th>
                            <th>Ownership Type</th>
                            <th>Production Year</th>
                            <th>RTP</th>
                            <th>CVT End Date</th>
                            <th>Jackpot Name</th>
                            <th>Commission Date</th>
                            <th>Created By</th>
                            <th>Modified By</th>
                            <th>Created At</th>
                          </tr>
                        </thead>
                        <tbody>
                          {slotDetails.map((slot, index) => (
                            <tr key={index}>
                              <td>{index + 1}</td>
                              <td>{slot.serialNumber}</td>
                              <td>{slot.provider}</td>
                              <td>{slot.cabinet}</td>
                              <td>{slot.gameMix}</td>
                              <td>{slot.gamingPlaces}</td>
                              <td>{slot.ownershipType}</td>
                              <td>{slot.productionYear}</td>
                              <td>{slot.rtp}</td>
                              <td>{slot.cvtEndDate}</td>
                              <td>{slot.jackpotName}</td>
                              <td>{slot.commissionDate}</td>
                              <td>{slot.createdBy}</td>
                              <td>{slot.modifiedBy}</td>
                              <td>{slot.createdAt}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Invoice Details Page Component
  const InvoiceDetailsPage = ({ invoice, onClose }) => {
    if (!invoice) return null;

    // Funcție pentru a găsi toate sloturile asociate cu acest invoice
    const getAssociatedSlots = () => {
      if (!invoice.serial_numbers) return [];
      
      // Try both newline and space separation
      const serialNumbersNewline = invoice.serial_numbers.split('\n').filter(s => s.trim());
      const serialNumbersSpace = invoice.serial_numbers.split(' ').filter(s => s.trim());
      
      // Use the one that has more items (more likely to be correct)
      const serialNumbers = serialNumbersNewline.length > serialNumbersSpace.length ? 
        serialNumbersNewline : serialNumbersSpace;
      
      return slotMachines.filter(slot => serialNumbers.includes(slot.serial_number));
    };

    // Funcție pentru a obține detaliile unui slot
    const getSlotDetails = (slot) => {
      const location = locations.find(loc => loc.id === slot?.location_id);
      const provider = providers.find(prov => prov.id === slot?.provider_id);
      const cabinet = cabinets.find(cab => cab.id === slot?.cabinet_id);
      const gameMix = gameMixes.find(gm => gm.id === slot?.game_mix_id);

      return {
        id: slot.id || slot._id,
        serialNumber: slot.serial_number || 'N/A',
        location: location?.name || 'N/A',
        provider: provider?.name || 'N/A',
        cabinet: cabinet?.name || 'N/A',
        gameMix: gameMix?.name || 'N/A',
        gamingPlaces: slot?.gaming_places || 'N/A',
        invoiceNumber: invoice?.invoice_number || 'N/A'
      };
    };

    const associatedSlots = getAssociatedSlots();
    const slotDetails = associatedSlots.map(getSlotDetails);

    // Funcție pentru export XLS
    const handleExportToXLS = () => {
      const data = slotDetails.map((slot, index) => ({
        'ID': index + 1,
        'Serial Number': slot.serialNumber,
        'Location': slot.location,
        'Provider': slot.provider,
        'Cabinet': slot.cabinet,
        'Game Mix': slot.gameMix,
        'Gaming Places': slot.gamingPlaces,
        'Invoice Number': slot.invoiceNumber
      }));

      const ws = XLSX.utils.json_to_sheet(data);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'Invoice Slots');
      
      const fileName = `invoice_${invoice.invoice_number}_slots_${formatDateDDMMYYYY(new Date())}.xlsx`;
      XLSX.writeFile(wb, fileName);
    };

    return (
      <div className="app-layout" data-theme={theme}>


        {/* Content */}
        <div className="layout-container">
          <div className="main-content">
            <div className="content-body">
              <div style={{ padding: '20px' }}>
                {/* Header Info */}
                <div style={{ 
                  background: 'var(--bg-secondary)', 
                  borderRadius: '12px', 
                  padding: '24px', 
                  marginBottom: '24px',
                  border: '1px solid var(--border-color)'
                }}>
                  <div style={{ 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    alignItems: 'center', 
                    marginBottom: '16px' 
                  }}>
                    <h1 style={{ 
                      color: 'var(--text-primary)', 
                      margin: '0',
                      fontSize: '24px',
                      fontWeight: '700'
                    }}>
                      📄 {invoice.invoice_number || 'Unnamed Invoice'}
                    </h1>
                    <button 
                      onClick={onClose}
                      style={{
                        background: 'var(--gradient-primary)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '8px',
                        padding: '8px 16px',
                        cursor: 'pointer',
                        fontSize: '14px',
                        fontWeight: '600',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px'
                      }}
                    >
                      ← Back
                    </button>
                  </div>
                  
                  <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
                    gap: '16px' 
                  }}>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>📄 Invoice Number:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {invoice.invoice_number}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>🏢 Company:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {invoice.company_name || 'N/A'}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>📅 Issue Date:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {invoice.issue_date ? formatDateDDMMYYYY(invoice.issue_date) : 'N/A'}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>📅 Due Date:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {invoice.due_date ? formatDateDDMMYYYY(invoice.due_date) : 'N/A'}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>💰 Amount:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {invoice.amount ? `${invoice.amount} RON` : 'N/A'}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>📊 Status:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {invoice.status || 'N/A'}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>📝 Description:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {invoice.description || 'N/A'}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>👤 Created by:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {(() => {
                          const user = Array.isArray(users) ? users.find(u => u.username === invoice.created_by) : null;
                          return user ? `${user.first_name} ${user.last_name}` : invoice.creator_name || 'Unknown';
                        })()}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>💼 Transaction Type:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {invoice.transaction_type || 'N/A'}
                      </p>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '14px' }}>📅 Created:</strong>
                      <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                        {invoice.created_at ? formatDateDDMMYYYY(invoice.created_at) : 'N/A'}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Slot Details Table */}
                <div style={{ 
                  background: 'var(--bg-secondary)', 
                  borderRadius: '12px', 
                  padding: '24px', 
                  marginBottom: '24px',
                  border: '1px solid var(--border-color)'
                }}>
                  <div style={{ 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    alignItems: 'center', 
                    marginBottom: '20px' 
                  }}>
                    <h2 style={{ 
                      color: 'var(--text-primary)', 
                      margin: '0',
                      fontSize: '20px',
                      fontWeight: '600'
                    }}>
                      🎰 Slot Details for Each Serial Number ({slotDetails.length})
                    </h2>
                    <button 
                      onClick={handleExportToXLS}
                      style={{
                        background: 'var(--gradient-primary)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '8px',
                        padding: '8px 16px',
                        cursor: 'pointer',
                        fontSize: '14px',
                        fontWeight: '600',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px'
                      }}
                    >
                      📊 Export to XLS
                    </button>
                  </div>
                  
                  {slotDetails.length > 0 ? (
                    <div className="table-container">
                      <table className="data-table">
                        <thead>
                          <tr>
                            <th>ID</th>
                            <th>Serial Number</th>
                            <th>Location</th>
                            <th>Provider</th>
                            <th>Cabinet</th>
                            <th>Game Mix</th>
                            <th>Gaming Places</th>
                            <th>Invoice Number</th>
                          </tr>
                        </thead>
                        <tbody>
                          {slotDetails.map((slot, index) => (
                            <tr key={slot.id}>
                              <td>{index + 1}</td>
                              <td>{slot.serialNumber}</td>
                              <td>{slot.location}</td>
                              <td>{slot.provider}</td>
                              <td>{slot.cabinet}</td>
                              <td>{slot.gameMix}</td>
                              <td>{slot.gamingPlaces}</td>
                              <td>{slot.invoiceNumber}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  ) : (
                    <div style={{
                      textAlign: 'center',
                      padding: '40px',
                      color: 'var(--text-secondary)',
                      fontSize: '16px'
                    }}>
                      No associated slots found for this invoice.
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // History Changes Page Component
  const HistoryChangesPage = React.memo(({ onClose }) => {
    const [historyData, setHistoryData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [authError, setAuthError] = useState(false);
    const hasFetchedRef = React.useRef(false);
    const cacheRef = React.useRef(null);
    const [filters, setFilters] = useState({
      dateFrom: '',
      dateTo: '',
      location: '',
      provider: '',
      gameMix: ''
    });
    const [multiFilters, setMultiFilters] = useState({ locations: [], providers: [], gameMixes: [] });
    const [openDropdown, setOpenDropdown] = useState(null);
    const [globalQuery, setGlobalQuery] = useState('');
    const [dropdownQuery, setDropdownQuery] = useState({ locations: '', providers: '', gameMixes: '' });
    // Date range filter (with presets)
    const [dateRange, setDateRange] = useState(() => {
      const now = new Date();
      const startMonth = new Date(now.getFullYear(), now.getMonth(), 1, 0, 0, 0, 0);
      const endMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0, 23, 59, 59, 999);
      return { from: startMonth, to: endMonth, preset: 'this_month' };
    });

    const startOfDay = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate(), 0, 0, 0, 0);
    const endOfDay = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate(), 23, 59, 59, 999);
    const startOfWeekMonday = (d) => {
      const day = d.getDay(); // 0=Sun ... 6=Sat
      const diff = (day === 0 ? -6 : 1 - day); // shift to Monday
      const res = new Date(d);
      res.setDate(d.getDate() + diff);
      return startOfDay(res);
    };
    const endOfWeekSunday = (d) => {
      const start = startOfWeekMonday(d);
      const res = new Date(start);
      res.setDate(start.getDate() + 6);
      return endOfDay(res);
    };

    const applyPreset = (preset) => {
      const now = new Date();
      let from = null; let to = null;
      if (preset === 'today') {
        from = startOfDay(now); to = endOfDay(now);
      } else if (preset === 'this_week') {
        from = startOfWeekMonday(now); to = endOfWeekSunday(now);
      } else if (preset === 'this_month') {
        from = new Date(now.getFullYear(), now.getMonth(), 1, 0, 0, 0, 0);
        to = new Date(now.getFullYear(), now.getMonth() + 1, 0, 23, 59, 59, 999);
      } else if (preset === 'last_month') {
        const last = new Date(now.getFullYear(), now.getMonth() - 1, 1);
        from = new Date(last.getFullYear(), last.getMonth(), 1, 0, 0, 0, 0);
        to = new Date(last.getFullYear(), last.getMonth() + 1, 0, 23, 59, 59, 999);
      } else if (preset === 'this_year') {
        from = new Date(now.getFullYear(), 0, 1, 0, 0, 0, 0);
        to = new Date(now.getFullYear(), 11, 31, 23, 59, 59, 999);
      } else if (preset === 'prev_year') {
        const y = now.getFullYear() - 1;
        from = new Date(y, 0, 1, 0, 0, 0, 0);
        to = new Date(y, 11, 31, 23, 59, 59, 999);
      } else if (preset === 'all_time') {
        from = null; to = null;
      }
      setDateRange({ from, to, preset });
    };

    const formatDateTimeDDMMYYYYHHMM = (value) => {
      if (!value) return '';
      const d = new Date(value);
      if (Number.isNaN(d.getTime())) return '';
      const dd = String(d.getDate()).padStart(2, '0');
      const mm = String(d.getMonth() + 1).padStart(2, '0');
      const yyyy = d.getFullYear();
      const hh = String(d.getHours()).padStart(2, '0');
      const mi = String(d.getMinutes()).padStart(2, '0');
      return `${dd}.${mm}.${yyyy} ${hh}:${mi}`;
    };

    // Helpers to parse Calendar (yyyy-mm-dd) to Date at day bounds
    const parseYMDToStart = (val) => {
      if (!val) return null;
      const [y, m, d] = String(val).split('-').map(Number);
      if (!y || !m || !d) return null;
      return new Date(y, m - 1, d, 0, 0, 0, 0);
    };
    const parseYMDToEnd = (val) => {
      if (!val) return null;
      const [y, m, d] = String(val).split('-').map(Number);
      if (!y || !m || !d) return null;
      return new Date(y, m - 1, d, 23, 59, 59, 999);
    };

    // Fetch history data
    const fetchHistoryData = async () => {
      if (hasFetchedRef.current && cacheRef.current) {
        setHistoryData(cacheRef.current);
        setLoading(false);
        return;
      }
      try {
        setLoading(true);
        const response = await fetch(`${API}/change-history/slots/all`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        if (response.ok) {
          const data = await response.json();
          // Fallback: if backend 'all' endpoint returns empty, aggregate per-entity
          if (Array.isArray(data) && data.length === 0) {
            try {
              const token = localStorage.getItem('token');
              const slotsRes = await fetch(`${API}/slot-machines`, {
                headers: { 'Authorization': `Bearer ${token}` }
              });
              if (slotsRes.ok) {
                const slots = await slotsRes.json();
                const slotIds = (Array.isArray(slots) ? slots : []).map(s => s.id).filter(Boolean).slice(0, 150);
                const results = await Promise.all(
                  slotIds.map(id => (
                    fetch(`${API}/change-history/slots/${id}`, {
                      headers: { 'Authorization': `Bearer ${token}` }
                    })
                      .then(r => r.ok ? r.json() : [])
                      .catch(() => [])
                  ))
                );
                const merged = results.flat().sort((a, b) => new Date(b.created_at || b.scheduled_datetime || 0) - new Date(a.created_at || a.scheduled_datetime || 0)).slice(0, 500);
                cacheRef.current = merged;
                hasFetchedRef.current = true;
                setHistoryData(merged);
              } else {
                cacheRef.current = [];
                hasFetchedRef.current = true;
                setHistoryData([]);
              }
            } catch (e) {
              cacheRef.current = [];
              hasFetchedRef.current = true;
              setHistoryData([]);
            }
          } else {
            cacheRef.current = data;
            hasFetchedRef.current = true;
            setHistoryData(data);
          }
        } else {
          if (response.status === 401 || response.status === 403) {
            setAuthError(true);
            showCustomNotification('Not authenticated. Please login again.', 'error');
          } else {
            console.error('Failed to fetch history data');
            showCustomNotification('Failed to fetch history data', 'error');
          }
        }
      } catch (error) {
        console.error('Error fetching history data:', error);
        showCustomNotification('Error fetching history data', 'error');
      } finally {
        setLoading(false);
      }
    };

    // Fetch only once on mount
    useEffect(() => {
      fetchHistoryData();
    }, []); // ok to run once; fetchHistoryData uses stable API/constants

    // Enrichment helper (must be defined BEFORE using in memos)
    const getContextForItem = (item) => {
      const slot = (Array.isArray(slotMachines) ? slotMachines : []).find(s => s.id === item.entity_id);
      const serial = slot?.serial_number || item.serial_number || 'N/A';
      const locationName = (Array.isArray(locations) ? locations : []).find(l => l.id === slot?.location_id)?.name
        || item.location_name || 'N/A';
      const providerName = (Array.isArray(providers) ? providers : []).find(p => p.id === slot?.provider_id)?.name
        || item.provider_name || 'N/A';
      const gameMixName = (Array.isArray(gameMixes) ? gameMixes : []).find(g => g.id === slot?.game_mix_id)?.name
        || item.game_mix_name || 'N/A';
      const modifiedBy = item.modified_by || item.user_name || 'N/A';
      return { serial, locationName, providerName, gameMixName, modifiedBy };
    };

    // Keep inputs controlled locally without format flips on each change
    const setDateFrom = useCallback((val) => {
      setFilters(prev => ({ ...prev, dateFrom: val }));
    }, []);
    const setDateTo = useCallback((val) => {
      setFilters(prev => ({ ...prev, dateTo: val }));
    }, []);

    // Parse dd.mm.yyyy into a Date (start or end of day)
    const parseDateDDMMYYYY = (value, endOfDay = false) => {
      if (!value || typeof value !== 'string') return null;
      const match = value.match(/^(\d{1,2})\.(\d{1,2})\.(\d{4})$/);
      if (!match) return null;
      const day = parseInt(match[1], 10);
      const monthIndex = parseInt(match[2], 10) - 1; // 0-based
      const year = parseInt(match[3], 10);
      const date = new Date(year, monthIndex, day);
      if (Number.isNaN(date.getTime())) return null;
      if (endOfDay) {
        date.setHours(23, 59, 59, 999);
      } else {
        date.setHours(0, 0, 0, 0);
      }
      return date;
    };

    // Options for multi-select dropdowns
    const locationOptions = React.useMemo(() => {
      const set = new Set();
      (historyData || []).forEach(it => set.add(getContextForItem(it).locationName));
      set.delete('N/A');
      return Array.from(set).sort();
    }, [historyData]);
    const providerOptions = React.useMemo(() => {
      const set = new Set();
      (historyData || []).forEach(it => set.add(getContextForItem(it).providerName));
      set.delete('N/A');
      return Array.from(set).sort();
    }, [historyData]);
    const gameMixOptions = React.useMemo(() => {
      const set = new Set();
      (historyData || []).forEach(it => set.add(getContextForItem(it).gameMixName));
      set.delete('N/A');
      return Array.from(set).sort();
    }, [historyData]);

    // Filter history data (multiselect OR within group, AND across groups)
    const filteredData = historyData.filter(item => {
      const ctx = getContextForItem(item);
      if (multiFilters.locations.length && !multiFilters.locations.includes(ctx.locationName)) return false;
      if (multiFilters.providers.length && !multiFilters.providers.includes(ctx.providerName)) return false;
      if (multiFilters.gameMixes.length && !multiFilters.gameMixes.includes(ctx.gameMixName)) return false;
      if (dateRange && (dateRange.from || dateRange.to)) {
        const when = new Date(item.created_at || item.applied_datetime || item.scheduled_datetime || 0);
        if (dateRange.from && when < dateRange.from) return false;
        if (dateRange.to && when > dateRange.to) return false;
      }
      if (globalQuery) {
        const q = globalQuery.toLowerCase();
        const hay = [
          ctx.serial,
          ctx.locationName,
          ctx.providerName,
          ctx.gameMixName,
          item.field_name,
          item.old_value,
          item.new_value,
          item.modified_by || item.user_name,
          item.modification_type || item.change_type,
          item.created_at,
          item.scheduled_datetime,
          item.applied_datetime
        ]
          .filter(Boolean)
          .join(' | ')
          .toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });

    // Handle date input click to prevent calendar from closing
    const handleDateInputClick = (e) => {
      e.preventDefault();
      e.stopPropagation();
      e.target.showPicker?.();
    };

    // (moved earlier to avoid temporal dead-zone)

    // Export to XLS
    const handleExportToXLS = () => {
      const data = filteredData.map((item, index) => ({
        'ID': index + 1,
        ...(() => { const c = getContextForItem(item); return {
          'Serial Number': c.serial,
          'Location': c.locationName,
          'Provider': c.providerName,
          'Game Mix': c.gameMixName,
        }; })(),
        'Field Modified': item.field_name || 'N/A',
        'Old Value': item.old_value || 'N/A',
        'New Value': item.new_value || 'N/A',
        'Modified By': getContextForItem(item).modifiedBy,
        'Modified At': item.created_at ? formatDateDDMMYYYY(item.created_at) : 'N/A',
        'Modification Type': item.modification_type || 'Manual'
      }));

      const ws = XLSX.utils.json_to_sheet(data);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'History Changes');
      
      const fileName = `history_changes_${formatDateDDMMYYYY(new Date())}.xlsx`;
      XLSX.writeFile(wb, fileName);
    };

    return (
      <div className="app-layout" data-theme={theme}>

        {/* Content */}
        <div className="layout-container">
          <div className="main-content">
            <div className="content-body">
              <div style={{ padding: '20px' }}>
                {/* Header */}
                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between', 
                  alignItems: 'center', 
                  marginBottom: '24px' 
                }}>
                  <h1 style={{ 
                    color: 'var(--text-primary)', 
                    margin: '0',
                    fontSize: '24px',
                    fontWeight: '700'
                  }}>
                    📊 All History Changes
                  </h1>
                  <div style={{ display: 'flex', gap: '10px' }}>
                    <button 
                      onClick={handleExportToXLS}
                      style={{
                        background: 'var(--gradient-primary)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '8px',
                        padding: '8px 16px',
                        cursor: 'pointer',
                        fontSize: '14px',
                        fontWeight: '600',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px'
                      }}
                    >
                      📥 Export XLS
                    </button>
                    <button 
                      onClick={onClose}
                      style={{
                        background: 'var(--bg-secondary)',
                        color: 'var(--text-primary)',
                        border: '1px solid var(--border-color)',
                        borderRadius: '8px',
                        padding: '8px 16px',
                        cursor: 'pointer',
                        fontSize: '14px',
                        fontWeight: '600'
                      }}
                    >
                      ✕ Close
                    </button>
                  </div>
                </div>

                {/* Filters */}
                <div style={{ 
                  background: 'var(--bg-secondary)', 
                  borderRadius: '12px', 
                  padding: '20px', 
                  marginBottom: '24px',
                  border: '1px solid var(--border-color)'
                }}>
                  <h3 style={{ 
                    color: 'var(--text-primary)', 
                    margin: '0 0 16px 0',
                    fontSize: '18px',
                    fontWeight: '600'
                  }}>
                    🔍 Filters
                  </h3>
                  <div style={{ display:'flex', gap: '12px', flexWrap: 'wrap' }}>
                    {/* Global search */}
                    <div style={{ flex:'1 1 240px' }}>
                      <input
                        type="text"
                        placeholder="Search in any column..."
                        value={globalQuery}
                        onChange={(e) => setGlobalQuery(e.target.value)}
                        style={{ width:'100%', padding:'8px 12px', border:'1px solid var(--border-color)', borderRadius:6, background:'var(--bg-primary)', color:'var(--text-primary)' }}
                      />
                    </div>
                    {/* Date presets */}
                    <div style={{ display:'flex', gap:6, alignItems:'center', flexWrap:'wrap' }}>
                      {[
                        {k:'today', t:'Today'},
                        {k:'this_week', t:'This week'},
                        {k:'this_month', t:'This month'},
                        {k:'last_month', t:'Last month'},
                        {k:'this_year', t:'This year'},
                        {k:'prev_year', t:'Previous year'},
                        {k:'all_time', t:'All time'}
                      ].map(p => (
                        <button key={p.k} onClick={() => applyPreset(p.k)} style={{
                          background: dateRange.preset===p.k? 'var(--gradient-primary)':'transparent',
                          color: dateRange.preset===p.k? '#fff':'var(--text-primary)',
                          border: '1px solid var(--border-color)', borderRadius:6, padding:'6px 10px', height:32, fontSize:12, cursor:'pointer'
                        }}>{p.t}</button>
                      ))}
                      <div style={{ display:'flex', gap:6, alignItems:'center', marginLeft:8 }}>
                        <input
                          type="date"
                          value={dateRange.from ? `${dateRange.from.getFullYear()}-${String(dateRange.from.getMonth()+1).padStart(2,'0')}-${String(dateRange.from.getDate()).padStart(2,'0')}` : ''}
                          onChange={(e) => setDateRange(prev => ({ ...prev, from: parseYMDToStart(e.target.value), preset: 'custom' }))}
                          style={{ height:32, padding:'6px 8px', border:'1px solid var(--border-color)', borderRadius:6, background:'var(--bg-primary)', color:'var(--text-primary)' }}
                        />
                        <span style={{ color:'var(--text-secondary)', fontSize:12 }}>to</span>
                        <input
                          type="date"
                          value={dateRange.to ? `${dateRange.to.getFullYear()}-${String(dateRange.to.getMonth()+1).padStart(2,'0')}-${String(dateRange.to.getDate()).padStart(2,'0')}` : ''}
                          onChange={(e) => setDateRange(prev => ({ ...prev, to: parseYMDToEnd(e.target.value), preset: 'custom' }))}
                          style={{ height:32, padding:'6px 8px', border:'1px solid var(--border-color)', borderRadius:6, background:'var(--bg-primary)', color:'var(--text-primary)' }}
                        />
                        <button onClick={() => applyPreset('all_time')} style={{
                          background: 'transparent', color:'var(--text-primary)', border:'1px solid var(--border-color)', borderRadius:6, padding:'6px 10px', height:32, fontSize:12, cursor:'pointer'
                        }}>Clear</button>
                      </div>
                    </div>
                    {[
                      { key:'locations', label:'Location', options: locationOptions },
                      { key:'providers', label:'Provider', options: providerOptions },
                      { key:'gameMixes', label:'Game Mix', options: gameMixOptions }
                    ].map(group => (
                      <div key={group.key} style={{ position:'relative' }}>
                        <button
                          onClick={() => setOpenDropdown(openDropdown === group.key ? null : group.key)}
                          aria-expanded={openDropdown === group.key}
                          className="btn-secondary"
                          style={{ minWidth: 180, display:'flex', justifyContent:'space-between', alignItems:'center' }}
                        >
                          <span>{group.label}</span>
                          <span style={{ opacity: 0.7 }}>{multiFilters[group.key].length || 0}</span>
                        </button>
                        {openDropdown === group.key && (
                          <div style={{ position:'absolute', zIndex:10, top:'calc(100% + 6px)', left:0, width:260, background:'var(--bg-primary)', border:'1px solid var(--border-color)', borderRadius:8, padding:10, boxShadow:'0 8px 24px rgba(0,0,0,0.3)' }}>
                            <input
                              type="text"
                              placeholder={`Search ${group.label.toLowerCase()}...`}
                              value={dropdownQuery[group.key] || ''}
                              onChange={(e) => setDropdownQuery(prev => ({ ...prev, [group.key]: e.target.value }))}
                              style={{ width:'100%', padding:'6px 10px', border:'1px solid var(--border-color)', borderRadius:6, background:'var(--bg-primary)', color:'var(--text-primary)' }}
                            />
                            <div style={{ maxHeight:220, overflowY:'auto', marginTop:6 }}>
                              {(group.options.filter(o => (dropdownQuery[group.key] ? o.toLowerCase().includes((dropdownQuery[group.key]||'').toLowerCase()) : true))).map(opt => {
                                const checked = multiFilters[group.key].includes(opt);
                                return (
                                  <label key={opt} style={{ display:'flex', alignItems:'center', gap:8, padding:'6px 4px', cursor:'pointer' }}>
                                    <input
                                      type="checkbox"
                                      checked={checked}
                                      onChange={(e) => {
                                        setMultiFilters(prev => {
                                          const next = new Set(prev[group.key]);
                                          if (e.target.checked) next.add(opt); else next.delete(opt);
                                          return { ...prev, [group.key]: Array.from(next) };
                                        });
                                      }}
                                    />
                                    <span>{opt}</span>
                                  </label>
                                );
                              })}
                            </div>
                            <div style={{ display:'flex', justifyContent:'flex-end', gap:6, marginTop:8 }}>
                              <button
                                onClick={() => setMultiFilters(prev => ({ ...prev, [group.key]: group.options.slice(0, 2000) }))}
                                style={{
                                  background:'transparent', border:'1px solid var(--border-color)', color:'var(--text-primary)',
                                  padding:'6px 10px', height:32, borderRadius:6, fontSize:12, cursor:'pointer'
                                }}
                              >Select all</button>
                              <button
                                onClick={() => setMultiFilters(prev => ({ ...prev, [group.key]: [] }))}
                                style={{
                                  background:'transparent', border:'1px solid var(--border-color)', color:'var(--text-primary)',
                                  padding:'6px 10px', height:32, borderRadius:6, fontSize:12, cursor:'pointer'
                                }}
                              >Clear</button>
                              <button
                                onClick={() => setOpenDropdown(null)}
                                style={{
                                  background:'transparent', border:'1px solid var(--border-color)', color:'var(--text-primary)',
                                  padding:'6px 10px', height:32, borderRadius:6, fontSize:12, cursor:'pointer'
                                }}
                              >Apply</button>
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Results */}
                <div style={{ 
                  background: 'var(--bg-primary)', 
                  borderRadius: '12px', 
                  padding: '20px',
                  border: '1px solid var(--border-color)'
                }}>
                  <div style={{ 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    alignItems: 'center', 
                    marginBottom: '16px' 
                  }}>
                    <h3 style={{ 
                      color: 'var(--text-primary)', 
                      margin: '0',
                      fontSize: '18px',
                      fontWeight: '600'
                    }}>
                      📋 History Records ({filteredData.length})
                    </h3>
                  </div>

                  {authError ? (
                    <div style={{
                      textAlign: 'center',
                      padding: '40px',
                      color: 'var(--text-secondary)',
                      fontSize: '16px'
                    }}>
                      Not authenticated. Please login.
                      <div style={{ marginTop: '12px' }}>
                        <button
                          onClick={() => { localStorage.removeItem('token'); window.location.reload(); }}
                          style={{
                            background: 'var(--gradient-primary)',
                            color: '#fff',
                            border: 'none',
                            borderRadius: '6px',
                            padding: '8px 12px',
                            cursor: 'pointer'
                          }}
                        >
                          Re-login
                        </button>
                      </div>
                    </div>
                  ) : loading ? (
                    <div style={{
                      textAlign: 'center',
                      padding: '40px',
                      color: 'var(--text-secondary)',
                      fontSize: '16px'
                    }}>
                      Loading history data...
                    </div>
                  ) : filteredData.length > 0 ? (
                    <div style={{ overflowX: 'auto' }}>
                      <table style={{
                        width: '100%',
                        borderCollapse: 'collapse',
                        fontSize: '14px'
                      }}>
                        <thead>
                          <tr style={{
                            backgroundColor: 'var(--bg-secondary)',
                            borderBottom: '2px solid var(--border-color)'
                          }}>
                          <th style={{
                            padding: '12px 8px',
                            textAlign: 'left',
                            fontWeight: 'bold',
                            color: 'var(--text-primary)',
                            borderBottom: '1px solid var(--border-color)',
                            fontSize: '13px'
                          }}>
                            ID
                          </th>
                           <th style={{
                            padding: '12px 8px',
                            textAlign: 'left',
                            fontWeight: 'bold',
                            color: 'var(--text-primary)',
                            borderBottom: '1px solid var(--border-color)',
                            fontSize: '13px'
                          }}>
                            Serial Number
                          </th>
                          <th style={{
                            padding: '12px 8px',
                            textAlign: 'left',
                            fontWeight: 'bold',
                            color: 'var(--text-primary)',
                            borderBottom: '1px solid var(--border-color)',
                            fontSize: '13px'
                          }}>
                            Location
                          </th>
                          <th style={{
                            padding: '12px 8px',
                            textAlign: 'left',
                            fontWeight: 'bold',
                            color: 'var(--text-primary)',
                            borderBottom: '1px solid var(--border-color)',
                            fontSize: '13px'
                          }}>
                            Provider
                          </th>
                          <th style={{
                            padding: '12px 8px',
                            textAlign: 'left',
                            fontWeight: 'bold',
                            color: 'var(--text-primary)',
                            borderBottom: '1px solid var(--border-color)',
                            fontSize: '13px'
                          }}>
                            Game Mix
                          </th>
                          <th style={{
                            padding: '12px 8px',
                            textAlign: 'left',
                            fontWeight: 'bold',
                            color: 'var(--text-primary)',
                            borderBottom: '1px solid var(--border-color)',
                            fontSize: '13px'
                          }}>
                            Field Modified
                          </th>
                          <th style={{
                            padding: '12px 8px',
                            textAlign: 'left',
                            fontWeight: 'bold',
                            color: 'var(--text-primary)',
                            borderBottom: '1px solid var(--border-color)',
                            fontSize: '13px'
                          }}>
                            Old Value
                          </th>
                          <th style={{
                            padding: '12px 8px',
                            textAlign: 'left',
                            fontWeight: 'bold',
                            color: 'var(--text-primary)',
                            borderBottom: '1px solid var(--border-color)',
                            fontSize: '13px'
                          }}>
                            New Value
                          </th>
                          <th style={{
                            padding: '12px 8px',
                            textAlign: 'left',
                            fontWeight: 'bold',
                            color: 'var(--text-primary)',
                            borderBottom: '1px solid var(--border-color)',
                            fontSize: '13px'
                          }}>
                            Modified By
                          </th>
                          <th style={{
                            padding: '12px 8px',
                            textAlign: 'left',
                            fontWeight: 'bold',
                            color: 'var(--text-primary)',
                            borderBottom: '1px solid var(--border-color)',
                            fontSize: '13px'
                          }}>
                            Modified At
                          </th>
                          <th style={{
                            padding: '12px 8px',
                            textAlign: 'left',
                            fontWeight: 'bold',
                            color: 'var(--text-primary)',
                            borderBottom: '1px solid var(--border-color)',
                            fontSize: '13px'
                          }}>
                            Type
                          </th>
                        </tr>
                        </thead>
                        <tbody>
                          {filteredData.map((item, index) => (
                            <tr key={item.id || index} style={{
                              borderBottom: '1px solid var(--border-color)',
                              background: index % 2 === 0 ? 'var(--bg-secondary)' : 'var(--bg-tertiary)'
                            }}>
                              <td style={{
                                padding: '12px 8px',
                                fontSize: '13px',
                                color: 'var(--text-secondary)'
                              }}>
                                {index + 1}
                              </td>
                              <td style={{
                                padding: '12px 8px',
                                fontSize: '13px',
                                color: 'var(--text-secondary)',
                                fontWeight: 'bold'
                              }}>
                                {getContextForItem(item).serial}
                              </td>
                              <td style={{
                                padding: '12px 8px',
                                fontSize: '13px',
                                color: 'var(--text-secondary)'
                              }}>
                                {getContextForItem(item).locationName}
                              </td>
                              <td style={{
                                padding: '12px 8px',
                                fontSize: '13px',
                                color: 'var(--text-secondary)'
                              }}>
                                {getContextForItem(item).providerName}
                              </td>
                              <td style={{
                                padding: '12px 8px',
                                fontSize: '13px',
                                color: 'var(--text-secondary)'
                              }}>
                                {getContextForItem(item).gameMixName}
                              </td>
                              <td style={{
                                padding: '12px 8px',
                                fontSize: '13px',
                                color: 'var(--text-secondary)',
                                fontWeight: 'bold'
                              }}>
                                {item.field_name || 'N/A'}
                              </td>
                              <td style={{
                                padding: '12px 8px',
                                fontSize: '13px',
                                color: 'var(--text-secondary)',
                                maxWidth: '150px',
                                wordBreak: 'break-word'
                              }}>
                                {item.old_value || 'N/A'}
                              </td>
                              <td style={{
                                padding: '12px 8px',
                                fontSize: '13px',
                                color: 'var(--text-secondary)',
                                maxWidth: '150px',
                                wordBreak: 'break-word'
                              }}>
                                {item.new_value || 'N/A'}
                              </td>
                      <td style={{
                                padding: '12px 8px',
                                fontSize: '13px',
                                color: 'var(--text-secondary)'
                              }}>
                        {(() => {
                          const type = (item.modification_type || item.change_type || '').toLowerCase();
                          const isTimer = type === 'scheduled' || !!item.applied_datetime || !!item.scheduled_datetime;
                          const name = item.modified_by || item.user_name || (isTimer ? 'Timer' : 'N/A');
                          return name;
                        })()}
                              </td>
                      <td style={{
                                padding: '12px 8px',
                                fontSize: '13px',
                                color: 'var(--text-secondary)'
                              }}>
                        {(() => {
                          const when = item.applied_datetime || item.created_at || item.scheduled_datetime;
                          return when ? formatDateTimeDDMMYYYYHHMM(when) : 'N/A';
                        })()}
                              </td>
                      <td style={{
                                padding: '12px 8px',
                                fontSize: '13px',
                                color: 'var(--text-secondary)'
                              }}>
                        {(() => {
                          const raw = (item.change_type || item.modification_type || '').toLowerCase();
                          const isTimer = raw === 'scheduled';
                          const label = isTimer ? 'Timer' : 'Manual';
                          const bg = isTimer ? '#ffd700' : '#4caf50';
                          const color = isTimer ? '#000' : '#fff';
                          return (
                            <span style={{ padding:'4px 8px', borderRadius:'4px', fontSize:'11px', fontWeight:'bold', backgroundColor:bg, color }}>
                              {label}
                            </span>
                          );
                        })()}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  ) : (
                    <div style={{
                      textAlign: 'center',
                      padding: '40px',
                      color: 'var(--text-secondary)',
                      fontSize: '16px'
                    }}>
                      No history changes found.
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  });

  const renderContent = () => {
    // Render Commission Date Details Page if active
    if (showCommissionDateDetailsPage && selectedCommissionDate) {
      return (
        <CommissionDateDetailsPage
          commissionDate={selectedCommissionDate}
          onClose={handleCloseCommissionDateDetails}
        />
      );
    }

    // Render Jackpot Details Page if active
    if (showJackpotDetailsPage && selectedJackpot) {
      return (
        <JackpotDetailsPage
          jackpot={selectedJackpot}
          onClose={handleCloseJackpotDetails}
        />
      );
    }

    // Render Metrology Details Page if active
    if (showMetrologyDetailsPage && selectedMetrology) {
      return (
        <MetrologyDetailsPage
          metrology={selectedMetrology}
          onClose={handleCloseMetrologyDetails}
        />
      );
    }

    // Render Invoice Details Page if active
            if (showLocationDetailsPage && selectedLocation) {
          return (
            <LocationDetailsPage
              location={selectedLocation}
              onClose={handleCloseLocationDetails}
            />
          );
        }

        if (showInvoiceDetailsPage && selectedInvoice) {
          return (
            <InvoiceDetailsPage
              invoice={selectedInvoice}
              onClose={handleCloseInvoiceDetails}
            />
          );
        }

        // Render History Changes Page if active
        if (showHistoryChangesPage) {
          return (
            <HistoryChangesPage
              onClose={handleCloseHistoryChanges}
            />
          );
        }

    // Define slotColumns at the beginning to be accessible in both 'slots' and 'warehouse' cases
    const slotColumns = [
            {
              key: 'serial_number',
              label: 'Serial Number',
              render: (item) => {
                const location = locations.find(l => l.id === item.location_id);
                return (
                  <div className="serial-cell" style={{ maxWidth: '120px' }}>
                    <div 
                      className={`serial-primary clickable-filter ${selectedSerialFilter === item.serial_number ? 'active-filter' : ''}`}
                      onClick={() => toggleSerialFilter(item.serial_number)}
                      style={{ cursor: 'pointer', fontSize: '0.9em' }}
                    >
                      <strong>{item.serial_number || 'N/A'}</strong>
                    </div>
                    <div className="serial-secondary">
                      <small 
                        className="location-info clickable-filter"
                        onClick={() => handleShowLocationDetails(location)}
                        style={{ fontSize: '0.8em', cursor: 'pointer' }}
                      >
                        {location ? location.name : 'N/A'}
                      </small>
                    </div>
                  </div>
                );
              }
            },
            { key: 'provider_id', label: 'Provider', render: (item) => {
                const provider = providers.find(p => p.id === item.provider_id);
                const cabinet = cabinets.find(c => c.id === item.cabinet_id);
                return (
                  <div>
                    <div 
                      className={`clickable-filter ${selectedProviderFilter === item.provider_id ? 'active-filter' : ''}`}
                      onClick={() => toggleProviderFilter(item.provider_id)}
                      style={{ cursor: 'pointer', fontWeight: 'bold' }}
                    >
                      {provider ? provider.name : 'N/A'}
                    </div>
                    <div
                      className={`clickable-filter ${selectedCabinetFilter === item.cabinet_id ? 'active-filter' : ''}`}
                      onClick={() => toggleCabinetFilter(item.cabinet_id)}
                      style={{ fontSize: 12, cursor: 'pointer' }}
                    >
                      {cabinet ? cabinet.name : 'No Cabinet'}
                    </div>
                  </div>
                );
        }
      },
            {
              key: 'game_mix_id',
              label: 'Game Mix',
              render: (item) => {
                const gameMix = gameMixes.find(gm => gm.id === item.game_mix_id);
                const cabinet = cabinets.find(c => c.id === item.cabinet_id);
                return (
                  <div>
                    <div 
                      className={`clickable-filter ${selectedGameMixFilter === item.game_mix_id ? 'active-filter' : ''}`}
                      onClick={() => toggleGameMixFilter(item.game_mix_id)}
                      style={{ cursor: 'pointer', fontWeight: 'bold' }}
                    >
                      {gameMix ? gameMix.name : 'N/A'}
                    </div>
                    <div 
                      className={`clickable-filter ${selectedCabinetFilter === item.cabinet_id ? 'active-filter' : ''}`}
                      onClick={() => toggleCabinetFilter(item.cabinet_id)}
                      style={{ fontSize: 12, cursor: 'pointer' }}
                    >
                      {cabinet && cabinet.model ? cabinet.model : 'No Model'}
                    </div>
                  </div>
                );
              }
            },
          { 
            key: 'property_details', 
            label: 'Property',
            render: (item) => {
          // 1. Dacă ownership_type este 'rent', afișează providerul de închiriere și contractul
          if (item.ownership_type === 'rent') {
            const rentProvider = providers.find(p => p.id === item.lease_provider_id);
            const contractNumber = item.lease_contract_number || (item.serial_number ? `RENT-${item.serial_number}-${new Date().getFullYear()}` : 'No Contract');
            return (
              <div className="property-cell">
                <div 
                  className={`property-primary clickable-filter ${selectedProviderFilter === item.lease_provider_id ? 'active-filter' : ''}`}
                  onClick={() => toggleProviderFilter(item.lease_provider_id)}
                  style={{ cursor: 'pointer' }}
                >
                  <strong>{rentProvider ? rentProvider.company_name : 'No Provider Selected'}</strong>
                </div>
                <div className="property-secondary">
                                      <small 
                      className={`clickable-filter ${selectedContractFilter === contractNumber ? 'active-filter' : ''}`}
                      onClick={() => toggleContractFilter(contractNumber)}
                      title={`Click to filter by contract: ${contractNumber}`}
                    >
                      {contractNumber}
                    </small>
                  {item.production_year && (
                    <small style={{ display: 'block', marginTop: '2px', color: 'var(--accent-color)', fontWeight: 'bold' }}>
                      {item.production_year}
                    </small>
                  )}
                  {/* Afișează facturile asociate */}
                  {(() => {
                    const associatedInvoices = invoices.filter(inv => 
                      inv.serial_numbers && inv.serial_numbers.includes(item.serial_number)
                    );
                    if (associatedInvoices.length > 0) {
                      return (
                        <div style={{ marginTop: '4px' }}>
                          {associatedInvoices.map((invoice, index) => (
                            <small 
                              key={invoice.id}
                              className={`clickable-filter ${selectedInvoiceFilter === invoice.invoice_number ? 'active-filter' : ''}`}
                              onClick={() => toggleInvoiceFilter(invoice.invoice_number)}
                              style={{ 
                                display: 'block', 
                                marginTop: '2px', 
                                color: 'var(--text-secondary)',
                                cursor: 'pointer',
                                fontSize: '0.8em'
                              }}
                              title={`Click to filter by invoice: ${invoice.invoice_number}`}
                            >
                              {invoice.invoice_number}
                            </small>
                          ))}
                        </div>
                      );
                    }
                    return null;
                  })()}

                </div>
              </div>
            );
          }
          // 2. Dacă ownership_type este 'property', afișează compania proprietar
              if (item.ownership_type === 'property') {
                const company = companies.find(c => c.id === item.owner_company_id);
                return (
                  <div className="property-cell">
                    <div 
                      className={`property-primary clickable-filter ${selectedCompanyFilter === item.owner_company_id ? 'active-filter' : ''}`}
                      onClick={() => toggleCompanyFilter(item.owner_company_id)}
                      style={{ cursor: 'pointer' }}
                    >
                  <strong>{company ? company.name : 'No Company Selected'}</strong>
                    </div>
                    <div className="property-secondary">
                  <small>Property Owned</small>
                  {item.production_year && (
                    <small style={{ display: 'block', marginTop: '2px', color: 'var(--accent-color)', fontWeight: 'bold' }}>
                      {item.production_year}
                    </small>
                  )}
                  {/* Afișează facturile asociate */}
                  {(() => {
                    const associatedInvoices = invoices.filter(inv => 
                      inv.serial_numbers && inv.serial_numbers.includes(item.serial_number)
                    );
                    if (associatedInvoices.length > 0) {
                      return (
                        <div style={{ marginTop: '4px' }}>
                          {associatedInvoices.map((invoice, index) => (
                            <small 
                              key={invoice.id}
                              className={`clickable-filter ${selectedInvoiceFilter === invoice.invoice_number ? 'active-filter' : ''}`}
                              onClick={() => toggleInvoiceFilter(invoice.invoice_number)}
                              style={{ 
                                display: 'block', 
                                marginTop: '2px', 
                                color: 'var(--text-secondary)',
                                cursor: 'pointer',
                                fontSize: '0.8em'
                              }}
                              title={`Click to filter by invoice: ${invoice.invoice_number}`}
                            >
                              {invoice.invoice_number}
                            </small>
                          ))}
                        </div>
                      );
                    }
                    return null;
                  })()}
                    </div>
                  </div>
                );
          }
          // 3. Dacă nu există ownership_type, caută factura și afișează buyer/seller
          const invoice = invoices.find(inv => 
            inv.serial_numbers && inv.serial_numbers.includes(item.serial_number)
          );
          if (invoice) {
            const buyer = companies.find(c => c.id === invoice.buyer_id);
            const seller = companies.find(c => c.id === invoice.seller_id);
                return (
                  <div className="property-cell">
                    <div 
                  className={`property-primary clickable-filter ${selectedCompanyFilter === invoice.buyer_id ? 'active-filter' : ''}`}
                  onClick={() => toggleCompanyFilter(invoice.buyer_id)}
                      style={{ cursor: 'pointer' }}
                    >
                  <strong>{buyer ? buyer.name : 'Unknown Customer'}</strong>
                    </div>
                    <div className="property-secondary">
                      <small 
                    className={`clickable-filter ${selectedInvoiceFilter === invoice.invoice_number ? 'active-filter' : ''}`}
                    onClick={() => toggleInvoiceFilter(invoice.invoice_number)}
                    title={`Click to filter by invoice: ${invoice.invoice_number}`}
                  >
                    {invoice.invoice_number}
                      </small>
                  {seller && (
                    <small style={{ marginLeft: '8px', color: 'var(--text-secondary)' }}>
                      → {seller.name}
                    </small>
                  )}
                  {item.production_year && (
                    <small style={{ display: 'block', marginTop: '2px', color: 'var(--accent-color)', fontWeight: 'bold' }}>
                      {item.production_year}
                    </small>
                  )}
                    </div>
                  </div>
                );
              }
          // 4. Dacă nu există nimic, fallback la Unknown
              return (
                <div className="property-cell">
              <div className="property-primary"><strong>No Owner Info</strong></div>
              <div className="property-secondary">
                <small>Serial: {item.serial_number || 'N/A'}</small>
                {item.production_year && (
                  <small style={{ display: 'block', marginTop: '2px', color: 'var(--accent-color)', fontWeight: 'bold' }}>
                    {item.production_year}
                  </small>
                )}
                {/* Afișează facturile asociate */}
                {(() => {
                  const associatedInvoices = invoices.filter(inv => 
                    inv.serial_numbers && inv.serial_numbers.includes(item.serial_number)
                  );
                  if (associatedInvoices.length > 0) {
                    return (
                      <div style={{ marginTop: '4px' }}>
                        {associatedInvoices.map((invoice, index) => (
                          <small 
                            key={invoice.id}
                            className={`clickable-filter ${selectedInvoiceFilter === invoice.invoice_number ? 'active-filter' : ''}`}
                            onClick={() => toggleInvoiceFilter(invoice.invoice_number)}
                            style={{ 
                              display: 'block', 
                              marginTop: '2px', 
                              color: 'var(--text-secondary)',
                              cursor: 'pointer',
                              fontSize: '0.8em'
                            }}
                            title={`Click to filter by invoice: ${invoice.invoice_number}`}
                          >
                            {invoice.invoice_number}
                          </small>
                        ))}
                      </div>
                    );
                  }
                  return null;
                })()}
              </div>
                </div>
              );
            }
          },

          { 
            key: 'technical_specs', 
            label: 'Technical Specs',
            render: (item) => {
              const formatAmount = (amount) => {
                if (!amount) return '0,00';
                const num = parseFloat(amount);
                if (isNaN(num)) return '0,00';
                const formatted = num.toFixed(2);
                const parts = formatted.split('.');
                const integerPart = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.');
                return `${integerPart},${parts[1]}`;
              };
              
              return (
                <div className="tech-specs-cell">
                  <div className="spec-row">
                    <span className="spec-label">Denom:</span>
                    <span className="spec-value">{item.denomination ? formatAmount(item.denomination) : 'N/A'}</span>
                  </div>
                  <div className="spec-row">
                    <span className="spec-label">Max Bet:</span>
                    <span className="spec-value">{item.max_bet ? formatAmount(item.max_bet) : 'N/A'}</span>
                  </div>
                  <div className="spec-row">
                    <span className="spec-label">RTP:</span>
                    <span 
                      className={`spec-value clickable-filter ${selectedRTPFilter === item.rtp ? 'active-filter' : ''}`}
                      onClick={() => toggleRTPFilter(item.rtp)}
                      style={{ cursor: 'pointer' }}
                    >
                      {item.rtp ? `${item.rtp}%` : 'N/A'}
                    </span>
                  </div>
                  <div className="spec-row">
                    <span className="spec-label">Places:</span>
                    <span 
                      className={`spec-value clickable-filter ${selectedPlacesFilter === item.gaming_places ? 'active-filter' : ''}`}
                      onClick={() => togglePlacesFilter(item.gaming_places)}
                      style={{ cursor: 'pointer' }}
                    >
                      {item.gaming_places || 'N/A'}
                    </span>
                  </div>
                </div>
              );
            }
      },
      // Add CVT Information column to slot machines table
                {
            key: 'cvt_information',
            label: 'CVT Information',
            render: (item) => {
              // Find metrology record for this slot with proper multi-serial handling
              const metrologyItem = metrology.find(m => {
                if (!m.serial_number) {
                  return false;
                }
                
                // Try both newline and space separation
                const serialNumbersNewline = m.serial_number.split('\n').filter(s => s.trim());
                const serialNumbersSpace = m.serial_number.split(' ').filter(s => s.trim());
                
                // Use the one that has more items (more likely to be correct)
                const serialNumbers = serialNumbersNewline.length > serialNumbersSpace.length ? 
                  serialNumbersNewline : serialNumbersSpace;
                
                return serialNumbers.includes(item.serial_number);
              });
              
              const cvtDate = metrologyItem?.cvt_expiry_date;
              const cvtType = metrologyItem?.cvt_type;
              
              if (!cvtDate && !cvtType) {
                return <span style={{ color: '#6b7280', fontStyle: 'italic' }}>No CVT Data</span>;
              }
              
              // Calculate days remaining
          let daysLeft = null;
          if (cvtDate) {
            const cvtExpiryDate = new Date(cvtDate);
            const now = new Date();
            const diff = Math.floor((cvtExpiryDate - now) / (1000 * 60 * 60 * 24));
            daysLeft = diff > 0 ? diff : 0;
          }
          
          // Color coding for days remaining
          let daysColor = '#10b981'; // Green for > 90 days
          if (daysLeft !== null) {
            if (daysLeft <= 30) {
              daysColor = '#ef4444'; // Red for ≤ 30 days
            } else if (daysLeft <= 90) {
              daysColor = '#f59e0b'; // Yellow for 31-90 days
            }
          }
          
          // Type colors
          const typeColors = {
            'periodic': { bg: '#dbeafe', text: '#1e40af', icon: '' },
            'reparation': { bg: '#fef3c7', text: '#d97706', icon: '' }
          };
          
          const colorScheme = typeColors[cvtType] || { bg: '#f3f4f6', text: '#6b7280', icon: '❓' };
          
          return (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {/* Row 1: CVT Type (Clickable) */}
              {cvtType && (
                <div 
                  onClick={() => handleMetrologyClick([metrologyItem])}
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '4px',
                    padding: '4px 8px',
                    borderRadius: '12px',
                    backgroundColor: colorScheme.bg,
                    color: colorScheme.text,
                    fontSize: '0.85em',
                    fontWeight: '500',
                    width: 'fit-content',
                    cursor: 'pointer',
                    transition: 'all 0.2s'
                  }}
                  onMouseEnter={(e) => {
                    e.target.style.opacity = '0.8';
                    e.target.style.transform = 'scale(1.05)';
                  }}
                  onMouseLeave={(e) => {
                    e.target.style.opacity = '1';
                    e.target.style.transform = 'scale(1)';
                  }}
                  title="Click to view all metrology details"
                >
                  <span style={{ textTransform: 'capitalize' }}>{cvtType}</span>
                </div>
              )}
              
              {/* Row 2: CVT Expiry Date */}
              {cvtDate && (
                <div 
                  className={`clickable-filter ${selectedCvtDateFilter === cvtDate ? 'active-filter' : ''}`}
                  onClick={() => toggleCvtDateFilter(cvtDate)}
                  style={{ 
                    fontSize: '0.9em', 
                    fontWeight: '500',
                    cursor: 'pointer',
                    padding: '2px 4px',
                    borderRadius: '4px',
                    transition: 'background-color 0.2s'
                  }}
                >
                  {formatDateDDMMYYYY(cvtDate)}
                </div>
              )}
              
              {/* Row 3: Days Left */}
              {daysLeft !== null && (
                <div style={{
                  textAlign: 'center', 
                  color: daysColor,
                  fontWeight: 'bold',
                  fontSize: '1.1em',
                  padding: '4px 8px',
                  borderRadius: '4px',
                  backgroundColor: daysColor === '#ef4444' ? 'rgba(239, 68, 68, 0.1)' : 
                                          daysColor === '#f59e0b' ? 'rgba(245, 158, 11, 0.1)' : 
                                          'rgba(16, 185, 129, 0.1)',
                  width: 'fit-content'
                }}>
                  {daysLeft} days left
                </div>
              )}
              

            </div>
          );
        }
      },


      {
        key: 'comision_date',
        label: 'Comision Date',
        render: (item) => {
          // Caută toate comision dates care conțin serialul slotului
          const associatedComisionDates = comisionDates.filter(cd => {
            if (!cd.serial_numbers) return false;
            // Verifică dacă serial_number-ul slotului este conținut în serial_numbers-ul comision date
            const comisionSerialNumbers = cd.serial_numbers.split(/\s+/).filter(s => s.trim());
            return comisionSerialNumbers.includes(item.serial_number);
          });
          
          if (associatedComisionDates.length === 0) {
            return <span style={{ color: '#aaa', fontStyle: 'italic' }}>No Comision Date</span>;
          }
          
          // Dacă este o singură comision date, afișează data
          if (associatedComisionDates.length === 1) {
            const comisionDate = associatedComisionDates[0];
            return (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                <span style={{ 
                  color: '#059669', 
                  cursor: 'pointer',
                  textDecoration: 'underline',
                  fontWeight: '500'
                }} onClick={() => {
                  // Aici poți adăuga logica pentru a deschide un popup cu detalii
                  showCustomNotification(`Commission Date: ${formatDateDDMMYYYY(comisionDate.commission_date)}`, 'info');
                }}>
                  {formatDateDDMMYYYY(comisionDate.commission_date)}
                </span>
              </div>
            );
          }
          
          // Dacă sunt multiple comision dates, afișează "Multiple Comision Dates" clicabil cu bulină
          return (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0px' }}>
              <span style={{ 
                color: '#059669', 
                cursor: 'pointer',
                textDecoration: 'underline',
                fontWeight: '500'
              }} onClick={() => {
                // Aici poți adăuga logica pentru a deschide un popup cu toate comision dates
                const dates = associatedComisionDates.map(cd => 
                  formatDateDDMMYYYY(cd.commission_date)
                ).join(', ');
                showCustomNotification(`Commission Dates: ${dates}`, 'info');
              }}>
                Multiple Comision Dates
              </span>
              <div style={{
                backgroundColor: '#059669',
                color: 'white',
                borderRadius: '50%',
                width: '18px',
                height: '18px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '11px',
                fontWeight: 'bold',
                minWidth: '18px',
                marginLeft: '0px'
              }}>
                {associatedComisionDates.length}
              </div>
            </div>
          );
        }
      },
      {
        key: 'created_by',
        label: 'Created By',
        render: (item) => {
          const creator = users.find(u => u.id === item.created_by || u.username === item.created_by);
          return (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <span style={{ 
                fontSize: '0.9em', 
                color: 'var(--text-primary)',
                fontWeight: '500'
              }}>
                {creator && creator.first_name && creator.last_name ? `${creator.first_name} ${creator.last_name}` : creator ? creator.username : item.created_by || 'Unknown'}
              </span>
              <span style={{ 
                fontSize: '0.8em', 
                color: 'var(--text-secondary)',
                fontStyle: 'italic'
              }}>
                {item.created_at ? formatDateDDMMYYYY(item.created_at) : 'N/A'}
              </span>
            </div>
          );
        }
      },
      {
        key: 'updated_by',
        label: 'Modified By',
        render: (item) => {
          const modifier = users.find(u => u.id === item.updated_by || u.username === item.updated_by);
          return (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <span style={{ 
                fontSize: '0.9em', 
                color: 'var(--text-primary)',
                fontWeight: '500'
              }}>
                {modifier && modifier.first_name && modifier.last_name ? `${modifier.first_name} ${modifier.last_name}` : modifier ? modifier.username : item.updated_by || 'N/A'}
              </span>
              <span style={{ 
                fontSize: '0.8em', 
                color: 'var(--text-secondary)',
                fontStyle: 'italic'
              }}>
                {item.updated_at ? formatDateDDMMYYYY(item.updated_at) : 'N/A'}
              </span>
            </div>
          );
        }
      },

    ];
    switch (activeView) {
      case 'dashboard':
        return renderDashboard();
      case 'companies':
        return renderTable('Companies', companies, [
          { 
            key: 'avatar', 
            label: 'Logo',
            render: (item) => (
                              <AvatarDisplay entityType="companies" entityId={item.id} size={50} entityName={item.name} />
            )
          },
          { key: 'name', label: 'Company Name' },
          { key: 'registration_number', label: 'Registration' },
          { key: 'contact_person', label: 'Contact Person' },
          { 
            key: 'email', 
            label: 'Email',
            render: (item) => (
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span>{item.email || 'N/A'}</span>
              </div>
            )
          },
          { 
            key: 'phone', 
            label: 'Phone',
            render: (item) => (
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span>{item.phone || 'N/A'}</span>
              </div>
            )
          }
        ], { 
          onAdd: () => handleAddEntity('companies'),
          onEdit: (item) => handleEditEntity(item, 'companies'),
          onDelete: (id) => handleDeleteEntity(id, 'companies'),
          onBulkEdit: () => handleBulkEdit('companies'),
          onBulkDelete: () => handleBulkDelete('companies'),
          onExport: () => handleExport('companies'),
          onImport: () => handleImport('companies')
        }, 'companies');
      case 'locations':
        return renderTable('Locations', locations, [
          { 
            key: 'avatar', 
            label: 'Avatar',
            render: (item) => (
                              <AvatarDisplay entityType="locations" entityId={item.id} size={50} entityName={item.name} />
            )
          },
          { key: 'name', label: 'Location Name' },
          { key: 'address', label: 'Address' },
          { key: 'city', label: 'City' },
          { key: 'county', label: 'County' },
          { 
            key: 'coordinates', 
            label: 'Coordinates',
            render: (item) => item.latitude && item.longitude ? 
              `${item.latitude.toFixed(4)}, ${item.longitude.toFixed(4)}` : 'N/A'
          },
          { 
            key: 'contact_person', 
            label: 'Contact Person',
            render: (item) => {
              // Dacă contact_person_id există, caută user-ul
              if (item.contact_person_id) {
                const contactUser = Array.isArray(users) ? users.find(u => u.id === item.contact_person_id) : null;
                if (contactUser) {
              return (
                <div>
                      <div style={{ fontWeight: 'bold' }}>
                        {contactUser.first_name && contactUser.last_name ? 
                          `${contactUser.first_name} ${contactUser.last_name}` : 
                          contactUser.username}
                      </div>
                      <div style={{ fontSize: '0.8em', color: 'var(--text-secondary)' }}>
                        {contactUser.email || 'N/A'} | {contactUser.phone || 'N/A'}
                  </div>
                </div>
              );
            }
              }
              // Dacă nu există contact_person_id, afișează contact_person ca text
              return item.contact_person ? (
                <div>
                  <div style={{ fontWeight: 'bold' }}>
                    {item.contact_person}
                  </div>
                  <div style={{ fontSize: '0.8em', color: 'var(--text-secondary)' }}>
                    {item.contact_email || 'N/A'} | {item.contact_phone || 'N/A'}
                  </div>
                </div>
              ) : 'No contact person';
            }
          }
        ], { 
          onAdd: () => handleAddEntity('locations'),
          onEdit: (item) => handleEditEntity(item, 'locations'),
          onDelete: (id) => handleDeleteEntity(id, 'locations'),
          onBulkEdit: () => handleBulkEdit('locations'),
          onBulkDelete: () => handleBulkDelete('locations'),
          onExport: () => handleExport('locations'),
          onImport: () => handleImport('locations')
        }, 'locations');
      case 'providers':
        return renderTable('Providers', providers, [
          {
            key: 'avatar',
            label: 'Avatar',
            render: (item) => (
              <div className="provider-avatar-cell" style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <AvatarDisplay entityType="providers" entityId={item.id} size={50} entityName={item.name || 'Unknown Provider'} />
              </div>
            )
          },
          { key: 'name', label: 'Provider Name' },
          { key: 'company_name', label: 'Company' },
          { 
            key: 'property', 
            label: 'Property',
            render: (item) => {
              // Property column: pentru Property type afișează "Company Name + Invoice Number"
              // pentru Rent type afișează "Provider Company Name + Lease Contract Number"
              if (item.property_type === 'property') {
                return `${item.company_name || 'N/A'} + ${item.invoice_number || 'N/A'}`;
              } else if (item.property_type === 'rent') {
                return `${item.name || 'N/A'} + ${item.lease_contract_number || 'N/A'}`;
              } else {
                return 'N/A';
              }
            }
          },
          { key: 'contact_person', label: 'Contact Person' },
          { 
            key: 'email', 
            label: 'Email',
            render: (item) => (
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ fontSize: '16px' }}>📧</span>
                <span>{item.email || 'N/A'}</span>
              </div>
            )
          },
          {
            key: 'website',
            label: 'Website',
            render: (item) => item.website ?
              <a href={item.website} target="_blank" rel="noopener noreferrer" className="link">
                {item.website}
              </a> : 'N/A'
          }
        ], {
          onAdd: () => handleAddEntity('providers'),
          onEdit: (item) => handleEditEntity(item, 'providers'),
          onDelete: (id) => handleDeleteEntity(id, 'providers')
        });
      case 'cabinets':
        return renderTable('Cabinets', cabinets, [
                      { key: 'logo', label: 'Logo', render: (item) => <AvatarDisplay entityType="cabinets" entityId={item.id} size={50} entityName={item.name} /> },
          { key: 'name', label: 'Name' },
          { key: 'model', label: 'Model' },
          { key: 'provider_id', label: 'Provider', render: (item) => {
              const provider = providers.find(p => p.id === item.provider_id);
              return provider ? provider.name : 'N/A';
          } },
        ], {
          onAdd: () => handleAddEntity('cabinets'),
          onEdit: (item) => handleEditEntity(item, 'cabinets'),
          onDelete: (id) => handleDeleteEntity(id, 'cabinets'),
          onBulkEdit: () => handleBulkEdit('cabinets'),
          onBulkDelete: () => handleBulkDelete('cabinets'),
          onExport: () => handleExport('cabinets'),
          onImport: () => handleImport('cabinets')
        }, 'cabinets');
      case 'slots': {
        // Show only active slots (including those without status set)
        const activeSlots = slotMachines.filter(s => s.status !== 'inactive');
        const activeCount = activeSlots.length;
        return renderTable(`Slot Machines`, activeSlots, slotColumns, {
          onAdd: () => handleAddEntity('slots'),
          onEdit: (item) => handleEditEntity(item, 'slots'),
          onDelete: (id) => handleDeleteEntity(id, 'slots'),
          onBulkEdit: () => handleBulkEdit('slots'),
          onBulkDelete: () => handleBulkDelete('slots'),
          onBulkDuplicate: () => handleBulkDuplicate('slots'),
          onExport: () => handleExport('slots'),
          onImport: () => handleImport('slots')
        }, 'slots');
      }
      case 'warehouse': {
        // Show only inactive slots
        const warehouseSlots = slotMachines.filter(s => s.status === 'inactive');
        const warehouseCount = warehouseSlots.length;
        return renderTable(`Warehouse`, warehouseSlots, slotColumns, {
          onAdd: () => handleAddEntity('slots'),
          onEdit: (item) => handleEditEntity(item, 'slots'),
          onDelete: (id) => handleDeleteEntity(id, 'slots'),
          onBulkEdit: () => handleBulkEdit('slots'),
          onBulkDelete: () => handleBulkDelete('slots'),
          onBulkDuplicate: () => handleBulkDuplicate('slots'),
          onExport: () => handleExport('slots'),
          onImport: () => handleImport('slots')
        }, 'slots');
      }
      case 'metrology': {
        // REDIRECT TO METROLOGY CVT - THE ONLY CORRECT METROLOGY TABLE
        return (
          <div style={{ padding: '40px', textAlign: 'center', color: '#666' }}>
            <h3>⚠️ Metrology Table Deprecated</h3>
            <p>This table has been replaced by Metrology CVT. Please use the Metrology CVT section instead.</p>
            <button 
              className="btn-primary"
              onClick={() => setActiveView('metrology2')}
              style={{ marginTop: '20px' }}
            >
              Go to Metrology CVT
            </button>
          </div>
        );
      }
      case 'metrology2': {
        const selectedMetrologyItems = selectedItems.filter(id => metrology.some(item => (item.id || item._id) === id));
        const hasSelectedItems = selectedMetrologyItems.length > 0;
        
        const filteredMetrology = filterData(metrology, metrologySearchTerm);
        
        return (
          <div className="table-container">
            <div className="table-header">
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <h2>Metrology CVT</h2>
                <div style={{
                  backgroundColor: '#3182ce',
                  color: 'white',
                  borderRadius: '50%',
                  width: '28px',
                  height: '28px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '14px',
                  fontWeight: 'bold',
                  minWidth: '28px'
                }}>
                  {filteredMetrology.length}
                </div>
              </div>
              <div className="table-actions">
                {/* Search input */}
                <input
                  type="text"
                  value={metrologySearchTerm}
                  onChange={e => setMetrologySearchTerm(e.target.value)}
                  placeholder="Search..."
                  style={{
                    padding: '6px 12px',
                    borderRadius: '6px',
                    border: '1px solid var(--border-color)',
                    fontSize: '1em',
                    minWidth: 180,
                    marginRight: 8
                  }}
                />
                {hasSelectedItems && (
                  <div style={{ 
                    display: 'flex', 
                    gap: '8px', 
                    alignItems: 'center',
                    background: 'var(--bg-primary)',
                    padding: '8px 12px',
                    borderRadius: '6px',
                    border: '1px solid var(--border-color)',
                    marginRight: '12px'
                  }}>
                    <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                      {selectedMetrologyItems.length} selected
                    </span>
                    <button 
                      className="btn-secondary"
                      onClick={() => handleBulkEdit('metrology2')}
                      style={{ fontSize: '0.85rem', padding: '4px 8px' }}
                    >
                      ✏️ Bulk Edit
                    </button>
                    <button 
                      className="btn-danger"
                      onClick={() => handleBulkDelete('metrology2')}
                      style={{ fontSize: '0.85rem', padding: '4px 8px' }}
                    >
                      🗑️ Bulk Delete
                    </button>
                  </div>
                )}
                <button 
                  className="btn-primary"
                  onClick={() => handleAddEntity('metrology2')}
                >
                  <span className="icon">➕</span>
                  Add CVT Date
                </button>
                <button 
                  className="btn-success"
                  onClick={() => handleExport('metrology2')}
                  title="Export Data"
                >
                  <span className="icon">📤</span>
                  Export
                </button>
                <button 
                  className="btn-info"
                  onClick={() => handleImport('metrology2')}
                  title="Import Data"
                >
                  <span className="icon">📥</span>
                  Import
                </button>
              </div>
            </div>
            
            <div className="table-wrapper">
              <table className="data-table">
                <thead>
                  <tr>
                    <th style={{ width: '40px' }}>
                      <input
                        type="checkbox"
                        checked={metrology.length > 0 && selectedMetrologyItems.length === metrology.length}
                        onChange={(e) => handleSelectAll(metrology, e.target.checked)}
                        style={{ cursor: 'pointer' }}
                      />
                    </th>
                    <th>#</th>
                    <th>Certificate Number</th>
                    <th>Issue Date</th>
                    <th>Authority</th>
                    <th>CVT Type</th>
                    <th>CVT End Date</th>
                    <th>Number of Slots</th>
                    <th>Created At</th>
                    <th>Created By</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredMetrology.map((item, index) => {
                    const createdByUser = Array.isArray(users) ? users.find(user => user.id === item.created_by || user.username === item.created_by) : null;
                    const daysUntilExpiry = item.cvt_expiry_date ? 
                      Math.ceil((new Date(item.cvt_expiry_date) - new Date()) / (1000 * 60 * 60 * 24)) : null;
                    const isSelected = selectedItems.includes(item.id || item._id);
                    
                    return (
                      <tr 
                        key={item.id || item._id}
                        style={{ 
                          backgroundColor: isSelected ? 'var(--accent-color)' : 'transparent',
                          opacity: isSelected ? 0.9 : 1
                        }}
                      >
                        <td>
                          <input
                            type="checkbox"
                            checked={isSelected}
                            onChange={(e) => handleItemSelection(item.id || item._id, e.target.checked)}
                            style={{ cursor: 'pointer' }}
                          />
                        </td>
                        <td>{index + 1}</td>
                        <td>
                          <strong 
                            onClick={() => handleShowMetrologyDetails(item)}
                            style={{
                              cursor: 'pointer',
                              color: '#3182ce',
                              textDecoration: 'underline',
                              transition: 'all 0.2s'
                            }}
                            onMouseEnter={(e) => {
                              e.target.style.color = '#2c5282';
                              e.target.style.textDecoration = 'none';
                            }}
                            onMouseLeave={(e) => {
                              e.target.style.color = '#3182ce';
                              e.target.style.textDecoration = 'underline';
                            }}
                            title="Click to view all metrology details"
                          >
                            {item.certificate_number || 'N/A'}
                          </strong>
                        </td>

                        <td>{item.issue_date ? formatDateDDMMYYYY(item.issue_date) : 'N/A'}</td>
                        <td>
                          <span style={{ 
                            fontWeight: '500',
                            color: 'var(--text-primary)'
                          }}>
                            {item.issuing_authority || 'N/A'}
                          </span>
                        </td>
                        <td>
                          <span style={{ 
                            display: 'flex', 
                            alignItems: 'center', 
                            gap: '4px',
                            color: item.cvt_type === 'periodic' ? '#3182ce' : '#dc3545'
                          }}>
                            {item.cvt_type || 'N/A'}
                          </span>
                        </td>
                        <td>
                          {item.cvt_expiry_date ? (
                            <div>
                              <div style={{ fontWeight: 'bold' }}>
                                {formatDateDDMMYYYY(item.cvt_expiry_date)}
                              </div>
                              {(() => {
                                const daysUntilExpiry = Math.ceil((new Date(item.cvt_expiry_date) - new Date()) / (1000 * 60 * 60 * 24));
                                return (
                                  <div style={{ 
                                    fontSize: '0.9em',
                                    color: daysUntilExpiry <= 30 ? '#dc3545' : daysUntilExpiry <= 90 ? '#ffc107' : '#28a745',
                                    fontWeight: 'bold'
                                  }}>
                                    {daysUntilExpiry > 0 ? `${daysUntilExpiry} days left` : `${Math.abs(daysUntilExpiry)} days overdue`}
                                  </div>
                                );
                              })()}
                            </div>
                          ) : 'N/A'}
                        </td>

                        <td>
                          <span style={{ 
                            backgroundColor: 'var(--accent-color)', 
                            color: 'white',
                            padding: '4px 8px',
                            borderRadius: '12px',
                            fontSize: '0.9em',
                            fontWeight: 'bold'
                          }}>
                            {item.serial_number ? item.serial_number.split('\n').filter(s => s.trim()).length : 0} slots
                          </span>
                        </td>
                        <td>{item.created_at ? formatDateDDMMYYYY(item.created_at) : 'N/A'}</td>
                        <td>
                          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                            <span style={{ 
                              fontSize: '0.9em', 
                              color: 'var(--text-primary)',
                              fontWeight: '500'
                            }}>
                              {item.creator_name || 'Unknown User'}
                            </span>
                            <span style={{ 
                              fontSize: '0.8em', 
                              color: 'var(--text-secondary)',
                              fontStyle: 'italic'
                            }}>
                              {item.updater_name ? `Modified by: ${item.updater_name}` : ''}
                            </span>
                          </div>
                        </td>
                        <td>
                          <div className="action-buttons">
                            <CvtAttachmentIndicator cvtId={item.id || item._id} onClick={() => handleOpenCvtAttachments(item.id || item._id)} />
                            <button 
                              className="btn-edit"
                              onClick={() => handleEditEntity(item, 'metrology2')}
                              title="Edit CVT Date"
                            >
                              ✏️
                            </button>
                            <button 
                              className="btn-delete"
                              onClick={() => handleDeleteEntity(item.id || item._id, 'metrology2')}
                              title="Delete CVT Date"
                            >
                              🗑️
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
              
              {filteredMetrology.length === 0 && (
                <div style={{ padding: '40px', textAlign: 'center', color: '#666' }}>
                  <h3>No CVT Records Found</h3>
                  <p>Use the "Add CVT Date" button to create your first CVT record.</p>
                </div>
              )}
            </div>
          </div>
        );
      }
              case 'jackpots': {
          return renderTable('Jackpot Records', jackpots, [
            { key: 'slot_count', label: 'NUMBER OF SLOTS', render: (item) => {
              if (!item.serial_number) return (
                <span style={{ 
                  backgroundColor: 'var(--accent-color)', 
                  color: 'white',
                  padding: '4px 8px',
                  borderRadius: '12px',
                  fontSize: '0.9em',
                  fontWeight: 'bold'
                }}>
                  0 slots
                </span>
              );
              
              // Split serial numbers by space and newline, then filter empty strings
              const serialNumbers = item.serial_number.split(/\s|\n/).filter(s => s.trim());
              
              // Count how many slots match these serial numbers
              const matchingSlots = slotMachines.filter(slot => 
                serialNumbers.includes(slot.serial_number)
              );
              
              const slotCount = matchingSlots.length;
              
              return (
                <span style={{ 
                  backgroundColor: slotCount > 0 ? 'var(--accent-color)' : '#ff6b6b', 
                  color: 'white',
                  padding: '4px 8px',
                  borderRadius: '12px',
                  fontSize: '0.9em',
                  fontWeight: 'bold'
                }}>
                  {slotCount} slot{slotCount !== 1 ? 's' : ''}
                </span>
              );
            }},
            { key: 'jackpot_name', label: 'Jackpot Name', render: (item) => (
              <span 
                style={{ 
                  color: '#3182ce', 
                  cursor: 'pointer', 
                  textDecoration: 'underline',
                  fontWeight: '500'
                }} 
                onClick={() => handleShowJackpotDetails(item)}
              >
                {item.jackpot_name || 'No Name'}
              </span>
            )},
            { key: 'jackpot_type', label: 'Type', render: (item) => {
              const typeColors = {
                'Progressive': '📈',
                'Fixed': '💰',
                'Mystery': '🎭'
              };
              return (
                <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                  {typeColors[item.jackpot_type] || '🎰'} {item.jackpot_type}
                </span>
              );
            }},

            { key: 'increment_rate', label: 'Increment Rate', render: (item) => (
              <span style={{ 
                color: 'var(--accent-color)', 
                fontWeight: 'bold'
              }}>
                {item.increment_rate ? `${(item.increment_rate * 100).toFixed(1)}%` : 'N/A'}
              </span>
            )},
            { key: 'description', label: 'Description', render: (item) => item.description || 'N/A' },
            { key: 'created_by', label: 'Created By', render: (item) => {
              const creator = users.find(u => u.id === item.created_by || u.username === item.created_by);
              return (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                  <span style={{ 
                    fontSize: '0.9em', 
                    color: 'var(--text-primary)',
                    fontWeight: '500'
                  }}>
                    {creator && creator.first_name && creator.last_name ? `${creator.first_name} ${creator.last_name}` : creator ? creator.username : item.created_by || 'Unknown'}
                  </span>
                  <span style={{ 
                    fontSize: '0.8em', 
                    color: 'var(--text-secondary)',
                    fontStyle: 'italic'
                  }}>
                    {item.created_at ? formatDateDDMMYYYY(item.created_at) : 'N/A'}
                  </span>
                </div>
              );
            }},
            { key: 'updated_by', label: 'Modified By', render: (item) => {
              const modifier = users.find(u => u.id === item.updated_by || u.username === item.updated_by);
              return (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                  <span style={{ 
                    fontSize: '0.9em', 
                    color: 'var(--text-primary)',
                    fontWeight: '500'
                  }}>
                    {modifier && modifier.first_name && modifier.last_name ? `${modifier.first_name} ${modifier.last_name}` : modifier ? modifier.username : item.updated_by || 'N/A'}
                  </span>
                  <span style={{ 
                    fontSize: '0.8em', 
                    color: 'var(--text-secondary)',
                    fontStyle: 'italic'
                  }}>
                    {item.updated_at ? formatDateDDMMYYYY(item.updated_at) : 'N/A'}
                  </span>
                </div>
              );
            }}
          ], { 
            onAdd: () => handleAddEntity('jackpots'),
            onEdit: (item) => handleEditEntity(item, 'jackpots'),
            onDelete: (id) => handleDeleteEntity(id, 'jackpots'),
            onBulkEdit: () => handleBulkEdit('jackpots'),
            onBulkDelete: () => handleBulkDelete('jackpots'),
            onExport: () => handleExport('jackpots'),
            onImport: () => handleImport('jackpots')
          }, 'jackpots');
        }
      case 'gamemixes':
        return renderTable('Game Mixes', gameMixes, [
          {
            key: 'avatar',
            label: 'Avatar',
            render: (item) => (
              <AvatarDisplay entityType="game_mixes" entityId={item.id} size={80} rectangular={true} entityName={item.name} />
            )
          },
          { key: 'name', label: 'Mix Name' },
          { key: 'description', label: 'Description' },
          {
            key: 'provider_id',
            label: 'Provider',
            render: (item) => {
              const provider = providers.find(p => p.id === item.provider_id);
              return provider ? provider.name : 'Unknown Provider';
            }
          },
          { key: 'games', label: 'Games', render: (item) => (item.games || []).join(', ') },
          {
            key: 'campus_web',
            label: 'Campus Web',
            render: (item) => {
              if (item.campus_web && item.campus_web.startsWith('https://')) {
                return (
                  <a 
                    href={item.campus_web} 
                    target="_blank" 
                    rel="noopener noreferrer" 
                    className="link"
                    style={{ color: 'var(--accent-color)', textDecoration: 'underline' }}
                  >
                    🌐 {item.campus_web}
                  </a>
                );
              }
              return item.campus_web || 'N/A';
            }
          }
        ], {
          onAdd: () => handleAddEntity('gamemixes'),
          onEdit: (item) => handleEditEntity(item, 'gamemixes'),
          onDelete: (id) => handleDeleteEntity(id, 'gamemixes')
        });
      case 'invoices':
        return renderTable('Invoices', invoices, [
          { 
            key: 'invoice_number', 
            label: 'Invoice Number',
            render: (item) => (
              <span 
                className="clickable-invoice-number" 
                onClick={() => handleInvoiceClick(item)}
                style={{ cursor: 'pointer', color: 'var(--accent-color)', textDecoration: 'underline' }}
              >
                {item.invoice_number}
              </span>
            )
          },
          { 
            key: 'buyer_id', 
            label: 'Customer',
            render: (item) => {
              const buyer = companies.find(c => c.id === item.buyer_id);
              return (
                <div>
                  <div style={{ fontWeight: 'bold' }}>
                    {buyer ? buyer.name : 'Unknown Customer'}
                  </div>
                  <div style={{ fontSize: '0.8em', color: 'var(--text-secondary)' }}>
                    {buyer ? buyer.contact_person || 'No contact person' : 'N/A'}
                  </div>
                </div>
              );
            }
          },
          { 
            key: 'seller_id', 
            label: 'Seller',
            render: (item) => {
              const seller = providers.find(p => p.id === item.seller_id);
              return (
                <div>
                  <div style={{ fontWeight: 'bold' }}>
                    {seller ? seller.name : 'Unknown Seller'}
                  </div>
                  <div style={{ fontSize: '0.8em', color: 'var(--text-secondary)' }}>
                    {seller ? seller.contact_person || 'No contact person' : 'N/A'}
                  </div>
                </div>
              );
            }
          },
          { 
            key: 'transaction_type', 
            label: 'Transaction Type',
            render: (item) => {
              const transactionTypeColors = {
                'rent': '🔵',
                'buy': '🟢', 
                'sell': '🟡'
              };
              const transactionTypeLabels = {
                'rent': 'Rent',
                'buy': 'Buy',
                'sell': 'Sell'
              };
              return (
                <span style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '4px',
                  fontWeight: 'bold'
                }}>
                  {transactionTypeColors[item.transaction_type] || '⚪'} {transactionTypeLabels[item.transaction_type] || 'N/A'}
                </span>
              );
            }
          },
          { 
            key: 'location', 
            label: 'Location',
            render: (item) => {
              // Find location based on serial numbers in the invoice
              let location = null;
              if (item.serial_numbers) {
                const serialArray = item.serial_numbers.split(' ').filter(s => s.trim());
                if (serialArray.length > 0) {
                  // Find the first slot machine with matching serial number
                  const slotMachine = slotMachines.find(slot => 
                    serialArray.includes(slot.serial_number)
                  );
                  if (slotMachine) {
                    location = locations.find(l => l.id === slotMachine.location_id);
                  }
                }
              }
              
              // Fallback to direct location_id if no slot machine found
              if (!location && item.location_id) {
                location = locations.find(l => l.id === item.location_id);
              }
              
              return (
                <div>
                  <div style={{ fontWeight: 'bold' }}>
                    {location ? location.name : 'No location'}
                  </div>
                  <div style={{ fontSize: '0.8em', color: 'var(--text-secondary)' }}>
                    {location ? `${location.city}, ${location.county}` : 'N/A'}
                  </div>
                </div>
              );
            }
          },
          { 
            key: 'issue_date', 
            label: 'Issue Date',
            render: (item) => formatDateDDMMYYYY(item.issue_date)
          },
          { 
            key: 'due_date', 
            label: 'Due Date',
            render: (item) => formatDateDDMMYYYY(item.due_date)
          },
          { 
            key: 'amount', 
            label: 'Amount',
            render: (item) => {
              const formatAmount = (amount) => {
                if (!amount) return '0,00';
                const num = parseFloat(amount);
                if (isNaN(num)) return '0,00';
                const formatted = num.toFixed(2);
                const parts = formatted.split('.');
                const integerPart = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.');
                return `${integerPart},${parts[1]}`;
              };
              return formatAmount(item.amount);
            }
          },
          { 
            key: 'status', 
            label: 'Status',
            render: (item) => {
              const statusColors = {
                'paid': '🟢',
                'pending': '🟡',
                'overdue': '🔴',
                'cancelled': '⚫'
              };
              return (
                <span style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '4px',
                  fontWeight: 'bold'
                }}>
                  {statusColors[item.status] || '⚪'} {item.status || 'Unknown'}
                </span>
              );
            }
          },

          { 
            key: 'slot_count', 
            label: 'NUMBER OF SLOTS', 
            render: (item) => {
              if (!item.serial_numbers) return (
                <span style={{ 
                  backgroundColor: 'var(--accent-color)', 
                  color: 'white',
                  padding: '4px 8px',
                  borderRadius: '12px',
                  fontSize: '0.9em',
                  fontWeight: 'bold',
                  cursor: 'pointer'
                }} onClick={() => setSelectedInvoiceSlots([])}>
                  0 slots
                </span>
              );
              const serials = item.serial_numbers.split(/\s|\n/).filter(s => s.trim());
              const associatedSlots = slotMachines.filter(slot => 
                serials.includes(slot.serial_number)
              );
              return (
                <span 
                  style={{ 
                    backgroundColor: 'var(--accent-color)', 
                    color: 'white',
                    padding: '4px 8px',
                    borderRadius: '12px',
                    fontSize: '0.9em',
                    fontWeight: 'bold',
                    cursor: 'pointer'
                  }} 
                  onClick={() => setSelectedInvoiceSlots(associatedSlots)}
                  title="Click to view slot details"
                >
                  {serials.length} slots
                </span>
              );
            }
          },
          { 
            key: 'description', 
            label: 'Description',
            render: (item) => {
              const cleanDescription = (description) => {
                if (!description) return 'No description';
                return description
                  .replace(/€/g, '')
                  .replace(/EUR/g, '')
                  .replace(/\s+/g, ' ')
                  .trim();
              };
              return cleanDescription(item.description);
            }
          }
        ], { 
          onAdd: () => handleAddEntity('invoices'),
          onEdit: (item) => handleEditEntity(item, 'invoices'),
          onDelete: (id) => handleDeleteEntity(id, 'invoices'),
          onBulkEdit: () => handleBulkEdit('invoices'),
          onBulkDelete: () => handleBulkDelete('invoices'),
          onExport: () => handleExport('invoices'),
          onImport: () => handleImport('invoices')
        });
      case 'onjn':
        // Combină ONJN Reports și Comision Dates într-un singur tabel
        console.log('🔄 Creating combinedOnjnData:', { onjnReports: onjnReports.length, comisionDates: comisionDates.length });
        const combinedOnjnData = [
          ...onjnReports.map(item => ({ ...item, type: 'onjn_report' })),
          ...comisionDates.map(item => ({ 
            ...item, 
            type: 'comision_date',
            report_number: `COM-${item.id.slice(0, 8)}`,
            report_type: 'Commission Date',
            report_date: item.commission_date,
            submission_date: null,
            created_by: item.created_by, // Păstrează câmpul created_by original
            entityType: 'comision_dates' // Entity type pentru atașamente
          }))
        ];
        console.log('📋 Combined data length:', combinedOnjnData.length);
        
        return renderTable('ONJN Reports', combinedOnjnData, [
          { 
            key: 'report_number', 
            label: 'Event Name',
            render: (item) => {
              if (item.type === 'comision_date') {
                return (
                  <span 
                    style={{ 
                      fontWeight: 'bold',
                      color: 'var(--text-primary)',
                      cursor: 'pointer',
                      textDecoration: 'underline',
                      padding: '2px 4px',
                      borderRadius: '4px',
                      transition: 'background-color 0.2s'
                    }}
                    onMouseEnter={(e) => e.target.style.backgroundColor = 'var(--background-secondary)'}
                    onMouseLeave={(e) => e.target.style.backgroundColor = 'transparent'}
                    onClick={() => handleOpenCommissionDateDetails(item)}
                    title="Click to edit Event Name"
                  >
                    {item.event_name || `COM-${item.id.slice(0, 8)}`}
                  </span>
                );
              } else {
                return item.report_number || 'N/A';
              }
            }
          },
          { 
            key: 'type', 
            label: 'Type',
            render: (item) => {
              if (item.type === 'comision_date') {
                return (
                  <span style={{ 
                    backgroundColor: '#3182ce', 
                    color: 'white',
                    padding: '4px 8px',
                    borderRadius: '12px',
                    fontSize: '0.8em',
                    fontWeight: 'bold',
                    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
                  }}>
                    📅 Commission Date
                  </span>
                );
              } else {
                return (
                  <span style={{ 
                    backgroundColor: '#3182ce', 
                    color: 'white',
                    padding: '4px 8px',
                    borderRadius: '12px',
                    fontSize: '0.8em',
                    fontWeight: 'bold',
                    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
                  }}>
                    📋 ONJN Report
                  </span>
                );
              }
            }
          },
          { 
            key: 'report_date', 
            label: 'Report Date',
            render: (item) => formatDateDDMMYYYY(item.report_date)
          },

          {
            key: 'slot_count',
            label: 'Number of Slots',
            render: (item) => {
              if (item.type === 'comision_date' && item.serial_numbers) {
                const serials = item.serial_numbers.split(/\s+/).filter(s => s.trim());
                return (
                  <div style={{ 
                    backgroundColor: '#3182ce', 
                    color: 'white',
                    padding: '4px 8px',
                    borderRadius: '12px',
                    fontSize: '0.9em',
                    fontWeight: 'bold',
                    display: 'inline-block',
                    minWidth: '60px',
                    textAlign: 'center',
                    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
                  }}>
                    {serials.length} slots
                  </div>
                );
              } else if (item.type === 'onjn_report') {
                // Pentru ONJN Reports, să calculăm numărul de sloturi din serial_numbers dacă există
                if (item.serial_numbers) {
                  const serials = item.serial_numbers.split(/\s+/).filter(s => s.trim());
                  return (
                    <div style={{ 
                      backgroundColor: '#3182ce', 
                      color: 'white',
                      padding: '4px 8px',
                      borderRadius: '12px',
                      fontSize: '0.9em',
                      fontWeight: 'bold',
                      display: 'inline-block',
                      minWidth: '60px',
                      textAlign: 'center',
                      boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
                    }}>
                      {serials.length} slots
                    </div>
                  );
                } else {
                  return (
                    <div style={{ 
                      backgroundColor: '#e5e7eb', 
                      color: '#6b7280',
                      padding: '4px 8px',
                      borderRadius: '12px',
                      fontSize: '0.9em',
                      fontWeight: 'bold',
                      display: 'inline-block',
                      minWidth: '60px',
                      textAlign: 'center'
                    }}>
                      0 slots
                    </div>
                  );
                }
              }
              return (
                <div style={{ 
                  backgroundColor: '#e5e7eb', 
                  color: '#6b7280',
                  padding: '4px 8px',
                  borderRadius: '12px',
                  fontSize: '0.9em',
                  fontWeight: 'bold',
                  display: 'inline-block',
                  minWidth: '60px',
                  textAlign: 'center'
                }}>
                  0 slots
                </div>
              );
            }
          },
          {
            key: 'gaming_places_count',
            label: 'Number of Gaming Places',
            render: (item) => {
              if (item.type === 'comision_date' && item.serial_numbers) {
                const serials = item.serial_numbers.split(/\s+/).filter(s => s.trim());
                // Calculate total gaming places from associated slots
                const associatedSlots = slotMachines.filter(slot => 
                  serials.includes(slot.serial_number)
                );
                const totalGamingPlaces = associatedSlots.reduce((total, slot) => 
                  total + (parseInt(slot.gaming_places) || 0), 0
                );
                return (
                  <div style={{ 
                    backgroundColor: '#28a745', 
                    color: 'white',
                    padding: '4px 8px',
                    borderRadius: '12px',
                    fontSize: '0.9em',
                    fontWeight: 'bold',
                    display: 'inline-block',
                    minWidth: '60px',
                    textAlign: 'center',
                    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
                  }}>
                    {totalGamingPlaces} places
                  </div>
                );
              } else if (item.type === 'onjn_report') {
                // Pentru ONJN Reports, să calculăm numărul de gaming places din serial_numbers dacă există
                if (item.serial_numbers) {
                  const serials = item.serial_numbers.split(/\s+/).filter(s => s.trim());
                  const associatedSlots = slotMachines.filter(slot => 
                    serials.includes(slot.serial_number)
                  );
                  const totalGamingPlaces = associatedSlots.reduce((total, slot) => 
                    total + (parseInt(slot.gaming_places) || 0), 0
                  );
                  return (
                    <div style={{ 
                      backgroundColor: '#28a745', 
                      color: 'white',
                      padding: '4px 8px',
                      borderRadius: '12px',
                      fontSize: '0.9em',
                      fontWeight: 'bold',
                      display: 'inline-block',
                      minWidth: '60px',
                      textAlign: 'center',
                      boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
                    }}>
                      {totalGamingPlaces} places
                    </div>
                  );
                } else {
                  return (
                    <div style={{ 
                      backgroundColor: '#e5e7eb', 
                      color: '#6b7280',
                      padding: '4px 8px',
                      borderRadius: '12px',
                      fontSize: '0.9em',
                      fontWeight: 'bold',
                      display: 'inline-block',
                      minWidth: '60px',
                      textAlign: 'center'
                    }}>
                      0 places
                    </div>
                  );
                }
              }
              return (
                <div style={{ 
                  backgroundColor: '#e5e7eb', 
                  color: '#6b7280',
                  padding: '4px 8px',
                  borderRadius: '12px',
                  fontSize: '0.9em',
                  fontWeight: 'bold',
                  display: 'inline-block',
                  minWidth: '60px',
                  textAlign: 'center'
                }}>
                  0 places
                </div>
              );
            }
          }
        ], { 
          onAdd: () => handleAddEntity('onjn'),
          onEdit: (item) => {
            if (item.type === 'comision_date') {
              handleEditEntity(item, 'comision_date');
            } else {
              handleEditEntity(item, 'onjn');
            }
          },
          onDelete: (id) => {
            const item = combinedOnjnData.find(item => item.id === id);
            if (item && item.type === 'comision_date') {
              handleDeleteEntity(id, 'comision_date');
            } else {
              handleDeleteEntity(id, 'onjn');
            }
          },
          onBulkEdit: () => handleBulkEdit('onjn'),
          onBulkDelete: () => handleBulkDelete('onjn'),
          onExport: () => handleExport('onjn'),
          onImport: () => handleImport('onjn'),
          additionalButtons: [
            {
              label: 'Add Comision Date',
              onClick: () => handleAddEntity('comision_date'),
              icon: '📅',
              style: { backgroundColor: 'var(--gradient-primary)', color: 'white' }
            }
          ],
          entityType: 'onjn'
        }, 'onjn');
      case 'legal':
        return renderTable('Legal Documents', legalDocuments, [
          { key: 'title', label: 'Document Title' },
          { key: 'document_type', label: 'Type' },
          { key: 'issuing_authority', label: 'Issuing Authority' },
          { 
            key: 'issue_date', 
            label: 'Issue Date',
            render: (item) => new Date(item.issue_date).toLocaleDateString()
          },
          { 
            key: 'expiry_date', 
            label: 'Expiry Date',
            render: (item) => item.expiry_date ? 
              new Date(item.expiry_date).toLocaleDateString() : 'No expiry'
          }
        ], { 
          onAdd: () => handleAddEntity('legal'),
          onEdit: (item) => handleEditEntity(item, 'legal'),
          onDelete: (id) => handleDeleteEntity(id, 'legal'),
          onBulkEdit: () => handleBulkEdit('legal'),
          onBulkDelete: () => handleBulkDelete('legal'),
          onExport: () => handleExport('legal'),
          onImport: () => handleImport('legal')
        });
      case 'users':
        return renderTable('Users', users, [
          { 
            key: 'avatar', 
            label: 'Avatar',
            render: (item) => (
                              <AvatarDisplay entityType="users" entityId={item.id} size={50} entityName={`${item.first_name} ${item.last_name}`} />
            )
          },
          { 
            key: 'username', 
            label: 'Name',
            render: (item) => (
              <div>
                <div style={{ fontWeight: 'bold' }}>
                  {item.first_name && item.last_name ? `${item.first_name} ${item.last_name}` : item.username || 'N/A'}
                </div>
                <div style={{ fontSize: '0.8em', color: 'var(--text-secondary)' }}>
                  {item.username || 'No username'}
                </div>
              </div>
            )
          },
          { 
            key: 'email', 
            label: 'Email',
            render: (item) => (
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ fontSize: '16px' }}>📧</span>
                <span>{item.email || 'N/A'}</span>
              </div>
            )
          },
          { 
            key: 'phone', 
            label: 'Phone',
            render: (item) => (
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ fontSize: '16px' }}>📞</span>
                <span>{item.phone || 'N/A'}</span>
              </div>
            )
          },
          { key: 'role', label: 'Role' },
          { 
            key: 'assigned_locations', 
            label: 'Assigned Locations',
            render: (item) => {
              if (item.role === 'admin') return 'All Locations';
              if (!item.assigned_locations || item.assigned_locations.length === 0) return 'No Locations';
              return `${item.assigned_locations.length} Location(s)`;
            }
          },
          { 
            key: 'created_at', 
            label: 'Created',
            render: (item) => new Date(item.created_at).toLocaleDateString()
          },
          { 
            key: 'is_active', 
            label: 'Active',
            render: (item) => item.is_active ? 'Yes' : 'No'
          }
        ], { 
          onAdd: () => {
            setEditingUser(null);
            setShowUserForm(true);
          },
          onEdit: handleEditUser,
          onDelete: (id) => handleDeleteEntity(id, 'users'),
          onBulkEdit: () => handleBulkEdit('users'),
          onBulkDelete: () => handleBulkDelete('users'),
          onExport: () => handleExport('users'),
          onImport: () => handleImport('users')
        });
      case 'comision_date':
        return renderTable('Comision Dates', comisionDates, [
          { 
            key: 'event_name', 
            label: 'Event Name',
            render: (item) => (
              <div style={{ fontWeight: 'bold', color: 'var(--text-primary)' }}>
                {item.event_name || 'Unnamed Event'}
              </div>
            )
          },
          { 
            key: 'commission_date', 
            label: 'Commission Date',
            render: (item) => new Date(item.commission_date).toLocaleDateString()
          },
          { 
            key: 'serial_numbers', 
            label: 'Serial Numbers',
            render: (item) => {
              const serials = item.serial_numbers.split(' ').filter(s => s.trim());
              return (
                <div>
                  <div style={{ fontWeight: 'bold' }}>
                    {serials.length} slot(s)
                  </div>
                  <div style={{ fontSize: '0.8em', color: 'var(--text-secondary)' }}>
                    {serials.slice(0, 3).join(', ')}
                    {serials.length > 3 && ` +${serials.length - 3} more`}
                  </div>
                </div>
              );
            }
          },
          { 
            key: 'created_at', 
            label: 'Created',
            render: (item) => new Date(item.created_at).toLocaleDateString()
          }
        ], { 
          onAdd: () => handleAddEntity('comision_date'),
          onEdit: (item) => handleEditEntity(item, 'comision_date'),
          onDelete: (id) => handleDeleteEntity(id, 'comision_date'),
          onBulkEdit: () => handleBulkEdit('comision_date'),
          onBulkDelete: () => handleBulkDelete('comision_date'),
          onExport: () => handleExport('comision_date'),
          onImport: () => handleImport('comision_date')
        });
      default:
        return renderDashboard();
      case 'marketing': {
        const marketingColumns = [
          { key: 'name', label: 'Name', sortable: true },
          { key: 'type', label: 'Type', sortable: true },
          { key: 'description', label: 'Description', sortable: true },
          { key: 'locations', label: 'Locations', sortable: false, render: (value) => {
            if (!value || value.length === 0) return 'None';
            const locationNames = value.map(locId => {
              const location = locations.find(l => l.id === locId);
              return location ? location.name : locId;
            });
            return locationNames.join(', ');
          }},
          { key: 'start_at', label: 'Start Date', sortable: true, render: (value) => formatDateDDMMYYYY(value) },
          { key: 'end_at', label: 'End Date', sortable: true, render: (value) => formatDateDDMMYYYY(value) },
          { key: 'status', label: 'Status', sortable: true },
          { key: 'payouts', label: 'Payouts', sortable: false, render: (value) => {
            if (!value || value.length === 0) return '0';
            const totalAmount = value.reduce((sum, payout) => sum + (payout.amount || 0), 0);
            return `${value.length} (${totalAmount.toFixed(2)} RON)`;
          }},
          { key: 'created_at', label: 'Created', sortable: true, render: (value) => formatDateDDMMYYYY(value) },
          { key: 'created_by', label: 'Created By', sortable: true }
        ];
        
        return renderTable('Marketing Campaigns', marketingCampaigns, marketingColumns, {
          onAdd: () => { setMarketingForm(emptyMarketingForm); setShowMarketingForm(true); },
          onEdit: (item) => { setMarketingForm(item); setShowMarketingForm(true); },
          onDelete: async (id) => {
            if (confirm('Are you sure you want to delete this campaign?')) {
              try {
                const headers = { 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem('token')}` };
                const res = await fetch(`${API}/marketing/campaigns/${id}`, { method: 'DELETE', headers });
                if (res.ok) {
                  await fetchMarketingCampaigns();
                  showCustomNotification('Campaign deleted', 'success');
                } else {
                  showCustomNotification('Failed to delete campaign', 'error');
                }
              } catch (error) {
                showCustomNotification('Error deleting campaign', 'error');
              }
            }
          },
          onBulkEdit: () => handleBulkEdit('marketing'),
          onBulkDelete: () => handleBulkDelete('marketing'),
          onExport: () => handleExport('marketing'),
          onImport: () => handleImport('marketing')
        }, 'marketing');
      }
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }
  return (
    <div className={`app-layout ${theme}`}>
      {/* Unified Header */}
      <div className="main-header" style={{
        color: theme === 'light' ? 'white' : 'inherit'
      }}>
        <div className="header-left">
          <div className="header-logo">
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <img 
                src="/logo.png" 
                alt="CASHPOT Logo" 
                style={{
                  height: '35px',
                  width: 'auto',
                  maxWidth: '150px',
                  objectFit: 'contain'
                }}
              />
            </div>
          </div>
        </div>
        <div className="header-right">
          <button 
            className="theme-toggle"
            onClick={() => {
              const themes = ['light', 'dark', 'dark-gambling'];
              const currentIndex = themes.indexOf(theme);
              const nextIndex = (currentIndex + 1) % themes.length;
              setTheme(themes[nextIndex]);
            }}
            title={`Current: ${theme}. Click to cycle themes`}
          >
            {theme === 'light' ? '☀️' : theme === 'dark' ? '🌙' : '🎰'}
          </button>
          <div className="header-user-info">
            <div className="header-user-avatar">
              {avatar ? (
                <img
                  src={`data:${avatar.mime_type};base64,${avatar.file_data}`}
                  alt="User Avatar"
                  className="user-avatar-img"
                />
              ) : (
                <div className="user-avatar-placeholder">
                  {user?.username?.charAt(0).toUpperCase()}
                </div>
              )}
            </div>
            <div className="header-user-details">
              <span className="header-user-name">
                {user?.first_name && user?.last_name 
                  ? `${user.first_name} ${user.last_name}` 
                  : user?.username}
              </span>
              <span className="header-user-role">{user?.role}</span>
            </div>
          </div>

          <button onClick={logout} className="header-logout-btn" title="Logout">
            ⏻
          </button>
        </div>
      </div>

      {/* Layout Container */}
      <div className="layout-container" data-sidebar={isSidebarCollapsed ? 'collapsed' : 'expanded'}>
        {/* Sidebar */}
        <div className="sidebar" aria-expanded={!isSidebarCollapsed}>
        <div className="sidebar-header" style={{display:'flex',alignItems:'center',justifyContent:'space-between',padding:'8px 12px'}}>
          <span className="sidebar-title" style={{opacity: isSidebarCollapsed ? 0 : 1, transition:'opacity .15s'}}>Menu</span>
          <button
            className="sidebar-toggle"
            aria-label="Toggle sidebar"
            aria-pressed={isSidebarCollapsed}
            onClick={toggleSidebar}
            title={isSidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          >{isSidebarCollapsed ? '»' : '«'}</button>
        </div>
        <nav className="sidebar-nav">
          {navigationItems.map(item => (
            <button
              key={item.id}
              className={`nav-item ${activeView === item.id ? 'active' : ''}`}
              title={item.label}
              onClick={() => {
                // Close Commission Date Details page when navigating to other modules
                if (showCommissionDateDetailsPage) {
                  setShowCommissionDateDetailsPage(false);
                  setSelectedCommissionDate(null);
                }
                if (showJackpotDetailsPage) {
                  setShowJackpotDetailsPage(false);
                  setSelectedJackpot(null);
                }
                if (showMetrologyDetailsPage) {
                  setShowMetrologyDetailsPage(false);
                  setSelectedMetrology(null);
                }
                if (showLocationDetailsPage) {
                  setShowLocationDetailsPage(false);
                  setSelectedLocation(null);
                }
                if (showInvoiceDetailsPage) {
                  setShowInvoiceDetailsPage(false);
                  setSelectedInvoice(null);
                }
                if (showHistoryChangesPage) {
                  setShowHistoryChangesPage(false);
                }
                setActiveView(item.id);
              }}
            >
              <span className="nav-icon">{item.icon}</span>
              <span className="nav-label">{item.label}</span>
              {item.count !== undefined && (
                <span className="nav-count">{item.count}</span>
              )}
            </button>
          ))}
        </nav>
        
        <div className="sidebar-footer">
          <div className="user-info">
            <div className="user-avatar">
              {user?.username?.charAt(0).toUpperCase()}
            </div>
            <div className="user-details">
                <span className="user-name">
                  {user?.first_name && user?.last_name 
                    ? `${user.first_name} ${user.last_name}` 
                    : user?.username}
                </span>
              <span className="user-role">{user?.role}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="main-content">

        <div className="content-body">
          {renderContent()}
        </div>
      </div>
      </div> {/* Close layout-container */}
      
      {/* Entity Form Modal */}
      {showEntityForm && (
        <EntityForm
          entityType={entityType}
          entity={editingEntity}
          onSave={handleSaveEntity}
          onClose={handleCloseEntityForm}
          companies={companies}
          locations={locations}
          providers={providers}
          cabinets={cabinets}
          gameMixes={gameMixes}
          invoices={invoices}
          users={users}
          slotMachines={slotMachines}
          metrology={metrology}
          jackpots={jackpots}
          showCustomNotification={showCustomNotification}
        />
      )}

      {/* Marketing Campaign Modal */}
      {showMarketingForm && (
        <div className="modal-backdrop" onClick={() => setShowMarketingForm(false)}>
          <div className="modal-content">
            <div className="modal-header">
              <h2>{marketingForm.id ? 'Edit Campaign' : 'Create Campaign'}</h2>
              <button className="modal-close" onClick={() => setShowMarketingForm(false)}>✕</button>
            </div>

            <form onSubmit={(e) => e.preventDefault()} className="user-form">
              <div className="form-section">
                <div className="form-grid">
                  <div>
                    <label>Name *</label>
                    <input 
                      className="form-input" 
                      value={marketingForm.name || ''} 
                      onChange={(e) => setMarketingForm({...marketingForm, name: e.target.value})} 
                      placeholder="Campaign name"
                    />
                  </div>
                  <div>
                    <label>Type *</label>
                    <select 
                      className="form-input" 
                      value={marketingForm.type || 'promotion'} 
                      onChange={(e) => setMarketingForm({...marketingForm, type: e.target.value})}
                    >
                      <option value="promotion">Promotion</option>
                      <option value="tombola">Tombola</option>
                      <option value="tournament">Tournament</option>
                    </select>
                  </div>
                  <div>
                    <label>Start Date *</label>
                    <input 
                      type="datetime-local" 
                      className="form-input" 
                      value={marketingForm.start_at || ''} 
                      onChange={(e) => setMarketingForm({...marketingForm, start_at: e.target.value})} 
                    />
                  </div>
                  <div>
                    <label>End Date *</label>
                    <input 
                      type="datetime-local" 
                      className="form-input" 
                      value={marketingForm.end_at || ''} 
                      onChange={(e) => setMarketingForm({...marketingForm, end_at: e.target.value})} 
                    />
                  </div>
                  <div className="form-grid-span">
                    <label>Locations *</label>
                    <div className="checkbox-chips">
                      {locations.map(l => (
                        <label key={l.id} className="checkbox-chip">
                          <input 
                            type="checkbox" 
                            checked={marketingForm.locations?.includes(l.id) || false} 
                            onChange={(e) => {
                              setMarketingForm(prev => {
                                const set = new Set(prev.locations || []);
                                if (e.target.checked) set.add(l.id); else set.delete(l.id);
                                return { ...prev, locations: Array.from(set) };
                              });
                            }} 
                          />
                          <span>{l.name}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                  <div className="form-grid-span">
                    <label>Description</label>
                    <textarea 
                      className="form-textarea" 
                      rows={3} 
                      value={marketingForm.description || ''} 
                      onChange={(e) => setMarketingForm({...marketingForm, description: e.target.value})} 
                      placeholder="Campaign description"
                    />
                  </div>
                </div>

                <div className="form-section">
                  <h3>Payouts (explicit dates)</h3>
                  <div className="payouts-add-row">
                    <input type="date" id="mp_date" className="form-input" />
                    <select id="mp_loc" className="form-input">
                      <option value="">Select Location</option>
                      {locations.map(l => (<option key={l.id} value={l.id}>{l.name}</option>))}
                    </select>
                    <input type="number" min="0" step="0.01" id="mp_amt" placeholder="Amount (RON)" className="form-input" />
                    <button 
                      type="button"
                      className="btn-secondary" 
                      onClick={() => {
                        const d = document.getElementById('mp_date').value;
                        const loc = document.getElementById('mp_loc').value;
                        const amt = parseFloat(document.getElementById('mp_amt').value || '0');
                        if (!d || !loc || !amt) {
                          showCustomNotification('Please fill all payout fields', 'error');
                          return;
                        }
                        setMarketingForm(prev => ({ 
                          ...prev, 
                          payouts: [...(prev.payouts || []), { 
                            date: new Date(d).toISOString(), 
                            location_id: loc, 
                            amount: amt 
                          }] 
                        }));
                        // Clear inputs
                        document.getElementById('mp_date').value = '';
                        document.getElementById('mp_loc').value = '';
                        document.getElementById('mp_amt').value = '';
                      }}
                    >
                      Add Payout
                    </button>
                  </div>
                  
                  <div className="table-container">
                    <table className="data-table">
                      <thead>
                        <tr>
                          <th>Date</th>
                          <th>Location</th>
                          <th>Amount (RON)</th>
                          <th>Action</th>
                        </tr>
                      </thead>
                      <tbody>
                        {(marketingForm.payouts || []).map((p, idx) => {
                          const loc = locations.find(l => l.id === p.location_id);
                          return (
                            <tr key={idx}>
                              <td>{formatDateDDMMYYYY(p.date)}</td>
                              <td>{loc ? loc.name : p.location_id}</td>
                              <td>{p.amount.toFixed(2)}</td>
                              <td>
                                <button 
                                  type="button"
                                  className="btn-danger" 
                                  onClick={() => {
                                    setMarketingForm(prev => ({
                                      ...prev,
                                      payouts: prev.payouts.filter((_, i) => i !== idx)
                                    }));
                                  }}
                                  style={{ padding: '2px 6px', fontSize: '12px' }}
                                >
                                  🗑️
                                </button>
                              </td>
                            </tr>
                          );
                        })}
                        {(!marketingForm.payouts || marketingForm.payouts.length === 0) && (
                          <tr>
                            <td colSpan={4} style={{ textAlign: 'center', padding: '10px', color: 'var(--text-secondary)' }}>
                              No payouts yet.
                            </td>
                          </tr>
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>

              <div className="form-actions">
                <button type="button" onClick={() => setShowMarketingForm(false)} className="btn-cancel">
                  Cancel
                </button>
                <button 
                  type="button"
                  className="btn-save" 
                  disabled={savingMarketing} 
                  onClick={async () => {
                    if (!marketingForm.name || !marketingForm.type || !marketingForm.start_at || !marketingForm.end_at || !marketingForm.locations?.length) {
                      showCustomNotification('Please fill all required fields', 'error');
                      return;
                    }
                    
                    setSavingMarketing(true);
                    try {
                      const headers = { 
                        'Content-Type': 'application/json', 
                        'Authorization': `Bearer ${localStorage.getItem('token')}` 
                      };
                      
                      const method = marketingForm.id ? 'PUT' : 'POST';
                      const url = marketingForm.id 
                        ? `${API}/marketing/campaigns/${marketingForm.id}` 
                        : `${API}/marketing/campaigns`;
                      
                      const res = await fetch(url, { 
                        method, 
                        headers, 
                        body: JSON.stringify({ ...marketingForm }) 
                      });
                      
                      if (res.ok) {
                        setShowMarketingForm(false);
                        setMarketingForm(emptyMarketingForm);
                        await fetchMarketingCampaigns();
                        showCustomNotification(
                          marketingForm.id ? 'Campaign updated' : 'Campaign created', 
                          'success'
                        );
                      } else {
                        showCustomNotification('Failed to save campaign', 'error');
                      }
                    } catch (error) {
                      showCustomNotification('Error saving campaign', 'error');
                    } finally { 
                      setSavingMarketing(false); 
                    }
                  }}
                >
                  {savingMarketing ? 'Saving...' : (marketingForm.id ? 'Update Campaign' : 'Create Campaign')}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Bulk Edit Form Modal */}
      {showBulkEditForm && (
        <BulkEditForm
          entityType={bulkEditType}
          selectedItems={selectedItems}
          onSave={handleBulkEditSave}
          onClose={() => setShowBulkEditForm(false)}
          companies={companies}
          locations={locations}
          providers={providers}
          cabinets={cabinets}
          gameMixes={gameMixes}
          slotMachines={slotMachines}
        />
      )}
      
      {/* User Edit Modal */}
      {showUserForm && (
        <UserEditForm
          user={editingUser}
          onSave={handleSaveUser}
          onClose={handleCloseUserForm}
          companies={companies}
          locations={locations}
          showCustomNotification={showCustomNotification}
        />
      )}

      {/* Invoice Popup Modal */}
              {showInvoicePopup && !showInvoiceDetailsPage && (
          <InvoicePopup 
            invoice={selectedInvoice} 
            onClose={handleCloseInvoicePopup} 
          />
        )}
        {showAddCvtDatePopup && (
          <AddCvtDatePopup 
            onClose={handleCloseAddCvtDatePopup} 
          />
        )}
        
        {/* Jackpot Popup Modal */}
                {selectedJackpots && (
          <JackpotPopup 
            jackpots={selectedJackpots}
            onClose={handleCloseJackpotPopup}
          />
        )}
        
        {selectedInvoiceSlots && (
          <InvoiceSlotsPopup 
            slots={selectedInvoiceSlots}
            onClose={handleCloseInvoiceSlotsPopup}
          />
        )}

        {/* Slot Attachments Modal */}
        {showSlotAttachmentsModal && selectedSlotId && (
          <div className="modal-overlay" onClick={handleCloseSlotAttachments}>
            <div className="modal-content" onClick={e => e.stopPropagation()}>
              <div className="modal-header">
                <h2>Slot Attachments</h2>
                <button className="modal-close" onClick={handleCloseSlotAttachments}>×</button>
              </div>
              <div className="modal-body">
                <FileDisplay 
                  entityType="slots" 
                  entityId={selectedSlotId} 
                  showCustomNotification={showCustomNotification}
                  onFileDelete={() => {
                    // Refresh attachment count after delete
                    console.log('Slot file deleted, attachment count should refresh');
                  }}
                />
              </div>
            </div>
          </div>
        )}

        {/* Entity Attachments Modal */}
        {showEntityAttachmentsModal && selectedEntityType && selectedEntityId && (
          <div className="modal-overlay" onClick={handleCloseEntityAttachments}>
            <div className="modal-content" onClick={e => e.stopPropagation()}>
              <div className="modal-header">
                <h2>{getEntityDisplayName(selectedEntityType)} Attachments</h2>
                <button className="modal-close" onClick={handleCloseEntityAttachments}>×</button>
              </div>
              <div className="modal-body">
                <FileDisplay 
                  entityType={selectedEntityType} 
                  entityId={selectedEntityId} 
                  showCustomNotification={showCustomNotification}
                  onFileDelete={() => {
                    // Refresh attachment count after delete
                    if (selectedEntityType === 'slots') {
                      // For slots, the AttachmentIndicator will refresh automatically
                    } else {
                      // For other entities, we might need to trigger a refresh
                      console.log('File deleted, attachment count should refresh');
                    }
                  }}
                />
              </div>
            </div>
          </div>
        )}

        {/* Metrology Popup Modal */}
        {selectedMetrology && !showMetrologyDetailsPage && (
          <MetrologyPopup 
            metrology={selectedMetrology}
            onClose={handleCloseMetrologyPopup}
          />
        )}

        {/* CVT Attachments Modal */}
        {showCvtAttachments && selectedCvtForAttachments && (
          <div className="modal-overlay" onClick={handleCloseCvtAttachments}>
            <div className="modal-content" onClick={e => e.stopPropagation()}>
              <div className="modal-header">
                <h2>CVT Attachments</h2>
                <button className="modal-close" onClick={handleCloseCvtAttachments}>×</button>
              </div>
              <div className="modal-body">
                <FileDisplay 
                  entityType="metrology" 
                  entityId={selectedCvtForAttachments} 
                  showCustomNotification={showCustomNotification}
                  onFileDelete={() => {
                    // Refresh attachment count after delete
                    console.log('CVT file deleted, attachment count should refresh');
                  }}
                />
              </div>
            </div>
          </div>
        )}

        {/* Change History Modal */}
        {showChangeHistoryModal && (
          <div className="modal-overlay" onClick={handleCloseChangeHistory}>
            <div className="modal-content" onClick={e => e.stopPropagation()} style={{ maxWidth: '900px', width: '90%' }}>
              <div className="modal-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ fontSize: '18px' }}>📋</span>
                  <h2>Change History for {selectedHistoryEntityId === 'all' ? 'All Slot Machines' : getEntityDisplayName(selectedHistoryEntityType)}</h2>
                </div>
                <button className="modal-close" onClick={handleCloseChangeHistory}>×</button>
              </div>
              <div className="modal-body">
                {changeHistoryData.length === 0 ? (
                  <div style={{ 
                    textAlign: 'center', 
                    padding: '40px 20px',
                    color: 'var(--text-secondary)',
                    fontSize: '14px'
                  }}>
                    No changes in history for {selectedHistoryEntityId === 'all' ? 'any slot machines' : `this ${getEntityDisplayName(selectedHistoryEntityType).toLowerCase()}`}
                  </div>
                ) : (
                  <div style={{ 
                    maxHeight: '500px', 
                    overflowY: 'auto',
                    padding: '0 8px'
                  }}>
                    {changeHistoryData.map((change, index) => (
                      <div key={change.id} style={{
                        border: '1px solid var(--border-color)',
                        borderRadius: '8px',
                        padding: '16px',
                        marginBottom: '12px',
                        backgroundColor: index % 2 === 0 ? 'var(--background-primary)' : 'var(--background-secondary)',
                        fontFamily: 'var(--font-family)'
                      }}>
                        <div style={{
                          display: 'flex',
                          justifyContent: 'space-between',
                          alignItems: 'flex-start',
                          marginBottom: '8px'
                        }}>
                          <div style={{ flex: 1 }}>
                            <div style={{
                              display: 'flex',
                              alignItems: 'center',
                              gap: '8px',
                              marginBottom: '4px'
                            }}>
                              <span style={{ 
                                fontWeight: '600', 
                                color: 'var(--text-primary)',
                                fontSize: '14px'
                              }}>
                                {change.entity_id} - {change.field_name}
                              </span>
                              {change.applied_successfully === true ? (
                                <span style={{ color: '#4caf50', fontWeight: '500', fontSize: '12px' }}>✅ Applied</span>
                              ) : change.applied_successfully === false ? (
                                <span style={{ color: '#f44336', fontWeight: '500', fontSize: '12px' }}>❌ Failed</span>
                              ) : (
                                <span style={{ color: '#ff9800', fontWeight: '500', fontSize: '12px' }}>⏳ Pending</span>
                              )}
                            </div>
                            <div style={{
                              display: 'flex',
                              gap: '16px',
                              fontSize: '13px',
                              color: 'var(--text-secondary)',
                              marginBottom: '8px'
                            }}>
                              <span><strong>Old:</strong> {change.old_value || '-'}</span>
                              <span><strong>New:</strong> {change.new_value || '-'}</span>
                            </div>
                            <div style={{
                              display: 'flex',
                              gap: '16px',
                              fontSize: '12px',
                              color: 'var(--text-secondary)'
                            }}>
                              <span><strong>Scheduled:</strong> {new Date(change.scheduled_datetime).toLocaleString()}</span>
                              <span><strong>By:</strong> {change.user_name}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* All Modifications History Modal */}
        {showAllModificationsModal && (
          <div className="modal-overlay" onClick={handleCloseAllModificationsHistory}>
            <div className="modal-content" onClick={e => e.stopPropagation()} style={{ maxWidth: '900px', width: '90%' }}>
              <div className="modal-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ fontSize: '18px' }}>📊</span>
                  <h2>All Modifications History for {selectedAllModificationsEntityId === 'all' ? 'All Slot Machines' : getEntityDisplayName(selectedAllModificationsEntityType)}</h2>
                </div>
                <button className="modal-close" onClick={handleCloseAllModificationsHistory}>×</button>
              </div>
              <div className="modal-body">
                {allModificationsData.length === 0 ? (
                  <div style={{ 
                    textAlign: 'center', 
                    padding: '40px 20px',
                    color: 'var(--text-secondary)',
                    fontSize: '14px'
                  }}>
                    No modifications in history for {selectedAllModificationsEntityId === 'all' ? 'any slot machines' : `this ${getEntityDisplayName(selectedAllModificationsEntityType).toLowerCase()}`}
                  </div>
                ) : (
                  <div style={{ 
                    maxHeight: '500px', 
                    overflowY: 'auto',
                    padding: '0 8px'
                  }}>
                    {allModificationsData.map((modification, index) => (
                      <div key={modification.id} style={{
                        border: '1px solid var(--border-color)',
                        borderRadius: '8px',
                        padding: '16px',
                        marginBottom: '12px',
                        backgroundColor: index % 2 === 0 ? 'var(--background-primary)' : 'var(--background-secondary)',
                        fontFamily: 'var(--font-family)'
                      }}>
                        <div style={{
                          display: 'flex',
                          justifyContent: 'space-between',
                          alignItems: 'flex-start',
                          marginBottom: '8px'
                        }}>
                          <div style={{ flex: 1 }}>
                            <div style={{
                              display: 'flex',
                              alignItems: 'center',
                              gap: '8px',
                              marginBottom: '4px'
                            }}>
                              <span style={{ 
                                fontWeight: '600', 
                                color: 'var(--text-primary)',
                                fontSize: '14px'
                              }}>
                                {modification.entity_id} - {modification.field_name}
                              </span>
                              <span style={{ 
                                color: modification.change_type === 'Scheduled' ? '#3182ce' : '#059669', 
                                fontWeight: '500', 
                                fontSize: '12px',
                                backgroundColor: modification.change_type === 'Scheduled' ? '#dbeafe' : '#d1fae5',
                                padding: '2px 6px',
                                borderRadius: '4px'
                              }}>
                                {modification.change_type}
                              </span>
                              {modification.applied_successfully === true ? (
                                <span style={{ color: '#4caf50', fontWeight: '500', fontSize: '12px' }}>✅ Applied</span>
                              ) : modification.applied_successfully === false ? (
                                <span style={{ color: '#f44336', fontWeight: '500', fontSize: '12px' }}>❌ Failed</span>
                              ) : (
                                <span style={{ color: '#ff9800', fontWeight: '500', fontSize: '12px' }}>⏳ Pending</span>
                              )}
                            </div>
                            <div style={{
                              display: 'flex',
                              gap: '16px',
                              fontSize: '13px',
                              color: 'var(--text-secondary)',
                              marginBottom: '8px'
                            }}>
                              <span><strong>Old:</strong> {modification.old_value || '-'}</span>
                              <span><strong>New:</strong> {modification.new_value || '-'}</span>
                            </div>
                            <div style={{
                              display: 'flex',
                              gap: '16px',
                              fontSize: '12px',
                              color: 'var(--text-secondary)'
                            }}>
                              <span><strong>Date:</strong> {new Date(modification.scheduled_datetime).toLocaleString()}</span>
                              <span><strong>By:</strong> {modification.user_name}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Custom Notification */}
        {showNotification && (
          <div style={{
            position: 'fixed',
            top: '20px',
            right: '20px',
            zIndex: 10000,
            fontFamily: 'var(--font-family)'
          }}>
            <div style={{
              backgroundColor: notificationType === 'success' ? '#4caf50' : 
                             notificationType === 'error' ? '#f44336' :
                             notificationType === 'warning' ? '#ff9800' : '#2196f3',
              color: 'white',
              padding: '16px 20px',
              borderRadius: '8px',
              boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
              border: '1px solid rgba(255, 255, 255, 0.2)',
              maxWidth: '400px',
              wordWrap: 'break-word',
              animation: 'slideInRight 0.3s ease-out'
            }}>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px'
              }}>
                <span style={{ fontSize: '18px' }}>
                  {notificationType === 'success' ? '✅' :
                   notificationType === 'error' ? '❌' :
                   notificationType === 'warning' ? '⚠️' : 'ℹ️'}
                </span>
                <span style={{ fontSize: '14px', fontWeight: '500' }}>
                  {notificationMessage}
                </span>
              </div>
            </div>
          </div>
        )}

        {/* Custom Individual Delete Confirmation Modal */}
        {showDeleteConfirm && fileToDelete && (
          <div 
            onClick={() => {
              console.log('🔥 Individual delete overlay clicked, closing modal');
              cancelDeleteEntity();
            }}
            style={{
              position: 'fixed',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              backgroundColor: 'rgba(0, 0, 0, 0.6)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              zIndex: 99999
            }}
          >
            <div 
              onClick={(e) => {
                console.log('🔥 Individual delete modal content clicked, preventing close');
                e.stopPropagation();
              }}
              style={{
                backgroundColor: 'var(--bg-secondary)',
                borderRadius: '12px',
                padding: '24px',
                maxWidth: '450px',
                width: '90%',
                boxShadow: 'var(--glass-shadow)',
                border: '1px solid var(--border-color)',
                position: 'relative',
                backdropFilter: 'var(--glass-blur)'
              }}
            >
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                marginBottom: '20px'
              }}>
                <span style={{ fontSize: '24px' }}>⚠️</span>
                <h3 style={{
                  margin: 0,
                  color: 'var(--text-primary)',
                  fontSize: '20px',
                  fontWeight: '600',
                  fontFamily: 'var(--font-family)'
                }}>
                  Delete Confirmation
                </h3>
              </div>
              
              <p style={{
                margin: '0 0 24px 0',
                color: 'var(--text-secondary)',
                fontSize: '15px',
                lineHeight: '1.6',
                fontFamily: 'var(--font-family)'
              }}>
                Are you sure you want to delete this <strong style={{color: 'var(--text-primary)'}}>{getEntityDisplayName(fileToDelete.type)}</strong>?
                <br />
                <span style={{color: '#ff4757', fontSize: '13px'}}>This action cannot be undone.</span>
              </p>
              
              <div style={{
                display: 'flex',
                gap: '12px',
                justifyContent: 'flex-end'
              }}>
                <button
                  onClick={() => {
                    console.log('🔥 Individual delete cancel button clicked');
                    cancelDeleteEntity();
                  }}
                  style={{
                    padding: '10px 20px',
                    border: '1px solid var(--border-color)',
                    borderRadius: '8px',
                    backgroundColor: 'transparent',
                    color: 'var(--text-primary)',
                    cursor: 'pointer',
                    fontSize: '14px',
                    fontWeight: '500',
                    fontFamily: 'var(--font-family)',
                    transition: 'all 0.2s ease'
                  }}
                  onMouseOver={(e) => {
                    e.target.style.backgroundColor = 'var(--bg-tertiary)';
                  }}
                  onMouseOut={(e) => {
                    e.target.style.backgroundColor = 'transparent';
                  }}
                >
                  Cancel
                </button>
                <button
                  onClick={() => {
                    console.log('🔥 Individual delete confirm button clicked');
                    confirmDeleteEntity();
                  }}
                  style={{
                    padding: '10px 20px',
                    border: 'none',
                    borderRadius: '8px',
                    background: 'var(--gradient-danger)',
                    color: 'white',
                    cursor: 'pointer',
                    fontSize: '14px',
                    fontWeight: '600',
                    fontFamily: 'var(--font-family)',
                    transition: 'all 0.2s ease'
                  }}
                  onMouseOver={(e) => {
                    e.target.style.opacity = '0.9';
                  }}
                  onMouseOut={(e) => {
                    e.target.style.opacity = '1';
                  }}
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Custom Bulk Delete Confirmation Modal */}
        {showBulkDeleteConfirm && (
          console.log('🔥 RENDERING BULK DELETE MODAL:', { showBulkDeleteConfirm, bulkDeleteType, selectedItems }) || null
        ) && (
                      <div 
              onClick={() => {
                console.log('🔥 Overlay clicked, closing modal');
                cancelBulkDelete();
              }}
              style={{
                position: 'fixed',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                backgroundColor: 'rgba(0, 0, 0, 0.6)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                zIndex: 99999
              }}
            >
            <div 
              onClick={(e) => {
                console.log('🔥 Modal content clicked, preventing close');
                e.stopPropagation();
              }}
              style={{
                backgroundColor: 'var(--bg-secondary)',
                borderRadius: '12px',
                padding: '24px',
                maxWidth: '450px',
                width: '90%',
                boxShadow: 'var(--glass-shadow)',
                border: '1px solid var(--border-color)',
                position: 'relative',
                backdropFilter: 'var(--glass-blur)'
              }}
            >
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                marginBottom: '20px'
              }}>
                <span style={{ fontSize: '24px' }}>⚠️</span>
                <h3 style={{
                  margin: 0,
                  color: 'var(--text-primary)',
                  fontSize: '20px',
                  fontWeight: '600',
                  fontFamily: 'var(--font-family)'
                }}>
                  Bulk Delete Confirmation
                </h3>
              </div>
              
              <p style={{
                margin: '0 0 24px 0',
                color: 'var(--text-secondary)',
                fontSize: '15px',
                lineHeight: '1.6',
                fontFamily: 'var(--font-family)'
              }}>
                Are you sure you want to delete <strong style={{color: 'var(--text-primary)'}}>{selectedItems.length} {getEntityDisplayName(bulkDeleteType)}</strong>?
                <br />
                <span style={{color: '#ff4757', fontSize: '13px'}}>This action cannot be undone.</span>
              </p>
              
              <div style={{
                display: 'flex',
                gap: '12px',
                justifyContent: 'flex-end'
              }}>
                <button
                  onClick={() => {
                    console.log('🔥 Cancel button clicked');
                    cancelBulkDelete();
                  }}
                  style={{
                    padding: '10px 20px',
                    border: '1px solid var(--border-color)',
                    borderRadius: '8px',
                    backgroundColor: 'transparent',
                    color: 'var(--text-primary)',
                    cursor: 'pointer',
                    fontSize: '14px',
                    fontWeight: '500',
                    fontFamily: 'var(--font-family)',
                    transition: 'all 0.2s ease'
                  }}
                  onMouseOver={(e) => {
                    e.target.style.backgroundColor = 'var(--bg-tertiary)';
                  }}
                  onMouseOut={(e) => {
                    e.target.style.backgroundColor = 'transparent';
                  }}
                >
                  Cancel
                </button>
                <button
                  onClick={() => {
                    console.log('🔥 Delete All button clicked');
                    confirmBulkDelete();
                  }}
                  style={{
                    padding: '10px 20px',
                    border: 'none',
                    borderRadius: '8px',
                    background: 'var(--gradient-danger)',
                    color: 'white',
                    cursor: 'pointer',
                    fontSize: '14px',
                    fontWeight: '600',
                    fontFamily: 'var(--font-family)',
                    transition: 'all 0.2s ease'
                  }}
                  onMouseOver={(e) => {
                    e.target.style.opacity = '0.9';
                  }}
                  onMouseOut={(e) => {
                    e.target.style.opacity = '1';
                  }}
                >
                  Delete All
                </button>
              </div>
            </div>
          </div>
        )}
        {/* Bulk Status Confirmation Modal */}
        {showBulkStatusConfirm && (
          <div 
            onClick={() => {
              console.log('🔥 Status modal overlay clicked, closing modal');
              cancelBulkStatus();
            }}
            style={{
              position: 'fixed',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              backgroundColor: 'rgba(0, 0, 0, 0.6)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              zIndex: 99999
            }}
          >
            <div 
              onClick={(e) => {
                console.log('🔥 Status modal content clicked, preventing close');
                e.stopPropagation();
              }}
              style={{
                backgroundColor: 'var(--bg-secondary)',
                borderRadius: '12px',
                padding: '24px',
                maxWidth: '450px',
                width: '90%',
                boxShadow: 'var(--glass-shadow)',
                border: '1px solid var(--border-color)',
                position: 'relative',
                backdropFilter: 'var(--glass-blur)'
              }}
            >
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                marginBottom: '20px'
              }}>
                <span style={{ fontSize: '24px' }}>⚠️</span>
                <h3 style={{
                  margin: 0,
                  color: 'var(--text-primary)',
                  fontSize: '20px',
                  fontWeight: '600',
                  fontFamily: 'var(--font-family)'
                }}>
                  Status Change Confirmation
                </h3>
              </div>
              
              <p style={{
                margin: '0 0 24px 0',
                color: 'var(--text-secondary)',
                fontSize: '15px',
                lineHeight: '1.6',
                fontFamily: 'var(--font-family)'
              }}>
                Are you sure you want to set <strong style={{color: 'var(--text-primary)'}}>{selectedItems.length} slots</strong> to <strong style={{color: '#ff4757'}}>INACTIVE</strong>?
                <br />
                <span style={{color: '#ff4757', fontSize: '13px'}}>These slots will disappear from the Slot Machines list and be moved to Warehouse.</span>
              </p>
              
              <div style={{
                display: 'flex',
                gap: '12px',
                justifyContent: 'flex-end'
              }}>
                <button
                  onClick={() => {
                    console.log('🔥 Cancel status button clicked');
                    cancelBulkStatus();
                  }}
                  style={{
                    padding: '10px 20px',
                    border: '1px solid var(--border-color)',
                    borderRadius: '8px',
                    backgroundColor: 'transparent',
                    color: 'var(--text-primary)',
                    cursor: 'pointer',
                    fontSize: '14px',
                    fontWeight: '500',
                    fontFamily: 'var(--font-family)',
                    transition: 'all 0.2s ease'
                  }}
                  onMouseOver={(e) => {
                    e.target.style.backgroundColor = 'var(--bg-tertiary)';
                  }}
                  onMouseOut={(e) => {
                    e.target.style.backgroundColor = 'transparent';
                  }}
                >
                  Cancel
                </button>
                <button
                  onClick={() => {
                    console.log('🔥 Confirm status button clicked');
                    confirmBulkStatus();
                  }}
                  style={{
                    padding: '10px 20px',
                    border: 'none',
                    borderRadius: '8px',
                    background: 'var(--gradient-warning)',
                    color: 'white',
                    cursor: 'pointer',
                    fontSize: '14px',
                    fontWeight: '600',
                    fontFamily: 'var(--font-family)',
                    transition: 'all 0.2s ease'
                  }}
                  onMouseOver={(e) => {
                    e.target.style.opacity = '0.9';
                  }}
                  onMouseOut={(e) => {
                    e.target.style.opacity = '1';
                  }}
                >
                  Set Inactive
                </button>
              </div>
            </div>
          </div>
        )}
        {/* Modal pentru acțiuni programate specifice provider */}
        {showScheduledChangesModal && (
          <div className="modal-overlay" onClick={() => setShowScheduledChangesModal(false)}>
            <div className="modal-content" onClick={e => e.stopPropagation()} style={{ width: '95vw', maxWidth: '1000px', height: 'auto', maxHeight: '90vh', overflow: 'auto' }}>
              <div className="modal-header">
                <h2>⏱️ Scheduled Actions for Provider</h2>
                <button className="modal-close" onClick={() => setShowScheduledChangesModal(false)}>✕</button>
              </div>
              <div style={{ padding: '20px' }}>
                {scheduledChanges.filter(change => change.entityType === 'providers').length === 0 ? (
                  <p style={{ textAlign: 'center', color: 'var(--text-secondary)', fontSize: '16px' }}>
                    No scheduled actions for this provider
                  </p>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    {scheduledChanges.filter(change => change.entityType === 'providers').map((change, index) => (
                      <div key={change.id} style={{ border: '1px solid var(--border-color)', borderRadius: '8px', padding: '16px', backgroundColor: 'var(--bg-secondary)' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                          <div>
                            <h4 style={{ margin: '0 0 8px 0', color: 'var(--text-primary)', fontSize: '16px' }}>
                              Provider ID: {change.itemId}
                            </h4>
                            <p style={{ margin: '0', color: 'var(--text-secondary)', fontSize: '14px' }}>
                              <strong>Scheduled for:</strong> {change.scheduledDateTime}
                            </p>
                            <p style={{ margin: '4px 0 0 0', color: 'var(--text-secondary)', fontSize: '14px' }}>
                              <strong>Modified by:</strong> {change.userName}
                            </p>
                          </div>
                          <button
                            onClick={() => {
                              const historyEntry = {
                                id: Date.now(),
                                originalChange: change,
                                cancelledAt: new Date().toISOString(),
                                status: 'cancelled',
                                entityType: change.entityType,
                                itemId: change.itemId,
                                userName: change.userName,
                                scheduledDateTime: change.scheduledDateTime,
                                changes: change.changes
                              };
                              setChangeHistory(prev => [historyEntry, ...prev]);
                              setScheduledChanges(prev => prev.filter(c => c.id !== change.id));
                            }}
                            style={{ padding: '4px 8px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '12px' }}
                          >
                            Delete
                          </button>
                        </div>
                        <div style={{ marginTop: '12px' }}>
                          <h5 style={{ margin: '0 0 8px 0', color: 'var(--text-primary)', fontSize: '14px' }}>
                            Scheduled Changes:
                          </h5>
                          <pre style={{ background: 'var(--bg-tertiary)', padding: '8px', borderRadius: '4px', fontSize: '13px', color: 'var(--text-secondary)' }}>
                            {JSON.stringify(change.changes, null, 2)}
                          </pre>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Modal pentru istoric modificări specifice provider */}
        {showHistoryModal && (
          <div className="modal-overlay" onClick={() => setShowHistoryModal(false)}>
            <div className="modal-content" onClick={e => e.stopPropagation()} style={{ width: '95vw', maxWidth: '1000px', height: 'auto', maxHeight: '90vh', overflow: 'auto' }}>
              <div className="modal-header">
                <h2>📋 Change History for Provider</h2>
                <button className="modal-close" onClick={() => setShowHistoryModal(false)}>✕</button>
              </div>
              <div style={{ padding: '20px' }}>
                {changeHistory.filter(entry => entry.entityType === 'providers').length === 0 ? (
                  <p style={{ textAlign: 'center', color: 'var(--text-secondary)', fontSize: '16px' }}>
                    No changes in history for this provider
                  </p>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    {changeHistory.filter(entry => entry.entityType === 'providers').map((entry, index) => (
                      <div key={entry.id} style={{ border: '1px solid var(--border-color)', borderRadius: '8px', padding: '16px', backgroundColor: 'var(--bg-secondary)' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                          <div>
                            <h4 style={{ margin: '0 0 8px 0', color: 'var(--text-primary)', fontSize: '16px' }}>
                              Provider ID: {entry.itemId}
                            </h4>
                            <p style={{ margin: '0', color: 'var(--text-secondary)', fontSize: '14px' }}>
                              <strong>Status:</strong> {entry.status}
                            </p>
                            <p style={{ margin: '4px 0 0 0', color: 'var(--text-secondary)', fontSize: '14px' }}>
                              <strong>Modified by:</strong> {entry.userName}
                            </p>
                          </div>
                          <span style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>
                            {entry.appliedAt || entry.cancelledAt}
                          </span>
                        </div>
                        <div style={{ marginTop: '12px' }}>
                          <h5 style={{ margin: '0 0 8px 0', color: 'var(--text-primary)', fontSize: '14px' }}>
                            Applied Changes:
                          </h5>
                          <pre style={{ background: 'var(--bg-tertiary)', padding: '8px', borderRadius: '4px', fontSize: '13px', color: 'var(--text-secondary)' }}>
                            {JSON.stringify(entry.changes, null, 2)}
                          </pre>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
        {showScheduledChangeForSlot !== null && (
          <div className="modal-overlay" onClick={() => setShowScheduledChangeForSlot(null)}>
            <div className="modal-content" onClick={e => e.stopPropagation()} style={{ width: '95vw', maxWidth: '600px', height: 'auto', maxHeight: '90vh', overflow: 'auto' }}>
              <div className="modal-header">
                <h2>⏱️ Scheduled Action for Slot</h2>
                <button className="modal-close" onClick={() => setShowScheduledChangeForSlot(null)}>✕</button>
              </div>
              <div style={{ padding: '20px' }}>
                {scheduledChanges.filter(change => change.entityType === 'slots' && change.itemId === showScheduledChangeForSlot).length === 0 ? (
                  <div style={{ textAlign: 'center' }}>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '16px', marginBottom: '20px' }}>
                      No scheduled actions for this slot
                    </p>
                    <button 
                      onClick={() => {
                        const currentChanges = scheduledChanges.filter(change => change.entityType === 'slots' && change.itemId === showScheduledChangeForSlot);
                        if (currentChanges.length > 0) {
                          // Afișează modal cu modificările existente pentru editare
                          setShowScheduledChangeForSlot(null);
                          setScheduleChangeData({
                            ...slotMachines.find(slot => slot.id === showScheduledChangeForSlot),
                            existingChanges: currentChanges
                          });
                          setShowScheduleChangeModal(true);
                        } else {
                          // Nu există modificări, deschide modal normal
                          setShowScheduledChangeForSlot(null);
                          setScheduleChangeData(slotMachines.find(slot => slot.id === showScheduledChangeForSlot));
                          setShowScheduleChangeModal(true);
                        }
                      }}
                      style={{
                        padding: '10px 20px',
                        backgroundColor: 'var(--accent-color)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '8px',
                        cursor: 'pointer',
                        fontSize: '14px',
                        fontWeight: '600'
                      }}
                    >
                      Schedule New Change
                    </button>
                  </div>
                ) : (
                  <div>
                    {scheduledChanges.filter(change => change.entityType === 'slots' && change.itemId === showScheduledChangeForSlot).map(change => (
                    <div key={change.id} style={{ border: '1px solid var(--border-color)', borderRadius: '8px', padding: '16px', backgroundColor: 'var(--bg-secondary)', marginBottom: 12 }}>
                      <div style={{ marginBottom: 8 }}>
                          <strong style={{ color: '#2c3e50' }}>Scheduled for:</strong> <span style={{ color: '#2c3e50' }}>{change.scheduledDateTime}</span><br />
                          <strong style={{ color: '#2c3e50' }}>Modified by:</strong> <span style={{ color: '#2c3e50' }}>{(() => {
                            // Caută utilizatorul complet în lista de utilizatori
                            const user = Array.isArray(users) ? users.find(u => u.username === change.userName) : null;
                            if (user && user.first_name && user.last_name) {
                              return `${user.first_name} ${user.last_name}`;
                            } else if (user && user.username) {
                              return user.username;
                            } else {
                              return change.userName || 'Unknown User';
                            }
                          })()}</span>
                      </div>
                        <div style={{ background: 'var(--bg-tertiary)', padding: '12px', borderRadius: '4px', fontSize: '13px', color: 'var(--text-secondary)' }}>
                          <div style={{ marginBottom: '8px', fontWeight: 'bold', color: 'var(--text-primary)' }}>Changes:</div>
                          
                          {/* Tabel cu modificările */}
                          <div style={{ 
                            border: '1px solid var(--border-color)', 
                            borderRadius: '4px', 
                            overflow: 'hidden',
                            marginTop: '8px'
                          }}>
                            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px' }}>
                              <thead>
                                <tr style={{ backgroundColor: 'var(--bg-secondary)', borderBottom: '1px solid var(--border-color)' }}>
                                  <th style={{ padding: '8px', textAlign: 'left', borderRight: '1px solid var(--border-color)', fontWeight: 'bold', color: 'var(--text-primary)' }}>Field</th>
                                  <th style={{ padding: '8px', textAlign: 'left', borderRight: '1px solid var(--border-color)', fontWeight: 'bold', color: 'var(--text-primary)' }}>Old Value</th>
                                  <th style={{ padding: '8px', textAlign: 'left', fontWeight: 'bold', color: 'var(--text-primary)' }}>New Value</th>
                                </tr>
                              </thead>
                              <tbody>
                                {/* Status - Always show */}
                                <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                                  <td style={{ padding: '8px', borderRight: '1px solid var(--border-color)', fontWeight: 'bold', color: 'var(--text-primary)' }}>Status</td>
                                  <td style={{ padding: '8px', borderRight: '1px solid var(--border-color)', color: 'var(--text-secondary)' }}>
                                    {change.changes?.status?.old || change.oldValue || '-'}
                                  </td>
                                  <td style={{ padding: '8px', color: 'var(--text-secondary)' }}>
                                    {change.changes?.status?.new || change.newValue || '-'}
                                  </td>
                                </tr>
                                
                                {/* Provider - Always show */}
                                <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                                  <td style={{ padding: '8px', borderRight: '1px solid var(--border-color)', fontWeight: 'bold', color: 'var(--text-primary)' }}>Provider</td>
                                  <td style={{ padding: '8px', borderRight: '1px solid var(--border-color)', color: 'var(--text-secondary)' }}>
                                    {(() => {
                                      const providerId = change.changes?.provider_id?.old || change.provider_id?.old;
                                      const oldProvider = providers.find(p => p.id === providerId);
                                      return oldProvider ? oldProvider.name : (providerId || '-');
                                    })()}
                                  </td>
                                  <td style={{ padding: '8px', color: 'var(--text-secondary)' }}>
                                    {(() => {
                                      const providerId = change.changes?.provider_id?.new || change.provider_id?.new;
                                      const newProvider = providers.find(p => p.id === providerId);
                                      return newProvider ? newProvider.name : (providerId || '-');
                                    })()}
                                  </td>
                                </tr>
                                
                                {/* Game Mix - Always show */}
                                <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                                  <td style={{ padding: '8px', borderRight: '1px solid var(--border-color)', fontWeight: 'bold', color: 'var(--text-primary)' }}>Game Mix</td>
                                  <td style={{ padding: '8px', borderRight: '1px solid var(--border-color)', color: 'var(--text-secondary)' }}>
                                    {(() => {
                                      const gameMixId = change.changes?.game_mix_id?.old || change.game_mix_id?.old;
                                      const oldGameMix = gameMixes.find(g => g.id === gameMixId);
                                      return oldGameMix ? oldGameMix.name : (gameMixId || '-');
                                    })()}
                                  </td>
                                  <td style={{ padding: '8px', color: 'var(--text-secondary)' }}>
                                    {(() => {
                                      const gameMixId = change.changes?.game_mix_id?.new || change.game_mix_id?.new;
                                      const newGameMix = gameMixes.find(g => g.id === gameMixId);
                                      return newGameMix ? newGameMix.name : (gameMixId || '-');
                                    })()}
                                  </td>
                                </tr>
                                
                                {/* Cabinet - Always show */}
                                <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                                  <td style={{ padding: '8px', borderRight: '1px solid var(--border-color)', fontWeight: 'bold', color: 'var(--text-primary)' }}>Cabinet</td>
                                  <td style={{ padding: '8px', borderRight: '1px solid var(--border-color)', color: 'var(--text-secondary)' }}>
                                    {(() => {
                                      const cabinetId = change.changes?.cabinet_id?.old || change.cabinet_id?.old;
                                      const oldCabinet = cabinets.find(c => c.id === cabinetId);
                                      return oldCabinet ? oldCabinet.name : (cabinetId || '-');
                                    })()}
                                  </td>
                                  <td style={{ padding: '8px', color: 'var(--text-secondary)' }}>
                                    {(() => {
                                      const cabinetId = change.changes?.cabinet_id?.new || change.cabinet_id?.new;
                                      const newCabinet = cabinets.find(c => c.id === cabinetId);
                                      return newCabinet ? newCabinet.name : (cabinetId || '-');
                                    })()}
                                  </td>
                                </tr>
                                
                                {/* Model - Always show */}
                                <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                                  <td style={{ padding: '8px', borderRight: '1px solid var(--border-color)', fontWeight: 'bold', color: 'var(--text-primary)' }}>Model</td>
                                  <td style={{ padding: '8px', borderRight: '1px solid var(--border-color)', color: 'var(--text-secondary)' }}>
                                    {change.changes?.model?.old || change.model?.old || '-'}
                                  </td>
                                  <td style={{ padding: '8px', color: 'var(--text-secondary)' }}>
                                    {change.changes?.model?.new || change.model?.new || '-'}
                                  </td>
                                </tr>
                                
                                {/* Location - Always show */}
                                <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                                  <td style={{ padding: '8px', borderRight: '1px solid var(--border-color)', fontWeight: 'bold', color: 'var(--text-primary)' }}>Location</td>
                                  <td style={{ padding: '8px', borderRight: '1px solid var(--border-color)', color: 'var(--text-secondary)' }}>
                                    {(() => {
                                      const locationId = change.changes?.location_id?.old || change.location_id?.old;
                                      const oldLocation = locations.find(l => l.id === locationId);
                                      return oldLocation ? oldLocation.name : (locationId || '-');
                                    })()}
                                  </td>
                                  <td style={{ padding: '8px', color: 'var(--text-secondary)' }}>
                                    {(() => {
                                      const locationId = change.changes?.location_id?.new || change.location_id?.new;
                                      const newLocation = locations.find(l => l.id === locationId);
                                      return newLocation ? newLocation.name : (locationId || '-');
                                    })()}
                                  </td>
                                </tr>
                              </tbody>
                            </table>
                    </div>
                        </div>
                      </div>
                    ))}
                    <div style={{ textAlign: 'center', marginTop: '20px', display: 'flex', gap: '10px', justifyContent: 'center' }}>
                      <button 
                        onClick={() => {
                          const currentChanges = scheduledChanges.filter(change => change.entityType === 'slots' && change.itemId === showScheduledChangeForSlot);
                          if (currentChanges.length > 0) {
                            handleEditScheduledDateTime(currentChanges[0]);
                          }
                        }}
                        style={{
                          padding: '10px 20px',
                          backgroundColor: '#17a2b8',
                          color: 'white',
                          border: 'none',
                          borderRadius: '8px',
                          cursor: 'pointer',
                          fontSize: '14px',
                          fontWeight: '600'
                        }}
                      >
                        Edit Date/Time
                      </button>
                      <button 
                        onClick={() => {
                          const currentChanges = scheduledChanges.filter(change => change.entityType === 'slots' && change.itemId === showScheduledChangeForSlot);
                          if (currentChanges.length > 0) {
                            // Afișează modal cu modificările existente pentru editare
                            setShowScheduledChangeForSlot(null);
                            setScheduleChangeData({
                              ...slotMachines.find(slot => slot.id === showScheduledChangeForSlot),
                              existingChanges: currentChanges
                            });
                            setShowScheduleChangeModal(true);
                          } else {
                            // Nu există modificări, deschide modal normal
                            setShowScheduledChangeForSlot(null);
                            setScheduleChangeData(slotMachines.find(slot => slot.id === showScheduledChangeForSlot));
                            setShowScheduleChangeModal(true);
                          }
                        }}
                        style={{
                          padding: '10px 20px',
                          backgroundColor: 'var(--accent-color)',
                          color: 'white',
                          border: 'none',
                          borderRadius: '8px',
                          cursor: 'pointer',
                          fontSize: '14px',
                          fontWeight: '600'
                        }}
                      >
                        Schedule Additional Change
                      </button>
                      <button 
                        onClick={() => {
                          // Anulare modificări programate
                          const changes = scheduledChanges.filter(change => change.entityType === 'slots' && change.itemId === showScheduledChangeForSlot);
                          if (changes.length > 0) {
                            // Afișează modal custom pentru confirmare
                            setShowCancelConfirmation(true);
                            setCancelConfirmationData({
                              slotId: showScheduledChangeForSlot,
                              changesCount: changes.length
                            });
                          }
                        }}
                        style={{
                          padding: '10px 20px',
                          backgroundColor: '#e74c3c',
                          color: 'white',
                          border: 'none',
                          borderRadius: '8px',
                          cursor: 'pointer',
                          fontSize: '14px',
                          fontWeight: '600'
                        }}
                      >
                        Cancel Changes
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Schedule Change Modal */}
        {showScheduleChangeModal && scheduleChangeData && (
          <div className="modal-overlay" onClick={() => setShowScheduleChangeModal(false)}>
            <div className="modal-content" onClick={e => e.stopPropagation()} style={{ width: '95vw', maxWidth: '600px', height: 'auto', maxHeight: '90vh', overflow: 'auto' }}>
              <div className="modal-header">
                <h2>⏱️ Schedule Changes for Slot Machine</h2>
                <button className="modal-close" onClick={() => setShowScheduleChangeModal(false)}>✕</button>
    </div>
                                            <div style={{ padding: '20px' }}>
                                <ScheduleChangeForm 
                                  slot={scheduleChangeData}
                                  providers={providers}
                                  cabinets={cabinets}
                                  gameMixes={gameMixes}
                                  locations={locations}
                                  users={users}
                                  onSave={(scheduledData) => {
                                    console.log('Scheduling change:', scheduledData);
                                    
                                    // Create a comprehensive change object with ALL fields (current and new values)
                                    const changes = {
                                      status: {
                                        old: scheduleChangeData.status,
                                        new: scheduledData.newStatus
                                      },
                                      provider_id: {
                                        old: scheduleChangeData.provider_id,
                                        new: scheduledData.provider_id || scheduleChangeData.provider_id
                                      },
                                      game_mix_id: {
                                        old: scheduleChangeData.game_mix_id,
                                        new: scheduledData.game_mix_id || scheduleChangeData.game_mix_id
                                      },
                                      cabinet_id: {
                                        old: scheduleChangeData.cabinet_id,
                                        new: scheduledData.cabinet_id || scheduleChangeData.cabinet_id
                                      },
                                      model: {
                                        old: scheduleChangeData.model,
                                        new: scheduledData.model || scheduleChangeData.model
                                      },
                                      location_id: {
                                        old: scheduleChangeData.location_id,
                                        new: scheduledData.location_id || scheduleChangeData.location_id
                                      }
                                    };
                                    
                                    // Create the scheduled change with all modifications
                                    const change = {
                                      id: Date.now() + Math.random(),
                                      entityType: 'slots',
                                      itemId: scheduleChangeData.id,
                                      action: 'comprehensive_update',
                                      oldValue: scheduleChangeData.status,
                                      newValue: scheduledData.newStatus,
                                      changes: changes,
                                      scheduledDateTime: scheduledData.scheduledDateTime,
                                      timestamp: new Date().toISOString(),
                                      userName: user?.username || 'Unknown User'
                                    };
                                    
                                    setScheduledChanges(prev => [...prev, change]);
                                    
                                    const timeUntilExecution = new Date(scheduledData.scheduledDateTime).getTime() - Date.now();
                                    const minutes = Math.floor(timeUntilExecution / (1000 * 60));
                                    const seconds = Math.floor((timeUntilExecution % (1000 * 60)) / 1000);
                                    
                                    showCustomNotification(
                                      `Change scheduled successfully. Will execute in ${minutes}:${seconds.toString().padStart(2, '0')}`,
                                      'success'
                                    );
                                    
                                    setShowScheduleChangeModal(false);
                                    setScheduleChangeData(null);
                                  }}
                                  onCancel={() => {
                                    setShowScheduleChangeModal(false);
                                    setScheduleChangeData(null);
                                  }}
                                />
              </div>
            </div>
          </div>
        )}

        {/* Cancel Confirmation Modal */}
        {showCancelConfirmation && (
          <div className="modal-overlay" onClick={() => setShowCancelConfirmation(false)}>
            <div className="modal-content" onClick={e => e.stopPropagation()} style={{ width: '400px', maxWidth: '90vw' }}>
              <div className="modal-header">
                <h2>⚠️ Cancel Scheduled Changes</h2>
                <button className="modal-close" onClick={() => setShowCancelConfirmation(false)}>✕</button>
              </div>
              <div style={{ padding: '20px' }}>
                <p style={{ color: 'var(--text-primary)', fontSize: '16px', marginBottom: '20px' }}>
                  Do you want to cancel the scheduled changes?
                </p>
                <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
                  <button 
                    onClick={() => setShowCancelConfirmation(false)}
                    style={{
                      padding: '10px 20px',
                      backgroundColor: '#6c757d',
                      color: 'white',
                      border: 'none',
                      borderRadius: '8px',
                      cursor: 'pointer',
                      fontSize: '14px',
                      fontWeight: '600'
                    }}
                  >
                    No
                  </button>
                  <button 
                    onClick={handleCancelScheduledChanges}
                    style={{
                      padding: '10px 20px',
                      backgroundColor: '#e74c3c',
                      color: 'white',
                      border: 'none',
                      borderRadius: '8px',
                      cursor: 'pointer',
                      fontSize: '14px',
                      fontWeight: '600'
                    }}
                  >
                    Yes, Cancel
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Custom Confirmation Modal */}
        {confirmModalData.isOpen && (
          <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            zIndex: 1000
          }}>
            <div style={{
              backgroundColor: 'var(--bg-primary)',
              borderRadius: '8px',
              padding: '24px',
              maxWidth: '500px',
              width: '90%',
              boxShadow: '0 4px 20px rgba(0, 0, 0, 0.3)',
              border: '1px solid var(--border-color)'
            }}>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                marginBottom: '16px'
              }}>
                <span style={{ fontSize: '24px', marginRight: '12px' }}>⚠️</span>
                <h3 style={{
                  margin: 0,
                  color: 'var(--text-primary)',
                  fontSize: '18px',
                  fontWeight: 'bold'
                }}>
                  {confirmModalData.title}
                </h3>
              </div>
              
              <div style={{
                color: 'var(--text-secondary)',
                marginBottom: '24px',
                lineHeight: '1.5',
                whiteSpace: 'pre-line'
              }}>
                {confirmModalData.message}
              </div>
              
              <div style={{
                display: 'flex',
                justifyContent: 'flex-end',
                gap: '12px'
              }}>
                <button
                  onClick={confirmModalData.onCancel}
                  style={{
                    padding: '8px 16px',
                    border: '1px solid var(--border-color)',
                    borderRadius: '4px',
                    backgroundColor: 'transparent',
                    color: 'var(--text-primary)',
                    cursor: 'pointer',
                    fontSize: '14px'
                  }}
                >
                  Cancel
                </button>
                <button
                  onClick={confirmModalData.onConfirm}
                  style={{
                    padding: '8px 16px',
                    border: 'none',
                    borderRadius: '4px',
                    backgroundColor: '#dc3545',
                    color: 'white',
                    cursor: 'pointer',
                    fontSize: '14px',
                    fontWeight: 'bold'
                  }}
                >
                  Continue
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Edit Date/Time Modal */}
        {editDateTimeModal.isOpen && (
          <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            zIndex: 1000
          }}>
            <div style={{
              backgroundColor: 'var(--bg-primary)',
              borderRadius: '8px',
              padding: '24px',
              maxWidth: '400px',
              width: '90%',
              boxShadow: '0 4px 20px rgba(0, 0, 0, 0.3)',
              border: '1px solid var(--border-color)'
            }}>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                marginBottom: '16px'
              }}>
                <span style={{ fontSize: '24px', marginRight: '12px' }}>⏰</span>
                <h3 style={{
                  margin: 0,
                  color: 'var(--text-primary)',
                  fontSize: '18px',
                  fontWeight: 'bold'
                }}>
                  Edit Scheduled Date/Time
                </h3>
              </div>
              
              <div style={{
                color: 'var(--text-secondary)',
                marginBottom: '24px',
                lineHeight: '1.5'
              }}>
                <p>Currently scheduled for: <strong>{editDateTimeModal.scheduledChange?.scheduledDateTime}</strong></p>
                <p>Select new date and time:</p>
              </div>
              
              <div style={{ marginBottom: '24px' }}>
                <input
                  type="datetime-local"
                  value={editDateTimeModal.newDateTime}
                  onChange={(e) => setEditDateTimeModal(prev => ({ ...prev, newDateTime: e.target.value }))}
                  style={{
                    width: '100%',
                    padding: '12px',
                    border: '1px solid var(--border-color)',
                    borderRadius: '4px',
                    fontSize: '14px',
                    backgroundColor: 'var(--bg-secondary)',
                    color: 'var(--text-primary)'
                  }}
                />
              </div>
              
              <div style={{
                display: 'flex',
                justifyContent: 'flex-end',
                gap: '12px'
              }}>
                <button
                  onClick={editDateTimeModal.onCancel}
                  style={{
                    padding: '8px 16px',
                    border: '1px solid var(--border-color)',
                    borderRadius: '4px',
                    backgroundColor: 'transparent',
                    color: 'var(--text-primary)',
                    cursor: 'pointer',
                    fontSize: '14px'
                  }}
                >
                  Cancel
                </button>
                <button
                  onClick={() => editDateTimeModal.onSave(editDateTimeModal.newDateTime)}
                  style={{
                    padding: '8px 16px',
                    border: 'none',
                    borderRadius: '4px',
                    backgroundColor: '#17a2b8',
                    color: 'white',
                    cursor: 'pointer',
                    fontSize: '14px',
                    fontWeight: 'bold'
                  }}
                >
                  Save Changes
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Report Details Modal */}
        {showReportDetailsModal && selectedReportDetails && (
          <ReportDetailsModal 
            report={selectedReportDetails}
            onClose={() => {
              setShowReportDetailsModal(false);
              setSelectedReportDetails(null);
            }}
          />
        )}
    </div>
  );
};
// Main App Component
const App = () => {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
};

const AppContent = () => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading application...</p>
      </div>
    );
  }

  return (
    <div className="App">
      {user ? <Dashboard /> : <Login />}
    </div>
  );
};

export default App;

// Adaug componenta GameMixAvatar sub AvatarDisplay
function GameMixAvatar({ entityId, name }) {
  const { avatar, loading } = useAvatar('game_mixes', entityId);
  if (loading) return <div style={{ width: 20, height: 95 }} />;
  if (avatar) {
    return <img src={`data:${avatar.mime_type};base64,${avatar.file_data}`} alt="Avatar" style={{ width: 20, height: 95, objectFit: 'cover', borderRadius: 4 }} />;
  }
  // Fallback: background albastru cu text alb, font fix
  
  return (
    <div style={{ 
      width: 20, 
      height: 95, 
      background: '#1976d2', 
      color: '#ffffff', 
      fontWeight: 'bold', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center', 
      borderRadius: 4, 
      lineHeight: '1.1'
    }}>
      {name}
    </div>
  );
}