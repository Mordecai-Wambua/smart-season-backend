# SmartSeason Field Monitoring System (Backend API)
A robust, RESTful API built to track crop progress across multiple fields during a growing season.
Designed with a clean, decoupled architecture to support modern frontends, the system features strict role-based data isolation, secure JWT authentication, and dynamic status computation.

## Tech Stack
- Framework: Django 5.x & Django REST Framework (DRF)
- Database: PostgreSQL
- Authentication: Djoser & SimpleJWT (Stateless JSON Web Tokens)
- Package Manager: uv
- Documentation: OpenAPI 3.0 via drf-spectacular

## Setup Instructions
### Prerequisites
- uv installed
- postgresql db installed


### 1. Clone & Environment Setup
Clone the repository and navigate into the backend directory:

``` Bash
git clone https://github.com/Mordecai-Wambua/smart-season-backend
cd smartseason-backend
```

Create a .env file in the root directory and add the following configuration:

```Code snippet
DEBUG=True
SECRET_KEY=your-secure-development-key
DATABASE_URL=postgres://postgres:postgrespassword@127.0.0.1:5432/smartseason
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### 2. Database Initialization
Spin up the PostgreSQL database

### 3. Install Dependencies & Migrate
Initialize the virtual environment, install packages, and apply migrations:

```Bash
uv sync
python manage.py migrate
```

### 4. Run the Application
Start the development server:

```Bash
python manage.py runserver
```

The API will be available at http://localhost:8000.

You can view the interactive Swagger API documentation at http://localhost:8000/api/docs/.

### Demo Credentials
To test the role-based isolation, you can use the following pre-configured accounts (or create your own via the /api/auth/users/ endpoint):
```
Admin (Coordinator)
Username: admin_demo
Password: securepassword123

Field Agent
Username: agent_demo
Password: securepassword123
```

## Design Decisions
- Decoupled Architecture:
  - Built as a pure, headless REST API to seamlessly integrate with modern SSR/SSG frontends (e.g., Next.js).
  - CORS is pre-configured for local frontend development.

- Stateless Authentication:
  - Implemented JWTs via Djoser to handle user identity securely without relying on server-side session overhead.

- Strict Data Isolation:
  - Object-level permissions and overridden get_queryset() methods ensure Field Agents can physically only query, view, and update fields explicitly assigned to them, while Admins retain global oversight.

- Dynamic Status Computation:
  - Instead of storing potentially stale status strings in the database, the status (Active, At Risk, Completed) is computed dynamically via a Python @property upon serialization, driven by the field's lifecycle stage and the nature of its most recent update.

- Automated API Documentation:
  - Integrated drf-spectacular to automatically generate an interactive OpenAPI Swagger UI, ensuring frontend integration is frictionless.

## Assumptions Made
1. Deferred Assignment: Admins can create a field without immediately assigning an agent (agent=null). This accommodates real-world planning phases where fields are mapped out before seasonal staff are hired.
2. The "At Risk" Heuristic: A field is flagged as "At Risk" if the most recent observation (FieldUpdate) is marked as an issue by an agent. If a subsequent update is posted without an issue flag, the field naturally returns to an "Active" status.
3. Frontend Password Validation: The API does not require password confirmation (re_password) during registration, operating under the assumption that the decoupled frontend handles basic UX form validation prior to submission.
4. Role Immutability via REST: Field Agents cannot promote themselves. The role field is strictly read-only on the /users/me/ endpoint to prevent privilege escalation.