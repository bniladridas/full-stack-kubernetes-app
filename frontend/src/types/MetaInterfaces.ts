// Interfaces for Meta Information

// System Diagnostics Interface
export interface SystemDiagnostics {
  python_version: string;
  os: {
    system: string;
    release: string;
    machine: string;
  };
  cpu: {
    cores: number;
    usage_percent: number;
  };
  memory: {
    total: number;
    available: number;
    percent_used: number;
  };
}

// Environment Information Interface
export interface EnvironmentInfo {
  debug: string;
  cors_origins: string[];
}

// Health Check Interface
export interface HealthCheckResponse {
  status: 'healthy' | 'unhealthy';
  application_name: string;
  version: string;
  database_status: string;
  timestamp: string;
  environment: EnvironmentInfo;
  system_diagnostics: SystemDiagnostics;
}

// User Metadata Interface
export interface UserMetadata {
  id?: number;
  username: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  last_login?: Date;
  created_at?: Date;
}

// Application Metadata Interface
export interface ApplicationMetadata {
  name: string;
  version: string;
  environment: 'development' | 'staging' | 'production';
  build_timestamp: string;
  dependencies?: string[];
}

// Authentication Metadata Interface
export interface AuthMetadata {
  token_type: string;
  access_token: string;
  expires_at?: Date;
  permissions?: string[];
}

// Comprehensive Metadata Interface
export interface AppMetadata {
  user?: UserMetadata;
  health?: HealthCheckResponse;
  application?: ApplicationMetadata;
  auth?: AuthMetadata;
}
