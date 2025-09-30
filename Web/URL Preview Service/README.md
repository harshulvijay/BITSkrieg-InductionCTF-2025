# URL Preview Service

## Challenge Description

Our URL preview service blocks localhost and private IPs for security. Find a way to bypass these protections and retrieve the flag.

**Challenge URL:** `http://localhost:3000`  
**Difficulty:** Medium  
**Category:** Web  
**Points:** 150

---

## Writeup

### Overview

This SSRF challenge requires accessing an internal flag service on `localhost:5001` through a web application with URL filtering.

## Solution

The application blocks direct access to localhost but allows HTTP redirects. Use this payload to bypass the protection:

```
http://httpbin.org/redirect-to?url=http://localhost:5001/flag
```

## How it Works

1. The app validates `httpbin.org` (allowed domain)
2. httpbin.org redirects to `localhost:5001/flag`
3. The app follows the redirect and retrieves the flag

## Steps

1. Run `docker-compose up`
2. Go to `http://localhost:3000`
3. Enter the payload URL and submit
4. Get the flag!
