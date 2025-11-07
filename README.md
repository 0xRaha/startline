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


## 🧩 Planned Features
- [ ] Simple routing system
- [ ] HTTP request parsing (method, path, headers)  
- [ ] `App` class to register and serve routes  
- [ ] Basic `Request` and `Response` classes  
- [ ] Static file serving  
- [ ] Threaded server mode  

---

> _Startline: every journey begins somewhere._
