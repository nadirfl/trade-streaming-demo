Write-Host "Starting Docker containers..."
docker compose up -d

Write-Host "Containers:"
docker ps

Write-Host "Start Java producer manually with:"
Write-Host "cd producer-java"
Write-Host ".\mvnw.cmd spring-boot:run"

Write-Host "Start Python consumer manually with:"
Write-Host "cd consumer-python"
Write-Host "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass"
Write-Host ".\venv\Scripts\Activate.ps1"
Write-Host "python consumer.py"

Write-Host "Start Python Pipeline manually with:"
Write-Host "cd pipeline-python"
Write-Host "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass"
Write-Host ".\venv\Scripts\Activate.ps1"
Write-Host "python bronze_to_silver.py"
Write-Host "python gold_pipeline.py"

Write-Host "Query data in Docker Postgres DB with:"
Write-Host "docker exec -it trade-postgres psql -U trade_user -d trade_db"
Write-Host "SELECT * FROM bronze_trade_events;"
Write-Host "SELECT * FROM silver_trade_events;"
Write-Host "SELECT * FROM gold_trades;"
Write-Host "python gold_pipeline.py"