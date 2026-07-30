#azure, #python, #CSharp

# Accessing stdout and stderr Programmatically (C# and Python)

**Tags:** #csharp #python #subprocess #azure-learning #dev-notes  
**Date:** 2026-04-08

---

## Overview

Both C# and Python allow you to read and write to `stdout` and `stderr` — either for your own process or for child processes you launch. The core use cases are:

- Writing diagnostic/error output from your own app
- Capturing output from external tools or scripts
- Streaming output in real time without waiting for a process to finish

---

## Python

### Writing to Your Own Streams

```python
import sys

# Write to stdout and stderr
sys.stdout.write("This goes to stdout\n")
sys.stderr.write("This goes to stderr\n")

# print() defaults to stdout
print("stdout message")
print("stderr message", file=sys.stderr)
```

---

### Capture Output from a Child Process

Use `subprocess.run()` when you want to wait for the process to finish and collect all output at once.

```python
import subprocess

result = subprocess.run(
    ["ping", "8.8.8.8", "-c", "4"],
    capture_output=True,   # captures both stdout and stderr
    text=True              # decodes bytes to str automatically
)

print(result.stdout)       # stdout as a string
print(result.stderr)       # stderr as a string
print(result.returncode)   # exit code
```

---

### Stream Output in Real Time

Use `subprocess.Popen()` when you need to process output line-by-line as the process runs.

```python
import subprocess

process = subprocess.Popen(
    ["ping", "8.8.8.8"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

for line in process.stdout:
    print(f"[OUT] {line}", end="")

process.wait()

for line in process.stderr:
    print(f"[ERR] {line}", end="")
```

---

### Merge stderr into stdout

```python
result = subprocess.run(
    ["mycommand"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,  # redirect stderr into stdout stream
    text=True
)
print(result.stdout)
```

---

## C#

Uses `System.Diagnostics.Process` with `ProcessStartInfo` to redirect streams.

### Capture Output After Process Completes

```csharp
using System.Diagnostics;

var process = new Process
{
    StartInfo = new ProcessStartInfo
    {
        FileName = "ping",
        Arguments = "8.8.8.8",
        RedirectStandardOutput = true,  // capture stdout
        RedirectStandardError = true,   // capture stderr
        UseShellExecute = false,        // required for redirection
        CreateNoWindow = true
    }
};

process.Start();

string stdout = process.StandardOutput.ReadToEnd();
string stderr = process.StandardError.ReadToEnd();

process.WaitForExit();

Console.WriteLine($"STDOUT:\n{stdout}");
Console.WriteLine($"STDERR:\n{stderr}");
Console.WriteLine($"Exit code: {process.ExitCode}");
```

> [!warning] Deadlock Risk Calling `ReadToEnd()` on stdout and then stderr **sequentially** can deadlock if the process fills the stderr buffer before you read it. Always read both streams **concurrently**.

---

### Async Read to Avoid Deadlocks (Recommended)

```csharp
process.Start();

// Read both streams concurrently
var stdoutTask = process.StandardOutput.ReadToEndAsync();
var stderrTask = process.StandardError.ReadToEndAsync();

process.WaitForExit();

string stdout = await stdoutTask;
string stderr = await stderrTask;
```

---

### Stream Output in Real Time Using Events

Best pattern for long-running processes. Mirrors the Python `Popen` approach.

```csharp
var process = new Process
{
    StartInfo = new ProcessStartInfo
    {
        FileName = "ping",
        Arguments = "8.8.8.8",
        RedirectStandardOutput = true,
        RedirectStandardError = true,
        UseShellExecute = false,
        CreateNoWindow = true
    },
    EnableRaisingEvents = true
};

process.OutputDataReceived += (sender, e) =>
{
    if (e.Data != null)
        Console.WriteLine($"[OUT] {e.Data}");
};

process.ErrorDataReceived += (sender, e) =>
{
    if (e.Data != null)
        Console.WriteLine($"[ERR] {e.Data}");
};

process.Start();
process.BeginOutputReadLine();   // start async stdout reading
process.BeginErrorReadLine();    // start async stderr reading

process.WaitForExit();
```

---

### Writing to Your Own Process Streams

```csharp
Console.Out.WriteLine("This goes to stdout");
Console.Error.WriteLine("This goes to stderr");
```

### Redirect Your Own App's Output

```csharp
using var writer = new StreamWriter("output.log");
Console.SetOut(writer);    // redirect stdout
Console.SetError(writer);  // redirect stderr

Console.WriteLine("This now goes to output.log");
```

---

## Quick Comparison

|Task|Python|C#|
|---|---|---|
|Write to stdout|`print()` or `sys.stdout.write()`|`Console.WriteLine()`|
|Write to stderr|`print(..., file=sys.stderr)`|`Console.Error.WriteLine()`|
|Capture child process|`subprocess.run(capture_output=True)`|`ProcessStartInfo` + `RedirectStandard*`|
|Stream in real time|`Popen` + iterate `stdout`|`OutputDataReceived` event|
|Merge stderr → stdout|`stderr=subprocess.STDOUT`|Read both async / manual merge|
|Avoid deadlocks|Not usually an issue|Use `ReadToEndAsync()` concurrently|

---

## Notes

- The C# async/event pattern maps well to Azure SDK streaming patterns (Durable Functions, Service Bus message processing).
- `UseShellExecute = false` is **required** in C# whenever you redirect streams — forgetting this is a common gotcha.
- In Python, `text=True` on `subprocess.run()` saves you from manually decoding bytes — always include it unless you need raw bytes.
- The `EnableRaisingEvents = true` flag in C# must be set **before** calling `process.Start()`.