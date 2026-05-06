# Xylostack: A Full-Stack Digital Instrument & Library

**Live Project:** [https://finalproject.jakef.tech](https://finalproject.jakef.tech)  
**Developer:** Jake Fowler  
**Institution:** James Madison University - Computer Science  
**Date:** May 2026

## Project Overview

Xylostack is a web-based digital instrument platform that allows users to design, play, and share custom xylophone "stacks." Users can map specific musical notes to visual interfaces, save unique instrument configurations, and build a library of melodic sequences stored in a production-grade database.

---

## Technical Claims & Evidence

### 1. Production-Grade Deployment & Infrastructure

* **Claim:** Successfully deployed a Django application to a cloud environment with custom domain mapping and SSL encryption.
* **Evidence:** The application is live at `finalproject.jakef.tech`. Infrastructure is managed via the **DigitalOcean App Platform**, utilizing Gunicorn as the WSGI server and WhiteNoise for efficient static file serving.

### 2. Relational Database Management (PostgreSQL)

* **Claim:** Migrated from a local development database (SQLite) to a managed production relational database, handling complex schema migrations and permission configurations.
* **Evidence:** Integrated a **Managed PostgreSQL** instance on DigitalOcean. Successfully executed remote migrations and handled Postgres 15+ schema permissioning (`GRANT ALL ON SCHEMA public`) to ensure data persistence for Users, Stacks, and Songs.

### 3. Full-Stack Data Modeling

* **Claim:** Designed and implemented a relational schema that supports custom instrument mapping and musical sequences.
* **Evidence:** * **InstrumentStack Model:** Stores custom note-to-color mappings (JSONField) and metadata.
  * **Song Model:** Utilizes JSON arrays to store melodic sequences, allowing for programmatic playback of user-generated content.
  * **User Relationship:** Implemented One-to-Many relationships allowing users to own and manage their personal library of instruments.

### 4. Advanced Security Configuration

* **Claim:** Implemented production-level security protocols to protect user data and server integrity.
* **Evidence:** * Configured `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` to prevent cross-site request forgery on the live domain.
  * Managed sensitive credentials (Secret Keys, Database URLs) via secure Environment Variables rather than hardcoding.
  * Toggled `DEBUG` mode to `False` in production to prevent sensitive traceback exposure.

### 5. Interactive Frontend & Audio Logic

* **Claim:** Developed a low-latency interactive interface for real-time audio playback based on dynamic database state.
* **Evidence:** The "Rainbow Octave" stack dynamically renders UI keys based on database-stored hex codes and note mappings, triggering high-fidelity audio samples via the browser's Web Audio API.

---

## Tech Stack

* **Backend:** Django (Python 3.12+)
* **Database:** PostgreSQL (Managed via DigitalOcean)
* **Frontend:** HTML5, CSS3, JavaScript (ES6+)
* **Hosting:** DigitalOcean App Platform
* **Static Assets:** WhiteNoise
* **Domain Management:** get.tech DNS with CNAME Aliasing

---

## Installation & Local Development

1. **Clone the repository:**

    ```bash
    git clone [https://github.com/](https://github.com/)[your-username]/xylostack.git
    cd xylostack
    ```

2. **Setup Virtual Environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Environment Variables:**
    Create a `.env` file in the root directory:

    ```env
    DJANGO_DEBUG=True
    DJANGO_SECRET_KEY=your-secret-key
    DATABASE_URL=postgres://user:password@localhost:5432/dbname
    ```

5. **Run Migrations and Server:**

    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

---

## Future Roadmap

* **MIDI Support:** Allow users to play their custom stacks using external MIDI controllers.
* **Social Sharing:** Implementation of public/private toggles for song sequences to allow community collaboration.
* **WAV Export:** Enable users to export their recorded sequences as high-quality audio files.
