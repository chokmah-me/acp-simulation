# Modern Architecture Patterns

## Core Principles

1. **Feature-based module structure** - Vertical slicing by domain
2. **Layered architecture** - Separation of concerns (Route → Manager → Database)
3. **Functional composition** - Functions over classes
4. **Result monads** - Type-safe error handling
5. **Configuration-driven** - Extract business logic to config files

## Module Structure

### Standard Feature Layout

```
src/features/
  ├── user-management/
  │   ├── manager.ts           # Business logic layer
  │   ├── endpoint.ts          # API routes/handlers
  │   ├── database.ts          # Data access layer
  │   ├── types.ts             # Domain types
  │   ├── config.ts            # Feature configuration
  │   └── tests/
  │       ├── manager.test.ts
  │       └── endpoint.test.ts
```

### Layer Responsibilities

**endpoint.ts** (API Layer)
- Express/Discord route definitions
- Request validation
- Response formatting
- Call manager functions
- NO business logic

**manager.ts** (Business Logic Layer)
- Core feature logic
- Orchestrate operations
- Call database functions
- Return Result<T, E>
- NO direct HTTP/DB concerns

**database.ts** (Data Access Layer)
- Database queries
- Data transformation
- Connection handling
- Return Result<T, E>
- NO business logic

### Example Implementation

**database.ts:**
```typescript
import { ok, err, Result } from '../../common/errors/result';
import type { User, UserId } from './types';

export function createUserDatabase(db: DatabaseConnection) {
  return {
    async getUser(id: UserId): Promise<Result<User, Error>> {
      try {
        const user = await db.query('SELECT * FROM users WHERE id = $1', [id]);
        if (!user) {
          return err(new Error(`User ${id} not found`));
        }
        return ok(user);
      } catch (e) {
        return err(new Error(`Database error: ${e.message}`));
      }
    },

    async createUser(data: Omit<User, 'id'>): Promise<Result<User, Error>> {
      try {
        const user = await db.insert('users', data);
        return ok(user);
      } catch (e) {
        return err(new Error(`Failed to create user: ${e.message}`));
      }
    }
  };
}
```

**manager.ts:**
```typescript
import { ok, err, Result } from '../../common/errors/result';
import type { User, CreateUserData } from './types';
import type { UserDatabase } from './database';

export function createUserManager(userDb: UserDatabase) {
  return {
    async registerUser(data: CreateUserData): Promise<Result<User, Error>> {
      // Business logic: validate data
      if (!data.email || !data.email.includes('@')) {
        return err(new Error('Invalid email address'));
      }

      // Check if user exists
      const existingUser = await userDb.getUserByEmail(data.email);
      if (existingUser.ok) {
        return err(new Error('User already exists'));
      }

      // Create user
      return userDb.createUser(data);
    },

    async getUser(id: string): Promise<Result<User, Error>> {
      return userDb.getUser(id);
    }
  };
}
```

**endpoint.ts:**
```typescript
import { Router } from 'express';
import type { UserManager } from './manager';

export function createUserEndpoints(userManager: UserManager) {
  const router = Router();

  router.post('/users', async (req, res) => {
    const result = await userManager.registerUser(req.body);

    if (result.ok) {
      res.status(201).json(result.value);
    } else {
      res.status(400).json({ error: result.error.message });
    }
  });

  router.get('/users/:id', async (req, res) => {
    const result = await userManager.getUser(req.params.id);

    if (result.ok) {
      res.json(result.value);
    } else {
      res.status(404).json({ error: result.error.message });
    }
  });

  return router;
}
```

## Result Monad Pattern

### Basic Usage

```typescript
import { ok, err, Result } from '../common/errors/result';

// Define return type
function divide(a: number, b: number): Result<number, Error> {
  if (b === 0) {
    return err(new Error('Division by zero'));
  }
  return ok(a / b);
}

// Use the result
const result = divide(10, 2);
if (result.ok) {
  console.log('Success:', result.value); // 5
} else {
  console.error('Error:', result.error.message);
}
```

### Chaining Results

```typescript
async function getUserProfile(userId: string): Promise<Result<UserProfile, Error>> {
  const userResult = await getUser(userId);
  if (!userResult.ok) {
    return err(userResult.error);
  }

  const settingsResult = await getUserSettings(userId);
  if (!settingsResult.ok) {
    return err(settingsResult.error);
  }

  return ok({
    user: userResult.value,
    settings: settingsResult.value
  });
}
```

### Result Helpers

```typescript
// Unwrap with default
function getValueOrDefault<T>(result: Result<T, Error>, defaultValue: T): T {
  return result.ok ? result.value : defaultValue;
}

// Map over result
function mapResult<T, U>(
  result: Result<T, Error>,
  fn: (value: T) => U
): Result<U, Error> {
  return result.ok ? ok(fn(result.value)) : result;
}

// Usage
const doubled = mapResult(divide(10, 2), x => x * 2);
```

## Functional Composition

### Replace Class Inheritance

**❌ Old Pattern (Class Inheritance):**
```typescript
class BaseService {
  constructor(protected db: Database) {}

  protected async query(sql: string) {
    return this.db.execute(sql);
  }
}

class UserService extends BaseService {
  async getUser(id: string) {
    return this.query(`SELECT * FROM users WHERE id = '${id}'`);
  }
}
```

**✅ New Pattern (Function Composition):**
```typescript
// Composable query function
function createQueryExecutor(db: Database) {
  return async (sql: string, params: unknown[]) => {
    return db.execute(sql, params);
  };
}

// User service as composed functions
function createUserService(db: Database) {
  const query = createQueryExecutor(db);

  return {
    async getUser(id: string) {
      return query('SELECT * FROM users WHERE id = $1', [id]);
    }
  };
}
```

### Higher-Order Functions

```typescript
// Decorator pattern with functions
function withLogging<T extends (...args: any[]) => any>(fn: T): T {
  return ((...args: any[]) => {
    console.log(`Calling ${fn.name} with`, args);
    const result = fn(...args);
    console.log(`Result:`, result);
    return result;
  }) as T;
}

// Use it
const loggedGetUser = withLogging(getUser);
```

### Pipe/Compose Utilities

```typescript
// Pipe: left to right
function pipe<T>(...fns: Array<(arg: T) => T>) {
  return (value: T) => fns.reduce((acc, fn) => fn(acc), value);
}

// Compose: right to left
function compose<T>(...fns: Array<(arg: T) => T>) {
  return (value: T) => fns.reduceRight((acc, fn) => fn(acc), value);
}

// Usage
const processUser = pipe(
  validateUser,
  normalizeData,
  enrichWithDefaults,
  formatForDisplay
);

const user = processUser(rawUserData);
```

## Configuration-Driven Logic

### Extract Business Rules to Config

**❌ Hardcoded Logic:**
```typescript
function calculateDiscount(user: User, amount: number): number {
  if (user.isPremium) {
    if (amount > 100) {
      return amount * 0.20;
    }
    return amount * 0.10;
  }
  return 0;
}
```

**✅ Configuration-Driven:**
```typescript
// config.ts
export const discountRules = [
  {
    condition: (user: User, amount: number) => user.isPremium && amount > 100,
    discount: 0.20
  },
  {
    condition: (user: User, amount: number) => user.isPremium,
    discount: 0.10
  },
  {
    condition: () => true,
    discount: 0
  }
];

// logic.ts
function calculateDiscount(user: User, amount: number): number {
  const rule = discountRules.find(r => r.condition(user, amount));
  return amount * (rule?.discount ?? 0);
}
```

## Dependency Injection

### Factory Functions

```typescript
// Dependencies
interface Dependencies {
  db: Database;
  logger: Logger;
  config: Config;
}

// Create feature with injected dependencies
export function createUserFeature(deps: Dependencies) {
  const database = createUserDatabase(deps.db);
  const manager = createUserManager(database, deps.logger);
  const endpoints = createUserEndpoints(manager);

  return {
    database,
    manager,
    endpoints
  };
}

// Bootstrap
const userFeature = createUserFeature({
  db: databaseConnection,
  logger: appLogger,
  config: appConfig
});
```

## Migration Strategy

### From Monolith to Features

**Step 1: Identify feature boundaries**
```
Current: chatbot.ts (3000 lines)
Target:
  - src/features/chat/
  - src/features/commands/
  - src/features/conversation/
```

**Step 2: Extract one function at a time**
```
1. Extract pure functions first (no dependencies)
2. Then functions with minimal dependencies
3. Finally, stateful/complex functions
```

**Step 3: Maintain backwards compatibility**
```typescript
// Old file (chatbot.ts)
import { handleMessage } from './features/chat/manager';

// Keep old export, delegate to new
export function processMessage(msg: Message) {
  return handleMessage(msg); // Delegate to new location
}
```

**Step 4: Update imports gradually**
```
1. Extract module
2. Re-export from old location
3. Update imports file-by-file
4. Remove re-export when all imports updated
```

## Testing Patterns

### Test Pure Functions

```typescript
// Easy to test (pure)
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// Test
expect(calculateTotal([{ price: 10 }, { price: 20 }])).toBe(30);
```

### Test with Dependency Injection

```typescript
// manager.test.ts
const mockDb = {
  getUser: jest.fn().mockResolvedValue(ok({ id: '1', name: 'Test' }))
};

const manager = createUserManager(mockDb);
const result = await manager.getUser('1');

expect(result.ok).toBe(true);
expect(mockDb.getUser).toHaveBeenCalledWith('1');
```

## Common Mistakes to Avoid

1. **Mixing layers** - Don't put business logic in endpoints
2. **Not using Result** - Always wrap errors in Result<T,E>
3. **Large managers** - Split into smaller, focused managers
4. **Tight coupling** - Use dependency injection
5. **Missing types** - Every public function needs types
6. **Skipping tests** - Test business logic thoroughly

## Refactoring Checklist

When extracting to modern patterns:

- [ ] Created feature directory under `src/features/`
- [ ] Separated into manager/endpoint/database layers
- [ ] All functions return Result<T,E>
- [ ] No business logic in endpoint.ts
- [ ] No HTTP concerns in manager.ts
- [ ] No business logic in database.ts
- [ ] Types defined in types.ts
- [ ] Configuration extracted to config.ts
- [ ] Unit tests for manager functions
- [ ] Integration tests for endpoints
- [ ] JSDoc comments on all exports
- [ ] Updated imports in calling code
