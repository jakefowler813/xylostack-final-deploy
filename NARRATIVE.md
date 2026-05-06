# XyloStack: Project Plan

**Team Name:** team-jake  
**Student Name:** Jake Fowler

---

## Part 1: Project Narrative

### Purpose

XyloStack is a full-stack web application designed to solve a prevalent problem in beginner music education. Most entry-level percussion instruments, such as children's xylophones use color-coded keys to assist learners in identifying notes. However, the industry lacks a universal standard for these colors. For instance, a "C" key might be red on one brand’s model, but blue on an instrument from another manufacturer. This lack of standardization creates a significant barrier for beginners, as traditional sheet music or video tutorials often use color cues that do not match the student's specific instrument.

The main idea of XyloStack is to provide a platform where users can create a "digital twin" of their physical instrument. By allowing users to map specific colors to musical pitches, the application can dynamically render songs in a way that perfectly aligns with the user’s device. This is important because it reduces the effort required to find what key to hit next. By ensuring that the "yellow note" on the screen always corresponds to the "yellow key" in front of the learner, XyloStack makes practicing immediate and accessible for young children, neurodivergent learners, and hobbyists alike.

### Users

The application is designed for two primary user groups: **Music Educators/Parents (Creators)** and **Beginning Learners (Players)**.

**Creators** are the "administrators" of the learning experience. They typically have a basic understanding of music and a desire to facilitate learning for others. Their primary background involves managing resources, whether in a formal classroom setting or at home. These users need a way to build, save, and manage custom instrument configurations (which we call "Stacks"). XyloStack benefits these users by automating a task they currently have to do manually: re-coloring or labeling sheet music by hand to match a child's toy. The app allows them to set up a profile once and apply it to an entire library of songs, significantly improving their instructional efficiency and allowing for a more personalized teaching approach for every student in a diverse classroom.

**Players** are the ones actually hitting the keys. Their background is usually "novice," and they may not have any prior experience with music theory or traditional notation. Their primary need is a clean, intuitive interface that provides immediate, accurate visual instructions. XyloStack improves their experience by eliminating the frustration of "wrong-color" cues. This creates a positive feedback loop where the learner can successfully play a melody on their first try, building the musical confidence necessary for long-term engagement. This accessibility is particularly impactful for those with learning differences who may find traditional black-and-white sheet music overwhelming or inaccessible.

### Features

The core functionalities of XyloStack center on the **Instrument Stack-Builder** and the **Dynamic Visual Player**.

The **Stack-Builder** is the primary CRUD interface for authenticated users. Users can create a new digital instrument by defining its "Stack." They specify the name of the stack, the number of keys (e.g., an 8-key or 12-key set), and use a color-picker to assign a hex code to specific musical pitches (e.g., C4, D4, E4). Because this data is persistent, users can update their Stack if they change instruments or delete it if it's no longer needed. This provides full control over their digital inventory.

The **Dynamic Visual Player** uses these custom Stacks to render music. When a user selects a song from the library, the application’s logic fetches the pitch data for that song and cross-references it with the user’s active Stack. For example, if a parent sets up a Stack where the note **"G"** is **Green**, and the student opens the song "Ode to Joy," every "G" note in the sequence will be automatically rendered as a green block. The interface will display a "falling note" visualization, similar to rhythm-based video games, where the colored blocks fall toward a baseline that represents the physical xylophone. This concrete visualization ensures that the student only needs to match the color on the screen to the color on their lap to play successfully.

### Data

XyloStack will manage four main types of data to facilitate the relationship between users, instruments, and music.

**Objects and Properties:**

* **User:** `username` (string), `email` (string), `role` (string: Admin/Member).
* **InstrumentStack:** `title` (string), `key_count` (integer), `owner_id` (Foreign Key to User).
* **XyloKey:** `pitch` (string, e.g., "C4"), `color_hex` (string/hex code), `order` (integer), `stack_id` (Foreign Key to InstrumentStack).
* **Song:** `title` (string), `tempo_bpm` (integer), `author_id` (Foreign Key to User).
* **Note:** `pitch` (string), `duration_ticks` (float), `sequence` (integer), `song_id` (Foreign Key to Song).

**CRUD Example:**
An authenticated user **Creates** an `InstrumentStack` titled "Hot Cross Buns" They then add several `XyloKey` objects (e.g., Pitch: "C4", Color: "#FF0000"). If the user later realizes they made a mistake or the physical key is actually orange, they can **Update** the `color_hex` property. If they stop using that instrument, they can **Delete** the Stack, which will cascade-delete the associated keys. Users can also **Read** their list of Stacks via a personalized dashboard.

**Relationships:**
The data follows a **One-to-Many** structure. One **User** can own multiple **InstrumentStacks**. One **InstrumentStack** contains many **XyloKeys**. One **Song** contains many **Notes**. This structure allows the application to overlay a specific Stack onto any Song in the database to generate a personalized view for the learner.
