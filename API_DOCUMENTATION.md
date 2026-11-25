# API

- POST /api/auth/register
- POST /api/auth/login
- GET /api/auth/me
- GET /api/profile
- PUT /api/profile
- GET /api/careers
- GET /api/assessment/questions
- POST /api/assessment/submit
- GET /api/assessment/history
- POST /api/roadmap/generate
- GET /api/roadmap
- GET /api/roadmap/{id}
- POST /api/roadmap/regenerate
- GET /api/resources
- GET /api/resources/recommended
- POST /api/resources/save
- GET /api/progress/dashboard
- POST /api/progress/topic
- GET /api/milestones
- POST /api/milestones
- PUT /api/milestones/{id}
- GET /api/study-sessions
- POST /api/study-sessions
- PUT /api/study-sessions/{id}
- DELETE /api/study-sessions/{id}

Protected endpoints require `Authorization: Bearer <JWT>`.

`GET /api/roadmap` accepts an optional `career_goal` query parameter to load that career's saved roadmap and topic progress, for example `/api/roadmap?career_goal=Data%20Scientist`. Without it, the currently selected profile career is used.

`POST /api/roadmap/generate` accepts an optional JSON `career_goal` field. If omitted, the profile's selected career is used. Existing roadmaps are reused only when their phases and topics match the current career plan.
