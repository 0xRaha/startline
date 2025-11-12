# 🏁 Startline

**Startline** is a minimal, educational web framework built from scratch in Python, inspired by Flask’s simplicity.  
It’s currently in active development and being developed solo as a foundation for a future hybrid Python + Rust framework.

The main goal right now is to:
- Learn how web frameworks work under the hood  
- Build every core part (routing, request/response handling, server loop) **from scratch** using Python’s standard library  
- Prepare the project for a **Rust-powered core** later, allowing it to handle **far more concurrent users** while keeping the **same simplicity and developer experience**


## Vision
Startline aims to become:
- **Lightweight** – no external dependencies, only the Python standard library  
- **Educational** – readable, simple, and ideal for learning framework internals  
- **High-Performance** – future integration with **Rust** (via PyO3) for concurrency and system-level speed  

I plan to gradually move performance-critical parts (like the HTTP server and router) to Rust once the Python version is stable


## Roadmap


### Core Foundations
- [x] Implement basic HTTP server using Python's socket module  
- [x] Add request parsing (method, path, headers, body)  
- [x] Create Request and Response classes  
- [x] Build simple routing system  
- [x] Implement App class to manage routes and run the server  
- [ ] Add error handling (404, 500 responses)  
- [ ] Add URL parameters and dynamic routing (`/user/<id>`)  
- [ ] Implement middleware system (before and after request)  

### Core Features
- [ ] Support static file serving (HTML, CSS, JS)  
- [ ] Add configuration system (debug, port, host, etc.)  
- [ ] Add logging (access logs, error logs, timestamps)  
- [ ] Add colorized console output for requests (status, path, method)  
- [ ] Add simple debugger/error page in debug mode  
- [ ] Add threaded server mode (handle multiple requests concurrently)  
- [ ] Implement keep-alive and connection reuse  
- [ ] Implement templating support  
- [ ] Implement sessions and cookies  

### Developer Experience & Optimization
- [ ] Write basic examples and tests  
- [ ] Measure and optimize request handling speed  
- [ ] Add simple benchmark script  
- [ ] Add CLI tool  
- [ ] Document core API (App, Router, Request, Response, ServerInterface)  
- [ ] Add contribution guide  

---

> _Startline: every journey begins somewhere._
