# BJJ Platform Roadmap

## Vision

Build the ultimate platform for Brazilian Jiu-Jitsu practitioners, gyms, and coaches.

The platform starts as a personal training and competition tracker and evolves into:

- Match Vault
- OpenMat Finder
- Seminar Marketplace
- Coach Marketplace
- Gym Management Platform
- BJJ Streaming Platform

Long term vision:

"The Operating System of the BJJ Community"

---

# Phase 1 - Foundation (BUILDING NOW)

Goal:
Create a usable product for athletes.

## Features

### User Accounts

- Registration
- Login
- OAuth (Google, Apple)
- User Profile

### Athlete Profile

- Name
- Belt
- Weight Class
- Academy
- Country

### Training Journal

- Date
- Gi / No-Gi
- Techniques Practiced
- Training Notes

### Competition Journal

- Tournament
- Opponent
- Result
- Video Link
- Notes

---

## Architecture (cost-minimized for Azure Free Tier / low-spend real build)

Frontend

- React

Backend

- APIM (Consumption tier — pay-per-call, near-zero cost at low volume)
- AKS (single Standard_B2s node, stop/start when idle to avoid compute charges)
- Azure SQL (free tier: 100K vCore-seconds + 32GB storage/month, forever free, one per subscription)

Infrastructure

- Bicep
- GitHub Actions
- Azure Container Registry (Basic tier)

Observability

- Application Insights (free up to 5GB ingestion/month)

---

# Phase 2 - Match Vault

Goal:
Allow athletes to securely store and share competition videos.

## Features

### Video Upload

Upload competition footage.

### Share Links

Example:

https://platform.com/match/1234

Share via:

- WhatsApp
- Instagram
- Discord
- Email

### Match Metadata

- Tournament
- Opponent
- Result
- Rule Set
- Gi/No-Gi

---

## Architecture

Storage

- Azure Blob Storage

Processing

- Event Grid
- Azure Functions

Video Services

- Thumbnail Generation
- Preview Generation

---

# Phase 3 - AI Fight Journal

Goal:
Provide insights on competition performance.

## Features

### Fight Notes

Users document:

- Mistakes
- Successes
- Strategies

### AI Coach

Questions:

- What are my recurring mistakes?
- Which submissions work best?
- Which positions need improvement?

---

## Architecture

- Azure OpenAI
- Azure AI Search
- APIM
- AKS

---

# Phase 4 - OpenMat Finder

Goal:
Help athletes discover training opportunities.

## Features

### Map

Display:

- Open Mats
- Academies
- Seminars

### Filters

- Distance
- Gi
- No-Gi
- Free
- Paid

### Attendance

Users can:

- Join
- Cancel
- Follow

---

## Architecture

- Maps API
- Redis Cache
- OpenMat Service

---

# Phase 5 - OpenMat Booking

Goal:
Allow gyms to manage attendance.

## Features

### Reservation System

Users reserve spots.

### Attendance Tracking

Gym owners see:

- Registered Athletes
- Remaining Capacity

### Payment Options

Option A: Pay at gym
Option B: Pay online

---

## Revenue

Commission per booking.

Example: 10€ → 9€ Gym / 1€ Platform

---

# Phase 6 - Seminar Marketplace

Goal:
Become the easiest way to organize seminars.

## Features

### Seminar Listings

- Instructor
- Date
- Capacity
- Pricing

### Online Payments

Powered by Stripe.

### QR Check-In

Generate ticket. Scan on arrival.

---

## Revenue

Commission on registrations.

---

# Phase 7 - Gym Portal

Goal:
Create value for academy owners.

## Features

### Academy Profile

- Photos
- Classes
- Schedule

### OpenMat Management

Create events. Track attendance.

### Analytics

- Visitors
- Registrations
- Revenue

---

# Phase 8 - Coach Portal

Goal:
Give instructors professional tools.

## Features

### Coach Profile

- Biography
- Seminars
- Experience

### Private Lessons

Booking system.

### Content Publishing

Publish instructional content.

---

# Phase 9 - Video Marketplace

Goal:
Enable coaches to monetize content.

## Features

### Course Creation

Upload:

- Series
- Modules
- Lessons

### Pricing

- One-time payment
- Bundle
- Subscription

### Revenue Sharing

Platform commission on sales.

---

# Phase 10 - BJJ Streaming Platform

Goal:
Create the Netflix of BJJ.

## Features

### On-Demand Learning

Watch:

- Courses
- Seminars
- Academy Content

### Smart Recommendations

Recommend content based on:

- Belt
- Weight Class
- Gi/No-Gi

### Multi-Device

- Mobile
- Tablet
- TV

---

# Phase 11 - Competition Ecosystem

Goal:
Integrate tournaments and rankings.

## Features

### Tournament Discovery

Find events nearby.

### Registration

Register directly.

### Rankings

Personal ranking history.

### External Integrations

Potential:

- Smoothcomp
- IBJJF
- ADCC

---

# Phase 12 - Multi-Tenant SaaS

Goal:
Provide an operating platform for academies.

## Features

### Academy Management

- Members
- Billing
- Events
- Courses

### Revenue

Monthly Subscription

Examples: Starter / Professional / Enterprise

---

# Technical Roadmap

## Learn AZ-305

Phase 1-3

- APIM
- AKS
- Azure SQL
- AI Search
- Azure OpenAI

## Learn Event-Driven Architecture

Phase 2-6

- Event Grid
- Service Bus
- Azure Functions

## Learn Networking

Phase 6-12

- Application Gateway
- WAF
- Private Endpoints
- Hub & Spoke

## Learn SaaS Architecture

Phase 7-12

- Multi-Tenant Design
- Identity
- RBAC
- Subscription Management

---

# First Revenue Goal

OpenMat Booking

Commission: 1€ per registration

Example: 1000 registrations/month = 1000€/month without subscriptions.

---

# Ultimate Goal

The global platform where athletes:

- Train
- Compete
- Learn
- Share videos
- Discover gyms
- Join seminars

while gyms and coaches monetize their expertise.
