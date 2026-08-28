import type { ApiClient } from '../types/api';
import { MockApi } from './mockApi';
import { RealApi } from './realApi';
export const api: ApiClient = import.meta.env.VITE_API_MODE === 'real' ? new RealApi() : new MockApi();
export const apiMode = import.meta.env.VITE_API_MODE === 'real' ? 'real' : 'mock';
