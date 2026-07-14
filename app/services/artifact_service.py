from pathlib import Path

class ArtifactService:

    def save(self, artifacts, output_dir="generated"):

        Path(output_dir).mkdir(exist_ok=True)

        for artifact in artifacts:
            path = Path(output_dir) / artifact.filename

            with open(path, "w", encoding="utf-8") as f:
                f.write(artifact.content)