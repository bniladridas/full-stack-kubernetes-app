# Full-Stack Kubernetes Application

## Project Overview
This is a full-stack web application demonstrating a modern microservices architecture with Docker and Kubernetes support.

### My Role and Contributions
As the lead developer, I have:
- Designed and implemented the full-stack application architecture
- Resolved critical database connection and authentication issues
- Optimized Docker configurations and deployment strategies
- Implemented robust error handling and logging mechanisms

### Technologies and Tools Used
- **Frontend**:
  - React.js
  - TypeScript
  - Nginx
  - Docker

- **Backend**:
  - FastAPI
  - SQLAlchemy
  - Pydantic
  - PostgreSQL
  - Python 3.9

- **DevOps**:
  - Docker
  - Docker Compose
  - Kubernetes (planned)
  - Prometheus Instrumentation

### Recent Fixes and Improvements
1. **Database Connection Issues**
   - Resolved authentication problems with PostgreSQL
   - Fixed permission issues for database user `myappuser`
   - Updated `pg_hba.conf` to use `scram-sha-256` authentication
   - Granted necessary schema privileges to the application user

2. **Configuration Management**
   - Improved environment variable handling
   - Enhanced error logging and diagnostics
   - Standardized database connection settings

### Issues Solved

| Issue | Complexity | Impact | Resolution Strategy |
|-------|------------|--------|---------------------|
| PostgreSQL Authentication Failure | High | Critical | Reconfigured `pg_hba.conf` to use `scram-sha-256` authentication |
| Database User Privilege Escalation | Medium | High | Updated `postgres-init.sh` to grant precise schema and table privileges |
| Environment Variable Configuration | Low | Medium | Standardized environment variable handling in `config.py` |
| Docker Compose Service Connectivity | Medium | High | Fixed Dockerfile paths and service dependencies |
| Backend Startup Configuration | Low | Medium | Corrected FastAPI app initialization using settings object |
| CORS and Security Middleware | Low | Medium | Implemented robust CORS and authentication middleware |
| Logging and Error Handling | Medium | High | Enhanced logging configuration and error tracking |

#### Complexity and Impact Legend
- **Complexity**: Low (1-3 days), Medium (4-7 days), High (8+ days)
- **Impact**: Low (minor functionality), Medium (significant feature), High (critical system functionality)

### Prerequisites
- Docker
- Docker Compose
- Git
- Web browser

### Setup and Installation

#### Clone the Repository
```bash
git clone https://github.com/bniladridas/full-stack-kubernetes-app.git
cd full-stack-kubernetes-app
```

#### Environment Configuration
1. Ensure Docker and Docker Compose are installed
2. No additional configuration required - uses default environment variables

#### Running the Application
```bash
# Start all services
docker-compose up -d --build

# View logs
docker-compose logs backend
```

#### Accessing the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs

### Troubleshooting
- Check Docker logs for detailed error messages
- Ensure all environment variables are correctly set
- Verify network connectivity between services

### Future Roadmap
- Kubernetes deployment
- Enhanced authentication
- Advanced monitoring and logging
- Continuous Integration/Continuous Deployment (CI/CD) pipeline
