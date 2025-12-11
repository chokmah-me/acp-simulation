# TypeScript Style Guide for Refactoring

## Core Principles
- Prefer functional composition over class inheritance
- Use strict typing (no `any` types)
- Immutable data structures where possible
- Pure functions for business logic

## Async Patterns

### Always Use async/await Over .then() Chains

**❌ Avoid:**
```typescript
function getData() {
  return fetch('/api/data')
    .then(res => res.json())
    .then(data => process(data))
    .catch(err => console.error(err));
}
```

**✅ Prefer:**
```typescript
async function getData() {
  try {
    const res = await fetch('/api/data');
    const data = await res.json();
    return process(data);
  } catch (err) {
    // Use Result monad instead (see Error Handling section)
    throw err;
  }
}
```

## Error Handling

### Use Result<T, E> Monads

Wrap errors in Result types instead of try/catch in business logic.

**Pattern:**
```typescript
import { ok, err, Result } from '../common/errors/result';

function riskyOperation(input: string): Result<Data, Error> {
  if (!input) {
    return err(new Error('Input is required'));
  }

  try {
    const result = performOperation(input);
    return ok(result);
  } catch (e) {
    return err(e instanceof Error ? e : new Error(String(e)));
  }
}

// Usage
const result = riskyOperation(input);
if (result.ok) {
  console.log(result.value);
} else {
  console.error(result.error);
}
```

### Where to Use try/catch

Only use try/catch at system boundaries:
- API route handlers
- Database connection layers
- External service calls
- Top-level application entry points

**Business logic should use Result monads.**

## Function Composition

### Replace Classes with Functions

**❌ Avoid:**
```typescript
class UserService {
  constructor(private db: Database) {}

  async getUser(id: string) {
    return this.db.query('users', { id });
  }

  async updateUser(id: string, data: Partial<User>) {
    return this.db.update('users', id, data);
  }
}
```

**✅ Prefer:**
```typescript
// Factory function pattern
function createUserService(db: Database) {
  return {
    async getUser(id: string) {
      return db.query('users', { id });
    },

    async updateUser(id: string, data: Partial<User>) {
      return db.update('users', id, data);
    }
  };
}

// Or pure functions
async function getUser(db: Database, id: string) {
  return db.query('users', { id });
}
```

### Use Higher-Order Functions

**Pattern:**
```typescript
// Compose operations
const processData = pipe(
  validateInput,
  transformData,
  enrichWithMetadata,
  formatOutput
);

// Use map/filter/reduce over loops
const activeUsers = users
  .filter(u => u.isActive)
  .map(u => ({ id: u.id, name: u.name }));
```

## Documentation

### JSDoc for All Exported Functions

**Required format:**
```typescript
/**
 * Calculates the total price including tax
 * @param subtotal - Price before tax in cents
 * @param taxRate - Tax rate as decimal (e.g., 0.08 for 8%)
 * @returns Total price in cents
 * @throws {Error} If subtotal is negative
 */
export function calculateTotal(subtotal: number, taxRate: number): number {
  if (subtotal < 0) {
    throw new Error('Subtotal cannot be negative');
  }
  return Math.round(subtotal * (1 + taxRate));
}
```

### Inline Comments for Complex Logic

Use inline comments sparingly, only for non-obvious logic:

```typescript
// Use binary search since array is sorted by timestamp
const index = binarySearch(events, targetTime);

// Cache result for 5 minutes (300000ms)
cache.set(key, value, 300000);
```

## Type Safety

### No `any` Types

**❌ Avoid:**
```typescript
function processData(data: any) {
  return data.map((item: any) => item.value);
}
```

**✅ Prefer:**
```typescript
interface DataItem {
  value: number;
  label: string;
}

function processData(data: DataItem[]): number[] {
  return data.map(item => item.value);
}

// If truly unknown, use `unknown`
function processData(data: unknown): number[] {
  if (!Array.isArray(data)) {
    throw new Error('Data must be an array');
  }
  return data.map(item => {
    if (typeof item === 'object' && item !== null && 'value' in item) {
      return item.value as number;
    }
    throw new Error('Invalid item structure');
  });
}
```

### Use `satisfies` Operator

For objects that need both type checking and inference:

```typescript
const config = {
  timeout: 5000,
  retries: 3,
  endpoint: '/api/data'
} satisfies Config;

// TypeScript knows exact keys, not just Config type
config.timeout; // OK
config.unknown; // Error
```

## Null Handling

### Proper Null Checks

**❌ Avoid:**
```typescript
if (user) {
  console.log(user.name);
}
```

**✅ Prefer:**
```typescript
if (user !== null && user !== undefined) {
  console.log(user.name);
}

// Or use optional chaining
console.log(user?.name);

// Or nullish coalescing
const name = user?.name ?? 'Anonymous';
```

## String Handling

### Template Literals Over Concatenation

**❌ Avoid:**
```typescript
const message = 'Hello, ' + user.name + '! You have ' + count + ' messages.';
```

**✅ Prefer:**
```typescript
const message = `Hello, ${user.name}! You have ${count} messages.`;
```

## Modern Array Methods

### Prefer Declarative Over Imperative

**❌ Avoid:**
```typescript
const result = [];
for (let i = 0; i < users.length; i++) {
  if (users[i].isActive) {
    result.push(users[i].name);
  }
}
```

**✅ Prefer:**
```typescript
const result = users
  .filter(user => user.isActive)
  .map(user => user.name);
```

## Imports

### Organize Imports by Type

```typescript
// External dependencies first
import { Client } from 'discord.js';
import express from 'express';

// Internal modules second
import { createUserService } from './services/user';
import { logger } from './utils/logger';

// Types last
import type { User, Config } from './types';
```

## Naming Conventions

- **Variables/Functions**: camelCase (`getUserById`, `isActive`)
- **Classes/Interfaces/Types**: PascalCase (`UserService`, `ApiResponse`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_RETRIES`, `API_ENDPOINT`)
- **Private fields**: prefix with `_` (`_internalCache`)
- **Boolean variables**: prefix with `is`, `has`, `should` (`isActive`, `hasPermission`)

## File Organization

```typescript
// 1. Imports
import { thing } from './other';

// 2. Types/Interfaces
interface Config {
  timeout: number;
}

// 3. Constants
const DEFAULT_TIMEOUT = 5000;

// 4. Helper functions (not exported)
function formatData(data: unknown) {
  // ...
}

// 5. Main exported functions
export function mainFunction() {
  // ...
}

// 6. Default export (if needed)
export default mainFunction;
```

## When to Extract

Extract code into a new module when:
- Function exceeds 50 lines
- Logic is reused in 2+ places
- Function has 4+ parameters (consider object parameter)
- Function does multiple unrelated things
- Code has complex logic that needs dedicated testing

## Testing Considerations

Write functions that are easy to test:
- Pure functions (same input → same output)
- Inject dependencies (don't hard-code)
- Single responsibility
- Avoid side effects in business logic
