# .NET Beginner’s Cheat Sheet (for Experienced Programmers)

## What “.NET” actually is (first misconception killer)

**.NET is not a language.**  
It’s a **runtime + standard library + tooling ecosystem**.

Think:

- JVM ≈ .NET runtime
    
- Java/Kotlin ≈ C#/F#
    
- Maven/Gradle ≈ dotnet CLI + NuGet
    

---

## Core components

### 1. .NET Runtime

Executes compiled code.

- **CLR** (Common Language Runtime)
    
- Handles:
    
    - Memory management (GC)
        
    - Type safety
        
    - JIT compilation
        
    - Security boundaries
        

You compile → IL (Intermediate Language) → JIT → native code.

---

### 2. Languages

Most common:

- **C#** → primary, modern, expressive
    
- F# → functional-first
    
- VB.NET → legacy but supported
    

C# is the default choice unless you have a reason not to.

---

### 3. Base Class Library (BCL)

The standard library.

Examples:

- `System`
    
- `System.IO`
    
- `System.Net.Http`
    
- `System.Threading.Tasks`
    
- `System.Collections.Generic`
    

If you’re looking for “how do I do X?” — start here before NuGet.

---

## The dotnet CLI (you live here)

### Create projects

`dotnet new console dotnet new webapi dotnet new classlib dotnet new xunit`

Templates define:

- Project structure
    
- Default dependencies
    
- Build config
    

---

### Build & run

`dotnet build dotnet run dotnet test dotnet publish`

No IDE dependency. Visual Studio is optional.

---

## Project anatomy (.csproj)

Modern .NET uses **SDK-style projects**.

Example:

`<Project Sdk="Microsoft.NET.Sdk">   <PropertyGroup>     <TargetFramework>net8.0</TargetFramework>     <Nullable>enable</Nullable>     <ImplicitUsings>enable</ImplicitUsings>   </PropertyGroup> </Project>`

Key ideas:

- XML is minimal
    
- Convention over configuration
    
- Dependencies are resolved automatically
    

---

## Solution vs Project

- **Project (.csproj)** → one buildable unit
    
- **Solution (.sln)** → container for projects
    

Typical layout:

`MyApp.sln /src   MyApp.Api   MyApp.Core   MyApp.Infrastructure /tests   MyApp.Tests`

---

## Program entry point (modern .NET)

Old:

`static void Main(string[] args)`

New:

`Console.WriteLine("Hello World");`

This is **top-level statements**.  
Compiler generates `Main` for you.

---

## Types & OOP basics (with .NET flavor)

### Classes

`class Device {     public string Name { get; set; } }`

### Records (value semantics)

`record Device(string Name);`

Records:

- Immutable by default
    
- Structural equality
    
- Excellent for DTOs
    

---

### Interfaces

`interface IDeviceService {     Device Get(string id); }`

Convention:

- Interfaces start with `I`
    

---

### Inheritance & polymorphism

`abstract class Device {     public abstract void Activate(); }  class Laptop : Device {     public override void Activate() {} }`

.NET strongly encourages **composition + interfaces** over deep inheritance.

---

## Dependency Injection (first-class citizen)

Built-in DI container.

`builder.Services.AddScoped<IDeviceService, DeviceService>();`

Lifetimes:

- `Singleton` → one instance
    
- `Scoped` → per request
    
- `Transient` → every resolution
    

DI is not optional in real .NET apps — it’s the backbone.

---

## Async is the default

`async Task<Device> GetAsync() {     await Task.Delay(100);     return new Device(); }`

Rules:

- Async all the way down
    
- Avoid `.Result` and `.Wait()`
    
- `Task` ≠ thread
    

---

## HTTP & APIs (ASP.NET Core)

### Minimal API

`app.MapGet("/devices", () => devices);`

### Controller-based

`[ApiController] [Route("api/devices")] class DevicesController : ControllerBase {     [HttpGet]     public IActionResult Get() => Ok(); }`

Minimal APIs are now preferred for simple services.

---

## Configuration

Uses layered providers:

- appsettings.json
    
- appsettings.{Environment}.json
    
- Environment variables
    
- Key Vault
    
- Command-line
    

`builder.Configuration["MySetting"];`

Strongly-typed config:

`builder.Services.Configure<MyOptions>(     builder.Configuration.GetSection("MyOptions"));`

---

## Logging

Built-in abstractions:

`ILogger<MyClass> logger; logger.LogInformation("Hello");`

Pluggable backends:

- Console
    
- Application Insights
    
- Seq
    
- OpenTelemetry
    

---

## NuGet (package management)

`dotnet add package Newtonsoft.Json dotnet list package`

NuGet ≈ npm + Maven hybrid.

Avoid dependency sprawl — .NET’s BCL is large for a reason.

---

## Testing

xUnit example:

`[Fact] public void AddsNumbers() {     Assert.Equal(4, Add(2,2)); }`

Testing is deeply integrated with CLI and CI.

---

## Memory & performance notes

- GC is generational
    
- Value types (`struct`) vs reference types (`class`) matter
    
- `Span<T>` / `Memory<T>` for high-performance work
    
- Avoid premature optimization — .NET is fast by default
    

---

## Cross-platform reality

.NET runs on:

- Windows
    
- Linux
    
- macOS
    
- Containers
    
- Azure App Service
    
- Azure Container Apps
    
- Azure Functions
    

Same binaries. Same code.

---

## Typical .NET app stack (modern)

- ASP.NET Core
    
- EF Core or Dapper
    
- Managed Identity
    
- OpenAPI / Swagger
    
- CI via GitHub Actions or Azure DevOps
    
- Deployed to App Service / Containers
    

---

## Common beginner traps (even for good programmers)

- Overusing inheritance
    
- Fighting DI instead of embracing it
    
- Writing synchronous code in async apps
    
- Treating .NET like Java 8-era Java
    
- Ignoring nullable reference types
    

---

## Mental model to keep

> .NET is opinionated about **structure**, not creativity.

Once you learn the conventions:

- You write less code
    
- You wire less infrastructure
    
- You focus on business logic
    

---

## Where to go next (learning order)

1. C# language depth (records, pattern matching)
    
2. ASP.NET Core request pipeline
    
3. Dependency injection deeply
    
4. Async internals
    
5. Identity (Entra ID + OAuth)
    
6. Containers & cloud deployment