

## Usage
### Start Services
To start the services, use the following command:
```bash
docker-compose up
```

### Specify Profiles
To start services for a specific platform, use the `--profile` flag. Examples:
- For Linux:
  ```bash
  docker-compose --profile linux up
  ```
- For Windows:
  ```bash
  docker-compose --profile windows up
  ```
- For macOS:
  ```bash
  docker-compose --profile macos up
  ```

### Stop Services
To stop the services, use:
```bash
docker-compose down
```

---



