# FleetFlow --- Fleet Management System

FleetFlow is a high‑performance fleet management system built using
**FastAPI, PostgreSQL, and HTML**.\
It enables efficient management of vehicles, drivers, and fleet
operations through a clean and scalable backend architecture.

Built for the **Odoo Hackathon**, with emphasis on performance,
scalability, and clean engineering practices.

------------------------------------------------------------------------

# Architecture

Client (HTML Interface)\
↓\
FastAPI Backend\
↓\
PostgreSQL Database

------------------------------------------------------------------------

# Features

## Core Features

-   Vehicle management
-   Driver management
-   Trip tracking
-   Fleet operational monitoring

## Backend Engineering

-   FastAPI REST API
-   PostgreSQL database integration
-   SQLAlchemy ORM
-   Connection pooling
-   Environment‑based configuration

## System Design

-   Scalable backend architecture
-   Clean separation of concerns
-   Production‑ready structure

------------------------------------------------------------------------

# Tech Stack

Backend: - FastAPI - PostgreSQL - SQLAlchemy - Python

Frontend: - HTML - CSS

Deployment: - Render / Railway / VPS ready

------------------------------------------------------------------------

# Project Structure

    FleetFlow-OdooHackathon/
    │
    ├── main.py
    ├── database.py
    ├── requirements.txt
    ├── procfile.txt
    │
    ├── templates/
    │   └── index.html
    │
    ├── static/
    │
    ├── .env.example
    └── README.md

------------------------------------------------------------------------

# Setup Instructions

## 1. Clone repository

    git clone https://github.com/Sansfear87/FleetFlow-OdooHackathon.git
    cd FleetFlow-OdooHackathon

## 2. Create virtual environment

Windows:

    python -m venv venv
    venv\Scripts\activate

Linux / Mac:

    python -m venv venv
    source venv/bin/activate

## 3. Install dependencies

    pip install -r requirements.txt

## 4. Configure environment

Create `.env` file:

    DATABASE_URL=postgresql://username:password@localhost:5432/fleetflow

## 5. Run server

    uvicorn main:app --reload

Open browser:

    http://127.0.0.1:8000

------------------------------------------------------------------------

# API Documentation

Swagger UI:

    http://127.0.0.1:8000/docs

------------------------------------------------------------------------

# Hackathon Objective

FleetFlow demonstrates:

-   Backend engineering capability
-   Database design skills
-   Production‑ready architecture
-   Clean API implementation

------------------------------------------------------------------------

# Author

Amir\
Odoo Hackathon Participant\
GitHub: https://github.com/Sansfear87

------------------------------------------------------------------------

# License

MIT License
