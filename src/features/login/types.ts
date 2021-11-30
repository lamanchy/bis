import { existingRoles } from './RoleSwitch'

export type Credentials =
  | { username: string; password: string }
  | { email: string; password: string }

export type Role = keyof typeof existingRoles