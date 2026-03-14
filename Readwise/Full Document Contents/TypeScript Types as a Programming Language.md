---
created: 2026-03-14T09:49:40+00:00
modified: 2026-03-14T11:09:59+00:00
tags: [articles]
title: TypeScript Types as a Programming Language
---

## TypeScript Types as a Programming Language

![rw-book-cover](https://marmelab.com/_astro/cover-large.M4lQp-3S.jpg)

### Metadata

- Author: [[Thiery Michel]]
- Full Title: TypeScript Types as a Programming Language
- Category: articles
- Summary: The article shows that TypeScript types can act like functions and compute new types from other types. It demonstrates generics, constraints (extends), conditional types, infer, recursion, mapped types, and utility-like helpers. These features let you encode complex type-level logic for safer and more expressive code.
- URL: <https://marmelab.com/blog/2025/12/04/typescript-type-as-a-programming-language.html>

### Full Document

![TypeScript Types as a Programming Language](https://marmelab.com/_astro/cover-large.M4lQp-3S_ZNaXak.webp)

Did you know TypeScript is Turing complete? In this post, I will approach type definitions as writing a program. The goal is not to write Doom in TypeScript or perform math operations—those have already been done:

While those are impressive, they raise the question: Why? The goal is to become better at writing types by treating them like programs.

In TypeScript, you can define types that depend on other types. These work like functions: for a given input type, they produce an output type.

```
// The simplest function there is, identity:
const identity = (value) => value;
// becomes
type Identity<Type> = Type;
// and we can call it like this
type Result = Identity<number>;
// type Result = number

// A more complex one
const createObject = (a, b) => ({ a, b });
// becomes
type CreateObject<A, B> = { a: A, b: B };
// and can be called like this
type Result = CreateObject<string, boolean>;
// type Result = { a: string; b: boolean }
```

The `extends` keyword tells TypeScript that a type parameter must extend a given type, like typing function arguments.

```
type CreateObject<A extends string, B> = { a: A, b: B };
// A must be a string, otherwise we get an error
type Errored = CreateObject<number, boolean>;
// Type 'number' does not satisfy the constraint 'string'
type Result = CreateObject<'name', boolean>;
// type Result = { a: "name"; b: boolean; }
```

You can also provide a default type to your generic type function, just like you would with a function parameter.

```
type CreateObject<
  Key extends string = 'defaultName',
  Value = string
> = { [Key]: Value };
// Key and Value are optional now
type Result = CreateObject;
// type Result = { defaultName: string }
type Result2 = CreateObject<'name'>;
// type Result2 = { name: string; }
type Result3 = CreateObject<'name', boolean>;
// type Result3 = { name: boolean; }
```

With this, we can already create a generic CRUD type generator:

```
type Crud<Resource extends { id: string | number }> = {
  // Create takes all the fields except id
  create: (resource: Omit<Resource, 'id'>) => Resource;
  // Read takes an id and returns a resource or undefined
  getOne: (id: Resource['id']) => Resource | undefined;
  // Update takes an id and a partial resource (without id)
  // and returns a resource or undefined
  update: (
    id: Resource['id'],
    resource: Partial<Omit<Resource, 'id'>>
  ) => Resource | undefined;
  // Delete takes an id
  // and returns a boolean indicating if the resource was deleted
  delete: (id: Resource['id']) => boolean;
  // List takes a partial resource (without id) as a filter
  // and returns an array of resources
  getList: (filter: Partial<Omit<Resource, 'id'>>) => Resource[];
}
// Example usage
type User = { id: number; name: string; email: string };
type UserCrud = Crud<User>;
// type UserCrud = {
//     create: (resource: Omit<User, 'id'>) => User;
//     getOne: (id: number) => User | undefined;
//     update: (id: number, resource: Partial<Omit<User, 'id' >>) =>
//       User | undefined;
//     delete: (id: number) => boolean;
//     getList: (filter: Partial<Omit<User, 'id'>>) => User[];
// }
```

We have functions. Can we have conditions too? Yes, we can. By using the `extends` keyword to create conditions in type functions. `extends` tests if a type is part of another type. Then you use ternary syntax: `condition? trueCase: falseCase`.

```
type IsNumber<Value extends unknown> =
  Value extends number ? true : false;

type Result = IsNumber<7>
// type Result = true
type Result2 = IsNumber<'seven'>;
// type Result = false
```

Retrieving Event Type from an Event

```
type CreateEvent = {
  type: "create";
  payload: { name: string }
};
type UpdateEvent = {
  type: "update";
  payload: { id: number; name?: string }
};
type DeleteEvent = {
  type: "delete";
  payload: { id: number }
};
type UnknownEvent = unknown;

type Event = CreateEvent | UpdateEvent | DeleteEvent | UnknownEvent;

type InferEventType<T extends Event> = T extends CreateEvent
  ? "create"
  : T extends UpdateEvent
  ? "update"
  : T extends DeleteEvent
  ? "delete"
  : never;

// Example usage
type EventType = InferEventType<UpdateEvent>; // 'update'
type EventType2 = InferEventType<CreateEvent>; // 'create'
type EventType3 = InferEventType<DeleteEvent>; // 'delete'
type EventType4 = InferEventType<'An event'>; // never
```

The `infer` keyword creates a variable inside a type definition. It supports destructuring.

```
// First, use the infer keyword to destructure
// the first element of an array and then return it
type First<Element> =
  Element extends [infer FirstElement, ...any[]] ? FirstElement : never

// Example usage
type Result = First<[string, number, boolean]>;
// type Result = string
type Result2 = First<[]>;
// type Result2 = never
```

With `infer`, the Event example from the Conditional Types section can be simplified to:

```
type InferEventType<
  T extends Event
> = T extends { type: infer EventType } ? EventType : never;
// We define a variable EventType that extracts the type field from T.
// No need to check each event type separately.

// Example usage
type EventType = InferEventType<UpdateEvent>; // 'update'
type EventType2 = InferEventType<CreateEvent>; // 'create'
type EventType3 = InferEventType<DeleteEvent>; // 'delete'
type EventType4 = InferEventType<{}>; // never
```

A type can call itself, allowing you to create recursive types.

You can use recursion to type recursive data structures, like a tree:

```
type TreeNode<Value> = {
  value: Value;
  children?: TreeNode<Value>[];
}

type StringTree = TreeNode<string>;
const tree: StringTree = {
  value: 'root',
  children: [
    { value: 'child1' },
    { value: 'child2', children: [
        { value: 'grandchild1' }
      ] }
  ]
};
```

But you can also use recursion to iterate over an array. Let's implement a `Find` type that searches for a type in an array. It returns the type if found, otherwise `never`:

```
type Find<ArrayType extends unknown[], ValueType> =
  // Destructure the array into its first element and the rest
  ArrayType extends [infer First, ...infer Rest]
    // Check if the first element is of the type we are looking for
    ? First extends ValueType
      // If it is, return it
      ? First
      // Otherwise, recurse on the rest of the array
      : Find<Rest, ValueType>
    : never; // If the array is empty, return never

// Example usage with events
type EventsArray = [{
  type: 'create';
  payload: { name: string; };
}, {
  type: 'update';
  payload: { id: number; name?: string; };
}, {
  type: 'delete';
  payload: { id: number; };
}];

type CreateEvent = Find<
  EventsArray,
  { type: 'create'; payload: { name: string; }; }
>;
// type CreateEvent = { type: "create"; payload: { name: string; }; }
type UpdateEvent = Find<
  EventsArray,
  { type: 'update'; payload: { id: number; name?: string; }; }
>;
// type UpdateEvent = {
//   type: "update";
//   payload: { id: number; name?: string | undefined; };
// }
type DeleteEvent = Find<
  EventsArray,
  { type: 'delete'; payload: { id: number; }; }
>;
// type DeleteEvent = { type: "delete"; payload: { id: number; }; }
type UnknownEvent = Find<
  EventsArray,
  { type: 'unknown'; payload: {}; }
>;
// type UnknownEvent = never
```

You might wonder when this would be useful. Imagine a middleware system where middlewares modify operation results based on the operation argument. You know the middleware types and want to find the result type for a specific argument:

```
// Middleware type:
// takes an argument of type Arg and returns a result of type Result
type Middleware<Arg, Result> = (arg: Arg) => Result;

// Example middlewares
type Middlewares = [
  Middleware<
    { type: "getList"; withComments: true },
    { id: number; name: string; comments: string[] }[]
  >,
  Middleware<{ type: "getList" }, { id: number; name: string }[]>,
  Middleware<
    { type: "getOne"; withComments: true },
    { id: number; name: string; comments: string[] }
  >,
  Middleware<{ type: "getOne" }, { id: number; name: string }>
];

// Find the middleware with argument matching type Target
type FindMiddleware<Target> = Find<Middlewares, Middleware<Target, any>>;

// Get the result type of a middleware
type GetResult<MiddlewareInput extends Middleware<any, any>> =
  MiddlewareInput extends Middleware<any, infer Result> ? Result : never;

// Putting all pieces together
type GetMiddlewareResult<Arg> = GetResult<FindMiddleware<Arg>>;

type ListResult = GetMiddlewareResult<{ type: "getList" }>;
// type ListResult = { id: number; name: string; }[]

type OneResult = GetMiddlewareResult<{ type: "getOne" }>;
// type OneResult = { id: number; name: string; }

type ListWithCommentsResult = GetMiddlewareResult<{
  type: "getList";
  withComments: true;
}>;
// type ListWithCommentsResult = {
//   id: number;
//   name: string;
//   comments: string[]
// }[]

type OneWithCommentsResult = GetMiddlewareResult<{
  type: "getOne";
  withComments: true;
}>;
// type OneWithCommentsResult = {
//   id: number;
//   name: string;
//   comments: string[]
// }
```

TypeScript allows you to work with strings at the type level using template literals.

You can perform simple string concatenation:

```
type HelloWorld<Greeted extends string = 'world'> = `Hello ${Greeted}`

type DefaultResult = HelloWorld; // 'Hello world'
type Result = HelloWorld<'TypeScript'>; // 'Hello TypeScript'
```

You can also perform more complex string manipulations, such as removing all spaces from a string using the `infer` keyword and recursion:

```
type RemoveWhitespace<S extends string> =
  S extends `${infer First} ${infer Rest}`
    ? `${First}${RemoveWhitespace<Rest>}`
    : S;

type Result = RemoveWhitespace<'Hello   World  !'>;
// type Result = "HelloWorld!"
```

```
type Getter<Key extends string> = `get${Capitalize<Key>}`;
type Result = Getter<'name'>;
// type Result = "getName"
type Result2 = Getter<'firstName'>;
// type Result2 = "getFirstName"
```

> Note: `Capitalize` is a built-in utility type that capitalizes the first letter of a string type. You can implement it yourself using `Uppercase` and recursion:
>
>
> ```
> type Capitalize<
>   S extends string
> > = S extends `${infer First}${infer Rest}`
>   ? `${Uppercase<First>}${Rest}`
>   : S;
> // Uppercase is also a utility type
> // but it is implemented as compiler intrinsic magic.
> 
> // Example usage
> type Result = Capitalize<"hello">;
> // type Result = "Hello"
> ```

With recursion, we can loop over arrays, but how do we iterate over object properties? Mapped types allow you to create a new type by transforming each property of an existing type. Mapped types are built on the syntax of indexed access types and the `keyof` operator.

Indexed access types allow you to get the type of a property of an object type by using the syntax `Type[Key]`:

```
type User = { id: number; name: string; email: string };
type UserId = User['id'];
// type UserId = number
type UserName = User['name'];
// type UserName = string
```

They can also be used with a union of keys to get the union of the types of those keys:

The `keyof` operator allows you to get the union of all keys of a type.

```
type User = { id: number; name: string; email: string };
type UserKeys = keyof User;
// type UserKeys = "id" | "name" | "email"
```

Finally, by adding the `in` keyword, we can iterate over all keys of a type.

```
type UserPropertiesAsString = {
  // Here K is each key of User
  // and we map over it to create a function
  // that returns the type of the property (User[K])
  [K in keyof User]: () => User[K];
};
// type UserPropertiesAsString = {
//   id: () => number;
//   name: () => string;
//   email: () => string;
// }
```

With this, you can create a type that transforms all methods of an object so that they return a Promise.

```
type Promisify<R extends Record<string, (...args: any) => any>> = {
  [K in keyof R]:
    (...args: Parameters<R[K]>) => Promise<ReturnType<R[K]>>;
};

type Input = {
  getName: () => string;
  getById: (id: string) => { id: string; name: string };
};

type PromisifiedInput = Promisify<Input>;
// type PromisifiedInput = {
//     getName: () => Promise<string>;
//     getById: (id: string) => Promise<{
//         id: string;
//         name: string;
//     }>;
// }
```

Here is a more complex example of a mapped type: Let's take a resource type and a list of filter keys to generate `getByFilterType` methods for each filter key:

```
type Product = {
  id: number;
  name: string;
  quantity: number;
  inStock: boolean;
};
type CrudWithFilters<
  Resource extends { id: string | number },
  FilterKeys extends keyof Resource
> = {
  // getByFilter for each filter key
  [K in FilterKeys as `getBy${Capitalize<string & K>}`]:
    (value: Resource[K]) => Resource[];
}
type ProductCrudWithFilters = CrudWithFilters<
  Product,
  'name' | 'quantity' | 'inStock'
>;
// type ProductCrudWithFilters = {
//     getByName: (value: string) => Product[];
//     getByQuantity: (value: number) => Product[];
//     getByInStock: (value: boolean) => Product[];
// }

// Example usage with actual functions
const productCrud: CrudWithFilters<
  Product,
  'name' | 'quantity' | 'inStock'
> = {
  getByName: (name: string) => [
    { id: 1, name, quantity: 10, inStock: true }
  ],
  getByQuantity: (quantity: number) => [
    { id: 2, name: 'Product 2', quantity, inStock: false }
  ],
  getByInStock: (inStock: boolean) => [
    { id: 3, name: 'Product 3', quantity: 5, inStock }
  ],
};

// The type of productCrud is correctly inferred,
// and you will get type errors
// if your function implementation does not match the expected type.
const erroredProductCrud: CrudWithFilters<
  Product,
  'name' | 'quantity' | 'inStock'
> = {
  getByName: (name: number) => [
    { id: 1, name: 'Product 1', quantity: 10, inStock: true }
  ],
  // Type
  // '(name: number) => {
  //   id: number;
  //   name: string;
  //   quantity: number;
  //   inStock: true;
  // }[]'
  // is not assignable to type
  // '(value: string) => Product[]'.
  // Types of parameters 'name' and 'value' are incompatible.
  //   Type 'string' is not assignable to type 'number'.
  getByQuantity: (quantity: string) =>
    [{ id: 2, name: 'Product 2', quantity: 5, inStock: false }],
  // Type
  // '(quantity: string) => {
  //   id: number;
  //   name: string;
  //   quantity: number;
  //   inStock: false;
  // }[]'
  // is not assignable to type
  // '(value: number) => Product[]'.
  // Types of parameters 'quantity' and 'value' are incompatible.
  //   Type 'number' is not assignable to type 'string'
  getByInStock: (inStock: boolean) => 'not found',
  // Type
  // '(inStock: boolean) => string'
  // is not assignable to type
  // '(value: boolean) => Product[]'.
  // Type 'string' is not assignable to type 'Product[]'.
};
```

With keyof, we can return anything based on the shape of an object, not just an object. For example, here is a function that transforms an object of functions into a single function. It takes the object key as the first argument and the function arguments as the rest.

```
// First let's define our helpers:
// ObjToFunc take any object of functions
// and convert it into a single function
type ObjectToFunc<Obj extends Record<string, (...args: any) => any>> = {
  // it maps over the key of the object argument
  // and for each one define a function.
  <K extends keyof Obj>(key: K, ...args: Parameters<Obj[K]>): ReturnType<
    Obj[K]
  >;
};

// this result in an union type of function for each of the object key.
type Example = ObjectToFunc<
  {
    getStringLength: (s: string) => number;
    isEven: (n: number) => boolean;
  }
>
// type Example =
// | (key: getStringLength, s: string) => number
// | (key: isEven, n: number) => boolean;

// Now let's create the actual function

const transformObjectToFunction = <
  Obj extends Record<string, (...args: any) => any>
>(
  obj: Obj
): ObjectToFunc<Obj> => {
  return ((key: string, ...args: unknown[]) => {
    const func = obj[key];
    return func(...args);
  }) as ObjectToFunc<Obj>;
};

// Example usage: combining a collection of getList functions
// for different resources into a single getList function

const getList = transformObjectToFunction({
  authors: (filter: { name?: string }) => [
    { id: 1, name: "Author 1" },
    { id: 2, name: "Author 2" },
  ],
  posts: (filter: { authorId?: number; published?: boolean }) => [
    { id: 1, title: "A post" },
  ],

  comments: (filter: { postId?: number; authorId?: number }) => [
    { id: 1, content: "A comment" },
  ],
});

getList("posts", { authorId: 1 });
// No error
// Inferred as
// const getList: <"posts">(key: "posts", filter: {
//     authorId?: number;
//     published?: boolean;
// }) => {
//     id: number;
//     title: string;
// }[]
getList("posts", { name: 'Author 1' });
// Error: Object literal may only specify known properties,
// and name does not exist in type:
// { authorId?: number | undefined; published?: boolean | undefined; }
getList("authors", { name: "Author 1" });
// No error
// Inferred as
// const getList: <"authors">(key: "authors", filter: {
//     name?: string | undefined;
// }) => {
//     id: number;
//     name: string;
// }[]

```

> Note: The previous example use ReturnType and Parameters those are utility types provided by typescript. ReturnType return the type of the value returned by a given function type. If you are curious it can be reimplemented like this:
>
>
> ```
> type ReturnType<T extends (...args: any) => any> = T extends (
>   ...args: any
> ) => infer R
>   ? R
>   : any;
> ```
> Parameters return of the arguments of a given function type It can be reimplemented like this:
>
>
> ```
> type Parameters<T extends (...args: any) => any> = T extends (
>   ...args: infer P
> ) => any
>   ? P
>   : never;
> ```

By treating typescript type definition as a Programming language it is possible to define advanced generic types. Those generic types in turn allow for more generic code, reducing duplication and improving type safety across your codebase.

The key takeaways are:

- Generic types are functions that transform types
- Conditional types (`extends?:`) enable branching logic
- The `infer` keyword acts like variable assignment and allows to extract value from another like destructuring.
- Recursion allows iteration over arrays and complex types
- Template literals enable string manipulation at the type level
- Mapped types provide iteration over object properties

With these tools, you can create sophisticated type utilities that adapt to your needs, catch errors at compile time, and provide excellent autocomplete in your IDE. The next time you write a type definition, think of it as writing a program—because that's exactly what you're doing.

![Thiery Michel](https://marmelab.com/_astro/thiery.B8LndfaD_Z1mt6ME.webp)Thiery Michel
