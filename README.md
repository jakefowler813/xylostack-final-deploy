# XyloStack: The Visual Music Engine

**Live Site:** [https://finalproject.jakef.tech](https://finalproject.jakef.tech)  
**Author:** Jake Fowler (JMU Computer Science, Class of 2026)

XyloStack is a full-stack musical application designed to bridge the gap between sheet music and visual learning. By allowing users to map specific musical pitches to custom color schemes, the platform provides an intuitive, color-coded interface for learning and playing melodies.

---

## 🚀 Key Features & Technical Claims

### 1. Multi-User CRUD Architecture

* **Instrument Stacks:** Users can create, edit, and delete custom "Instrument Stacks".
* **User-Generated Content (UGC):** Logged-in users can compose and save their own songs using a custom JSON-based note sequence system.
* **Object-Level Permissions:** Implemented strict backend logic to ensure users can only edit or delete their own data, while maintaining read-access to "Universal" admin-provided content.

### 2. State-Persistent Navigation System

* **Navigation Loop Resolution:** Solved the UX challenge of bridging instrument selection and song playback. By passing `stack_id` parameters through the URL, the application maintains the selected instrument context while browsing the song library.

### 3. RESTful Web Service (API)

* **List Endpoint (`/api/songs/`):** A public-facing JSON API that exposes the community song library for external consumption.
* **Detail Endpoint (`/api/songs/<id>/`):** A granular data resource for individual song parameters, including Title, BPM, and the raw Note Sequence.
* **JSON Serialization:** Song data is stored and served using standardized JSON arrays to ensure compatibility with modern performance tools.

### 4. Search & Discovery Engine

* **Dynamic Filtering:** A built-in search engine that filters the community library by song title while preserving the selected instrument context.
* **Visibility Control:** A "Public/Private" toggle system allowing users to keep compositions personal or contribute them to the global community library and API.

---

## Technical Stack

* **Backend:** Python 3.12, Django 5.x
* **Database:** PostgreSQL (Production), SQLite (Local Development)
* **Frontend:** Bootstrap 5, Custom CSS3, JavaScript (DOM & Clipboard API)
* **Deployment:** DigitalOcean App Platform
* **Production Tools:** Gunicorn, WhiteNoise (Static File Management), Environment Variables for Secret Key management.

---

## Project Architecture

* **InstrumentStack:** Linked to a `User` (Owner) and contains a collection of `XyloKey` objects.
* **XyloKey:** Defines the relationship between a musical pitch (e.g., C4), a hex color code, and its display order.
* **Song:** Stores musical metadata and the JSON-formatted `note_sequence`. Links to an optional `Author` and uses a visibility boolean for library inclusion.

---

## Security & Best Practices

* **CSRF Protection:** Integrated Django CSRF tokens for all state-changing forms.
* **Secure Deployment:** `DEBUG` mode is disabled in production. Sensitive credentials (SECRET_KEY, DATABASE_URL) are handled via server-side environment variables.
* **Defensive Design:** Implemented "Confirm Deletion" screens and server-side validation to prevent accidental data loss or unauthorized URL manipulation.

---

## Installation & Local Development

1. **Clone the repository:**

    ```bash
    git clone https://github.com/347s26/347s26-final-project-team-jake.git
    cd 347s26-final-project-team-jake
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

## Future Goals

* **MIDI Support:** Allow users to play their custom stacks using external MIDI controllers.
* **Social Sharing:** Implementation of public/private toggles for song sequences to allow community collaboration.
* **WAV Export:** Enable users to export their recorded sequences as high-quality audio files.
