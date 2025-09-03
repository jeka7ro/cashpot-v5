import React, { createContext, useContext, useEffect, useState } from 'react';
import * as XLSX from 'xlsx';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8002';
const API = `${BACKEND_URL}/api`;

// Calendar Component
const Calendar = ({ value, onChange, placeholder = "Select date" }) => {
  const [showCalendar, setShowCalendar] = useState(false);
  const [currentDate, setCurrentDate] = useState(new Date());

  const formatDate = (date) => {
    if (!date) return '';
    return new Date(date).toISOString().split('T')[0];
  };

  const formatDisplayDate = (date) => {
    if (!date) return placeholder;
    return new Date(date).toLocaleDateString('ro-RO', {
      day: '2-digit',
      month: '2-digit', 
      year: 'numeric'
    });
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

  const monthNames = [
    'Ianuarie', 'Februarie', 'Martie', 'Aprilie', 'Mai', 'Iunie',
    'Iulie', 'August', 'Septembrie', 'Octombrie', 'Noiembrie', 'Decembrie'
  ];

  const days = getDaysInMonth(currentDate);
  const selectedDateObj = value ? new Date(value) : null;

  return (
    <div className="calendar-container">
      <div 
        className="calendar-input"
        onClick={() => setShowCalendar(!showCalendar)}
      >
        <span className="calendar-value">
          {formatDisplayDate(value)}
        </span>
        <span className="calendar-icon">📅</span>
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
              {['D', 'L', 'M', 'M', 'J', 'V', 'S'].map(day => (
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
              Azi
            </button>
            <button 
              type="button"
              onClick={() => setShowCalendar(false)}
              className="calendar-close-btn"
            >
              Închide
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
const AvatarUpload = ({ entityType, entityId, currentAvatar, onAvatarChange }) => {
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const { user } = useAuth();

  const handleFileUpload = async (file) => {
    if (!file || !file.type.startsWith('image/')) {
      alert('Please select a valid image file');
      return;
    }

    if (file.size > 5 * 1024 * 1024) { // 5MB limit
      alert('File size must be less than 5MB');
      return;
    }

    setUploading(true);
    try {
      // Convert file to base64
      const base64 = await new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result.split(',')[1]);
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
          filename: `avatar_${Date.now()}.${file.name.split('.').pop()}`,
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
        onAvatarChange(attachment);
      } else {
        throw new Error('Upload failed');
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert('Failed to upload avatar');
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

// Custom hook for fetching avatars
const useAvatar = (entityType, entityId) => {
  const [avatar, setAvatar] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchAvatar = async () => {
    if (!entityType || !entityId) return;
    
    setLoading(true);
    try {
      const response = await fetch(`${API}/attachments/${entityType}/${entityId}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      
      if (response.ok) {
        const attachments = await response.json();
        // Find the first image attachment as avatar
        const avatarAttachment = attachments.find(att => 
          att.mime_type.startsWith('image/') && 
          att.filename.includes('avatar')
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

// Avatar Display Component (for tables)
const AvatarDisplay = ({ entityType, entityId, size = 40 }) => {
  const { avatar, loading } = useAvatar(entityType, entityId);

  if (loading) {
    return (
      <div className="avatar-display loading" style={{ width: size, height: size }}>
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
        style={{ width: size, height: size }}
      />
    );
  }

  // Default avatar with initials or icon
  return (
    <div className="avatar-display default" style={{ width: size, height: size }}>
      <svg width={size * 0.6} height={size * 0.6} viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
      </svg>
    </div>
  );
};

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

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
      setUser(data.user);
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
  if (!type) return 'Entity';
  
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
    metrology: 'Metrology',
    jackpots: 'Jackpot',
    comision_dates: 'Comision Date'
  };
  return names[type] || type;
};

// Bulk Edit Form Component
const BulkEditForm = ({ entityType, selectedItems, onSave, onClose }) => {
  const [formData, setFormData] = useState({});

  const handleChange = (field, value) => {
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
      slots: ['status', 'denomination', 'max_bet'],
      gamemixes: ['status'],
      invoices: ['status'],
      onjn: ['status'],
      legal: ['status'],
      users: ['role', 'is_active']
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
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    
    try {
      await login(username, password);
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
        <div className="login-header">
          <h1>CASHPOT</h1>
          <p>Gaming Industry Management System</p>
        </div>
        
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="form-input"
              placeholder="Enter your username"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="form-input"
              placeholder="Enter your password"
            />
          </div>
          
          {error && <div className="error-message">{error}</div>}
          
          <button type="submit" disabled={loading} className="login-button">
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
        
        <div className="login-footer">
          <p>Demo Admin: admin / admin</p>
          <p>Contact your administrator for access</p>
        </div>
      </div>
    </div>
  );
};

// Generic Entity Form Component
const EntityForm = ({ entityType, entity, onSave, onClose, companies, locations, providers, cabinets, gameMixes, invoices }) => {
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
        manager_id: ''
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
        provider_id: '',
        location_id: ''
      },
      slots: {
        cabinet_id: '',
        game_mix_id: '',
        provider_id: '',
        model: '',
        serial_number: '',
        denomination: 0.10,
        max_bet: 100.00,
        rtp: 95.00,
        gaming_places: 1,
        commission_date: '',
        invoice_number: ''
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
        description: ''
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
        expiry_date: '',
        issuing_authority: '',
        description: ''
      },
      metrology: {
        serial_number: '',
        certificate_number: '',
        certificate_type: '',
        issue_date: new Date().toISOString().split('T')[0],
        expiry_date: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        issuing_authority: '',

        
        description: ''
      }
    };
    return defaults[type] || {};
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
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
              <label>Phone *</label>
              <input
                type="tel"
                value={formData.phone || ''}
                onChange={(e) => handleChange('phone', e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Email *</label>
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
            {entity && (
              <div className="form-group">
                <label>Company Logo</label>
                <div className="avatar-section">
                  <AvatarUpload
                    entityType="companies"
                    entityId={entity.id}
                    currentAvatar={avatar}
                    onAvatarChange={handleAvatarChange}
                  />
                </div>
              </div>
            )}
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
              <label>Email *</label>
              <input
                type="email"
                value={formData.email || ''}
                onChange={(e) => handleChange('email', e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Phone *</label>
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
            {entity && (
              <div className="form-group">
                <label>Provider Logo</label>
                <div className="avatar-section">
                  <AvatarUpload
                    entityType="providers"
                    entityId={entity.id}
                    currentAvatar={avatar}
                    onAvatarChange={handleAvatarChange}
                  />
                </div>
              </div>
            )}
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
              <label>Model *</label>
              <input
                type="text"
                value={formData.model || ''}
                onChange={(e) => handleChange('model', e.target.value)}
                required
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
              <label>Location *</label>
              <select
                value={formData.location_id || ''}
                onChange={(e) => handleChange('location_id', e.target.value)}
                required
              >
                <option value="">Select Location</option>
                {locations.map(location => (
                  <option key={location.id} value={location.id}>{location.name}</option>
                ))}
              </select>
            </div>
            {entity && (
              <div className="form-group">
                <label>Cabinet Logo</label>
                <div className="avatar-section">
                  <AvatarUpload
                    entityType="cabinets"
                    entityId={entity.id}
                    currentAvatar={avatar}
                    onAvatarChange={handleAvatarChange}
                  />
                </div>
              </div>
            )}
          </>
        );

      case 'slots':
        return (
          <>
            <div className="form-group">
              <label>Cabinet *</label>
              <select
                value={formData.cabinet_id || ''}
                onChange={(e) => handleChange('cabinet_id', e.target.value)}
                required
              >
                <option value="">Select Cabinet</option>
                {cabinets.map(cabinet => (
                  <option key={cabinet.id} value={cabinet.id}>
                    {cabinet.manufacturer} {cabinet.model} - {cabinet.serial_number}
                  </option>
                ))}
              </select>
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
              <label>Game Mix *</label>
              <select
                value={formData.game_mix_id || ''}
                onChange={(e) => handleChange('game_mix_id', e.target.value)}
                required
              >
                <option value="">Select Game Mix</option>
                {gameMixes.map(mix => (
                  <option key={mix.id} value={mix.id}>{mix.name}</option>
                ))}
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
              <label>Invoice Number</label>
              <select
                value={formData.invoice_number || ''}
                onChange={(e) => handleChange('invoice_number', e.target.value)}
              >
                <option value="">Select Invoice</option>
                {invoices.map(invoice => (
                  <option key={invoice.id} value={invoice.invoice_number}>
                    {invoice.invoice_number} - {invoice.amount}€
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Model *</label>
              <input
                type="text"
                value={formData.model || ''}
                onChange={(e) => handleChange('model', e.target.value)}
                required
              />
            </div>
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
            <div className="form-group">
              <label>Gaming Places *</label>
              <input
                type="number"
                value={formData.gaming_places || ''}
                onChange={(e) => handleChange('gaming_places', parseInt(e.target.value))}
                required
              />
            </div>
            <div className="form-group">
              <label>Commission Date</label>
              <Calendar
                value={formData.commission_date}
                onChange={(date) => handleChange('commission_date', date)}
                placeholder="Select commission date"
              />
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
            {entity && (
              <div className="form-group">
                <label>Game Mix Avatar</label>
                <div className="avatar-section">
                  <AvatarUpload
                    entityType="game_mixes"
                    entityId={entity.id}
                    currentAvatar={avatar}
                    onAvatarChange={handleAvatarChange}
                  />
                </div>
              </div>
            )}
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
                <option value="">Select Location</option>
                {locations
                  .filter(location => {
                    // Show all locations if no company selected
                    if (!formData.company_id) return true;
                    // Show locations that match the selected company
                    return location.company_id === formData.company_id;
                  })
                  .map(location => (
                    <option key={location.id} value={location.id}>{location.name}</option>
                  ))}
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
      metrology: 'Metrology'
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
const UserEditForm = ({ user, onSave, onClose, companies, locations }) => {
  const [formData, setFormData] = useState({
    username: user?.username || '',
    email: user?.email || '',
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
                <label>Email</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
                  required
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
                />
              </div>
            </div>
          )}

          {/* Module Access */}
          <div className="form-section">
            <h3>Module Access</h3>
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
  const [users, setUsers] = useState([]);
  const [metrology, setMetrology] = useState([]);
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
  const [activeView, setActiveView] = useState('dashboard');
  const [loading, setLoading] = useState(true);
  const [darkMode, setDarkMode] = useState(true);

  // User avatar hook
  const { avatar } = useAvatar('users', user?.id);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };
      
      const [statsRes, companiesRes, locationsRes, providersRes, cabinetsRes, slotMachinesRes, gameMixesRes, invoicesRes, onjnRes, legalRes, usersRes, metrologyRes, adminDataRes] = await Promise.all([
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
        user?.role === 'admin' ? fetch(`${API}/users`, { headers }) : Promise.resolve({ json: () => [] }),
        fetch(`${API}/metrology`, { headers }),
        user?.role === 'admin' ? fetch(`${API}/admin/companies-locations`, { headers }) : Promise.resolve({ json: () => ({ companies: [], locations: [] }) })
      ]);
      
      const [statsData, companiesData, locationsData, providersData, cabinetsData, slotMachinesData, gameMixesData, invoicesData, onjnData, legalData, usersData, metrologyData, adminData] = await Promise.all([
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
        usersRes.json ? usersRes.json() : [],
        metrologyRes.json(),
        adminDataRes.json ? adminDataRes.json() : { companies: [], locations: [] }
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
      setUsers(usersData);
      setMetrology(metrologyData);
      setCompaniesLocations(adminData);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Navigation items
  const navigationItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'companies', label: 'Companies', icon: '🏢', count: companies.length },
    { id: 'locations', label: 'Locations', icon: '📍', count: locations.length },
    { id: 'providers', label: 'Providers', icon: '🎮', count: providers.length },
    { id: 'cabinets', label: 'Cabinets', icon: '🎰', count: cabinets.length },
    { id: 'gamemixes', label: 'Game Mixes', icon: '🎲', count: gameMixes.length },
    { id: 'slots', label: 'Slots', icon: '🎯', count: slotMachines.length },
    { id: 'invoices', label: 'Invoices', icon: '💰', count: invoices.length },
    { id: 'onjn', label: 'ONJN Reports', icon: '📋', count: onjnReports.length },
    { id: 'metrology', label: 'Metrology', icon: '🔬', count: metrology.length },
    { id: 'legal', label: 'Legal Documents', icon: '📄', count: legalDocuments.length },
    ...(user?.role === 'admin' ? [{ id: 'users', label: 'Users', icon: '👥', count: users.length }] : []),
  ];

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
      const token = localStorage.getItem('token');
      const method = editingUser ? 'PUT' : 'POST';
      const url = editingUser ? `${API}/users/${editingUser.id}` : `${API}/users`;
      
      const response = await fetch(url, {
        method,
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(userData)
      });

      if (response.ok) {
        await fetchDashboardData(); // Refresh data
        handleCloseUserForm();
        alert('✅ User saved successfully!');
      } else {
        const errorData = await response.json();
        alert(`❌ Failed to save user: ${errorData.detail || 'Unknown error'}`);
        console.error('Failed to save user');
      }
    } catch (error) {
      alert(`❌ Error saving user: ${error.message}`);
      console.error('Error saving user:', error);
    }
  };

  // Generic entity handlers
  const handleAddEntity = (type) => {
    console.log('🔍 handleAddEntity called with type:', type);
    setEntityType(type);
    setEditingEntity(null);
    setShowEntityForm(true);
  };

  const handleEditEntity = (entityData, type) => {
    console.log('🔍 handleEditEntity called with type:', type);
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
      const token = localStorage.getItem('token');
      const method = editingEntity ? 'PUT' : 'POST';
      
      // Add fallback for undefined entityType
      if (!entityType) {
        console.error('❌ entityType is undefined in handleSaveEntity');
        alert('❌ Error: Entity type is not defined. Please try again.');
        return;
      }
      
      const endpoint = getEntityEndpoint(entityType);
      
      console.log('🔍 handleSaveEntity called with:');
      console.log('  - entityType:', entityType);
      console.log('  - editingEntity:', editingEntity);
      console.log('  - entityData:', entityData);
      console.log('🌐 API URL:', `${API}/${endpoint}/${editingEntity?.id || ''}`);
      console.log('📤 Request body:', entityData);
      
      const url = editingEntity ? `${API}/${endpoint}/${editingEntity.id}` : `${API}/${endpoint}`;
      
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
        await fetchDashboardData(); // Refresh data
        handleCloseEntityForm();
        alert(`✅ ${getEntityDisplayName(entityType)} saved successfully!`);
      } else {
        const error = await response.json();
        console.error('Failed to save entity:', error);
        console.log('📡 Response status:', response.status, response.statusText);
        alert(`❌ Failed to save ${getEntityDisplayName(entityType)}: ${error.detail || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Error saving entity:', error);
      alert(`❌ Error saving ${getEntityDisplayName(entityType)}: ${error.message}`);
    }
  };

  const handleDeleteEntity = async (entityId, type) => {
    console.log('🔥 DELETING DIRECTLY:', entityId, type);

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
        alert('✅ Item deleted successfully!');
        await fetchDashboardData(); // Refresh data
      } else {
        const error = await response.json();
        console.error('❌ DELETE Failed:', error);
        alert('❌ Failed to delete: ' + (error.detail || 'Unknown error'));
      }
    } catch (error) {
      console.error('💥 Delete exception:', error);
      alert('❌ Error deleting: ' + error.message);
    }
  };

  const getEntityEndpoint = (type) => {
    console.log('🔍 getEntityEndpoint called with type:', type);
    
    if (!type) {
      console.error('❌ getEntityEndpoint called with undefined type');
      return 'unknown';
    }
    
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
      jackpots: 'jackpots',
      comision_dates: 'comision-dates'
    };
    const endpoint = endpoints[type] || type;
    console.log('📍 Resolved endpoint:', endpoint);
    return endpoint;
  };

  // Bulk Edit Handler
  const handleBulkEdit = (entityType) => {
    if (selectedItems.length === 0) {
      alert('Please select items to bulk edit');
      return;
    }
    setBulkEditType(entityType);
    setBulkEditData({});
    setShowBulkEditForm(true);
  };

  const handleBulkDelete = async (entityType) => {
    console.log('🔥 BULK DELETE CLICKED:', entityType);
    console.log('🔥 Selected items:', selectedItems);
    
    if (selectedItems.length === 0) {
      alert('❌ Please select items to delete first!');
      return;
    }

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

      alert(`✅ Successfully deleted ${successCount} of ${selectedItems.length} items!`);
      await fetchDashboardData();
      setSelectedItems([]);
      console.log('🔄 Data refreshed, selections cleared');
      
    } catch (error) {
      console.error('💥 Bulk delete error:', error);
      alert('❌ Bulk delete failed: ' + error.message);
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
      const updatePromises = selectedItems.map(async (itemId) => {
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

      const results = await Promise.all(updatePromises);
      const successCount = results.filter(Boolean).length;
      
      if (successCount === selectedItems.length) {
        alert(`✅ Successfully updated ${successCount} ${getEntityDisplayName(bulkEditType)} items!`);
      } else {
        alert(`⚠️ Updated ${successCount} of ${selectedItems.length} items. Some updates failed.`);
      }

      await fetchDashboardData();
      setShowBulkEditForm(false);
      setSelectedItems([]);
    } catch (error) {
      console.error('Bulk edit error:', error);
      alert(`❌ Bulk edit failed: ${error.message}`);
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
      alert('No data to export');
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
    
    alert(`✅ ${exportData.length} ${getEntityDisplayName(entityType)} items exported to Excel successfully!`);
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
          alert('No data found in Excel file');
          return;
        }
        
        // Validate required fields based on entity type
        const requiredFields = getRequiredFields(entityType);
        const missingFields = requiredFields.filter(field => 
          !Object.keys(importData[0]).includes(field)
        );
        
        if (missingFields.length > 0) {
          alert(`Missing required columns: ${missingFields.join(', ')}`);
          return;
        }
        
        // Show preview and confirm import
        const confirmImport = confirm(
          `Found ${importData.length} rows in Excel file.\n\n` +
          `Sample data:\n${JSON.stringify(importData[0], null, 2)}\n\n` +
          `Proceed with import?`
        );
        
        if (confirmImport) {
          // Process import (for now, just show success - actual API calls would go here)
          console.log(`Importing ${importData.length} ${entityType}:`, importData);
          alert(`✅ Ready to import ${importData.length} ${getEntityDisplayName(entityType)} items!\n\n(Note: Actual import functionality would process these items through the API)`);
        }
        
      } catch (error) {
        console.error('Import error:', error);
        alert(`❌ Error reading Excel file: ${error.message}`);
      }
    };
    input.click();
  };

  // Search Filter Function
  const filterData = (data, searchTerm) => {
    if (!data || !Array.isArray(data)) {
      console.warn('filterData: data is not an array:', data);
      return [];
    }
    
    if (!searchTerm) return data;
    
    const search = searchTerm.toLowerCase();
    return data.filter(item => {
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
      users: ['username', 'email', 'role']
    };
    return fields[entityType] || ['name'];
  };

  const renderTable = (title, data, columns, actions, entityType) => {
    // Apply search filter with null checks
    if (!data || !Array.isArray(data)) {
      console.warn(`renderTable: data is not an array for ${title}:`, data);
      data = [];
    }
    
    if (!columns || !Array.isArray(columns)) {
      console.warn(`renderTable: columns is not an array for ${title}:`, columns);
      columns = [];
    }
    
    const filteredData = filterData(data, searchTerm);
    
    return (
      <div className="table-container">
        <div className="table-header">
          <h2>{title}</h2>
          <div className="table-controls">
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
            <div className="table-actions">
              <button 
                className="btn-primary"
                onClick={() => actions?.onAdd && actions.onAdd()}
              >
                <span className="icon">➕</span>
                Add {title.slice(0, -1)}
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
          </div>
        </div>
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
                      <div className="table-row-actions">
                        <button 
                          className="btn-edit"
                          onClick={() => actions?.onEdit && actions.onEdit(item)}
                          title="Edit"
                        >
                          📝 Edit
                        </button>
                        <button 
                          className="btn-delete"
                          onClick={(e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            console.log('🔥 DIRECT DELETE HANDLER!', item.id, entityType);
                            handleDeleteEntity(item.id, entityType);
                          }}
                          title="Delete"
                        >
                          🗑️ Delete
                        </button>
                      </div>
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
        <h1>CASHPOT</h1>
        <p>Gaming Industry Management System</p>
      </div>
      
      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon" style={{ backgroundColor: '#3b82f6' }}>📊</div>
            <div className="stat-content">
              <h3>Total Companies</h3>
              <p className="stat-value">{stats.total_companies}</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon" style={{ backgroundColor: '#10b981' }}>📍</div>
            <div className="stat-content">
              <h3>Total Locations</h3>
              <p className="stat-value">{stats.total_locations}</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon" style={{ backgroundColor: '#f59e0b' }}>🎮</div>
            <div className="stat-content">
              <h3>Gaming Providers</h3>
              <p className="stat-value">{stats.total_providers}</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon" style={{ backgroundColor: '#ef4444' }}>🎰</div>
            <div className="stat-content">
              <h3>Gaming Cabinets</h3>
              <p className="stat-value">{stats.total_cabinets}</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon" style={{ backgroundColor: '#8b5cf6' }}>🎯</div>
            <div className="stat-content">
              <h3>Slot Machines</h3>
              <p className="stat-value">{stats.total_slot_machines}</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon" style={{ backgroundColor: '#06b6d4' }}>⚡</div>
            <div className="stat-content">
              <h3>Active Equipment</h3>
              <p className="stat-value">{stats.active_equipment}</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon" style={{ backgroundColor: '#f59e0b' }}>💰</div>
            <div className="stat-content">
              <h3>Invoices</h3>
              <p className="stat-value">{stats.total_invoices}</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon" style={{ backgroundColor: '#10b981' }}>📋</div>
            <div className="stat-content">
              <h3>ONJN Reports</h3>
              <p className="stat-value">{stats.total_onjn_reports}</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon" style={{ backgroundColor: '#ef4444' }}>📄</div>
            <div className="stat-content">
              <h3>Legal Documents</h3>
              <p className="stat-value">{stats.total_legal_documents}</p>
            </div>
          </div>
          {user?.role === 'admin' && (
            <div className="stat-card">
              <div className="stat-icon" style={{ backgroundColor: '#8b5cf6' }}>👥</div>
              <div className="stat-content">
                <h3>Total Users</h3>
                <p className="stat-value">{stats.total_users}</p>
              </div>
            </div>
          )}
        </div>
      )}

      {stats && stats.recent_activities && Array.isArray(stats.recent_activities) && stats.recent_activities.length > 0 && (
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
                  <p className="activity-date">{new Date(activity.date).toLocaleDateString()}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );

  const renderContent = () => {
    // Show loading state while data is being fetched
    if (loading) {
      return (
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading data...</p>
        </div>
      );
    }

    switch (activeView) {
      case 'dashboard':
        return renderDashboard();
      case 'companies':
        return renderTable('Companies', companies, [
          { 
            key: 'avatar', 
            label: 'Logo',
            render: (item) => (
              <AvatarDisplay entityType="companies" entityId={item.id} size={40} />
            )
          },
          { key: 'name', label: 'Company Name' },
          { key: 'registration_number', label: 'Registration' },
          { key: 'contact_person', label: 'Contact Person' },
          { key: 'email', label: 'Email' },
          { key: 'phone', label: 'Phone' }
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
          { key: 'name', label: 'Location Name' },
          { key: 'address', label: 'Address' },
          { key: 'city', label: 'City' },
          { key: 'county', label: 'County' },
          { 
            key: 'coordinates', 
            label: 'Coordinates',
            render: (item) => item.latitude && item.longitude ? 
              `${item.latitude.toFixed(4)}, ${item.longitude.toFixed(4)}` : 'N/A'
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
              <AvatarDisplay entityType="providers" entityId={item.id} size={40} />
            )
          },
          { key: 'name', label: 'Provider Name' },
          { key: 'company_name', label: 'Company' },
          { key: 'contact_person', label: 'Contact Person' },
          { key: 'email', label: 'Email' },
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
          onDelete: (id) => handleDeleteEntity(id, 'providers'),
          onBulkEdit: () => handleBulkEdit('providers'),
          onBulkDelete: () => handleBulkDelete('providers'),
          onExport: () => handleExport('providers'),
          onImport: () => handleImport('providers')
        }, 'providers');
      case 'cabinets':
        return renderTable('Cabinets', cabinets, [
          { 
            key: 'avatar', 
            label: 'Logo',
            render: (item) => (
              <AvatarDisplay entityType="cabinets" entityId={item.id} size={40} />
            )
          },
          { key: 'name', label: 'Name' },
          { key: 'model', label: 'Model' }
        ], { 
          onAdd: () => handleAddEntity('cabinets'),
          onEdit: (item) => handleEditEntity(item, 'cabinets'),
          onDelete: (id) => handleDeleteEntity(id, 'cabinets'),
          onBulkEdit: () => handleBulkEdit('cabinets'),
          onBulkDelete: () => handleBulkDelete('cabinets'),
          onExport: () => handleExport('cabinets'),
          onImport: () => handleImport('cabinets')
        }, 'cabinets');
      case 'slots':
        return renderTable('Slot Machines', slotMachines, [
          { key: 'model', label: 'Model' },
          { key: 'serial_number', label: 'Serial Number' },
          { 
            key: 'provider_id', 
            label: 'Provider',
            render: (item) => {
              const provider = providers.find(p => p.id === item.provider_id);
              return provider ? provider.name : 'Unknown Provider';
            }
          },
          { key: 'invoice_number', label: 'Invoice Number' },
          { 
            key: 'denomination', 
            label: 'Denomination',
            render: (item) => `${item.denomination}€`
          },
          { 
            key: 'max_bet', 
            label: 'Max Bet',
            render: (item) => `${item.max_bet}€`
          },
          { 
            key: 'rtp', 
            label: 'RTP',
            render: (item) => `${item.rtp}%`
          },
          { key: 'gaming_places', label: 'Gaming Places' }
        ], { 
          onAdd: () => handleAddEntity('slots'),
          onEdit: (item) => handleEditEntity(item, 'slots'),
          onDelete: (id) => handleDeleteEntity(id, 'slots'),
          onBulkEdit: () => handleBulkEdit('slots'),
          onBulkDelete: () => handleBulkDelete('slots'),
          onExport: () => handleExport('slots'),
          onImport: () => handleImport('slots')
        }, 'slots');
      case 'gamemixes':
        return renderTable('Game Mixes', gameMixes, [
          { 
            key: 'avatar', 
            label: 'Avatar',
            render: (item) => (
              <AvatarDisplay entityType="game_mixes" entityId={item.id} size={40} />
            )
          },
          { key: 'name', label: 'Mix Name' },
          { key: 'description', label: 'Description' },
          { key: 'game_count', label: 'Game Count' },
          { 
            key: 'games', 
            label: 'Top Games',
            render: (item) => item.games.slice(0, 3).join(', ') + 
              (item.games.length > 3 ? '...' : '')
          }
        ], { 
          onAdd: () => handleAddEntity('gamemixes'),
          onEdit: (item) => handleEditEntity(item, 'gamemixes'),
          onDelete: (id) => handleDeleteEntity(id, 'gamemixes'),
          onBulkEdit: () => handleBulkEdit('gamemixes'),
          onBulkDelete: () => handleBulkDelete('gamemixes'),
          onExport: () => handleExport('gamemixes'),
          onImport: () => handleImport('gamemixes')
        }, 'gamemixes');
      case 'invoices':
        return renderTable('Invoices', invoices, [
          { key: 'invoice_number', label: 'Invoice Number' },
          { 
            key: 'issue_date', 
            label: 'Issue Date',
            render: (item) => new Date(item.issue_date).toLocaleDateString()
          },
          { 
            key: 'due_date', 
            label: 'Due Date',
            render: (item) => new Date(item.due_date).toLocaleDateString()
          },
          { 
            key: 'amount', 
            label: 'Amount',
            render: (item) => `${item.amount} ${item.currency}`
          },
          { key: 'description', label: 'Description' }
        ], { 
          onAdd: () => handleAddEntity('invoices'),
          onEdit: (item) => handleEditEntity(item, 'invoices'),
          onDelete: (id) => handleDeleteEntity(id, 'invoices'),
          onBulkEdit: () => handleBulkEdit('invoices'),
          onBulkDelete: () => handleBulkDelete('invoices'),
          onExport: () => handleExport('invoices'),
          onImport: () => handleImport('invoices')
        }, 'invoices');
      case 'onjn':
        return renderTable('ONJN Reports', onjnReports, [
          { key: 'report_number', label: 'Report Number' },
          { key: 'report_type', label: 'Type' },
          { 
            key: 'report_date', 
            label: 'Report Date',
            render: (item) => new Date(item.report_date).toLocaleDateString()
          },
          { 
            key: 'submission_date', 
            label: 'Submitted',
            render: (item) => item.submission_date ? 
              new Date(item.submission_date).toLocaleDateString() : 'Not submitted'
          }
        ], { 
          onAdd: () => handleAddEntity('onjn'),
          onEdit: (item) => handleEditEntity(item, 'onjn'),
          onDelete: (id) => handleDeleteEntity(id, 'onjn'),
          onBulkEdit: () => handleBulkEdit('onjn'),
          onBulkDelete: () => handleBulkDelete('onjn'),
          onExport: () => handleExport('onjn'),
          onImport: () => handleImport('onjn')
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
        }, 'legal');
      case 'users':
        return renderTable('Users', users, [
          { 
            key: 'avatar', 
            label: 'Avatar',
            render: (item) => (
              <AvatarDisplay entityType="users" entityId={item.id} size={40} />
            )
          },
          { key: 'username', label: 'Username' },
          { key: 'email', label: 'Email' },
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
        }, 'users');
      case 'metrology':
        return renderTable('Metrology', metrology, [
          { key: 'serial_number', label: 'Serial Number' },
          { key: 'certificate_number', label: 'Certificate Number' },
          { key: 'certificate_type', label: 'Certificate Type' },
          { key: 'issuing_authority', label: 'Issuing Authority' },
          { key: 'issue_date', label: 'Issue Date', render: (item) => item.issue_date ? new Date(item.issue_date).toLocaleDateString() : 'N/A' },
          { key: 'cvt_type', label: 'CVT Type' },
          { key: 'cvt_expiry_date', label: 'CVT Expiry Date', render: (item) => item.cvt_expiry_date ? new Date(item.cvt_expiry_date).toLocaleDateString() : 'N/A' },
          { key: 'description', label: 'Description' },
          { 
            key: 'created_at', 
            label: 'Created',
            render: (item) => new Date(item.created_at).toLocaleDateString()
          }
        ], { 
          onAdd: () => handleAddEntity('metrology'),
          onEdit: (item) => handleEditEntity(item, 'metrology'),
          onDelete: (id) => handleDeleteEntity(id, 'metrology'),
          onBulkEdit: () => handleBulkEdit('metrology'),
          onBulkDelete: () => handleBulkDelete('metrology'),
          onExport: () => handleExport('metrology'),
          onImport: () => handleImport('metrology')
        }, 'metrology');
      default:
        return renderDashboard();
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
    <div className={`app-layout ${darkMode ? 'dark' : 'light'}`}>
      {/* Header */}
      <div className="main-header">
        <div className="header-left">
          <span className="breadcrumb-text">
            {navigationItems.find(item => item.id === activeView)?.label || 'Dashboard'}
          </span>
        </div>
        <div className="header-right">
          <button 
            className="theme-toggle"
            onClick={() => setDarkMode(!darkMode)}
            title={darkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
          >
            {darkMode ? '☀️' : '🌙'}
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
              <span className="header-user-name">{user?.username}</span>
              <span className="header-user-role">{user?.role}</span>
            </div>
          </div>
          <button onClick={logout} className="header-logout-btn" title="Logout">
            🚪
          </button>
        </div>
      </div>

      {/* Layout Container */}
      <div className="layout-container">
        {/* Sidebar */}
        <div className="sidebar">
          <div className="sidebar-header">
            <div className="logo">
              <h2>CASHPOT</h2>
              <p>Gaming Management System</p>
            </div>
          </div>
        
        <nav className="sidebar-nav">
          {navigationItems.map(item => (
            <button
              key={item.id}
              className={`nav-item ${activeView === item.id ? 'active' : ''}`}
              onClick={() => setActiveView(item.id)}
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
              <span className="user-name">{user?.username}</span>
              <span className="user-role">{user?.role}</span>
            </div>
          </div>
          <button onClick={logout} className="logout-btn">
            🚪
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="main-content">
        <div className="content-header">
          <div className="breadcrumb">
            <span>{navigationItems.find(item => item.id === activeView)?.label || 'Dashboard'}</span>
          </div>
          <div className="header-actions">
            <span className="welcome-text">Welcome, {user?.username}</span>
          </div>
        </div>
        
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
        />
      )}

      {/* Bulk Edit Form Modal */}
      {showBulkEditForm && (
        <BulkEditForm
          entityType={bulkEditType}
          selectedItems={selectedItems}
          onSave={handleBulkEditSave}
          onClose={() => setShowBulkEditForm(false)}
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