# Portfolio Backend Integration Contracts

## Overview
This document outlines the API contracts and integration strategy for transforming the static portfolio into a dynamic full-stack application.

## Current Mock Data Structure
Located in `/app/frontend/src/data/mock.js`:
- **Hero Data**: Name, tagline, profile image
- **About**: Bio text
- **Skills**: Categorized technical skills
- **Projects**: Detailed project showcases with images, tech stacks, features
- **Certificates**: Achievement records with descriptions
- **Education**: Academic background with grades
- **Contact**: Email, phone, social links

## Database Models

### 1. Profile Model
```javascript
{
  _id: ObjectId,
  name: String,
  tagline: String,
  bio: String,
  profileImageUrl: String,
  contact: {
    email: String,
    phone: String,
    github: String,
    linkedin: String
  },
  createdAt: Date,
  updatedAt: Date
}
```

### 2. Skills Model
```javascript
{
  _id: ObjectId,
  categories: [{
    name: String,
    items: [String],
    order: Number
  }],
  updatedAt: Date
}
```

### 3. Projects Model
```javascript
{
  _id: ObjectId,
  title: String,
  status: String, // "Completed", "Active", "In Progress"
  description: String,
  imageUrl: String,
  techStack: [String],
  features: [String],
  outcome: String,
  githubLink: String,
  liveDemo: String,
  order: Number,
  featured: Boolean,
  createdAt: Date,
  updatedAt: Date
}
```

### 4. Certificates Model
```javascript
{
  _id: ObjectId,
  title: String,
  issuer: String,
  year: String,
  description: String,
  order: Number,
  createdAt: Date
}
```

### 5. Education Model
```javascript
{
  _id: ObjectId,
  degree: String,
  institution: String,
  period: String,
  grade: String,
  location: String,
  order: Number,
  createdAt: Date
}
```

## API Endpoints

### Profile Endpoints
- `GET /api/profile` - Get profile information
- `PUT /api/profile` - Update profile information

### Skills Endpoints
- `GET /api/skills` - Get all skill categories
- `PUT /api/skills` - Update skills data

### Projects Endpoints
- `GET /api/projects` - Get all projects (query: ?featured=true)
- `GET /api/projects/:id` - Get specific project
- `POST /api/projects` - Create new project
- `PUT /api/projects/:id` - Update project
- `DELETE /api/projects/:id` - Delete project

### Certificates Endpoints
- `GET /api/certificates` - Get all certificates
- `POST /api/certificates` - Create new certificate
- `PUT /api/certificates/:id` - Update certificate
- `DELETE /api/certificates/:id` - Delete certificate

### Education Endpoints
- `GET /api/education` - Get education records
- `POST /api/education` - Create education record
- `PUT /api/education/:id` - Update education record
- `DELETE /api/education/:id` - Delete education record

## Frontend Integration Strategy

### 1. Data Service Layer
Create `/app/frontend/src/services/api.js`:
```javascript
const API_BASE = process.env.REACT_APP_BACKEND_URL + '/api';

export const portfolioAPI = {
  getProfile: () => fetch(`${API_BASE}/profile`),
  getSkills: () => fetch(`${API_BASE}/skills`),
  getProjects: () => fetch(`${API_BASE}/projects`),
  getCertificates: () => fetch(`${API_BASE}/certificates`),
  getEducation: () => fetch(`${API_BASE}/education`)
};
```

### 2. Replace Mock Data
- Remove import of `mock.js` from Portfolio component
- Replace static data with API calls using React hooks
- Add loading states and error handling
- Implement data caching for better performance

### 3. State Management
Use React hooks for state management:
- `useState` for component state
- `useEffect` for data fetching
- Custom hooks for API integration

## Implementation Phases

### Phase 1: Backend API Development
1. Create database models with Mongoose
2. Implement CRUD endpoints for all resources
3. Add data validation and error handling
4. Seed database with current mock data

### Phase 2: Frontend Integration
1. Create API service layer
2. Replace mock data with API calls
3. Add loading states and error handling
4. Implement data refresh mechanisms

### Phase 3: Dynamic Features
1. Add admin interface for content management (optional)
2. Implement image upload for projects
3. Add analytics tracking
4. Performance optimization

## Data Migration
1. Transform current mock data into database seed files
2. Create migration scripts to populate initial data
3. Ensure data consistency between mock and database

## Error Handling Strategy
- Frontend: Graceful fallbacks to cached/default data
- Backend: Comprehensive error responses with status codes
- Logging: Track API usage and errors for debugging

## Performance Considerations
- Database indexing on frequently queried fields
- API response caching
- Image optimization for project showcases
- Lazy loading for non-critical sections

## Security Measures
- Input validation and sanitization
- CORS configuration for frontend origin
- Rate limiting on API endpoints
- Secure headers implementation

This contract ensures seamless integration between the existing frontend and the new backend, maintaining the portfolio's professional appearance while adding dynamic capabilities.