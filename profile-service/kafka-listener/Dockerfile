# === Stage 1: Build the application ===
FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /app

# Copy gradle wrapper files to leverage Docker layer caching
COPY gradle/ gradle/
COPY gradlew build.gradle settings.gradle ./
# For Kotlin DSL projects, uncomment the next line:
# COPY gradlew build.gradle.kts settings.gradle.kts ./

# Download dependencies (cached unless build files change)
RUN ./gradlew dependencies --no-daemon

# Copy source code and build the package
COPY src ./src
RUN ./gradlew bootJar -x test --no-daemon

# === Stage 2: Create the runtime image ===
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

# Create a non-root user for security
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring

# Copy only the executable bootJar from the builder stage
COPY --from=builder /app/build/libs/*.jar app.jar

# Expose the default Spring Boot port
EXPOSE 8080

# Run the application with optimized memory settings
ENTRYPOINT ["java", "-XX:+UseG1GC", "-jar", "app.jar"]
