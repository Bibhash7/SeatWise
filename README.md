# SeatWise
This web application is designed to allocate seats for candidates based on their preferences for exam centers, ensuring an optimal distribution across multiple centers. The application is built with **Django Rest Framework, PostgreSQL, Pandas** for data processing, and **Docker** for containerization. **Redis queues** are used to handle background tasks, ensuring smooth and efficient backend processing. Additionally, **Swagger UI** is integrated for API documentation and testing.

## Features
- **Optimal Seat Allocation:** Allocates exam seats based on students' preferences for exam centers, ensuring efficient use of available resources.
- **RESTful API:** Built with Django Rest Framework to provide a robust and flexible API for managing exam centers, candidates, and seat allocations.
- **Custom Management Commands:** Includes a custom Django command to automate the creation of a superuser, simplifying the setup process.
- **Dockerized Deployment:** The entire application is containerized using Docker, making it easy to deploy and scale.
- **Django Redis Queue:** Background task processing using django_rq and Redis for handling heavy computations asynchronously.
- **Swagger UI:** Integrated for interactive API documentation and testing.

## Docker Image
https://hub.docker.com/repository/docker/tarbi/seatwise/general

## Data Model
[![Seat-Wise-DFD.png](https://i.postimg.cc/3w3Mz2Fm/Seat-Wise-DFD.png)](https://postimg.cc/Xr1DCGhY)

## Project Structure

```plaintext
├── config/
│   ├── settings.py                          # Django settings file
│   ├── urls.py                              # URL routing for the application
│   ├── wsgi.py                              # WSGI entry point for the application
│   ├── asgi.py                              # ASGI entry point for the application
│   └── ...
├── exam_allocation/
|   ├── utils/
|   |   ├── groupify.py                      # Group stuends according to exam center choice and join with exam center for processing
|   ├── tasks/
|   |   ├── process_allocation_in_queue.py   # process the allocation in background on django redis queue.
|   ├── management
|   |   ├── commands
|   |   |   ├── __init__.py
|   |   |   ├── custom_superuser.py          # Create custom superuser upon docker compose up
|   ├── migrations
|   |   ├── __init__.py
|   |   ├── 0001_initial.py                  # Initial migration file
│   ├── models.py                            # Django models for Exam, ExamCenter, Student, and Allocation
│   ├── views.py                             # Views and business logic for seat allocation
│   ├── constants.py                         # Predefined constants for readability and better scalability
│   └── ...
├── Dockerfile                               # Dockerfile for containerizing the application
├── docker-compose.yml                       # Docker Compose file for setting up development and production environments
└── README.md                                # Project documentation
```

## API Endpoints
- **GET/admin:** For CRUD operation on Exam, Student, ExamCenter.
- **POST/generate-allocation:** For generate the allocation that will be stored in Allocation table.
- **GET/get-task-status/:** For check the task status

## Sceenshots
- **Exams**
  
[![Seat-Wise-1.png](https://i.postimg.cc/vHSsK0Pn/Seat-Wise-1.png)](https://postimg.cc/VdMprWPs)
- **Exam Center**

[![Seat-Wise-2.png](https://i.postimg.cc/HWZRWVQD/Seat-Wise-2.png)](https://postimg.cc/PND22f32)
- **Students**
  
[![Seat-Wise-3.png](https://i.postimg.cc/k52DZVFJ/Seat-Wise-3.png)](https://postimg.cc/p9t25L64)
- **API call via Postman**
  
[![Seat-Wise-7.png](https://i.postimg.cc/kgW5b5vF/Seat-Wise-7.png)](https://postimg.cc/218mprJV)
- **Seat Allocation View**
  
[![Seat-Wise-4.png](https://i.postimg.cc/j2phw0xN/Seat-Wise-4.png)](https://postimg.cc/7JNzdRTY)
- **Django Redis Queue**

[![Seat-Wise-6.png](https://i.postimg.cc/BbtWch9f/Seat-Wise-6.png)](https://postimg.cc/ctq5dBLF)
- **Swagger UI**

[![Seat-Wise-8.png](https://i.postimg.cc/PrQwgKBk/Seat-Wise-8.png)](https://postimg.cc/bsdrb0y6)

## Test Case Coverage Report: 92% code coverage

- [![Seat-Wise-5.png](https://i.postimg.cc/fW2wV9Pw/Seat-Wise-5.png)](https://postimg.cc/Z0NkgCZg)

