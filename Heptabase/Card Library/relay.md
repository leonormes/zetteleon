# relay

Now, let's start PostgreSQL and RabbitMQ using Docker Compose. I'll modify the compose file to include PostgreSQL:
Let's try starting the services with the explicit compose file:
I'll create a clean checklist of steps to get Relay running locally for the Bunny-Hutch application:

## Prerequisites

- 

- 

## Setup Steps

1. Create Working Directory

```bash
mkdir -p relay && cd relay
```

1. Download Compose File

```bash
wget https://raw.githubusercontent.com/Health-Informatics-UoN/hutch/refs/heads/main/samples/Bunny/relay.compose.yml
```

1. Configure Services in `relay.compose.yml`:

   - 

      - Image: postgres:16

      - Port: 5432

      - Database: hutch-relay

      - Health check configured

   - 

      - Image: rabbitmq:3-management

      - Management port: 15672

   - 

      - Image: [ghcr.io/health-informatics-uon/hutch/relay:dev-latest](http://ghcr.io/health-informatics-uon/hutch/relay:dev-latest)

      - Ports: 8080, 8081

      - Database migrations enabled

      - Proper service dependencies

2. Configure Environment Variables:

   - 

   - 

   - 

   - 

3. Start Services

```bash
docker compose -f relay.compose.yml up -d
```

1. Create User for Bunny

```bash
docker exec -it hutch-relay-relay-1 dotnet Hutch.Relay.dll users add local-bunny
```

## Configuration Details

### Database Settings

```yaml
ConnectionStrings__Default: Server=postgres;Port=5432;Database=hutch-relay;User Id=postgres;Password=postgres
Database__ApplyMigrationsOnStartup: "true"
```

### RabbitMQ Settings

```yaml
RelayTaskQueue__ConnectionString: amqp://user:password@rabbitmq:5672
```

### Upstream Task API Settings

```yaml
UpstreamTaskApi__BaseUrl: http://localhost:8080
UpstreamTaskApi__Username: local-bunny
UpstreamTaskApi__Password: <generated_password>
UpstreamTaskApi__CollectionId: local-bunny
```

## Verification Steps

1. Check all services are running:

```bash
docker compose -f relay.compose.yml ps
```

1. Verify PostgreSQL is healthy:

   - Status should show "(healthy)"

   - Port 5432 should be accessible

2. Verify RabbitMQ is running:

   - Management interface available at <http://localhost:15672>

   - Default credentials: user/password

3. Verify Relay is operational:

   - Service should be running without restarts

   - Ports 8080 and 8081 should be accessible

This checklist provides a complete setup guide for running Relay locally, with all necessary configuration and verification steps.