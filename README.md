# Restaurant Management System
[](https://github.com/mashakrot/database-project#restaurant-management-system)

## `Introduction`
[](https://github.com/mashakrot/database-project#introduction)

A restaurant management system made with **React**, **Flask**, and **PostgreSQL**. It provides a dashboard for managing restaurant reservations, inventory, suppliers, users and staff schedules. This project was made for university Database Systems course. 

1. [Tech Stack](https://github.com/mashakrot/database-project#tech-stack)
2. [Features](https://github.com/mashakrot/database-project#features)
3. [Project Structure](https://github.com/mashakrot/database-project#project-structure)
4. [Getting Started](https://github.com/mashakrot/database-project#getting-started)
5. [API Endpoints](https://github.com/mashakrot/database-project#api-endpoints)

## `Tech Stack`
[](https://github.com/mashakrot/database-project#tech-stack)

- React
- React Router
- Tailwind CSS
- Flask
- Flask-CORS
- PostgreSQL
- psycopg2

## `Features`
[](https://github.com/mashakrot/database-project#features)

👉 **Dashboard** – access the main tools from one place

👉 **Authentication** – sign in with an email and password using password hashes stored in PostgreSQL.

👉 **Reservations** – view restaurant reservations and their current status.

👉 **Inventory management** – check stock, change quantities, and find supplier information.

👉 **User management** – view, add, and delete restaurant users.

👉 **Staff schedules** – view and manage employee shifts, including their dates, times, and approval status.

## `Project Structure`
[](https://github.com/mashakrot/database-project#project-structure)

```text
.
├── app.py                         # Flask API
├── restaurant_db.sql              # PostgreSQL database dump
├── migration_add_password_hash.sql
├── package.json                   # Frontend and startup scripts
├── inventoryEnd.js                # Inventory page helper script
├── reservationsEnd.js             # Reservations page helper script
└── frontend/
    └── src/
        ├── components/            # Shared navigation components
        └── pages/                 # Login, dashboard, inventory, reservations, users, schedules
```

## `Getting Started`
[](https://github.com/mashakrot/database-project#getting-started)

### Prerequisites

- Python 3.9+
- Node.js and npm
- PostgreSQL

### 1. Install Python dependencies

From the project root, install the backend packages:

```bash
pip install flask psycopg2 flask-cors
```

### 2. Set up the database

Create a PostgreSQL database named `restaurant_db`, then restore the database dump:

```bash
createdb -U postgres restaurant_db
pg_restore -U postgres -d restaurant_db restaurant_db.sql
```

Add the password hash column required by login:

```bash
psql -U postgres -d restaurant_db -f migration_add_password_hash.sql
```

Update the PostgreSQL connection settings in `app.py` to match your local PostgreSQL username, password, host, and port.

### 3. Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

### 4. Start the application

From the project root:

```bash
npm run start
```

This starts the Flask API and the React development server. Open [http://localhost:3000](http://localhost:3000) in your browser.

The Flask API runs at [http://localhost:5000](http://localhost:5000).

## `API Endpoints`
[](https://github.com/mashakrot/database-project#api-endpoints)

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/login` | Authenticate a user |
| `POST` | `/get_inventory` | Retrieve inventory |
| `POST` | `/get_supplier_by_itemname` | Retrieve supplier details |
| `POST` | `/update_inventory` | Update an inventory quantity |
| `GET` | `/get_reservations` | Retrieve reservations |
| `GET` / `POST` | `/get_schedules` | Retrieve staff schedules |
| `POST` | `/add_shift` | Add a staff shift |
| `POST` | `/edit_shift` | Edit a staff shift |
| `GET` / `POST` | `/users` | Retrieve or create users |
| `DELETE` | `/users/<user_id>` | Delete a user |
