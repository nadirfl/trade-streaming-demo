# Trade Streaming Demo

## Überblick

Dieses Projekt simuliert eine vereinfachte Event-Driven Data Pipeline für Trade Events.

Die Anwendung besteht aus einem Java Spring Producer, der Trade Events erzeugt und über Kafka veröffentlicht, einem Python Consumer, der die Events konsumiert und persistiert, sowie einer Data Pipeline, welche die Daten in Bronze-, Silver- und Gold-Layer transformiert.

### Architektur

```text
Spring Boot Producer
        │
        ▼
      Kafka
        │
        ▼
 Python Consumer
        │
        ▼
Bronze Layer (PostgreSQL)
        │
        ▼
Silver Layer (PostgreSQL)
        │
        ▼
Gold Layer (PostgreSQL)
```

---

# Setup

## Voraussetzungen

Folgende Software muss installiert sein:

### Docker Desktop

Wird verwendet für:

* Kafka Broker
* Kafka UI
* PostgreSQL

Je nach Sytem müssen folgende Schritte vorgängig durchgeführt werden:

1. Hardware-Virtualisierung im BIOS/UEFI aktivieren
   - Intel VT-x
   - AMD-V / SVM Mode

2. Windows Subsystem for Linux (WSL2) installieren

```powershell
wsl --install -d Ubuntu
```

3. Ubuntu initialisieren
    - Ubuntu einmal starten
    - Linux-Benutzer erstellen
4. Docker Desktop installieren
5. Docker Desktop starten

Bei Berechtigungsproblemen kann es erforderlich sein, Docker Desktop oder das Terminal als Administrator auszuführen.

### Java

Empfohlen:

* Java 21 oder neuer

Prüfen:

```bash
java -version
```

### Python

Empfohlen:

* Python 3.11+

Prüfen:

```bash
python --version
```

### Git

Optional zur Versionsverwaltung.

---

## Infrastruktur starten

Im Projektverzeichnis:

```bash
docker compose up -d
```

Dadurch werden gestartet:

* PostgreSQL
* Kafka
* Kafka UI

Prüfen:

```bash
docker ps
```

Kafka UI:

```text
http://localhost:8080
```

---

## Java Producer starten

```bash
cd producer-java
.\mvnw.cmd spring-boot:run
```

Der Producer erzeugt periodisch Dummy Trade Events und veröffentlicht diese in Kafka.

---

## Python Consumer starten

```bash
cd consumer-python
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1

python consumer.py
```

Der Consumer konsumiert Events aus Kafka und speichert diese im Bronze Layer.

---

## Bronze-to-Silver Pipeline ausführen

```bash
cd pipeline-python
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1

python bronze_to_silver.py
```

## Gold-Pipeline ausführen
```bash
cd pipeline-python
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1

python gold_pipeline.py
```

---

# Ports
- Kafka UI: http://localhost:8080
- Spring Producer: http://localhost:8081
- PostgreSQL: http://localhost:5432
- Kafka: http://localhost:9092

---

# Komponenten

## Kafka

Kafka dient als zentrales Messaging-System zwischen Producer und Consumer.

### Topic

```text
trade-events
```

Alle Trade Events werden in dieses Topic veröffentlicht.

---

## Spring Boot Producer

Verantwortlich für:

* Erzeugen von Dummy Trade Events
* Serialisierung als JSON
* Versand nach Kafka

Beispiel:

```json
{
  "eventId": "evt-123",
  "tradeId": "trd-456",
  "eventType": "NEW",
  "eventTimestamp": "2026-05-25T12:00:00Z",
  "quantity": 1000,
  "price": 99.5,
  "counterparty": "UBS",
  "instrument": "BOND-XS123",
  "currency": "CHF"
}
```

---

## Python Consumer

Verantwortlich für:

* Konsumieren von Kafka Events
* Speicherung der Rohdaten
* Persistierung im Bronze Layer

Der Consumer enthält bewusst keine fachliche Transformationslogik.

---

## Bronze Layer

Zweck:

Speicherung der unveränderten Rohdaten aus Kafka.

Eigenschaften:

* Vollständige Nachvollziehbarkeit
* Reprocessing möglich
* Original Events bleiben erhalten

---

## Silver Layer

Zweck:

Bereinigung und Validierung der Rohdaten.

Aufgaben:

* Feldvalidierung
* Datentyp-Konvertierung
* Fehlererkennung
* Deduplizierung

Die Silver-Tabelle enthält strukturierte und validierte Events.

---

## Gold Layer

Zweck:

Bereitstellung fachlich aufbereiteter Daten.

Eigenschaften:

* Ein Datensatz pro Trade
* Aktueller Trade-Zustand
* Tableau- und Reporting-fähig

Der Gold Layer stellt die konsumierbare Sicht für Analytics und Reporting dar.

---

# Datenfluss

1. Spring Boot erzeugt ein Trade Event.
2. Das Event wird an Kafka gesendet.
3. Der Python Consumer liest das Event.
4. Das Event wird im Bronze Layer gespeichert.
5. Die Pipeline transformiert Bronze nach Silver.
6. Silver wird zu Gold aggregiert.
7. Tableau kann auf den Gold Layer zugreifen.

---

# Aktueller Stand

Umgesetzt:

* Docker Infrastruktur
* Kafka
* Kafka UI
* PostgreSQL
* Spring Boot Producer
* Python Consumer
* Bronze Layer
* Silver Layer

Geplant:

* Gold Layer
* Automatisierte Pipeline-Ausführung
* Tableau Dashboard
* Monitoring
* Error Handling
* Schema Registry